#import the following modules
from tkinter import *
import csv, os, itertools, webbrowser
#create a dictioanry that stores a list of all the users
user = {}
headers = ['Account Username', 'Account Password', 'TV Programs  Purchased']
headers2 = ['Program Name', 'Program Description', 'Program Price', 'Program Rating', 'Program Reviews', 'Image', 'Url']
#class that keeps track of all the customers
class Customer:
    #constructor that initilizes the variables
    def __init__(self, auName, aPass, pShows):
        self.auName = auName
        self.aPass = aPass
        #the purchased shows that are sent to the function are part of a string, which is split into a list in the class
        self.pShows = pShows.split(',')
    #function that returns a variable that displays the user's account info.
    def pInfo(self):
        aInfo = 'Username: '+self.auName+' Password: '+self.aPass+'\nTransaction History:\n'
        shows = dict(itertools.zip_longest(*[iter(self.pShows)] * 2, fillvalue=""))
        for key, value in shows.items():
            aInfo+=key+':'+value+'\n'
        return aInfo
    #function that records the shows that the user has pruchased
    def transactions(self, sName, price):
        #append the purchased shows in the list
        if self.pShows[0] == 'none':
            self.pShows[0] = sName
            self.pShows.append(price)
        else:
            self.pShows.append(sName)
            self.pShows.append(price)
        numRow = 0
        pShows = ",".join(self.pShows)
        #opens the file in readmode and finds the row to record the transactions
        with open('Accounts.csv', 'r') as csvFile:
            readCSV = csv.DictReader(csvFile);
            for row in readCSV:
                numRow+=1
                if self.auName == row['Account Username']:
                    editR = numRow
        #Stores the contents of the csv file as a list and writes the new transactions into the list and then writes the data in the list as a file
        reader = csv.reader(open('Accounts.csv'))
        allUsers = list(reader)
        allUsers[editR][2] = pShows
        with open('Accounts.csv', 'w', newline='') as csvFile:
            Writer = csv.writer(csvFile)
            for cell in allUsers:
                Writer.writerow(cell)
#function that writes each user's information to the csv file when a new account is created
def writeTofile(auName):
    pShows = ",".join(user[auName].pShows)
    with open('Accounts.csv', 'a', newline='') as csvFile:
        writeCSV= csv.DictWriter(csvFile, fieldnames=headers)
        writeCSV.writerow({'Account Username': user[auName].auName, 'Account Password': user[auName].aPass, 'TV Programs  Purchased': pShows})
#function that creates the account for the user and stores the account as an object of the class Customer
def account():
    def cAccount():
        #checks to see if that username is already taken or not. If the username is not taken that an account can be created
        with open('Accounts.csv', 'r') as csvFile:
            readCSV = csv.DictReader(csvFile); checker = False
            for row in readCSV:
                if entry4.get() == row['Account Username']:
                    checker = True
        if checker == False:
            user[entry4.get()] = Customer(entry4.get(), entry5.get(), 'none') #an object is created for the user and stored in the dictionary. The key is the account username of the user
            writeTofile(entry4.get())
            menu2(entry4.get())
            #destroy the old window
            window3.destroy()
        else:
            print('Error! That username is already taken')
    os.system('cls')
    #create a new window
    window3 = Tk()
    window3.title('FanFavTV')
    window3.geometry('+650+115')
    text1 = Label(window3, text='Please enter your username').grid(row=0, column=0, sticky='w')
    text2= Label(window3, text='Please enter your password and click continue').grid(row=1, column=0, sticky='w')
    #create entry boxes to accept input from the user
    entry4 = StringVar()
    entry4 = Entry(window3)
    entry4.grid(row=0, column=1)
    entry5 = StringVar()
    entry5 = Entry(window3)
    entry5.grid(row=1, column=1)
    button = Button(text='Continue', fg='white', bg='green', command=cAccount).grid(row=2, column=0)
