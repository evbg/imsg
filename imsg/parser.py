#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 14:32:22 2014

@author: Evgeny Bogodukhov
@email: boevgeny@gmail.com
"""

import iata
import icao
import traceback
import logging


class Parser():

    def __init__(self):
        self.parsers = [
            iata.parser(),
            icao.parser(),
        ]

    def decode(self, raw):
        ret = None
        for parser in self.parsers:
            try:
                decoded = parser.decode(raw)
            except:
                logging.error(traceback.format_exc())
            else:
                if decoded is not None:
                    if decoded != {}:
                        ret = decoded
        return ret
