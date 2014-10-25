#
# jenkins_client.py - Jenkins Client utilities for JenkinsLEDScroller (using Python-Requests) 
#
# Author: Jaakko Hartikainen (jaakko.hartikainen@gmail.com)
#

import logging
import requests
import ledmatrix as ledmatrix

# Create basic attributes
JENKINS_ROOT="/jenkins"

# Jenkins hostname and authentication details. Use localhost as hostname if Jenkins is running on the same  system.
#
# Replace the JENKINS_USER and JENKINS_PASSWORD default values with the ones available from Jenkins User accounts - manager (API keys)

JENKINS_HOST="http://host:8080"
JENKINS_USER="jenkins"
JENKINS_PASSWORD="abcdefghiklmno"

# Polling frequency in seconds
POLL_INTERVAL=5

# Task names to poll
TASK_NAMES=["Test-Task-1","Test-Task-2"]

# Scroll speed in milliseconds

SCROLL_SPEED=1000

logger = logging.getLogger("jenkinsledscroller")

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
			ledmatrix.scroll(message, 2, 5)
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
			ledmatrix.scroll(message, 2, 5)
			logger.info("Scrolled message successfully ( " + message)
		except requests.exceptions.RequestException as e:
			logger.error("Cannot get test JSON data from Jenkins: " + str(e))

		


