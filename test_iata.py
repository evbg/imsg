#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 22:21:53 2014

@author: Evgeny Bogodukhov
@email: boevgeny@gmail.com
"""

if __name__ == "__main__":

    import imsg
    import logging
    import json

    LOG_FORMAT = ('\n%(asctime)s \n'
                  '%(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT)

    fh = logging.FileHandler('iata_msg_parser.log')
    #fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
#    ch.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(ch)

    try:
        from atools import  dict_del_vals
    except:
        def dict_del_vals(dict_in):
            return dict_in

    f = """ED  NI  AD  RR  EO  FR  EA  AA  DL  PX  RC  EB FLD EDL CRT MAP DLA TOF TOW ZFW ALC""".split()

    EXAMPLES = {
        "ED": {
            "EXAMPLES": [
                "ED041630",
            ]
        },
        "NI": {
            "EXAMPLES": [
                "NI052215",
            ]
        },
        "AD": {
            "EXAMPLES": [
                "AD1210",
                "AD051210",
                "AD1210/1220",
                "AD051210/051220",
            ]
        },
        "RR": {
            "EXAMPLES": [
                "RR1230",
                "RR",
            ]
        },
        "EO": {
            "EXAMPLES": [
                "EO1310",
            ]
        },
        "FR": {
            "EXAMPLES": [
                "FR1315/1325",
                "FR/1325",
                "FR1315",
                "FR",
            ]
        },
        "EA": {
            "EXAMPLES": [
                "EA1515",
                "EA1515 ULY",
            ]
        },
        "AA": {
            "EXAMPLES": [
                "AA1235",
                "AA031235",
            ]
        },
        "DL": {
            "EXAMPLES": [
                "DL72/0120",
                "DL13/81/0020/0015",
            ]
        },
        "PX": {
            "EXAMPLES": [
                "PX5",
                "PX112",
                "PX12/134/56",
            ]
        },
        "RC": {
            "EXAMPLES": [
                "RC1025 ULY",
            ]
        },
        "EB": {
            "EXAMPLES": [
                "EB1025",
            ]
        },
        "FLD": {
            "EXAMPLES": [
                "FLD03",
            ]
        },
        "EDL": {
            "EXAMPLES": [
                "EDL72/0120",
                "EDL13/81/0020/0015",
            ]
        },
        "CRT": {
            "EXAMPLES": [
                "CRT041530",
                "CRT1530/1515",
            ]
        },
        "MAP": {
            "EXAMPLES": [
                "MAP041530",
            ]
        },
        "DLA": {
            "EXAMPLES": [
                "DLA85A///",
                "DLA11C/14A/93B/65C",
                "DLA//93A/",
            ]
        },
        "TOF": {
            "EXAMPLES": [
                "TOF102100",
                "TOF6400",
            ]
        },
        "TOW": {
            "EXAMPLES": [
                "TOW362030",
                "TOW63452",
            ]
        },
        "ZFW": {
            "EXAMPLES": [
                "ZFW132500",
                "ZFW62400",
            ]
        },
        "ALC": {
            "EXAMPLES": [
                "ALC3B",
                "ALC3B/2",
            ]
        },
    }

    def tests():
        logger.info("tests():")
        for item_name in F:
            item = F[item_name]
            examples = EXAMPLES.get(item_name,{}).get("EXAMPLES", None)
            match_method = "finditer"
            try:
                pattern = re.compile(item, re.X|re.S)
            except:
                logging.error(traceback.format_exc())
            if examples is not None \
                    and match_method is not None \
                    and pattern is not None:
                logger.info("")
                logger.info("*"*40)
                logger.info(item_name)
                logger.info("*"*40)
                n = 0
                for example in examples:
                    n+=1
                    logger.info("-"*40)
                    logger.info("{N}) {EXAMPLE}".format(
                        N=str(n).rjust(2," "),
                        EXAMPLE=example
                    ))
                    logger.info("-"*40)
                    if match_method is not None:
                        logger.info("match_method: " + match_method)
                        method_func = methods.get(match_method, None)
                        if method_func is not None:
                            logger.info(json.dumps(method_func(pattern, example), indent=4, sort_keys=True).decode("unicode-escape"))
#    tests()

    parser = imsg.iata.Parser()

    messages = [
"""\
MVT
YQ752/05.VQBGC.DME
AA0404/0411
""",
"""\
BRGDS,
POLET OPS
MVT
POT4632/02.RA82077.EBB
AA2047/2057

ALL TIME UTC

BRGDS,
POLET OPS
""",
"""\
BRGDS,
POLET OPS
COR
MVT
YQ777/02.VQBGC.DME
AD1404/1421 EA1525 VOZ
DL15/0004
PX26
SI TEST1 TEST11
TEST2
TEST3
""",
"""
MVT
YQ765/09.VQBGC.DME
AD0908/0915 EA1025 EGO
PX30
""",
"""
=HEADER
RCV,2014/02/19 06:03
=PRIORITY
QN
=DESTINATION TYPE B
STX,ULYFWXH
STX,LEDFF7X
STX,VOZPLXH
=ORIGIN
QXTGWXS
=DBLSIG
XS
=MSGID
190603
=SMI
MVT
=TEXT
YQ703/19.VPBPR.LED
AA0548/0552

supplementary sender/recipients information
from /c=ww/a=sitamail/o=typeb/s=ledff7x
""",
]
    for msg in messages:
        msg_decoded =  parser.decode(msg)
        print json.dumps(msg_decoded, indent=4, sort_keys=True).decode("unicode-escape")
