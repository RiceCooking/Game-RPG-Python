import inquirer
import time
from src.karakter import karakter
from src.shop import shop
from src.battle import battle
from src.halaman_masuk import loading, clear, halaman_masuk, players, users, q
from src.buat_karakter import buat_karakter

def menu_user(user_id_login):
    while True:
        clear()
        jawaban = None
        while True:
            try:
                questions = [
                inquirer.List('opsi',
                  message = "=== Menu Utama ===",
                  choices=[
                      'Karakter', 
                      'Shop',   
                      'Battle',
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

        if opsi == 'Karakter':
            clear()
            karakter(user_id_login)

        elif opsi == 'Shop':
            clear()
            shop(user_id_login)

        elif opsi == 'Battle':
            clear()
            battle(user_id_login)

        elif opsi == 'Keluar':
            clear()
            loading("Kembali ke Halaman Masuk", 3)
            return
        

def menu_admin(user_id_login):
    while True:
        clear()
        
        list_players = players.search(q.role == 'user')
        total_user = len(list_players)
        
        print(f"=== DASHBOARD ADMIN ===")
        print(f"Total Player: {total_user}")
        print("-----------------------")
        
        menu = [
            inquirer.List('opsi',
                          message="Pilih Tindakan:",
                          choices=[
                              'Hapus Data Player',
                              'Keluar'
                          ])
        ]
        jawaban = inquirer.prompt(menu)
        
        if not jawaban: 
            break
        opsi = jawaban
        
        if opsi['opsi'] == 'Hapus Data Player':
            
            if total_user == 0:
                print("\n[Info] Belum ada player yang terdaftar.")
                time.sleep(2)
                continue

            choices_hapus = []
            mapping_id = {}
            
            for p in list_players:
                u_data = users.get(doc_id=p['user_id'])
                u_name = u_data['username'] if u_data else "Unknown"
                char_name = p['karakter'] if p['karakter'] else "Belum Buat Char"
                
                label = f"{u_name} | {char_name} (Lvl {p['level']})"
                
                choices_hapus.append(label)
                mapping_id[label] = p['user_id']
            
            choices_hapus.append("<< Batal >>")
            
            menu_hapus = [
                inquirer.List('target',
                              message="Pilih user yang akan DIHAPUS PERMANEN:",
                              choices=choices_hapus)
            ]
            ans_hapus = inquirer.prompt(menu_hapus)
            
            if not ans_hapus or ans_hapus['target'] == "<< Batal >>":
                continue
            
            target_label = ans_hapus['target']
            target_id = mapping_id[target_label]
            
            loading(f"Menghapus permanen data {target_label}...", 2)
            
            users.remove(doc_ids=[target_id])
            players.remove(q.user_id == target_id)
            
            loading("Kembali ke Dashboard Admin", 2)

        elif opsi['opsi'] == 'Keluar':
            loading("Logout Admin...", 2)
            break

def main():
    sign_in = True
    login_s = None
    
    while sign_in == True:
        # === PANGGIL FUNGSI DARI FILE SEBELAH ===
        hasil_aktivitas = halaman_masuk() 

        # === CEK HASILNYA ===
        if hasil_aktivitas is False:
            # User pilih 'Keluar' -> Matikan Loop
            sign_in = False
            break
        
        elif hasil_aktivitas is not None:
            # User berhasil Login -> Simpan data
            login_s = hasil_aktivitas
        
        # (Kalau None, dia otomatis muter lagi ke atas)

        # === MASUK GAME LOOP ===
        while login_s != None:
            clear()
            user_id_login = login_s.doc_id
            
            # Pakai 'q' biar konsisten
            data_player = players.get(q.user_id == user_id_login)

            if data_player['role'] == 'admin':
                menu_admin(user_id_login)
                login_s = None
            
            elif data_player['role'] == 'user':   
                if data_player['karakter'] == None:
                    buat_karakter(user_id_login)
                else:
                    menu_user(user_id_login)
                    login_s = None