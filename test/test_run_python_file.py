from functions.run_python_file import run_python_file


cases = [
	("calculator", "main.py"),
	("calculator", "main.py", ["3 + 5"]),
	("calculator", "tests.py"),
	("calculator", "../main.py"),
	("calculator", "nonexistent.py"),
	("calculator", "lorem.txt")

]

for case in cases:
	resp = run_python_file(*case)
	print(resp)
