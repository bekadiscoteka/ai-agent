from functions.get_file_info import get_file_info

test_cases = {
	("calculator", '.'): True,
	("calculator", 'pkg'): True,
	("calculator", '/bin'): False,
	("calculator", '../'): False,
}

def tests():
	
	passed = 0
	failed = 0

	for args, value in test_cases.items():
		resp: str = get_file_info(args[0], args[1])
		print(f"Result for '{args[1]}' directory:\n{resp}")

	return 0


if __name__ == "__main__":
	tests()

