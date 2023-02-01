import tkinter as tk
from tkinter import messagebox
class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.board = [[" " for i in range(8)] for j in range(8)]
        self.turn = "X"
        self.create_widgets()
        
    def create_widgets(self):
        for i in range(8):
            for j in range(8):
                button = tk.Button(self.master, text=" ", font=("Helvetica", 20), width=3, height=1, name="button"+str(i)+str(j), command=lambda i=i, j=j: self.play(i, j))
                button.grid(row=i, column=j)
                button.config(bg="grey")
                if((i+j)%2==0):
                    button.config(bg="white")
                    
    def play(self, i, j):
        
        if self.board[i][j] == " ":
            self.board[i][j] = self.turn
            self.turn = "O" if self.turn == "X" else "X"
            
            self.update_button(i, j)
            self.check_win()
            
    def update_button(self, i, j):
        
        button = self.master.children["button" + str(i) + str(j)]
        button["text"] = self.board[i][j]
        
    def check_win(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " " or self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                self.end_game(self.board[i][0])
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " " or self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.end_game(self.board[1][1])
        
    def end_game(self, winner):
        messagebox.showinfo("Fim de Jogo", winner + " venceu!")
        self.master.destroy()
        
root = tk.Tk()
root.title("Jogo da Velha")
game = TicTacToe(root)
root.mainloop()
