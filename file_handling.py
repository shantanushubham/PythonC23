import csv
import json

USER_PATH = "/Users/shantanu/B/AirTribe/PythonC23/files/users.json"
CSV_PATH = "/Users/shantanu/B/AirTribe/PythonC23/files/users.csv"
CSV_FIELDS = ["name", "email", "age", "isAdmin"]


def read_users_from_file():
    with open(USER_PATH, "r") as file:  # r means we are opening the file to READ
        content = file.read()
        user_list: list = json.loads(content)
        return user_list


def add_user(user_dict):
    user_list = read_users_from_file()
    user_list.append(user_dict)
    content = json.dumps(user_list, indent=2)

    with open(USER_PATH, "w") as file:
        file.write(content)


def read_users_from_csv():
    with open(CSV_PATH, "r", newline="") as file:  # newline="" avoids extra blank rows
        reader = csv.DictReader(file)  # each row becomes a dict using the header row
        user_list = []
        for row in reader:
            user_list.append(
                {
                    "name": row["name"],
                    "email": row["email"],
                    "age": int(row["age"]),
                    "isAdmin": row["isAdmin"].lower() == "true",
                }
            )
        return user_list


def add_user_csv(user_dict):
    user_list = read_users_from_csv()
    user_list.append(user_dict)

    with open(CSV_PATH, "w", newline="") as file:  # w overwrites the whole file
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()  # writes name,email,age,isAdmin as the first row
        writer.writerows(user_list)


# read_users_from_file()
# add_user(
#     {
#         "name": "Aadityesh Jain",
#         "email": "aadityesh@example.com",
#         "age": 24,
#         "isAdmin": True,
#     }
# )

# print(read_users_from_csv())
add_user_csv(
    {
        "name": "Aadityesh Jain",
        "email": "aadityesh@example.com",
        "age": 24,
        "isAdmin": True,
    }
)
