import random
import datetime
import math

NoOfNumbers = 5
randomlist = []
#start of data generation
for i in range(0, NoOfNumbers):
    randomlist.append(random.random())
    print(randomlist[i])
print("Zakonczenie generowania ciagu liczb.")
#end of data generation

#start clearing and defining parameters
listofpairs = []
listofloserpairs = []
listofnumbers = randomlist
koniec_szukania = 0
listofwinners = []
change_the_listofnumbers = 0
round = 1
#end clearing and defining parameters

#start of loop
while (koniec_szukania == 0):
    if change_the_listofnumbers == 1:
        listofnumbers = listofwinners
        listofwinners = []
    n = int(math.ceil(len(listofnumbers) / 2))
    print ("liczba par", n)
    
    if n == 1:
        koniec_szukania = 1
        if float(listofnumbers[0]) > float(listofnumbers[1]):
            if round == 1:
                max_1 = listofnumbers[0]
            if round == 2:
                max_2 = listofnumbers[0]
            listofloserpairs.append(str(listofnumbers[0])+";"+str(listofnumbers[1]))
        else:
            if round == 1:
                max_1 = listofnumbers[1]
            if round == 2:
                max_2 = listofnumbers[1]
            listofloserpairs.append(str(listofnumbers[1])+";"+str(listofnumbers[0]))
    else:
        for i in range(0, n):
            if 2*i+1<len(listofnumbers):
                if listofnumbers[2*i] > listofnumbers[2*i+1]:
                    listofwinners.append(listofnumbers[2*i])
                    listofloserpairs.append(str(listofnumbers[2*i])+";"+str(listofnumbers[2*i+1]))
                else:
                    listofwinners.append(listofnumbers[2*i+1])
                    listofloserpairs.append(str(listofnumbers[2*i+1])+";"+str(listofnumbers[2*i]))
            else:
                listofwinners.append(str(listofnumbers[2*i]))
    change_the_listofnumbers = 1
#end of loop

#start clear the parameter to provide new players for the tournament
listofnumbers = []
#end clear the parameter to provide new players for the tournament

#start creation of new players
for i in range(0, len(listofloserpairs)):
    pairforcomparison = listofloserpairs[i].split(";")
    if float(pairforcomparison[0]) == float(max_1):
        listofnumbers.append(pairforcomparison[1])


####start of second tournament for the losers with the winner
listofpairs = []
listofloserpairs = []
koniec_szukania = 0
listofwinners = []
change_the_listofnumbers = 0
round = 2
#start of loop
while (koniec_szukania == 0):
    if change_the_listofnumbers == 1:
        listofnumbers = listofwinners
        listofwinners = []
    n = int(math.ceil(len(listofnumbers) / 2))
    print ("liczba par", n)
    
    if n == 1:
        koniec_szukania = 1
        if float(listofnumbers[0]) > float(listofnumbers[1]):
            if round == 1:
                max_1 = listofnumbers[0]
            if round == 2:
                max_2 = listofnumbers[0]
            listofloserpairs.append(str(listofnumbers[0])+";"+str(listofnumbers[1]))
        else:
            if round == 1:
                max_1 = listofnumbers[1]
            if round == 2:
                max_2 = listofnumbers[1]
            listofloserpairs.append(str(listofnumbers[1])+";"+str(listofnumbers[0]))
    else:
        for i in range(0, n):
            if 2*i+1<len(listofnumbers):
                if listofnumbers[2*i] > listofnumbers[2*i+1]:
                    listofwinners.append(listofnumbers[2*i])
                    listofloserpairs.append(str(listofnumbers[2*i])+";"+str(listofnumbers[2*i+1]))
                else:
                    listofwinners.append(listofnumbers[2*i+1])
                    listofloserpairs.append(str(listofnumbers[2*i+1])+";"+str(listofnumbers[2*i]))
            else:
                listofwinners.append(str(listofnumbers[2*i]))
    change_the_listofnumbers = 1
#end of loop


print("Maksymalna liczba to:", max_1)
print("Druga maksymalna liczba to:", max_2)



#def tournament()