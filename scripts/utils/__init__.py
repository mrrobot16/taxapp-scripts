import fitz
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("open_ai_api_key")

openai.api_key = openai_api_key

def read_pdf_text(pdf_path):
    content = ""

    with fitz.open(pdf_path) as pdf_file:
        num_pages = pdf_file.page_count

        for page_num in range(num_pages):
            page = pdf_file[page_num]
            page_text = page.get_text()
            content += page_text
    return content


def generate_summary(pdf_path):
    text = read_pdf_text(pdf_path)
    return gpt3_completion('Please summarize the following document: ' + text)


def gpt3_completion(prompt, engine='gpt-3.5-turbo-16k', temp=0.5, top_p=0.3, tokens=1000):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    try:
        response = openai.ChatCompletion.create(
            model=engine,
            messages=[
                {"role": "system", "content": "You are a helpful tax CPA for the United States of America with experience working with the IRS."},
                {"role": "user", "content": prompt}
            ],
            temperature=temp,
            max_tokens=tokens
        )
        return response['choices'][0]['message']['content']
    except Exception as oops:

        return "GPT-3 error: %s" % oops