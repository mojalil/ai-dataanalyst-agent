import os
from dotenv import load_dotenv
from modules.db import PostgresManager
from modules import llm

load_dotenv()

assert os.getenv("POSTGRES_DATABASE_URL") is not None, "POSTGRES_DATABASE_URL not found in .env file"
assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY not found in .env file"

DB_URL = os.getenv("POSTGRES_DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", help="The prompt for the AI")
    args = parser.parse_args()

    with PostgresManager(DB_URL) as db:
        db.connect_with_url()
        users = db.get_all("users")
        print(users)

        table_definitions = db.get_table_definition_for_prompt()

        prompt = llm.add_cap_ref(args.prompt, "Here are the table definitions:", "TABLE_DEFINITIONS", table_definitions)
        prompt = llm.add_cap_ref(prompt, "Here are the users:", "USERS", str(users))

        prompt_response = llm.prompt(prompt)

        sql_queries = prompt_response.split('__________')

        for sql_query in sql_queries:
            db.run_sql(sql_query)

if __name__ == "__main__":
    main()
