import random
import datetime

#Arrays to be used - randomArray - array with random numbers, sortedArrayAsc - array with sorted ascending numbers, sortedArrayDesc - array with sorted ascending numbers
randomArray = []
sortedArrayAsc = []
sortedArrayDesc = []

#variables explanation:
#inputArray - parameter for input array to be sorted
#ifSave = parameter set 1 if as an output there should be saved the sorted array
#inputType = parameter defining type of input array - if it's random (R), sorted ASC (A) or sorted DESC (D)
resultsList = []

#noOfGeneratedNumber - how many items contain array of random numbers
noOfGeneratedNumber = 30000

print("Start of random array generation")
for i in range(0, noOfGeneratedNumber):
	randomArray.append(float(random.random()))
print("End of random array generation")

#print("random array:")
#for i in range(len(randomArray)):
#    print(randomArray[i])

#Selection sort
def selectionSort(inputArray, inputType = "Z",measurePoint = 0):
	#Array to be sorted
	A = []
	for i in range(0, len(inputArray)):
		A.append(inputArray[i])
	#print("Start - Selection sort")
	startTime = datetime.datetime.now()
	for i in range(len(A)):
		#Find the min value in the remaining not sorted part of array
		min_idx = i
		for j in range(i+1, len(A)):
			if A[min_idx] > A[j]:
				min_idx = j
		#Swap the minimum with the first array element
		A[i], A[min_idx] = A[min_idx], A[i]
	endTime = datetime.datetime.now()
#	print("End - Selection sort")
	resultsList.append("S;"+str(inputType)+";"+str(measurePoint)+";"+str(endTime-startTime))

#Insertion sort
def insertionSort(inputArray, inputType = "Z", measurePoint = 0):
#	print("Start - Insertion sort")
	A = []
	for i in range(0, len(inputArray)):
		A.append(inputArray[i])
	startTime = datetime.datetime.now()
	for i in range(1, len(A)):
		key = A[i]
		#Moving elements of A[0..i-1], which are greater that key, to one position ahead of their current position
		j = i-1
		while j >=0 and key < A[j] :
				A[j+1] = A[j]
				j -= 1
		A[j+1] = key
	endTime = datetime.datetime.now()
#	print("End - Insertion sort")
	resultsList.append("I;"+str(inputType)+";"+str(measurePoint)+";"+str(endTime-startTime))

def mergeSortEngine(alist):
	if len(alist)>1:
		mid = len(alist)//2
		lefthalf = alist[:mid]
		righthalf = alist[mid:]

		mergeSortEngine(lefthalf)
		mergeSortEngine(righthalf)

		i=0
		j=0
		k=0
		while i < len(lefthalf) and j < len(righthalf):
			if lefthalf[i] <= righthalf[j]:
				alist[k]=lefthalf[i]
				i=i+1
			else:
				alist[k]=righthalf[j]
				j=j+1
			k=k+1

		while i < len(lefthalf):
			alist[k]=lefthalf[i]
			i=i+1
			k=k+1

		while j < len(righthalf):
			alist[k]=righthalf[j]
			j=j+1
			k=k+1

def mergeSort(inputArray, inputType = "Z", ifSave = 0, saveResults = 0, measurePoint = 0):
	A = []
	for i in range(0, len(inputArray)):
		A.append(inputArray[i])
	#print("Start - Merge sort")
	startTime = datetime.datetime.now()
	mergeSortEngine(A)
	endTime = datetime.datetime.now()
	#print("End - Merge sort")
	if (ifSave == 1):
		for i in range(len(A)):
			sortedArrayAsc.append(A[i])
	if (saveResults == 1):
		resultsList.append("M;"+str(inputType)+";"+str(measurePoint)+";"+str(endTime-startTime))


##Section used to determine times and produce sorted array ASC and DESC
#print("Start - random sorting")
#selectionSort(randomArray, "R")
#insertionSort(randomArray, "R")
print("Start - generation of sorted array ASC")
mergeSort(randomArray, "R", 1, 0, 0)
#print("End - random sorting")
print("End - generation of sorted array ASC")

###Section reversing sorted array
print("Start - Sorting Desc")
reverseStart = datetime.datetime.now()
#for i in range(0, len(sortedArrayAsc)):
#	sortedArrayDesc.append(list(reversed(sortedArrayAsc))[i])
sortedArrayDesc = list(reversed(sortedArrayAsc))
reverseEnd = datetime.datetime.now()
print("End - Sorting Desc, lasted: "+str(reverseEnd - reverseStart))

#print("sortowany DESC")
#print(sortedArrayDesc)
#sortedArrayDesc = list(reversed(sortedArrayAsc))

