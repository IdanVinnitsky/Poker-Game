import tkinter as tk
from tkinter import messagebox
from pokerpage import *

def play():
    messagebox.showinfo("Play", "Let's play the game!")
    main()


def rules():
    messagebox.showinfo("Rules", "Here are the rules of the game:")


class MenuPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.canvas = tk.Canvas(self, width=900, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.photo = tk.PhotoImage(file="assets\\menu.png")
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        x = 380
        y = 100

        self.play_button = tk.Button(self, text="Play", command=play,
                                     width=10, height=2, font=('Arial', 20), bg="green")
        self.play_button.place(x=x, y=y)

        self.rules_button = tk.Button(self, text="Rules", command=rules,
                                      width=10, height=2, font=('Arial', 20), bg="green")
        self.rules_button.place(x=x, y=y + 100)

        self.exit_button = tk.Button(self, text="Exit", command=self.master.quit,
                                     width=10, height=2, font=('Arial', 20), bg="green")
        self.exit_button.place(x=x, y=y + 200)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("900x500")
    menu_page = MenuPage(master=root)
    menu_page.mainloop()
