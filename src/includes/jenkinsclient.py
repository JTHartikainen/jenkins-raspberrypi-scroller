#
# jenkins_client.py - Jenkins Client utilities for JenkinsLEDScroller (using Python-Requests) 
#
# Author: Jaakko Hartikainen (jaakko.hartikainen@gmail.com)
#

import logging
import requests
import ledmatrix as ledmatrix

# Get the global logger object

logger = logging.getLogger(LOGGERNAME)

class JenkinsClient(): 

	def __init__(self):
		logger.info("JenkinsClient loaded")

	def showsettings(self):
		print("Jenkins ROOT.......................: " + JENKINS_ROOT + "\n");
		print("Jenkins HOSTNAME...................: " + JENKINS_HOST + "\n");
		print("Jenkins USER.......................: " + JENKINS_USER + "\n");
		print("Jenkins PASSWORD...................: " + JENKINS_PASSWORD + "\n");
		print("Poll interval (seconds)............: " + str(POLL_INTERVAL) + "\n");
		print("Scrolling speed in milliseconds:...: " + str(SCROLL_SPEED) + "\n");

	def lastbuild(self):
		logger.info("Requesting last build data from Jenkins...")
		try:
			r = requests.get(JENKINS_HOST + JENKINS_ROOT + "/job/" + TASK_NAMES[0] + "/api/json", auth=(JENKINS_USER, JENKINS_PASSWORD)) or exit("Error fetching URL!")
			lastBuildData = r.json().get("lastCompletedBuild")
			ledmatrix.initledmatrix()
			logger.info("LED matrix hardware init OK!")
			message = "Last completed build data: " + str(lastBuildData)
			logger.info("Sending message to LED screen...")
			ledmatrix.scroll(message, 2, 5)
			logger.info("Scrolled message successfully ( " + message)
		except requests.exceptions.RequestException as e:
			logger.error("Cannot request last build data: " + str(e))

	def displayname(self):
		logger.info("Requesting test JSON from Jenkins...")
		try:
			r = requests.get(JENKINS_HOST + JENKINS_ROOT + "/job/" + TASK_NAMES[0] + "/api/json", auth=(JENKINS_USER, JENKINS_PASSWORD)) or exit("Error fetching URL!")
			logger.info("Request processed successfully.")
			logger.debug("Request URL: " + r.url + ", request status code: " + str(r.status_code))
			logger.debug("Request contents as JSON: " + str(r.json()))
			# Attempt to display status of first task name at screen
			ledmatrix.initledmatrix()
			logger.info("LED matrix hardware init OK!")
			displayName = r.json().get("displayName")
			message = "Build polling active for task: " + str(displayName)
			logger.info("Sending message to LED screen...")
			ledmatrix.scroll(message, 2, 5)
			logger.info("Scrolled message successfully ( " + message)
		except requests.exceptions.RequestException as e:
			logger.error("Cannot get test JSON data from Jenkins: " + str(e))

		


