from PyPDF2 import PdfMerger, PdfReader, PdfWriter

while True:
    # Specify the PDF file paths
    pdf_file1 = input("Please input the pdf absoulate path:\n")
    # pdf_file2 = 't1.pdf'
    pdf_file1 = pdf_file1.strip()
    output_file = pdf_file1

    # Initialize the PdfMerger
    merger = PdfMerger()

    # Add the PDF files
    merger.append(pdf_file1)
    # merger.append(pdf_file2)

    # Merge and write to an output file
    merger.write(output_file)
    merger.close()

    # Modify metadata
    reader = PdfReader(output_file)
    writer = PdfWriter()

    # print("  ---- ", pdf_version)
    # Copy all pages from the reader to the writer
    for page in reader.pages:
        writer.add_page(page)

    # pdf_version = input("Please input the version of the output pdf file, e.g., 1.3, 1.4. \nThe default version is 1.4 when you do not type in anything:").strip()
    # # print("pdf_version is ", pdf_version)
    # # writer.pdf_version = pdf_version
    # pdf_version = "1.4" if pdf_version.strip() == "" else pdf_version.strip()

    # Edit metadata
    metadata = reader.metadata  # Read existing metadata
    metadata.update({
        '/Producer': '',  # Set a custom producer
        # '/Author': 'xxx xxx',  # Optional: Update or add other metadata fields
    })
    writer.add_metadata(metadata)

    # Write the final file with updated metadata
    with open(output_file, "wb") as f_out:
        writer.write(f_out)



    # Read the file
    # with open(output_file, 'rb') as file:
    #     content = file.read()
    #     # print(str(content)[7:10], "  --- test")

    # current_ver = str(content)[7:10]
    # current_ver = f"%PDF-{current_ver}"
    # current_ver = "b'" + current_ver + "'"

    # sub_s = f'%PDF-{pdf_version}'
    # sub_s = "b'" + sub_s + "'"

    # # Replace the version in the header
    # content = content.replace(eval(current_ver), eval(sub_s), 1)  # Adjust versions as needed

    # # Write back to a new file
    # with open(output_file, 'wb') as file:
    #     file.write(content)

    # print("PDF version updated manually.")


    print(f"PDF Producer updated in {output_file}")
