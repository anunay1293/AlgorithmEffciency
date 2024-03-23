
import multiprocessing
import time

################### Bubble Sort ########################

def bubble_sort(arr):
    for i in range(len(arr)):

        # keep track if elements have been swapped
        swapped_elements = False

        # shortens the length of the unsorted part of the array each loop
        unsorted_arr = len(arr) - i - 1
        for j in range(0, unsorted_arr):

            # Compare neighboring elements, and swaps if needed
            if arr[j] > arr[j + 1]:
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp

                swapped_elements = True

        # Break is array is already sorted. Otherwise, continues comparing
        if not swapped_elements:
            break

    return arr


######################################################

################### Merge Sort ########################
def merge_sort(arr):
    if len(arr) > 1:
        # Finding the middle of the array
        mid = len(arr) // 2

        # Dividing the array into left and right sections
        L = arr[:mid]
        R = arr[mid:]

        # Sorting each half of the array
        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        # Copying elements over
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking for any elements remaining
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

        return arr


######################################################
    
################### Heap Sort ########################
def build_max_heap(arr, n, i):
    root = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[root]:
        root = left

    if right < n and arr[right] > arr[root]:
        root = right

    if root != i:
        arr[i], arr[root] = arr[root], arr[i]
        build_max_heap(arr, n, root)