#function that accepts the credit card number when the user chooses to purchase a show
def credit(auName):
    #this function is run when the button is clicked. It repeatedly promts the user to enter an acceptable credit card number. Afterwards it returns the user to the purchasing menu.
    def checkcNum():
        checker = False
        def congrats():
            #destroy the old window
            window10.destroy()
        try:
            if int(entry5.get()) >1000 and int(entry5.get())<9999:
                os.system('cls')
                checker = True
                window9.destroy()
                window10 = Tk()
                window10.title('FanFavTV')
                window10.geometry('+650+115')
                text1= Label(window10, text="Congatulations! Enjoy the show\n and don't forget to rate and review\n the show after watching.").grid(row=0, column=0, sticky='w')
                button1= Button(window10, text='Continue', fg='white', bg='green',command =congrats).grid(row=1, column=0)
        except ValueError:
            print('Error, Please enter a corect credit card number')
        if checker==False:
            os.system('cls')
            print('Error, Please enter a corect credit card number')
    os.system('cls')
    #create a new window
    window9 = Tk()
    window9.title('FanFavTV')
    window9.geometry('+650+115')
    text1 = Label(window9, text='Please enter your 4 digit credit card number: ').grid(row=0, column=0, sticky='w')
    #create entry boxes to accept input from the user
    entry5 = IntVar()
    entry5 = Entry(window9)
    entry5.grid(row=0, column=1)
    button = Button(window9, text='Continue',  fg='white', bg='green', command =checkcNum).grid(row=1, column=0)
    mainloop()
