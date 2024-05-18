import logging
import time
import flask
import secrets
import re

import _libs.classes.System.Database as Database
import _libs.classes.System.Settings as SysSettings
import _libs.classes.System.MailService as MailService

import _libs.services._passwordManager as PasswordManager
import _libs.services._mailTemplates as MailTemplates

from waitress import serve
from datetime import timedelta
from datetime import datetime
from flask import Flask
from urllib.parse import urlparse

engine = Flask(__name__)
engine.secret_key = secrets.token_hex(64)
logger = None
database = None
settings = None
mail_service = None
sessions = dict()
registrations = dict()
json_service = Database.JsonManager("_data/settings.json")

# =========================
# =       TECHNICAL       =
# =========================
def authRequired(func):
    def authCheck(*args, **kwargs):
        if settings.getPanelPass() == "notsetup":
            return flask.redirect("/install")
        if ("token" not in flask.session):
            return flask.redirect("/auth")
        if (flask.session["token"] not in sessions):
            return flask.redirect("/auth")
        return func(*args, **kwargs)
    authCheck.__name__ = func.__name__
    return authCheck
@engine.before_request
def before_request():
    flask.session.permanent = True
    flask.permanent_session_lifetime = timedelta(minutes=60)
@engine.route("/terms")
def terms():
    return settings.getTerms()
@engine.route("/contacts")
def contacts():
    return settings.getContacts()
@engine.template_filter('rutime')
def rutimer(s):
    return format(datetime.fromtimestamp(s), '%d.%m.%Y')

# =========================
# =      MAIN  PART       =
# =========================
@engine.route("/")
@authRequired
def root_manager():
    catlist = database.catGetAll()
    subcatdict = dict()
    user = database.userGet(sessions.get(flask.session["token"]))
    profile = database.profileGet(user.getID())
    for cat in catlist:
        subcatdict[cat.getID()] = database.subcatGetByCat(cat.getID())
    return flask.render_template(
        "forum.html",
        catlist = catlist,
        subcatdict = subcatdict,
        user = user,
        profile = profile
    )
@engine.route("/profile")
@authRequired
def profile():
    user = database.userGet(sessions.get(flask.session["token"]))
    profile = database.profileGet(user.getID())
    user_sets = database.settingsGet(user.getID())
    return flask.render_template(
        "profile.html",
        user = user,
        profile = profile,
        user_sets = user_sets
    )
@engine.route("/profile/tag/<tag>")
@authRequired
def profile_tag(tag : str):
    user = database.userGet(sessions.get(flask.session["token"]))
    profile = database.profileGet(user.getID())
    if not database.userIsExist(tag=tag):
        return flask.redirect("/profile")
    other = database.userGet(tag=tag)
    other_profile = database.profileGet(other.getID())
    user_sets = database.settingsGet(other.getID())
    return flask.render_template(
        "profile_others.html",
        user = user,
        profile = profile,
        other = other,
        other_profile = other_profile,
        user_sets = user_sets
    )
@engine.route("/profile/update/<type>", methods=['POST'])
@authRequired
def profile_update(type : str):
    data = dict(flask.request.form)
    user = database.userGet(sessions.get(flask.session["token"]))
    if type == "p":
        if len(data['username']) > 30:
            return "Имя слишком длинное."
        if not re.match("^[A-ЯЁ][а-яё]+\s[A-ЯЁ][а-яё]+$", data['username']):
            return "Имя должно содержать только русские символы и иметь формат 'Имя Фамилия'"
        database.profileSet(
            user.getID(),
            "name",
            str(data['username'])
        )
        if (user.getTag() != data['usertag']):
            isBusy = database.userIsExist(tag = data['usertag'])
            if isBusy:
                return "Тег уже занят другим участником форума."
            if len(data['usertag']) not in range(3, 13):
                return "Тег должен иметь длину от 3 до 12 символов."
            if not re.match("^[A-Za-z0-9]+([A-Za-z0-9]*|[._-]?[A-Za-z0-9]+)*$", data['usertag']):
                return "Тег должен содержать латинские символы, цифры и символы '.','_','-'"
            database.userSet(
                user.getID(),
                "tag",
                data['usertag']
            )
        if (len(data['new-password']) > 0 and len(data['new-password']) < 8):
            return "Минимальная длина пароля 8 символов."
        if (len(data['new-password']) >= 8):
            if PasswordManager.isValid(
                data['current-password'],
                settings.getPasswordSalt(),
                user.getPassword()
            ):
                newpass = PasswordManager.hashPassword(
                    data['new-password'],
                    settings.getPasswordSalt()
                )
                database.userSet(
                    user.getID(),
                    "password",
                    newpass
                )
        return flask.redirect("/profile")
    if type == "s":
        hide_email = False
        if ("hide-email" in data):
            hide_email = not hide_email
        database.settingsSetBool(
            user.getID(),
            "hide_email",
            hide_email
        )
        print(hide_email)
        return flask.redirect("/profile")
