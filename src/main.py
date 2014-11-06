#
# main.py - Main file for Jenkins+Raspberry Pi LED Matrix Scroller
#
# Author: Jaakko Hartikainen (jaakko.hartikainen@gmail.com)
#

import logging
import datetime
from cfg import config
from includes import jenkinsclient

# Initialize logging

logger = logging.getLogger(LOGGERNAME)
hdlr = logging.FileHandler(str(LOGPATH))
formatter = logging.Formatter("%(asctime)s %(module)s %(levelname)s - %(message)s")
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

# Output success text

logger.info("Jenkins LED Scroller started!")

# Create new Jenkins Client instance and run a method to simply verify functionality

jenkins = jenkinsclient.JenkinsClient()
logger.info( jenkins.showsettings() )
jenkins.displayname()
logger.info("Jenkins LED Scroller stopping!")
logging.shutdown()

