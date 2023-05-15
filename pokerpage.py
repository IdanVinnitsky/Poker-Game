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

def button_clicked():
    print("Button clicked!")


class PokerScreen(tk.Frame):
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

            # place the card images on the canvas at specified coordinates and size
            self.card1_img = tk.PhotoImage(file="cards\\" + self.image_dict[Card(CardRank.ACE, Suit.SPADES)])
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            self.canvas.create_image(440, 360, image=self.card1_img, anchor="nw")
            self.canvas.create_image(366, 360, image=self.card1_img, anchor="nw")

            self.back_image = tk.PhotoImage(file="assets\\back_of_a_card.png")  # size : 74 x 107 px


            self.card1_flop = None
            self.card2_flop = None
            self.card3_flop = None
            self.card4_flop = None
            self.card5_flop = None




        except tk.TclError as e:
            print("Error loading image:", str(e))
            self.photo = None

    def set_first_flop(self, flop):
        self.card1_flop = tk.PhotoImage(file="cards\\" + self.image_dict[flop[0]])
        self.card2_flop = tk.PhotoImage(file="cards\\" + self.image_dict[flop[1]])
        self.card3_flop = tk.PhotoImage(file="cards\\" + self.image_dict[flop[2]])

    def set_card4_flop(self, card4):
        self.card4_flop = tk.PhotoImage(file="cards\\" + self.image_dict[card4])

    def show_card4_flop(self):
        x = 472
        y = 169
        self.canvas.create_image(x, y, image=self.card4_flop, anchor="nw")

    def show_card5_flop(self):
        x = 546
        y = 169
        self.canvas.create_image(x, y, image=self.card5_flop, anchor="nw")

    def set_card5_flop(self, card5):
        self.card4_flop = tk.PhotoImage(file="cards\\" + self.image_dict[card5])


    def show_first_flop(self):
        x = 250
        y = 169

        self.canvas.create_image(x, y, image=self.card1_flop, anchor="nw")
        x += 74

        self.canvas.create_image(x, y, image=self.card2_flop, anchor="nw")
        x += 74

        self.canvas.create_image(x, y, image=self.card3_flop, anchor="nw")
        x += 74


    def show(self):
        self.lift()

    def buttons_1(self):
        # Create the button
        button = tk.Button(root, text="BET", command=button_clicked, width=10, height=2)

        # Place the button at the specified coordinates
        x = 580
        y = 450
        button.place(x=x, y=y)

        # Create the button
        button = tk.Button(root, text="CHECK", command=button_clicked, width=10, height=2)

        # Place the button at the specified coordinates
        x = 680
        y = 450
        button.place(x=x, y=y)

        # Create the button
        button = tk.Button(root, text="FOLD", command=button_clicked, width=10, height=2)

        # Place the button at the specified coordinates
        x = 780
        y = 450
        button.place(x=x, y=y)

    def buttons_2(self):
        # Create the button
        button = tk.Button(root, text="CALL & RAISE", command=button_clicked, width=10, height=2)

        # Place the button at the specified coordinates
        x = 580
        y = 450
        button.place(x=x, y=y)

        # Create the button
        button = tk.Button(root, text="CALL", command=button_clicked, width=10, height=2)

        # Place the button at the specified coordinates
        x = 680
        y = 450
        button.place(x=x, y=y)

        # Create the button
        button = tk.Button(root, text="FOLD", command=button_clicked, width=10, height=2)

        # Place the button at the specified coordinates
        x = 780
        y = 450
        button.place(x=x, y=y)



    def show_other_players(self, num):
        if num >= 1:
            self.canvas.create_image(62, 306, image=self.back_image, anchor="nw")
            self.canvas.create_image(136, 306, image=self.back_image, anchor="nw")
        if num >= 2:
            self.canvas.create_image(59, 56, image=self.back_image, anchor="nw")
            self.canvas.create_image(133, 56, image=self.back_image, anchor="nw")
        if num >= 3:
            self.canvas.create_image(366, 2, image=self.back_image, anchor="nw")
            self.canvas.create_image(440, 2, image=self.back_image, anchor="nw")
        if num >= 4:
            self.canvas.create_image(672, 56, image=self.back_image, anchor="nw")
            self.canvas.create_image(746, 56, image=self.back_image, anchor="nw")
        if num >= 5:
            self.canvas.create_image(672, 306, image=self.back_image, anchor="nw")
            self.canvas.create_image(746, 306, image=self.back_image, anchor="nw")

    def show_card_at_coordinates(self, card):
        x = 60
        y = 60

        # Get the image file path for the specified card
        card_image_file = self.image_dict[card]
        card_img = tk.PhotoImage(file="cards\\" + card_image_file)

        # Create a canvas image item with the card image
        self.canvas.create_image(x, y, image=card_img, anchor="nw")




root = tk.Tk()
root.geometry("900x500")

page = PokerScreen(root)
page.pack(fill="both", expand=True)

page.show_other_players(1)

card = Card(CardRank.TWO, Suit.SPADES)
page.show_card_at_coordinates(card)

page.buttons_1()

flop = [Card(CardRank.ACE, Suit.SPADES),
        Card(CardRank.ACE, Suit.SPADES),
        Card(CardRank.ACE, Suit.SPADES)]

page.set_first_flop(flop)

page.show_first_flop()

root.mainloop()
