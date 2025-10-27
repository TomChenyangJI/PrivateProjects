from component import convert_txt_to_pdf, copy_files_to_another_folder
import os


os.makedirs("../job_descriptions_pdf", exist_ok=True)
os.makedirs('../job_descriptions_pdf/mannual_intervene', exist_ok=True)


if __name__ == "__main__":
    files = os.listdir("../job_descriptions_en")
    for file in files:
        # print(file)
        try:
            if os.path.isfile(f"../job_descriptions_en/{file}") and file.endswith("txt"):
                convert_txt_to_pdf(f"../job_descriptions_en/{file}", file)
        except Exception as e:
            copy_files_to_another_folder(f"../job_descriptions_en/{file}")
            print(file)
            print(e)
            continue

