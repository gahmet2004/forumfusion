import sqlite3
import threading
import logging
import json
import time

import _libs.classes.User.User as User
import _libs.classes.User.Profile as Profile
import _libs.classes.User.Punishment as Punishment
import _libs.classes.User.Settings as UserSettings

import _libs.classes.System.Settings as Settings

import _libs.classes.Forum.Category as Category
import _libs.classes.Forum.Review as Review
import _libs.classes.Forum.SubCategory as SubCategory
import _libs.classes.Forum.Topic as Topic

import _libs.services._databaseRequests
import _libs.services._dictSerializer

import os.path as Path

class JsonManager:
    def __init__(self, json_file : str) -> None:
        self.file = json_file
        self.getData = self.checkExists(self.getData)
        return
    def checkExists(self, func):
        if Path.exists(self.file):
            return func
        self.writeData(_libs.services._databaseRequests._DEFAULT_JSON_SETTINGS)
        return func
    def writeData(self, data : dict) -> None:
        with open(self.file, "w") as writefile:
            json.dump(data, writefile)
    def getData(self) -> dict:
        with open(self.file) as readfile:
            return json.load(readfile)

class DatabaseManager:
    def __init__(self, db_name : str, logger : logging.Logger) -> None:
        """
        initialize the database manager for requests and commits.
        """
        self.connection = sqlite3.connect(
            db_name,
            check_same_thread = False,
            isolation_level = None
        )
        self.cursor = self.connection.cursor()
        self.locker = threading.Lock()
        self.logger = logger
        self.logger.info(f"Successfully connected to database '{db_name}'")
    def execute(
            self,
            request : str,
            type : str = 'run',
            parameters = ()
    ):
        """
        type : use 'run', 'script', 'one' or 'many', depending on what return you require.
        """
        resultset = None
        self.locker.acquire()
        try:
            if (type == "run"):
                resultset = self.cursor.execute(request, parameters)
                self.connection.commit()
            if (type == "script"):
                resultset = self.cursor.executescript(request)
                self.connection.commit()
            if (type == "fetchone"):
                self.cursor.execute(request, parameters)
                resultset = self.cursor.fetchone()
            if (type == "many"):
                self.cursor.execute(request, parameters)
                resultset = self.cursor.fetchmany()
        except Exception as e:
            self.logger.error(e)
        finally:
            self.locker.release()
        return resultset
