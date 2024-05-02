import random
import json

with open("prompts.json", "r") as file:
    all_prompts = json.load(file)

with open("valid_responses.json", "r") as file:
    all_valid_responses = json.load(file)

def create_prompt(question, val):
    prompt_word=random.choice(all_prompts[question][2][val])
    return prompt_word

def input_to_prompt():
    prompt_words=[]
    user_responses=[]
    for question in all_prompts:
        responses = "\n".join(all_prompts[question][1])
        valid_responses=all_valid_responses[0:len(all_prompts[question][1])]
        val=''
        while val not in valid_responses:
            val=input(f"{question} \n Please select one of the following options: \n {responses}")
            if val not in valid_responses:
                print(f"please make sure you type {', '.join(valid_responses[0:-1])} or {valid_responses[-1]}")
            else:
                user_responses.append(val)
                prompt_words.append(create_prompt(question, val))
    prompt_str=' '.join(prompt_words)
    return (user_responses, prompt_str)



# class PromptGenerator:
#     # NOTE: Don't forget to generate doc by doing <leader>c on the class name.

#     # Holds all the questions: key is the quetsion and value is the possible answers
#     question_dict = {}

#     # This will be the result
#     result = ''



#     def __str__(self):
#         return str(self.__dict__)
