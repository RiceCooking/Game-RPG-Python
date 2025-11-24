from tinydb import TinyDB, Query
import time
import os
import sys
import inquirer

DB_PATH = 'data/rpg_game_db.json' 
db = TinyDB(DB_PATH)
users = db.table('users')
players = db.table('players')
user = Query()
player = Query()

def halaman_masuk():
    clear()
    jawaban = None
    while True:
        try:
            questions = [
            inquirer.List('opsi',
                          message = "=== Halaman masuk ===",
                          choices=[
                              'Register',
                              'Login',  
                              'Keluar',
                              ]),
        ]
            answer = inquirer.prompt(questions)


            if not answer:
                raise KeyboardInterrupt

            jawaban = answer
            break

        except (KeyboardInterrupt, EOFError):
            loading("Pilihlah berdasarkan opsi", 2)
            clear()

    opsi = jawaban['opsi']

    if opsi == 'Register':
        clear()
        register()
        return None

    elif opsi == 'Login':
        clear()
        return login()

    elif opsi == 'Keluar':
        clear()
        loading("Keluar dari Program", 3)
        return False

def loading(text="Loading", durasi=5):
    print(text, end="")
    for i in range(durasi):
        time.sleep(1)
        sys.stdout.write(".")
        sys.stdout.flush()
    print(" Selesai")


def clear():
    os.system("cls || clear")

def register():
    print("=== Register ===")
    try:
        username = input("Username\t\t:")
        if users.search(user.username == username):
            print("Username tidak tersedia")
            time.sleep(2)
            return
        password = input("Password\t\t:")
        konfpass = input("Konfirmasi Password\t:")

        if " " in username:
            print("Username tidak boleh mengandung spasi")
            time.sleep(3)
            return
        if " " in password:
            print("Password tidak boleh mengandung spasi")
            time.sleep(3)
            return     
        if password != konfpass:
            print("Password tidak sesuai")
            time.sleep(3)
            return
        if len(username) < 3:
            print("Username minimal 3 karakter")
            time.sleep(2)
            return
        if len(password) < 3:
            print("Password minimal 3 karakter")
            time.sleep(2)
            return

        
        id = users.insert({
            'username' : username,
            'password' : password
        })

        players.insert({
            'user_id' : id,
            'role' : 'user',
            'karakter' : None,
            'class' : None,
            'level' : 1,
            'exp' : 0,
            'hp' : 0,
            'attack' : 0,
            'koin' : 150,
            'inventory' : [],
            'senjata_aktif' : None
        })
        print("Pengguna baru mendapatkan 150 koin.")
        loading("Proses Register", 3)

    except (KeyboardInterrupt, EOFError):
        print("Bearlih ke halaman masuk")
        time.sleep(2)
        return

def login():
    print("=== Login ====")
    try:
        username = input("Username\t\t:")
        password = input("Password\t\t:")
        if " " in username:
            print("Username tidak boleh mengandung spasi")
            time.sleep(2)
            return None
        if " " in password:
            print("Password tidak boleh mengandung spasi")
            time.sleep(2)
            return None

        if username == "":
            print("Username tidak boleh kosong")
            return None
        if password == "":
            print("Password tidak boleh kosong")
            return None
        user_data = users.get(user.username == username)

        if not user_data:
            print("Username tidak ditemukan")
            time.sleep(2)
            return None
        
        if user_data['password'] == password:
            loading("Proses Login", 3)
            return user_data
        else:
            print("Password salah")
            time.sleep(2)
            return None
    except (KeyboardInterrupt, EOFError):
        print("Bearlih ke halaman masuk")
        time.sleep(2)
        return None
    