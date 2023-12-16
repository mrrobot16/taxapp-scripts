import os
import pandas as pd
import typer
import fitz  # PyMuPDF
from datetime import datetime

app = typer.Typer()

def estimate_tokens(file_path):
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    elif file_path.endswith('.pdf'):
        text = read_pdf_text(file_path)
    else:
        return 0  # Unsupported file format

    char_count = len(text)
    token_count = char_count / 4  # Approximate token count
    return token_count

def read_pdf_text(pdf_path):
    content = ""
    with fitz.open(pdf_path) as pdf_file:
        num_pages = pdf_file.page_count
        for page_num in range(num_pages):
            page = pdf_file[page_num]
            content += page.get_text()
    return content

def process_directory(directory_path, max_tokens):
    report_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt") or filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            token_count = estimate_tokens(file_path)
            token_difference = max_tokens - token_count
            exceeded_max = token_count > max_tokens
            report_data.append([filename, int(token_count), int(token_difference), exceeded_max])
    return report_data

def generate_csv_report(report_data, output_path):
    data_frame = pd.DataFrame(report_data, columns=['Filename', 'Token Count', 'Token Difference', 'Exceeded Max'])
    data_frame.to_csv(output_path, index=False)

def get_formatted_datetime():
    return datetime.now().strftime("%d-%m-%y-%H:%M")

@app.command()
def token_report(directory_path: str, output_folder: str, max_tokens: int):
    report_data = process_directory(directory_path, max_tokens)
    formatted_datetime = get_formatted_datetime()
    output_csv_path = os.path.join(output_folder, f"token_report-{formatted_datetime}.csv")
    generate_csv_report(report_data, output_csv_path)
    typer.echo(f"Report generated at {output_csv_path}")

@app.command()
def placeholder(name: str):
    pass

if __name__ == "__main__":
    app()