#function to allow users to uy the shows
def bShows(auName):
    #this funtion is run when the first button is clicked
    def browseMethods():
        #if the user chose option 1 then run the search funtion
        if var3.get() == 1:
            def search():
                #if the user searches for a show not in the database then they will be returned to the browsing menu
                def invalidShow():
                    window7.destroy(); bShows(auName)
                #if the user chooses to purchase the show then the transaction is recorded and they are asked toenter their credit card number
                def buy(sName, sPrice):
                    window8.destroy()
                    if var4.get() == 1:
                        user[auName].transactions(sName, sPrice); os.system('cls'); credit(auName); bShows(auName)
                    elif var4.get() == 2:
                        os.system('cls'); bShows(auName)
                #the user will be unable to purchase the a previously purchased show
                with open('TVShows.csv', 'r') as csvFile:
                    readCSV = csv.DictReader(csvFile); checker = False
                    for row in readCSV:
                        if entry3.get().upper() == row['Program Name']:
                            checker2 = False
                            for shows in user[auName].pShows:
                                if row['Program Name'] == shows:
                                    window7.destroy()
                                    print("Sorry but you have already purchased this show!\nPlease select another show to pucrchase")
                                    bShows(auName)
                                    checker2 = True
                            #if they haven't purchased this show before then the show's infomation page is displayed
                            if checker2 == False:
                                sName = row['Program Name']; sPrice = row['Program Price']
                                window7.destroy()
                                window8 = Tk()
                                window8.title('FanFavTV')
                                window8.geometry('+100+115')
                                Scroll1 = Scrollbar(window8)
                                cover = PhotoImage(file=row['Image'])
                                #this variable contanes the image of the show
                                TextImage = Label(window8, image=cover).pack(side=LEFT)
                                Text1 = Text(window8, height=4, width=50)
                                Scroll1.pack(side=RIGHT, fill=Y)
                                Text1.pack(side=LEFT, fill=Y)
                                Scroll1.config(command=Text1.yview)
                                Text1.config(yscrollcommand=Scroll1.set)
                                sInfo = 'Program Name: '+row['Program Name']+'\nProgram Description: '+row['Program Description']+'\nProgram Price: '+row['Program Price']+'\nProgram Rating: '+row['Program Rating']+'\nUser Reviews:'+'\n'+row['Program Reviews']
                                Text1.insert(END, sInfo)
                                var4 = IntVar()
                                text2 = Label(window8, text='Would you like to purchase this show!').pack()
                                Radiobutton(window8, text='Yes', padx=20, variable=var4, value=1).pack()
                                Radiobutton(window8, text='No', padx = 20, variable=var4, value=2).pack()
                                button = Button(window8, text='Continue', fg='white', bg='green', command = lambda: buy(sName, sPrice)).pack()
                                #open the url if the user requires more info
                                def openurl():
                                    webbrowser.open(row['Url'])
                                text3 = Label(window8, text='Would you like to view more information?\n If so then press the Info button').pack()
                                button2 = Button(window8, text='Info', fg='white', bg='orange', command = openurl).pack()
                                mainloop()
                #if the user searches for a show not in the database then the error message will be displayed
                if checker == False:
                    text1 = Label(window7, text='Error! No results found! Press').grid()
                    button = Button(window7, text=' Return', fg='white', bg='purple', command = invalidShow).grid()
            window6.destroy()
            #create new window
            window7 = Tk()
            window7.title('FanFavTV')
            window7.geometry('+650+115')
            text1 = Label(window7, text='Please enter the name of the show: ').grid(row=0, column=0, sticky='w')
            #entry variable to accpet user input
            entry3 = StringVar()
            entry3 = Entry(window7)
            entry3.grid(row=0, column=1)
            #run the search funtion when this button is pressed
            button = Button(window7, text='Continue', fg='white', bg='green', command = search).grid(row=1, column=0)
        elif var3.get() == 2:
            def order():
                window11.destroy()
                aShows = ''
                #read the tv show csv file as a list
                data = csv.reader(open('TVShows.csv'))
                tvShows = list(data)
                if var5.get() == 1:
                    #if the user chose to view the shows in alphabetical order then run the abShow function
                    def abShow():
                        index = int(entry6.get())
                        #the user is prohibited from purchasing the same show again
                        for series in user[auName].pShows:
                            if series == aList[index-1][0]:
                                print('Error! You have already purchased this show!')
                                os.system('cls'); window12.destroy(); bShows(auName)
                        try:
                            #record the transacion if the user chose to buy the game, otherwise, send them back to the browsing menu
                            def buy2(sName, sPrice):
                                window13.destroy()
                                if var6.get() == 1:
                                    user[auName].transactions(sName, sPrice); os.system('cls'); credit(auName); bShows(auName)
                                elif var6.get() == 2:
                                    os.system('cls'); bShows(auName)
                            #send the user back to the browsing menu if he/she enters 0. Otherwise, display the information page of that show and ask the user if he/she wishes to make a purchase
                            if int(entry6.get()) == 0:
                                os.system('cls'); window12.destroy(); bShows(auName)
                            elif int(entry6.get())<0 or int(entry6.get())>10:
                                print('Error! Please enter a number in the specified range.')
                            else:
                                os.system('cls'); sInfo = ''
                                window12.destroy()
                                window13 = Tk()
                                window13.title('FanFavTV')
                                window13.geometry('+100+115')
                                Scroll = Scrollbar(window13)
                                cover = PhotoImage(file=aList[index-1][5])
                                TextImage = Label(window13, image=cover).pack(side=LEFT)
                                Text1 = Text(window13, height=4, width=50)
                                Scroll.pack(side=RIGHT, fill=Y)
                                Text1.pack(side=LEFT, fill=Y)
                                Scroll.config(command=Text1.yview)
                                Text1.config(yscrollcommand=Scroll.set)
                                sInfo += 'Program Name: '+aList[index-1][0]+'\nProgram Description: '+aList[index-1][1]+'\nProgram Price: '+aList[index-1][2]+'\nProgram Rating: '+aList[index-1][3]+'\nUser Reviews:'+'\n'+aList[index-1][4]
                                Text1.insert(END, sInfo)
                                var6 = IntVar()
                                text2 = Label(window13, text='Would you like to purchase this show!').pack()
                                Radiobutton(window13, text='Yes', padx=20, variable=var6, value=1).pack()
                                Radiobutton(window13, text='No', padx = 20, variable=var6, value=2).pack()
                                button = Button(window13, text='Continue', fg='white', bg='green', command = lambda: buy2(aList[index-1][0], aList[index-1][2])).pack()
                                text3 = Label(window13, text='Would you like to view more information?\n If so then press the Info button').pack()
                                def openurl():
                                    webbrowser.open(aList[index-1][6])
                                button2 = Button(window13, text='Info', fg='white', bg='orange', command = openurl).pack()
                                mainloop()
                        except ValueError:
                            print('Error, Please enter one of the numbers listed')
                    #Append the information of each tv show in a list
                    aList = []
                    for row in tvShows[1:]:
                        aList.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
                    #sort the list by alphabetical order
                    aList = sorted(aList)
                    #display the shows and a number beside each show so the user can choose which show they would like to purchase
                    counter = 0
                    for show in aList:
                        counter +=1
                        aShows += show[0]+' - '+str(counter)+'\n'
                    window12 = Tk()
                    #create a new window
                    window12.title('FanFavTV')
                    window12.geometry('+180+115')
                    Scroll = Scrollbar(window12)
                    Text1 = Text(window12, height=4, width=50)
                    Scroll.pack(side=RIGHT, fill=Y)
                    Text1 .pack(side=LEFT, fill=Y)
                    Scroll.config(command=Text1.yview)
                    Text1.config(yscrollcommand=Scroll.set)
                    Text1.insert(END, aShows)
                    Text2 = Label(window12, text="Please enter the number beside the name of the show\nyou would like to pucrchase. Otherwise press 0 to go back.").pack()
                    entry6 = IntVar()
                    entry6 = Entry(window12)
                    entry6.pack()
                    button = Button(window12, text='Continue', fg='white', bg='green', command =abShow).pack()
                #if the user selects option 2 then he/she can choose how to view the shows
                #Note to Mr. Hughes. In the following lines I know I have  used the same code twice. However, I ran into problems when making functions so please excuse my reusing of code.
                elif var5.get() == 2:
                    #if the user chose to view the shows by order of ratings
                    def rbShow():
                        index = int(entry6.get())
                        #the user is prohibited from purchasing the same show again
                        for series in user[auName].pShows:
                            if series == theList[index-1][0]:
                                print('Error! You have already purchased this show!')
                                os.system('cls'); window12.destroy(); bShows(auName)
                        try:
                            #record the transacion if the user chose to buy the game, otherwise, send them back to the browsing menu
                            def buy2(sName, sPrice):
                                window13.destroy()
                                if var6.get() == 1:
                                    user[auName].transactions(sName, sPrice); os.system('cls'); credit(auName); bShows(auName)
                                elif var6.get() == 2:
                                    os.system('cls'); bShows(auName)
                            #send the user back to the browsing menu if he/she enters 0. Otherwise, display the information page of that show and ask the user if he/she wishes to make a purchase
                            if int(entry6.get()) == 0:
                                os.system('cls'); window12.destroy(); bShows(auName)
                            elif int(entry6.get())<0 or int(entry6.get())>10:
                                print('Error! Please enter a number in the specified range.')
                            else:
                                os.system('cls'); sInfo = ''
                                window12.destroy()
                                window13 = Tk()
                                window13.title('FanFavTV')
                                window13.geometry('+100+115')
                                Scroll = Scrollbar(window13)
                                cover = PhotoImage(file=theList[index-1][5])
                                TextImage = Label(window13, image=cover).pack(side=LEFT)
                                Text1 = Text(window13, height=4, width=50)
                                Scroll.pack(side=RIGHT, fill=Y)
                                Text1.pack(side=LEFT, fill=Y)
                                Scroll.config(command=Text1.yview)
                                Text1.config(yscrollcommand=Scroll.set)
                                sInfo += 'Program Name: '+theList[index-1][0]+'\nProgram Description: '+theList[index-1][1]+'\nProgram Price: '+theList[index-1][2]+'\nProgram Rating: '+theList[index-1][3]+'\nUser Reviews:'+'\n'+theList[index-1][4]
                                Text1.insert(END, sInfo)
                                var6 = IntVar()
                                text2 = Label(window13, text='Would you like to purchase this show!').pack()
                                Radiobutton(window13, text='Yes', padx=20, variable=var6, value=1).pack()
                                Radiobutton(window13, text='No', padx = 20, variable=var6, value=2).pack()
                                button = Button(window13, text='Continue', fg='white', bg='green', command = lambda: buy2(theList[index-1][0], theList[index-1][2])).pack()
                                text3 = Label(window13, text='Would you like to view more information?\n If so then press the Info button').pack()
                                def openurl():
                                    webbrowser.open(theList[index-1][6])
                                button2 = Button(window13, text='Info', fg='white', bg='orange', command = openurl).pack()
                                mainloop()
                        except ValueError:
                            print('Error, Please enter one of the numbers listed')
                    #Append the information of each tv show in a list
                    theList = []
                    for row in tvShows[1:]:
                        theList.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
                    #sort the list of shows by ratings using bubblesort
                    exhanges = True
                    #compares a value to the next value in the list. Then goes back to the start to repeat process.
                    while exhanges:
                      exhanges = False
                      for element in range(len(theList)-1):
                          if theList[element][3] < theList[element+1][3]:
                              exhanges = True
                              tempV = theList[element]
                              theList[element] = theList[element+1]
                              theList[element+1] = tempV
                   #display the shows and a number beside the show so the user can choose which show they would like to purchase
                    counter = 0
                    for show in theList:
                        counter +=1
                        aShows += show[0]+' - '+str(counter)+'\n'
                    window12 = Tk()
                    #create a new window
                    window12.title('FanFavTV')
                    window12.geometry('+180+115')
                    Scroll = Scrollbar(window12)
                    Text1 = Text(window12, height=4, width=50)
                    Scroll.pack(side=RIGHT, fill=Y)
                    Text1.pack(side=LEFT, fill=Y)
                    Scroll.config(command=Text1.yview)
                    Text1.config(yscrollcommand=Scroll.set)
                    Text1.insert(END, aShows)
                    Text2 = Label(window12, text="Please enter the number beside the name of the show\nyou would like to pucrchase. Otherwise press 0 to go back.").pack()
                    entry6 = IntVar()
                    entry6 = Entry(window12)
                    entry6.pack(side='bottom')
                    button = Button(window12, text='Continue', fg='white', bg='green', command =rbShow).pack()
            window6.destroy()
            #create a new window
            window11 = Tk()
            window11.title('FanFavTV')
            window11.geometry('+650+115')
            var5 = IntVar()
            #Allow user to select between two mehtods of viewing the list shows
            Radiobutton(window11, text='View Shows in alphabetical order', padx=20, variable=var5, value=1).grid(row=0, column=0, sticky='w')
            Radiobutton(window11, text='View Shows by ratings', padx = 20, variable=var5, value=2).grid(row=1, column=0, sticky='w')
            button = Button(window11, text='Continue', fg='white', bg='green', command = order).grid(row=2, column=0)
        elif var3.get() == 3:
            window6.destroy(); menu2(auName)
    os.system('cls')
    #create a new window
    window6 = Tk()
    window6.title('FanFavTV')
    window6.geometry('+650+115')
    var3 = IntVar()
    #create radiobuttons to allow the user to select an option
    Radiobutton(window6, text='Search for a show in the database', padx=20, variable=var3, value=1).grid(row=0, column=0, sticky='w')
    Radiobutton(window6, text='View the list of all shows', padx = 20, variable=var3, value=2).grid(row=1, column=0, sticky='w')
    Radiobutton(window6, text='Return to account options', padx=20, variable=var3, value=3).grid(row=2, column=0, sticky='w')
    button6 = Button(window6, text='Continue', fg='white', bg='green', command = browseMethods).grid(row=3, column=0)
