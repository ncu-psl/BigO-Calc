def module2_1():
    a = 2**0.5
    print('%.6f' % (a))

def module2_2():
    top = 10
    bottom = 20
    height = 8
    area = (top+bottom)*height/2
    print('Area of a Trapezoid:%.1f' % area)

def module2_3():
    prime_number = [1]
    for i in range(2,1001):
        prime_flag = True
        for prime in prime_number:
            if prime != 1:
                if i%prime == 0:
                    prime_flag = False
        if prime_flag == True:
            prime_number.append(i)
    print(prime_number)