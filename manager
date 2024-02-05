import random
import string
import time
import sqlite3
import subprocess

from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet


conn = sqlite3.connect('database.db')
cur = conn.cursor()


def setting_up_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY,
        key CHAR(255),
        application CHAR(255),
        email_or_username CHAR(255),
        password CHAR(255),  
        user CHAR(255),  
        FOREIGN KEY(user) REFERENCES pin(hwid)
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pin (
        id INTEGER PRIMARY KEY,
        pin_number CHAR(4),
        hwid CHAR(255) DEFAULT NULL
    )""")


class Manager:
    def __init__(self):
        self.hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        self.letters = string.ascii_letters
        self.numbers = string.digits
        self.special = string.punctuation

        self.combined = self.letters + self.numbers + self.special
        self.shuffled = ''.join(random.sample(self.combined, len(self.combined)))

        cur.execute("SELECT pin_number FROM pin WHERE hwid = ?", (self.hwid,))

        if not cur.fetchone():
            self.create_pin(self.hwid)
        else:
            self.enter_pin(self.hwid)


    def enter_pin(self, hwid) -> bool:
        attempt = True
        while attempt:
            pin = input("Enter your 4 digit pin: ")

            if pin.isnumeric() and len(pin) == 4:
                cur.execute("""
                    SELECT pin_number FROM pin WHERE hwid = ?
                """, (hwid,))
                fetched_pin = cur.fetchone()

                
                if check_password_hash(fetched_pin[0], pin):
                    self.logged_in = True
                    self.main(hwid)
                else:
                    print("Wrong pin was entered")
                    return False
            else:
                print("Error well entering PIN please try again")


    def create_pin(self, hwid) -> None:
        attempt = True
        while attempt:
            pin = input("Set your 4 digit pin: ")

            if pin.isnumeric() and len(pin) == 4:
                pin = generate_password_hash(pin)

                cur.execute("""
                    INSERT INTO pin (pin_number, hwid)
                    VALUES (?, ?)
                """, (pin, hwid))

                conn.commit()
                attempt = False

                self.enter_pin(hwid)

            else:
                print("Something went wrong perhaps your pin is to long or not all digits?")


    def add_password(self, hwid) -> str:
        try:
            app = input("Application: ")
            email_or_user = input("Username/Email: ")
            password = input("Password: ")

            key = Fernet.generate_key()
            encrypted_password, encrypted_user = Fernet(key).encrypt(password.encode()), Fernet(key).encrypt(email_or_user.encode())

            cur.execute("""
                INSERT INTO passwords (key, application, email_or_username, password, user)
                VALUES (?, ?, ?, ?, ?)
            """, (key, app, encrypted_user, encrypted_password, hwid))
            conn.commit()

            return "Successfully added password for {}".format(app)
        
        except Exception as e:
            return "ERROR | Something went wrong: {}".format(e)


    def fetch_password(self, hwid):
        try: 
            get_all_apps = cur.execute("SELECT application FROM passwords WHERE user = ?", (hwid,))
            if not get_all_apps:
                print("No applications are added")
                time.sleep(0.5)
                self.main(hwid)

            print(get_all_apps.fetchall())
            print("What application do you want to get your password from?")
            chosen_app = input("App: ")

            data = cur.execute("SELECT * FROM passwords WHERE application = ?", (chosen_app,))

            for row in data:
                fetched_key, fetched_user, fetched_pass = row[1], row[3], row[4]

            decrypted_user, decrypted_pass = Fernet(fetched_key).decrypt(fetched_user).decode(), Fernet(fetched_key).decrypt(fetched_pass).decode()
            
            return f"Application: {chosen_app} | User/Email: {decrypted_user} | Password: {decrypted_pass}"

        except Exception as e:
            return "ERROR | Something went wrong: {}".format(e)
    

    def gen_rand_pass(self) -> str:
        try:
            length = int(input("Length of password: "))
            rand_pass = ""

            for _ in range(length):
                rand_pass += self.shuffled[random.randint(0, len(self.shuffled))]
            
            return f"Password | {rand_pass}"

        except Exception as e:
            return f"ERROR | Something went wrong: {e}"


    def main(self, hwid) -> None:
        print("Welcome to the password manager user {}".format(hwid))
        print("Command | [1. Add a password] | [2. Fetch a password for a added application] | [3. Generate a random password] |[4. Exit the application]")
        command_enter_loop = True
        while command_enter_loop:
            cmd_inp = input("Command: ")

            if cmd_inp == '1':
                print(self.add_password(hwid))
            elif cmd_inp == '2':
                print(self.fetch_password(hwid))
            elif cmd_inp == '3':
                print(self.gen_rand_pass())
            elif cmd_inp == '4':
                command_enter_loop = False
                print("Exiting the application")
                time.sleep(0.25)
                exit()
            else:
                print("Something went wrong please check your command input")


if __name__ == "__main__":
    setting_up_db()
    Manager()
