import inquirer
from tinydb import TinyDB, Query

DB_PATH = 'data/rpg_game_db.json'
db = TinyDB(DB_PATH)
players = db.table('players')
Q = Query()


# --------------------------------------
# Ambil data player dari DB
# --------------------------------------
def get_player(username):
    player = players.get(Q.username == username)
    if player is None:
        player = {
            "username": username,
            "hp": 100,
            "attack": 20,
            "coin": 0,
            "exp": 0
        }
        players.insert(player)
    return player


# --------------------------------------
# Simpan ke DB
# --------------------------------------
def save_player(player):
    players.update(player, Q.username == player["username"])


# --------------------------------------
# Sistem battle turn-based
# --------------------------------------
def sistem_battle(player, boss_hp, boss_attack, reward_coin, reward_exp):
    hp_user = player["hp"]
    attack_user = player["attack"]

    print("\n--- BATTLE DIMULAI ---")

    while True:
        # Serangan user
        boss_hp -= attack_user
        print(f"\nKamu menyerang! HP Boss sekarang: {boss_hp}")

        if boss_hp <= 0:
            print("\n🎉 Kamu menang!")
            print(f"+{reward_coin} koin, +{reward_exp} exp")

            player["coin"] += reward_coin
            player["exp"] += reward_exp
            save_player(player)
            return True

        # Serangan boss
        hp_user -= boss_attack
        print(f"Boss menyerang! HP kamu sekarang: {hp_user}")

        if hp_user <= 0:
            print("\n☠ Kamu kalah... tidak mendapat reward.")
            return False


# --------------------------------------
# Menu Battle
# --------------------------------------
def battle(username):
    player = get_player(username)

    while True:
        questions = [
            inquirer.List(
                "opsi",
                message="=== Pilih Boss untuk Battle ===",
                choices=[
                    ("Boss Level 1", 1),
                    ("Boss Level 2", 2),
                    ("Boss Level 3", 3),
                    ("Keluar", 4)
                ]
            )
        ]

        jawaban = inquirer.prompt(questions)
        opsi = jawaban["opsi"]

        if opsi == 4:
            print("Keluar dari battle.")
            break

        if opsi == 1:
            print("\nMelawan Boss Level 1...")
            sistem_battle(
                player,
                boss_hp=60,
                boss_attack=10,
                reward_coin=50,
                reward_exp=50
            )

        elif opsi == 2:
            print("\nMelawan Boss Level 2...")
            sistem_battle(
                player,
                boss_hp=90,
                boss_attack=15,
                reward_coin=75,
                reward_exp=75
            )

        elif opsi == 3:
            print("\nMelawan Boss Level 3...")
            sistem_battle(
                player,
                boss_hp=150,
                boss_attack=25,
                reward_coin=150,
                reward_exp=150
            )

        else:
            print("Pilihan tidak valid.")
