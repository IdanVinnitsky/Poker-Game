import tkinter as tk


class PokerPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.screen()

    def create_widgets(self):
        # Create a canvas for the table
        self.table_canvas = tk.Canvas(self, width=800, height=600, bg="green")
        self.table_canvas.pack(side="top", pady=20)

        # Create the players
        self.player1_canvas = tk.Canvas(self.table_canvas, width=100, height=100, bg="white")
        self.player1_canvas.place(x=50, y=300)

        self.player2_canvas = tk.Canvas(self.table_canvas, width=100, height=100, bg="white")
        self.player2_canvas.place(x=150, y=200)

        self.player3_canvas = tk.Canvas(self.table_canvas, width=100, height=100, bg="white")
        self.player3_canvas.place(x=250, y=100)

        self.player4_canvas = tk.Canvas(self.table_canvas, width=100, height=100, bg="white")
        self.player4_canvas.place(x=450, y=100)

        self.player5_canvas = tk.Canvas(self.table_canvas, width=100, height=100, bg="white")
        self.player5_canvas.place(x=550, y=200)

        self.player6_canvas = tk.Canvas(self.table_canvas, width=100, height=100, bg="white")
        self.player6_canvas.place(x=650, y=300)

        # Create the flop
        self.flop_canvas = tk.Canvas(self.table_canvas, width=200, height=100, bg="blue")
        self.flop_canvas.place(x=300, y=250)

    def screen(self):
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        height = 650
        width = 1240
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 4)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.master.title('Poker Game')


root = tk.Tk()
poker_page = PokerPage(master=root)
poker_page.mainloop()
