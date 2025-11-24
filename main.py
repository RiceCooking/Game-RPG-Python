from src.halaman_masuk import halaman_masuk, players, users, loading, clear

sign_in = True
login_s = None

while sign_in == True:
    hasil = halaman_masuk()
    # Kalau user minta KELUAR (return False)
    if hasil == False:
        sign_in = False
    # Kalau user berhasil LOGIN (return Data User)
    elif hasil is not None:
        login_s = hasil

    while login_s != None:
        #TODO
        pass
