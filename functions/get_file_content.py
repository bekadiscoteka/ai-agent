import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"reads content of file. If content is above {MAX_CHARS} characters, it will truncate output at that",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the file. (default is the working directory itself)",
            ),
        },
    ),
)

def get_file_content(working_dir, file_path):
	try:
		working_dir_abs = os.path.abspath(working_dir)
		target = os.path.normpath( os.path.join(working_dir_abs, file_path) )
		valid = os.path.commonpath( [working_dir_abs, target] ) == working_dir_abs

		if not valid:
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'	
		if not os.path.isfile(target):
			return f'Error: File not found or is not a regular file: "{file_path}"'	


		with open(target) as fd:
			content: str = fd.read(MAX_CHARS)
			if fd.read(1) is not None:
				content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'	

			return content

	except Exception as e:
		return f'Error: {e}'
		
		
	
	


