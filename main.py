############################################
#### DATABASE STRUCTURE ######
"""
Users:indx,id,pass,stat
cnvs:sender, reciever, chron, contents, stat
"""
###########################################
#Author: adityan
############################################
#### LIBRARIES ######
from os import system, name
import time
import mysql.connector
from clint.textui import colored, puts
mydb = mysql.connector.connect(host="hosthere",user="username",password="password", database = 'dbname')
mycursor = mydb.cursor()
############################################
#### VARIABLES #####
pascal = """

                                                  _..._                    
                                               .-'_..._''.           .---. 
_________   _...._                           .' .'      '.\          |   | 
\        |.'      '-.                       / .'                     |   | 
 \        .'```'.    '.                    . '                       |   | 
  \      |       \     \   __              | |                 __    |   | 
   |     |        |    |.:--.'.         _  | |              .:--.'.  |   | 
   |      \      /    ./ |   \ |      .' | . '             / |   \ | |   | 
   |     |\`'-.-'   .' `" __ | |     .   | /\ '.          .`" __ | | |   | 
   |     | '-....-'`    .'.''| |   .'.'| |// '. `._____.-'/ .'.''| | |   | 
  .'     '.            / /   | |_.'.'.-'  /    `-.______ / / /   | |_'---' 
'-----------'          \ \._,\ '/.'   \_.'              `  \ \._,\ '/      
                        `--'  `"                            `--'  `"       

"""
psmall = """
    ____  ___   _____ _________    __ 
   / __ \/   | / ___// ____/   |  / / 
  / /_/ / /| | \__ \/ /   / /| | / /  
 / ____/ ___ |___/ / /___/ ___ |/ /___
/_/   /_/  |_/____/\____/_/  |_/_____/
                                      
"""
x = True
############################################
#### FUNCTIONS #####
### Generic ###
#Clear
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
#colored print
def gprint(t):
    puts(colored.cyan(t))
def rprint(t):
    puts(colored.red(t))
def bprint(t):
    puts(colored.blue(t))
### User Interface ###
#splash screen
def splash(pascal):
    clear()
    gprint(pascal)
    rprint('----by adityan')
    time.sleep(1)

def onquit(psmall):
    clear()
    print()
    print()
    print()
    print()
    print('\t\t\t\t\t\tThank you for using Pascal')
    print()
    print()
    print()
    print()
    time.sleep(0.5)
    clear()

def invalidinp():
    clear()
    print()
    print()
    print()
    print()
    print('\t\t\t\t\t\tInvalid Input')
    print()
    print()
    print()
    print()
    time.sleep(0.5)
    clear()

### User Management ###
#Get Users - works
def getuser(id):
    mycursor.execute('select * from users where id = "' + id + '";')
    l = mycursor.fetchall()
    mydb.commit()
    return l

#authenticate user
def authuser(id,passwd):
    l = getuser(id)
    if len(l) == 0:
        return 1
    else:
        if l[0][1] == passwd:
            return 0
        else:
            return 2

#Create User - works 
def createuser(id,passwd):
    #returns 1 if the user was created succesfully and 0 if the user exists
    #check if the user exists
    l = getuser(id)
    if len(l) == 0:
        #get index
        mycursor.execute('select max(indx) from users')
        l = mycursor.fetchall()
        indx = l[0][0] + 1
        #stat
        stat = 't'
        #create user
        c = 'insert into users(id, pass, stat, indx) values(%s,%s,%s,%s)'
        v = (id,passwd,stat,indx)
        mycursor.execute(c,v)
        mydb.commit()
        return 0
    else:
        return 1

#Change User Status
def updateuserstat(id,stat):
    l = getuser(id)
    c = 'update users set stat="%s" where id="%s";'
    v = (stat,id)
    mycursor.execute(c,v)
    mydb.commit()
    return 0

####################################################
####################################################
### Conversational ###
#Getting all the messeges and processing them
def getmsgs():
    mycursor.execute('select * from cnvs;')
    l = mycursor.fetchall()
    mydb.commit()
    return l

#Checking if there have been messeges between two people
def checkmsg(id,rcv):
    l = getmsgs()
    if len(l) == 0: return 1
    else:
        for i in l:
            if id == i[0][1:-1]:#sender is the same as id or if it is the same as the reciver
                return 0
            elif rcv == i[0][1:-1]:
                return 0#there are messeges
            else:
                return 1#there arent any messeges

#Getting the max(chron) value - works
def maxchron():
    l = getmsgs()
    chron = []
    for i in l:
        chron.append(i[2])
    if len(chron) != 0:return max(chron)
    
#Display messeges
def displaymsg(id,recv):
    #get all the messeges where the user is either the person sending the messege or reciving it
    l = getmsgs()
    for i in l:
        if id == i[0][1:-1] and recv == i[1][1:-1]:#if the messege was sent by the user
            bprint(f'\t\t\t You: {i[3][1:-1]}')
        elif recv == i[0][1:-1] and id == i[1][1:-1]:#if the messege was sent by the talker person
            rprint(f'{recv} : {i[3][1:-1]}')
        else:
            print()

