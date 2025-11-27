import inquirer
import time
from prettytable import PrettyTable
from src.halaman_masuk import players, player, clear
from src.battle import calculate_total_attack
from src.shop import SENJATA_DATA

# ==========================================
# MENU UTAMA KARAKTER
# ==========================================
def karakter(user_id_login):
    while True:
        clear()  # membersihkan layar terminal
        print("=== Menu Karakter ===")

        # Menu pilihan dengan inquirer
        menu = [
            inquirer.List(
                'opsi',
                message="Pilih menu",
                choices=[
                    'Statistik',
                    'Inventory',
                    'Kembali'
                ]
            )
        ]
        
        try:
            jawaban = inquirer.prompt(menu)

            if not jawaban:
                return  # jika user keluar dari menu secara paksa (Ctrl+C return None)

            # Ke halaman statistik karakter
            if jawaban['opsi'] == "Statistik":
                statistik(user_id_login)

            # Ke menu inventory
            elif jawaban['opsi'] == "Inventory":
                inventory(user_id_login)

            # Kembali ke menu sebelumnya
            elif jawaban['opsi'] == "Kembali":
                break
        
        except (KeyboardInterrupt, EOFError):
            break # Kembali ke menu utama game

# ==========================================
# HALAMAN STATISTIK KARAKTER
# ==========================================
def statistik(user_id_login):
    clear()
    data = players.get(player.user_id == user_id_login)  # ambil data player berdasarkan id
    
    total_attack = calculate_total_attack(data)  # hitung total attack karakter

    # Membuat tabel statistik karakter
    table = PrettyTable()
    table.title = "STATISTIK KARAKTER"
    table.field_names = ["Atribut", "Nilai"]

    # Mengisi isi tabel
    table.add_row(["Nama", data['karakter']])
    table.add_row(["Kelas", data['class']])
    table.add_row(["Level", data['level']])
    table.add_row(["Exp", f"{data['exp']}/{data['level'] * 50}"])
    table.add_row(["HP", data['hp']])
    table.add_row(["Attack", data['attack']])
    table.add_row(["Senjata Aktif", data['senjata_aktif'] or "Tidak ada"])

    # Jika ada senjata aktif dan senjata ada di data senjata
    if data['senjata_aktif'] and data['senjata_aktif'] in SENJATA_DATA:
        weapon_bonus = SENJATA_DATA[data['senjata_aktif']]['attack_bonus']
        table.add_row(["Bonus Senjata", f"+{weapon_bonus}"])

    table.add_row(["Total Attack", total_attack])
    table.add_row(["Koin", data['koin']])

    print(table)
    
    try:
        input("\nTekan Enter untuk kembali...")
    except (KeyboardInterrupt, EOFError):
        pass # Abaikan error, langsung kembali

# ==========================================
# MENU INVENTORY
# ==========================================
def inventory(user_id_login):
    while True:
        clear()
        data = players.get(player.user_id == user_id_login)

        # Membuat tabel inventory
        table = PrettyTable()
        table.title = "INVENTORY SENJATA"
        table.field_names = ["No", "Senjata", "Rarity", "Attack Bonus"]

        # Menampilkan semua senjata di inventory
        for i, item in enumerate(data['inventory'], start=1):
            if item in SENJATA_DATA:  # jika senjata valid
                stats = SENJATA_DATA[item]
                table.add_row([i, item, stats['rarity'], f"+{stats['attack_bonus']}"])
            else:  # senjata tidak terdaftar
                table.add_row([i, item, "Unknown", "Unknown"])

        print(table)

        # Menampilkan senjata aktif saat ini
        if data['senjata_aktif'] and data['senjata_aktif'] in SENJATA_DATA:
            current_weapon_stats = SENJATA_DATA[data['senjata_aktif']]
            print(f"\nSenjata Aktif: {data['senjata_aktif']} [{current_weapon_stats['rarity']}] (+{current_weapon_stats['attack_bonus']} Attack)")

        # Menu tindakan inventory
        menu = [
            inquirer.List(
                'opsi',
                message="Pilih tindakan",
                choices=[
                    'Lihat Detail Senjata',
                    'Hapus Senjata',
                    'Ganti Senjata Aktif',
                    'Kembali'
                ]
            )
        ]
        
        try:
            jawaban = inquirer.prompt(menu)
            
            if not jawaban: 
                break # Ctrl+C handling

            # Arahkan sesuai pilihan
            if jawaban['opsi'] == "Lihat Detail Senjata":
                lihat_detail_senjata(user_id_login)

            elif jawaban['opsi'] == "Hapus Senjata":
                hapus_senjata(user_id_login)

            elif jawaban['opsi'] == "Ganti Senjata Aktif":
                ganti_senjata(user_id_login)

            elif jawaban['opsi'] == "Kembali":
                break
        
        except (KeyboardInterrupt, EOFError):
            break

