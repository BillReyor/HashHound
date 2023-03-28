import re
import sys
import PyPDF2

def get_file_path(prompt: str) -> str:
    return input(prompt)

def read_contents(file_path: str) -> str:
    try:
        with open(file_path, 'rb') as f:
            contents = f.read()
            if file_path.lower().endswith('.pdf'):
                return extract_pdf_text(contents)
            else:
                return contents
    except FileNotFoundError:
        print("Input file not found!")
        sys.exit()

def extract_pdf_text(pdf_contents: bytes) -> str:
    pdf_reader = PyPDF2.PdfFileReader(pdf_contents)
    contents = ''
    for page in range(pdf_reader.getNumPages()):
        contents += pdf_reader.getPage(page).extractText()
    return contents

def find_hashes(contents: str) -> list:
    return re.findall(r'\b([a-fA-F\d]{32,64})\b', contents)

def write_hashes_to_file(output_file_path: str, input_file_path: str, hashes: list):
    with open(output_file_path, 'w') as f:
        f.write(f"Hashes found in {input_file_path}:\n")
        for hash in hashes:
            f.write(f"{hash}\n")
        f.write(f"Output file path: {output_file_path}")

def main():
    input_file_path = get_file_path("Please provide a file path for input: ")
    output_file_path = get_file_path("Please provide a file path for output: ")

    contents = read_contents(input_file_path)
    hashes = find_hashes(contents)
    write_hashes_to_file(output_file_path, input_file_path, hashes)

if __name__ == '__main__':
    main()
