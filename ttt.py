import tkinter as tk
from tkinter import messagebox
from math import inf as infinity
from random import choice
import platform
import time
from os import system
import ttt as tela
import datetime

iniciado = False
class TicTacToe:
    def __init__(self, master):
        self.master = master
        
        self.tabuleiro = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 2, 3, 0, 0, 4, 5, 6],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, -1, 0, 0, 0, 0],
        ]

        #self.tabuleiro = [[" " for i in range(8)] for j in range(8)]
        #self.turn = "X"
        button = tk.Button(self.master, text=str("Start"), font=("Helvetica", 20), width=3, height=1, name="start", command=lambda: self.play(0, 0,1))
        button.grid(row=9, column=3)
        self.create_widgets()
        self.HUMANO = Jogador(1,-1,'G')
        self.COMP = Jogador(6,+1,'R')
        
    def create_widgets(self):
        
        for i in range(8):
            for j in range(8):
                if(self.tabuleiro[i][j]==0):
                    simbolo=" "
                elif(self.tabuleiro[i][j]>0):
                    simbolo="R"
                else:
                    simbolo="G"
                button = tk.Button(self.master, text=str(simbolo), font=("Helvetica", 20), width=3, height=1, name="button"+str(i)+str(j), command=lambda i=i, j=j: self.play(i, j,0))
                button.grid(row=i, column=j)
                button.config(bg="grey")
                if((i+j)%2==0):
                    button.config(bg="white")
                  
    def play(self, i, j,inicio):
        global iniciado
        if(inicio==1):
            iniciado = True

        if(iniciado==False):
            return
        else:
        
            jogador=self.HUMANO
            x=i
            y=j
            qj=0
            check=None
            if(check==None):
                x=i
                y=j
                if movimento_valido(x, y,jogador,qj,self.tabuleiro) or inicio == 1:
                    if(inicio==0):
                        if(self.tabuleiro[x][y]>0):
                            self.COMP.px[self.tabuleiro[x][y]-1]=-2
                            self.COMP.py[self.tabuleiro[x][y]-1]=-2
                            self.COMP.qnt[self.tabuleiro[x][y]-1]=0
                            
                        self.tabuleiro[x][y]=jogador.valor
                        #self.tabuleiro[x][y]=jogador.simbolo
                        self.update_button(x,y)

                        self.tabuleiro[jogador.px[qj]][jogador.py[qj]] = 0
                        #self.tabuleiro[jogador.px[qj]][jogador.py[qj]] = 0
                        self.update_button(jogador.px[qj],jogador.py[qj])
                        jogador.px[qj]=x
                        jogador.py[qj]=y

                        
                        print('Vez do Humano [{}]'.format(1))
                        
                        check=self.check_win(self.tabuleiro)    
                    if(check=='G'):
                        self.end_game('G')
                    elif(check==None):
                        profundidade = len (celulas_possiveis(self.tabuleiro,self.COMP))
                        if profundidade == 0 or fim_jogo(self):
                            return

                        # limpa_console()
                        print('Vez do Computador [{}]'.format(-1))
                        #exibe_tabuleiro(self.tabuleiro, 1, -1)
                        
                        move,qj = minimax(self, profundidade, self.COMP, self.HUMANO)
                        x, y= move[0], move[1]

                        self.tabuleiro[x][y]=qj+1
                        self.update_button(x,y)

                        self.tabuleiro[self.COMP.px[qj]][self.COMP.py[qj]] = 0
                        self.update_button(self.COMP.px[qj],self.COMP.py[qj])
                        
                        self.COMP.px[qj]=x
                        self.COMP.py[qj]=y
                        #exec_movimento(x, y, COMP,)
                        

                        check=self.check_win(self.tabuleiro)
                        if(check=='R'):
                            self.end_game('R')
                
                else:
                    print("movimento invalido")    
            # if self.tabuleiro[i][j] == " ":
            #     self.tabuleiro[i][j] = self.turn
            #     self.turn = "O" if self.turn == "X" else "X"
                
            #     self.update_button(i, j)
            #     self.check_win()
                
    def update_button(self, i, j):
        if(self.tabuleiro[i][j]==0):
            simbolo=" "
        elif(self.tabuleiro[i][j]>0):
            simbolo="R"
        else:
            simbolo="G"


        button = self.master.children["button" + str(i) + str(j)]
        button["text"] = simbolo

    def check_win(self,estado):
        #estado=self.tabuleiro
        soma=0
        # SOMA PARA SABER QUANTOS RATOS ESTAO VIVOS
        somaG=0

        win_estado = []
            # TEM RATO NA LINHA DE BAIXO
        win_estado.append(estado[7][0]) # [0][7]
        win_estado.append(estado[7][1]) # [1][7]
        win_estado.append(estado[7][2]) # [2][7]
        win_estado.append(estado[7][3]) # [3][7]
        win_estado.append(estado[7][4]) # [4][7]
        win_estado.append(estado[7][5]) # [5][7]
        win_estado.append(estado[7][6]) # [6][7]
        win_estado.append(estado[7][7]) # [7][7]    

        for x in range(len(win_estado)):
            if (win_estado[x]>0):
                return self.COMP.simbolo
        # então o jogador vence!

        for line in estado:
            for cell in line:   
                if cell>0:
                    soma=soma+1
                if cell < 0:
                    somaG=1 
        

        # CONFERE SE TEM ALGUM RATO VIVO
        if(soma==0): return self.HUMANO.simbolo
        # CONFERE SE GATO TA MORTO
        if(somaG==0): return self.COMP.simbolo



        return None
         
    def end_game(self, winner):
        global iniciado
        iniciado = False
        messagebox.showinfo("Fim de Jogo", winner + " venceu!")
        self.master.destroy()


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

