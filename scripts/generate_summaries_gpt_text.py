import asyncio
import typer
import time
import os

from services.openai import OpenAIService

app = typer.Typer()

def generate_summaries(text_path):
    with open(text_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return OpenAIService().chat_completion('Please summarize the following document: ' + text)

async def main(txt_folder_path, summary_folder_path):
    exceed_token_files = []
    text_files_list = os.listdir(txt_folder_path)

    for text_file in text_files_list:
        if not text_file.endswith('.txt'):
            continue

        summary_file_path = os.path.join(summary_folder_path, text_file)
        summary_excess_file_path = os.path.join(summary_folder_path + '-errors', text_file)

        if os.path.isfile(summary_file_path):
            continue

        text_path = os.path.join(txt_folder_path, text_file)
        summary = generate_summaries(text_path)

        if summary['status'] == 200:
            with open(summary_file_path, 'w') as file:
                file.write(summary['message'])

        elif summary['status'] == 400:
            exceed_token_files.append(text_file)
            with open(summary_excess_file_path, 'w') as file:
                file.write(str(summary))

    print('exceed_tokenFiles: ', exceed_token_files)

@app.command()
def generate_summary(txt_folder_path: str, summary_folder_path: str):
    start_time = time.time()
    asyncio.run(main(txt_folder_path, summary_folder_path))
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

@app.command()
def placeholder(name: str):
    pass

if __name__ == "__main__":
    app()


    