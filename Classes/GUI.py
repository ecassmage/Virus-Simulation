import tkinter as tk

import Files.FileOpener as FileOpener


class GUI:
    def __init__(self):

        self.stg = FileOpener.openStg()

        self.tk = tk.Tk()
        self.win = tk.Canvas(self.tk, width=self.stg['window']['width'], height=self.stg['window']['height'])

        self.__initializeGraphics__()

    def __initializeGraphics__(self):
        self.win.pack()

    def checkCoordinates(self, Humans):
        try:
            if Humans is None or Humans == "N/A":
                return
            listOfAll = self.win.find_all()
            for human in Humans:
                if human.update:
                    self.win.coords(human.id, human.coord[0]-human.size, human.coord[1]-human.size, human.coord[0]+human.size, human.coord[1]+human.size)
                    self.win.itemconfig(human.id, fill=human.color)
                elif human.id in listOfAll:
                    self.win.delete(human.id)

        except tk.TclError:
            return

    def update(self):
        self.tk.update()

    def mainloop(self):
        self.tk.mainloop()


if __name__ == '__main__':
    gui = GUI()
    gui.tk.mainloop()
    pass
