# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unicodedata import normalize
import locale


def moeda(valor):
    valor = locale.currency(valor, grouping=True, symbol=False)
    return '{}'.format(valor)


def moeda_real(numero):
    try:
        contador = 0
        valor_y = ''
        num = numero.__str__()
        if '.' in num:
            preco, centavos = num.split('.')
        else:
            preco = num
            centavos = '00'

        tamanho = len(preco)
        while tamanho > 0:
            valor_y = valor_y + preco[tamanho - 1]
            contador += 1
            if contador == 3 and tamanho > 1:
                valor_y = valor_y + '.'
                contador = 0
            tamanho -= 1

        tamanho = len(valor_y)
        valor_x = ''
        while tamanho > 0:
            valor_x = valor_x + valor_y[tamanho - 1]
            tamanho -= 1

        return "R$ {},{}".format(valor_x, centavos)
    except:
        return numero


def dia_da_semana(dia):
    dia = dia.weekday()
    dias = (u'Segunda-feira', u'Terça-feira', u'Quarta-feira', u'Quinta-feira', u'Sexta-feira', u'Sábado', u'Domingo')
    return dias[dia]


def normalizar(texto):
    return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').lower()


def NORMALIZAR(texto):
    return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').upper()


def Normalizar(texto):
    return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').capitalize()

