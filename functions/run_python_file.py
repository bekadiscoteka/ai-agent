import subprocess
from os import path as p
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
	try:
		abs_workdir = p.normpath( p.abspath(working_directory) )
		abs_filepath = p.normpath( p.join(abs_workdir, file_path) )

		if p.commonpath( [abs_workdir, abs_filepath] ) != abs_workdir:
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
		if not p.isfile( abs_filepath ):
			return f'Error: "{file_path}" does not exist or is not a regular file'	
		if not (abs_filepath.split('.')[-1] == "py"):
			return f'Error: "{file_path}" is not a Python file'

		command = ["python", abs_filepath]
		if args != None:
			command.extend(args)

		obj = subprocess.run(command, capture_output=True, cwd=abs_workdir, text=True)
		out_text = ""
		if obj.returncode != 0:
			out_text += f"Process exited with code {obj.returncode}\n"

		if len(obj.stdout) != 0:
			out_text += f"STDOUT: {obj.stdout}\n"
		elif len(obj.stderr) != 0:
			out_text += f"STDERR: {obj.stderr}\n"
		else:
			out_text += f"No output produced"

		return out_text
	except Exception as e:
		return f"Error: executing Python file: {e}"
