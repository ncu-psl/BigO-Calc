#!/usr/bin/env python
# coding: utf-8

# ![title](https://i.imgur.com/GSGG2ps.png)

# In[99]:


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
    
    def add_table(self): 
        '''
        呼叫此函式當visitor進入新的scope
        first in last out
        '''
        table = symbol_table(self.__current_scope_number)
        self.table_list.append(table)
        self.current_table = table
        self.__current_scope_number+=1
    
    def pop_table(self):
        '''呼叫此函式當visitor離開scope'''
        if self.__current_scope_number is not 0:
            self.table_list.pop()
            self.__current_scope_number -= 1
            if self.__current_scope_number is not 0:
                self.current_table = self.table_list[-1]

        else: 
            print('table list is empty')
           
    def add_symbol(self, symbol_name, value):
        sym = symbol(symbol_name,value)
        self.current_table.update(sym)
        
    def get_symbol_value(self,symbol_name:str):
        for t in reversed(self.table_list):
            if symbol_name in t.table:
                return t.get_symbol_value(symbol_name)
        return None
    
    def print_current_table(self):
        return self.current_table.table

class symbol_table(object):
    '''
    此class的目的是為了儲存每個scope中的symbol name 以及value
    將資訊存在table中
    table中儲存identifier這個類別的物件
    '''
    def __init__(self,scope_number):
        self.table = {}
        self.can_replace_varables = []
        self.num = scope_number #分辨此table屬於哪個scope，從0開始編號
        
    def update(self, symbol):
        '''
        確認table中是否出現過該symbol
        如果有:替換該symbol 的value
        無:將symbol存入table
           '''
        self.table.update({symbol.name:symbol.value})
        
    def get_symbol_value(self,symbol_name:str):
        return self.table[symbol_name]
       
class symbol():
    '''
    存放著symbol的名字以及被賦的值
    皆以字串保存    
    '''
    def __init__(self, name:str, value:str):
        self.name = name
        self.value = value
    


# manager = table_manager()
# current_scope_number = -1
# manager.add_table()
# current_scope_number+=1
# 
# manager.add_symbol('n','n++')
# manager.add_symbol('m','m')

# a = symbol('n','n--')
# manager.add_symbol(a)
# 

# manager.get_symbol_value('m')

# current_scope_number = 0
# current_scope_number = manager.add_table(current_scope_number)
# 

# !jupyter-notebook list

# current_scope_number = manager.add_table(current_scope_number)
# current_scope_number
# 

# manager.table_list
