#!/usr/bin/env python
class Color(object):
    """A class for color styling"""
    def __init__(self):
        self.black = '\033[0;30m'
        self.bblack = '\033[1;30m'
        self.red = '\033[0;31m'
        self.bred = '\033[1;31m'
        self.green = '\033[0;32m'
        self.bgreen = '\033[1;32m'
        self.yellow = '\033[0;33m'
        self.byellow = '\033[1;33m'
        self.blue = '\033[0;34m'
        self.bblue = '\033[1;34m'
        self.magenta = '\033[0;35m'
        self.bmagenta = '\033[1;35m'
        self.cyan = '\033[0;36m'
        self.bcyan = '\033[1;36m'
        self.white = '\033[0;37m'
        self.bwhite = '\033[1;37m'
        self.reset = '\033[0m'
        
