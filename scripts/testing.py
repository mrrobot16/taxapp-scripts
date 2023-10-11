from dotenv import load_dotenv
# Now you can access the environment variables as usual
import os
# Load environment variables from the .env file in the current directory
load_dotenv()

openai_api_key = os.getenv("open_ai_api_key")
print("openai_api_key: ", openai_api_key)
