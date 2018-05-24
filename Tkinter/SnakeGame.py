#!/bin/env python
from Tkinter import *

class Snake(Tk):
    def __init__(self):
        WIDTH=300
        HEIGHT=300
        
        Tk.__init__(self)

        self.title("Snake")

        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.grid(columnspan=3)
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.create)
        self.canvas.bind("<Key>", self.create)

        newGame = Button(self, text="New Game", command=self.new_game)
        newGame.grid(row=1, column=0, sticky=E)

        self.score_label = Label(self)
        self.score_label.grid(row=1, column=1)

        self.score_label = Label(self)
        self.score_label.grid(row=1, column=2)

        self.new_game()
        self.redraw()

    def new_game(self):
        self.lives = 3
        self.score = 0
        self.mainloop()

    def redraw(self):
        self.score_label.text="00000"

    def create(self, origin):
        pass

if __name__ == '__main__':
    Snake()
