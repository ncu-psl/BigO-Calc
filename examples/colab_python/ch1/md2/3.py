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