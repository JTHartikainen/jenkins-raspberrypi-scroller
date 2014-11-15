#
# jenkins_client.py - Jenkins Client utilities for JenkinsLEDScroller (using Python-Requests) 
#
# Author: Jaakko Hartikainen (jaakko dot hartikainen at gmail dot com )
#

import logging
import requests

# RP
#from . import ledmatrix as ledmatrix

# Debug
from . import ledmatrix_dummy as ledmatrix

class JenkinsClient(): 

	def __init__(self, config):
		self.config = config
		self.logger = logging.getLogger(config.LOGGERNAME)
		self.logger.info("JenkinsClient loaded")
		ledmatrix.initledmatrix()
		self.logger.info("LED matrix hardware init OK!")

	def showsettings(self):
		print("Jenkins ROOT.......................: " + self.config.JENKINS_ROOT + "\n");
		print("Jenkins HOSTNAME...................: " + self.config.JENKINS_HOST + "\n");
		print("Jenkins USER.......................: " + self.config.JENKINS_USER + "\n");
		print("Jenkins PASSWORD...................: " + self.config.JENKINS_PASSWORD + "\n");
		print("Poll interval (seconds)............: " + str(self.config.POLL_INTERVAL) + "\n");
		print("Scrolling speed in milliseconds:...: " + str(self.config.SCROLL_SPEED) + "\n");

	def lastbuild(self):
		self.logger.info("Requesting last build data from Jenkins...")
		try:
			for taskname in self.config.TASK_NAMES:
				r = requests.get(self.config.JENKINS_HOST + self.config.JENKINS_ROOT + "/job/" + taskname + "/api/json", auth=(self.config.JENKINS_USER, self.config.JENKINS_PASSWORD)) or exit("Error fetching URL!")
				lastBuildData = r.json().get("lastCompletedBuild")			
				message = "Last completed build data for " + taskname + " is " + str(lastBuildData)
				self.logger.info("Sending message to LED screen...")
				ledmatrix.scroll(message, self.config.COLOR_GREEN, 5)
				self.logger.info("Scrolled message successfully ( " + message)
		except requests.exceptions.RequestException as e:
			self.logger.error("Cannot request last build data: " + str(e))

	def display_tasks_to_poll(self):
		self.logger.info("Requesting JSON from Jenkins...")
		try:
			for taskname in self.config.TASK_NAMES:
				r = requests.get(self.config.JENKINS_HOST + self.config.JENKINS_ROOT + "/job/" + taskname + "/api/json", auth=(self.config.JENKINS_USER, self.config.JENKINS_PASSWORD)) or exit("Error fetching URL!")
				self.logger.info("Request processed successfully.")
				self.logger.debug("Request URL: " + r.url + ", request status code: " + str(r.status_code))
				self.logger.debug("Request contents as JSON: " + str(r.json()))
				displayName = r.json().get("displayName")
				message = "Build polling active for task: " + str(displayName)
				self.logger.info("Sending message to LED screen...")
				ledmatrix.scroll(message, self.config.COLOR_GREEN, 5)
				self.logger.info("Scrolled message successfully ('" + message + "')")
		except requests.exceptions.RequestException as e:
			self.logger.error("Cannot get test JSON data from Jenkins: " + str(e))

	def poll_tasks(self):
		self.logger.info("Entering polling mode...")
		display_tasks_to_poll();
		while 1:
			# states = load_task_states()
			# for state in states
			#	if state != previous_task_states[state]
			#		scroll message for changed state
			#	elif 
			#		debug("No change observed for task " + taskname)		
			#



