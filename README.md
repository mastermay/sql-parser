sql-parser
==========
> A simple version of SQL parser written in Python and C++, the results are saved in a tree.
> For now, only SELECT queries are implemented.

###Python
**Prerequisites:**
* PLY (Python Lex-Yacc) [HELP](http://www.dabeaz.com/ply/ply.html)

**Usage**
```
python yacc.py

-> SELECT a, b FROM c
 + QUERY
   + [SELECT]
   + [FIELDS]
     + [FIELD]
       + a
     + [FIELD]
       + b
   + [FROM]
   + [TABLE]
     + c

-> SELECT a . b , c . d FROM aaa AS a , ccc AS c               
 + QUERY
   + [SELECT]
   + [FIELDS]
     + [FIELD]
       + a.b
     + [FIELD]
       + c.d
   + [FROM]
   + [TABLES]
     + [TABLE]
       + aaa
       + AS
       + a
     + [TABLE]
       + ccc
       + AS
       + c

-> SELECT a FROM ( SELECT b FROM c WHERE d > 1 ) ORDER BY e
 + QUERY
   + [SELECT]
   + [FIELD]
     + a
   + [FROM]
   + [TABLE]
     + QUERY
       + [SELECT]
       + [FIELD]
         + b
       + [FROM]
       + [TABLE]
         + c
       + [WHERE]
       + [CONDITION]
         + [TERM]
           + d
           + >
           + 1
   + [ORDER BY]
   + [FIELD]
     + e

-> SELECT COUNT ( * ) FROM a WHERE b < 1 AND c > 2 ORDER BY d 
 + QUERY
   + [SELECT]
   + [FIELD]
     + COUNT(*)
   + [FROM]
   + [TABLE]
     + a
   + [WHERE]
   + [CONDITIONS]
     + [TERM]
       + b
       + <
       + 1
     + [AND]
     + [TERM]
       + c
       + >
       + 2
   + [ORDER BY]
   + [FIELD]
     + d
```

### C++
**Prerequisites:**
* Lex
* Yacc

**Usage**
```
make
./sql_parser
//enter your select queries
```