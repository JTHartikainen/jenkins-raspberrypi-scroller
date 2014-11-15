#
# config.py - Configuration file for JenkinsLEDScroller
#
# Global application name 
APPNAME = "Jenkins LED Scroller"
AUTHORNAME = "jhartika (jaakko dot hartikainen at gmail dot com)"
#
# Logging options"
LOGPATH = "log.txt"
LOGGERNAME = "jenkinsledscroller"

# Debug mode (ignores all hardware GPIO operations, outputs to console instead)
DEBUGMODE = "true"

# Jenkins context root, hostname and authentication details. Use localhost as hostname if Jenkins is running on the same  system.
#
# Replace the JENKINS_USER and JENKINS_PASSWORD default values with the ones available from Jenkins User accounts - manager (API keys)

JENKINS_ROOT="/jenkins"
JENKINS_HOST="http://host:8080"
JENKINS_USER="jenkins"
JENKINS_PASSWORD="abc"

# Polling frequency in seconds
POLL_INTERVAL=5

# Task names to poll
TASK_NAMES=["Test-Task-1","Test-Task-2"]

# Scroll speed in milliseconds
SCROLL_SPEED=1000

COLOR_RED=1
COLOR_GREEN=2
COLOR_ORANGE=3