@engine.route("/f/<int:id>")
@authRequired
def subcat_list(id : int):
    try:
        subcat = database.subcatGet(id)
    except:
        return "Invalid subcategory;"
    topics = database.topicGetBySubcat(subcat.getID())
    creators = dict()
    for topic in topics:
        creators[topic.getID()] = database.userGet(topic.getAuthor()).getTag()
    user = database.userGet(sessions.get(flask.session["token"]))
    profile = database.profileGet(user.getID())
    return flask.render_template(
        "topic.html",
        user = user,
        profile = profile,
        subcat = subcat,
        topics = topics,
        creators = creators
    )
@engine.route("/t/<int:id>")
@authRequired
def topic_display(id : int):
    try:
        topic = database.topicGet(id)
    except:
        return "Topic was not found!"
    comments = database.reviewGetByTopic(id)
    commentor = dict()
    for comment in comments:
        commentor[comment.getID()] = database.userGet(comment.getAuthor()).getTag()
    author = database.userGet(topic.getAuthor())
    return flask.render_template(
        "topic_view.html",
        topic = topic,
        comments = comments,
        commentor = commentor,
        author = author
    )
@engine.route("/t/add_comment/<int:topic_id>", methods = ['POST'])
@authRequired
def topic_comment(topic_id : int):
    try:
        topic = database.topicGet(topic_id)
    except:
        return "Topic was not found!"
    data = dict(flask.request.form)
    if len(data['comment-content']) > 300:
        return "Комментарий должен быть не длинее 300 символов."
    user = database.userGet(sessions.get(flask.session["token"]))
    database.reviewAdd(
        topic_id,
        user.getID(),
        data['comment-content'],
        False,
        "",
        0,
        int(time.time()),
        int(time.time())
    )
    return flask.redirect(f"/t/{topic_id}")
    


@engine.route("/add/<int:subcat_id>/<mode>", methods=['POST'])
@authRequired
def topic_add(subcat_id : int, mode : str):
    try:
        subcat = database.subcatGet(subcat_id)
    except:
        return "Subcategory doesn't exist;"
    if mode == "request":
        data = dict(flask.request.form)
        if len(data['title']) > 40:
            return "Название должно быть не длинее 40 символов."
        user = database.userGet(sessions.get(flask.session["token"]))
        topic = database.topicAdd(
            subcat_id,
            user.getID(),
            data['title'],
            "No preview due to my lazy ass.",
            data['content'],
            "",
            False,
            "",
            int(time.time()),
            int(time.time())
        )
        return flask.redirect(f"/t/{topic.getID()}")
    if mode == "form":
        subcat = database.subcatGet(subcat_id)
        return flask.render_template(
            "topic_add.html",
            subcat = subcat
        )


# =========================
# =   AUTHENTIFICATION    =
# =========================
@engine.route("/logout")
def auth_logout():
    flask.session["token"] = ""
    return flask.redirect("/")
@engine.route("/auth")
def auth_form():
    if ("token" in flask.session):
        if (flask.session["token"] in sessions):
            return flask.redirect("/")
    return flask.render_template("auth.html")
@engine.route("/auth/approve/<mail>/<hashcode>")
def auth_approve(mail : str, hashcode : str):
    if mail not in registrations:
        return "No mail found in requests;"
    checker = registrations[mail]
    checkhash = checker[len(checker) - 1]
    if (hashcode != checkhash):
        return "Invalid hash approvement code;"
    user = database.userAdd(
        checker[1],
        checker[2],
        checker[3],
        "user",
        int(time.time()),
        int(time.time())
    )
    database.profileAdd(
        user.getID(),
        checker[0],
        "profile/no-avatar.png",
        "About Me",
        list(),
        list()
    )
    database.settingsAdd(
        user.getID(),
        True,
        True,
        True,
        True,
        True
    )
    registrations.pop(mail)
    temp = flask.render_template_string("Аккаунт успешно создан! Вы будете перенаправлены на страницу авторизации через 3 секунды.")
    return temp, {"Refresh": "3; url=/"}
