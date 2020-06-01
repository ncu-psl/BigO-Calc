import re

def infixStringToList(infixString:str):
    infixList = []
    tmp = ''
    re_VarOrNum = re.compile(r'\w')
    for char in infixString:
        if char == ' ':
            if(tmp != ''):
                infixList.append(tmp)
                tmp = ''
            continue
        if re_VarOrNum.match(char):
            tmp = tmp + char
        else:
            if tmp != '':
                infixList.append(tmp)
            tmp = char
            infixList.append(tmp)
            tmp = ''

    if tmp!='':
        infixList.append(tmp)
    return infixList
##########
def priority(op:str):
    return 0 if op in '' else 1 if op in "+-" else 2 if op in "*/" else 0

def toPostfix(infixString:str):
    infix = infixStringToList(infixString)
    stack = []
    output = []
    re_VarOrNum = re.compile(r'\w')
    i = 1
    for expr in infix:
        if expr == '(':     #(
            stack.append('(')
        elif re_VarOrNum.match(expr): #var or num
            output.append(expr)
        elif expr in '+-*/': #op
            if stack == []:
                stack.append(expr)
            else:
                reverse_stack = stack[::-1]
                for i, op in enumerate(reverse_stack):
                    if op == '(':
                        stack.append(expr)
                        break
                    elif priority(expr) <= priority(op):
                        output.append(stack.pop())
                        if len(reverse_stack)-1 == i:
                            stack.append(expr)
                    else:
                        stack.append(expr)

        elif expr == ')':
            while stack[-1]!='(':
                output.append(stack.pop())
            stack.pop()
    
    output.extend(stack[::-1])
    return output



def getUpateRate(name: str,infixString:str)->str:
    '''
    input : infix , type:str
    output: upateRate , type:str 
    '''
    try:
        infix = infixStringToList(infixString)
        postfix = toPostfix(infix)
        rate:str=''
        stack = []
        re_VarOrNum = re.compile(r'\w')
        for expr in postfix:
            if re_VarOrNum.match(expr):
                stack.append(expr)
            elif expr in '+-*/':
                try: 
                    if name in stack[-2:]:
                        stack.pop()
                        stack.pop()
                        stack.append(name)
                        if rate == '':
                            rate = expr
                        elif priority(rate) < priority(expr):
                            rate = expr
                    else:
                        stack.pop()
                except:
                    print('var or num less than two elements when meeting op')
    except:
        return ''
    return rate

if __name__ == '__main__':
    
    midMinusOne = '(low + high)/2-1'
    a = 'a+b'
    postfixMidMinusOne = ['low','high','+','2','/','1','-']
    output = toPostfix(midMinusOne)
    rate = getUpateRate('low', midMinusOne)
