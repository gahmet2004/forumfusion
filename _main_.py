import logging
import _libs.classes.System.Database as Database

from flask import Flask

engine = Flask(__name__)
logger = None
database = None

@engine.route('/')
def root_manager():
    return 'Fuck me :)'

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename = "_data/latest.log")
    logger.info('hello')
    database = Database.Database("_data/forum.sql", logger)
    # from waitress import serve
    # serve(
    #     engine,
    #     host = "localhost",
    #     port = 8080
    # )
    engine.run(
        host = "localhost",
        port = 8080,
        debug = True
    )