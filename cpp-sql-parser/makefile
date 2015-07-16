LEX=flex
YACC=yacc
CC=g++

sql_parser: sql_y.o sql_l.o treeNode.o
	$(CC) sql_y.o sql_l.o treeNode.o  -o $@ -lfl


y.tab.c: sql.y lex.yy.c
	$(YACC) -vdt sql.y

lex.yy.c: sql.l treeNode.o
	$(LEX) sql.l

sql_y.o: y.tab.c
	$(CC) -c $< -o $@

sql_l.o: lex.yy.c
	$(CC) -c $< -o $@
treeNode.o: treeNode.cpp
	$(CC) -std=c++11 -c $< -o $@
clean:
	rm -f *.c *.o sql_parser y.output y.tab.h
