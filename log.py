#!/usr/bin/env python3
import logging

level    = logging.DEBUG
format   = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

handlers = [logging.FileHandler('frame.log'), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)