@engine.route("/auth/<type>", methods=['POST'])
def auth_session(type : str):
    data = dict(flask.request.form)
    if type == "log":
        if not database.userIsExist(tag = data['tag']):
            return "Пользователь не найден."
        target_user = database.userGet(tag = data['tag'])
        if not PasswordManager.isValid(
            data['password'],
            settings.getPasswordSalt(),
            target_user.getPassword()
        ):
            return "Пароль неверн."
        flask.session["token"] = secrets.token_hex(64)
        sessions[flask.session["token"]] = target_user.getID()
        database.userSet(
            target_user.getID(),
            "last_seen",
            int(time.time())
        )
        return flask.redirect("/")
    if type == "reg":
        if (data['email'] in registrations):
            return "На данный E-mail уже было отправлено приглашение."
        if len(data['username']) > 30:
            return "Имя слишком длинное."
        if not re.match("^[A-ЯЁ][а-яё]+\s[A-ЯЁ][а-яё]+$", data['username']):
            return "Имя должно содержать только русские символы и иметь формат 'Имя Фамилия'"
        new_username = data['username']
        isBusy = database.userIsExist(tag = data['tag'])
        if isBusy:
            return "Тег уже занят другим участником форума."
        if len(data['tag']) not in range(3, 13):
            return "Тег должен иметь длину от 3 до 12 символов."
        if not re.match("^[A-Za-z0-9]+([A-Za-z0-9]*|[._-]?[A-Za-z0-9]+)*$", data['tag']):
            return "Тег должен содержать латинские символы, цифры и символы '.','_','-'"
        new_usertag = data['tag']
        new_email = data['email']
        if (database.userEmailUsed(new_email)):
            return "Данная почта уже используется!"
        if (len(data['password']) < 8):
            return "Минимальная длина пароля 8 символов."
        new_password = PasswordManager.hashPassword(
            data['password'],
            settings.getPasswordSalt()
        )
        new_invite_hash = secrets.token_urlsafe(32)
        registrations[new_email] = (
            new_username,
            new_usertag,
            new_email,
            new_password,
            new_invite_hash
        )
        genlink = str("http://" + urlparse(flask.request.base_url).hostname + f"/auth/approve/{new_email}/{new_invite_hash}")
        print(MailTemplates._SUBJECT_AUTH.replace("/username/", new_username))
        print(MailTemplates._BODY_AUTH.replace("/link/", genlink))
        mail_service.sendMessage(
            MailTemplates._SUBJECT_AUTH.replace("/username/", new_username),
            new_email,
            MailTemplates._BODY_AUTH.replace("/link/", genlink)
        )
        return "Проверьте вашу почту на ссылку с приглашением!"


# =========================
# =     INSTALLATION      =
# =========================
@engine.route("/install")
def installation():
    if settings.getPanelPass() != "notsetup":
        return flask.redirect("/")
    return flask.render_template("installation.html")
@engine.route("/install_complete", methods=['POST'])
def installation_complete():
    if settings.getPanelPass() != "notsetup":
        return flask.redirect("/")
    data = dict(flask.request.form)
    settings.password_salt = PasswordManager.getSalt()
    settings.panel_pass =  PasswordManager.hashPassword(data['panel_pass'], settings.getPasswordSalt())
    settings.mail_host = data['smtp_server']
    settings.mail_port = data['smtp_port']
    settings.mail_from = data['smtp_user']
    settings.mail_pass = data['smtp_pass']
    settings.mail_user = settings.getMailFrom()
    mail_service = MailService.MailService(
        settings.getMailHost(),
        settings.getMailPort(),
        settings.getMailFrom(),
        settings.getMailUser(),
        settings.getMailPass()
    )
    json_service.writeData(SysSettings.settings_to_dict(settings))
    user = database.userAdd(
        data['usertag'],
        data['email'],
        PasswordManager.hashPassword(data['password'], settings.getPasswordSalt()),
        "admin",
        int(time.time()),
        int(time.time())
    )
    database.profileAdd(
        user.getID(),
        data['username'],
        "profile/no-avatar.png",
        "admin account",
        list(),
        list()
    )
    database.settingsAdd(
        user.getID(),
        True,
        True,
        True,
        True,
        True
    )
    mail_service.sendMessage(
        MailTemplates._SUBJECT_INSTALL,
        user.getEmail(),
        MailTemplates._BODY_INSTALL + urlparse(flask.request.base_url).hostname
    )
    return flask.redirect("/")

# =========================
# =     INITIALIZING      =
# =========================
if __name__ == '__main__':
    # ==============
    # === LOGGER ===
    # ==============
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename = "_data/latest.log")
    # ================
    # === DATABASE ===
    # ================
    database = Database.Database("_data/forum.sql", logger)
    # =======================
    # === SYSTEM SETTINGS ===
    # =======================
    settings = SysSettings.dict_to_Settings(
        json_service.getData()
    )
    # ====================
    # === MAIL SERVICE ===
    # ====================
    mail_service = MailService.MailService(
        settings.getMailHost(),
        settings.getMailPort(),
        settings.getMailFrom(),
        settings.getMailUser(),
        settings.getMailPass()
    )
    # ===================
    # === SERVER INIT ===
    # ===================
    serve(
        engine,
        host = "0.0.0.0",
        port = 80
    )