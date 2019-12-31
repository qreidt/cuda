# ALGORITMO PARA SOLUÇÃO DO PROBLEMA DA MOCHILA
# INICIALMENTE BASEADO EM:
# https://www.geeksforgeeks.org/python-program-for-dynamic-programming-set-10-0-1-knapsack-problem/

# O ALGORITMO ORIGINAL RECEBE OS DADOS EM DOIS ARRAYS DISTINTOS E APENAS
# RETORNA O VALOR DA MELHOR COMBINAÇÃO

# ALGORITMO ATUAL RECEBE UM ALGORITMO DE OBJETOS (CADA OBJETO É UMA CLASSE QUE POSSUI UMA
# IDENTIFICAÇÃO ÚNICA, UM PESO E UM VALOR) E RETORNA UMA COMBINAÇÃO (CLASSE QUE CONTÉM UM O
# VALOR TOTAL DA COMBINAÇÃO E LISTA DE OBJETOS PARA ATINGIR TAL COMBINAÇÃO)

from builtins import range, len, enumerate
from math import ceil, floor
from threading import Thread
from datetime import datetime


class Objeto:  # CLASSE PARA FACILITAR A MANIPULAÇÃO DE ITENS
    def __init__(self, identificacao, peso, valor):
        self.id = identificacao  # IDENTIFICADOR
        self.peso = peso
        self.valor = valor

    def __repr__(self):  # MOSTRAR COMO O OBJETO VAI SER REPRESENTADO EM UM PRINT
        return 'Objeto(%i)' % self.id


class Mochila:  # CLASSE PARA MONTAR COMBINAÇÕES DE OBJETOS (BASICAMENTE A MOCHILA)
    def __init__(self):
        self.valor = 0
        self.objetos = []

    def addObjeto(self, objeto):
        mochila = Mochila()
        mochila.valor = self.valor + objeto.valor
        mochila.objetos = self.objetos + [objeto]
        return mochila

    def __repr__(self):
        # return 'Valor: %i, %i Objetos' % (self.valor, len(self.objetos))
        return 'Combinacao(%i)' % self.valor


def knapSackThread(start, end, i, obj):
    global K

    # PERCORRER A LINHA DE COMBINAÇÕES PULANDO A
    # PRIMEIRA COLUNA DA LINHA
    for j in range(start, end + 1):

        # LIMITAR O TAMANHO DO OBJETO QUE VAI ENTRAR NA COMBINAÇÃO
        # A MEDIDA QUE ELE VAI PERCORRENDO A LINHA, ELE LIBERA OBJETOS MAIORES
        # E A COMBINAÇÃO É FEITA COM OBJETOS MENORES DA LINHA ANTERIOR ( POR ISSO MANTER A PRIMEIRA LINHA VAZIA )
        if obj.peso <= j:

            # CALCULAR NOVO VALOR
            value = obj.valor + K[i - 1][j - obj.peso].valor

            # SE O NOVO VALOR FOR MAIOR DO QUE O OBTIDO NA LINHA ANTERIOR
            if value > K[i - 1][j].valor:

                # ADICIONAR OBJETO À COMBINAÇÃO DA LINHA ANTERIOR
                K[i][j] = K[i - 1][j - obj.peso].addObjeto(obj)

            # SE NÃO, DEIXE COMO ESTÁ
            else:
                K[i][j] = K[i - 1][j]

        # DEIXAR COMO ESTÁ TAMBÉM
        else:
            K[i][j] = K[i - 1][j]


