#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 06:59:27 2014

@author: Evgeny Bogodukhov
@email: boevgeny@gmail.com
"""

import re
import logging
from ..cyr2lat import cyr2lat

ICAO_MSG_PATTERNS = {
    3: {

    "PATTERN": re.compile("""

    # Поле типа 3. Тип, номер сообщения и исходные данные
    # Field Type 3 — Message Type, Number and Reference Data

    # ОТКРЫТАЯ СКОБКА
    # OPEN BRACKET
    \(?

    # a) Индекс типа сообщения
    (?P<Message_Type_Designator>
        ALR|RCF|FPL|DLA|CHG|CNL|DEP|ARR|CPL|EST|CDN|ACP|LAM|RQP|RQS|SPL
    )
    # b) Номер сообщения
    (?P<Message_Number>
        [A-Z]{1,4}
        /
        [A-Z]{1,4}
        \d{3}
    )?
    # c) Исходные данные
    (?P<Reference_Data>
        [A-Z]{1,4}
        /
        [A-Z]{1,4}
        \d{3}
    )?
    """, re.X),
    "MATCH_METHOD": "search"
    },

    5: {

    "PATTERN": re.compile("""

    # Поле типа 5. Описание аварийного положения
    # Field Type 5 — Description of Emergency

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    # a) Аварийная стадия
    (?P<Phase_of_Emergency>
        INCERFA|ALERFA|DETRESFA
    )

    # ДЕЛИТЕЛЬНАЯ КОСАЯ ЧЕРТА
    # OBLIQUE STROKE
        /

    # b) Составитель сообщения
    (?P<Originator_of_Message>
        [A-Z]{8}
    )

    # ДЕЛИТЕЛЬНАЯ КОСАЯ ЧЕРТА
    # OBLIQUE STROKE
        /

    # c) Характер аварийного положения
    (?P<Nature_of_Emergency>
        .*
    )
    """, re.X|re.S),
    "MATCH_METHOD": "search",
    },

    7: {

    "PATTERN": re.compile("""

    # Поле типа 7. Опознавательный индекс воздушного судна и режим и код ВОРЛ
    # Field Type 7 — Aircraft Identification and Mode A Code

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    # a) Опознавательный индекс воздушного судна
    (?P<Aircraft_Identification>
        [A-Z\d]{1,7}
    )


    (# < < < ? ? ? НЕОБЯЗАТЕЛЬНЫЙ БЛОК НАЧАЛО

    # ДЕЛИТЕЛЬНАЯ КОСАЯ ЧЕРТА
    # OBLIQUE STROKE
        /

    # b) Режим ВОРЛ
    (?P<SSR_Mode>
        [A-Z]
    )

    # c) Код ВОРЛ
    (?P<SSR_Code>
        \d{4}
    )

    )?# > > > ? ? ? НЕОБЯЗАТЕЛЬНЫЙ БЛОК КОНЕЦ
    """, re.X),
    "MATCH_METHOD": "search",
    },

    8: {

    "PATTERN": re.compile("""

    # Поле типа 8. Правила полетов и тип полета

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    # a) Правила полетов
    (?P<Flight_Rules>
        I|V|Y|Z
    )

    (# < < < ? ? ? НЕОБЯЗАТЕЛЬНЫЙ БЛОК НАЧАЛО

    # b) Тип полета
    (?P<Type_of_flight>
        S|N|G|M|X
    )

    )?# > > > ? ? ? НЕОБЯЗАТЕЛЬНЫЙ БЛОК КОНЕЦ
    """, re.X),
    "MATCH_METHOD": "search",
    },

    9: {

    "PATTERN": re.compile("""

    # Поле типа 9. Число и тип воздушных судов и категория турбулентности следа

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    (# < < < ? ? ? НЕОБЯЗАТЕЛЬНЫЙ БЛОК НАЧАЛО

    # a) Число воздушных судов (если больше одного)
    (?P<Number_of_Aircraft>
        \d{1,2}
    )

    )?# > > > ? ? ? НЕОБЯЗАТЕЛЬНЫЙ БЛОК КОНЕЦ

    # b) Тип воздушного судна
    (?P<Type_of_Aircraft>
        \w{2,4}
    )

    # ДЕЛИТЕЛЬНАЯ КОСАЯ ЧЕРТА
    # OBLIQUE STROKE
        /

    # c) Категория турбулентности следа
    (?P<Wake_Turbulence_Category>
        H|M|L
    )
    """, re.X),
    "MATCH_METHOD": "search",
    },

   10: {

    "PATTERN": re.compile("""

    # Поле типа 10. Оборудование

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    # a) Средства радиосвязи, навигационные средства и средства захода на посадку
    (?P<Radio_Communication_Navigation_and_Approach_Aid_Equipment>
        N?
        [A-Z\d]*
    )

    # ДЕЛИТЕЛЬНАЯ КОСАЯ ЧЕРТА
    # OBLIQUE STROKE
        /

    # b) Оборудование наблюдения
    (?P<Surveillance_Equipment>
        [A-Z]{1,2}
    )

    """, re.X),
    "MATCH_METHOD": "search",
    },

   13: {

    "PATTERN": re.compile("""

    # Поле типа 13. Аэродром и время вылета
    # Field Type 13 — Departure Aerodrome and Time

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    # a) Аэродром вылета
    (?P<Departure_Aerodrome>
        [A-Z]{4}
    )

    (# < < < ? ? ? НЕОБЯЗАТЕЛЬНЫЙ БЛОК НАЧАЛО

    # b) Время
    (?P<Time>
        \d{4}
    )
    )?# > > > ? ? ? НЕОБЯЗАТЕЛЬНЫЙ БЛОК КОНЕЦ

    """, re.X),
    "MATCH_METHOD": "search",
    },

   14: {

    "PATTERN": re.compile("""

    # Поле типа 14. Расчетные данные

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    # a) Пограничный пункт
    (?P<Boundary_Point>
        [A-Z\d]+
    )

    # ДЕЛИТЕЛЬНАЯ КОСАЯ ЧЕРТА
    # OBLIQUE STROKE
        /

    # b) Время пролета пограничного пункта
    (?P<Time_at_Boundary_Point>
        \d{4}
    )

    # c) Разрешенный уровень пролета
    (?P<Cleared_Level>
        ([FA]\d{3})|([SM]\d{4})
    )
    (
        # d) Дополнительные данные о пролете
        (?P<Supplementary_Crossing_Data>
            ([FA]\d{3})|([SM]\d{4})
        )

        # e) Условия пролета
        (?P<Crossing_Condition>
            A|B
        )? # должно быть вместе с d)
    )?

    """, re.X),
    "MATCH_METHOD": "search",
    },

   15: {

    "PATTERN": re.compile("""

   # Поле типа 15. Маршрут
   # Field Type 15 — Route

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    # a) Крейсерская скорость или число Маха
    (?P<Cruising_Speed_or_Mach_Number>
        ([KN]\d{4})|([M]\d{3})
    )

    # b) Запрашиваемый крейсерский уровень
    (?P<Requested_Cruising_Level>
        ([FA]\d{3})|([SM]\d{4})
    )

    # ПРОБЕЛ
    # SPACE
        \s

    # c1) Стандартный маршрут вылета
    (?P<Standard_Departure_Route>
        .*
    )

    """, re.X|re.S),
    "MATCH_METHOD": "search",
    },

   16: {

    "PATTERN": re.compile("""

    # Поле типа 16. Аэродром назначения, общее расчетное
    # истекшее время, запасной(ые) аэродром(ы)
    # Field Type 16 — Destination Aerodrome and Total Estimated
    # Elapsed Time, Alternate Aerodrome(s)

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    # a) Аэродром назначения
    (?P<Destination_Aerodrome>
        [A-Z]{4}
    )

    # b) Общее расчетное истекшее время
    (?P<Total_Estimated_Elapsed_Time>
        \d{4}
    )

    (# < < < ? ? ? НЕОБЯЗАТЕЛЬНЫЙ БЛОК НАЧАЛО

    # ПРОБЕЛ
    # SPACE
        \s

    # c) Запасной(ые) аэродром(ы)
    (?P<Alternate_Aerodromes>
        ([A-Z]{4}(\s))*
        ([A-Z]{4})?
    )

    )?# > > > ? ? ? НЕОБЯЗАТЕЛЬНЫЙ БЛОК КОНЕЦ

    """, re.X),
    "MATCH_METHOD": "search",
    },

   17: {

    "PATTERN": re.compile("""

    # Поле типа 17. Аэродром и время прибытия
    # Field Type 17 — Arrival Aerodrome and Time

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    # a) Аэродром прибытия
    (?P<Arrival_Aerodrome>
        [A-Z]{4}
    )

    # b) Время прибытия
    (?P<Time_of_Arrival>
        \d{4}
    )


    (# < < < ? ? ? НЕОБЯЗАТЕЛЬНЫЙ БЛОК НАЧАЛО

    # ПРОБЕЛ
    # SPACE
        \s

    # c) Название аэродрома прибытия
    (?P<Name_of_Arrival_Aerodrome>
        .*
    )

    )?# > > > ? ? ? НЕОБЯЗАТЕЛЬНЫЙ БЛОК КОНЕЦ

    """, re.X),
    "MATCH_METHOD": "search",
    },

   18: {

   "PATTERN": re.compile("""

    # Поле типа 18. Прочая информация
    # Field Type 18 — Other Information

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    # a) 0 (ноль) при отсутствии прочей информации
    (?P<ZERO>
        0
        (?=
            \s*\Z
        )
    )?

    # EET
    # Основные точки или индексы границ РПИ и суммарное расчетное
    # истекшее время до таких точек или границ РПИ, когда это
    # предписывается на основе региональных аэронавигационных
    # соглашений или соответствующим полномочным органом ОВД

    (?P<EET>
        (?<=
            EET/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # RIF
    # Сведения о маршруте до измененного аэродрома назначения, после
    # чего следует принятый в ИКАО четырехбуквенный индекс местопо-
    # ложения аэродрома. Для использования пересмотренного маршрута
    # необходимо получить новое диспетчерское разрешение в полете.

    (?P<RIF>
        (?<=
            RIF/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # REG
    # Регистрационные знаки воздушного судна только в случае
    # необходимости и, если они отличаются от опознавательного индекса
    # воздушного судна, приведенного в п. 7.

    (?P<REG>
        (?<=
            REG/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # SEL
    # Код SELCAL, если это
    # полномочным органом ОВД.


    (?P<SEL>
        (?<=
            SEL/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # OPR
    # Название эксплуатанта, если его нельзя определить по опознава-
    # тельному индексу воздушного судна, приведенному в п. 7.

    (?P<OPR>
        (?<=
            OPR/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # STS
    # Причины уделения особого внимания со стороны ОВД, например
    # санитарное воздушное судно; воздушное судно с одним неработающим
    # двигателем, например STS/HOSP, STS/ONE ENG INOP.

    (?P<STS>
        (?<=
            STS/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # TYP
    # Тип(ы) воздушного(ых) судна (судов), перед которым(и) при необхо-
    # димости указывается количество воздушных судов, если в п. 9
    # вставлено ZZZZ.

    (?P<TYP>
        (?<=
            TYP/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # PER
    # Летно-технические данные воздушного судна, если это предписывается
    # соответствующим полномочным органом ОВД.

    (?P<PER>
        (?<=
            PER/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # COM
    # Основные данные о связном оборудовании согласно требованиям
    # соответствующего полномочного органа ОВД, например COM/UHF
    # only (только УВЧ-оборудование связи).

    (?P<COM>
        (?<=
            COM/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # DAT
    # Основные данные о наличии возможностей линии передачи данных с
    # использованием одной или нескольких букв S, H, V и M, например,
    # DAT/S – для спутниковой линии передачи данных, DAT/H – для
    # ВЧ-линии передачи данных, DAT/V – для ОВЧ-линии передачи
    # данных, DAT/M – для линии передачи данных ВОРЛ с режимом S.

    (?P<DAT>
        (?<=
            DAT/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # NAV
    # Основные данные о навигационном оборудовании согласно
    # требованию соответствующего полномочного органа ОВД.

    (?P<NAV>
        (?<=
            NAV/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # DEP
    # Название аэродрома вылета, если в п. 13 вставлены ZZZZ или принятый
    # в ИКАО четырехбуквенный индекс местоположения органа ОВД, от
    # которого могут быть получены данные о дополнительном плане полета,
    # если в п. 13 вставлен AFIL.

    (?P<DEP>
        (?<=
            DEP/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # DEST
    # Название аэродрома назначения, если в п. 16 вставлено ZZZZ.

    (?P<DEST>
        (?<=
            DEST/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # ALTN
    # Название запасного(ых) аэродрома(ов) пункта назначения, если в п. 16
    # вставлено ZZZZ.

    (?P<ALTN>
        (?<=
            ALTN/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # RALT
    # Название запасного(ых) аэродрома(ов) на маршруте.

    (?P<RALT>
        (?<=
            RALT/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # CODE
    # Адрес воздушного судна (выраженный в форме буквенно-цифрового
    # кода из шести шестнадцатиричных чисел), если требуется
    # соответствующим полномочным органом ОВД. Например: "F00001" –
    # наименьшее значение адреса воздушного судна, содержащееся в
    # конкретном блоке, регулируемом ИКАО.

    (?P<CODE>
        (?<=
            CODE/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # RMK
    # Любые другие замечания открытым текстом, если это предписывается
    # соответствующим полномочным органом ОВД, или командир
    # воздушного судна считает это необходимым в целях обеспечения
    # обслуживания воздушного движения.

    (?P<RMK>
        (?<=
            RMK/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # PBN
    # Performance Based Navigation

    (?P<PBN>
        (?<=
            PBN/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # SUR
    # Surveillance applications and capabilities

    (?P<SUR>
        (?<=
            SUR/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # DOF
    # Date of flight departure

    (?P<DOF>
        (?<=
            DOF/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # DLE
    # Enroute delay or holding

    (?P<DLE>
        (?<=
            DLE/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # ORGN
    # Originator’s 8 letter AFTN address

    (?P<ORGN>
        (?<=
            ORGN/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # TALT
    # Takeoff alternate

    (?P<TALT>
        (?<=
            TALT/
        )

        .+?

        (
            (?=
                \s+[A-Z]{3,4}/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?


    """, re.X|re.S),
    "MATCH_METHOD": "finditer",
    },

   19: {

    "PATTERN": re.compile("""

    # Поле типа 19. Дополнительная информация
    # Field Type 19 — Supplementary Information

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    # a) Запас топлива (максимальную продолжительность полета) в часах и минутах
    (?P<Fuel_Endurance>
        (?<=
            E/
        )
        \d{4}
    )?

    # b) Общее число лиц на борту
    (?P<Total_Number_of_Persons_on_Board>
        (?<=
            P/
        )
        \d{1,3}
    )?

    # c) Доступность частот или аварийного приводного передатчика
    (?P<Frequency_or_ELT_Availability>
        (?<=
            R/
        )
        [UVE]+
    )?

    # d) Доступность аварийно-спасательного оборудования
    (?P<Survival_Equipment_Availability>
        (?<=
            S/
        )
        [PDMJ]+
    )?

    # e) Спасательные жилеты
    (?P<Life_Jackets>
        (?<=
            J/
        )

        [LFUV]+
    )?

    # f) Спасательные лодки
    (?P<Dinghies>
        (?<=
            D/
        )

        .+?

        (
            (?=
                \s+\w/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    # g) Воздушное судно
    (?P<Aircraft>
        (?<=
            A/
        )

        .+?

        (
            (?=
                \s+\w/
            )
        |
            (?=
                \s*\Z
            )
        )

    )?

    # h) Дополнительные замечания
    (?P<Remarks>
        (?<=
            N/
        )

        .+?

        (
            (?=
                \s+\w/
            )
        |
            (?=
                \s*\Z
            )
        )
    )?

    #i) Фамилия командира воздушного судна
    (?P<Name_of_the_Pilot_in_Command>
        (?<=C/)\w+
    )?
    """, re.X|re.S),

    "MATCH_METHOD": "finditer"
    },

   20: {

    "PATTERN": re.compile("""

    #Поле типа 20. Информация для аварийного оповещения в целях поиска и спасания

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    -?

    # a) Обозначение эксплуатанта
    (?P<Identity_of_Operator>
        \w+
    )

    # ПРОБЕЛ
    # SPACE
        \s+

    # b) Орган, с которым последний раз устанавливалась связь
    (?P<Unit_which_made_Last_Contact>
        \w+
    )

    # ПРОБЕЛ
    # SPACE
        \s+

    # c) Время, когда последний раз устанавливалась двусторонняя связь
    (?P<Time_of_Last_Two_way_Contact>
        \d{4}
    )

    # ПРОБЕЛ
    # SPACE
        \s+

    # d) Частота, на которой последний раз устанавливалась связь
    (?P<Frequency_of_Last_Contact>
        [\d\.,]+
    )

    # ПРОБЕЛ
    # SPACE
        \s+

    # e) Последнее сообщенное местоположение
    (?P<Last_Reported_Position>
        \w+
    )

    # ПРОБЕЛ
    # SPACE
        \s+

    # f) Метод определения последнего известного местоположения
    #    По мере необходимости открытым текстом.
    # g) Действия, предпринятые передающим органом
    #    По мере необходимости открытым текстом.
    # h) Прочая относящаяся к делу информация
    #    По мере необходимости открытым текстом.
    (?P<Other_Information>
        .*?\Z
    )

    """, re.X|re.S),

#    "MATCH_METHOD": "finditer"
    "MATCH_METHOD": "search"
    },

   21: {

    "PATTERN": re.compile("""
    # Поле типа 21. Информация об отказе радиосвязи
    # Field Type 21 — Radio Failure Information

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    -?

    # a) Время, когда последний раз устанавливалась двусторонняя связь
    (?P<Time_of_Last_Two_way_Contact>
        \d{4}
    )

    # ПРОБЕЛ
    # SPACE
        \s+

    # b) Частота, на которой последний раз устанавливалась связь
    (?P<Frequency_of_Last_Contact>
        [\d\.,]+
    )

    # ПРОБЕЛ
    # SPACE
        \s+

    # c) Последнее сообщенное местоположение
    (?P<Last_Reported_Position>
        \w+
    )

    # ПРОБЕЛ
    # SPACE
        \s+

    # d) Время пролета последнего сообщения местоположения
    (?P<Time_at_Last_Reported_Position>
        \d{4}
    )

    # ПРОБЕЛ
    # SPACE
        \s+

    # e) Сохранившиеся возможности ведения связи
    # БУКВЫ, необходимые для указания сохранившихся на борту воздушного
    # судна возможностей ведения связи, если это известно; при этом
    # используются правила группирования данных, предусмотренные для поля
    # типа 10, или открытый текст.

    # f) Любые необходимые замечания
    # По мере необходимости открытым текстом.
    (?P<Remaining_COM_Capability_and_Any_Necessary_Remarks>
        .*?\Z
    )




    """, re.X|re.S),
    "MATCH_METHOD": "search",
    },

   22: {

    "PATTERN": re.compile("""
    # Поле типа 22. Изменение
    # Field Type 22 — Amendment

    # ОДИН ДЕФИС
    # SINGLE HYPHEN

    -?

    # a) Указатель типа
    (?P<Field_Indicator>
        \d{1,2}
    )

    # ДЕЛИТЕЛЬНАЯ КОСАЯ ЧЕРТА
    # OBLIQUE STROKE
        /

    # b) Измененные данные
    (?P<Amended_Data>

        .+

    )

    """, re.X|re.S),
    "MATCH_METHOD": "split_hyphen"
    },
}

ICAO_MSG_FIELDS = {
    "ALR": {
        "FIELDS": (3,  5,  7,  8,  9, 10, 13,     15, 16,     18, 19, 20        )
    },
    "RCF": {
        "FIELDS": (3,      7,                                             21    )
    },

    "FPL": {
        "FIELDS": (3,      7,  8,  9, 10, 13,     15, 16,     18                )
    },
    "DLA": {
        "FIELDS": (3,      7,             13,         16                        )
    },
    "CHG": {
        "FIELDS": (3,      7,             13,         16,                     22)
    },
    "CNL": {
        "FIELDS": (3,      7,             13,         16,                       )
    },
    "DEP": {
        "FIELDS": (3,      7,             13,         16                        )
    },
    "ARR": {
        "FIELDS": (3,      7,             13,         16, 17                    )
    },

    "CPL": {
        "FIELDS": (3,      7,  8,  9, 10, 13, 14, 15, 16,     18                )
    },
    "EST": {
        "FIELDS": (3,      7,             13, 14,     16                        )
    },
    "CDN": {
        "FIELDS": (3,      7,             13,         16,                     22)
    },
    "ACP": {
        "FIELDS": (3,      7,             13,         16                        )
    },
    "LAM": {
        "FIELDS": (3,                                                           )
    },

    "RQP": {
        "FIELDS": (3,      7,             13,         16                        )
    },
    "RQS": {
        "FIELDS": (3,      7,             13,         16                        )
    },
    "SPL": {
        "FIELDS": (3,      7,             13,         16,     18, 19            )
    },
}

def method_finditer(p, text):
    ret = {}
    result = p.finditer(text)
    group_name_by_index = dict( [ (v, k) for k, v in p.groupindex.items() ] )

    for match in result:
        for group_index, group in enumerate( match.groups() ) :
            if group:
                ret[group_name_by_index[ group_index + 1 ]] = group
    return ret

def method_search(p, text):
    ret = {}
    result = p.search(text)
    if result is not None:
        for group_name in p.groupindex:
            ret[group_name] = result.group(group_name)
    return ret

def method_split(p, text, split_pattern=None):
    ret = []
    split = split_pattern.split(text)
    for item in split:
        ret.append(method_finditer(p, item))
    return ret

def method_split_hyphen(p, text):
    pattern_hyphen = re.compile("-")
    return method_split(p, text, pattern_hyphen)

methods = {
    "finditer": method_finditer,
    "search": method_search,
    "split_hyphen": method_split_hyphen
}


class ICAO_ats_msg_parser():
    def __init__(self, raw=None):
        self.raw = raw
        self.msg = None
        self.msg_decoded = None
        self.decode_errors = None

    def extract_msg_from_raw(self, raw=None):
        logging.debug("RAW:\n{RAW}".format(RAW=raw))

        if raw is None:
            raw = self.raw
        if raw is None:
            return None
        ret = None
        raw_lat = cyr2lat(raw)
        logging.debug("RAW_LAT:\n{RAW_LAT}".format(RAW_LAT=raw_lat))
        pattern_msg = re.compile("""

    \(
(?P<Message>

    # ОТКРЫТАЯ СКОБКА
    # OPEN BRACKET

    # a) Индекс типа сообщения
    (?P<Head>
        ALR|RCF|FPL|DLA|CHG|CNL|DEP|ARR|CPL|EST|CDN|ACP|LAM|RQP|RQS|SPL
    )
    # b) Номер сообщения
    (?P<Tail>
        -.*?
    )?


    # ЗАКРЫТАЯ СКОБКА
    # CLOSED BRACKET
)
    \)

""", re.X|re.S)

        match = pattern_msg.search(raw_lat)
        if match is not None:
            ret = match.group(pattern_msg.groupindex["Message"])
        return ret

    def get_fields_list_from_msg(self, msg):
        return msg.split("-")

    def get_msg_type_from_fields_list(self, fields_list):
        msg_type = fields_list[0]
        logging.debug("MSG_TYPE: {MSG_TYPE}".format(MSG_TYPE=msg_type))
        return msg_type

    def get_matrix_by_msg_type(self, msg_type):
        matrix = ICAO_MSG_FIELDS.get(msg_type, {}).get("FIELDS", None)
        logging.debug("MATRIX: {MATRIX}".format(MATRIX=matrix))
        return matrix

    def get_matches_by_combine(self, combine):
        ret = None
        field_number, text = combine
        logging.debug("field: {FIELD} - text: {TEXT}".format(
            FIELD=field_number,
            TEXT=text,
        ))
        pattern_item = ICAO_MSG_PATTERNS[field_number]
        pattern = pattern_item["PATTERN"]
        match_method = pattern_item["MATCH_METHOD"]
        method_func = methods.get(match_method, None)
        if method_func is not None:
            ret = method_func(pattern, text)
        logging.debug(ret)
        return ret

    def decode(self, raw = None):
        if raw is None:
            raw = self.raw
        else:
            self.raw = raw
        if raw is None:
            return None
        ret = {}
        msg = self.extract_msg_from_raw(raw)
        fields_list = self.get_fields_list_from_msg(msg)
        msg_type = self.get_msg_type_from_fields_list(fields_list)
        matrix = self.get_matrix_by_msg_type(msg_type)
        combines = zip(matrix, fields_list)
        for combine in combines:
            matches = self.get_matches_by_combine(combine)
            ret[combine[0]] = matches
        return {
            "PARTS": ret,
            "MSG": {
                "STANDARD": "ICAO",
                "CATEGORY": "ATS",
                "TYPE": ret.get(3, {}).get("Message_Type_Designator", None)
            }
        }
