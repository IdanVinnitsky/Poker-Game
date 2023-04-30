import tkinter as tk
from tkinter import messagebox
from tkinter import Tk


class MenuPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.screen()

    def create_widgets(self):
        self.play_button = tk.Button(self, text="Play", command=self.play, width=20, height=5, font=('Arial', 20))
        self.play_button.pack(side="top")

        self.rules_button = tk.Button(self, text="Rules", command=self.rules, width=20, height=5, font=('Arial', 20))
        self.rules_button.pack(side="top")

        self.exit_button = tk.Button(self, text="Exit", command=self.master.quit, width=20, height=5,
                                     font=('Arial', 20))
        self.exit_button.pack(side="bottom")

    def play(self):
        messagebox.showinfo("Play", "Let's play the game!")

    def rules(self):
        messagebox.showinfo("Rules", "Here are the rules of the game:")

    def screen(self):
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        height = 650
        width = 1240
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 4)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.master.title('Account System')


root = tk.Tk()
menu_page = MenuPage(master=root)
menu_page.mainloop()
