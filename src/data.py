import pandas as pd
from paths import DATA_FILE

df = pd.read_csv(DATA_FILE)

def apply_filter(age_range, gender, first_generation, family_income_level, course_type, study_mode, semester):
    d = df
    if gender:
        d = d[d["gender"] == gender]
    if first_generation is not None:
        d = d[d["first_generation"] == first_generation]
    if family_income_level:
            d = d[d["family_income_level"] == family_income_level]
    if course_type:
            d = d[d["course_type"] == course_type]
    if study_mode:
            d = d[d["study_mode"] == study_mode]
    if semester:
            d = d[d["semester"] == semester]
    d = d[d["age"].between(*age_range)]

    return d