#print("Start - sortedASC sorting")
#selectionSort(sortedArrayAsc, "A")
#insertionSort(sortedArrayAsc, "A")
#mergeSort(sortedArrayAsc, "A", 0)
#print("End - sortedASC sorting")
#print("Start - sortedDESC sorting")
#selectionSort(sortedArrayDesc, "D")
#insertionSort(sortedArrayDesc, "D")
#mergeSort(sortedArrayDesc, "D", 0)
#print("End - sortedDESC sorting")

#print("random array:")
#for i in range(0, len(randomArray)):
#	print(randomArray[i])

#print("sorted ASC array:")
#for i in range(0, len(sortedArrayAsc)):
#	print(sortedArrayAsc[i])

#print("sorted DESC array:")
#for i in range(0, len(sortedArrayDesc)):
#	print(sortedArrayDesc[i])

##Section of calculations of times:
loopStart = 0
loopEnd = 5
startNumber = 0
endNumber = 6000
print("Start: First loop")
print("Start - random array")
for i in range(loopStart,loopEnd):
	selectionSort(randomArray[startNumber:endNumber], "R", 1)
for i in range(loopStart,loopEnd):
	insertionSort(randomArray[startNumber:endNumber], "R", 1)
for i in range(loopStart,loopEnd):
	mergeSort(randomArray[startNumber:endNumber], "R", 0, 1, 1)
print("End - random array")
print("Start - ASC array")
for i in range(loopStart,loopEnd):
	selectionSort(sortedArrayAsc[startNumber:endNumber], "A", 1)
for i in range(loopStart,loopEnd):
	insertionSort(sortedArrayAsc[startNumber:endNumber], "A", 1)
for i in range(loopStart,loopEnd):
	mergeSort(sortedArrayAsc[startNumber:endNumber], "A", 0, 1, 1)
print("End - ASC array")
print("Start - DESC array")
for i in range(loopStart,loopEnd):
	selectionSort(sortedArrayDesc[startNumber:endNumber], "D", 1)
for i in range(loopStart,loopEnd):
	insertionSort(sortedArrayDesc[startNumber:endNumber], "D", 1)
for i in range(loopStart,loopEnd):
	mergeSort(sortedArrayDesc[startNumber:endNumber], "D", 0, 1, 1)
print("End - DESC array")
print("End: First loop")
startNumber = 6001
endNumber = 12000
print("Start: Second loop")
for i in range(loopStart,loopEnd):
	selectionSort(randomArray[startNumber:endNumber], "R", 2)
for i in range(loopStart,loopEnd):
	insertionSort(randomArray[startNumber:endNumber], "R", 2)
for i in range(loopStart,loopEnd):
	mergeSort(randomArray[startNumber:endNumber], "R", 0, 1, 2)
print("End - random array")
print("Start - ASC array")
for i in range(loopStart,loopEnd):
	selectionSort(sortedArrayAsc[startNumber:endNumber], "A", 2)
for i in range(loopStart,loopEnd):
	insertionSort(sortedArrayAsc[startNumber:endNumber], "A", 2)
for i in range(loopStart,loopEnd):
	mergeSort(sortedArrayAsc[startNumber:endNumber], "A", 0, 1, 2)
print("End - ASC array")
print("Start - DESC array")
for i in range(loopStart,loopEnd):
	selectionSort(sortedArrayDesc[startNumber:endNumber], "D", 2)
for i in range(loopStart,loopEnd):
	insertionSort(sortedArrayDesc[startNumber:endNumber], "D", 2)
for i in range(loopStart,loopEnd):
	mergeSort(sortedArrayDesc[startNumber:endNumber], "D", 0, 1, 2)
print("End - DESC array")
print("End: Second loop")
startNumber = 12001
endNumber = 18000
print("Start: Third loop")
print("Start - random array")
for i in range(loopStart,loopEnd):
	selectionSort(randomArray[startNumber:endNumber], "R", 3)
for i in range(loopStart,loopEnd):
	insertionSort(randomArray[startNumber:endNumber], "R", 3)
for i in range(loopStart,loopEnd):
	mergeSort(randomArray[startNumber:endNumber], "R", 0, 1, 3)
print("End - random array")
print("Start - ASC array")
for i in range(loopStart,loopEnd):
	selectionSort(sortedArrayAsc[startNumber:endNumber], "A", 3)
for i in range(loopStart,loopEnd):
	insertionSort(sortedArrayAsc[startNumber:endNumber], "A", 3)
for i in range(loopStart,loopEnd):
	mergeSort(sortedArrayAsc[startNumber:endNumber], "A", 0, 1, 3)
print("End - ASC array")
print("Start - DESC array")
for i in range(loopStart,loopEnd):
	selectionSort(sortedArrayDesc[startNumber:endNumber], "D", 3)
for i in range(loopStart,loopEnd):
	insertionSort(sortedArrayDesc[startNumber:endNumber], "D", 3)
