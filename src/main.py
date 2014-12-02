#
# main.py - Main file for Jenkins+Raspberry Pi LED Matrix Scroller
#
# Author: Jaakko Hartikainen (jaakko dot hartikainen at gmail dot com )
#
import logging
import datetime
from cfg import config
from includes import loggerhelper
from includes import jenkinsclient

# Create loggerhelper

logger = loggerhelper.create_custom_logger(config, config.LOGGERNAME, logging.DEBUG)
logger.info("Logging setup successful.")

# Create new Jenkins Client instance and run a method to simply verify functionality

logger.info(config.APPNAME + " starting up...")
jenkins = jenkinsclient.JenkinsClient(config)
logger.info( jenkins.showsettings() )
#jenkins.display_tasks_to_poll()
jenkins.poll_tasks()
logger.info("Jenkins LED Scroller stopping!")
logging.shutdown()

