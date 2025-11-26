import inquirer
import random
from src.halaman_masuk import players, player, loading, clear

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

GACHA_PROBABILITIES = {
    "Common": 60,
    "Uncommon": 25,
    "Rare": 12,
    "Legendary": 3
}

def get_random_senjata():
    rand = random.randint(1, 100)
    cumulative_prob = 0
    
    for rarity, prob in GACHA_PROBABILITIES.items():
        cumulative_prob += prob
        if rand <= cumulative_prob:
            senjata_rarity = [s for s, stats in SENJATA_DATA.items() if stats['rarity'] == rarity]
            return random.choice(senjata_rarity)
    
    senjata_common = [s for s, stats in SENJATA_DATA.items() if stats['rarity'] == "Common"]
    return random.choice(senjata_common)

def gacha_senjata(user_id_login, jumlah):
    data = players.get(player.user_id == user_id_login)
    koin = data['koin']
    inventory = data['inventory']
    
    if jumlah == 1:
        if koin < 50:
            loading("Koin tidak cukup!", 2)
            return
        
        players.update({'koin': koin - 50}, player.user_id == user_id_login)
        
        senjata = get_random_senjata()
        inventory.append(senjata)
        players.update({'inventory': inventory}, player.user_id == user_id_login)
        
        senjata_stats = SENJATA_DATA[senjata]
        print(f"Selamat! Anda mendapatkan: {senjata}")
        print(f"Rarity: {senjata_stats['rarity']}, Attack Bonus: +{senjata_stats['attack_bonus']}")
        loading("Kembali ke Shop", 5)
        
    elif jumlah == 10:
        if koin < 450:
            loading("Koin tidak cukup!", 2)
            return
        
        players.update({'koin': koin - 450}, player.user_id == user_id_login)
        
        senjata_didapat = []
        rarity_count = {"Common": 0, "Uncommon": 0, "Rare": 0, "Legendary": 0}
        
        for _ in range(10):
            senjata = get_random_senjata()
            inventory.append(senjata)
            senjata_didapat.append(senjata)
            rarity_count[SENJATA_DATA[senjata]['rarity']] += 1
        
        players.update({'inventory': inventory}, player.user_id == user_id_login)
        
        print("Hasil Gacha x10:")
        print("=" * 40)
        for i, senjata in enumerate(senjata_didapat, 1):
            stats = SENJATA_DATA[senjata]
            print(f"{i}. {senjata} [{stats['rarity']}] (+{stats['attack_bonus']} Attack)")
        
        print("\nSummary Rarity:")
        for rarity, count in rarity_count.items():
            print(f"{rarity}: {count}")
        
        loading("Kembali ke Shop", 5)

def shop(user_id_login):
    while True:
        clear()
        data = players.get(player.user_id == user_id_login)
        print("=== SHOP ===")
        print(f"Koin Anda: {data['koin']}")
        
        menu = [
            inquirer.List(
                'opsi',
                message="Pilih menu:",
                choices=[
                    'Gacha x1 (50 koin)',
                    'Gacha x10 (450 koin)',
                    'Kembali'
                ]
            )
        ]
        ans = inquirer.prompt(menu)

        if not ans:
            return
        
        if ans['opsi'] == 'Gacha x1 (50 koin)':
            gacha_senjata(user_id_login, 1)
        elif ans['opsi'] == 'Gacha x10 (450 koin)':
            gacha_senjata(user_id_login, 10)
        elif ans['opsi'] == 'Kembali':
            break