#Sending a messege - works
def sendmsg(id,rcv,cnts):#takes in the id, the rcv messege contents
    #check if messeges exist btw these two people
    c = checkmsg(id,rcv)
    if c == 1:#no messeges
        #send a messege from id to rcv
        #get chron
        chron = 1
        #set stat
        stat = 'f'#not read
        c = 'insert into cnvs(sender,receiver,chron,contents,stat) values("%s","%s",%s,"%s","%s");'
        v = (id,rcv,chron,cnts,stat)
        mycursor.execute(c,v)
        mydb.commit()
    else:
        #send messege from id to rcv
        #get chron
        chron = maxchron() + 1
        #set stat
        stat = 'f'
        c = 'insert into cnvs(sender,receiver,chron,contents,stat) values("%s","%s",%s,"%s","%s");'
        v = (id,rcv,chron,cnts,stat)
        mycursor.execute(c,v)
        mydb.commit()

#creating a contact list
def contactlist(id):
    l = getmsgs()
    l1 = []
    for i in l:
        if i[0][1:-1] not in l1 and i[0][1:-1] != id:
            l1.append(i[0][1:-1])
        elif i[1][1:-1] not in l1 and i[1][1:-1] != id:
            l1.append(i[1][1:-1])
        else:#is in the list
            continue
    return l1

def chat(id,recv):
    while True:
        clear()
        gprint(psmall)
        print('-----------------------------------------------------------------------')
        print(f'{recv} | Type !r to reload !b to go back and !q to quit')
        print('-----------------------------------------------------------------------')
        displaymsg(id,recv)
        print('-----------------------------------------------------------------------')
        msg = str(input('>'))
        if msg == '!b':
            break
        elif msg == '!r':
            continue
        elif msg == '!q':
            clear()
            exit()
        else:
            sendmsg(id,recv,msg)

def rchat(id):
    while z:
        clear()
        gprint(psmall)
        bprint(f'Welcome {id}')
        gprint(f'1. Contact List')
        gprint(f'2. New Conversation')
        #search for a user
        gprint(f'3. Log into another account')
        gprint(f'4. Exit')
        chc = int(input("> "))
        if chc == 1:
            #bring up the contact list
            clear()
            gprint(psmall)
            bprint('Contact List')
            cl = contactlist(id)
            if len(cl) != 0:# if the contact list is not empty
                a = 1
                for i in cl:
                    rprint(f'{a}. {i}')
                    a += 1
                recv = str(input(">"))
                if recv not in cl:
                    bprint('Starting a new Conversation')
                    time.sleep(0.5)
                    chat(id,recv)
                else:
                    chat(id,recv)
        elif chc == 2:
            bprint('New conversation')
            recv = str(input("Enter Username of User: "))
            l = getuser(recv)
            if len(l) != 0:
                chat(id,recv)
            else:
                print()
                print()
                print()
                print()
                bprint('\t\t\t\t\tThe User doesnt exits')
                print()
                print()
                print()
                print()
                time.sleep(0.5)
                continue
        elif chc == 3:
            y = False
            break
        elif chc == 4:
            clear()
            exit()
        else:
            invalidinp()
            continue

############################################
#### RUNTIME ######
#code structure
### Main Loop
    ## Login/Signup/Quit
        # Login
            # Contact List
            # New Conversation
            # Different Account
            # Quit
        # Signup
            # Contact List 
            # New Conversation
            # Different Account
            # Quit
        # Quit
#############################################
#### CODE ###
x = True
y = True
z = True
while x:
    #login/signup/quit loop
    splash(pascal)
    x = True
    clear()
    gprint(psmall)
    gprint("Pascal is a chat application that works over the internet. You can either Log in or Sign up.")
    rprint('1. Login')
    rprint('2. Signup')
    rprint('3. Quit out of the application')
    ch = int(input('> '))
    if ch == 1:#log in
        while y:
            y = True
            clear()
            gprint(psmall)
            gprint('Login')
            id = str(input('Username: '))
            passwd = str(input('Password: '))
            clear()
            l = getuser(id)
            auth = authuser(id,passwd)
            if auth == 1:
                clear()
                print()
                print()
                print()
                print()
                bprint('\t\t\t\t\tUser Doesnt Exist; Please try again')
                print()
                print()
                print()
                print()
                time.sleep(0.5)
                continue
            elif auth == 2:
                print()
                print()
                print()
                print()
                bprint('\t\t\t\t\tPasswords dont match; Please try again')
                print()
                print()
                print()
                print()
                time.sleep(0.5)
                continue
            else:
                gprint(psmall)
                rchat(id)
                pass
        else:
            if x == False:
                clear()
                break
    elif ch == 2:#signup
        while y:
            y = True
            clear()
            gprint(psmall)
            gprint('Signup')
            id = str(input('Username: '))
            passwd = str(input('Password: '))
            clear()
            c = createuser(id,passwd)
            if c == 0:
                gprint(psmall)
                rchat(id)
            else:
                print()
                print()
                print()
                print()
                print('\t\t\t\t\tUser Exists, Try logging in')
                print()
                print()
                print()
                print()
                x = False
        else:
            if x == False:
                clear()
                break

    elif ch == 3:onquit(psmall);break
    else:clear();invalidinp();continue
#############################################