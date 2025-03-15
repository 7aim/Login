import datetime
import json

"""
@Homework@
session management
hashing passwords
error handling
modular system
"""
LOG_DATA = "log.txt"
def loadLog():
        with open(LOG_DATA, 'r') as f:
            return f.read()      
def saveLog(log_data):
    with open(LOG_DATA, 'a') as f:
        f.write(log_data)

FILE_USERS = "users.json"
def loadUsers():
    try:
        with open(FILE_USERS, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
def saveUsers(user_data):
    with open(FILE_USERS, 'w') as f:
        json.dump(user_data, f, indent=4)

def saveLogTemp():
    for log in activity_log[-1:]:
        saveLog(f"{log['timestamp']} | {log['username']} | {log['action']} | {log['status']}\n")

#user,password,role
users = loadUsers()
#log
activity_log = []
#current account
logged_in = None

# Giris,cixis kimi emaliyyatlari qeyde alir.
def logActivity(username, action, status):
    timestamp = datetime.datetime.now()
    activity_log.append({
        'timestamp': timestamp,
        'username': username,
        'action': action,
        'status': status
    })
    return activity_log

# Qeydiyyat hissesi,qeydiyyatdan kecen ilk nefer admin hesab olunur.
def registerUser():
    global users
    #name
    user = input("Username: ")
    while len(user) < 3:
        print("Character number must be greater than 2")
        user = input("Username: ")
    while user in users:
        print("\nUser already exists!")
        user = input("Username: ")  

        logActivity(user, "Register Attempt", "Failure: User exists")
        saveLogTemp()    
    #password
    password = input("Password: ")
    while len(password) < 3:
        print("Password length must be greater than 5")
        password = input("Password: ")
    #role
    if len(users) == 0:
        role = 'admin'
    else:
        role = 'user'

    users[user] = {'password': password, 'role': role}
    saveUsers(users)
    print(f"\nRegistration successful. You're now {'admin' if role == 'admin' else 'user'}!")

    logActivity(user, "Register", "Success")
    saveLogTemp()

# Login hissesi
def loginUser():
    global logged_in
    #name
    user = input("Username: ")
    while user not in users:
        print("\nUser not found!")
        user = input("Username: ")

        logActivity(user, "Login Attempt", "Failure: User not found")
        saveLogTemp()
    #password
    password = input("Password: ")
    if users[user]['password'] == password:
        logged_in = user
        print(f"\nWelcome {user}!")

        logActivity(user, "Login", "Success")
        saveLogTemp()
    else:
        print("\nIncorrect password!")
        logActivity(user, "Login Attempt", "Failure: Wrong password")
        saveLogTemp()
        loginUser()

# Sifre sifirlama
def resetPassword():
    global logged_in

    if logged_in is None:
        print("\nYou need to login first!")

        logActivity(None, "Password Reset Attempt", "Failure: Not logged in")
        saveLogTemp()     
    # Admin basqalarinin sifresini deyise biler.
    if users[logged_in]['role'] == 'admin':
        target = input("Enter username to reset: ")
        if target not in users:
            print("\nUser not found!")

            logActivity(logged_in, "Admin Password Reset", f"Failure: {target} not found")
            saveLogTemp()
            resetPassword()
    else:
        target = logged_in
    
    new_pass = input("New password: ")
    users[target]['password'] = new_pass
    print("\nPassword updated successfully!")

    logActivity(logged_in, "Password Reset", f"Success: {target}'s password changed")
    saveLogTemp()

# Hesab silme
def deleteAccount():
    global logged_in, users

    if logged_in is None:
        print("\nLogin required!")

        logActivity(None, "Delete Attempt", "Failure: Not logged in")
        saveLogTemp() 
    if users[logged_in]['role'] == 'admin':
        target = input("Enter username to delete: ")
        if target not in users:
            print("\nUser not found!")

            logActivity(logged_in, "Admin Delete Attempt", f"Failure: {target} not found")
            saveLogTemp()          
    else:
        target = logged_in
    
    confirm = input(f"Delete {target}? (y/n): ").lower()
    if confirm == 'y':
        del users[target]
        print("\nAccount deleted!")

        logActivity(logged_in, "Account Deleted", f"Success: {target} removed")
        saveLogTemp()
        if target == logged_in:
            logged_in = None
    else:
        print("\nDeletion canceled!")
        logActivity(logged_in, "Delete Attempt", "Cancelled")
        saveLogTemp()

# Adminin deyisiklikler apardigi hisse(Qeydiyyatlara ve loga baxmaq,rol deyismek)
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
                saveLogTemp()
            else:
                print("\nInvalid role!")
        
        elif choice == '3':
            print("\nActivity Log:")
            print(loadLog())
        
        elif choice == '4':
            break
        
        else:
            print("\nInvalid choice!")

# Esas hisse
while True:
    print("\n" + "-"*30)

    # Hesab qeydiyyatdadirsa bu hisseye atir
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
            saveLogTemp()
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
    
    # Hesab qeydiyyatda deyilse bu hisseye atir
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