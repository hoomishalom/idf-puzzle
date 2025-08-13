""" 
maker - Tom Shabtay
notation - () with a number inside means there is an further explanation to the specific line in the attached file
"""

import random
import time

def makeArr(minJmp, length):
    # initialize the array
    arr = [0 for i in range(length)]

    # "place" the 250 vase in a random place which matches the limitations
    location_250 = random.randint(0, 24) # (1)
    arr[location_250] = 250
    
    # "place" the 628 vase in a random place which matches the limitations
    location_628 = random.randint(max(12, location_250 + 1), min(length, location_250 + (628-250)//minJmp) - 1) # (2)
    arr[location_628] = 628
    
    
    # pick random volumes of vaces in [0 - location_250]
    if location_250 >= 1:
        arr[0] = random.randint(1, 250 - minJmp*location_250)
    if location_250 > 1:
        for i in range(1, location_250):
            arr[i] = random.randint(arr[i-1] + minJmp, 250 - minJmp*(location_250 - i)) # (3)

    # pick random volumes of vaces in [location_250 - location_628]
    if location_628 >= location_250 + 2:
        arr[location_250 + 1] = random.randint(250 + minJmp, 628 - minJmp*(location_628 - location_250))
    if location_628 > location_250 + 2:
        for i in range(location_250 + 2, location_628):
            arr[i] = random.randint(arr[i-1] + minJmp, 628 - minJmp*(location_628 - i)) # (3)
    
    # pick random volumes of vaces in [location_628 - 49]
    if location_628 < length:
        for i in range(location_628 + 1, length):
            arr[i] = random.randint(arr[i-1] + minJmp, 999 - minJmp*(length - i - 1)) # (3)

    return arr

def findingAlgorithmFor250(arr):
    low = 0
    high = 24 # (1)
    counter = 0 # turn counter

    # simple binary search
    while high > low:
        counter += 8 # steps to determine if the volume of the vace is >/</= compared to 250 (4)
        mid = (high + low) // 2
        
        if arr[mid] == 250:
            return [counter, mid, [f"{i}:{j}" for i,j in enumerate(arr[low:high+1])], arr] # first and second items are essential for the program, third one is for debugging purposes
        elif arr[mid] < 250:
            low = mid + 1
        else:
            high = mid - 1
    
    return [counter, mid, [f"{i}:{j}" for i,j in enumerate(arr[low:high+1])], arr] # (view line 55)

def findingAlgorithmFor628(arr, low_bound):
    low = low_bound # left most location possible for 628
    high = min(len(arr) - 1, low_bound + (628-250)//10)  # (2)
    counter = 0 # turn counter

    while high - low > 2: # (5)
        counter += 6
        mid = (high + low) // 2

        if arr[mid] >= 628:
            high = mid          # the reason there isn't a -1 is because arr[mid] can be 628 due to some of the algorithm's drawbacks
        else:
            low = mid + 1
    
    mid = (high + low) // 2
    if high - low == 1: # 2 vaces left. (5)
        counter += 6
        
        if (arr[high] == 628):
            location_628 = high
        else:
            location_628 = low

    else: # 3 vaces left, (6)
        counter += 10
        
        if (arr[mid] == 628): # this vace is 628
            location_628 = mid
        elif (arr[mid] > 628): # left vace is 628
            location_628 = mid - 1
        else: # right vace is 628
            location_628 = mid + 1
    
    
    return [counter, location_628, [f"{i}:{j}" for i,j in enumerate(arr[low:high+1])], [f"{i}:{j}" for i,j in enumerate(arr)]] # first and last items are essential for the program, last one is for debugging purposes

run = True

if run:
    max_iterations = 0
    max_250 = 0
    max_628 = 0
    max_arr = []

    start_time = time.time()

    """ 
    checks the algorithm with 1,000,000 random arrays which represent the vaces and saves: 
        max_iterations - the worst case scenario of iterations to find 250 and 628
        max_250 - the worst case scenario of iterations to find 250 only
        max_628 - the worst case scenario of iterations to find 628 only
        max_arr - first array that produces the (max_iterations)
    """
    for i in range(1_000_000):
        arr = makeArr(10, 50)
        res_250 = findingAlgorithmFor250(arr)
        res_628 = findingAlgorithmFor628(arr, res_250[1])
        
        if arr[res_628[1]] != 628:
            print(f"algorithm isnt working error at: {res_628}")

        if res_250[0] + res_628[0] > max_iterations:
            max_iterations = res_250[0] + res_628[0]
            max_arr = arr
        if res_250[0] > max_250:
            max_250 = res_250[0]
        if res_628[0] > max_628:
            max_628 = res_628[0]

    end_time = time.time()  

    print(f"time to run: {end_time - start_time}")
    print(f"max_iterations: {max_iterations}")
    print(f"max_250: {max_250}")
    print(f"max_628: {max_628}")
    print(*[f"{i}:{j}" for i,j in enumerate(max_arr)])
    