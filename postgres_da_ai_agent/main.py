import os
from dotenv import load_dotenv
from modules.db import PostgresManager
from modules import llm

load_dotenv()

assert os.getenv("POSTGRES_DATABASE_URL") is not None, "POSTGRES_DATABASE_URL not found in .env file"
assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY not found in .env file"

DB_URL = os.getenv("POSTGRES_DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    # parse arguments using argparse

    with PostgresManager(DB_URL) as db:
        db.connect_with_url()
        users = db.get_all("users")
        print(users)

        # call db_manger.get_talbe_definitions_for_prompt() to get tables in prompt ready format

        # create two blank calls to llm.add_cap_ref() that update our current prompt passed in form cli

        # call llm.prompt() to get prompt response variable

        # parse sql response from prompt_response using SQL_QUERY_DELIMITER '__________'

        # call db_manager.run_sql() with the parsed sql

    pass

if __name__ == "__main__":
    main()