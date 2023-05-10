import tkinter as tk
from card import *
import os


def create_card_dict():
    folder_path = 'cards'
    file_list = os.listdir(folder_path)

    cards = []
    values = list(CardRank)
    suits = list(Suit)  # ♠ ♣ ♥ ♦
    for value in values:
        for suit in suits:
            card = Card(value, suit)
            cards.append(card)

    dictionary = {}

    for i in range(52):
        dictionary[cards[i]] = file_list[i]

    return dictionary


class Page(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.image_dict = create_card_dict()

        # create a canvas widget for the background image
        self.canvas = tk.Canvas(self, width=900, height=500)
        self.canvas.pack(fill="both", expand=True)

        # create a photo object from the image file and display it on the canvas
        try:
            self.photo = tk.PhotoImage(file="assets\\pokerscreen.png")
            self.card1_img = tk.PhotoImage(file="cards\\02_club.png")
            card2_img = tk.PhotoImage(file="cards\\" + self.image_dict[Card(CardRank.KING, Suit.HEARTS)])

            # place the card images on the canvas at specified coordinates and size
            self.card1_img = tk.PhotoImage(file="cards\\" + self.image_dict[Card(CardRank.ACE, Suit.SPADES)])
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            self.canvas.create_image(440, 360, image=self.card1_img, anchor="nw")
        except tk.TclError as e:
            print("Error loading image:", str(e))
            self.photo = None

        # if self.photo is not None:
            # self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

            # get the card images from the image_dict and resize them
            #card1_img = tk.PhotoImage(file="cards\\" + self.image_dict[Card(CardRank.ACE, Suit.SPADES)])
            #card2_img = tk.PhotoImage(file="cards\\" + self.image_dict[Card(CardRank.KING, Suit.HEARTS)])


            # self.canvas.create_image(0, 0, image=card1_img)

    def show(self):
        self.lift()


root = tk.Tk()
root.geometry("900x500")

page = Page(root)
page.pack(fill="both", expand=True)

root.mainloop()