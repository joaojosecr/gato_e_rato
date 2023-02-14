import tkinter as tk

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo da Velha")
        self.master.geometry("300x300")
        self.turn = 'X'
        self.buttons = []
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.master, text="", font=("Helvetica", 24), width=5, height=2, command=lambda row=i, col=j: self.play(row, col))
                btn.grid(row=i, column=j)
                self.buttons.append(btn)

    def play(self, row, col):
        self.buttons[row * 3 + col].config(text=self.turn, state='disabled')
        self.turn = 'O' if self.turn == 'X' else 'X'
        self.check_win()

    def check_win(self):
        for i in range(3):
            if self.buttons[i].cget('text') == self.buttons[i+3].cget('text') == self.buttons[i+6].cget('text') != '':
                self.win(self.buttons[i].cget('text'))
            if self.buttons[i*3].cget('text') == self.buttons[i*3+1].cget('text') == self.buttons[i*3+2].cget('text') != '':
                self.win(self.buttons[i*3].cget('text'))
        if self.buttons[0].cget('text') == self.buttons[4].cget('text') == self.buttons[8].cget('text') != '':
            self.win(self.buttons[0].cget('text'))
        if self.buttons[2].cget('text') == self.buttons[4].cget('text') == self.buttons[6].cget('text') != '':
            self.win(self.buttons[2].cget('text'))

    def win(self, player):
        for btn in self.buttons:
            btn.config(state='disabled')
        tk.messagebox.showinfo("Jogo da Velha", player + " venceu!")

root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
