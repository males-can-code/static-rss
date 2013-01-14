#!/usr/bin/python3

import sys
import time
import os
import inspect
import re
from time import strftime

class Log(object):
    def __init__(self, log_file=False, level='debug', display=True, show='all', maxlength=15):
        self.log_file = log_file
        self.display = display
        self.show = show
        self.level = level
        self.maxlength = maxlength
        self.color_info = '\033[37m'         # white
        self.color_error = '\033[31m'
        self.color_debug = '\033[0m'
        self.color_warning = '\033[33m'
        self.color_reset = '\033[0m'

        self.color_message = '\033[35m'
        self.color_ip = '\033[1;32m'          # green
        self.color_inbound = '\033[1;36m'     # cyan
        self.color_outbound = '\033[1;31m'    # red
        self.color_listen = '\033[1;94m'      # blue
        self.color_connect = '\033[1;32m'     # green

        if self.log_file:
            try:
                with open(self.log_file) as f: pass
            except IOError as e:
                try:
                    FILE = open(self.log_file, 'w')
                    FILE.close()
                except IOError as e:
                    print('WARNING ... Couldn\'t create file \'%s\' Not writing logs!'%self.log_file)
                    return

    def create_message(self, msg_type, module, message, color):
        if self.level == 'error':
            if msg_type == 'debug' or msg_type == 'warning' or msg_type == 'info':
                return
        if self.level == 'warning':
            if msg_type =='debug' or msg_type == 'info':
                return
        if self.level == 'info':
            if msg_type == 'debug':
                return

        # custom syntax highlighting
        message = re.sub( '<<<', self.color_inbound + '<<<' + self.color_reset, message )
        message = re.sub( '>>>', self.color_outbound + '>>>' + self.color_reset, message )
        message = re.sub( 'LISTEN', self.color_listen + 'LISTEN' + self.color_reset, message )
        message = re.sub( 'CONNECT', self.color_connect + 'CONNECT' + self.color_reset, message )

        address = re.findall( r'[0-9]+(?:\.[0-9]+){3}', message )
        if address:
            message = re.sub( r'[0-9]+(?:\.[0-9]+){3}', self.color_ip + address[0] + self.color_reset, message )

        timestamp = strftime("%H:%M:%S")
        module = module.ljust(self.maxlength)
        msg_type = msg_type.ljust(7)

        if self.display:
            #print(timestamp, color + msg_type.upper() + self.color_reset, module, color, message, self.color_reset)
            #print(timestamp, module, color + msg_type.upper(), message, self.color_reset)
            print(timestamp, module, color, message, self.color_reset)
        if self.log_file:
            FILE = open(self.log_file, 'a')
            FILE.write(timestamp + ' ' + msg_type + ' ' + module + ' ' + message + '\n')
            FILE.close()


    def info(self, message):
        color = self.color_info
        self.create_message('info', inspect.stack()[1][3], message, color)

    def debug(self, message):
        color = self.color_debug
        self.create_message('debug', inspect.stack()[1][3], message, color)

    def warning(self, message):
        color = self.color_warning
        self.create_message('warning', inspect.stack()[1][3], message, color)

    def error(self, message):
        color = self.color_error
        self.create_message('error', inspect.stack()[1][3], message, color)
