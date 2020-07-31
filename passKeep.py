from passwords import *
import time
from getpass import getpass

while True:
    print("Enter option you want:")
    print("1 - Login")
    print("2 - Sign up")
    print("3 - Exit")
    opt = input()

    try:
        opt = int(opt)
    except:
        print("Incorrect option")
        continue

    if opt is 1:
        username = input("Login: ")
        #password = input("Password:")
        password = getpass()

        try:
            b = login(username, password)
            if b is -1:
                raise Exception
            print("Logged in as", username, "\n")
            break
        except:
            print("Incorrect credentials")
            continue
    
    if opt is 2:
        username = input("Login: ")
        
        while True:
            password = getpass()
            passwordConfirm = getpass("Confirm password: ")

            if password in passwordConfirm:
                break
            else:
                continue
        
        ret = newUser(username, password)
        if ret is -1:
            print("an error occured adding user")
        else:
            print(ret)
        print("\n")
        continue
    
    if opt is 3:
        exit()

    else:
        print("Incorrect option")
        continue

while True:
    print("--------MAIN MENU--------")
    print("1 - List all your saved services")
    print("2 - Lookup service by name")
    print("3 - Add a service")
    print("4 - Exit")
    print("-------------------------")

    inp = input("Enter an option: ")

    try:
        inp = int(inp)
    except:
        print("\nIncorrect option\n")
        continue
    
    if inp is 1:
        services = listAllServices(username)
        print(services, "\n")
        input("Press enter key to continue")
        continue

    if inp is 2:
        service = input("Enter service name: ")
        cred, s = getServiceCredentials(username, service, password)
        if cred is -1:
            print(f"Service {s} not found in user database")
        elif cred is 0:
            print("Could not verify master password")
        else:
            print(cred)
        input("Press enter key to continue")
        print("\n")
        continue

    if inp is 3:
        service = input("Enter service name: ")
        serviceUsername = input("Enter service username: ")
        servicePass = getpass("Enter service password: ")

        r = addService(username, password, service, serviceUsername, servicePass)
        if r is -1:
            print("An error occured adding service")
        else:
            print(f"{service} has been added to password keeper")
        input("\nPress enter key to continue")
        print("\n")
        continue

    if inp is 4:
        try:
            disconnect()
        except:
            print("err")
        exit()

    else:
        print("\nIncorrect option\n")