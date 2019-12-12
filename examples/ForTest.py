import ast
from astpp import parseprint
# s = 'def f(a: \'annotation\', b=1, c=2, *d, e, f=3, **g) -> \'return annotation\':\
# \n\tpass'
# expr_ast = ast.parse(s)
# def f(a:'annotation', b=1, c=2, *d, e, f=3, **g) -> return 'annotation':
    
#     pass
s = "i = -2"
parseprint(s)
