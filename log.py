#!/usr/bin/env python3
import logging
from logging.handlers import TimedRotatingFileHandler


level    = logging.DEBUG
format   = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logFile='logs/frame.log'

handlers = [logging.FileHandler(logFile), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)


handlers = [logging.StreamHandler(logFile), TimedRotatingFileHandler(logFile,'midnight',1)]

logging.basicConfig(level = level, format = format, handlers = handlers)