for i in range(loopStart,loopEnd):
	mergeSort(sortedArrayDesc[startNumber:endNumber], "D", 0, 1, 3)
print("End - DESC array")
print("End: Third loop")
startNumber = 18001
endNumber = 24000
print("Start: Fourth loop")
print("Start - random array")
for i in range(loopStart,loopEnd):
	selectionSort(randomArray[startNumber:endNumber], "R", 4)
for i in range(loopStart,loopEnd):
	insertionSort(randomArray[startNumber:endNumber], "R", 4)
for i in range(loopStart,loopEnd):
	mergeSort(randomArray[startNumber:endNumber], "R", 0, 1, 4)
print("End - random array")
print("Start - ASC array")
for i in range(loopStart,loopEnd):
	selectionSort(sortedArrayAsc[startNumber:endNumber], "A", 4)
for i in range(loopStart,loopEnd):
	insertionSort(sortedArrayAsc[startNumber:endNumber], "A", 4)
for i in range(loopStart,loopEnd):
	mergeSort(sortedArrayAsc[startNumber:endNumber], "A", 0, 1, 4)
print("End - ASC array")
print("Start - DESC array")
for i in range(loopStart,loopEnd):
	selectionSort(sortedArrayDesc[startNumber:endNumber], "D", 4)
for i in range(loopStart,loopEnd):
	insertionSort(sortedArrayDesc[startNumber:endNumber], "D", 4)
for i in range(loopStart,loopEnd):
	mergeSort(sortedArrayDesc[startNumber:endNumber], "D", 0, 1, 4)
print("End - DESC array")
print("End: Fourth loop")
startNumber = 24001
endNumber = 30000
print("Start: Fifth loop")
print("Start - random array")
for i in range(loopStart,loopEnd):
	selectionSort(randomArray[startNumber:endNumber], "R", 5)
for i in range(loopStart,loopEnd):
	insertionSort(randomArray[startNumber:endNumber], "R", 5)
for i in range(loopStart,loopEnd):
	mergeSort(randomArray[startNumber:endNumber], "R", 0, 1, 5)
print("End - random array")
print("Start - ASC array")
for i in range(loopStart,loopEnd):
	selectionSort(sortedArrayAsc[startNumber:endNumber], "A", 5)
for i in range(loopStart,loopEnd):
	insertionSort(sortedArrayAsc[startNumber:endNumber], "A", 5)
for i in range(loopStart,loopEnd):
	mergeSort(sortedArrayAsc[startNumber:endNumber], "A", 0, 1, 5)
print("End - ASC array")
print("Start - DESC array")
for i in range(loopStart,loopEnd):
	selectionSort(sortedArrayDesc[startNumber:endNumber], "D", 5)
for i in range(loopStart,loopEnd):
	insertionSort(sortedArrayDesc[startNumber:endNumber], "D", 5)
for i in range(loopStart,loopEnd):
	mergeSort(sortedArrayDesc[startNumber:endNumber], "D", 0, 1, 5)
print("End - DESC array")
print("End: Fifth loop")

print("time results")
for i in range(0, len(resultsList)):
	print(resultsList[i])

##to write down results of general tests
with open('testing results.txt', 'w') as f:
    for item in resultsList:
        f.write("%s\n" % item)




##Section of comparison of performance between Insertion sort and merge sort on sorted array enriched with some random numbers

noOfGeneratedNumber = 100000
randomArray = []
sortedArrayAsc = []

print("Start of random array generation")
for i in range(0, noOfGeneratedNumber):
    randomArray.append(float(random.random()))
print("End of random array generation")

print("Start - generation of sorted array ASC")
mergeSort(randomArray, "R", 1, 0, 0)
#print("End - random sorting")
print("End - generation of sorted array ASC")


resultsList = []
sortedArray1 = sortedArrayAsc[0:100000]

print("Start - append the first array")
for i in range(0, 10000):
    sortedArray1.append(float(random.random()))
print("End - append the first array")

print("Time measures")
resultsList.append("Results of performance comparison")
sortedLength = noOfGeneratedNumber
step = 10
print("Start - first loops")
for i in (0,1,2,3,4,5,6,7,8,9,10):
	resultsList.append("array 10 000 with additional " + str(i)+" random numbers at the end of array")
	print(sortedLength+i*step);
	insertionSort(sortedArray1[0:sortedLength+i*step]);
	mergeSort(sortedArray1[0:sortedLength+i*step],saveResults = 1);
print("End - first loops")

##results of simulations of performance of insertion sort and merge sort
with open('testing results2.txt', 'w') as f:
    for item in resultsList:
        f.write("%s\n" % item)

for i in range(0, len(resultsList)):
	print(resultsList[i])