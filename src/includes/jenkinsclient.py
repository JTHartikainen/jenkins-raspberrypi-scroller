#
# jenkins_client.py - Jenkins Client utilities for JenkinsLEDScroller (using Python-Requests) 
#
# Author: Jaakko Hartikainen (jaakko dot hartikainen at gmail dot com )
#

import logging
import requests
import time

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
		self.logger.info("Jenkins ROOT.......................: " + self.config.JENKINS_ROOT + "\n");
		self.logger.info("Jenkins HOSTNAME...................: " + self.config.JENKINS_HOST + "\n");
		self.logger.info("Jenkins USER.......................: " + self.config.JENKINS_USER + "\n");
		self.logger.info("Jenkins PASSWORD...................: " + self.config.JENKINS_PASSWORD + "\n");
		self.logger.info("Poll interval (seconds)............: " + str(self.config.POLL_INTERVAL) + "\n");
		self.logger.info("Scrolling speed in milliseconds:...: " + str(self.config.SCROLL_SPEED) + "\n");

	def lastbuild(self,dict):
		self.logger.info("Requesting last build data from Jenkins...")
		try:
			for taskname in self.config.TASK_NAMES:
				r = requests.get(self.config.JENKINS_HOST + self.config.JENKINS_ROOT + "/job/" + taskname + "/api/json?depth=1", auth=(self.config.JENKINS_USER, self.config.JENKINS_PASSWORD)) or exit("Error fetching URL!")
				lastBuildData = r.json().get("lastCompletedBuild")			
				message = "Last completed build data for " + taskname + " is " + lastBuildData.get("fullDisplayName")
				dict[taskname] = lastBuildData
				#self.logger.info("Sending message to LED screen...")
				#ledmatrix.scroll(message, self.config.COLOR_GREEN, 5)
				self.logger.info(message)
		except requests.exceptions.RequestException as e:
			self.logger.error("Cannot request last build data: " + str(e))

	def display_tasks_to_poll(self):
		self.logger.info("Requesting JSON from Jenkins...")
		try:
			for taskname in self.config.TASK_NAMES:
				r = requests.get(self.config.JENKINS_HOST + self.config.JENKINS_ROOT + "/job/" + taskname + "/api/json", auth=(self.config.JENKINS_USER, self.config.JENKINS_PASSWORD)) or exit("Error fetching URL!")
				self.logger.info("Request processed successfully.")
				self.logger.debug("Request URL: " + r.url + ", request status code: " + str(r.status_code))
				#self.logger.debug("Request contents as JSON: " + str(r.json()))
				displayName = r.json().get("displayName")
				message = "Build polling active for task: " + str(displayName)
				self.logger.info("Sending message to LED screen...")
				ledmatrix.scroll(message, self.config.COLOR_GREEN, 5)
				self.logger.info("Scrolled message successfully ('" + message + "')")
		except requests.exceptions.RequestException as e:
			self.logger.error("Cannot get test JSON data from Jenkins: " + str(e))

	def poll_tasks(self):
		self.logger.info("Entering polling mode...")
		self.display_tasks_to_poll()
		lastbuilds = {}
		builds = {} 
		while 1:
			self.lastbuild(builds)
			for taskname in self.config.TASK_NAMES:
				try:
					if (lastbuilds[taskname].get("number") != builds[taskname].get("number")):
						self.logger.info("!!! Changed build status for " + taskname + "!")
						if (builds[taskname].get("result") == "SUCCESS"):
							ledmatrix.scroll("         Build " + builds[taskname].get("fullDisplayName") + " success!           ", self.config.COLOR_GREEN, 1)
						elif (builds[taskname].get("result") == "ABORTED"):
							ledmatrix.scroll("         Build " + builds[taskname].get("fullDisplayName") + " aborted!           ", self.config.COLOR_ORANGE, 1)
						elif (builds[taskname].get("result") == "FAILED"):
							ledmatrix.scroll("         Build " + builds[taskname].get("fullDisplayName") + " failed!            ", self.config.COLOR_RED, 1)
						lastbuilds[taskname] = builds[taskname]
				except KeyError as e:
					lastbuilds[taskname] = builds[taskname]
				self.logger.info("Previous status for " + taskname + " (" + lastbuilds[taskname].get("fullDisplayName") + ") is: " + lastbuilds[taskname].get("result"))
				self.logger.info("Current status for " + taskname + " (" + builds[taskname].get("fullDisplayName") + " is: " + builds[taskname].get("result"))
			#self.logger.info("Dictionary keys: " + str(builds))
			time.sleep(self.config.POLL_INTERVAL)


