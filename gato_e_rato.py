#!/usr/bin/env python3
# -*- codificacao: utf-8 -*-
"""
Created on Sun Sep 23 15:33:59 2018
@author: talles medeiros, decsi-ufop
"""

"""
Este código servirá de exemplo para o aprendizado do algoritmo MINIMAX 
na disciplina de Inteligência Artificial - CSI457
Semestre: 2018/2
"""

#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system


"""
Um versão simples do algoritmo MINIMAX para o Jogo da Velha.
"""

# Representando a variável que identifica cada jogador
# HUMANO = Oponente humano
# COMP = Agente Inteligente
# tabuleiro = dicionário com os valores em cada posição (x,y)
# indicando o jogador que movimentou nessa posição.
# Começa vazio, com zero em todas posições.
class Jogador():

    def __init__(self, qnt, simbolo,) -> None:
        super().__init__()
        self.qnt=[]
        self.px=[]
        self.py=[]
        for i in range( qnt):
            self.qnt.append(1)
        self.simbolo=simbolo
        # DEFINE POSIÇÕES SE FOR GATO OU RATO, E A POSIÇÃO DE CADA UM EM X E Y
        if(qnt==1): 
            self.px.append(7)
            self.py.append(3)
        else:
            self.px.append(1)
            self.py.append(0)

            self.px.append(1)
            self.py.append(1)

            self.px.append(1)
            self.py.append(2)

            self.px.append(1)
            self.py.append(5)

            self.px.append(1)
            self.py.append(6)

            self.px.append(1)
            self.py.append(7)

            
HUMANO = Jogador(1,-1)
COMP = Jogador(6,+1)

tabuleiro = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, -1, 0, 0, 0, 0],
]




"""
Funcao para avaliacao heuristica do estado.
:parametro (estado): o estado atual do tabuleiro
:returna: +1 se o computador vence; -1 se o HUMANOo vence; 0 empate
 """
def avaliacao(estado):
    
    if vitoria(estado, COMP):
        placar = +1
    elif vitoria(estado, HUMANO):
        placar = -1
    else:
        placar = 0

    return placar
""" fim avaliacao (estado)------------------------------------- """

def vitoria(estado, jogador):
    """
    Esta funcao testa se um jogador especifico vence. Possibilidades:

    SE TEM UM RATO NA ULTIMA LINHA DO TABULEIRO

    :param. (estado): o estado atual do tabuleiro
    :param. (jogador): um HUMANO ou um Computador
    :return: True se jogador vence
    """
    win_estado = [
        # TEM RATO NA LINHA DE BAIXO
        [estado[0][7]], # [0][7]
        [estado[1][7]], # [1][7]
        [estado[2][7]], # [2][7]
        [estado[3][7]], # [3][7]
        [estado[4][7]], # [4][7]
        [estado[5][7]], # [5][7]
        [estado[6][7]], # [6][7]
        [estado[7][7]], # [7][7]    
    ]

    # então o jogador vence!
    if [jogador.simbolo] in win_estado:
        return True
    else:
        return False
""" ---------------------------------------------------------- """

"""
Testa fim de jogo para ambos jogadores de acordo com estado atual
return: será fim de jogo caso ocorra vitória de um dos jogadores.
"""
def fim_jogo(estado):
    return vitoria(estado, HUMANO) or vitoria(estado, COMP)
""" ---------------------------------------------------------- """

"""
Verifica celulas vazias e insere na lista para informar posições
ainda permitidas para próximas jogadas.
"""
def celulas_vazias(estado,jogador):
    celulas = []
    for x, row in enumerate(estado):
        for y, cell in enumerate(row):
            if cell == 0: celulas.append([x, y])
            if jogador.simbolo == -1:
                if cell == +1: celulas.append([x, y])
            else:
                if cell == -1: celulas.append([x, y])
                
    return celulas
""" ---------------------------------------------------------- """

def celulas_vazias2(estado,jogador):
    celulas = []
    
    if(jogador.simbolo==1):

        for j in range(len(jogador.qnt)):
            if (jogador.qnt[j]==1):
                celulas.append([jogador.px[j]+1,jogador.py[j]])

                if(jogador.py[j]<7):
                    if(tabuleiro[jogador.px[j]+1][jogador.py[j]+1]==-1):
                        celulas.append([jogador.px[j]+1,jogador.py[j]+1])
                
                if(jogador.py[j]>0):
                    if(tabuleiro[jogador.px[j]+1][jogador.py[j]-1]==-1):
                        celulas.append([jogador.px[j]+1,jogador.py[j]-1])
                if(jogador.px[j]==1):
                    celulas.append([jogador.px[j]+2,jogador.py[j]])

    else:
        for i in range(jogador.px[0]-1,-1,-1):
            celulas.append([i,jogador.py[0]])
            if(tabuleiro[i][jogador.py[0]]==1):
                break
        for i in range(jogador.py[0]-1,-1,-1):
            celulas.append([jogador.px[0],i])
            if(tabuleiro[jogador.px[0]][i]==1):
                break
        
        for i in range(jogador.px[0]+1,8,1):
            celulas.append([i,jogador.py[0]])
            if(tabuleiro[i][jogador.py[0]]==1):
                break
        for i in range(jogador.py[0]+1,8,1):
            celulas.append([jogador.px[0],i])
            if(tabuleiro[jogador.px[0]][i]==1):
                break
                
    return celulas



"""
Um movimento é valido se a célula escolhida está vazia.
:param (x): coordenada X
:param (y): coordenada Y
:return: True se o tabuleiro[x][y] está vazio ou se tem inimigo
"""
def movimento_valido(x, y,jogador,qj):
    if [x, y] in celulas_vazias2(tabuleiro,jogador):
        return True
    else:
        return False
