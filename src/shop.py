import inquirer       
import random          
import time           
from src.halaman_masuk import players, player, loading, clear


#     DATA SENJATA (TETAP)
SENJATA_DATA = {
    "Pedang Pendek": {"attack_bonus": 5, "rarity": "Common"},
    "Pedang Besi": {"attack_bonus": 10, "rarity": "Common"},
    "Pedang Perak": {"attack_bonus": 15, "rarity": "Uncommon"},
    "Pedang Baja": {"attack_bonus": 20, "rarity": "Rare"},
    "Kapak Perunggu": {"attack_bonus": 8, "rarity": "Common"},
    "Kapak Besi": {"attack_bonus": 12, "rarity": "Uncommon"},
    "Kapak Perak": {"attack_bonus": 18, "rarity": "Rare"},
    "Palu Perang": {"attack_bonus": 25, "rarity": "Legendary"}
}

# Probabilitas rarity saat gacha (total = 100)
GACHA_PROBABILITIES = {
    "Common": 60,
    "Uncommon": 25,
    "Rare": 12,
    "Legendary": 3
}

#      PICK SENJATA RANDOM BERDASAR PROBABILITAS
def get_random_senjata():
    random_number = random.randint(1, 100)     # pilih angka acak 1..100
    cumulative = 0                              # untuk akumulasi probabilitas
    
    for rarity, chance in GACHA_PROBABILITIES.items():  # loop semua rarity
        cumulative += chance                    # tambahkan probabilitas
        if random_number <= cumulative:         # cek apakah masuk range rarity ini
            # ambil semua senjata yang rarity-nya sama
            list_senjata_by_rarity = [
                nama for nama, stats in SENJATA_DATA.items()
                if stats['rarity'] == rarity
            ]
            return random.choice(list_senjata_by_rarity)  # pilih 1 senjata acak
    
    # fallback jika error
    common_items = [
        nama for nama, stats in SENJATA_DATA.items()
        if stats['rarity'] == "Common"
    ]
    return random.choice(common_items)


# LOGIKA GACHA (x1 dan x10)
def gacha_senjata(user_id, jumlah_penarikan):

    user_data = players.get(player.user_id == user_id)   # ambil data player
    user_koin = user_data['koin']                        # jumlah koin user
    user_inventory = user_data['inventory']              # inventory user (list)


    # GACHA x1
    if jumlah_penarikan == 1:
        biaya = 50                                       # harga gacha x1
        
        if user_koin < biaya:                            # cek koin cukup?
            loading("Koin tidak cukup!", 2)
            return
        
        # Potong koin langsung dari database
        players.update({'koin': user_koin - biaya}, player.user_id == user_id)
        
        senjata_didapat = get_random_senjata()           # roll 1 senjata
        senjata_stats = SENJATA_DATA[senjata_didapat]    # ambil data senjata
        
        print(f"Mendapatkan: {senjata_didapat} [{senjata_stats['rarity']}]")
        
        # Cek duplikat
        if senjata_didapat in user_inventory:
            print("DUPLIKAT! Kamu sudah memiliki senjata ini.")
            print("Item hangus (tidak masuk inventory).")
        else:
            user_inventory.append(senjata_didapat)       # tambah ke inventory
            players.update({'inventory': user_inventory}, player.user_id == user_id)
            print(f"SELAMAT! {senjata_didapat} berhasil ditambahkan ke tas.")
        
        loading("Kembali ke Shop", 4)
        return


    # GACHA x10
    elif jumlah_penarikan == 10:
        biaya = 450                                      # harga gacha x10
        
        if user_koin < biaya:                             # cek koin cukup?
            loading("Koin tidak cukup!", 2)
            return
        
        players.update({'koin': user_koin - biaya}, player.user_id == user_id)  # potong koin
        
        batch_item_baru = []                              # kumpulan item baru dari 10 roll
        
        print("Hasil Gacha x10:")
        print("=" * 40)
        
        for index in range(1, 11):                        # loop 10 kali gacha
            senjata_didapat = get_random_senjata()        # roll senjata
            senjata_stats = SENJATA_DATA[senjata_didapat]
            
            # cek duplikat terhadap inventory lama + batch 10X
            duplikat = (
                senjata_didapat in user_inventory or
                senjata_didapat in batch_item_baru
            )
            
            if duplikat:
                print(f"[{index}] {senjata_didapat} (Duplikat - Hangus)")
            else:
                batch_item_baru.append(senjata_didapat)   # simpan ke kumpulan 10 roll
                print(
                    f"[{index}] {senjata_didapat} [{senjata_stats['rarity']}] "
                    f"(+{senjata_stats['attack_bonus']} Atk)"
                )
                time.sleep(0.1)                           # animasi/efek sedikit
            
        # Jika ada minimal 1 item baru → simpan ke DB
        if batch_item_baru:
            final_inventory = user_inventory + batch_item_baru
            players.update({'inventory': final_inventory}, player.user_id == user_id)
        
        print("-" * 40)
        print(f"Ringkasan: {len(batch_item_baru)} item baru berhasil disimpan.")
        
        loading("Kembali ke Shop", 5)

# MENU SHOP
def shop(user_id):
    while True:
        clear()                                           # bersihkan layar
        
        user_data = players.get(player.user_id == user_id) # refresh data player
        
        print("=== SHOP ===")
        print(f"Koin Anda: {user_data['koin']}")           # tampilkan koin terbaru
        
        # buat menu pakai inquirer
        menu_options = [
            inquirer.List(
                'opsi',
                message="Pilih menu",
                choices=[
                    'Gacha x1 (50 koin)',
                    'Gacha x10 (450 koin)',
                    'Kembali'
                ]
            )
        ]
        
        jawaban = inquirer.prompt(menu_options)            # tampilkan menu
        
        if not jawaban:                                    # jika user keluar
            return
        
        pilihan = jawaban['opsi']                          # ambil pilihan menu
        
        if pilihan == 'Gacha x1 (50 koin)':
            gacha_senjata(user_id, 1)                      # jalankan gacha 1x
        
        elif pilihan == 'Gacha x10 (450 koin)':
            gacha_senjata(user_id, 10)                     # jalankan gacha 10x
        
        elif pilihan == 'Kembali':
            break                                          # kembali ke menu sebelumnya