#function that allows the user to rate or review a show that he/she has pruchased
def rateReview(auName):
    shows = ''
    def options():
        os.system('cls')
        window14.destroy()
        #users who have not purchased any shows will be prohibited from rating or reviwing
        if user[auName].pShows[0] == 'none':
            print('Error, you have not purchased any shows yet so please purchase a show first!')
            menu2(auName)
        else:
            #if user chose to rate a show then run this function
            def rShow(count):
                try:
                    index = int(entry7.get())
                    if index == 0:
                        os.system('cls'); window15.destroy(); rateReview(auName)
                    elif index>count:
                        print('Error! Please enter one of the numbers displayed beside the show.')
                    else:
                        for row in tvShows:
                            def rate():
                                #the user's rating is used to calculate the new rating for the show and that new rating is stored in the csv file
                                try:
                                    rating = entry8.get()
                                    if float(rating)>0 and float(rating)<11:
                                        os.system('cls'); print('Thank you for rating the show!')
                                        for row in tvShows:
                                            if lKeys[index-1] == row[0]:
                                                row[3] = (float(row[3])+float(rating))/2
                                        with open('TVShows.csv', 'w', newline='') as csvFile:
                                            Writer = csv.writer(csvFile)
                                            for cell in tvShows:
                                                Writer.writerow(cell)
                                        window16.destroy(); rateReview(auName)
                                    else:
                                        print('Error! Please enter a rating that is in the specified range')
                                except ValueError:
                                    print('Error, Please enter a number out of 10 for the rating')
                            if lKeys[index-1] == row[0]:
                                #the user is prompted to enter a rating out of 10
                                window15.destroy()
                                window16 = Tk()
                                window16.title('FanFavTV')
                                window16.geometry('+650+115')
                                Text1 = Label(window16, text='Please enter a rating out of 10:').grid(row=0, column=0)
                                entry8 = DoubleVar()
                                entry8 = Entry(window16)
                                entry8.grid(row=0, column=1)
                                button = Button(window16, text='Continue', fg='white', bg='green', command =rate).grid(row=1, column=0)
                                mainloop()
                except ValueError:
                    print('Error, Please enter one of the numbers listed')
            #if user chose to review a show then run this function
            def revShow(count):
                try:
                    index = int(entry7.get())
                    if index == 0:
                        os.system('cls'); window15.destroy(); rateReview(auName)
                    elif index>count:
                        print('Error! Please enter one of the numbers displayed beside the show.')
                    else:
                        for row in tvShows:
                            def review():
                                #the user's review is recorded in the csv file, in the row that stores the user reviews
                                userRev = entry8.get(); os.system('cls');print('Thank you for reviewing the show!')
                                for row in tvShows:
                                    if lKeys[index-1] == row[0]:
                                        row[4] += 'User: '+auName+'\nReview: '+userRev+'\n'
                                with open('TVShows.csv', 'w', newline='') as csvFile:
                                    Writer = csv.writer(csvFile)
                                    for cell in tvShows:
                                        Writer.writerow(cell)
                                window16.destroy(); rateReview(auName)
                            if lKeys[index-1] == row[0]:
                                #the user is prompted to enter a review for the show
                                window15.destroy()
                                window16 = Tk()
                                window16.geometry('+650+115')
                                window16.title('FanFavTV')
                                Text1 = Label(window16, text='Please enter a review:').grid(row=0, column=0)
                                entry8 = StringVar()
                                entry8 = Entry(window16)
                                entry8.grid(row=0, column=1)
                                button = Button(window16, text='Continue', fg='white', bg='green', command =review).grid(row=1, column=0)
                                mainloop()
                except ValueError:
                    print('Error, Please enter one of the numbers listed')
            #create a dictionary of all he shows
            shows = dict(itertools.zip_longest(*[iter(user[auName].pShows)] * 2, fillvalue=""))
            #create a list of all the names of the shows, ie.e, create a list of keys from the dictionay of shows
            lKeys = list(shows.keys()); data = csv.reader(open('TVShows.csv')); tvShows = list(data)
            show = ''; counter = 0
            #ask the user which show they would like to rate/review
            for key in shows.keys():
                counter+=1
                show += key+' - '+str(counter)+'\n'
            window15 = Tk()
            window15.title('FanFavTV')
            window15.geometry('+180+115')
            Scroll = Scrollbar(window15)
            Text1 = Text(window15, height=4, width=50)
            Scroll.pack(side=RIGHT, fill=Y)
            Text1.pack(side=LEFT, fill=Y)
            Scroll.config(command=Text1.yview)
            Text1.config(yscrollcommand=Scroll.set)
            Text1.insert(END, show)
            #if user choses option 1 then ask him/her which show they would like to rate
            if var7.get() == 1:
                Text1 = Label(window15, text="Please enter the number beside the name of the show\nyou would like to rate. Otherwise press 0 to go back.").pack()
                entry7 = IntVar()
                entry7 = Entry(window15)
                entry7.pack()
                button = Button(window15, text='Continue', fg='white', bg='green', command = lambda: rShow(counter)).pack()
            #if user choses option 1 then ask him/her which show they would like to review
            elif var7.get() == 2:
                Text1 = Label(window15, text="Please enter the number beside the name of the show\nyou would like to review. Otherwise press 0 to go back.").pack()
                entry7 = IntVar()
                entry7 = Entry(window15)
                entry7.pack()
                button = Button(window15, text='Continue', fg='white', bg='green', command = lambda: revShow(counter)).pack()
            #if user chose option 3 then return to the account menu
            elif var7.get() == 3:
                window15.destroy()
                menu2(auName)
    #create a new window and ask the user to choose from one of the three options
    window14 = Tk()
    window14.title('FanFavTV')
    window14.geometry('+650+115')
    var7 = IntVar()
    Radiobutton(window14, text='Rate the shows you have purchased', padx=20, variable=var7, value=1).grid(row=0, column=0, sticky='w')
    Radiobutton(window14, text='Review the shows you have purchased', padx = 20, variable=var7, value=2).grid(row=1, column=0, sticky='w')
    Radiobutton(window14, text='Return to account options', padx=20, variable=var7, value=3).grid(row=2, column=0, sticky='w')
    button = Button(window14, text='Continue', fg='white', bg='green', command =options).grid(row=3, column=0)
