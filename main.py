#!usr/bin/python3

import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from prompts import system_prompt, available_functions
from collections.abc import Callable
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

from google.genai import types


SYS_INSTRUCTION = genai.types.GenerateContentConfig(system_instruction=system_prompt, temperature=0, tools=[available_functions])
MODEL_NAME = "gemini-2.5-flash"

def call_function(
    function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:
	
	function_map: dict[str, Callable[..., str]] = {
		"get_files_info": get_files_info,
		"get_file_content": get_file_content,
		"write_file": write_file,
		"run_python_file": run_python_file,
	}

	call_id = getattr(function_call, "id", None)

	function_name = function_call.name or ""
	function_args = function_call.args.copy() or {}
	if verbose:
		print(f"Calling function: {function_name}({function_args})")
	else:
		print(f" - Calling function: {function_name}")


	if function_map.get(function_name, "not found") == "not found":
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_name,
					response={"error": f"Unknown function: {function_name}"},
				)
			],
		)
	
	
	function_args["working_dir"] = "./calculator"
	result: str = function_map[function_name](**function_args)

	return types.Content(
		role="tool",
		parts=[
			types.Part.from_function_response(
				name=function_name,
				response={"result": result},
			)
		],
	)


	

def main():
	load_dotenv()
	api_key = os.environ.get("API_KEY")
	if api_key == None:
		raise RuntimeError("environtmental variable not found")
	
	parser = argparse.ArgumentParser(description = "Chatbot")
	parser.add_argument("user_prompt", type=str, help="Write your prompt")	
	parser.add_argument("--verbose", action="store_true", help="print detailed report about tokens used")
	parser.add_argument("--short", action="store_true", help="get short answer")
	args = parser.parse_args()
	prompt = args.user_prompt

	if args.short:
		propmt = "answer shortly: " + prompt

	client = genai.Client(api_key=api_key)
	messages: list[genai.types.Content] = [
		genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)])
	]


	for _ in range(20):
		req_obj = client.models.generate_content(model=MODEL_NAME, contents=messages, config=SYS_INSTRUCTION)

		if req_obj == None:
			raise RuntimeError("out of tokens maybe!?")

		message_content = req_obj.candidates[0].content
		messages.append(req_obj.candidates[0].content)

		usage_metadata = req_obj.usage_metadata
		
		response = {
			"User prompt: ": prompt,
			"Prompt tokens: ": usage_metadata.prompt_token_count,
			"Response tokens: ": usage_metadata.candidates_token_count,
			#"Response:\n": req_obj.content.text
		}

		if args.verbose:
			for key, value in response.items():
				print(key + str(value))

		if req_obj.function_calls == None:
			print(f"finished: {req_obj.text}")
			return 0

		function_calls = req_obj.function_calls
		function_parts = []
		if function_calls == None:
			print("function calls returned is None type")
		else:
			for function_call in function_calls:
				function_call_result = call_function(function_call, args.verbose)
				if function_call_result.parts == None:
					raise Exception("function call returned empty .parts")
				if function_call_result.parts[0].function_response == None:
					raise Exception("function call returned empty .function_response")

				if function_call_result.parts[0].function_response.response == None:
					raise Exception("function call returned empty .response")

				if args.verbose:
					print(f"-> {function_call_result.parts[0].function_response.response["result"] or function_call_result.parts[0].function_response.response["error"]}")
				function_parts.extend(function_call_result.parts)	

		messages.append(genai.types.Content(role="user", parts=function_parts))

			
	print("model interaction took too long, truncated conversation\n " + req_obj.text)					
	sys.exit(1)

	#if req_obj.text != None:	
	#	print("Response:\n" + req_obj.text)
	#else:
	#	print("there is no response text")

	
	

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(e)

