import random
import datetime
import math

NoOfNumbers = 7000000

randomlist = []
print("Rozpoczecie generowania ciagu liczb.")
for i in range(0, NoOfNumbers):
    randomlist.append(random.random())
print("Zakonczenie generowania ciagu liczb.")
listofresults = []

#wyszukanie najwyższych wartości podwójnym przeszukaniem
def double_search(startnumber, endnumber):
    #print("Podwojne przeszukanie wszystkich elementow")
    max_1 = 0
    max_2 = 0
    listofnumbers = randomlist[startnumber:endnumber]
    starttime = datetime.datetime.now()
    for i in range(0, len(listofnumbers)):
        if listofnumbers[i] > max_1:
            max_1 = listofnumbers[i]
    for i in range(0, len(listofnumbers)):
        if (listofnumbers[i] > max_2 and listofnumbers[i] < max_1):
            max_2 = listofnumbers[i]
    endtime = datetime.datetime.now()
    #print("Maksymalna liczba jest rowna: ", max_1, ", druga co do wielkosci jest rowna: ", max_2, ", czas wyszukiwania wynosi: ", endtime - starttime)
    listofresults.append("Podwójne"+str(max_1)+";"+str(max_2)+";"+str(endtime-starttime))



#wyszukanie najwyższych wartości pojedynczym przeszukaniem
def single_search(startnumber, endnumber):
    #print("Pojedyncze przeszukanie wszystkich elementow")
    max_1 = 0
    max_2 = 0
    listofnumbers = randomlist[startnumber:endnumber]
    starttime = datetime.datetime.now()
    for i in range(0, len(listofnumbers)):
        if listofnumbers[i] > max_2 and listofnumbers[i] < max_1:
            max_2 = listofnumbers[i]
        if listofnumbers[i] > max_2 and listofnumbers[i] > max_1:
            max_2 = max_1
            max_1 = listofnumbers[i]
    endtime = datetime.datetime.now()
    #print("Maksymalna liczba jest rowna: ", max_1, ", druga co do wielkosci jest rowna: ", max_2, ", czas wyszukiwania wynosi: ", endtime - starttime)
    listofresults.append("Pojedyncze"+str(max_1)+";"+str(max_2)+";"+str(endtime-starttime))

#wyszukanie najwyższych wartości metodą turniejową
def tournament_search(startnumber, endnumber):
    #print("Przeszukanie wszystkich elementow metodą turniejową")
    #start clearing and defining parameters
    listofloserpairs = []
    listofnumbers = randomlist[startnumber:endnumber]
    koniec_szukania = 0
    listofwinners = []
    change_the_listofnumbers = 0
    round = 1
    #end clearing and defining parameters
    starttime = datetime.datetime.now()
    #start of loop
    while (koniec_szukania == 0):
        if change_the_listofnumbers == 1:
            listofnumbers = listofwinners
            listofwinners = []
        n = int(math.ceil(len(listofnumbers) / 2))
        
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
                    if float(listofnumbers[2*i]) > float(listofnumbers[2*i+1]):
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
    #end creation of new players

    ####start of second tournament for the losers with the winner
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
        
        if n == 1:
            koniec_szukania = 1
            if float(listofnumbers[0]) > float(listofnumbers[1]):
                if round == 1:
                    max_1 = listofnumbers[0]
                if round == 2:
                    max_2 = listofnumbers[0]
#                listofloserpairs.append(str(listofnumbers[0])+";"+str(listofnumbers[1]))
            else:
                if round == 1:
                    max_1 = listofnumbers[1]
                if round == 2:
                    max_2 = listofnumbers[1]
#                listofloserpairs.append(str(listofnumbers[1])+";"+str(listofnumbers[0]))
        else:
            for i in range(0, n):
                if 2*i+1<len(listofnumbers):
                    if listofnumbers[2*i] > listofnumbers[2*i+1]:
                        listofwinners.append(listofnumbers[2*i])
#                        listofloserpairs.append(str(listofnumbers[2*i])+";"+str(listofnumbers[2*i+1]))
                    else:
                        listofwinners.append(listofnumbers[2*i+1])
#                       listofloserpairs.append(str(listofnumbers[2*i+1])+";"+str(listofnumbers[2*i]))
                else:
                    listofwinners.append(str(listofnumbers[2*i]))
        change_the_listofnumbers = 1
    #end of loop
    endtime = datetime.datetime.now()
    #print("Maksymalna liczba jest rowna: ", max_1, ", druga co do wielkosci jest rowna: ", max_2, ", czas wyszukiwania wynosi: ", endtime - starttime)
    listofresults.append("Turniej"+str(max_1)+";"+str(max_2)+";"+str(endtime-starttime))


print("1. Double search")
for i in range(0,10):    
    double_search(1000000, 2200000)
print("2. Double search")
for i in range(0,10):
    double_search(2200000, 3400000)
print("3. Double search")
for i in range(0,10):    
    double_search(3400000, 4600000)
print("4. Double search")
for i in range(0,10):    
    double_search(4600000, 5800000)
print("5. Double search")
for i in range(0,10):
    double_search(5800000, 7000000)
print("1. single search")
for i in range(0,10):
    single_search(1000000, 2200000)
print("2. single search")
for i in range(0,10):
    single_search(2200000, 3400000)
print("3. single search")
for i in range(0,10):
    single_search(3400000, 4600000)
print("4. single search")
for i in range(0,10):
    single_search(4600000, 5800000)
print("5. single search")
for i in range(0,10):
    single_search(5800000, 7000000)
print("1. tournament search")
for i in range(0,10):
    tournament_search(1000000, 2200000)
print("2. tournament search")
for i in range(0,10):
    tournament_search(2200000, 3400000)
print("3. tournament search")
for i in range(0,10):
    tournament_search(3400000, 4600000)
print("4. tournament search")
for i in range(0,10):
    tournament_search(4600000, 5800000)
print("5. tournament search")
for i in range(0,10):
    tournament_search(5800000, 7000000)

for i in range(0, len(listofresults)):
    print(listofresults[i])