def knapSack(num_threads):
    global OBJS, K, W

    # EXTENDER O ARRAY DE OBJETOS
    OBJS.insert(0, OBJS[0])

    # GERAR UMA MATRIZ DE n_itens + 1 x tamanho_da_mochila + 1
    # ESTA MATRIZ É A BASE DO ALGORITMO O-1 DO PROBLEMA DA MOCHILA
    # EXPLICAÇÃO À PARTIR DOS @21:00 LINK: https://www.youtube.com/watch?v=SJSRKnxu9Ig
    # PREENCHER A MATRIZ COM CLASSES DE COMBINAÇÃO
    K = [[Mochila() for x in range(W + 1)] for x in range(len(OBJS))]

    # REALIZAR A DIVISÃO DE QUANTOS ITENS CADA THREAD IRA CALCULAR DE CADA LINHA
    per_thread = W / NUM_THREADS

    # CASO SEJA UM NÚMERO INTEIRO, A ULTIMA THREAD IRA TER A MESMA QUANTUDADE QUE AS OUTRAS
    if per_thread == ceil(per_thread):
        last_thread = per_thread - 1
        per_thread = per_thread - 1

    # CASO NÃO SEJA, A ULTIMA THREAD IRÁ RECEBER UM ITEM A MAIS POR CADA LINHA
    else:
        last_thread = ceil(per_thread) - 1
        per_thread = floor(per_thread) - 1

    # PASSAR AS VARIAVEIS DE FLOAT PARA INT
    per_thread = int(per_thread)
    last_thread = int(last_thread)

    # INICIAR ARRAY DE THREADS
    threads = []
    for t in range(num_threads):
        threads.append(0)

    # TRABALHAR NA MATRIZ K[][] DE MANEIRA BOTTOM UP
    # PULANDO A PRIMEIRA LINHA DA MATRIZ
    for i, obj in enumerate(OBJS[1:], start=1):

        start = 1  # INICIAR SEMPRE NA SEGUNDA COLUNA
        end = start + per_thread

        # INICIAR THREADS E IR PASSANDO O INTERVALO DE CADA UMA
        for t, thread in enumerate(threads):
            # INICIAR A THREAD PASSANDO QUANDO FUNÇÃO ELA DEVE EXECUTAR E SEUS PARÂMETROS
            threads[t] = Thread(target=knapSackThread, args=(start, end, i, obj))

            # TACA-LE PAU NA THREAD
            threads[t].start()

            # ATUALIZAR INTERVALO
            start = start + end
            if t + 2 == num_threads and per_thread != last_thread:
                end = start + last_thread
            else:
                end = start + per_thread

        # JUNTAR TODAS AS THREADS À THREAD PRINCIPAL
        for thread in threads:
            thread.join()

    # RETORNAR ÚLTIMA COMBINAÇÃO DA MATRIZ
    return K[len(OBJS) - 1][W]


# VALORES PARA TESTAR O ALGORITMO

NUM_THREADS = 2  # NÚMEDO DE THREADS
W = 550  # PESO MÁXIMO DA MOCHILA

# LISTA DE OBJETOS
OBJS = [
    # Objeto(1, 1, 8),
    # Objeto(2, 2, 10),
    # Objeto(3, 3, 12),
    # Objeto(4, 23, 5),
    Objeto(1, 26, 27),
    Objeto(2, 17, 31),
    Objeto(3, 23, 34),
    Objeto(4, 6, 8),
    Objeto(5, 5, 29),
    Objeto(6, 15, 21),
    Objeto(7, 28, 22),
    Objeto(8, 19, 24),
    Objeto(9, 20, 7),
    Objeto(10, 5, 25),
    Objeto(11, 15, 15),
    Objeto(12, 32, 32),
    Objeto(13, 11, 19),
    Objeto(14, 16, 32),
    Objeto(15, 11, 28),
    Objeto(16, 23, 28),
    Objeto(17, 30, 16),
    Objeto(18, 14, 28),
    Objeto(19, 20, 34),
    Objeto(20, 15, 11),
    Objeto(21, 26, 21),
    Objeto(22, 30, 16),
    Objeto(23, 30, 33),
    Objeto(24, 30, 27),
    Objeto(25, 18, 29),
    Objeto(26, 31, 22),
    Objeto(27, 35, 17),
    Objeto(28, 15, 9)
]

# OBS: TODAS AS VARIAVEIS DECLARADAS AQUI PODEM SER CONSIDERADAS GLOBAIS

K = []

antes_de_executar = datetime.now()  # ARMAZENAR DATA E HORA DO MOMENTO ANTES DE EXECUTAR O ALGORITMO

melhor_combinacao = knapSack(NUM_THREADS)  # INICIAR O ALGORITMO COM OS VALORES DEFINIDOS ACIMA

depois_de_executar = datetime.now()  # ARMAZENAR DATA E HORA DO MOMENTO DEPOIS DO ALGORITMO FINALIZAR

peso_total = 0
for item in melhor_combinacao.objetos:
    peso_total = peso_total + item.peso

# MOSTRAR OS RESULTADOS NO TERMINAL
print('Tempo de execução: ' + str(depois_de_executar - antes_de_executar))
print('Valor: %i' % melhor_combinacao.valor)
print('Peso Total: %i' % peso_total)
print('Objetos: %i' % len(melhor_combinacao.objetos))

for objeto in melhor_combinacao.objetos:
    print('\t' + 'ID: %i, Valor: %i, Peso: %i' % (objeto.id, objeto.valor, objeto.peso))

