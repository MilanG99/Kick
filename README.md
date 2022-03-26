# Kick - Interpreted Language (Written in Python)

This project is a toy interpreted language that is implemented with Python. It is complete with a lexer, tokenizer, recursive-descent parser, and interpreter.

This is currently a WIP. Modifications and updates to come.

# Files
lexer.py :
- python source code for the project lexer
- used by the parser/interpreter

parser.py :
- python source code for the rescursive-descent parser/interpreter
- contains code for the parser and test driver function to showcase functionality of parser and interpreter
- execute via command line (see Execute Programs with Kick)
- command line used for input/output during execution

# Execute Programs with Kick

- to compile and run the project, type: "python parser.py <test_file>" in a command line in the project directory
- <test_file> should be replaced by the desired test file name
- example:
	- python parser.py test1.txt
	- will tokenize, parse, and interpret the contents of test1.txt as input

# Notes

- open the test1.txt, test2.txt, test3.txt, test4.txt, test5.txt files to view/modify code being processed
- to make other test cases, you can modify the test files or add new ones