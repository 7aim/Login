import datetime
import hashlib
import json

# Sifre hashlama funksiyasi
def hashPassword(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

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

SESSION_DATA = "session.json"
def loadSession():
    try:
        with open(SESSION_DATA,"r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
def saveSession(session_data):
    with open(SESSION_DATA,"w") as f:
        json.dump(session_data, f, indent=4)

#user,password,role
users = loadUsers()
#log
activity_log = []
#current account
logged_in = loadSession()

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
        print("User already exists!\n")
        user = input("Username: ")  

        logActivity(user, "Register Attempt", "Failure: User exists")
        saveLogTemp()    
    #password
    password = input("Password: ")
    while len(password) < 3:
        print("Password length must be greater than 5")
        password = input("Password: ")
    hashed_password = hashPassword(password)
    #role
    if len(users) == 0:
        role = 'admin'
    else:
        role = 'user'

    users[user] = {'password': hashed_password, 'role': role}
    saveUsers(users)
    print(f"Registration successful. You're now {'admin' if role == 'admin' else 'user'}!\n")

    logActivity(user, "Register", "Success")
    saveLogTemp()

# Login hissesi
def loginUser():
    global logged_in
    #name
    user = input("Username: ")
    while user not in users:
        print("User not found!\n")
        user = input("Username: ")

        logActivity(user, "Login Attempt", "Failure: User not found")
        saveLogTemp()
    #password
    while True:
        password_login = input("Password: ")
        hashed_password_login = hashPassword(password_login)
        if hashed_password_login == users[user]['password']:
            logged_in = user
            saveSession(logged_in)
            print(f"Welcome {user}!\n")

            logActivity(user, "Login", "Success")
            saveLogTemp()
            break
        else:
            print("Incorrect password!\n")
            logActivity(user, "Login Attempt", "Failure: Wrong password")
            saveLogTemp()

# Sifre sifirlama
def resetPassword():
    

    if logged_in is None:
        print("You need to login first!\n")

        logActivity(None, "Password Reset Attempt", "Failure: Not logged in")
        saveLogTemp()     
    # Admin basqalarinin sifresini deyise biler.
    if users[logged_in]['role'] == 'admin':
        target = input("Enter username to reset: ")
        if target not in users:
            print("User not found!\n")

            logActivity(logged_in, "Admin Password Reset", f"Failure: {target} not found")
            saveLogTemp()
            resetPassword()
    else:
        target = logged_in
    
    new_pass = input("New password: ")
    new_pass = hashPassword(new_pass)
    users[target]['password'] = new_pass
    saveUsers(users)
    print("Password updated successfully!\n")

    logActivity(logged_in, "Password Reset", f"Success: {target}'s password changed")
    saveLogTemp()

# Hesab silme
def deleteAccount():
    global logged_in, users
    logged_in = loadSession()
    if logged_in is None:
        print("Login required!\n")

        logActivity(None, "Delete Attempt", "Failure: Not logged in")
        saveLogTemp() 
    if users[logged_in]['role'] == 'admin':
        target = input("Enter username to delete: ")
        if target not in users:
            print("User not found!\n")

            logActivity(logged_in, "Admin Delete Attempt", f"Failure: {target} not found")
            saveLogTemp()          
    else:
        target = logged_in
    
    confirm = input(f"Delete {target}? (y/n): ").lower()
    if confirm == 'y':
        del users[target]
        print("Account deleted!\n")

        logActivity(logged_in, "Account Deleted", f"Success: {target} removed")
        saveLogTemp()
        if target == logged_in:
            logged_in = None
    else:
        print("Deletion canceled!\n")
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
                print("User not found!\n")
                continue

            new_role = input("New role (admin/user): ").lower()

            if new_role in ['admin', 'user']:
                users[user]['role'] = new_role
                print("Role updated!\n")
                logActivity(logged_in, "Role Changed", f"{user} -> {new_role}")
                saveLogTemp()
            else:
                print("Invalid role!\n")
        
        elif choice == '3':
            print("\nActivity Log:\n")
            print(loadLog())
        
        elif choice == '4':
            break
        
        else:
            print("Invalid choice!\n")