#menu that contains the account options
def menu2(auName):
    #if user chose  option 1 then their transaction history is displaed
    def op1():
        def check4():
            window5.destroy()
            menu2(auName)
        window4.destroy()
        window5 = Tk()
        window5.title('FanFavTV')
        window5.geometry('+650+115')
        Scroll1 = Scrollbar(window5)
        Text1 = Text(window5, height=4, width=50)
        Scroll1.pack(side=RIGHT, fill=Y)
        Text1.pack(side=LEFT, fill=Y)
        Scroll1.config(command=Text1.yview)
        Text1.config(yscrollcommand=Scroll1.set)
        acInfo = user[auName].pInfo()
        Text1.insert(END, acInfo)
        button = Button(window5, text='Continue', fg='white', bg='green', command = check4).pack()
    #if user chose option 2 then the function bShows is run. This function is responisble for allowing users to purchase shows.
    def op2():
        window4.destroy()
        bShows(auName)
    #if user chose option 3 then the function rateReview is run. This function is responisble for allowing users to rate or review shows.
    def op3():
        window4.destroy()
        rateReview(auName)
    #if the user chose option 4 then they are logged out and returned to the first menu
    def op4():
        window4.destroy()
        menu()
    #create a new window and  allow the user to choose one of four options
    window4 = Tk()
    window4.title('FanFavTV')
    window4.geometry('+650+115')
    ms1 = 'Welcome user '+auName+'! Please select from the following'
    text1 = Label(window4, text=ms1).grid(row=0, column=0)
    text2 = Label(window4, text='Please enter your selection').grid(row=1, column=0, sticky='w')
    button = Button(window4, text='Display Account Information', fg='white', bg='red', command = op1, width = 33).grid(row=2, column=0, sticky='w')
    button2 = Button(window4, text='Browse TV Programs', fg='white', bg='blue', command = op2, width = 33).grid(row=3, column=0, sticky='w')
    button3 = Button(window4, text='Rate or Review TV Programs', fg='black', bg='yellow', command = op3, width = 33).grid(row=4, column=0, sticky='w')
    button4 = Button(window4, text='Log off',fg='white', bg='black', command = op4, width = 33).grid(row=5, column=0, sticky='w')
    #speacial button is there to allow the user to clear the screen
    def cS():
        os.system('cls')
    specialButton = Button(window4, text='Please use this button to clear the console', fg='black', bg='pink', command = cS, width = 33).grid(row=6, column=0, sticky='w')
