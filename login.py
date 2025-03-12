import datetime
users = {}
activity_log = []
logged_in = None


def log_activity(username, action, status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    activity_log.append({
        'timestamp': timestamp,
        'username': username,
        'action': action,
        'status': status
    })

while True:

    print("\n0-Admin panel\n1-Register\n2-Login\n3-Reset password\n4-Logout\n5-Delece account")
    secim = input("0/1/2/3/4 : ")

    if secim == "0":
        while True:
            print("\n[ADMIN PANEL]")
            print("1. List users")
            print("2. Change user role")
            print("3. View activity log")
            print("4. Back")
            choice = input("Select: ")
            
            if choice == '1':
                print("\nRegistered Users:")
                for user, data in users.items():
                    print(f"- {user}")
            
            elif choice == '2':
                user = input("Username: ")
                if user not in users:
                    print("\nUser not found!")
                    continue
                new_role = input("New role (admin/user): ").lower()
                if new_role in ['admin', 'user']:
                    users[user]['role'] = new_role
                    print("\nRole updated!")
                    log_activity(logged_in, "Role Changed", f"{user} -> {new_role}")
                else:
                    print("\nInvalid role!")
            
            elif choice == '3':
                print("\nActivity Log:")
                for log in activity_log[-10:]:
                    print(f"{log['timestamp']} | {log['username']} | {log['action']} | {log['status']}")
            
            elif choice == '4':
                break
            
            else:
                print("\nInvalid choice!")
    
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


        