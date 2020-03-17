import ast
from astpp import parseprint

s = "class D(Basic):\n\tdef foo()->D:\n\t\ti=0\n\t\td=D()\n\t\treturn d"
parseprint('\n'+s)