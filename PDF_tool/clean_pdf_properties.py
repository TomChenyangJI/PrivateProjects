import os
import time
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from pathlib import Path


# global variables
# script_path = Path(__file__).absolute()
script_parent_path = Path(__file__).parent
current_directory = script_parent_path

# CONSTANT
INTERVAL = 60

def scheduler(target, interval=INTERVAL):
    while True:
        target()
        print("the process is sleeping ... ")
        time.sleep(interval)


def clean_pdf_file_properties(file):

    merger = PdfMerger()
    merger.append(file)
    merger.write(file)
    merger.close()

    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    metadata = reader.metadata
    # print(metadata["/Producer"])
    metadata.update({
        '/Producer': '',  # Set a custom producer
        # '/Author': ' ',  # Optional: Update or add other metadata fields
    })
    writer.add_metadata(metadata)
    with open(file, "wb") as f_out:
        writer.write(f_out)


def get_all_dirnames(file=os.path.join(current_directory, "dirnames.txt")):
    with open(file, "r") as fi:
        lines = fi.readlines()
        lines = [line.strip() for line in lines]
        return lines


def get_all_pdf_files(dirname, all_files=[]):
    components = os.listdir(dirname)
    components = [os.path.join(dirname, component) for component in components]

    for component in components:
        if os.path.isdir(component):
            # this is a sub-folder
            get_all_pdf_files(component)

        elif os.path.isfile(component) and component.endswith("pdf"):
            # this is a pdf file
            # os.path.getmtime()
            all_files.append(component)

    return all_files


def clean_all_files_properties():
    all_files = []

    dirnames = get_all_dirnames()
    dirnames = list(set(dirnames))

    for dirname in dirnames:
        sub_all_files = get_all_pdf_files(dirname)
        all_files.extend(sub_all_files)

    all_files = list(set(all_files))
    for file in all_files:
        print("Properties-cleaned: ", file)
        clean_pdf_file_properties(file)


if __name__ == "__main__":
    print("Current Directory: ", current_directory)
    scheduler(clean_all_files_properties)