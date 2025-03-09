users = {}
#logged_in = None

while True:

    print("\n1-Register\n2-Login\n3-Reset password\n4-Logout\n")
    secim = input("1/2/3/4 : ")
    
    if secim == "1":
        user = input("Username: ")
        if user not in users:
            users[user] = input("Şifre: ")
            print("\nRegistration complete")
        else:
            print("\nUser already exists")
    
    if secim == "2":
        user = input("UsernAme: ")
        if users[user] == input("Şifre: "):
            #logged_in = user
            print(f"\nWelcome {user}!")
        else:
            print("\nIncorrect input")
    
    if secim == "3":
        user = input("Username: ")
        if user in users:
            users[user] = input("NEw password: ")
            print("\nPassword changed!")
        else:
            print("\nNo user")
    
    if secim == "4":
        print("Exited")
        #logged_in = None
        
