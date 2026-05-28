import os

def get_file_info(working_dir, directory: str = '.'):
	try: 
		working_dir_abs = os.path.abspath(working_dir)
		target = os.path.normpath( os.path.join(working_dir_abs, directory) )
		print(f"DEBUG INFO: working dir = {working_dir}, target = {target}")
		valid = os.path.commonpath( [working_dir_abs, target] ) == working_dir_abs

		if not valid:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
		if not os.path.isdir(target):
			return f'Error: "{directory}" is not a directory'
		
		return f'Success: "{directory}" is within the working directory'	
	except Exception as e:
		return f"Error: {e}"
