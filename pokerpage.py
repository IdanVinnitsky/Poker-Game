import sys
import tkinter as tk
from tkinter.constants import BOTH, TOP, RAISED, E
from tkinter.simpledialog import askstring

from HandAct import HandAct
from ProtocolAct import ProtocolAct
from card import *
import os

from gameprotocol import GameProtocol
from player import Player
from virtualHand import VHand
from tkinter import messagebox
from tkinter import simpledialog
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

        self.text_objects: dict[str, int] = {}
        self.topW = None
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

        self.fold_button = None
        self.call_button = None
        self.check_button = None
        self.raise_button = None

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
        self.disable_buttons()
        self.canvas.delete(self.user_message_id)
        player_answer = HandAct(act)
        val = '0'
        if player_answer == HandAct.RAISE:
            val = simpledialog.askstring("Input Box", "How much money:", parent=self.root)
        self.vhand.send_player_response(player_answer, val)

    def get_vhand(self):
        return self.vhand

    def display_name_and_money(self, player):
        # self.canvas.create_text(540, 362, text=str(player.get_name()), font=("Arial", 18))
        self.canvas.create_text(540, 362, text='You', font=("Arial", 18))
        self.canvas.create_text(540, 382, text=str(player.get_money()), font=("Arial", 16))

        # text = self.canvas.create_text(540, 392, text=str(player.get_respone()), font=("Arial", 16), fill="red", anchor=E)
        # bbox = self.canvas.bbox(text)E
        # rect = self.canvas.create_rectangle(bbox, outline="yellow",fill="black", width=5)
        # self.canvas.tag_raise(text, rect)
        # self.canvas.tag_raise(rect, text)
        if self.text_objects.get(player.id) is None:
            self.text_objects[player.id] = self.canvas.create_text(540, 392, text=str(player.get_respone()),
                                                                   font=("Arial", 16), fill="red")
        else:
            self.canvas.delete(self.text_objects[player.id])
            self.text_objects[player.id] = self.canvas.create_text(540, 392, text=str(player.get_respone()),
                                                                   font=("Arial", 16), fill="red")

    def show_my_cards(self, card1, card2):
        self.card1_img = tk.PhotoImage(file="cards/" + self.image_dict[card1])
        self.card2_img = tk.PhotoImage(file="cards/" + self.image_dict[card2])

        self.canvas.create_image(366, 360, image=self.card1_img, anchor="nw")
        self.canvas.create_image(440, 360, image=self.card2_img, anchor="nw")

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

    def set_buttons_FClR(self):

        self.fold_button = tk.Button(self.root, text="FOLD",
                                     command=lambda: self.button_clicked("fold"),
                                     width=10, height=2)
        x = 580
        y = 450
        self.fold_button.place(x=x, y=y)

        self.call_button = tk.Button(self.root, text="CALL",
                                     command=lambda: self.button_clicked("call"),
                                     width=10, height=2)
        x = 680
        y = 450
        self.call_button.place(x=x, y=y)

        self.raise_button = tk.Button(self.root, text="RAISE",
                                      command=lambda: self.button_clicked("raise"),
                                      width=10, height=2)
        x = 780
        y = 450
        self.raise_button.place(x=x, y=y)

    def set_buttons_FChR(self):
        self.fold_button = tk.Button(self.root, text="FOLD",
                                     command=lambda: self.button_clicked("fold"),
                                     width=10, height=2)
        x = 580
        y = 450
        self.fold_button.place(x=x, y=y)

        self.check_button = tk.Button(self.root, text="CHECK",
                                      command=lambda: self.button_clicked("check"),
                                      width=10, height=2)
        x = 680
        y = 450
        self.check_button.place(x=x, y=y)

        self.raise_button = tk.Button(self.root, text="RAISE",
                                      command=lambda: self.button_clicked("raise"),
                                      width=10, height=2)
        x = 780
        y = 450
        self.raise_button.place(x=x, y=y)

    def disable_buttons(self):
        if self.fold_button is not None:
            self.fold_button.config(state="disabled")
        if self.call_button is not None:
            self.call_button.config(state="disabled")
        if self.check_button is not None:
            self.check_button.config(state="disabled")
        if self.raise_button is not None:
            self.raise_button.config(state="disabled")
    #
    # def enable_buttons1(self):
    #     self.bet_button.config(state="normal")

    def buttons_1(self):
        # Create the button
        self.bet_button = tk.Button(self.root, text="BET",
                                    command=lambda: self.button_clicked("bet"),
                                    width=10, height=2)

        # Place the button at the specified coordinates
        x = 580
        y = 450
        self.bet_button.place(x=x, y=y)

        # Create the button
        self.check_button = tk.Button(self.root, text="CHECK",
                                      command=lambda: self.button_clicked("check"),
                                      width=10, height=2)

        # Place the button at the specified coordinates
        x = 680
        y = 450
        self.check_button.place(x=x, y=y)

        # Create the button
        self.fold_button = tk.Button(self.root, text="FOLD",
                                     command=lambda: self.button_clicked("fold"),
                                     width=10, height=2)

        # Place the button at the specified coordinates
        x = 780
        y = 450
        self.fold_button.place(x=x, y=y)

    def buttons_2(self):
        # Create the button
        self.call_button = tk.Button(self.root, text="CALL",
                                     command=lambda: self.button_clicked("call"),
                                     width=10, height=2)

        # Place the button at the specified coordinates
        x = 680
        y = 450
        self.call_button.place(x=x, y=y)

        # Create the button
        self.fold_button = tk.Button(self.root, text="FOLD",
                                     command=lambda: self.button_clicked("fold"),
                                     width=10, height=2)

        # Place the button at the specified coordinates
        x = 780
        y = 450
        self.fold_button.place(x=x, y=y)

        self.raise_button = tk.Button(self.root, text="RAISE",
                                      command=lambda: self.button_clicked("raise"),
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

    def show_other_players(self, other_players):
        num = len(other_players)
        if num >= 1:
            # self.canvas.delete('all')
            self.canvas.create_image(62, 306, image=self.back_image, anchor="nw")
            self.canvas.create_image(136, 306, image=self.back_image, anchor="nw")

            self.canvas.create_text(240, 362, text=str(other_players[0].get_name()), font=("Arial", 16))
            self.canvas.create_text(240, 392, text=str(other_players[0].get_money()), font=("Arial", 16))
            self.canvas.create_text(240, 422, text=str(other_players[0].get_respone()), font=("Arial", 16), fill="red")
            # text.pack()
            # self.canvas.create_

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

    def update_label(self, label):
        self.canvas.itemconfig(label, text="Updated text")

    def labels(self):
        # Create a label with specified width and height
        label = self.canvas.create_text(20, 450, text=self.pr.get_round_status(), width=10, height=2)

        self.root.after(2000, self.update_label(label))

    def update_screen(self, isOnlyScreen):
        self.show_my_cards(self.vhand.player.cards[0], self.vhand.player.cards[1])
        self.display_name_and_money(self.vhand.player)

        if isOnlyScreen == False:
            self.user_message_id = self.canvas.create_text(50, 362, text=self.vhand.player.name + " your turn", font=("Arial", 18))
            if self.vhand.in_game_protocol.round_status == HandAct.BET or \
                    self.vhand.in_game_protocol.round_status == HandAct.RAISE or \
                    self.vhand.in_game_protocol.round_status == HandAct.CALL:
                self.set_buttons_FClR()
            else:
                self.set_buttons_FChR()

        # self.labels()
        self.show_other_players(self.vhand.otherHands)

        if self.vhand.flop is not None:
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

        self.signup_button = tk.Button(self.root, text="Signup",
                                       command=lambda: self.board_button_clicked("Signup"),
                                       width=10, height=2)
        self.login_button = tk.Button(self.root, text="Login",
                                      command=lambda: self.board_button_clicked("Login"),
                                      width=10, height=2)
        self.start_button = tk.Button(self.root, text="Start Game",
                                      command=lambda: self.board_button_clicked("StartGame"),
                                      width=10, height=2)
        self.exit_button = tk.Button(self.root, text="Exit Game",
                                     command=lambda: self.board_button_clicked("Exit"),
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

    def board_button_clicked(self, act: str):
        if act == 'Login':
            self.login_screen()
            # self.vhand.login()
        elif act == 'StartGame':
            self.vhand.startGame()
        elif act == 'Signup':
            self.signupScreen()
        else:
            print("Wrong Action:", act)

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
        tk.Button(top, text="Signup", command=lambda: self.signScreenAct(entry1, entry2)).pack(pady=5, side=TOP)
        # Create a Button Widget in the Toplevel Window
        button = tk.Button(top, text="Cancel", command=lambda: self.close_win(top))
        button.pack(pady=5, side=TOP)

    def login_screen(self):
        self.root.overrideredirect(1)
        self.root.withdraw()
        # Create a Toplevel window
        self.topW = tk.Toplevel(self.root)
        self.topW.geometry("550x250")

        # Create an Entry Widget in the Toplevel window
        # tk.Label(top, text="UserName")
        label = tk.Label(self.topW, text="UserName")
        label.pack()
        entry1 = tk.Entry(self.topW, width=25)
        entry1.pack()
        label1 = tk.Label(self.topW, text="Password")
        label1.pack()
        tk.Label(self.topW, text="Password")
        entry2 = tk.Entry(self.topW, width=25)
        entry2.pack()

        # Create a Button to print something in the Entry widget
        tk.Button(self.topW, text="Login", command=lambda: self.login_screen_action(entry1, entry2)).pack(pady=5,
                                                                                                          side=TOP)
        tk.Button(self.topW, text="Signup", command=lambda: self.signup_screen_action(entry1, entry2)).pack(pady=5,
                                                                                                            side=TOP)

        button = tk.Button(self.topW, text="Cancel", command=lambda: self.close_win(self.root))
        button.pack(pady=5, side=TOP)

    def close_win(self, top):
        top.destroy()

    def login_screen_action(self, e1, e2):
        # self.root.deiconify()
        # self.topW.withdraw()
        print("Val", e1.get())
        print("Val", e2.get())
        self.login(e1.get(), e2.get())
        status, message = self.vhand.receiveMessage()
        if status:
            # messagebox.showinfo("Information", message)
            self.topW.withdraw()
            self.root.overrideredirect(0)
            self.root.deiconify()
        else:
            messagebox.showwarning("Warning", message)

    def signup_screen_action(self, e1, e2):
        # self.root.deiconify()
        # self.topW.withdraw()
        print("Val", e1.get())
        print("Val", e2.get())
        self.sigin(e1.get(), e2.get())
        status, message = self.vhand.receiveMessage()
        if status:
            messagebox.showinfo("Information", message)
        else:
            messagebox.showwarning("Warning", message)

    def signScreenAct(self, e1, e2):
        print("Val", e1.get())
        print("Val", e2.get())
        self.sigin(e1.get(), e2.get())
        status, message = self.vhand.receiveMessage()
        if status:
            messagebox.showinfo(message, "Information")
        else:
            messagebox.showwarning(message, "Warning")

    def login(self, userName: str, paswword: str):
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
        send_msg = pr.create_message(ProtocolAct.SIGNUP, player)
        self.vhand.send(send_msg)

    def connectGame(self):
        pass

    def about(self):
        pass

    def exit(self):
        pass

    def set_title(self, param):
        self.root.title(param)


def main():
    root = tk.Tk()
    root.geometry("900x500")

    page = PokerScreen(root)
    page.createMenu()
    # page.login_screen()

    page.pack(fill="both", expand=True)

    vhand = page.get_vhand()
    vhand.initUIHand(page)
    page.login(sys.argv[1], sys.argv[2])
    status, message = vhand.receiveMessage()
    if status:
        page.set_title("Wellcome " + sys.argv[1])

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
