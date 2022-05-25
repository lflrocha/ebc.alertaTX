

destinatarios = [
    "luis.rocha@ebc.com.br",
    "lflrocha@gmail.com",
    "gilvani.moletta@ebc.com.br",
    "sergio.lima@ebc.com.br",
    "regio.sousa@ebc.com.br",

    # "wagner.bastos@ebc.com.br",
    # "israel.silva@ebc.com.br",
    # "renan.goncalves@ebc.com.br",
    # "jhefferson.silva@ebc.com.br",
    # "pedro.boszczovski@ebc.com.br",
    # "emerson.weirich@ebc.com.br",

]

transmissores = [
    ("TX_MAUA", "96916", "history", 100),
    # ("TX_MENDANHA", "98046", "history", ""),
    ("TX_MENDANHA_RESERVA", "97514", "history", 40),
    ("TX_MOGI", "97111", "history", 40),
    # ("TX_PENA_RESERVA", "97682", "history_uint", 40),
    ("TX_PENA_RJ", "104756", "history", 40),
    ("TX_SAO_LUIS_ANYWAVE", "102650", "history", 1200),
    ("TX_SFN_ITAQUERA", "97439", "history", 100),
    ("TX_SFN_JARAGUA", "97359", "history", 80),
    ("TX_SUMARE_SP", "96286", "history", 6000),
    ("TX_SUMARE_RJ", "102652", "history_text", 1840),
    ("TX_TORRE_DIGITAL", "90204", "history", 600),
    ("TX_TORRE_TV_CONTROLE_DF", "30892", "history_uint", 2000),
]

banco = {
    'database': 'zabbix',
    'user': 'zabbix_telemetria',
    'password': 'zbxt@2021!',
    'host': '10.61.13.140',
    'port': 5432
}
