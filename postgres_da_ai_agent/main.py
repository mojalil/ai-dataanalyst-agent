import os
from dotenv import load_dotenv
from modules.db import PostgresManager

load_dotenv()

assert os.getenv("POSTGRES_DATABASE_URL") is not None, "POSTGRES_DATABASE_URL not found in .env file"
assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY not found in .env file"

DB_URL = os.getenv("POSTGRES_DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    # parse arguments using argparse

    # parser = argparse.ArgumentParser(description='Process some integers.')
    # args = parser.parse_args()
    # print(args)


    # connect to db using statement and create a db manager

    with PostgresManager(DB_URL) as db:
        db.connect_with_url()
        users = db.get_all("users")
        print(users)

    # call db_manager.get_table_definition_for_prompt() to get the tables in prompt form

    # create two black calls to llm.add_cap_ref and update that update our current prompt from the cli

    pass

if __name__ == "__main__":
    main()