"""
Um versão simples do algoritmo MINIMAX para o Jogo da Velha.

# Representando a variável que identifica cada jogador
# HUMANO = Oponente humano
# COMP = Agente Inteligente
# tabuleiro = dicionário com os valores em cada posição (x,y)
# indicando o jogador que movimentou nessa posição.
# Começa vazio, com zero em todas posições.
"""
class Jogador():

    def __init__(self, qnt, valor, simbolo) -> None:
        super().__init__()
        self.qnt=[]
        self.px=[]
        self.py=[]
        for i in range( qnt):
            self.qnt.append(1)
        self.simbolo=simbolo
        self.valor=valor
        
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

            
HUMANO = Jogador(1,-1,'G')
COMP = Jogador(6,+1,'R')

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
    
    vencedor=estado.check_win(estado.tabuleiro)
    #print(vencedor)         
    if vencedor=='R':
        return 100000000
    elif vencedor=='G':
        return -100000000
    else:
        aux=0
        diagonal = 0
        retorno=[]
        ratovivo=0
        linhagato=0
        for rato in range(6):
            # nao perder rato
            ratovivo=estado.COMP.qnt[rato]+ratovivo
            
        rato=0
        for rato in range(6):    
            # if (rato == 1 or rato == 4):
            #     aux=1
            # else:
            #     aux=0
            
           
            # rato na diagonal do outro rato para proteger
            try:
                if ( estado.tabuleiro[estado.COMP.px[rato]+1][estado.COMP.py[rato]-1] > 0):

                    diagonal += 9
                else:
                    diagonal -= 4
                if (estado.tabuleiro[estado.COMP.px[rato]+1][estado.COMP.py[rato]+1] > 0):    
                    diagonal += 9
                else:
                    diagonal -= 4
            except:
                print("")

            
            # gato fora da linha e coluna do rato
            if (estado.COMP.px[rato]==estado.HUMANO.px[0] or estado.COMP.py[rato]==estado.HUMANO.py[0]):

                linhagato = - 9
                try:
                    if ( estado.tabuleiro[estado.COMP.px[rato]-1][estado.COMP.py[rato]-1] > 0):

                        linhagato = 8
                    if ( estado.tabuleiro[estado.COMP.px[rato]-1][estado.COMP.py[rato]+1] > 0):

                        linhagato = 8
                except:
                    print("")

            # rato mais perto do fim
            retorno.append(estado.COMP.px[rato]+2*ratovivo+aux+diagonal+linhagato)
        return max(retorno)

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
    vencedor=estado.check_win(estado.tabuleiro)
    #print(vencedor)         
    if vencedor=='R':
        return True
    elif vencedor=='G':
        return True
    else:
        return False
        
""" ---------------------------------------------------------- """

"""
Verifica celulas vazias e insere na lista para informar posições
ainda permitidas para próximas jogadas.
"""

