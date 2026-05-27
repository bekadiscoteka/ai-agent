import os
import argparse
from dotenv import load_dotenv
from google import genai

def main():
	load_dotenv()
	api_key = os.environ.get("API_KEY")
	if api_key == None:
		raise RuntimeError("environtmental variable not found")
	
	parser = argparse.ArgumentParser(description = "Chatbot")
	parser.add_argument("user_prompt", type=str, help="user prompt")
	args = parser.parse_args()
	prompt = args.user_prompt

	client = genai.Client(api_key=api_key)
	model = "gemini-2.5-flash"
	req_obj = client.models.generate_content(model=model, contents=prompt)
	if req_obj == None:
		raise RuntimeError("out of tokens maybe!?")

	usage_metadata = req_obj.usage_metadata
	
	response = {
		"User prompt: ": prompt,
		"Prompt tokens: ": usage_metadata.prompt_token_count,
		"Response tokens: ": usage_metadata.candidates_token_count,
		"Response:\n": req_obj.text
	}

	for key, value in response.items():
		print(key + str(value))
	
	

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(e)

