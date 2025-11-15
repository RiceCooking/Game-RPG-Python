import random
from karakter import player

RARITY_LIST = {
    "Common": 1,
    "Uncommon": 3,
    "Rare": 6,
    "Epic": 10,
    "Legendary": 15,
    "Mythical": 25
}

RARITY_PROB = {
    "Common": 50,
    "Uncommon": 25,
    "Rare": 12,
    "Epic": 8,
    "Legendary": 4,
    "Mythical": 1
}

def roll_rarity():
    total = sum(RARITY_PROB.values())
    rand = random.uniform(0, total)
    cumulative = 0

    for rarity, prob in RARITY_PROB.items():
        cumulative += prob
        if rand <= cumulative:
            return rarity

    return "Common"


def gacha_pull():
    """Melakukan 1x gacha, menghasilkan sebuah senjata pedang."""
    rarity = roll_rarity()
    bonus_attack = RARITY_LIST[rarity]

    weapon = {
        "nama": f"Pedang {rarity}",
        "rarity": rarity,
        "bonus_attack": bonus_attack
    }
    return weapon

def shop():
    while True:
        print("\n=== TOKO GACHA ===")
        print("1. Pull x1 (100 koin)")
        print("2. Pull x10 (1000 koin)")
        print("3. Kembali ke menu utama")
        print(f"\nKoin kamu: {player['koin']}")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            if player["koin"] < 100:
                print("Koin tidak cukup!")
                continue

            player["koin"] -= 100
            weapon = gacha_pull()
            player["inventory"].append(weapon)

            print(f"\nKamu mendapatkan: {weapon['nama']} (+{weapon['bonus_attack']} atk)")
            input("\nTekan Enter untuk lanjut...")

        elif pilihan == "2":
            if player["koin"] < 1000:
                print("Koin tidak cukup!")
                continue

            player["koin"] -= 1000
            print("\nHasil Gacha x10:\n")

            for i in range(10):
                weapon = gacha_pull()
                player["inventory"].append(weapon)
                print(f"{i+1}. {weapon['nama']} (+{weapon['bonus_attack']} atk)")

            input("\nTekan Enter untuk lanjut...")

        elif pilihan == "3":
            return 

        else:
            print("Pilihan tidak valid!")

