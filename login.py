import datetime

"""
@Homework@
users, activity_log should be as external file (.txt)
session management
hashing passwords
error handling
modular system
"""
#user,password,role
users = {}

#log
activity_log = []

#current account
logged_in = None

#Giris,cixis kimi emaliyyatlari qeyde alir.
def logActivity(username, action, status):
    timestamp = datetime.datetime.now()
    activity_log.append({
        'timestamp': timestamp,
        'username': username,
        'action': action,
        'status': status
    })

#Qeydiyyat hissesi,qeydiyyatdan kecen ilk nefer admin hesab olunur.
def registerUser():

    user = input("Username: ")
    if user in users:
        print("\nUser already exists!")
        logActivity(user, "Register Attempt", "Failure: User exists")
         
    password = input("Password: ")

    if len(users) == 0:
        role = 'admin'
    else:
        role = 'user'

    users[user] = {'password': password, 'role': role}
    print(f"\nRegistration successful. You're now {'admin' if role == 'admin' else 'user'}!")
    logActivity(user, "Register", "Success")

#Login hissesi
def loginUser():
    global logged_in
    user = input("Username: ")
    if user not in users:
        print("\nUser not found!")
        logActivity(user, "Login Attempt", "Failure: User not found")
         
    password = input("Password: ")
    if users[user]['password'] == password:
        logged_in = user
        print(f"\nWelcome {user}!")
        logActivity(user, "Login", "Success")
    else:
        print("\nIncorrect password!")
        logActivity(user, "Login Attempt", "Failure: Wrong password")

#Sifre sifirlama
def resetPassword():
    global logged_in
    if logged_in is None:
        print("\nYou need to login first!")
        logActivity(None, "Password Reset Attempt", "Failure: Not logged in")
        
    #admin basqalarinin sifresini deyise biler.
    if users[logged_in]['role'] == 'admin':
        target = input("Enter username to reset: ")
        if target not in users:
            print("\nUser not found!")
            logActivity(logged_in, "Admin Password Reset", f"Failure: {target} not found")
            resetPassword()
                    
    else:
        target = logged_in
    
    new_pass = input("New password: ")
    users[target]['password'] = new_pass
    print("\nPassword updated successfully!")
    logActivity(logged_in, "Password Reset", f"Success: {target}'s password changed")

#Hesab silme
def deleteAccount():
    global logged_in, users
    if logged_in is None:
        print("\nLogin required!")
        logActivity(None, "Delete Attempt", "Failure: Not logged in")
        
    
    if users[logged_in]['role'] == 'admin':
        target = input("Enter username to delete: ")
        if target not in users:
            print("\nUser not found!")
            logActivity(logged_in, "Admin Delete Attempt", f"Failure: {target} not found")
            
    else:
        target = logged_in
    
    confirm = input(f"Delete {target}? (y/n): ").lower()
    if confirm == 'y':
        del users[target]
        print("\nAccount deleted!")
        logActivity(logged_in, "Account Deleted", f"Success: {target} removed")
        if target == logged_in:
            logged_in = None
    else:
        print("\nDeletion canceled!")
        logActivity(logged_in, "Delete Attempt", "Cancelled")

#Adminin deyisiklikler apardigi hisse(Qeydiyyatlara ve loga baxmaq,rol deyismek)
def adminPanel():
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
                logActivity(logged_in, "Role Changed", f"{user} -> {new_role}")
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
            logActivity(logged_in, "Logout", "Success")
            logged_in = None
        elif choice == '2':
            resetPassword()
        elif choice == '3':
            deleteAccount()
        elif choice == '4' and users[logged_in]['role'] == 'admin':
            adminPanel()
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
            registerUser()
        elif choice == '2':
            loginUser()
        elif choice == '3':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice!")