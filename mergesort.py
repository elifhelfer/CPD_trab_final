def merge(left_array:list, right_array:list, index:int) -> list:
    merged_arr = []
    i = 0
    j = 0
    while i < len(left_array) and j < len(right_array):
        if left_array[i][index] <= right_array[j][index]:
            merged_arr.append(left_array[i])
            i+=1
        else:
            merged_arr.append(right_array[j])
            j+=1
        
    while i < len(left_array):
        merged_arr.append(left_array[i])
        i+=1

    while j < len(right_array):
        merged_arr.append(right_array[j])
        j+=1
            
    return merged_arr

def mergesort(array:list, index:int) -> list:
    if len(array)>1:
        left_array = array[:len(array)//2]
        right_array = array[len(array)//2:]

        left_sorted = mergesort(left_array, index)
        right_sorted = mergesort(right_array, index)

        return merge(left_sorted,right_sorted, index)
    return array

def dec_mergesort(array:list, index:int) -> list:
    return (mergesort(array,index)[::-1])

if __name__ == '__main__':
    # example
    arr = [
    [12, 34, 56],
    [78, 90, 3],
    [34, 56, 78],
    [90, 12, 34],
    [56, 78, 90],
    [12, 34, 56],
    [78, 90, 12],
    [34, 56, 78],
    [90, 12, 34],
    [56, 78, 90]
]

    print(dec_mergesort(arr, 2))
    print(dec_mergesort(arr, 1))
    print(dec_mergesort(arr, 0))

