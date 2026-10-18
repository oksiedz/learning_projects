import random
import datetime


# #############################Quick sort code
# This function is same in both iterative and recursive
def partition_end(arr, start, stop):
	index = start - 1
	x = arr[stop]

	for j in range(start, stop):
		if arr[j] <= x:
			# increment index of smaller element
			index = index + 1
			arr[index], arr[j] = arr[j], arr[index]

	arr[index + 1], arr[stop] = arr[stop], arr[index + 1]
	return index + 1


def partition_start(arr, start, stop):
	pivot = start
	index = start + 1
	for j in range(start + 1, stop + 1):
		if arr[j] <= arr[pivot]:
			arr[index], arr[j] = arr[j], arr[index]
			index = index + 1
	arr[pivot], arr[index - 1] = arr[index - 1], arr[pivot]
	return index - 1


def partition_rand(arr, start, stop):
	rand_pivot = random.randrange(start, stop)
	arr[start], arr[rand_pivot] = arr[rand_pivot], arr[start]
	return partition_start(arr, start, stop)


# Function to do Quick sort
# arr[] --> Array to be sorted,
# start --> Starting index,
# stop --> Ending index
def quick_sort_iterative(arr, start, stop, mode):

	# Create an auxiliary stack
	size = stop - start + 1
	stack = [0] * size
	# initialize top of stack
	top = -1

	# push initial values of l and h to stack
	top = top + 1
	stack[top] = start
	top = top + 1
	stack[top] = stop

	# Keep popping from stack while is not empty
	while top >= 0:

		# Pop h and l
		stop = stack[top]
		top = top - 1
		start = stack[top]
		top = top - 1

		# Set pivot element at its correct position in
		# sorted array
		p = 0
		if mode == 1:
			p = partition_rand(arr, start, stop)
		if mode == 2:
			p = partition_start(arr, start, stop)
		if mode == 3:
			p = partition_end(arr, start, stop)

		# If there are elements on left side of pivot,
		# then push left side to stack
		if p - 1 > start:
			top = top + 1
			stack[top] = start
			top = top + 1
			stack[top] = p - 1

		# If there are elements on right side of pivot,
		# then push right side to stack
		if p + 1 < stop:
			top = top + 1
			stack[top] = p + 1
			top = top + 1
			stack[top] = stop


def quick_sort_engine(input_array, q_s_mode=1, input_type="Z", if_save=0, save_results=0, measure_point=0):
	a = []
	for i1 in range(0, len(input_array)):
		a.append(input_array[i1])
	print("Quicksort Start: " + str(input_type))
	st = datetime.datetime.now()
	quick_sort_iterative(input_array, 0, len(a) - 1, q_s_mode)
	et = datetime.datetime.now()
	print("Quicksort End: " + str(input_type))
	if if_save == 1:
		for i2 in range(len(input_array)):
			sortedArrayAsc.append(input_array[i2])
	if save_results == 1:
		resultsList.append("Q;" + str(q_s_mode) + ";"+str(input_type) + ";" + str(measure_point) + ";" + str(et - st))


# #############################Merge Sort code
def merge_sort(array):
	if len(array) > 1:
		mid = len(array)//2
		left_half = array[:mid]
		right_half = array[mid:]

		merge_sort(left_half)
		merge_sort(right_half)

		i1 = 0
		j = 0
		k = 0
		while i1 < len(left_half) and j < len(right_half):
			if left_half[i1] <= right_half[j]:
				array[k] = left_half[i1]
				i1 = i1 + 1
			else:
				array[k] = right_half[j]
				j = j + 1
			k = k + 1

		while i1 < len(left_half):
			array[k] = left_half[i1]
			i1 = i1 + 1
			k = k + 1

		while j < len(right_half):
			array[k] = right_half[j]
			j = j + 1
			k = k + 1


def merge_sort_engine(input_array, input_type="Z", if_save=0, save_results=0, measure_point=0):
	a = []
	for i1 in range(0, len(input_array)):
		a.append(input_array[i1])
	print("Start - Merge sort")
	start_time = datetime.datetime.now()
	merge_sort(a)
	end_time = datetime.datetime.now()
	print("End - Merge sort")
	if if_save == 1:
		for i2 in range(len(a)):
			sortedArrayAsc.append(a[i2])
	if save_results == 1:
		resultsList.append("M;"+str(input_type)+";"+str(measure_point)+";"+str(end_time-start_time))


