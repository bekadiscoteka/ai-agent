import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_file_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)



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
