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
    def __init__(self, identificacao, valor, peso):
        self.id = identificacao  # IDENTIFICADOR
        self.valor = valor
        self.peso = peso

    def __repr__(self):  # MOSTRAR COMO O OBJETO VAI SER REPRESENTADO EM UM PRINT
        return 'Objeto(%i)' % self.id


class Combinacao:  # CLASSE PARA MONTAR COMBINAÇÕES DE OBJETOS (BASICAMENTE A MOCHILA)
    def __init__(self):
        self.valor = 0
        self.objetos = []

    def addObjeto(self, objeto):
        self.valor = self.valor + objeto.valor
        self.objetos = self.objetos + [objeto]
        return self

    def __repr__(self):
        return 'Valor: %i, %i Objetos' % (self.valor, len(self.objetos))


def knapSack(objs, we):
    # GERAR UMA MATRIZ DE n_itens + 1 x tamanho_da_mochila + 1
    # ESTA MATRIZ É A BASE DO ALGORITMO O-1 DO PROBLEMA DA MOCHILA
    # EXPLICAÇÃO À PARTIR DOS @21:00 LINK: https://www.youtube.com/watch?v=SJSRKnxu9Ig
    # PREENCHER A MATRIZ COM CLASSES DE COMBINAÇÃO
    k = [[Combinacao() for x in range(we + 1)] for x in range(len(objs) + 1)]

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
                    k[i][j] = k[i - 1][j - obj.peso]
                    k[i][j] = k[i][j].addObjeto(obj)

                # SE NÃO, DEIXE COMO ESTÁ
                else:
                    k[i][j] = k[i - 1][j]

            # DEIXAR COMO ESTÁ TAMBÉM
            else:
                k[i][j] = k[i - 1][j]

    # RETORNAR ÚLTIMA COMBINAÇÃO DA MATRIZ
    return k[len(objs) - 1][we]


# VALORES PARA TESTAR O ALGORITMO

# LISTA DE OBJETOS
OBJS = [
    Objeto(1, 6, 1),
    Objeto(2, 10, 2),
    Objeto(3, 12, 3),
    # Objeto(4, 23, 5)
]
W = 5  # PESO MÁXIMO DA MOCHILA

# INICIAR O ALGORITMO COM OS VALORES DEFINIDOS ACIMA
comb = knapSack(OBJS, W)

# MOSTRAR OS RESULTADOS NO TERMINAL
print('Valor: %i, Peso Total: %i' % (comb.valor, len(comb.objetos)))
for objeto in comb.objetos:
    print('ID: %i, Valor: %i, Peso: %i' % (objeto.id, objeto.valor, objeto.peso))
