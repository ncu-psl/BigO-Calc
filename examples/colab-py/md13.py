def bmi(kg,m):
    bmi = kg/(m ** 2)
    return(round(bmi, 2))
def main():
    print(bmi(68,1.7))