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

        self.parsers_dict = {
            "iata": iata.Parser(),
            "icao": icao.Parser(),
        }

        self.parsers = [
            iata.Parser(),
            icao.Parser(),
        ]

    def decode(self, raw, standard=None):
        ret = None
        if standard in self.parsers_dict:
            try:
                decoded = self.parsers_dict[standard](raw)
            except:
                logging.debug(traceback.format_exc())
            else:
                if decoded is not None:
                    if decoded != {}:
                        ret = decoded
        else:
            for parser in self.parsers:
                try:
                    decoded = parser.decode(raw)
                except:
                    logging.debug(traceback.format_exc())
                else:
                    if decoded is not None:
                        if decoded != {}:
                            ret = decoded
        return ret
