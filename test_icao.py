#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 22:58:33 2014

@author: Evgeny Bogodukhov
@email: boevgeny@gmail.com
"""


if __name__ == "__main__":

    import json
    import logging
    import imsg

    LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                  '-35s %(lineno) -5d: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT)

    fh = logging.FileHandler('icao_ats_msg_parser.log')
    #fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


    EXAMPLES = {
        3: {
            "EXAMPLES": [
                "(FPL",
                "(CNL",
                "(CHGA/B234A/B231",
                "(CPLA/B002",
            ],
        },
        5: {
            "EXAMPLES": [
                "ALERFA/EINNZQZX/REPORT OVERDUE (ДОНЕСЕНИЕ НЕ" "\n"
                "ПОСТУПИЛО ВОВРЕМЯ)"
            ],
        },
        7: {
            "EXAMPLES": [
                "–BAW902",
                "–SAS912/A5100",
            ],
        },
        8: {
            "EXAMPLES": [
                "–V",
                "–IS",
            ],
        },
        9: {
            "EXAMPLES": [
                "–DC3/M",
                "–B707/M",
                "–2FK27/M",
                "–ZZZZ/L",
                "–3ZZZZ/L",
                "–B747/H",
            ],
        },
        10: {
            "EXAMPLES": [
                "–S/A",
                "–SCHJ/CD",
                "–SAFJ/SD",
            ],
        },
        13: {
            "EXAMPLES": [
                "–EHAM0730",
                "–AFIL1625",
            ],
        },
        14: {
            "EXAMPLES": [
                "–LN/1746F160",
                "–CLN/1831F240F180A",
                "–5420N05000W/0417F290",
                "–LNX/1205F160F200B",
                "–ZD126028/0653F130",
            ],
        },
        15: {
            "EXAMPLES": [
                "–K0410S1500 A4 CCV R11",
                "–K0290A120 BR 614",
                "–N0460F290 LEK2B LEK UA6 FNE UA6 XMM/M078F330 UA6N PON"   "\n"
                "UR10N CHW UA5 NTS DCT 4611N00412W DCT STG UA5 FTM"        "\n"
                "FATIM1A",
                "–M082F310 BCN1G BCN UG1 52N015W 52N020W 52N030W 50N040W"  "\n"
                "49N050W DCT YQX",
                "–N0420F310 R10 UB19 CGC UA25 DIN/N0420F330 UR14 IBY UR1 MID",
            ],
        },
        16: {
            "EXAMPLES": [
                "–EINN0630",
                "–EHAM0645 EBBR",
                "–EHAM0645 EBBR EDDL",
            ],
        },
        17: {
            "EXAMPLES": [
                "–EHAM1433",
                "–ZZZZ1620 DEN HELDER",
            ],
        },
        18: {
            "EXAMPLES": [
                "–0",
                "–EET/15W0315 20W0337 30W0420 40W0502",
                "–STS/ONE ENG INOP",
                "–DAT/S",
            ],
        },
        19: {
            "EXAMPLES": [
                "-E/0745 P/6 R/VE S/M J/L D/2 8 C YELLOW" "\n"
                "A/YELLOW RED TAIL N145E C/SMITH"         "\n"
                "N/ANY OTHER COMMENTS"
            ],
        },
        20: {
            "EXAMPLES": [
                "-USAF LGGGZAZX 1022 126,7 GN 1022" "\n"
                "PILOT REPORT OVER NDB ATS UNITS"   "\n"
                "ATHENS FIR ALERTED NIL"
            ],
        },
        21: {
            "EXAMPLES":[
                "–1232 121,3 CLA 1229 TRANSMITTING ONLY (ПЕРЕДАЧА ТОЛЬКО" "\n"
                "НА) 126,7 LAST POSITION CONFIRMED BY RADAR (ПОСЛЕДНЕЕ"   "\n"
                "МЕСТОПОЛОЖЕНИЕ ПОДТВЕРЖДЕНО РАДАРОМ)"
            ],
        },
        22: {
            "EXAMPLES":[
                "-8/IN",
                "-14/ENO/0145F290A090A",
                "-8/I-14/ENO/0148F290A110A"
            ],
        },
    }

    def tests():
        print "tests():"
        ICAO_MSG_PATTERNS = imsg.icao.icao_ats_msg_parser.ICAO_MSG_PATTERNS
        for item_name in ICAO_MSG_PATTERNS:
            item = ICAO_MSG_PATTERNS[item_name]
            examples = EXAMPLES.get(item_name,{}).get("EXAMPLES", None)
            match_method = item.get("MATCH_METHOD", None)
            pattern = item.get("PATTERN", None)
            print
            print "*"*40
            print item_name
            print "*"*40
            if examples is not None \
                    and match_method is not None \
                    and pattern is not None:
                for example in examples:
                    print example
                    if match_method is not None:
                        print "match_method is not None:", match_method
                        method_func = imsg.icao.icao_ats_msg_parser.methods.get(match_method, None)
                        if method_func is not None:
                            print "method_func is not None:"
                            print json.dumps(method_func(pattern, example), indent=4).decode("unicode-escape")
    tests()
    parser = imsg.icao.parser()

    messages = [
#"""
#-TITLE REJ -MSGTYP IFPL -FILTIM 232136 -ORIGINDT 1401232139
#-BEGIN ADDR
#       -FAC UWWWPOTX
#-END ADDR
#-COMMENT THIS MESSAGE HAS BEEN REJECTED AUTOMATICALLY
#
#-ERROR EFPM233: FLIGHT PLAN ALREADY GENERATED FROM RPL DATA
#-OLDMSG
#(FPL-POT742-IS
#-SB20/M-SDFGIRWY/H
#-UDYZ0010
#-N0348F180 SEVAN3E SEVAN B140 GIDLA/N0356F300 N82
# LAPTO/K0657F300 A234 USEMA R11 PT PT2A
#-UUOO0227 UUDD UUOB
#-PBN/B1D1 DOF/140124 REG/VPBPR
# EET/UGGG0019 URRV0035 UUWV0154
# RMK/FLIGHT IS DELAYED FROM 140123)
#""",
u"""
(АРР-ПО773-УУДД-УУОБ0625-РЕГ/ЖЩБГЦ)

""",
u"""
(ФПЛ-ПО723М-ИС
-СФ34/М-СДФГ/С
-УУДД0230
-К0452Ф190 ДЦТ ДК ДЦТ ФЖ Р11 ТС ДЦТ
-УУОО0115 УУДД УУОО
-ДОФ/140212 РЕГ/VQBGС КВС/ГОРБУНОВ)
""",
]
    for msg in messages:
        msg_decoded =  parser.decode(msg)
        print json.dumps(msg_decoded, indent=4, sort_keys=True).decode("unicode-escape")

