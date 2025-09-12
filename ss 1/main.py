import random 


welcome_message = "Selamat datang di program Python!"
chupy_position = random.randint(1,4)
print(welcome_message)

nama_user = input( "masukan nama anda :" )

bentuk_goa = "|_|"
goa_kosong =  [bentuk_goa] *4


goa = goa_kosong.copy()
goa[chupy_position -1] = "|0_0|"


print(f'''Halo {nama_user}, chupy si anjing lucu bersembunyi di salah satu goa dibawah ini
      {goa_kosong}''')
pilihan_user =int(input("menurut kamu dinomor berapa chupy berada? 1-2-3-4? "))

conf = input(f"apakah kamu yakin dengan pilihanmu {pilihan_user}? (y/n) ")

if conf == "n":
    print("oke program diakhiri ")
    exit()
elif conf == "y":
    if pilihan_user == chupy_position:
        print(f"{goa} selamat kamu menang")
    else:
        print(f"{goa} maaf kamu kalah")
    
else:
    print("input tidak valid, program diakhiri")
    exit()