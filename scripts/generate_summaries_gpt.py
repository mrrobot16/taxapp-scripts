import asyncio
import typer
import time
from datetime import datetime
import os
import fitz
import PyPDF2

from services.openai import OpenAIService


app = typer.Typer()


def read_pdf_text(pdf_path):
    content = ""

    with fitz.open(pdf_path) as pdf_file:
        num_pages = pdf_file.page_count

        for page_num in range(num_pages):
            page = pdf_file[page_num]
            page_text = page.get_text()
            content += page_text
    return content


def generate_summaries(pdf_path):
    text = read_pdf_text(pdf_path)
    return OpenAIService().chat_completion('Please summarize the following document: ' + text)

async def main(pdf_folder_path, text_folder_path):
    exceed_token_files = []
    forms_folder_list_dir = os.listdir(pdf_folder_path)
    for form_pdf in forms_folder_list_dir:
        form_txt_file_path = os.path.join(text_folder_path, form_pdf.split('.')[0]+'.txt')
        form_text_excess_file_path = os.path.join(text_folder_path + '-excess', form_pdf.split('.')[0]+'.txt')
        is_file = os.path.isfile(form_txt_file_path)
        pdf_path = os.path.join(pdf_folder_path, form_pdf)
        if is_file:
            continue
        summary = generate_summaries(pdf_path)
        print("\n")
        print('pdf_path', pdf_path)
        print("\n")
        print('summary', summary)
        print('\n')
        if summary['status'] == 400:
            print("\n")
            print('Error')
            print('pdf_path', pdf_path)
            print(form_pdf)
            print(summary)
            exceed_token_files.append(form_pdf)
            with open(form_text_excess_file_path, 'w') as file:
                file.write(str(summary))
            continue
        if summary['status'] == 200:
            print("\n")
            print('Success')
            print('pdf_path', pdf_path)
            with open(form_txt_file_path, 'w') as file:
                file.write(summary['message'])
    print('\n')
    print('exceed_tokenFiles: ', exceed_token_files)

@app.command()
def generate_summary(pdf_folder_path: str, text_folder_path: str):
    start_time = time.time()
    asyncio.run(main(pdf_folder_path, text_folder_path))
    end_time = time.time()
    print("\n")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

@app.command()
def placeholder(name: str):
    pass

if __name__ == "__main__":
    app()
