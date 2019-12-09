import ast
str = '''
k=0
# for i in range(10):
#     k=k+10
l=0
'''

expr_ast = ast.parse(str)
print(ast.dump(expr_ast))
