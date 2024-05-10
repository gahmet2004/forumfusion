import sqlite3
import threading
import logging

import User.User as User
import User.Profile as Profile
import User.Punishment as Punishment
import User.Settings as UserSettings

import System.Settings as Settings

import Forum.Category as Category
import Forum.Review as Review
import Forum.SubCategory as SubCategory
import Forum.Topic as Topic

from datetime import datetime

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
            type : str = 'run'
    ):
        """
        type : use 'run', 'one' or 'many', depending on what return you require.
        """
        resultset = None
        self.locker.acquire()
        try:
            if (type == "run"):
                self.cursor.execute(request)
                self.connection.commit()
            if (type == "fetchone"):
                self.cursor.execute(request)
                resultset = self.cursor.fetchone()
            if (type == "many"):
                self.cursor.execute(request)
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
        self.__initialize__()
    def __initialize__(self):
        from _libs.services._databaseRequests import _DEFAULT_INIT
        self.manager.execute(_DEFAULT_INIT)
        self.logger.info(f"Database attached successfully.")