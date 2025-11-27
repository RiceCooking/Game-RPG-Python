import inquirer
from src.halaman_masuk import players, player, clear
from src.shop import SENJATA_DATA

# Data boss berisi statistik musuh & reward
BOSS_DATA = {
    1: {"nama": "Goblin King", "hp": 50, "attack": 25, "reward_koin": 30, "reward_exp": 15},
    2: {"nama": "Orc Warlord", "hp": 75, "attack": 40, "reward_koin": 60, "reward_exp": 30},
    3: {"nama": "Dragon", "hp": 100, "attack": 75, "reward_koin": 100, "reward_exp": 50}
}


def calculate_total_attack(user_data):
    
    attack = user_data.get('attack', 0)  # attack dasar user
    senjata_aktif = user_data['senjata_aktif']  # nama senjata aktif user
    
    # Jika user punya senjata aktif dan ada dalam database SENJATA_DATA
    if senjata_aktif and senjata_aktif in SENJATA_DATA:
        weapon_bonus = SENJATA_DATA[senjata_aktif]['attack_bonus']  # bonus attack dari senjata
        return attack + weapon_bonus  # total attack = dasar + bonus
    
    return attack  # jika tidak memakai senjata → return attack dasar


def sistem_battle(user_id_login, boss_level):

    data = players.get(player.user_id == user_id_login)  # mengambil data user yang sedang login
    boss = BOSS_DATA[boss_level]  # mengambil data boss berdasarkan level
    
    total_attack = calculate_total_attack(data)  # total attack user (termasuk bonus senjata)
    
    # Informasi pembuka battle
    print(f"\n=== BATTLE vs {boss['nama']} ===")
    print(f"HP Boss: {boss['hp']}, Attack: {boss['attack']}")
    print(f"HP Anda: {data['hp']}, Attack: {data['attack']}")
    
    # Jika user memakai senjata, tampilkan bonusnya
    if data['senjata_aktif']:
        weapon_bonus = SENJATA_DATA[data['senjata_aktif']]['attack_bonus']
        print(f"Senjata: {data['senjata_aktif']} (+{weapon_bonus} Attack)")
    
    print(f"Total Attack: {total_attack}")  # total attack akhir
    
    # Variabel HP di dalam pertarungan (supaya tidak mengubah database sampai battle selesai)
    hp_user = data['hp']
    hp_boss = boss['hp']
    attack_boss = boss['attack']
    
    round_count = 1  # menghitung number of rounds
    
    # LOOP PERTARUNGAN
    while True:
        print(f"\n--- Round {round_count} ---")
        
        # User menyerang boss
        hp_boss -= total_attack
        print(f"Anda menyerang {boss['nama']} dengan {total_attack} damage!")
        print(f"HP {boss['nama']} tersisa: {max(0, hp_boss)}")  # max untuk mencegah angka negatif
        
        # Jika boss mati → user menang
        if hp_boss <= 0:
            print(f"\nSelamat! Anda mengalahkan {boss['nama']}!")
            
            # Hitung reward
            koin_baru = data['koin'] + boss['reward_koin']
            exp_baru = data['exp'] + boss['reward_exp']
            
            # Hitung level up (jika exp sudah cukup)
            level_baru = data['level']
            exp_required = level_baru * 50  # exp yang dibutuhkan untuk naik level
            
            if exp_baru >= exp_required:
                level_baru += 1  # naik level
                exp_baru = exp_baru - exp_required  # sisa exp setelah naik
                attack_baru = data['attack'] + 2  # bonus stat
                hp_baru = data['hp'] + 10
                
                # Update attack & HP karena naik level
                players.update({
                    'attack': attack_baru,
                    'hp': hp_baru
                }, player.user_id == user_id_login)
                
                print(f"Level up! Sekarang level {level_baru}")
                print(f"HP +10, Attack +2")
            
            # Update exp/koin/level setelah battle
            players.update({
                'koin': koin_baru,
                'exp': exp_baru,
                'level': level_baru
            }, player.user_id == user_id_login)
            
            print(f"Reward: {boss['reward_koin']} koin, {boss['reward_exp']} exp")
            input("\nTekan Enter untuk melanjutkan...")
            return  # battle selesai
        
        # SERANGAN BALIK BOSS
        hp_user -= attack_boss
        print(f"\n{boss['nama']} menyerang Anda dengan {attack_boss} damage!")
        print(f"HP Anda tersisa: {max(0, hp_user)}")
        
        # Jika user mati → kalah
        if hp_user <= 0:
            print(f"\nAnda kalah melawan {boss['nama']}!")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        # Jika battle berlanjut → next round
        round_count += 1
        input("\nTekan Enter untuk lanjut ke round berikutnya...")


def battle(user_id_login):
    
    while True:
        clear() # bersihkan layar
        
        data = players.get(player.user_id == user_id_login)  # ambil data user
        total_attack = calculate_total_attack(data)  # total attack akhir user
        
        print("=== BATTLE ===")
        print(f"Attack Total Anda: {total_attack}")
        
        # Menu pilihan boss
        menu = [
            inquirer.List(
                'opsi',
                message="Pilih boss:",
                choices=[
                    'Boss lvl 1 (Goblin King) - 50 HP',
                    'Boss lvl 2 (Orc Warlord) - 75 HP',
                    'Boss lvl 3 (Dragon) - 100 HP',
                    'Kembali'
                ]
            )
        ]
        jawaban = inquirer.prompt(menu) # tampilkan menu pilihan
        
        if not jawaban:  # jika user keluar paksa (CTRL + C)
            return
        
        if "(Goblin King)" in jawaban['opsi']:   # panggil battle boss level 1
            sistem_battle(user_id_login, 1)
        elif "(Orc Warlord)" in jawaban['opsi']: # panggil battle boss level 2
            sistem_battle(user_id_login, 2)
        elif "(Dragon)" in jawaban['opsi']:      # panggil battle boss level 3
            sistem_battle(user_id_login, 3)
        elif jawaban['opsi'] == 'Kembali':
            break  # keluar ke menu utama
