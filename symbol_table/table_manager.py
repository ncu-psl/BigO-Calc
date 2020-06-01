# ![title](https://i.imgur.com/GSGG2ps.png)
from bigo_ast.bigo_ast import FuncDeclNode, ForNode, FuncCallNode, CompilationUnitNode, IfNode, VariableNode, \
    AssignNode, ConstantNode, Operator, BasicNode, WhileNode, ArrayNode
from symbol_table.arithmetic import priority, getUpateRate
import symbol_table.arithmetic
class table_manager(object):
    '''
    使用table_list管理程式中所有scope的symbol table
    table_list中只會有當前的scope以及父scope的table
    '''
    def __init__(self):
        self.table_list = []
        self.__current_scope_number = 0 #1以上表示 table_list中有存放 table
        self.current_table:symbol_table
        
    @property
    def current_scope_number(self):
        return self.__current_scope_number
    
    def push_table(self, scope_type:str = 'other'): 
        '''
        呼叫此函式當visitor進入新的scope
        first in last out
        '''
        if scope_type == 'else':
            self.table_list[-1].scope_type = 'other'
        table = symbol_table(self.__current_scope_number, scope_type)
        
        self.table_list.append(table)
        self.current_table = table
        self.__current_scope_number+=1

    def pop_table(self):
        '''呼叫此函式當visitor離開scope'''
        if self.__current_scope_number is not 0:
            self.update_symbol_to_parent_table(self.table_list[-1].scope_type)
            self.table_list.pop()
            self.__current_scope_number -= 1
            if self.__current_scope_number is not 0:
                self.current_table = self.table_list[-1]
        else: 
            print('table list is empty')
           
    def add_symbol(self,node : BasicNode):
        symbol_name, value, rate = self.find_changed_symbol(node)
        sym = Symbol(symbol_name, value, rate)
        self.table_list[-1].update(sym)
        
    def get_symbol_rate(self, symbol_name):

        item = self.table_list[-1].table.get(symbol_name, None)
        if item != None:
            rate = item[1]
            return rate
        

    def get_symbol_value(self, symbol_name:str, recursive = False):
        '''
        往父層scope尋找是symbol 是否被重新賦值
        '''
        if recursive == False:  #尋找當前的scope查看是否有 a = a (+-*/) (number) 的pattern
            return self.current_table.get_symbol_value(symbol_name)

        above_compilation_or_funcdef = False
        for t in reversed(self.table_list):
            if above_compilation_or_funcdef == True:
                break
            if table.scope_type in ['compilation', 'funcdef']:
                above_compilation_or_funcdef = True
            if symbol_name in t.table:
                return t.get_symbol_value(symbol_name)
        return None

    def update_symbol_to_parent_table(self, scope_type = 'other'):
        above_compilation_or_funcdef = False
        for sym_table in reversed(self.table_list[:-1]):
            if len(self.current_table.table) == 0:
                return
            if above_compilation_or_funcdef == True:
                return
            if sym_table.scope_type in ['compilation', 'funcdef']:
                above_compilation_or_funcdef = True
            pop = []
            for symbol in self.current_table.table.items():
                parent_table_sym_val = sym_table.table.get(symbol[0], 'none')
                if parent_table_sym_val != 'none':
                    parent_pri = priority(parent_table_sym_val[1])
                    symbol_pri = priority(symbol[1][1])
                    tmp = Symbol(symbol[0], symbol[1][0], symbol[1][1])

                    if self.current_table.scope_type in ['if','else']:
                        if symbol_pri <= parent_pri:
                            if self.current_table.scope_type == 'else':
                                self.table_list[-2].scope_type = 'if_else'
                    pop.append(symbol[0])
                    self.table_list[-2].update(tmp)
            for sym in pop:
                self.current_table.table.pop(sym)

    def print_current_table(self):
        return self.current_table.table

    def find_changed_symbol(self, node : BasicNode):#回傳值是 (str,str)
        #不能處理 m = n++ 這類的 expression
        if type(node) == AssignNode:
            if type(node.target) == VariableNode:
                value = self.find_changed_symbol(node.value)
                rate = getUpateRate(node.target.name, value)
                return node.target.name, value, rate
            else:
                raise NotImplementedError('type(node.target) != VariableNode\n')
 
        if type(node) == VariableNode:
            return str(node.name)
        
        if type(node) == ConstantNode:
            return str(node.value)
        
        if type(node) == Operator:
            if node.op == '<<':
                return '(' + self.find_changed_symbol(node.left) + '*2**' + self.find_changed_symbol(node.right) + ')'
            elif node.op == '>>':
                return '(' + self.find_changed_symbol(node.left)+ '/(2**' + self.find_changed_symbol(node.right) + ')' + ')'
            else:
                return '(' + self.find_changed_symbol(node.left)+ node.op + self.find_changed_symbol(node.right) + ')'
        if type(node) == ArrayNode:
            return 'array'

    def getUpateRate(name: str,infixString:str)->str:
        return arithmetic.getUpateRate(name, infixString)

class symbol_table(object):
    '''
    此class的目的是為了儲存每個scope中的symbol name 以及value
    將資訊存在table中
    table中儲存identifier這個類別的物件
    '''
    def __init__(self, scope_number,  scope_type:str = 'other'):
        self.table = {}
        self.can_replace_varables = []
        self.num = scope_number #分辨此table屬於哪個scope，從0開始編號
        self.scope_type = scope_type #{compilation, funcdef, others}
        
    def update(self, symbol):
        '''
        確認table中是否出現過該symbol
        如果有:替換該symbol 的value
        無:將symbol存入table
        '''
        self.table.update({symbol.name:[symbol.value,symbol.rate]})
        
    def get_symbol_value(self,symbol_name:str, default = None):
        try:
            return self.table[symbol_name]
        except:
            return default
       
class Symbol():
    '''
    存放著symbol的名字以及被賦的值
    皆以字串保存    
    '''
    def __init__(self, name:str = '', value:str = '', rate : str = None):
        self.name = name
        self.value = value
        self.rate = rate