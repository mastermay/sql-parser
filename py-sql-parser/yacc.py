import ply.lex as lex
import re
from math import *
import ply.yacc as yacc
from node import node

#TOKENS
tokens=('SELECT','FROM','WHERE','ORDER','BY','NAME','AND','OR','COMMA',
'LP','RP','AVG','BETWEEN','IN','SUM','MAX','MIN','COUNT','NUMBER','AS','DOT')
  
literals = ['=','+','-','*', '^','>','<' ] 
#DEFINE OF TOKENS
def t_LP(t):
    r'\('
    return t

def t_DOT(t):
    r'\.'
    return t

def t_AS(t):
    r'AS'
    return t

def t_SUM(t):
    r'SUM'
    return t

def t_MIN(t):
    r'MIN'
    return t

def t_MAX(t):
    r'MAX'
    return t

def t_COUNT(t):
    r'COUNT'
    return t

def t_AVG(t):
    r'AVG'
    return t

def t_RP(t):
    r'\)'
    return t

def t_BETWEEN(t):
    r'BETWEEN'
    return t

def t_IN(t):
    r'IN'
    return t

def t_SELECT(t):
    r'SELECT'
    return t

def t_FROM(t):
    r'FROM'
    return t

def t_WHERE(t):
    r'WHERE'
    return t

def t_ORDER(t):
    r'ORDER'
    return t

def t_BY(t):
    r'BY'
    return t

def t_OR(t):
    r'OR'
    return t

def t_AND(t):
    r'AND'
    return t

def t_COMMA(t):
    r','
    return t

def t_NUMBER(t):
    r'[0-9]+'
    return t

def t_NAME(t):
    r'[A-Za-z]+|[a-zA-Z_][a-zA-Z0-9_]*|[A-Z]*\.[A-Z]$'
    return t

# IGNORED
t_ignore = " \t"
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# LEX ANALYSIS   
lex.lex()

#PARSING
def p_query(t):
    '''query :  select 
            | LP query RP
                '''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[2]

def p_select(t):
    '''select :   SELECT list FROM table WHERE lst ORDER BY list
	        | SELECT list FROM table WHERE lst
	        | SELECT list FROM table ORDER BY list
	        | SELECT list FROM table '''
    if len(t)==10:
        t[0]=node('QUERY')
	t[0].add(node('[SELECT]'))
	t[0].add(t[2])
	t[0].add(node('[FROM]'))
	t[0].add(t[4])
	t[0].add(node('[WHERE]'))
	t[0].add(t[6])
	t[0].add(node('[ORDER BY]'))
	t[0].add(t[9])
    elif len(t)==8:
        t[0]=node('QUERY')
	t[0].add(node('[SELECT]'))
	t[0].add(t[2])
	t[0].add(node('[FROM]'))
	t[0].add(t[4])
	t[0].add(node('[ORDER BY]'))
	t[0].add(t[7])
    elif len(t)==7:
        t[0]=node('QUERY')
	t[0].add(node('[SELECT]'))
	t[0].add(t[2])
	t[0].add(node('[FROM]'))
	t[0].add(t[4])
	t[0].add(node('[WHERE]'))
	t[0].add(t[6])
    else:
	t[0]=node('QUERY')
	t[0].add(node('[SELECT]'))
	t[0].add(t[2])
	t[0].add(node('[FROM]'))
	t[0].add(t[4])

def p_table(t):
    '''table : NAME
            | LP query RP
            | NAME AS NAME
            | table AS NAME
            | table COMMA table'''
    if len(t)==2:
        t[0]=node('[TABLE]')
	t[0].add(node(t[1]))
    elif t[2]=='AS' and isinstance(t[1], node):
	t[0]=node('[TABLE]')
	t[0].add(t[1])
	t[0].add(node('AS'))
	t[0].add(node(t[3]))
    elif t[2]=='AS' and not isinstance(t[1], node):
	t[0]=node('[TABLE]')
	t[0].add(node(t[1]))
	t[0].add(node('AS'))
	t[0].add(node(t[3]))
    elif t[2]==',':
	t[0]=node('[TABLES]')
	t[0].add(t[1])
	t[0].add(t[3])
    else :
	t[0]=node('[TABLE]')
	t[0].add(t[2])
        

