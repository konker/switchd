# -*- coding: utf-8 -*-
#
# switchd.watcher
#
# Copyright 2013 Konrad Markus
#
# Author: Konrad Markus <konker@luxvelocitas.com>
#

import os
import sys
import logging
import signal
import pyev
from subprocess import Popen
import RPi.GPIO as GPIO


class Watcher(object):
    def __init__(self, config):
        self.active = False
        self.config = config
        self.watcher = None
        self.loop = pyev.Loop()

        # initialize and start a signal watchers
        sigterm_watcher = pyev.Signal(signal.SIGTERM, self.loop, self.sigterm_cb)
        sigterm_watcher.start()
        sigint_watcher = pyev.Signal(signal.SIGINT, self.loop, self.sigint_cb)
        sigint_watcher.start()

        self.loop.data = [sigterm_watcher, sigint_watcher]

        # init GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config['GPIO_in'], GPIO.IN)
        GPIO.setup(config['GPIO_out'], GPIO.OUT, initial=GPIO.HIGH)


    def interval_cb(self, watcher, revents):
        logging.debug("Interval complete.. ")
        if GPIO.input(self.config['GPIO_in']):
            logging.info("Powering off")
            Popen(self.config['command'], bufsize=0, shell=False)
            self.halt()


    def sigterm_cb(self, watcher, revents):
        logging.info("SIGTERM caught. Exiting..")
        self.halt()


    def sigint_cb(self, watcher, revents):
        logging.info("SIGINT caught. Exiting..")
        self.halt()


    def start(self):
        logging.info("Event loop start")
        self.watcher = pyev.Timer(self.config["interval_secs"], 1.0, self.loop, self.interval_cb)
        self.watcher.start()
        self.loop.start()


    def halt(self):
        logging.info("Halting...")
        if self.loop.data:
            while self.loop.data:
                self.loop.data.pop().stop()

        if self.watcher:
            self.watcher.stop()

        self.loop.stop(pyev.EVBREAK_ALL)



