import datetime

#user,password,role
users = {}

#log
activity_log = []

#current account
logged_in = None

#Giris,cixis kimi emaliyyatlari qeyde alir.
def log_activity(username, action, status):
    timestamp = datetime.datetime.now()
    activity_log.append({
        'timestamp': timestamp,
        'username': username,
        'action': action,
        'status': status
    })

#Qeydiyyat hissesi,qeydiyyatdan kecen ilk nefer admin hesab olunur.
def register_user():

    user = input("Username: ")
    if user in users:
        print("\nUser already exists!")
        log_activity(user, "Register Attempt", "Failure: User exists")
         
    password = input("Password: ")

    if len(users) == 0:
        role = 'admin'
    else:
        role = 'user'

    users[user] = {'password': password, 'role': role}
    print(f"\nRegistration successful. You're now {'admin' if role == 'admin' else 'user'}!")
    log_activity(user, "Register", "Success")

#Login hissesi
def login_user():
    global logged_in
    user = input("Username: ")
    if user not in users:
        print("\nUser not found!")
        log_activity(user, "Login Attempt", "Failure: User not found")
         
    password = input("Password: ")
    if users[user]['password'] == password:
        logged_in = user
        print(f"\nWelcome {user}!")
        log_activity(user, "Login", "Success")
    else:
        print("\nIncorrect password!")
        log_activity(user, "Login Attempt", "Failure: Wrong password")

#Sifre sifirlama
def reset_password():
    global logged_in
    if logged_in is None:
        print("\nYou need to login first!")
        log_activity(None, "Password Reset Attempt", "Failure: Not logged in")
        
    #admin basqalarinin sifresini deyise biler.
    if users[logged_in]['role'] == 'admin':
        target = input("Enter username to reset: ")
        if target not in users:
            print("\nUser not found!")
            log_activity(logged_in, "Admin Password Reset", f"Failure: {target} not found")
            reset_password()
                    
    else:
        target = logged_in
    
    new_pass = input("New password: ")
    users[target]['password'] = new_pass
    print("\nPassword updated successfully!")
    log_activity(logged_in, "Password Reset", f"Success: {target}'s password changed")

#Hesab silme
def delete_account():
    global logged_in, users
    if logged_in is None:
        print("\nLogin required!")
        log_activity(None, "Delete Attempt", "Failure: Not logged in")
        
    
    if users[logged_in]['role'] == 'admin':
        target = input("Enter username to delete: ")
        if target not in users:
            print("\nUser not found!")
            log_activity(logged_in, "Admin Delete Attempt", f"Failure: {target} not found")
            
    else:
        target = logged_in
    
    confirm = input(f"Delete {target}? (y/n): ").lower()
    if confirm == 'y':
        del users[target]
        print("\nAccount deleted!")
        log_activity(logged_in, "Account Deleted", f"Success: {target} removed")
        if target == logged_in:
            logged_in = None
    else:
        print("\nDeletion canceled!")
        log_activity(logged_in, "Delete Attempt", "Cancelled")

#Adminin deyisiklikler apardigi hisse(Qeydiyyatlara ve loga baxmaq,rol deyismek)
def admin_panel():
    while True:
        print("\n[ADMIN PANEL]")
        print("1. List users")
        print("2. Change user role")
        print("3. View activity log")
        print("4. Back")
        choice = input("Select: ")
        
        if choice == '1':
            print("\nRegistered Users:")
            for user in users.items():
                print(f"- user : {user[0]} --- role : {user[1]["role"]}")
        
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

#Esas hisse
while True:
    print("\n" + "-"*30)

    #hesab qeydiyyatdadirsa bu hisseye atir
    if logged_in:
        print(f"Logged in as: {logged_in} ({users[logged_in]['role']})")

        print("1. Logout")
        print("2. Reset Password")
        print("3. Delete Account")
        if users[logged_in]['role'] == 'admin':
            print("4. Admin Panel")
        print("5. Exit")
        
        choice = input("Select: ")
        
        if choice == '1':
            log_activity(logged_in, "Logout", "Success")
            logged_in = None
        elif choice == '2':
            reset_password()
        elif choice == '3':
            delete_account()
        elif choice == '4' and users[logged_in]['role'] == 'admin':
            admin_panel()
        elif choice == '5':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice!")
    
    #hesab qeydiyyatda deyilse bu hisseye atir
    else:

        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Select: ")
        
        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice!")
