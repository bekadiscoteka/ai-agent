import os

def get_file_info(working_dir, directory: str = '.'):
	try: 
		working_dir_abs = os.path.abspath(working_dir)
		target = os.path.normpath( os.path.join(working_dir_abs, directory) )
		valid = os.path.commonpath( [working_dir_abs, target] ) == working_dir_abs

		if not valid:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
		if not os.path.isdir(target):
			return f'Error: "{directory}" is not a directory'

		# prepare the dictionary

		dirlist = os.listdir(target)
		contents_list: list[str] = []

		for name in dirlist:
			path = os.path.join(target, name)
			size = os.path.getsize(path)
			is_dir = os.path.isdir(path)

			contents_list.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
		
		return '\n'.join(contents_list) 
	except Exception as e:
		return f"Error: {e}"
