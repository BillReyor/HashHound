import re
import sys
import PyPDF2
from io import BytesIO
from collections import defaultdict


def get_file_path(prompt: str) -> str:
    return input(prompt)


def read_contents(file_path: str) -> str:
    try:
        with open(file_path, 'rb') as f:
            contents = f.read()
            if file_path.lower().endswith('.pdf'):
                return export_pdf_to_text(contents)
            else:
                return contents.decode()
    except FileNotFoundError:
        print("Input file not found!")
        sys.exit()


def export_pdf_to_text(pdf_contents: bytes) -> str:
    file_like_object = BytesIO(pdf_contents)
    pdf_reader = PyPDF2.PdfReader(file_like_object)
    contents = ''
    for page_num in range(len(pdf_reader.pages)):
        contents += pdf_reader.pages[page_num].extract_text()
    return contents


def save_contents_to_file(file_path: str, contents: str):
    with open(file_path, 'w') as f:
        f.write(contents)


def find_hashes(contents: str) -> defaultdict:
    grouped_hashes = defaultdict(list)
    hash_regexes = {
        'MD5': r'\b[a-fA-F0-9]{32}\b',
        'SHA1': r'\b[a-fA-F0-9]{40}\b',
        'SHA256': r'\b[a-fA-F0-9]{64}\b'
    }

    rows = re.split(r'[\r\n]+', contents)
    for i, row in enumerate(rows):
        for hash_type, regex in hash_regexes.items():
            found_hashes = re.findall(regex, row)
            if found_hashes:
                grouped_hashes[hash_type].extend(found_hashes)
            elif "Sample" in row:
                # If the line has "Sample", this means it's a header row, and we should skip it.
                continue
            else:
                # If no hashes were found, we can assume that it's a malware family name and skip this row.
                break

    return grouped_hashes


def write_hashes_to_file(output_file_path: str, input_file_path: str, hashes: defaultdict):
    with open(output_file_path, 'wb') as f:
        f.write(f"Hashes found in {input_file_path}:\n".encode())
        for hash_type, hash_list in hashes.items():
            f.write(f"\n{hash_type}:\n".encode())
            for hash in hash_list:
                f.write(f"{hash}\n".encode())
        f.write(f"\nOutput file path: {output_file_path}\n".encode())


def main():
    input_file_path = get_file_path("Please provide a file path for input: ")
    intermediate_file_path = "file.txt"
    output_file_path = get_file_path("Please provide a file path for output: ")

    contents = read_contents(input_file_path)
    save_contents_to_file(intermediate_file_path, contents)

    contents_from_file = read_contents(intermediate_file_path)
    hashes = find_hashes(contents_from_file)
    write_hashes_to_file(output_file_path, input_file_path, hashes)


if __name__ == '__main__':
    main()
