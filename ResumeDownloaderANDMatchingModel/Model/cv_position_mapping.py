import os
import json


# get all chile professions
child_prof = os.listdir("../Files")
# print(child_prof)

# save child professions to json file
def save_child_profs_table():
    with open("./Relations/child_prof.json", "w") as outfi:
        json.dump({"child prof": child_prof}, outfi)
# save_child_profs_table()

# save parent professions to json file
def save_parent_profs_table():
    with open("./Relations/parent_child_prof_map.json", "r") as infi:
        p_c_map = json.load(infi)
        print(list(p_c_map.keys()))
        with open("./Relations/parent_prof.json", "w") as outfi:
            json.dump({"parent prof": list(p_c_map.keys())}, outfi)
# save_parent_profs_table()

# save specific position cv sample with specific overviews (e.g., position overview, company overview) to json file
def save_company_position_overview_map(overview_type):
    with open("./Relations/child_prof.json", "r") as infi:
        json_obj = json.load(infi)
        child_profs = json_obj["child prof"]
    position_overview_mapping = {}
    parent_folder = "../Files"
    for child_prof in child_profs:
        base_folder = os.path.join(parent_folder, child_prof)
        text_cv_folder = os.path.join(base_folder, "text_cv")
        overview_folder = os.path.join(base_folder, overview_type)
        result = os.path.isdir(overview_folder)
        if result:  # this means, there are specific positions in this child profession having position overviews
            # get txt positions
            txt_cv = os.listdir(text_cv_folder)
            position_names = [position.split(".")[0].strip() for position in txt_cv]
            # print(position_names)
            overviews = os.listdir(overview_folder)
            overviews = [overview.split(".")[0] for overview in overviews]
            for position in position_names:
                if position in overviews:
                    # position_overview_mapping[child_prof + "/" + position] = True
                    if position_overview_mapping.get(child_prof):
                        position_overview_mapping[child_prof][position] = True
                    else:
                        position_overview_mapping[child_prof] = {position: True}
                else:
                    # position_overview_mapping[child_prof + "/" + position] = False
                    if position_overview_mapping.get(child_prof):
                        position_overview_mapping[child_prof][position] = False
                    else:
                        position_overview_mapping[child_prof] = {position: False}

    print(position_overview_mapping)
    overview_type = overview_type.strip().replace(" ", "_").lower()
    with open(f"./Relations/{overview_type}_mapping.json", "w") as outfi:
        json.dump(position_overview_mapping, outfi)
# save_company_position_overview_map("Position Overview")

