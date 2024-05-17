import logging
import time

import _libs.classes.System.Database as Database
import _libs.classes.System.Settings as SysSettings
import _libs.classes.System.MailService as MailService

from flask import Flask

engine = Flask(__name__)
logger = None
database = None
settings = None
mail_service = None
json_service = Database.JsonManager("_data/settings.json")

@engine.route('/')
def root_manager():
    print(database.punishmentSet(2, 'reason', "dolb2"))
    print(database.punishmentSet(2, 'duration', 100))
    return "Hello"

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
    engine.run(
        host = "localhost",
        port = 8080,
        debug = True
    )