def heap_sort(arr):
    arr_len = len(arr)
    for i in range(arr_len // 2 - 1, -1, -1):
        build_max_heap(arr, arr_len, i)

    for i in range(arr_len - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        build_max_heap(arr, i, 0)

    return arr


######################################################

################### Quick Sort #######################
def new_partition(arr, low, high):
    pi = low
    while low <= high:
        if arr[low] <= arr[pi]:
            low += 1
        else:
            arr[low], arr[high] = arr[high], arr[low]
            high -= 1
    arr[pi], arr[low-1] = arr[low-1], arr[pi]
    return low-1


def run_quick_sort(arr, low, high):
    if low < high:
        pi = new_partition(arr, low, high)
        run_quick_sort(arr, low,
                       pi - 1)  # sorting everything to the left of the
        # pivot
        run_quick_sort(arr, pi + 1,
                       high)  # sorting everything to the right of the
        # pivot

def partition(arr, low, high):
    i = low - 1
    pivot = arr[high]

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def run_quick_sort1(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        run_quick_sort(arr, low,
                       pi - 1)  # sorting everything to the left of the
        # pivot
        run_quick_sort(arr, pi + 1,
                       high)  # sorting everything to the right of the
        # pivot

def quick_sort(arr):
    run_quick_sort(arr, 0, len(arr) - 1)
    return arr

######################################################

################### Counting Sort ####################   
def counting_sort(arr):
    # find max value
    max_val = max(arr)
    min_val = min(arr)

    temp_size = (max_val - min_val) + 1

    # initalize a count_arr to the size of the input arr + 1
    count_arr = [0] * (temp_size)

    # Set count_arr[i] to equal the number of elements equal to i
    for i in range(len(arr)):
        count_arr[arr[i] - min_val] = (count_arr[arr[i] - min_val] + 1)

    temp_arr = [0] * (temp_size)

    # Set temp_arr[i] to equal the number of elements less than or equal to i
    for i in range(1, temp_size):
        temp_arr[i] = (count_arr[i] + count_arr[i - 1])

    # create sorted array
    sorted_arr = []

    # iterate over count array
    for i in range(min_val, max_val + 1):
        # check if value is in array
        if count_arr[i - min_val] > 0:
            # continue appending if element appears more than once
            while count_arr[i - min_val] > 0:
                sorted_arr.append(i)
                count_arr[i - min_val] -= 1

    return sorted_arr


######################################################

################### Radix Sort #######################

def counting_sort_helps_radix(arr, exp):
    arr_len = len(arr)
    # declare the output array
    output = [0] * (arr_len)
    # initialize array having 0
    count = [0] * (10)

    # find min_val
    min_val = min(arr)

    # Store count of occurrences in count[]
    for i in range(0, arr_len):
        index = arr[i] // exp
        modulo = index % 10
        count[modulo] += 1

    # Get actual position of current digit
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array
    i = arr_len - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    # Get the sorted array
    i = 0
    for i in range(0, len(arr)):
        arr[i] = output[i]

    return arr


def radix_sort(arr):
    # Find the maximum number
    max_num = max(arr)
    # determine if there are negative numbers in unsorted array
    min_num = min(arr)

    exp = 1

    # create sorted arr array
    sorted_arr = []

    # if there are negative values, split the array into positive and negative
    if min_num < 0:
        pos_unsorted_arr = []
        neg_unsorted_arr = []
        sorted_pos_arr = []
        sorted_neg_arr = []

        for i in arr:
            if i < 0:
                neg_unsorted_arr.append(i)
            else:
                pos_unsorted_arr.append(i)

        # convert negative elements to positive
        for i in range(len(neg_unsorted_arr)):
            neg_unsorted_arr[i] = neg_unsorted_arr[i] * (-1)

        # Find max value of the negative unsorted array
        max_num_negative = max(neg_unsorted_arr)

        # sort negative elements
        while max_num_negative // exp >= 1:
            sorted_neg_arr = counting_sort_helps_radix(neg_unsorted_arr, exp)
            exp *= 10

        # Reverse the array and convert it back to negative
        sorted_neg_arr.reverse()

        for i in range(len(sorted_neg_arr)):
            sorted_neg_arr[i] = sorted_neg_arr[i] * (-1)

        # Reset the max number and exp for the unsorted positive array
        max_num = max(arr)
        exp = 1

        # sort positive array
        while max_num // exp >= 1:
            sorted_pos_arr = counting_sort_helps_radix(pos_unsorted_arr, exp)
            exp *= 10

        # concatenate the negative and positive sorted arrays
        sorted_arr = sorted_neg_arr + sorted_pos_arr

    else:
        while max_num // exp >= 1:
            sorted_arr = counting_sort_helps_radix(arr, exp)
            exp *= 10

    return sorted_arr


######################################################

################### Insertion Sort ######################
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


######################################################

################### Bucket Sort ######################
def bucket_sort(arr):
    temp_arr = []

    # create sorted array and initialize to 0
    sorted_arr = [0] * (len(arr))

    # find max value to determine bucket size
    max_value = max(arr)
    size = max_value / len(arr)

    # create buckets
    for i in range(len(arr)):
        temp_arr.append([])

    # insert elements into buckets
    for i in range(len(arr)):
        if arr[i] == min(arr):
            idx = 0
            temp_arr[idx].append(arr[i])
        else:
            idx = int(arr[i] / size)
            if idx != len(arr):
                temp_arr[idx].append(arr[i])
            else:
                temp_arr[len(arr) - 1].append(arr[i])

    # Sort buckets with insertion sort
    for i in range(len(arr)):
        temp_arr[i] = insertion_sort(temp_arr[i])

    # concatenate each element from each bucket in order
    idx = 0
    for i in range(len(arr)):
        for j in range(len(temp_arr[i])):
            temp = temp_arr[i][j]
            sorted_arr[idx] = temp
            idx += 1

    return sorted_arr


######################################################

################### Get Median Algorithm ########################
def get_median(arr):
    # formula for finding the median
    median_formula = len(arr) // 2
    median = 0 # clear median value
    # back up to ensure list is sorted
    sorted_arr = quick_sort(arr)

    if len(arr) % 2 == 0:
        median = (sorted_arr[median_formula] + sorted_arr[median_formula - 1]) // 2
    else:
        median = sorted_arr[median_formula]

    return median

######################################################

################### QuickSelect Method Algorithm ########################
def quick_select(arr, low, high, k):
    # base case for recursion
    if len(arr) == 1:
        return arr[0]

    kth_smallest = 0
    # finding the median
    median_formula = len(arr) // 2
    median = 0
    side = None

    if high - low <= k < 0:
        print("Error: Index out of bound. Please try again.")

    else:
        if low <= high:
            # select pivot point
            pivot = partition(arr, low, high)

            # return if pivot is equal to k, return pivot element
            if pivot == k:
                return arr[pivot]
            elif k < pivot:
                kth_smallest = quick_select(arr, low, pivot - 1, k)
            else:
                kth_smallest = quick_select(arr, pivot + 1, high, k)

    # extracting only the kth-smallest element
    if isinstance(kth_smallest, tuple):
        if len(kth_smallest) > 1:
            kth_smallest = kth_smallest[0]

    # get median
    median = get_median(arr)

    return kth_smallest, median

######################################################
        
def get_time(algo, arr):
    start_time = time.time()
    algo(arr)
    end_time = time.time()
    return end_time - start_time


def run_algorithm(algoes, arr):
    pool = multiprocessing.Pool(processes=len(algoes))
    time_results = []

    for algo in algoes:
        result = pool.apply_async(get_time, (algo, arr.copy()))
        time_results.append(result)

    times = [float(result.get()) for result in time_results]
    return times

# Define all algorithms list
all_algorithms = [
    {'name': 'Bubble Sort', 'function': bubble_sort},
    {'name': 'Quick Sort', 'function': quick_sort},
    {'name': 'Heap Sort', 'function': heap_sort},
    {'name': 'Counting Sort', 'function': counting_sort},
    {'name': 'Radix Sort', 'function': radix_sort},
    {'name': 'Insertion Sort', 'function': insertion_sort},
    {'name': 'Bucket Sort', 'function': bucket_sort},
    {'name': 'Quick Select Sort', 'function': quick_select},
]

def main(arr, k=None):
    try:
        # Ensure arr is a list of integers
        #arr = [int(item) for item in arr.split()]  

        print("Sorted Array [EXPECTED OUTPUT]", quick_sort(arr.copy()))
        print("Sorted Array using Counting Sort: ", counting_sort(arr.copy()))
        print("Sorted Array using Quick Sort: ", quick_sort(arr.copy()))
        print("Sorted Array using Bucket Sort: ", bucket_sort(arr.copy()))
        print("Sorted Array using Heap Sort: ", heap_sort(arr.copy()))
        print("Sorted Array using Radix Sort: ", radix_sort(arr.copy()))
        #print("Sorted Array using Merge Sort: ", merge_sort(arr.copy()))
        print("Sorted Array using Bubble Sort: ", bubble_sort(arr.copy()))

        # Running QuickSelect Algorithm 
        if k is not None:
            kth_element = quick_select(arr.copy(), 0, len(arr) - 1, k - 1)  # Adjust k to zero-based index
            print(f"{k}-th smallest element: {kth_element}")

        # List of algorithms to run for timing comparison
        arr_algorithms = [bubble_sort, quick_sort, heap_sort, counting_sort, radix_sort, insertion_sort, bucket_sort]
        exe_times = run_algorithm(arr_algorithms, arr.copy())

        for algorithm, time_consume in zip(arr_algorithms, exe_times):
            print(f"{algorithm.__name__} Time: {time_consume:.6f} seconds")
            
    except ValueError:
        print("Please enter only integers separated by spaces.")

# Main check to run the GUI app
if __name__ == "__main__":
    main()