class Database:
    def __init__(self, db_name : str, logger : logging.Logger):
        """
        get class of database to interact with stored data.
        """
        self.manager = DatabaseManager(db_name, logger)
        self.logger = logger
        self.logger.info(f"Instance of database started. Database {db_name}")
        self.__run__()
    def __run__(self):
        self.manager.execute(_libs.services._databaseRequests._DEFAULT_INIT, 'script')
        self.logger.info(f"Database attached successfully.")
    #
    #   USERS PART : USER
    #
    def userIsExist(
            self, 
            id : str = None, 
            tag : str = None
        ) -> bool:
        request = "SELECT * FROM `users_user` WHERE "
        if tag == None:
            request += "`id` = ?"
            params = (id,)
        else:
            request += "`tag` = ?"
            params = (tag,)
        response = self.manager.execute(
            request,
            'one',
            params
        )
        return response is None            
    def userGet(
            self, 
            id : str = None, 
            tag : str = None
        ) -> User.User:
        request = "SELECT * FROM `users_user` WHERE "
        if tag == None:
            request += "`id` = ?"
            params = (id,)
        else:
            request += "`tag` = ?"
            params = (tag,)
        response = self.manager.execute(
            request,
            'one',
            params
        )
        return User.User(
            int(response[0]),
            str(response[1]),
            str(response[2]),
            str(response[3]),
            str(response[4]),
            int(response[5]),
            int(response[6])
        )
    def userSet(self, id : int, var : str, val) -> None:
        self.manager.execute(
            "UPDATE `users_user` SET ? = ? WHERE `id` = ?",
            'run',
            (var, val, id)
        )
    def userAdd(
            self,
            tag : str,
            email : str,
            password : str,
            group : str,
            last_seen : int,
            registration : int
    ) -> User.User:
        data = self.manager.execute(
            "INSERT INTO `users_user` (`tag`, `email`, `password`, `group`, `last_seen`, `registration`) VALUES (?, ?, ?, ?, ?, ?)",
            'run',
            (tag, email, password, group, last_seen, registration)
        )
        return self.userGet(id = data.lastrowid)
    #
    #   USERS PART : PROFILE
    #
    def profileGet(
            self, 
            id : str = None
        ) -> Profile.Profile:
        response = self.manager.execute(
            "SELECT * FROM `users_profile` WHERE `id` = ?",
            'one',
            (id,)
        )
        return Profile.Profile(
            int(response[0]),
            str(response[1]),
            str(response[2]),
            str(response[4]),
            _libs.services._dictSerializer.listIdDeserialize(str(response[5])),
            _libs.services._dictSerializer.listIdDeserialize(str(response[6]))
        )
    def profileSet(
            self,
            id : int, 
            var : str, 
            val
        ) -> None:
        return self.manager.execute(
            "UPDATE `users_profile` SET ? = ? WHERE `id` = ?",
            'run',
            (var, val, id)
        )
    def profileAdd(
            self,
            id : int,
            name : str,
            avatar : str,
            about : str,
            subs : list,
            followers : list
    ) -> Profile.Profile:
        subs = _libs.services._dictSerializer.listIdSerialize(subs)
        followers = _libs.services._dictSerializer.listIdSerialize(followers)
        self.manager.execute(
            "INSERT INTO `users_profile` (`id`, `name`, `avatar`, `about`, `subs`, `followers`) VALUES (?, ?, ?, ?, ?, ?)",
            'run',
            (id, name, avatar, about, subs, followers)
        )
        return self.profileGet(id)
    #
    #   USERS PART : PUNISHMENT
    #
    def punishmentIsExist(
        self,
        id : int
    ) -> bool:
        response = self.manager.execute(
            "SELECT * FROM `users_punishment` WHERE `id` = ?",
            'one',
            (id,)
        )
        return len(response) != 0
    def punishmentGet(
            self,
            id : int = None
    ) -> Punishment.Punishment:
        response = self.manager.execute(
            "SELECT * FROM `users_punishment` WHERE `id` = ?",
            'one',
            (id,)
        )
        return Punishment.Punishment(
            int(response[0]),
            int(response[1]),
            int(response[2]),
            str(response[3]),
            int(response[4]),
            int(response[5])
        )
    def punishmentsOfUser(
            self,
            user_id : int,
            activeRequired : bool = False
    ) -> list:
        request = "SELECT `id` FROM `users_punishment` WHERE `user_id` = ?"
        args = list()
        args.append(user_id)
        if activeRequired:
            request += " AND `duration` + `issued_at` < ?"
            args.append(int(time.time()))
        response = self.manager.execute(
            request,
            'many',
            args
        )
        _return = list()
        for ans in response:
            _return.append(self.punishmentGet(ans[0]))
        return
    def punishmentsOfAdmin(
            self,
            admin_id : int
    ) -> list:
        response = self.manager.execute(
            "SELECT `id` FROM `users_punishment` WHERE `admin_id` = ?",
            "many",
            (admin_id,)
        )
        _return = list()
        for ans in response:
            _return.append(self.punishmentGet(ans[0]))
        return _return
    def punishmentSet(
        self,
        id : int,
        var : str,
        val
    ):
        return self.manager.execute(
            "UPDATE `users_punishment` SET ? = ? WHERE `id` = ?", 
            "run", 
            (var, val, id)
        )
    def punishmentAdd(
            self,
            user_id : int,
            admin_id : int,
            reason : str,
            duration : int,
            issued_at : int
    ) -> Punishment.Punishment:
        data = self.manager.execute(
            "INSERT INTO `users_punishment` (`user_id`, `admin_id`, `reason`, `duration`, `issued_at`) VALUES (?, ?, ?, ?, ?)",
            'run',
            (user_id, admin_id, reason, duration, issued_at)
        )
        return self.punishmentGet(data.lastrowid)
    #
    #   USERS PART : SETTINGS
    #
    def settingsGet(
        self,
        id : int
    ) -> UserSettings.Settings:
        response = self.manager.execute(
            "SELECT * FROM `users_settings` WHERE `id` = ?",
            'one',
            (id,)
        )
        return UserSettings.Settings(
            int(response[0]),
            bool(response[1]),
            bool(response[2]),
            bool(response[3]),
            bool(response[4]),
            bool(response[5])
        )
    def settingsSetBool(
        self,
        id : int,
        var : str,
        val : bool
    ):
        return self.manager.execute(
            "UPDATE `users_settings` SET ? = ? WHERE `id` = ?", 
            "run", 
            (var, int(val), id)
        )
    def settingsAdd(
        self,
        id : int,
        email_new_topic_event : bool,
        email_new_review_event : bool,
        email_follower_event : bool,
        email_broadcast : bool,
        hide_email : bool
    ):
        args = (
            id,
            int(email_new_topic_event),
            int(email_new_review_event),
            int(email_follower_event),
            int(email_broadcast),
            int(hide_email)
        )
        self.manager.execute(
            "INSERT INTO `users_settings` (`id`, `email_new_topic_event`, `email_new_review_event`, `email_follower_event`, `email_broadcast`, `hide_email`) VALUES (?, ?, ?, ?, ?, ?)",
            'run',
            args
        )
        return self.settingsGet(id)
    #
    #   FORUM PART : SETTINGS
    #
    