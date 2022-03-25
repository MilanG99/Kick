
------------------ FILES ------------------

lexer.py
	- python source code for the project lexer
	- used by the parser/interpreter

parser.py
	- python source code for the rescursive-descent parser/interpreter
	- contains code for the parser and test driver function to showcase functionality of parser and interpreter
	- execute via command line (see RUN THE PARSER)
	- command line used for input/output during execution

------------------ RUN THE PARSER ------------------

- to compile and run the project, type: "python parser.py <test_file>" in a command line in the project directory
- <test_file> should be replaced by the desired test file name
- example:
	- python parser.py test1.txt
	- will tokenize, parse, and interpret the contents of test1.txt as input

------------------ NOTES ------------------

- open the test1.txt, test2.txt, test3.txt, test4.txt, test5.txt files to view/modify code being processed
- to make other test cases, you can modify the test files or add new ones