def celulas_possiveis(tabuleiro,jogador):
    celulas = []
    
    if(jogador.valor==1):
         
        for j in range(len(jogador.qnt)):
            if(jogador.qnt[j]>0):
                if(jogador.px[j]<7):
                    if (tabuleiro[jogador.px[j]+1][jogador.py[j]]==0):
                        celulas.append([[jogador.px[j]+1,jogador.py[j]],j])

                    if(jogador.py[j]<7):
                        if(tabuleiro[jogador.px[j]+1][jogador.py[j]+1]==-1):
                            celulas.append([[jogador.px[j]+1,jogador.py[j]+1],j])
                    
                    if(jogador.py[j]>0):
                        if(tabuleiro[jogador.px[j]+1][jogador.py[j]-1]==-1):
                            celulas.append([[jogador.px[j]+1,jogador.py[j]-1],j])
                if(jogador.px[j]==1):
                    if (tabuleiro[jogador.px[j]+2][jogador.py[j]]==0):
                        celulas.append([[jogador.px[j]+2,jogador.py[j]],j])

    else:
        for i in range(jogador.px[0]-1,-1,-1):
            celulas.append([[i,jogador.py[0]],0])
            if(tabuleiro[i][jogador.py[0]]>0):
                break
        for i in range(jogador.py[0]-1,-1,-1):
            celulas.append([[jogador.px[0],i],0])
            if(tabuleiro[jogador.px[0]][i]>0):
                break
        
        for i in range(jogador.px[0]+1,8,1):
            celulas.append([[i,jogador.py[0]],0])
            if(tabuleiro[i][jogador.py[0]]>0):
                break
        for i in range(jogador.py[0]+1,8,1):
            celulas.append([[jogador.px[0],i],0])
            if(tabuleiro[jogador.px[0]][i]>0):
                break
                
    return celulas


"""
Um movimento é valido se a célula escolhida está vazia.
:param (x): coordenada X
:param (y): coordenada Y
:return: True se o tabuleiro[x][y] está vazio ou se tem inimigo
"""
def movimento_valido(x, y,jogador,qj,tabuleiro):
    if [[x, y],0] in celulas_possiveis(tabuleiro,jogador):
        return True
    else:
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

""" ---------------------------------------------------------- """
def minimax(estado,profundidade,jogador,proxj):
    jog=0
    #limpa_console()
    if profundidade>4:
        profundidade=4
    if jogador.valor == COMP.valor:
        melhor = [-1, -1, -999999999]
    else:
        melhor = [-1, -1, +999999999]

    if profundidade == 0 or fim_jogo(estado):
        placar = avaliacao(estado)
        if placar==1:
            placar=placar+1
        return [-1, -1, placar],jog


    #print celulas_possiveis(estado.tabuleiro,jogador))
    for cell, qj in celulas_possiveis(estado.tabuleiro,jogador):
        #print(cell,profundidade)
        x=cell[0]
        y=cell[1]
        aux=qj
        valAnterior=estado.tabuleiro[x][y]

        estado.tabuleiro[jogador.px[aux]][jogador.py[aux]]=0
        if(jogador.valor==-1):
            estado.tabuleiro[x][y]=-1
        else:
            estado.tabuleiro[x][y]=aux+1
        xj=jogador.px[aux]
        yj=jogador.py[aux]
        jogador.px[aux]=x
        jogador.py[aux]=y

        if jogador.valor == COMP.valor:
            placar , qj = minimax(estado, profundidade - 1, proxj,jogador)
        else:
            placar , qj = minimax(estado, profundidade - 1, proxj,jogador)

        if(jogador.valor==-1):
            estado.tabuleiro[xj][yj]=-1
        else:
            estado.tabuleiro[xj][yj]=aux+1
        
        estado.tabuleiro[x][y]=valAnterior
        jogador.px[aux]=xj
        jogador.py[aux]=yj

        placar[0], placar[1] = x, y

        if jogador.valor == COMP.valor:
            if placar[2] > melhor[2]:
                melhor = placar  # valor MAX
                jog=aux

        else:
            if placar[2] < melhor[2]:
                melhor = placar  # valor MIN
                jog=aux

    return melhor,jog


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



def main():
    root = tk.Tk()
    root.title("Jogo da Velha")
    game = TicTacToe(root)
    root.mainloop()


if __name__ == '__main__':
    main()