""" ---------------------------------------------------------- """

"""
Executa o movimento no tabuleiro se as coordenadas são válidas
:param (x): coordenadas X
:param (y): coordenadas Y
:param (jogador): o jogador da vez
:param (qj): referente a qual jogador, por exemplo, Rato 2 (seria o R que está em tabuleiro[1][2] no tabuleiro inicial)
"""
def exec_movimento(x, y, jogador,qj):
    if movimento_valido(x, y,jogador,qj):
        tabuleiro[x][y] = jogador.simbolo
        tabuleiro[jogador.px[qj]][jogador.py[qj]] = 0
        jogador.px[qj]=x
        jogador.py[qj]=y
        return True
    else:
        print("movimento invalido")
        return False
""" ---------------------------------------------------------- """

"""
Função da IA que escolhe o melhor movimento
:param (estado): estado atual do tabuleiro
:param (profundidade): índice do nó na árvore (0 <= profundidade <= 9),
mas nunca será nove neste caso (veja a função iavez())
:param (jogador): um HUMANO ou um Computador
:return: uma lista com [melhor linha, melhor coluna, melhor placar]
"""
def minimax(estado, profundidade, jogador):

    # valor-minmax(estado)
    if jogador == COMP:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]

    # valor-minimax(estado) = avaliacao(estado)
    if profundidade == 0 or fim_jogo(estado):
        placar = avaliacao(estado)
        return [-1, -1, placar]

    for cell in celulas_vazias(estado):
        x, y = cell[0], cell[1]
        estado[x][y] = jogador
        placar = minimax(estado, profundidade - 1, -jogador)
        estado[x][y] = 0
        placar[0], placar[1] = x, y

        if jogador == COMP:
            if placar[2] > melhor[2]:
                melhor = placar  # valor MAX
        else:
            if placar[2] < melhor[2]:
                melhor = placar  # valor MIN
    return melhor
""" ---------------------------------------------------------- """

"""
Limpa o console para SO Windows
"""
def limpa_console():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')
""" ---------------------------------------------------------- """

"""
Imprime o tabuleiro no console
:param. (estado): estado atual do tabuleiro
"""
def exibe_tabuleiro(estado):
    print('\n\n-----------------------------------------')
    for row in estado:
        for cell in row:       
                    
            if cell == +1:
                print('| ', 'R ', end='')
            elif cell == -1:
                print('| ' , 'G ', end='')
            else:
                print('| ','  ', end='')
        print('|\n-----------------------------------------')
""" ---------------------------------------------------------- """

"""
Chama a função minimax se a profundidade < 9,
ou escolhe uma coordenada aleatória.
:param (comp_escolha): Computador escolhe X ou O
:param (humano_escolha): HUMANO escolhe X ou O
:return:
"""
def IA_vez(comp_escolha, humano_escolha):
    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    limpa_console()
    print('Vez do Computador [{}]'.format(comp_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    if profundidade == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(tabuleiro, profundidade, COMP)
        x, y = move[0], move[1]

    exec_movimento(x, y, COMP)
    time.sleep(1)
""" ---------------------------------------------------------- """

def HUMANO_vez(comp_escolha, humano_escolha):
    """
    O HUMANO joga escolhendo um movimento válido
    :param comp_escolha: Computador escolhe X ou O
    :param humano_escolha: HUMANO escolhe X ou O
    :return:
    """
    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    # Dicionário de movimentos válidos
    movimento = -1
    movimentos = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    limpa_console()
    print('Vez do HUMANO [{}]'.format(humano_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    while (movimento < 1 or movimento > 9):
        try:
            movimento = int(input('Use numero (1..9): '))
            coord = movimentos[movimento]
            tenta_movimento = exec_movimento(coord[0], coord[1], HUMANO)

            if tenta_movimento == False:
                print('Movimento Inválido')
                movimento = -1
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Inválida!')
""" ---------------------------------------------------------- """

"""
Funcao Principal que chama todas funcoes
"""
def main():

    limpa_console()
    humano_escolha = '' # Pode ser X ou O
    comp_escolha = '' # Pode ser X ou O
    primeiro = ''  # se HUMANO e o primeiro

    # HUMANO escolhe X ou O para jogar
    while humano_escolha != 'O' and humano_escolha != 'X':
        try:
            print('')
            humano_escolha = input('Escolha X or O\n: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada')

    # Setting Computador's choice
    if humano_escolha == 'X':
        comp_escolha = 'O'
    else:
        comp_escolha = 'X'

    # HUMANO pode começar primeiro
    limpa_console()
    while primeiro != 'S' and primeiro != 'N':
        try:
            primeiro = input('Primeiro a Iniciar?[s/n]: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada!')

    # Laço principal do jogo
    while len(celulas_vazias(tabuleiro)) > 0 and not fim_jogo(tabuleiro):
        if primeiro == 'N':
            IA_vez(comp_escolha, humano_escolha)
            primeiro = ''

        HUMANO_vez(comp_escolha, humano_escolha)
        IA_vez(comp_escolha, humano_escolha)

    # Mensagem de Final de jogo
    if vitoria(tabuleiro, HUMANO):
        limpa_console()
        print('Vez do HUMANO [{}]'.format(humano_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Venceu!')
    elif vitoria(tabuleiro, COMP):
        limpa_console()
        print('Vez do Computador [{}]'.format(comp_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Perdeu!')
    else:
        limpa_console()
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Empate!')

    exit()

# if __name__ == '__main__':
#     main()




exibe_tabuleiro(tabuleiro)
exec_movimento(1,3,HUMANO,0)
exibe_tabuleiro(tabuleiro)

exec_movimento(6,3,HUMANO,0)
exibe_tabuleiro(tabuleiro)