my_list=[10,20,30,10,20,30]
my_list_out=[]
pos=0
for item in my_list:
    if item == 10:
        my_list_out.append(pos)    
    pos+=1

print(my_list_out)