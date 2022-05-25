#!/opt/homebrew/bin/python3
# -*- coding: UTF-8 -*-

import psycopg2
import datetime

from sshtunnel import SSHTunnelForwarder

from bibliotecas import enviaEmail
from config import transmissores, destinatarios, banco


import asyncio
import telegram

TOKEN = "5336934102:AAEmTN_9-Z12RH3tMbXjasRgKYq0CNGQjo8"
CHAT = "-1001540276501"

async def teste(mensagem):
    bot = telegram.Bot(TOKEN)
    async with bot:
        await bot.send_message(text=mensagem, chat_id=CHAT)




agora = datetime.datetime.now()
agora_str = agora.strftime("%Y-%m-%d %H:%M:%S")

server = SSHTunnelForwarder(('10.61.13.140', 22), ssh_username="devel_web", ssh_password="qweDevel123", remote_bind_address=('10.61.13.140', 5432), local_bind_address=('localhost', 1234))
server.start()

for transmissor in transmissores:
    nome = transmissor[0]
    codigo = transmissor[1]
    database = transmissor[2]
    limite = transmissor[3]

    delta = datetime.timedelta(seconds=120)
    agora = datetime.datetime.now()
    inicio = agora - delta
    data_inicial = inicio.strftime("%s")
    data_final = agora.strftime("%s")
    data_inicial_str = inicio.strftime("%Y-%m-%d %H:%M:%S")

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
    sql = 'select * from %s where itemid = %s and clock >= %s and clock < %s order by clock desc' % (database, codigo, data_inicial, data_final)
    curs.execute(sql)
    linhas = curs.fetchall()

    linhas.reverse()
    if len(linhas) < 6:
        assunto = "Alerta Transmissores - Leitura incompleta - %s" % nome
        mensagem = "Foram identificadas falhas no recebimento de informações em %s\n" % data_inicial_str
        mensagem = mensagem + "Últimas leituras:\n"
        for linha in linhas:
            data = datetime.datetime.fromtimestamp(linha[1])
            data_str = data.strftime("%Y-%m-%d %H:%M:%S")
            # mensagem = mensagem + data_str + ": " + str(int(rec[2])) + '\n'
        # enviaEmail(assunto, mensagem, destinatarios)
    else:
        for rec in linhas:
            data = datetime.datetime.fromtimestamp(rec[1])
            data_str = data.strftime("%Y-%m-%d %H:%M:%S")
            if int(rec[2]) <= limite:
                assunto = "Alerta Transmissores - Potência abaixo do limite - %s" % nome
                mensagem = "A leitura da potência foi %s e o limite é %s" % (str(int(rec[2])), str(limite))
                enviaEmail(assunto, mensagem, destinatarios)
                asyncio.run(teste(assunto + ' ' + mensagem))

                break
    conn.close()
