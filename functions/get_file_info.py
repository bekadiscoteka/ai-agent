import os

def get_file_info(working_dir, directory: str = '.'):
	try: 
		target = os.path.normpath( os.path.join(working_dir, directory) )
		valid = os.path.commonpath( working_dir, target ) == working_dir

		if not valid:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
		if not os.path.exists(target):
			return f'Error: "{directory}" is not a directory'
		
		return f'Success: "{directory}" is within the working directory'	
	except Exception as e:
		return f"Error: {e}"
