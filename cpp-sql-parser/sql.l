%{
#include "head.h"
#include "y.tab.h"
#include<iostream>
#include<string>
using namespace std;
extern YYSTYPE yylval;

%}

digit        [0-9]
letter       [A-Za-z]
word         {letter}({letter}|{digit})*
whitespace   ([ \t]*)
compare      [<>=]|(!=)|(>=)|(<=)|(like)
number       {digit}+\.?(digit)*
%%

[\(]         {return LEFTPARENTHESIS;}
[\)]         {return RIGHTPARENTHESIS;}
select       {return SELECT;}
from         {return FROM;}
where        {return WHERE;}
{whitespace} {}
and          {yylval = new TreeNode("AND"); return LOGIC;}
or           {yylval = new TreeNode("OR"); return LOGIC;}
,            {return COMMA;}
;            {return SEMICOLON;}
{compare}    {yylval = new TreeNode(yytext);return COMPARE;}
{number}     {yylval = new TreeNode(yytext); return NUMBER;}
{word}       {yylval = new TreeNode(yytext); return WORD;}
.            {}
%%
int yywrap(void) {
return 1;
}

int yyerror(string s)
{
    cout << s << endl;
    return 1;
}
