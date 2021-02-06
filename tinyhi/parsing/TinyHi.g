grammar TinyHi;

program: Return* function EOF;

// functions

functions: function*;

function:
	'BEGIN' Name function_args? Return* block? 'END' Name? Return*;

function_args: '(' Name (',' Name)* ')';

block: functions expressions;

// expressions

expressions: expr*;

expr: (control | statement | assignment) Return*;

// Control Block

control: while_control | until_control | if_control;

while_control:
	'WHILE' condition Return* expressions 'END' 'WHILE'?;

until_control:
	'UNTIL' condition Return* expressions 'END' 'UNTIL'?;

if_control:
	'IF' condition Return* expressions else_control? 'END' 'IF'?;

else_control: 'ELSE' Return* expressions;

// Assignment

assignment: Name '<-' statement?;

// Statement

statement:
	brackets // Brackets
	| subscripting // Subscripting
	| statement statement // Concatenation
	| '~' statement // Negation
	| '#' statement // Length
	| statement '*' statement // Multiplication
	| statement '/' statement // Division
	| statement '+' statement // Sum
	| statement '-' statement // Subtraction
	| function_call // Function call
	| input_command // Input
	| String // String Literal
	| Int // Int Literal
	| Name; // Variable

brackets: '(' statement ')';

input_command: '?' Name;

function_call: Name '(' call_args? ')';

call_args: statement (',' statement)*;

subscripting: Name '[' statement ']';

// condition

condition: statement ConditionOp statement;

// Fragments
Name: '.'? [a-zA-Z_][a-zA-Z_0-9]*;

String: '"' [a-zA-Z_0-9]* '"';

Int: ('-')? [0-9]+;

ConditionOp: '<' | '>' | '=' | '<=' | '>=' | '<>';

Return: '\n' | '\r';

// Skip
WS: [ \t]+ -> skip;