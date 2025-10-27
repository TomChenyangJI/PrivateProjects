import json

# 10
with open("../Relations/position_overview_mapping.json", "r") as infi:
    json_obj = json.load(infi)
    child_professions = json_obj.keys()
    ten = []
    for child_profession in child_professions:
        # samples of one profession
        positions = json_obj.get(child_profession)

        """
        [cv_sample_path, overview_path]
        """
        for position in positions:
            if positions.get(position):
                # print(position)
                ten.append([f"{child_profession}/text_cv/{position}", f"{child_profession}/Position Overview/{position}"])
    with open("../data/10.json", "w") as outfi:
        json.dump(ten, outfi)


# 9
with open("../Relations/position_overview_mapping.json", "r") as infi:
    json_obj = json.load(infi)
    child_professions = json_obj.keys()
    nine = []
    for child_profession in child_professions:
        # cv samples
        cv_samples = json_obj.get(child_profession)
        true_samples = [key for key in cv_samples if (cv_samples.get(key))]
        false_samples = [key for key in cv_samples if (not cv_samples.get(key))]
        for false_sample in false_samples:
            for true_sample in true_samples:
                nine.append([f"{child_profession}/text_cv/" + false_sample, f"{child_profession}/Position Overview/" + true_sample])
        """
        [cv_sample_path, overview_path]
        """
    with open("../data/9.json", "w") as outfi:
        json.dump(nine, outfi)


# 8
with open("../Relations/parent_child_prof_map.json", "r") as infi:
    with open("../Relations/position_overview_mapping.json") as position_overview_infi:
        child_profession_overview_js_obj = json.load(position_overview_infi)
        eight = []
        js_obj = json.load(infi)
        parent_professions = js_obj.keys()
        for parent_profession in parent_professions:
            true_overviews = []
            false_overviews = []
            child_professions = js_obj.get(parent_profession)  # Game Designer
            for child_profession in child_professions:
                true_overviews_sub = []
                false_overviews_sub = []
                for other_child_profession in child_professions:
                    if other_child_profession != child_profession:
                        other_child_profession_overviews = child_profession_overview_js_obj.get(other_child_profession)
                        if other_child_profession_overviews is not None:
                            for overview in other_child_profession_overviews:
                                overview_path = f"{other_child_profession}/Position Overview/{overview}"
                                if other_child_profession_overviews.get(overview):
                                    """
                                            [cv_sample_path, overview_path]
                                            """
                                    true_overviews_sub.append(overview_path)
                position_overview_map = child_profession_overview_js_obj.get(child_profession)
                if position_overview_map is not None:
                    for position in position_overview_map.keys():
                        for overview in true_overviews_sub:
                            eight.append([f"{child_profession}/text_cv/{position}", overview])
        with open("../data/8.json", "w") as outfi:
            json.dump(eight, outfi)


# 7
with open("../Relations/parent_child_prof_map.json", "r") as parent_child_map_infi:
    with open("../Relations/position_overview_mapping.json", "r") as position_overview_map_infi:
        par_child_map = json.load(parent_child_map_infi)
        position_overview_map = json.load(position_overview_map_infi)

        seven = []

        par_professions = par_child_map.keys()
        for par_profession in par_professions:
            child_professions = par_child_map.get(par_profession)
            true_overviews = []
            for child_profession in child_professions:
                overviews = position_overview_map.get(child_profession)
                if overviews is not None:
                    samples = overviews.keys()
                    for sample in samples:
                        if overviews.get(sample):
                            true_overviews.append(f"{child_profession}/Position Overview/{sample}")
            other_profession_positions = []
            for other_par_profession in par_professions:
                if other_par_profession != par_profession:
                    # sample/position
                    other_child_professions = par_child_map.get(other_par_profession)
                    for other_profession in other_child_professions:
                        samples = position_overview_map.get(other_profession)
                        if samples is not None:
                            sample_positions = list(samples.keys())
                            sample_positions = [f"{other_profession}/text_cv/{ele}" for ele in sample_positions]
                            other_profession_positions.extend(sample_positions)
            for position in other_profession_positions:
                for overview in true_overviews:
                    seven.append([position, overview])

        with open(f"../data/7.json", "w") as outfi:
            json.dump(seven, outfi)



