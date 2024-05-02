import json

with open("json_files/questions.json", "r") as file:
    all_questions = json.load(file)

with open("json_files/valid_responses.json", "r") as file:
    all_valid_responses = json.load(file)


def ask_user():
    user_responses={}
    for question in all_questions:
        options = "\n".join(all_questions[question][1])
        valid_responses=all_valid_responses[0:len(all_questions[question][1])]
        val=''
        while val not in valid_responses:
            val=input(f"{all_questions[question][0]} \n Please select one of the following options: \n {options}")
            if val not in valid_responses:
                print(f"please make sure you type {', '.join(valid_responses[0:-1])} or {valid_responses[-1]}")
            else:
                user_responses[question]=(val, all_questions[question])
    return user_responses
