def module10():
    tuple_year=()
    for i in range(1, 2020 + 1):
        if ((i%4==0)and(i%100!=0)) or (i%400==0):
            tuple_year = tuple_year + (i, )
    print(tuple_year)