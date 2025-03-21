import time


def func(x: int):
    number_list = []

    for i in range(x):
        time.sleep(1)
        number_list.append(i)
    
    return number_list


for number in func(3):
    print(number)

def func_gen(x: int):
    for i in range(x):
        time.sleep(1)
        yield i

for number in func_gen(3):
    print(number)


print(next(func_gen(3)))
