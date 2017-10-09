__author__ = 'Charlie'
import tkinter as tk
import time


class Quitter(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NE+tk.SW)
        self.createWidgets()

    def createWidgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        for q in range(0, 4):
            self.rowconfigure(q, weight=1)
            self.columnconfigure(q, weight=1)

        self.quitButton1 = tk.Button(self, text='Click', command=self.quit)
        self.quitButton1.grid(row=0, column=0, sticky=tk.NE + tk.SW)

        self.quitButton2 = tk.Button(self, text='Any', command=self.quit)
        self.quitButton2.grid(row=1, column=1, sticky=tk.NE + tk.SW)

        self.quitButton3 = tk.Button(self, text='Widget', command=self.quit)
        self.quitButton3.grid(row=2, column=2, sticky=tk.NE + tk.SW)

        self.quitButton4 = tk.Button(self, text="They'll all make you quit", command=self.quit)
        self.quitButton4.grid(row=3, column=0, columnspan=3, sticky=tk.E + tk.NW)

        self.quitButton5 = tk.Button(self, text="Narrow", command=self.quit)
        self.quitButton5.grid(row=0, column=3, rowspan=3, sticky=tk.N + tk.SW)

        self.quitButton6 = tk.Button(self, text='BIG', command=self.quit)
        self.quitButton6.grid(row=3, column=3, ipadx=10, ipady=20,)

        self.quitButton7 = tk.Button(self, text='Stop', command=self.quit)
        self.quitButton7.grid(row=3, column=4, pady=5, sticky=tk.N)

        self.quitButton8 = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton8.grid(row=3, column=4, pady=5, sticky=tk.S)


class Mover(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NE+tk.SW)
        self.config(height=100, width=100)
        self.makeWidgets()

    def makeWidgets(self):
        self.clickIt = tk.Button(self, text="CATCH", command=self.quit)
        self.clickIt.grid(row=0, column=0)

    def makeWidgets2(self):
        self.clickIt2 = tk.Button(self, text="CATCH", command=self.quit)
        self.clickIt2.grid(row=1, column=0)


class Canvassing(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.makeWidgets()

    def makeWidgets(self):
        self.cnvs = tk.Canvas(self, height='10c', width='20c')
        self.cnvs.grid()

    def arcing(self):
        x = 0
        while True:
            OID = self.cnvs.create_arc(0, 0, 20, 20, start=0, extent=x, outline="#f11", fill="#1f1", width=2)
            time.sleep(0.5)
            self.cnvs.delete(OID)
            x = (x + 1) % 360


while True:
    response = input("Which widget ").lower()
    if response == "quitter":
        app = Quitter()
        break
    elif response == "mover":
        app = Mover()
        break
    elif response == "drawer":
        app = Canvassing()
        break

app.master.title('WidgetDemo')
app.mainloop()
app.arcing()