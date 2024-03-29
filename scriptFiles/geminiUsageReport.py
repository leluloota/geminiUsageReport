import datetime
import os
import platform
import socket
import configparser
from logger import log_handler
from functions import parser
import shutil

# General variables
now = datetime.datetime.now()
date = now.strftime("%Y%m%d")
time = now.strftime("%H:%M")
dateTime = now.strftime("%Y-%m-%d %H:%M")
hostName = socket.gethostname()
osVersion = platform.system() + ' ' + platform.release()
pythonVersion = platform.python_version()
osDistribution = platform.platform()
currentDirectory = os.getcwd()
scriptDirectory = os.path.dirname(currentDirectory)
configFile = scriptDirectory + r'\configFiles\geminiUsageReport.ini'

# Read program configurations
config = configparser.ConfigParser()
config.read(configFile)
programName = config.get('INITIALS', 'programName')
# Read logging properties
logLevel = config.get('LOGGING', 'logLevel')
enableConsole = config.get('LOGGING', 'enableConsole')
logFilePath = config.get('LOGGING', 'logFilePath')
# rotatorType = config.get('LOGGING', 'rotatorType')
logFileMaxBytes = int(config.get('LOGGING', 'logFileMaxBytes'))
# rotatorInterval = int(config.get('LOGGING', 'rotatorInterval'))
backupCount = int(config.get('LOGGING', 'backupCount'))

# Initialize logger
infoLog, errorLog, debugLog, warningLog, criticalLog, logFileName = log_handler(
    programName.replace(' ', ''), logLevel, enableConsole, logFilePath, logFileMaxBytes, backupCount)

# Program start
infoLog('{programName} started on {dateTime}'.format(programName=programName, dateTime=dateTime))
infoLog('Logger loaded successfully, log file: {logFileName}'.format(logFileName=logFileName))
infoLog('OS: {osVersion}, Python version: {pythonVersion}, current directory: {currentDirectory}'.format(
    osVersion=osVersion, pythonVersion=pythonVersion, currentDirectory=currentDirectory))
infoLog('')


# Read rest of required properties
sourceLogFiles = config.get('DATA', 'sourceLogFiles').split(',')  # Get source log file as list, use comma ase separator
infoLog('List of log files to handle:')
for logFile in sourceLogFiles:  # Log a list of source logfiles
    infoLog('{logFile}'.format(logFile=logFile))
workPath = config.get('INITIALS', 'workPath')  # Get path where log file is copied to
infoLog(f'Work path set to: {workPath}'.format(workPath=workPath))
infoLog('')

# Start looping log files
debugLog('Log file loop started')
for entry in sourceLogFiles:  # Get next file
    logFile = entry.rsplit('\\', 1)[-1]  # Get file name with extension
    infoLog(f'Log file: {logFile}'.format(logFile=logFile))
    try:
        shutil.copy(entry, workPath)  # Copy log file to work path
        infoLog(f'File: {entry} copied to {workPath}'.format(entry=entry, workPath=workPath))
        infoLog('')
    except Exception as e:
        errorLog('Log file copy failed')
        errorLog('Error message: {e}'.format(e=e))
    parser(logFile, workPath, infoLog, errorLog, debugLog)
