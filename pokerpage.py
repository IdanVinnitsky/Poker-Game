import tkinter as tk
from tkinter.constants import BOTH, TOP, RAISED
from tkinter.simpledialog import askstring

from HandAct import HandAct
from ProtocolAct import ProtocolAct
from card import *
import os

from gameprotocol import GameProtocol
from player import Player
from virtualHand import VHand
from tkinter import messagebox
from PIL import Image

from PIL import ImageTk, Image

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



class PokerScreen(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.raise_button = None
        self.signup_button = None
        self.root = parent
        self.vhand = VHand("127.0.0.1")

        self.image_dict = create_card_dict()

        # create a canvas widget for the background image
        self.canvas = tk.Canvas(self, width=900, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.player_answer = None

        self.menubar = None
        self.gameMenu = None
        self.helpmenu = None

        self.login_button = None
        self.start_button = None
        self.exit_button = None

        try:
            self.photo = tk.PhotoImage(file="assets/pokerscreen.png")
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

            self.back_image = tk.PhotoImage(file="assets/back_of_a_card.png")
            # size : 74 x 107 px

            self.card1_flop = None
            self.card2_flop = None
            self.card3_flop = None
            self.card4_flop = None
            self.card5_flop = None
        except tk.TclError as e:
            print("Error loading image:", str(e))
            self.photo = None

    def button_clicked(self, act: str):
        print("Button clicked!")
        self.player_answer = HandAct(act)
        if self.player_answer == HandAct.RAISE:
            val = askstring('Raise', 'What is your raise ?')
        self.vhand.send_player_response(HandAct(act), val)

    def get_vhand(self):
        return self.vhand

    def show_my_cards(self, card1, card2):
        self.card1_img = tk.PhotoImage(file="cards/" + self.image_dict[card1])
        self.card2_img = tk.PhotoImage(file="cards/" + self.image_dict[card2])

        self.canvas.create_image(440, 360, image=self.card1_img, anchor="nw")
        self.canvas.create_image(366, 360, image=self.card2_img, anchor="nw")

    def set_first_flop(self, flop):
        self.card1_flop = tk.PhotoImage(file="cards/" + self.image_dict[flop[0]])
        self.card2_flop = tk.PhotoImage(file="cards/" + self.image_dict[flop[1]])
        self.card3_flop = tk.PhotoImage(file="cards/" + self.image_dict[flop[2]])

    def set_2_flop(self, flop):
        # self.card1_flop = tk.PhotoImage(file="cards/" + self.image_dict[flop[0]])
        # self.card2_flop = tk.PhotoImage(file="cards/" + self.image_dict[flop[1]])
        # self.card3_flop = tk.PhotoImage(file="cards/" + self.image_dict[flop[2]])
        self.card4_flop = tk.PhotoImage(file="cards/" + self.image_dict[flop[3]])

    def set_3_flop(self, flop):
        # self.card1_flop = tk.PhotoImage(file="cards/" + self.image_dict[flop[0]])
        # self.card2_flop = tk.PhotoImage(file="cards/" + self.image_dict[flop[1]])
        # self.card3_flop = tk.PhotoImage(file="cards/" + self.image_dict[flop[2]])
        # self.card4_flop = tk.PhotoImage(file="cards/" + self.image_dict[flop[3]])
        self.card5_flop = tk.PhotoImage(file="cards/" + self.image_dict[flop[4]])

    def set_card4_flop(self, card4):
        self.card4_flop = tk.PhotoImage(file="cards/" + self.image_dict[card4])

    def show_card4_flop(self):
        x = 472
        y = 169
        self.canvas.create_image(x, y, image=self.card4_flop, anchor="nw")

    def show_card5_flop(self):
        x = 546
        y = 169
        self.canvas.create_image(x, y, image=self.card5_flop, anchor="nw")

    def set_card5_flop(self, card5):
        self.card4_flop = tk.PhotoImage(file="cards/" + self.image_dict[card5])


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
        self.bet_button = tk.Button(self.root, text="BET", command=lambda: self.button_clicked("bet"),
                                    width=10, height=2)

        # Place the button at the specified coordinates
        x = 580
        y = 450
        self.bet_button.place(x=x, y=y)

        # Create the button
        self.check_button = tk.Button(self.root, text="CHECK", command=lambda: self.button_clicked("check"),
                                      width=10, height=2)

        # Place the button at the specified coordinates
        x = 680
        y = 450
        self.check_button.place(x=x, y=y)

        # Create the button
        self.fold_button = tk.Button(self.root, text="FOLD", command=lambda: self.button_clicked("fold"),
                                     width=10, height=2)

        # Place the button at the specified coordinates
        x = 780
        y = 450
        self.fold_button.place(x=x, y=y)

    def buttons_2(self):
        # Create the button
        self.call_button = tk.Button(self.root, text="CALL & RAISE", command=self.button_clicked("call"),
                                          width=10, height=2)

        # Place the button at the specified coordinates
        x = 580
        y = 450
        self.call_button.place(x=x, y=y)

        # Create the button
        self.call_button = tk.Button(self.root, text="CALL", command=self.button_clicked("call"),
                                     width=10, height=2)

        # Place the button at the specified coordinates
        x = 680
        y = 450
        self.call_button.place(x=x, y=y)

        # Create the button
        self.fold_button = tk.Button(self.root, text="FOLD", command=self.button_clicked("fold"),
                                     width=10, height=2)

        # Place the button at the specified coordinates
        x = 780
        y = 450
        self.fold_button.place(x=x, y=y)

        self.raise_button = tk.Button(self.root, text="CALL & RAISE", command=self.button_clicked("raise"),
                                     width=10, height=2)

        # Place the button at the specified coordinates
        x = 450
        y = 450
        self.raise_button.place(x=x, y=y)

    def button_pressed1(self, button_name):
        if button_name == "Play":
            messagebox.showinfo("Play", "Let's play the game!")
        elif button_name == "Rules":
            messagebox.showinfo("Rules", "Here are the rules of the game:")
        elif button_name == "Exit":
            self.master.quit()


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
        card_img = tk.PhotoImage(file="cards/" + card_image_file)

        # Create a canvas image item with the card image
        self.canvas.create_image(x, y, image=card_img, anchor="nw")

    def get_player_answer(self):
        return self.player_answer

    def set_player_answer(self, val):
        self.player_answer = val


    def update_screen(self, num):
        self.show_my_cards(self.vhand.player.cards[0], self.vhand.player.cards[1])
        self.buttons_1()

        self.show_other_players(num)

        if self.vhand.flop != None:
            if len(self.vhand.flop) == 3:
                self.set_first_flop(self.vhand.flop)
                self.show_first_flop()

            if len(self.vhand.flop) == 4:
                self.set_2_flop(self.vhand.flop)
                self.show_first_flop()
                self.show_card4_flop()

            if len(self.vhand.flop) == 5:
                self.set_3_flop(self.vhand.flop)
                self.show_first_flop()
                self.show_card4_flop()
                self.show_card5_flop()

    def createMenu(self):

        self.signup_button = tk.Button(self.root, text="Signup", command=lambda: self.board_button_clicked("Signup"),
                                      width=10, height=2)
        self.login_button = tk.Button(self.root, text="Login", command=lambda: self.board_button_clicked("Login"),
                                    width=10, height=2)
        self.start_button = tk.Button(self.root, text="Start Game", command=lambda: self.board_button_clicked("StartGame"),
                                    width=10, height=2)
        self.exit_button = tk.Button(self.root, text="Exit Game", command=lambda: self.board_button_clicked("Exit"),
                                    width=10, height=2)

        x = 1
        y = 1
        self.login_button.place(x=x, y=y)

        x = 150
        y = 1
        self.start_button.place(x=x, y=y)

        x = 300
        y = 1
        self.exit_button.place(x=x, y=y)

        x = 500
        y = 1
        self.signup_button.place(x=x, y=y)

    def board_button_clicked(self, act:str):
        if act == 'Login':
            self.loginScreen()
            # self.vhand.login()
        elif act == 'StartGame':
            self.vhand.startGame()
        elif act == 'Signup':
            self.signupScreen()
        else:
            print("Wrong Action:",act)

    def signupScreen(self):
        # Create a Toplevel window
        top = tk.Toplevel(self.root)
        top.geometry("550x250")

        # Create an Entry Widget in the Toplevel window
        # tk.Label(top, text="UserName")
        label = tk.Label(top, text="UserName")
        label.pack()
        entry1 = tk.Entry(top, width=25)
        entry1.pack()
        label1 = tk.Label(top, text="Password")
        label1.pack()
        tk.Label(top, text="Password")
        entry2 = tk.Entry(top, width=25)
        entry2.pack()

        # Create a Button to print something in the Entry widget
        tk.Button(top, text="Signup", command=lambda: self.signScreenAct(entry1,entry2)).pack(pady=5, side=TOP)
        # Create a Button Widget in the Toplevel Window
        button = tk.Button(top, text="Cancel", command=lambda: self.close_win(top))
        button.pack(pady=5, side=TOP)

    def loginScreen(self):
        # Create a Toplevel window
        top = tk.Toplevel(self.root)
        top.geometry("550x250")

        # Create an Entry Widget in the Toplevel window
        # tk.Label(top, text="UserName")
        label = tk.Label(top, text="UserName")
        label.pack()
        entry1 = tk.Entry(top, width=25)
        entry1.pack()
        label1 = tk.Label(top, text="Password")
        label1.pack()
        tk.Label(top, text="Password")
        entry2 = tk.Entry(top, width=25)
        entry2.pack()

        # Create a Button to print something in the Entry widget
        tk.Button(top, text="Login", command=lambda: self.loginScreenAct(entry1,entry2)).pack(pady=5, side=TOP)
        # Create a Button Widget in the Toplevel Window
        button = tk.Button(top, text="Cancel", command=lambda: self.close_win(top))
        button.pack(pady=5, side=TOP)

    def close_win(self,top):
        top.destroy()

    def loginScreenAct(self,e1,e2):
        print("Val", e1.get())
        print("Val", e2.get())
        self.login(e1.get(), e2.get())
        status, message = self.vhand.receiveMessage()
        if status == True:
            messagebox.showinfo(message, "Information")
        else:
            messagebox.showwarning(message, "Warning")

    def signScreenAct(self,e1,e2):
        print("Val", e1.get())
        print("Val", e2.get())
        self.sigin(e1.get(), e2.get())
        status, message = self.vhand.receiveMessage()
        if status == True:
            messagebox.showinfo(message, "Information")
        else:
            messagebox.showwarning(message, "Warning")

    def login(self, userName: str, paswword: str ):
        player = Player(-1)
        player.name = userName
        player.password = paswword

        self.vhand.player = player

        pr = GameProtocol()
        send_msg = pr.create_message(ProtocolAct.LOGIN, player)
        self.vhand.send(send_msg)

    def sigin(self, userName: str, paswword: str):
        player = Player(-1)
        player.name = userName
        player.password = paswword

        self.vhand.player = player

        pr = GameProtocol()
        send_msg = pr.create_message(ProtocolAct.SIGNIN, player)
        self.vhand.send(send_msg)


    def connectGame(self):
        pass

    def about(self):
        pass

    def exit(self):
        pass


def main():
    root = tk.Tk()
    root.geometry("1200x700")

    page = PokerScreen(root)
    page.createMenu()
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
