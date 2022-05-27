#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import datetime
import json
import psycopg2
from sshtunnel import SSHTunnelForwarder

from bibliotecas import enviaEmail
from config import transmissores, destinatarios, banco


hoje = datetime.datetime.combine(datetime.datetime.today() + datetime.timedelta(days=1), datetime.time.min)
ontem = hoje - datetime.timedelta(days=1)
ontem_str =  ontem.strftime("%Y-%m-%d")



hoje_epoch = hoje.strftime("%s")
ontem_epoch = ontem.strftime("%s")
hoje_n_epoch = int(hoje.strftime("%s"))
ontem_n_epoch = int(ontem.strftime("%s"))

server = SSHTunnelForwarder(('10.61.13.140', 22), ssh_username="devel_web", ssh_password="qweDevel123", remote_bind_address=('10.61.13.140', 5432), local_bind_address=('localhost', 1234))
server.start()

texto_email = ""

for transmissor in transmissores:
    print(transmissor)
    nome = transmissor[0]
    codigo = transmissor[1]
    database = transmissor[2]
    limite = transmissor[3]

    params = {
        'database': 'zabbix',
        'user': 'zabbix_telemetria',
        'password': 'zbxt@2021!',
        'host': server.local_bind_host,
        'port': server.local_bind_port
    }
    conn = psycopg2.connect(**params)
    conn.set_session(readonly=True)
    curs = conn.cursor()
    sql = 'select * from %s where itemid = %s and clock >= %s and clock < %s order by clock desc' % (database, codigo, ontem_epoch, hoje_epoch)
    curs.execute(sql)
    linhas = curs.fetchall()
    linhas.reverse()

    lista_dados = []

    for linha in linhas:
        data = datetime.datetime.fromtimestamp(linha[1])
        data_str = data.strftime("%Y-%m-%d %H:%M")
        lista_dados.append([data_str, int(linha[2])])

    d = {}
    for key, value in lista_dados:
       if key not in d.keys():
          d[key] = []
       d[key].append(value)

    print(d)

    processado = {}
    for x in range(ontem_n_epoch, hoje_n_epoch, 60):
        data = datetime.datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M")
        if data in d.keys():
            processado[data] = int(sum(d[data]) / len(d[data]))
        else:
            processado[data] = "Sem dados"



    consolidado = {'ok': 0, 'potencia': 0, 'semdados': 0}
    for item in processado:
        dado = processado[item]
        if dado == "Sem dados":
            consolidado['semdados'] = consolidado['semdados'] + 1
        elif dado < limite:
            consolidado['potencia'] = consolidado['potencia'] + 1
        else:
            consolidado['ok'] = consolidado['ok'] + 1

    with open('consolidado/' + nome + '/' + ontem_str + '.json', 'w') as f:
        json.dump(consolidado, f)

    percentual_potencia = int(consolidado['potencia'] / 1440 * 100)
    percentual_semdados = int(consolidado['semdados'] / 1440 * 100)
    percentual_ok = 100 - percentual_potencia - percentual_semdados

    texto_email = texto_email + nome + '\n'
    texto_email = texto_email + "Operação normal: " + str(percentual_ok) + '%\n'
    texto_email = texto_email + "Potência abaixo do esperado: " + str(percentual_potencia) + '%\n'
    texto_email = texto_email + "Problema na coleta de dados: " + str(percentual_semdados) + '%\n\n'

    conn.close()

assunto = "Transmissores: consolidado do dia %s" % ontem_str
# enviaEmail(assunto, texto_email, destinatarios)

server.close()
