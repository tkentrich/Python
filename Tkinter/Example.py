#!/bin/env python

# Obtained from http://zetcode.com/gui/tkinter/drawing/


from tkinter import Tk, Canvas, Frame, BOTH

class Example(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.initUI()
    def initUI(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)
        # canvas.create_line(X1, Y1, X2, Y2)
        canvas.create_line(15, 25, 200, 25) 
        canvas.create_line(300, 35, 300, 200, dash=(4, 2)) # dash=(line, space)
        canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
        # canvas.create_rectangle(X1, Y1, X2, Y2)
        canvas.create_rectangle(20, 210, 30, 240,
                                outline="#05f", fill="#f05")
        # canvas.create_arc(X1, Y1, X2, Y2)
        canvas.create_arc(60, 210, 120, 240,
                          outline="#e5a", fill="#a85",
                          start=45, extent=270)
        canvas.create_rectangle(60, 210, 120, 240,
                                outline="#05f")
        # points=[X1,Y1,X2,Y2,...]
        points=[135,210,170,200,180,240,125,235]
        canvas.create_polygon(points, outline='#f00', fill='black',
                              dash=(2, 8), width=4)
        
        canvas.pack(fill=BOTH, expand=1)

def main():
    root=Tk()
    ex = Example()
    root.geometry("400x250+300+300")
    root.mainloop()

if __name__ == '__main__':
    main()
