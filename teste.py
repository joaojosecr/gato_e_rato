import tkinter as tk

class TicTacToe(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Jogo da Velha")
        self.geometry("300x300")

        # Create the buttons
        self.buttons = {}
        for i in range(3):
            for j in range(3):
                button = tk.Button(self, text=" ", width=10, height=5, font=("Helvetica", 20))
                button.grid(row=i, column=j)
                self.buttons[(i, j)] = button

        self.player = "X"

    def play(self, i, j):
        button = self.buttons[(i, j)]
        button["text"] = self.player
        self.player = "O" if self.player == "X" else "X"

if __name__ == "__main__":
    game = TicTacToe()
    game.mainloop()
