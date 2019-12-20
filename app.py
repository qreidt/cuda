# ALGORITMO PARA SOLUÇÃO DO PROBLEMA DA MOCHILA
# INICIALMENTE BASEADO EM:
# https://www.geeksforgeeks.org/python-program-for-dynamic-programming-set-10-0-1-knapsack-problem/

# O ALGORITMO ORIGINAL RECEBE OS DADOS EM DOIS ARRAYS DISTINTOS E APENAS
# RETORNA O VALOR DA MELHOR COMBINAÇÃO

# ALGORITMO ATUAL RECEBE UM ALGORITMO DE OBJETOS (CADA OBJETO É UMA CLASSE QUE POSSUI UMA
# IDENTIFICAÇÃO ÚNICA, UM PESO E UM VALOR) E RETORNA UMA COMBINAÇÃO (CLASSE QUE CONTÉM UM O
# VALOR TOTAL DA COMBINAÇÃO E LISTA DE OBJETOS PARA ATINGIR TAL COMBINAÇÃO)

from builtins import range, len, enumerate


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
        return 'Valor: %i, %i Objetos' % (self.valor, len(self.objetos))


def knapSack(objs, we):
    # GERAR UMA MATRIZ DE n_itens + 1 x tamanho_da_mochila + 1
    # ESTA MATRIZ É A BASE DO ALGORITMO O-1 DO PROBLEMA DA MOCHILA
    # EXPLICAÇÃO À PARTIR DOS @21:00 LINK: https://www.youtube.com/watch?v=SJSRKnxu9Ig
    # PREENCHER A MATRIZ COM CLASSES DE COMBINAÇÃO
    k = [[Mochila() for x in range(we + 1)] for x in range(len(objs) + 1)]

    # EXTENDER O ARRAY DE OBJETOS
    objs = [objs[0]] + objs

    # TRABALHAR NA MATRIZ K[][] DE MANEIRA BOTTOM UP
    # PULANDO A PRIMEIRA LINHA DA MATRIZ
    for i, obj in enumerate(objs[1:], start=1):

        # PERCORRER A LINHA DE COMBINAÇÕES PULANDO A
        # PRIMEIRA COLUNA DA LINHA
        for j, combinacao in enumerate(k[i][1:], start=1):

            # LIMITAR O TAMANHO DO OBJETO QUE VAI ENTRAR NA COMBINAÇÃO
            # A MEDIDA QUE ELE VAI PERCORRENDO A LINHA, ELE LIBERA OBJETOS MAIORES
            # E A COMBINAÇÃO É FEITA COM OBJETOS MENORES DA LINHA ANTERIOR ( POR ISSO MANTER A PRIMEIRA LINHA VAZIA )
            if obj.peso <= j:

                # CALCULAR NOVO VALOR
                value = obj.valor + k[i - 1][j - obj.peso].valor

                # SE O NOVO VALOR FOR MAIOR DO QUE O OBTIDO NA LINHA ANTERIOR
                if value > k[i - 1][j].valor:

                    # ADICIONAR OBJETO À COMBINAÇÃO DA LINHA ANTERIOR
                    k[i][j] = k[i - 1][j - obj.peso].addObjeto(obj)

                # SE NÃO, DEIXE COMO ESTÁ
                else:
                    k[i][j] = k[i - 1][j]

            # DEIXAR COMO ESTÁ TAMBÉM
            else:
                k[i][j] = k[i - 1][j]

    # RETORNAR ÚLTIMA COMBINAÇÃO DA MATRIZ
    return k[len(objs) - 1][we]


# VALORES PARA TESTAR O ALGORITMO

W = 550  # PESO MÁXIMO DA MOCHILA

# LISTA DE OBJETOS
OBJS = [
    # Objeto(1, 6, 1),
    # Objeto(2, 10, 2),
    # Objeto(3, 12, 3),
    # Objeto(4, 23, 5)
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
    Objeto(28, 15, 9),
]

# INICIAR O ALGORITMO COM OS VALORES DEFINIDOS ACIMA
comb = knapSack(OBJS, W)

peso_total = 0
for item in comb.objetos:
    peso_total = peso_total + item.peso

# MOSTRAR OS RESULTADOS NO TERMINAL
print('Valor: %i' % comb.valor)
print('Peso Total: %i' % peso_total)
print('Objetos: %i' % len(comb.objetos))
for objeto in comb.objetos:
    print('\t' + 'ID: %i, Valor: %i, Peso: %i' % (objeto.id, objeto.valor, objeto.peso))
