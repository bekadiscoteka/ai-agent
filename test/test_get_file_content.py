from functions.get_file_content import get_file_content

cases = {
	("calculator", "main.py"),
	("calculator", "pkg/calculator.py"),
	("calculator", "/bin/cat"),
	("calculator", "pkg/does_not_exist.py")
}

for case in cases:
	result = get_file_content(*case)
	print(result)

result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")
