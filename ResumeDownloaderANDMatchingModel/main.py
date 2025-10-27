import requests
from component import *
from config import *


# https://www.kickresume.com/en/help-center/finance-analyst-resume-samples/


if __name__ == "__main__":
    with open("professions.txt", "r") as infi:
        profs = infi.readlines()
        for prof in profs:
            prof = prof.strip()
            print("The Profession is : ", prof)
            # each profession has many samples
            trial = 0
            while trial < 3:
                try:
                    print("\tTrial: ", trial + 1)
                    get_profession_resume_samples(prof)
                except Exception as e:
                    print(e)
                    trial += 1
                else:
                    break
