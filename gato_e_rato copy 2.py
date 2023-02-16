import tkinter as tk
from tkinter import messagebox

# VARIAVEL AUX PARA INICAR JOGO
iniciado = False


# CLASSE DE INTERFACE GRAFICA
class GatoERato:
    def __init__(self, master):
        self.master = master


        self.tom=tk.PhotoImage(file="images\\tom3.png")
        self.jerry=tk.PhotoImage(file="images\\jerry3.png")
        self.vazio=tk.PhotoImage(file="images\\vazio.png")
        self.startt=tk.PhotoImage(file="images\\starttt.png")
        """
        CRIA TABULEIRO ONDE:
            VALORES > 0 = RATO
            VALORES < 0 = GATO
            VALORES = 0 = VAZIO
        """
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

       
        # CHAMADA DA FUNÇÃO QUE CRIA AS CELULAS (BOTOES) DO TABULEIRO
        self.create_widgets()
        
        # CRIANDO BOTAO DE START DO JOGO

        button = tk.Button(self.master, image=self.startt, width=70, height=70, name="startt", command=lambda: self.play(0, 0,1))
        button.grid(row=9,column=3)
        # button = tk.Button(self.master, image=self.start2, width=70, height=70, name="start2", command=lambda: self.play(0, 0,1))
        # button.grid(row=9,column=4)
        
        # CRIANDO JOGADORES
        self.HUMANO = Jogador(1,-1,'G')
        self.COMP = Jogador(6,+1,'R')
    
    # FUNÇÃO QUE CRIA AS CELULAS (BOTOES) DO TABULEIRO
    def create_widgets(self):
        
        for i in range(8):
            for j in range(8):
                if(self.tabuleiro[i][j]==0):
                    # CELULAS = 0  RECEBEM " "
                    simbolo=self.vazio
                elif(self.tabuleiro[i][j]>0):
                    # CELULAS > 0 = RATO 
                    simbolo=self.jerry
                else:
                    # CELULAS < 0 = GATO
                    simbolo=self.tom
                # CRIA CADA CELULA [i,j]
                #button = tk.Button(self.master, image=simbolo, font=("Helvetica", 20), width=70, height=70, name="button"+str(i)+str(j), command=lambda i=i, j=j: self.play(i, j,0))

                button = tk.Button(self.master, image=simbolo, width=70, height=70, name="button"+str(i)+str(j), command=lambda i=i, j=j: self.play(i, j,0))
                button.grid(row=i, column=j)
                button.config(bg="SteelBlue1")
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

                        # CHECA VITORIA
                        check=self.check_win(self.tabuleiro)    
                    if(check=='G'):
                        self.end_game('G')
                    elif(check==None):
                        profundidade = len (celulas_possiveis(self.tabuleiro,self.COMP))
                        if profundidade == 0 or fim_jogo(self):
                            return

                        # limpa_console()
                        print('Vez do Computador [{}]'.format(-1))
                        
                        
                        # VENCER MAIS RAPIDO
                        vencer=-1
                        direcao=0
                        for rato in range(6): 

                            if (self.COMP.px[rato]==6 and self.HUMANO.px[0]!=7 and self.HUMANO.py[0] != self.COMP.py[rato]):
                                # VERIFICA SE RATO ESTIVER A 1 PASSO DE GANHAR, JOGA NELE SEM IR NO MINIMAX
                                vencer = rato
                            if (self.COMP.px[rato]+1==self.HUMANO.px[0]):
                                # VERIFICA SE RATO ESTIVER A 1 PASSO DE CAPTURAR O GATO, JOGA E CAPTURA SEM IR NO MINIMAX
                                if(self.COMP.py[rato]-1==self.HUMANO.py[0]):
                                    vencer = rato
                                    direcao=-1
                                elif(self.COMP.py[rato]+1==self.HUMANO.py[0]):
                                    vencer = rato
                                    direcao=1

                        # OLHA CONDIÇÕES DE VENCER MAIS RAPIDO, SE NÃO, CHAMA MINIMAX
                        if(vencer>=0):
                            x=self.COMP.px[vencer]+1
                            y=self.COMP.py[vencer]+direcao
                            qj=vencer
                    
                        else:
                            move,qj = minimax(self, profundidade, self.COMP, self.HUMANO,1)
                            x, y= move[0], move[1]

                        # ATUALIZA TABULEIRO E INTERFACE
                        self.tabuleiro[x][y]=qj+1
                        self.update_button(x,y)

                        self.tabuleiro[self.COMP.px[qj]][self.COMP.py[qj]] = 0
                        self.update_button(self.COMP.px[qj],self.COMP.py[qj])
                        
                        # ATUALIZA POSIÇÃO DO JOGADOR
                        self.COMP.px[qj]=x
                        self.COMP.py[qj]=y                        
                        
                        # CHECA VITORIA
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
            # CELULAS = 0  RECEBEM " "
            simbolo=self.vazio
        elif(self.tabuleiro[i][j]>0):
            # CELULAS > 0 = RATO 
            simbolo=self.jerry
        else:
            # CELULAS < 0 = GATO
            simbolo=self.tom


        button = self.master.children["button" + str(i) + str(j)]
        button["image"] = simbolo

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