#this function contains the first menu
def menu():
    def firstmenuOptions():
        #the Accounts.csv file is opened to see if there is an account with the same username and password as entered by the user
        #if there is a match then the program proceeds to the second menu. Otherwise the program returns o the first menu.
        def signIn():
            with open('Accounts.csv', 'r') as csvFile:
                readCSV = csv.DictReader(csvFile); checker1 = False; checker2 = False
                for row in readCSV:
                    if entry2.get() == row['Account Username']:
                        if entry3.get() == row['Account Password']:
                            checker2 = True
                            menu2(entry2.get())
                            window2.destroy()
                        checker1 = True
            if checker1 == False or checker2 == False:
                window2.destroy(); print("Error! Account username or password can't be found in the database"); menu()
                #if user chose option 1 than he/she is prompted to log in
        if var1.get() == 1:
            os.system('cls')
            window1.destroy()
            window2 = Tk()
            window2.title('FanFavTV')
            window2.geometry('+650+115')
            text1 = Label(window2, text='Please enter your username').grid(row=0, column=0, sticky='w')
            text2 = Label(window2, text='Please enter your password').grid(row=1, column=0, sticky='w')
            entry2 = StringVar()
            entry2 = Entry(window2)
            entry2.grid(row=0, column=1)
            entry3 = StringVar()
            entry3 = Entry(window2)
            entry3.grid(row=1, column=1)
            button = Button(text='Continue', fg='white', bg='green', command=signIn).grid(row=2, column=0)
        #if the user chose option 2 then the account function is run. This function sets up a new account for the user
        elif var1.get() == 2:
            window1.destroy(); auName = account();
        #the application ends when the user chooses to end the program
        elif var1.get() == 3:
            window1.destroy(); os.system('cls'); print('Thank you for using the program!');exit()
        else:
            print('Please enter an appropriate selection')
    #create a new window
    window1 = Tk()
    window1.title('FanFavTV')
    window1.geometry('+650+115')
    logo = PhotoImage(file='peter.gif')
    text1 = Label(window1, text="------------------------------------------------------\nFanFavTV! Your place to get all your favorite shows\n------------------------------------------------------").grid(row=0, column=0)
    text2 = Label(window1, image=logo).grid(row=1, column=0)
    var1 = IntVar()
    #the user is asked to choose from one of 3 options
    Radiobutton(window1, text='Sign into your account', padx=20, variable=var1, value=1).grid(row=2, column=0, sticky='w')
    Radiobutton(window1, text='Create a new account', padx = 20, variable=var1, value=2).grid(row=3, column=0, sticky='w')
    Radiobutton(window1, text='Exit the program', padx=20, variable=var1, value=3).grid(row=4, column=0, sticky='w')
    text3 = Label(window1, text='Please enter your selection and press continue').grid(row=5, column=0, sticky='w')
    button = Button(text='Continue', fg='white', bg='green', command = firstmenuOptions).grid(row=6, column=0)
    mainloop()
