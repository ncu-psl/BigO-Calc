def module8():
    total=0
    i=0
    while total < 1000000:
        total += 10000
        total = total*(1+0.05/12)
        i+=1
    print(i)