import os


sub_files = os.listdir("job_descriptions_en")

for file in sub_files:
    if os.path.isfile(f"./job_descriptions_en/{file}"):
        print(file)