# #############################HeapSort
def heapify(arr, n, iterator):
	largest = iterator
	left = 2 * iterator + 1
	right = 2 * iterator + 2

	if left < n and arr[largest] < arr[left]:
		largest = left
	if right < n and arr[largest] < arr[right]:
		largest = right
	if largest != iterator:
		arr[iterator], arr[largest] = arr[largest], arr[iterator]
		heapify(arr, n, largest)


def heap_sort(arr):
	n = len(arr)

	for i1 in range(n//2 - 1, -1, -1):
		heapify(arr, n, i1)

	for i2 in range(n-1, 0, -1):
		arr[i2], arr[0] = arr[0], arr[i2]
		heapify(arr, i2, 0)


def heap_sort_engine(input_array, input_type="Z", if_save=0, save_results=0, measure_point=0):
	a = []
	for i1 in range(0, len(input_array)):
		a.append(input_array[i1])
	print("Start - Heap sort")
	start_time = datetime.datetime.now()
	heap_sort(a)
	end_time = datetime.datetime.now()
	print("End - Heap sort")
	if if_save == 1:
		for i2 in range(len(a)):
			sortedArrayAsc.append(a[i2])
	if save_results == 1:
		resultsList.append("H;"+str(input_type)+";"+str(measure_point)+";"+str(end_time - start_time))


# ###############################Working code
resultsList = []
sortedArrayAsc = []
sortedArrayDesc = []
array_input = []
random_array = []
noOfGeneratedNumber = 100000

print("Start of random array generation")
for i in range(0, noOfGeneratedNumber):
	random_array.append(float(random.random()))
print("End of random array generation")

# print("Input array is:")
# print(random_array)

array_input = list(random_array)
quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="R", if_save=1, save_results=0, measure_point=0)
print("reverse sorted Start")
sortedArrayDesc = list(reversed(sortedArrayAsc))
print("reverse sorted End")

loop_start = 0
loop_end = 5
print("Quick sort calculation")
print("Start - random array with random pivot")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="R", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="R", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="R", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="R", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="R", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")
print("Start - random array with first pivot")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="R", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="R", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="R", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="R", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="R", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")
print("Start - random array with end pivot")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="R", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="R", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="R", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="R", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="R", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")

print("Start - sorted ASC array with random pivot")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="A", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="A", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="A", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="A", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="A", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")
print("Start - sorted ASC array with first pivot")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="A", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="A", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="A", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="A", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="A", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")
print("Start - sorted asc array with end pivot")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="A", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="A", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="A", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="A", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="A", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")

print("Start - sorted DSC array with random pivot")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="D", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="D", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="D", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="D", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=1, input_type="D", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")
print("Start - sorted DSC array with first pivot")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="D", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="D", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="D", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="D", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=2, input_type="D", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")
print("Start - sorted DSC array with end pivot")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="D", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="D", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="D", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="D", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	quick_sort_engine(input_array=array_input, q_s_mode=3, input_type="D", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")

print("Merge sort calculation")
print("Start - random array")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="R", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="R", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="R", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="R", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="R", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")

print("Start - sorted ASC array")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="A", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="A", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="A", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="A", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="A", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")

print("Start - sorted DSC array")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="D", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="D", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="D", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="D", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	merge_sort_engine(input_array=array_input, input_type="D", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")



print("Heap sort calculation")
print("Start - random array")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="R", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="R", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="R", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="R", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(random_array[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="R", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")

print("Start - sorted ASC array")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="A", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="A", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="A", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="A", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayAsc[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="A", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")

print("Start - sorted DSC array")
print("Start: First loop")
start_number = 0
end_number = 20000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="D", if_save=0, save_results=1, measure_point=1)
print("End: First loop")
print("Start: Second loop")
start_number = 20001
end_number = 40000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="D", if_save=0, save_results=1, measure_point=2)
print("End: Second loop")
print("Start: Third loop")
start_number = 40001
end_number = 60000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="D", if_save=0, save_results=1, measure_point=3)
print("End: Third loop")
print("Start: Fourth loop")
start_number = 60001
end_number = 80000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="D", if_save=0, save_results=1, measure_point=4)
print("End: Fourth loop")
print("Start: Fifth loop")
start_number = 80001
end_number = 100000
for i in range(loop_start, loop_end):
	array_input = list(sortedArrayDesc[start_number:end_number])
	heap_sort_engine(input_array=array_input, input_type="D", if_save=0, save_results=1, measure_point=5)
print("End: Fifth loop")



# print ("Sorted array is:")
# print(sortedArrayAsc)
# print(randomArray)

print("Results:")
for i in resultsList:
	print(i)
