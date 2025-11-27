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
    attack = user_data.get('attack', 0)
    senjata_aktif = user_data['senjata_aktif']

    if senjata_aktif and senjata_aktif in SENJATA_DATA:
        weapon_bonus = SENJATA_DATA[senjata_aktif]['attack_bonus']
        return attack + weapon_bonus

    return attack


def sistem_battle(user_id_login, boss_level):
    try:
        data = players.get(player.user_id == user_id_login)
        boss = BOSS_DATA[boss_level]
        total_attack = calculate_total_attack(data)

        print(f"\n=== BATTLE vs {boss['nama']} ===")
        print(f"HP Boss: {boss['hp']}, Attack: {boss['attack']}")
        print(f"HP Anda: {data['hp']}, Attack: {data['attack']}")

        if data['senjata_aktif']:
            weapon_bonus = SENJATA_DATA[data['senjata_aktif']]['attack_bonus']
            print(f"Senjata: {data['senjata_aktif']} (+{weapon_bonus} Attack)")

        print(f"Total Attack: {total_attack}")

        hp_user = data['hp']
        hp_boss = boss['hp']
        attack_boss = boss['attack']
        round_count = 1

        while True:
            print(f"\n--- Round {round_count} ---")

            hp_boss -= total_attack
            print(f"Anda menyerang {boss['nama']} dengan {total_attack} damage!")
            print(f"HP {boss['nama']} tersisa: {max(0, hp_boss)}")

            if hp_boss <= 0:
                print(f"\nSelamat! Anda mengalahkan {boss['nama']}!")

                koin_baru = data['koin'] + boss['reward_koin']
                exp_baru = data['exp'] + boss['reward_exp']

                level_baru = data['level']
                exp_required = level_baru * 50

                if exp_baru >= exp_required:
                    level_baru += 1
                    exp_baru -= exp_required

                    players.update({
                        'attack': data['attack'] + 2,
                        'hp': data['hp'] + 10
                    }, player.user_id == user_id_login)

                    print(f"Level up! Sekarang level {level_baru}")
                    print("HP +10, Attack +2")

                players.update({
                    'koin': koin_baru,
                    'exp': exp_baru,
                    'level': level_baru
                }, player.user_id == user_id_login)

                print(f"Reward: {boss['reward_koin']} koin, {boss['reward_exp']} exp")

                try:
                    input("\nTekan Enter untuk melanjutkan...")
                except KeyboardInterrupt:
                    print("\nInput dibatalkan.")
                return

            hp_user -= attack_boss
            print(f"\n{boss['nama']} menyerang Anda dengan {attack_boss} damage!")
            print(f"HP Anda tersisa: {max(0, hp_user)}")

            if hp_user <= 0:
                print(f"\nAnda kalah melawan {boss['nama']}!")
                try:
                    input("\nTekan Enter untuk melanjutkan...")
                except KeyboardInterrupt:
                    print("\nInput dibatalkan.")
                return

            round_count += 1
            try:
                input("\nTekan Enter untuk lanjut ke round berikutnya...")
            except KeyboardInterrupt:
                print("\nPertarungan dihentikan.")
                return

    except KeyboardInterrupt:
        print("\nPertarungan dibatalkan oleh pengguna.")
        return


def battle(user_id_login):

    while True:
        try:
            clear()
            data = players.get(player.user_id == user_id_login)
            total_attack = calculate_total_attack(data)

            print("=== BATTLE ===")
            print(f"Attack Total Anda: {total_attack}")

            menu = [
                inquirer.List(
                    'opsi',
                    message="Pilih boss",
                    choices=[
                        'Boss lvl 1 (Goblin King) - 50 HP',
                        'Boss lvl 2 (Orc Warlord) - 75 HP',
                        'Boss lvl 3 (Dragon) - 100 HP',
                        'Kembali'
                    ]
                )
            ]

            jawaban = inquirer.prompt(menu)
            if not jawaban:
                return

            if "(Goblin King)" in jawaban['opsi']:
                sistem_battle(user_id_login, 1)
            elif "(Orc Warlord)" in jawaban['opsi']:
                sistem_battle(user_id_login, 2)
            elif "(Dragon)" in jawaban['opsi']:
                sistem_battle(user_id_login, 3)
            elif jawaban['opsi'] == 'Kembali':
                break

        except KeyboardInterrupt:
            print("\nKembali ke menu utama...")
            return
