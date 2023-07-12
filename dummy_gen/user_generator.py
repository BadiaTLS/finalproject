import pandas as pd
import random

def generate_excel_file(filename, num_rows_list, username_prefixes, role_list, name_role_list, major_list):
    data = {"username": [], "name": [], "email": [], "role": [], "gender":[], "major":[]}
    for num_rows, username_prefix, role, name_role, major in zip(
        num_rows_list, username_prefixes, role_list, name_role_list, major_list
    ):
        data["username"].extend([f"{username_prefix}{i+1}" for i in range(num_rows)])
        data["email"].extend(
            [f"{username_prefix}{i+1}@example.com" for i in range(num_rows)]
        )
        data["role"].extend([role] * num_rows)
        genders = random.choices(["male", "female"], k=num_rows)  # Randomly select gender values
        data["gender"].extend(genders)
        if role in ["dosen", "dininghall"]:
            data["major"].extend(["-"] * num_rows)
            data["name"].extend([name_role] * num_rows)
        else:
            data["name"].extend([f"{name_role} {username_prefix.upper()} {i+1}" for i in range(num_rows)])
            data["major"].extend([f"{major}"] * num_rows)
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

    print('User Generated Successfully')


# Example usage: generate 5 rows for the first combination of username prefix and name/role with the name/role 'Student', and 3 rows for the second combination with the name/role 'Dining Hall Staff'
generate_excel_file(
    "data_dummy_users.xlsx",
    [5, 5, 5, 5, 5, 5, 5, 3],
    [
        "ibda", "iee", "cfp", "asd", "bms", "scce", "dosen", "dininghall"
        ],
    [
        "student", "student", "student", "student", "student", "student", "dosen", "dininghall"
        ],
    [
        "Student", "Student", "Student", "Student", "Student", "Student", "Dosen", "Dining Hall"
        ],
    ["ibda", "iee", "cfp", "asd", "bms", "scce", "-", "-"],
)