# ==========================================
# LIHAT DETAIL SENJATA
# ==========================================
def lihat_detail_senjata(user_id_login):
    clear()
    data = players.get(player.user_id == user_id_login)
    inv = data['inventory']

    # Jika inventory kosong
    if not inv:
        print("Inventory kosong!")
        time.sleep(2)
        return

    # Filter hanya senjata valid yang ada di SENJATA_DATA
    valid_senjata = [s for s in inv if s in SENJATA_DATA]
    if not valid_senjata:
        print("Tidak ada senjata yang valid di inventory!")
        time.sleep(2)
        return

    try:
        # User memilih senjata
        menu = [
            inquirer.List(
                'pilih',
                message="Pilih senjata untuk melihat detail",
                choices=valid_senjata
            )
        ]
        jawaban = inquirer.prompt(menu)
        
        if not jawaban: 
            return

        senjata = jawaban['pilih']
        stats = SENJATA_DATA[senjata]

        # Menampilkan detail lengkap
        print(f"\n=== DETAIL SENJATA ===")
        print(f"Nama: {senjata}")
        print(f"Rarity: {stats['rarity']}")
        print(f"Attack Bonus: +{stats['attack_bonus']}")

        # Perbandingan dengan senjata aktif jika ada
        if data['senjata_aktif'] and data['senjata_aktif'] in SENJATA_DATA:
            current_stats = SENJATA_DATA[data['senjata_aktif']]
            print(f"\nPerbandingan dengan Senjata Aktif:")
            print(f"Senjata Aktif: {data['senjata_aktif']} (+{current_stats['attack_bonus']})")
            print(f"Senjata ini: {senjata} (+{stats['attack_bonus']})")

            # Menilai kekuatan senjata
            if stats['attack_bonus'] > current_stats['attack_bonus']:
                print("Senjata ini lebih kuat!")
            elif stats['attack_bonus'] < current_stats['attack_bonus']:
                print("Senjata ini lebih lemah.")
            else:
                print("Senjata ini sama kuatnya.")

        input("\nTekan Enter untuk kembali...")
        
    except (KeyboardInterrupt, EOFError):
        return

# ==========================================
# HAPUS SENJATA DARI INVENTORY
# ==========================================
def hapus_senjata(user_id_login):
    clear()
    data = players.get(player.user_id == user_id_login)
    inv = data['inventory']

    # Minimal harus punya 1 senjata
    if len(inv) <= 1:
        print("Minimal harus memiliki 1 senjata. Tidak bisa dihapus!")
        time.sleep(2)
        return

    # Daftar senjata valid
    valid_senjata = [s for s in inv if s in SENJATA_DATA]
    if not valid_senjata:
        print("Tidak ada senjata yang valid untuk dihapus!")
        time.sleep(2)
        return

    try:
        # User memilih senjata yang akan dihapus
        menu = [
            inquirer.List(
                'hapus',
                message="Pilih senjata yang ingin dihapus",
                choices=[f"{s} [{SENJATA_DATA[s]['rarity']}]" for s in valid_senjata]
            )
        ]
        jawaban = inquirer.prompt(menu)
        
        if not jawaban: 
            return

        # Mengambil nama senjata sebelum tanda '['
        senjata_nama = jawaban['hapus'].split(' [')[0]

        # Tidak boleh menghapus senjata aktif
        if senjata_nama == data['senjata_aktif']:
            print("Tidak bisa menghapus senjata yang sedang aktif!")
            print("Ganti senjata aktif terlebih dahulu.")
            time.sleep(3)
            return

        # Hapus senjata dari inventory
        inv.remove(senjata_nama)
        players.update({'inventory': inv}, player.user_id == user_id_login)

        print(f"{senjata_nama} berhasil dihapus.")
        time.sleep(2)
        
    except (KeyboardInterrupt, EOFError):
        return

# ==========================================
# GANTI SENJATA AKTIF
# ==========================================
def ganti_senjata(user_id_login):
    clear()
    data = players.get(player.user_id == user_id_login)
    inv = data['inventory']

    # Senjata valid
    valid_senjata = [s for s in inv if s in SENJATA_DATA]
    if not valid_senjata:
        print("Tidak ada senjata yang valid di inventory!")
        time.sleep(2)
        return

    try:
        # User memilih senjata baru
        menu = [
            inquirer.List(
                'pilih',
                message="Pilih senjata aktif",
                choices=[f"{s} [+{SENJATA_DATA[s]['attack_bonus']} Attack]" for s in valid_senjata]
            )
        ]
        jawaban = inquirer.prompt(menu)
        
        if not jawaban:
            return

        # Ambil nama senjata tanpa text bonus
        senjata_baru = jawaban['pilih'].split(' [')[0] #split(' [')[0] = hapus bagian info attack, ambil nama senjatanya saja.

        # Update senjata aktif
        players.update({'senjata_aktif': senjata_baru}, player.user_id == user_id_login)

        weapon_bonus = SENJATA_DATA[senjata_baru]['attack_bonus']
        print(f"Senjata aktif diganti menjadi {senjata_baru}")
        print(f"Attack Bonus: +{weapon_bonus}")
        time.sleep(3)
        
    except (KeyboardInterrupt, EOFError):
        return