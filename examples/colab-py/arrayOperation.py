def f(n):
    i=0
    for i in range(n):
        i+=1
    return i

def main():
    a = [0]
    a = a + [1,f(5)]
    print(a)

if __name__ == '__main__':
    main()