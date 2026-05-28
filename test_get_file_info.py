from functions.get_file_info import get_file_info

test_cases = {
	("calculator", '.'): True,
	("calculator", '/bin'): False,
	("calculator", '../'): False,
	("calculator", 'main.py'): False
}

def tests():
	
	passed = 0
	failed = 0

	for args, value in test_cases.items():
		resp: str = get_file_info(args[0], args[1])
		splitted = resp.split(':', maxsplit=1)


		if (splitted[0] == "Success") == value:
			passed += 1
		else:
			print(f'Test failed at inputs: {args}\nexpected: {"Success..." if value else "Error..."}, actual: {splitted[0]}')
			failed += 1

	print(f"passed: {passed}, failed: {failed}") 


if __name__ == "__main__":
	tests()

