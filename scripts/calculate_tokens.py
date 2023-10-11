import fitz  
import tiktoken

# Load your text from a file or provide it as a string
path = '../../2022-forms/forms/56.txt'
# with open('your_text_file.txt', 'r', encoding='utf-8') as file:
with open(path, 'r', encoding='utf-8') as file:
    text = file.read()

# Initialize the tokenizer with your text
tokenizer = tiktoken
tokenizer.from_str(text)

# Count the tokens
token_count = len(tokenizer)

print(f"Number of tokens in the text: {token_count}")