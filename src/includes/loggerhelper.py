#
# loggerhelper.py - helper class for logging
#
# Author: Jaakko Hartikainen (jaakko dot hartikainen at gmail dot com )
#

import logging

def create_custom_logger(config, name, loglevel):
	# Initialize logging
	logger = logging.getLogger(config.LOGGERNAME)
	hdlr = logging.FileHandler(str(config.LOGPATH))
	formatter = logging.Formatter("%(asctime)s %(module)s %(levelname)s - %(message)s")
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 
	logger.setLevel(loglevel)
	return logger
	# logger.setLevel(logging.DEBUG)

