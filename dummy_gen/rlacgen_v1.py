import pandas as pd
import random

def generate_rlac_class_excel_file(
    num_rows_list,
    class_code_prefixes,
    class_name_prefix,
    roles,
    num_attendees,
    class_days,
    class_time_pairs,
    times_per_week,
    rlac,
):
    # Read email addresses from first Excel file
    df1 = pd.read_excel("data_dummy_users.xlsx")
    email_addresses = df1.loc[df1["role"].isin(roles), "email"].tolist()

    # Generate dummy data for classes
    data = {
        "class_code": [],
        "class_name": [],
        "class_day": [],
        "class_start_time": [],
        "class_end_time": [],
        "attendees": [],
    }
    used_times = {}
    class_attendees = {}
    for num_rows, class_code_prefix in zip(num_rows_list, class_code_prefixes):
        for i in range(num_rows):
            class_code = f"{class_code_prefix}{i+1}"
            if class_code not in class_attendees:
                # Filter email addresses based on the "student" role
                filtered_email_addresses = df1.loc[
                    df1["role"] == "student", "email"
                ].tolist()

                class_attendees[class_code] = random.sample(
                    filtered_email_addresses,
                    min(num_attendees, len(filtered_email_addresses)),
                )

                # Filter email addresses based on the "dosen" role
                filtered_email_addresses = df1.loc[
                    df1["role"] == "dosen", "email"
                ].tolist()
                # Take one random email address from the filtered email addresses
                additional_attendee = random.choice(filtered_email_addresses)
                # Append the additional attendee to the existing class_attendees list
                class_attendees[class_code].append(additional_attendee)
            attendees = class_attendees[class_code]

            for _ in range(times_per_week):
                day = random.choice(class_days)
                available_times = [
                    start_time
                    for start_time, _ in class_time_pairs
                    if (class_code, day, start_time) not in used_times
                ]
                if not available_times:
                    continue
                start_time = random.choice(available_times)
                end_time = next(
                    end_time
                    for start, end_time in class_time_pairs
                    if start == start_time
                )
                used_times[(class_code, day)] = used_times.get((class_code, day), 0) + 1
                data["class_code"].append(class_code)
                data["class_name"].append(f"{class_name_prefix}{class_code}{i+1}")
                data["class_day"].append(day)
                data["class_start_time"].append(start_time)
                data["class_end_time"].append(end_time)
                data["attendees"].append(", ".join(attendees))
    df2 = pd.DataFrame(data)
    df2.to_excel("data_dummy_rlac_class.xlsx", index=False)

    print("RLAC Class Generated Successfully")


# Example usage: generate 5 rows for the first class code prefix and 5 rows for the second class code prefix with the class name prefix 'Dummy Class', roles ['student', 'teacher'], 5 attendees per class,
# possible class days ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'], possible class time pairs [('9:00:00', '12:00:00'), ('13:00:00', '16:00:00')], and 2 times per week for each class
generate_rlac_class_excel_file(
    [1, 1, 1, 1, 1, 1, 1],
    ["MATH", "IDIS", "RHET", "THEO", "HIST", "PHIL"],
    "",
    ["student", "dosen"],
    30,
    ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"],
    [("8:00:00", "10:00:00"), ("10:00:00", "12:00:00"), ("13:00:00", "16:00:00"), ("16:00:00", "18:00:00"), ("19:00:00", "21:00:00")],
    2,
)