"""
Funcao para avaliacao heuristica do estado.
:parametro (estado): o estado atual do tabuleiro
:returna: +1 se o computador vence; -1 se o HUMANOo vence; 0 empate
 """

def avaliacao(estado,jogador):
    
    vencedor=estado.check_win(estado.tabuleiro)
 
    if vencedor=='R':
        return 500#100000000
    elif vencedor=='G':
        return -500#100000000
    else:      
        
        diagonal = 0
        retorno=[]
        ratovivo=0
        linhagato=0
        for rato in range(6):
            # nao perder rato
            ratovivo=estado.COMP.qnt[rato]+ratovivo
            
        rato=0
        for rato in range(6):              
            # rato na diagonal do outro rato para proteger
            try:
                if ( estado.tabuleiro[estado.COMP.px[rato]+1][estado.COMP.py[rato]-1] > 0):

                    diagonal = 1
                else:
                    diagonal = -1
                if (estado.tabuleiro[estado.COMP.px[rato]+1][estado.COMP.py[rato]+1] > 0):    
                    diagonal = 1
                else:
                    diagonal = -1
            except:
                pass

            
            # gato fora da linha e coluna do rato
            if (estado.COMP.px[rato]==estado.HUMANO.px[0] or estado.COMP.py[rato]==estado.HUMANO.py[0]):
                try:
                    if ( estado.tabuleiro[estado.COMP.px[rato]-1][estado.COMP.py[rato]-1] > 0):

                        linhagato = 1
                    if ( estado.tabuleiro[estado.COMP.px[rato]-1][estado.COMP.py[rato]+1] > 0):

                        linhagato = 1
                except:
                    linhagato = -1

            # rato mais perto do fim

            retorno.append(0.2*estado.COMP.px[rato]+1*ratovivo+7*diagonal+15*linhagato)

        return sum(retorno)

""" fim avaliacao (estado)------------------------------------- """

"""
Testa fim de jogo para ambos jogadores de acordo com estado atual
return: será fim de jogo caso ocorra vitória de um dos jogadores.
"""
def fim_jogo(estado):
    vencedor=estado.check_win(estado.tabuleiro)
           
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
def minimax(estado,profundidade,jogador,proxj,exec):
    jog=0
   
    if profundidade>4:
        profundidade=4
    
    
    if jogador.valor == estado.COMP.valor:
        melhor = [-1, -1, -999999999]
    else:
        melhor = [-1, -1, +999999999]

    if profundidade == 0 or fim_jogo(estado):
        placar = avaliacao(estado,jogador)
        if placar==1:
            placar=placar+1
        return [-1, -1, placar],jog

    for cell, qj in celulas_possiveis(estado.tabuleiro,jogador):
        
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
        
        
        placar , qj = minimax(estado, profundidade - 1, proxj,jogador,exec)
        
        if(jogador.valor==-1):
            estado.tabuleiro[xj][yj]=-1
        else:
            estado.tabuleiro[xj][yj]=aux+1
        
        estado.tabuleiro[x][y]=valAnterior
        jogador.px[aux]=xj
        jogador.py[aux]=yj

        placar[0], placar[1] = x, y

        if jogador.valor == estado.COMP.valor:
            exec=0
            if placar[2] > melhor[2]:
                melhor = placar  # valor MAX
                jog=aux
        else:
            if placar[2] < melhor[2]:
                melhor = placar  # valor MIN
                jog=aux

    return melhor,jog


def main():
    root = tk.Tk()
    root.title("Gato e Rato")
    game = GatoERato(root)
    root.mainloop()


if __name__ == '__main__':
    main()