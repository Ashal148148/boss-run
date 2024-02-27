import os
import logging.config
import logging
from logs import logs_conf
logging.config.dictConfig(logs_conf)
logger = logging.getLogger(__name__)
logger.info('starting up')
logger.info(os.environ)
import src.gui
from nicegui import ui 

ui.run(reload=False, storage_secret='hi', on_air=False, port=80)
