import os
import typer
import time
import fitz

app = typer.Typer()

def pdf_to_text(pdf_file_path, text_file_path):
    with fitz.open(pdf_file_path) as pdf:
        full_text = ""
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text = page.get_text()
            full_text += text + "\n"
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(full_text)

def process_directory(pdf_folder_path, text_folder_path):
    for filename in os.listdir(pdf_folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder_path, filename)
            text_filename = os.path.splitext(filename)[0] + ".txt"
            text_path = os.path.join(text_folder_path, text_filename)
            pdf_to_text(pdf_path, text_path)

@app.command()
def convert_to_text(pdf_folder_path: str, text_folder_path: str):
    start_time = time.time()
    process_directory(pdf_folder_path, text_folder_path)
    end_time = time.time()
    print("\n")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

@app.command()
def placeholder(name: str):
    pass

if __name__ == "__main__":
    app()