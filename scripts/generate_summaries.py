import argparse
from tqdm import tqdm
import os
from utils import *
import os
import time

def main(args):
    start_time = time.time()
    forms_summary_folder = str(args.save_summaries)
    forms_folder = str(args.pdfs)
    exceed_token_files = []
    forms_folder_list_dir = tqdm(os.listdir(forms_folder))
    for pdf_file in forms_folder_list_dir:
        file2save = os.path.join(forms_summary_folder, pdf_file.split('.')[0]+'.txt')
        is_file = os.path.isfile(file2save)
        pdf_path = os.path.join(forms_folder, pdf_file)
        if is_file:
            continue
        summary = generate_summary(pdf_path)
        if 'GPT-3 error' in summary:
            print('Error')
            print(pdf_file)
            print(summary)
            exceed_token_files.append(pdf_file)
            continue
        with open(file2save, 'w') as f:
            f.write(summary)
    print('exceed_tokenFiles: ', exceed_token_files)
    print('Time Taken: ', time.time() - start_time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument('--save-summaries', type=str, required=True)
    parser.add_argument('--pdfs', type=str, required=True)
    args = parser.parse_args()

    os.makedirs(args.save_summaries,exist_ok=True)

    main(args)