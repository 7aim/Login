import login

while True:
    print("\n" + "-"*30)

    # Hesab qeydiyyatdadirsa bu hisseye atir
    logged_in = login.loadSession()
    if logged_in:
        print(logged_in)
        print(f"Logged in as: {logged_in} ({login.users[logged_in]['role']})")

        print("1. Logout")
        print("2. Reset Password")
        print("3. Delete Account")
        if login.users[logged_in]['role'] == 'admin':
            print("4. Admin Panel")
        print("5. Exit")
        
        choice = input("Select: ")
        
        if choice == '1':
            login.logActivity(logged_in, "Logout", "Success")
            with open("session.json", "w") as file:
                file.write("")
            login.saveLogTemp()
            logged_in = None
        elif choice == '2':
            login.resetPassword()
        elif choice == '3':
            login.deleteAccount()
        elif choice == '4' and login.users[logged_in]['role'] == 'admin':
            login.adminPanel()
        elif choice == '5':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice!")
    
    # Hesab qeydiyyatda deyilse bu hisseye atir
    else:

        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Select: ")
        
        if choice == '1':
            login.registerUser()
        elif choice == '2':
            login.loginUser()
        elif choice == '3':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice!")