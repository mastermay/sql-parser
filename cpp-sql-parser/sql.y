%{
#include "head.h"
#include<iostream>
#include<string>
using namespace std;

extern int yylex(void);
extern int yyparse(void);
extern int yyerror(string);

%}
%token SELECT FROM WHERE WORD COMMA SEMICOLON COMPARE NUMBER LOGIC LEFTPARENTHESIS RIGHTPARENTHESIS

%%
all:
    select SEMICOLON
{
    ((TreeNode *) $$)->print_node(1);
    return 0;
}

select:
    SELECT tnames FROM tables
{
    $$ = new TreeNode("QUERY");
    ((TreeNode *) $$) -> add( new TreeNode("SELECT") );
    ((TreeNode *) $$) -> add( (TreeNode *)$2 );
    ((TreeNode *) $$) -> add( new TreeNode("FROM") );
    ((TreeNode *) $$) -> add( (TreeNode *)$4 );
}

    | SELECT tnames FROM tables WHERE wheres
{
    $$ = new TreeNode("QUERY");
    ((TreeNode *) $$) -> add( new TreeNode("SELECT") );
    ((TreeNode *) $$) -> add( (TreeNode *)$2 );
    ((TreeNode *) $$) -> add( new TreeNode("FROM") );
    ((TreeNode *) $$) -> add( (TreeNode *)$4 );
    ((TreeNode *) $$) -> add( new TreeNode("WHERE") );
    ((TreeNode *) $$) -> add( (TreeNode *)$6 );
}

tnames:
    tname
{
    $$ = new TreeNode("FIELD");
    ((TreeNode *) $$) -> add( (TreeNode *)$1 );

}
    | tnames COMMA tname
{
    $$ = new TreeNode("FIELDS");
    ((TreeNode *) $$) -> add( (TreeNode *)$1 );
    ((TreeNode *) $$) -> add( new TreeNode(",") );
    ((TreeNode *) $$) -> add( (TreeNode *)$3 );
}

tname:
    WORD
{    
    $$ = new TreeNode($1->getData());
}


tables:
    table
{
    $$ = new TreeNode("TABLE");
    ((TreeNode *) $$) -> add( (TreeNode *)$1 );
}
    | tables COMMA table
{
    $$ = new TreeNode("TABLES");
    ((TreeNode *) $$) -> add( (TreeNode *)$1 );
    ((TreeNode *) $$) -> add( new TreeNode(",") );
    ((TreeNode *) $$) -> add( (TreeNode *)$3 );
}


table:
    WORD
{
    $$ = new TreeNode( $1->getData() );   
}
    | LEFTPARENTHESIS select RIGHTPARENTHESIS
{
    $$ = $2;
}

wheres:
    comp
{
    $$ = new TreeNode("CONDITION");
    ((TreeNode *) $$) -> add( (TreeNode *)$1 );
}
    | comp LOGIC wheres
{
    $$ = new TreeNode("CONDITIONS");
    ((TreeNode *) $$) -> add( (TreeNode *)$1 );
    ((TreeNode *) $$) -> add( (TreeNode *)$2 );
    ((TreeNode *) $$) -> add( (TreeNode *)$3 );
}

comp:
    wordornum COMPARE wordornum
{
    $$ = new TreeNode("COMPARE");
    ((TreeNode *) $$) -> add( (TreeNode *)$1 );
    ((TreeNode *) $$) -> add( (TreeNode *)$2 );
    ((TreeNode *) $$) -> add( (TreeNode *)$3 );
}

wordornum:
    WORD
{    
    $$ = new TreeNode( $1->getData() );
}
    | NUMBER
{
    $$ = new TreeNode( $1->getData() );
}

%%

int main()
{
    yyparse();
    return 0;
}
