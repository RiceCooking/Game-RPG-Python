from src.halaman_masuk import loading, player, players
import inquirer

def buat_karakter(user_id_login):
    print("=== Buat Karakter ===")
    while True:
        try:
            nama = input("Nama Karakter\t:")
            if nama.strip() == "":
                print("Nama karakter tidak boleh kosong")
                continue
            elif " " in nama:
                print("Nama karakter tidak boleh mengandung spasi")
                continue
            break
        except (KeyboardInterrupt, EOFError):
            print("Harap isi nama karakter dengan karakter string")
    pilihan = ""
    while True:
        try:
            pilihan_kelas = [
                inquirer.List('kelas',
                        message = "Kelas Karakter",
                        choices=[
                              'Warrior (HP : 100, Attack : 15)', 
                              'Tank (HP : 150, Attack : 10)',   
                              ]),
            ]
            jawaban = inquirer.prompt(pilihan_kelas)

            if not jawaban:
                raise KeyboardInterrupt
            pilihan = jawaban['kelas']
            break
        except(KeyboardInterrupt, EOFError):
            print("Pilihlah berdasarkan opsi")
            loading("Kembali", 1)

    kelas = ""
    hp = 0
    attack = 0

    if "Warrior" in pilihan:
        kelas = "Warrior"
        hp = 100
        attack = 15

    elif "Tank" in pilihan:
        kelas = "Tank"
        hp = 150
        attack = 10

    players.update({
            'karakter' : nama,
            'class' : kelas,
            'level' : 1,
            'hp' : hp,
            'attack' : attack,
        }, player.user_id == user_id_login)

    loading("Membuat Karakter", 2)
    return True