#if Accounts.csv exits then read the csv info as a list and recreate the instances of the customer class for each user with an account
if os.path.exists('Accounts.csv'):
    reader = csv.reader(open('Accounts.csv'))
    accounts = list(reader)
    for row in accounts[1:]:
        user[row[0]] = Customer(row[0], row[1], row[2])
    menu()#call on the menu function
#if  Accounts.csv file does not exit in the directory then create both the  Accounts.csv file (the one that stores all the user account info)
#and the TVShows.csv (the file that contains all the TV shows info)
elif os.path.exists('Accounts.csv') == False:
    file = open('Accounts.csv', 'w', newline='')
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()#write the headers into the file
    file.close()
    file = open('TVShows.csv', 'w', newline='')
    writer = csv.DictWriter(file, fieldnames=headers2)
    writer.writeheader()#write the headers into the file
    writer.writerow({'Program Name': 'SUITS', 'Program Description': 'The show follows Mike Ross, a Lawyer at Pearson Hardman. A guy who got his job in a questionable manner.', 'Program Price': '$150.00', 'Program Rating': 8.9, 'Program Reviews': '', 'Image': 'suits.gif', 'Url': 'https://suits.wikia.com/wiki/Suits_Wiki'})
    writer.writerow({'Program Name': 'FAMILY GUY', 'Program Description': 'The adventures of an endearingly ignorant dad and his hilariously odd family of middle-class New Englanders.', 'Program Price': '$300.00', 'Program Rating': 8.5, 'Program Reviews': '', 'Image': 'family.gif', 'Url': 'http://familyguy.wikia.com/wiki/Main_Page'})
    writer.writerow({'Program Name': 'BILLIONS', 'Program Description': 'The battle between justice and the rich. Follow Bobby Axelrod as he tries to keep his empire from going down at the hands of the US Attorney, Chuck Rodes.', 'Program Price': '$50.00', 'Program Rating': 8.5, 'Program Reviews': '', 'Image': 'billions.gif', 'Url': 'https://en.wikipedia.org/wiki/Billions_(TV_series)'})
    writer.writerow({'Program Name': 'POKEMON', 'Program Description': 'Follow Ash Ketchum and his adventure to become the best pokemon trainer in the world.', 'Program Price': '$300.00', 'Program Rating': 8.4, 'Program Reviews': '', 'Image': 'pokemon.gif', 'Url': 'https://bulbapedia.bulbagarden.net/wiki/Pokémon_Wiki'})
    writer.writerow({'Program Name': 'DRAGON BALL Z', 'Program Description': 'It is one fight after the other. Yet, Goku must keep fighting to get stonger to protect the Earth from threats from across the universe.', 'Program Price': '$200', 'Program Rating': 9.0, 'Program Reviews': '', 'Image': 'dbz.gif', 'Url': 'http://dragonball.wikia.com/wiki/Main_Page'})
    writer.writerow({'Program Name': 'SOUTH PARK', 'Program Description': 'This show revolves around four boys—Stan Marsh, Kyle Broflovski, Eric Cartman, and Kenny McCormick—and their bizarre adventures in and around the titular Colorado town.', 'Program Price': '$300', 'Program Rating': 9.2, 'Program Reviews': '', 'Image': 'southpark.gif', 'Url': 'http://southpark.wikia.com/wiki/South_Park_Archives'})
    writer.writerow({'Program Name': 'ADVENTURE TIME', 'Program Description': "It's one crazy adventure after another for human boy, Finn, and his best friend, Jake, a 28-year old dog with magical powers.", 'Program Price': '$200', 'Program Rating': 8.7, 'Program Reviews': '', 'Image': 'at.gif', 'Url': 'http://adventuretime.wikia.com/wiki/Adventure_Time_with_Finn_and_Jake_Wiki'})
    writer.writerow({'Program Name': 'SPONGEBOB SQUAREPANTS', 'Program Description': 'Its another exciting day fro spongebob in the bikini bottom! Excitement awaits at every corner.', 'Program Price': '$300', 'Program Rating': 8.0, 'Program Reviews': '', 'Image': 'sponge.gif', 'Url': 'https://en.wikipedia.org/wiki/SpongeBob_SquarePants'})
    writer.writerow({'Program Name': 'SILICON VALLEY', 'Program Description': "Follow Richard Hendrick's quest to rise to the top of the tech industry at sillicon valley.", 'Program Price': '$150.00', 'Program Rating': 9.5, 'Program Reviews': '', 'Image': 'sv.gif', 'Url': 'https://en.wikipedia.org/wiki/Silicon_Valley_(TV_series)'})
    writer.writerow({'Program Name': 'PRISON BREAK', 'Program Description': 'Observe the mastermind Michael Scofield as he tries to get his wrongfully conviceted brother out of prioson and find the truth about the situation.', 'Program Price': '$150.00', 'Program Rating': 9.5, 'Program Reviews': '', 'Image': 'prisonbreak.gif', 'Url': 'http://prisonbreak.wikia.com/wiki/Main_Page'})
    file.close()
    menu()
