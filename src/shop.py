from tinydb import TinyDB, Query
import random

DB_PATH = 'data/rpg_game_db.json'
db = TinyDB(DB_PATH)
players = db.table('players')
User = Query()

def get_player(name):
    data = players.get(User.name == name)
    if not data:
        new_player = {
            "name": name,
            "koin": 0,
            "inventory": []
        }
        players.insert(new_player)
        return new_player
    return data

def update_player(player):
    players.update(player, User.name == player['name'])

def shop(player_name):
    player = get_player(player_name)

    # Jenis senjata tetap → pedang
    weapon_type = "Pedang"

    # Rarity + bonus attack
    rarity_pool = {
        "Common": 1,
        "Uncommon": 3,
        "Rare": 7,
        "Epic": 15,
        "Legendary": 30,
        "Mythical": 60
    }

    # Persentase drop rate (bisa kamu ubah)
    rarity_chance = [
        ("Common", 50),
        ("Uncommon", 25),
        ("Rare", 15),
        ("Epic", 7),
        ("Legendary", 2.5),
        ("Mythical", 0.5)
    ]

    # Fungsi memilih rarity berdasarkan peluang
    def roll_rarity():
        r = random.uniform(0, 100)
        total = 0
        for rarity, chance in rarity_chance:
            total += chance
            if r <= total:
                return rarity
        return "Common"

    # Fungsi gacha 1x
    def gacha_one():
        rarity = roll_rarity()
        bonus = rarity_pool[rarity]

        weapon = {
            "nama": f"{weapon_type} {rarity}",
            "rarity": rarity,
            "bonus_attack": bonus,
            "jenis": weapon_type
        }

        player["inventory"].append(weapon)
        print(f"Kamu mendapatkan {weapon['nama']}! (ATK +{bonus})")

    # =====================
    #     MENU SHOP
    # =====================
    while True:
        print("\n=== SHOP GACHA ===")
        print("1. Pull x1 (100 koin)")
        print("2. Pull x10 (1000 koin)")
        print("3. Kembali")

        try:
            opsi = int(input("Pilih opsi: "))
        except:
            print("Input tidak valid!")
            continue

        # =====================
        #      OPSI 1
        # =====================
        if opsi == 1:
            if player["koin"] >= 100:
                player["koin"] -= 100
                gacha_one()
                update_player(player)
            else:
                print("Koin tidak cukup!")

        # =====================
        #      OPSI 2
        # =====================
        elif opsi == 2:
            if player["koin"] >= 1000:
                player["koin"] -= 1000
                print("=== Pull x10 ===")
                for _ in range(10):
                    gacha_one()
                update_player(player)
            else:
                print("Koin tidak cukup!")

        # =====================
        #      OPSI 3
        # =====================
        elif opsi == 3:
            print("Kembali ke menu utama...")
            break

        else:
            print("Opsi tidak dikenal!")
