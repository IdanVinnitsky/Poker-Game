import tkinter as tk
from card import *
import os
from virtualHand import VHand
from tkinter import messagebox


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
        self.root = parent
        self.vhand = VHand("127.0.0.1")

        self.image_dict = create_card_dict()

        # create a canvas widget for the background image
        self.canvas = tk.Canvas(self, width=900, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.player_answer = None

        try:
            self.photo = tk.PhotoImage(file="assets\\pokerscreen.png")
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

            self.back_image = tk.PhotoImage(file="assets\\back_of_a_card.png")
            # size : 74 x 107 px

            self.card1_flop = None
            self.card2_flop = None
            self.card3_flop = None
            self.card4_flop = None
            self.card5_flop = None

        except tk.TclError as e:
            print("Error loading image:", str(e))
            self.photo = None

    def get_vhand(self):
        return self.vhand

    def show_my_cards(self, card1, card2):
        self.card1_img = tk.PhotoImage(file="cards\\" + self.image_dict[card1])
        self.card2_img = tk.PhotoImage(file="cards\\" + self.image_dict[card2])

        self.canvas.create_image(440, 360, image=self.card1_img, anchor="nw")
        self.canvas.create_image(366, 360, image=self.card2_img, anchor="nw")

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
        self.bet_button = tk.Button(self.root, text="BET", command=lambda: button_clicked("BET"),
                                    width=10, height=2)

        # Place the button at the specified coordinates
        x = 580
        y = 450
        self.bet_button.place(x=x, y=y)

        # Create the button
        self.check_button = tk.Button(self.root, text="CHECK", command=lambda: button_clicked("CHECK"),
                                      width=10, height=2)

        # Place the button at the specified coordinates
        x = 680
        y = 450
        self.check_button.place(x=x, y=y)

        # Create the button
        self.fold_button = tk.Button(self.root, text="FOLD", command=lambda: button_clicked("FOLD"),
                                     width=10, height=2)

        # Place the button at the specified coordinates
        x = 780
        y = 450
        self.fold_button.place(x=x, y=y)

    def button_clicked(self, button_name):
        if button_name == "Play":
            messagebox.showinfo("Play", "Let's play the game!")
            self.disable_buttons()  # Disable buttons after Play button is pressed
        elif button_name == "Rules":
            messagebox.showinfo("Rules", "Here are the rules of the game:")
            self.disable_buttons()  # Disable buttons after Rules button is pressed
        elif button_name == "Exit":
            self.master.quit()

    def buttons_2(self):
        # Create the button
        self.callraise_button = tk.Button(self.root, text="CALL & RAISE", command=button_clicked,
                                          width=10, height=2)

        # Place the button at the specified coordinates
        x = 580
        y = 450
        self.callraise_button.place(x=x, y=y)

        # Create the button
        self.call_button = tk.Button(self.root, text="CALL", command=button_clicked,
                                     width=10, height=2)

        # Place the button at the specified coordinates
        x = 680
        y = 450
        self.call_button.place(x=x, y=y)

        # Create the button
        self.fold_button = tk.Button(self.root, text="FOLD", command=button_clicked,
                                     width=10, height=2)

        # Place the button at the specified coordinates
        x = 780
        y = 450
        self.fold_button.place(x=x, y=y)

    def disable_buttons1(self):
        self.bet_button.config(state="disabled")
        self.check_button.config(state="disabled")
        self.fold_button.config(state="disabled")

    def enable_buttons1(self):
        self.bet_button.config(state="normal")
        self.check_button.config(state="normal")
        self.fold_button.config(state="normal")



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

    def update_screen(self):
        print("AAAA")

    def get_player_answer(self):
        return self.player_answer

    def update_screen(self):
        self.show_my_cards(self.vhand.player.cards[0], self.vhand.player.cards[1])

def main():
    root = tk.Tk()
    root.geometry("900x500")

    page = PokerScreen(root)

    page.pack(fill="both", expand=True)

    vhand = page.get_vhand()
    vhand.initUIHand(page)


    root.mainloop()


if __name__ == '__main__':
    main()



'''
# place the card images on the canvas at specified coordinates and size
            self.card1_img = tk.PhotoImage
            (file="cards\\" + self.image_dict[Card(CardRank.ACE, Suit.SPADES)])
            
            self.canvas.create_image(440, 360, image=self.card1_img, anchor="nw")
            self.canvas.create_image(366, 360, image=self.card1_img, anchor="nw")
'''
