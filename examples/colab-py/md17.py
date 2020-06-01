def module17():
    try:
        n1,n2 = 1,0
        r = n1/n2
        print('r =', r)    
    except:
        print('Error: Input data or expression has error!')
    else:
        print('Else: No errors!')
    finally:
        print('Finally: Finish processing!')