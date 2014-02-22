#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 06:50:05 2014

@author: Evgeny Bogodukhov
@email: boevgeny@gmail.com
"""
import logging

CYR2LAT = {
    u"А":u"A",
    u"Б":u"B",
    u"В":u"W",
    u"Г":u"G",
    u"Д":u"D",
    u"Е":u"E",
    u"Ё":u"E",#
    u"Ж":u"V",
    u"З":u"Z",
    u"И":u"I",
    u"Й":u"J",
    u"К":u"K",
    u"Л":u"L",
    u"М":u"M",
    u"Н":u"N",
    u"О":u"O",
    u"П":u"P",
    u"Р":u"R",
    u"С":u"S",
    u"Т":u"T",
    u"У":u"U",
    u"Ф":u"F",
    u"Х":u"H",
    u"Ц":u"C",
    u"Ч":u"4",#
    u"Ш":u"S",#
    u"Щ":u"Q",
    u"Ъ":u"X",#
    u"Ы":u"Y",
    u"Ь":u"X",
    u"Э":u"E",#
    u"Ю":u"J",#
    u"Я":u"Q",#
}

def cyr2lat(cyr):
    lat = u""
    for letter in cyr:
        try:
            if letter.islower():
                letter_lat = CYR2LAT.get(letter.upper(), None)
            else:
                letter_lat = CYR2LAT.get(letter, None)
        except:
            letter_lat = None
        if letter_lat is not None:
            if letter.islower():
                lat += letter_lat.lower()
            else:
                lat += letter_lat
        else:
            try:
                lat += letter
            except Exception, e:
                logging.warning("LETTER: {0}".format(letter) )
                logging.error(e)
    return lat
