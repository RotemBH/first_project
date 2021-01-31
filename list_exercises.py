import math


def sum_list(_list):
    list_sum = 0
    for i in _list:
        list_sum += i
    return list_sum


def multiply_list(_list):
    list_sum = 1
    for i in _list:
        list_sum *= i
    return list_sum


def get_max(_list):
    max = -math.inf
    for i in _list:
        if i > max:
            max = i
    return max


def get_min(_list):
    min = math.inf
    for i in _list:
        if i < min:
            min = i
    return min


def remove_dup(_list):
    return list(set(_list))


def get_diff(l1,l2):
    # result = []
    # for i in l1:
    #     if i not in l2:
    #         result.append(i)
    # return result
    return list(set(l1)-set(l2))


if __name__ == '__main__':
    print(sum_list([1, 6, 4]))
    print(multiply_list([1, 6, 4, 5]))
    print(
        get_max([1, 6, 4, 5, 35, 12, 43, 23, 56, 78, 54, 34, 56, 76, 34, 234, 23454, 12, 34, 55, 34, 223]))
    print(
        get_min([16, 14, 56, 78, 54, 34, 56, 76, 34, 234, 23454, 12, 34, 55, 34, 223]))
    print(remove_dup([1,2,3,3,3,3,2,3,2,3,1,1,4]))
    print(get_diff([1,2,3,6],[2,4,5]))
