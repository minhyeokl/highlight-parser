import os
import sys
import xlsxwriter
import fitz  # PyMuPDF

def extract_memos_from_pdf(file_path):
    doc = fitz.open(file_path)
    memos = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        annotations = page.annots()

        if annotations:
            for annot in annotations:
                if annot.type[0] == 8:  # 8 is the type for highlight annotations in PyMuPDF
                    memos.append({'text': annot.info['content'], 'page': page_num + 1})
    
    return memos

def merge_duplicates(memos):
    memo_dict = {}
    for memo in memos:
        text = memo['text']
        page = memo['page']
        if text in memo_dict:
            memo_dict[text]['page'].append(page)
        else:
            memo_dict[text] = {'text': text, 'page': [page]}
    
    return list(memo_dict.values())

def export_memos_to_xlsx(memos, output_file):
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()

    # Write headers
    worksheet.write(0, 0, 'Text')
    worksheet.write(0, 1, 'Page')

    row = 1
    for memo in memos:
        worksheet.write(row, 0, memo['text'])
        for col, page in enumerate(memo['page'], start=1):
            worksheet.write(row, col, page)
        row += 1

    workbook.close()

def main(input_file_path, output_file_path):
    memos = extract_memos_from_pdf(input_file_path)
    memos.sort(key=lambda x: x['text'])
    print(f"Total memos: {len(memos)}")
    merged_memos = merge_duplicates(memos)
    export_memos_to_xlsx(merged_memos, output_file_path)


if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        # PyInstaller로 패키징된 실행 파일인 경우
        current_folder = os.path.dirname(sys.executable)
    else:
        # 일반적인 파이썬 스크립트인 경우
        current_folder = os.path.dirname(os.path.abspath(__file__))
    
    input_file_path = os.path.join(current_folder, 'index.pdf')
    output_file_path = os.path.join(current_folder, 'output.xlsx')
    main(input_file_path, output_file_path)