import sqlite3

from player import Player


class AccountsRepository:

    def __init__(self, db_file=None):
        self.db_file = 'AccountSystem.db'


    def create_table(self):
        connection = sqlite3.connect(self.db_file)
        cur = connection.cursor()
        query = "CREATE TABLE IF NOT EXISTS AccountDB (id INTEGER PRIMARY KEY, name TEXT, password TEXT)"
        cur.execute(query)
        connection.commit()
        connection.close()


    def signup(self, player: Player):
        if player.name == '' or player.password == '':
            print("Error: values cant be empty")

        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()

            find_player = 'SELECT * FROM AccountDB WHERE name = ?'
            cursor.execute(find_player, (player.name,))
            result = cursor.fetchall()
            if len(result) > 0:
                print('Error:Player exist with same name')
                return

            query = "INSERT INTO AccountDB(name, password) VALUES(?,?)"
            cursor.execute(query, (player.name, player.password))
            connection.commit()
            connection.close()
            print('Success : New Account Created, Successfully')
        except Exception as es:
            print('Error:Something went wrong try again', es)

    def login(self, player: Player):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        find_player = 'SELECT * FROM AccountDB WHERE name = ?'
        cursor.execute(find_player, (player.name,))
        # result = cursor.fetchall()
        result = cursor.fetchone()
        if result == None:
            return -1
        else:
            return result[0]

        print('Success', 'Logged in Successfully')

    # def change_password(self, player: Player):
    #     if email_entry3.get() == "" or new_password_entry.get() == "":
    #         messagebox.showerror('Error', 'All Fields Are Required')
    #
    #     else:
    #         db = sqlite3.connect("./Database/AccountSystem.db")
    #         cursor = db.cursor()
    #         query = "select * from AccountDB where Email=?"
    #         cursor.execute(query, [(email_entry3.get())])
    #         row = cursor.fetchone()
    #         if row is None:
    #             messagebox.showerror("Error", "Email does not exist")
    #             exit_window()
    #
    #         else:
    #             query = '''update AccountDB set Password=? where Email=?'''
    #             cursor.execute(query, [new_password_entry.get(), email_entry3.get()])
    #             db.commit()
    #             db.close()
    #             messagebox.showinfo("Congrats", "Password Changed Successfully")
    #             exit_window()

