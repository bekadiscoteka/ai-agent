import os
from os import path


def write_file(working_dir: str, target_dir: str, content: str):
	try:
		abs_working_dir = path.normpath( path.abspath(working_dir) )
		abs_target_dir = path.normpath( path.join(abs_working_dir, target_dir) )
		os.makedirs( os.path.dirname(abs_target_dir), exist_ok=True )

		if path.commonpath( [abs_working_dir, abs_target_dir] ) != abs_working_dir:
			return f'Error: Cannot write to "{target_dir}" as it is outside the permitted working directory'
		if path.isdir( target_dir ):
			return f'Error: Cannot write to "{target_dir}" as it is a directory'
		

		with open(abs_target_dir, "w") as fd:
			fd.write(content)

		return f'Successfully wrote to "{target_dir}" ({len(content)} characters written)'
	except Exception as e:
		return f"ERROR: {e}"