def p_lst(t):
    ''' lst  : condition
             | condition AND condition
             | condition OR condition
             | NAME BETWEEN NUMBER AND NUMBER
             | NAME IN LP query RP
             | NAME '<' agg
             | NAME '>' agg
             | agg '>' NUMBER
             | NAME '=' agg
             | agg '=' NUMBER
             | agg '<' NUMBER
              '''
    
    if len(t)==2:
        t[0]=node('[CONDITION]')
	t[0].add(t[1])
    elif t[2]==',':
	t[0]=node('[CONDITIONS]')
	t[0].add(t[1])
	t[0].add(t[3])
    elif t[2]=='AND':
	t[0]=node('[CONDITIONS]')
	t[0].add(t[1])
	t[0].add(node('[AND]'))
	t[0].add(t[3])
    elif t[2]=='OR':
	t[0]=node('[CONDITIONS]')
	t[0].add(t[1])
	t[0].add(node('[OR]'))
	t[0].add(t[3])
    elif t[2]=='BETWEEN':
        temp='%s >= %s & %s <= %s'%(t[1],str(t[3]),t[1],str(t[5]))
	t[0]=node('[CONDITION]')
	t[0].add(node('[TERM]'))
	t[0].add(node(temp))
    elif t[2]=='IN':
	t[0]=node('[CONDITION]')
	t[0].add(node(t[1]))
	t[0].add(node('[IN]'))
	t[0].add(t[4])
    elif t[2]=='<' and len(t)==4:
        temp='%s < %s'%(str(t[1]),str(t[3]))
	t[0]=node('[CONDITION]')
	t[0].add(node('[TERM]'))
	t[0].add(node(temp))
    elif t[2]=='=' and len(t)==4:
        temp='%s = %s'%(str(t[1]),str(t[3]))
	t[0]=node('[CONDITION]')
	t[0].add(node('[TERM]'))
	t[0].add(node(temp))
    elif t[2]=='>' and len(t)==4:
        temp='%s > %s'%(str(t[1]),str(t[3]))
	t[0]=node('[CONDITION]')
	t[0].add(node('[TERM]'))
	t[0].add(node(temp))
    else:
        t[0]=node('')
        

def p_condition(t):
    ''' condition : NAME '>' NUMBER
                  | NAME '>' agg  
                  | NAME '<' NUMBER
                  | NAME '<' agg
                  | NAME '=' NUMBER
                  | NAME '=' agg
                  | NAME '>' NAME
                  | NAME '<' NAME
                  | NAME '=' NAME
                  | list '>' list
                  | list '<' list
                  | list '=' list
                  | list '>' NUMBER
                  | list '<' NUMBER
                  | list '=' NUMBER  '''
    t[0]=node('[TERM]')
    if isinstance(t[1], node) :
        t[0].add(t[1])
    else :
	t[0].add(node(str(t[1])))
    t[0].add(node(t[2]))
    if isinstance(t[3], node) :
        t[0].add(t[3])
    else :
	t[0].add(node(str(t[3])))

def p_agg(t):
    ''' agg : SUM LP NAME RP
            | AVG LP NAME RP
            | COUNT LP NAME RP
            | MIN LP NAME RP 
            | MAX LP NAME RP
            | COUNT LP '*' RP '''
    t[0]='%s(%s)'%(t[1],t[3])

def p_list(t):
    ''' list : '*'
	     | NAME
             | NAME DOT NAME 
             | list COMMA list
             | list AND NAME
             | list OR NAME        
             | agg '''
    if len(t)==2:
        t[0]=node('[FIELD]')
	t[0].add(node(t[1]))
    elif t[2]==',':
	t[0]=node('[FIELDS]')
	t[0].add(t[1])
	t[0].add(t[3])
    else:
        temp='%s.%s'%(t[1],t[3])
	t[0]=node('[FIELD]')
	t[0].add(node(temp))
    
def p_error(t):
    print("Syntax error at '%s'" % t.value)

yacc.yacc()

while 1:
    try:
        s = raw_input('-> ')  
        pass
    except EOFError:
        break
    parse=yacc.parse(s)
    parse.print_node(0)
