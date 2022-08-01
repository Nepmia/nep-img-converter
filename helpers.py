import argparse
import os
import dotenv
import logging as log

dotenv.load_dotenv()

log_base_dir = os.getenv("LOG_BASE_DIR")

# Arg setup
parser = argparse.ArgumentParser()


# Prompt setup
basic_answers =  {
        "yes" : True,
        "y" : True,
        "no" : False,
        "n" : False,
}

basic_no_default = "[y/N]"
basic_yes_default = "[Y/n]"

def verify_logs() -> bool:  
    """Check if log folder exists

    Returns:
        bool: If log exist 
    """
    if not os.path.exists(log_base_dir):
        return False
    return True

def create_log_folder():
    """Create the log folder
    """
    os.mkdir(log_base_dir)    

def user_prompt(valid_answers:dict, question:str, display_answer:str, default:str = None) -> str: 
    """CLI user interaction method. Allow to ask questions to the user and execute something with the answer.
    Args:
        valid_answers (dict): a dict of the valid answers (yes : true, no : false, y : true, n : false, maybe : maybe, idk : thing).
        question (str): The question you ask to the user.
        display_answer (str): The possible answers you'll show to the user (like: [Y/n]).
        default (str, optional): Default answer that will be given if the user just press enter without entering any answer, is optional. Defaults to None.
    Returns:
        str: The value of the key of valid_answers that the user gave. 
    """
    log.info(f"Prompting question: {question} to the user with available answers: {display_answer}")
    log.info("Awaiting user answer.")

    # Always print to the terminal
    print(question)
    print("Please answer with:", display_answer)
    while True:
        user_answer = input().lower()
        if user_answer == "" and default is not None:
            return default
        elif user_answer in valid_answers:
            return valid_answers[user_answer]
        else:
            log.info("User entered incorect info, re-prompting")
            print("Incorect answer.", "Please retry. \n")
            print(question)
            print("Please answer with:", display_answer)
