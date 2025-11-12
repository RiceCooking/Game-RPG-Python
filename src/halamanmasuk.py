from tinydb import TinyDB, Query
import time
import getpass

DB_PATH = 'data/rpg_game_db.json' 
db = TinyDB(DB_PATH)
users = db.table('users')
players = db.table('players')
user = Query()
player = Query()

def register():
    print("=== Register ===")
    try:
        username = input("Username\t\t:")
        password = getpass.getpass("Password\t\t:")
        konfpass = getpass.getpass("Konfirmasi Password\t:")

        if " " in username:
            print("Username tidak boleh mengandung spasi")
            time.sleep(2)
            return
        if " " in password:
            print("Password tidak boleh mengandung spasi")
            time.sleep(2)
            return     
        if password != konfpass:
            print("Password tidak sesuai")
            time.sleep(2)
            return
        if len(username) < 3:
            print("Username minimal 3 karakter")
            time.sleep(2)
            return
        if len(password) < 3:
            print("Password minimal 3 karakter")
            time.sleep(2)
            return
        if users.search(user.username == username):
            print("Username tidak tersedia")
            time.sleep(2)
            return
        
        id = users.insert({
            'username' : username,
            'password' : password
        })

        players.insert({
            'user_id' : id,
            'karakter' : None,
            'class' : None,
            'level' : 0,
            'exp' : 0,
            'hp' : 0,
            'attack' : 0,
            'koin' : 150,
            'inventory' : [],
            'senjata_aktif' : None
        })
        print("Berhasil Registrasi\n Pengguna baru mendapatkan 150 koin.")
        time.sleep(3)

    except (KeyboardInterrupt, EOFError):
        print("Bearlih ke halaman masuk")
        time.sleep(2)
        return

        

def login():
    print("=== Login ====")
    try:
        username = input("Username\t\t:")
        password = getpass.getpass("Password\t\t:")
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
            print("Berhasil Login")
            time.sleep(3)
            return user_data
        else:
            print("Password salah")
            time.sleep(2)
    except (KeyboardInterrupt, EOFError):
        print("Bearlih ke halaman masuk")
        time.sleep(2)
        return None