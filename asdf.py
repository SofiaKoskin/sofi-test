from typing import Any


def append_list(value: Any, my_list: list = None):
    if not my_list:
        my_list = []
    my_list.append(value)
    return my_list


list1 = append_list(1)
list2 = append_list(2, [])
list3 = append_list(3)

print(list1)  # [1]
print(list2)  # [2]
print(list3)  # [3]
