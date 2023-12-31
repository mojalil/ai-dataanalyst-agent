import os
from dotenv import load_dotenv
from postgres_da_ai_agent.modules.db import PostgresManager
from postgres_da_ai_agent.modules import llm
import re

load_dotenv()

assert os.getenv("POSTGRES_DATABASE_URL") is not None, "POSTGRES_DATABASE_URL not found in .env file"
assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY not found in .env file"

DB_URL = os.getenv("POSTGRES_DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

POSTGRES_TABLE_DEFINITIONS_CAP_REF = "TABLE_DEFINITIONS"
POSTGRES_SQL_QUERY_CAP_REF = "SQL_QUERY"
TABLE_RESPONSE_FORMAT_CAP_REF = "TABLE_RESPONSE_FORMAT"

SQL_DELIMITER = "__________"

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", help="The prompt for the AI")
    args = parser.parse_args()

    if not args.prompt:
        print("Please provide a prompt with --prompt")
        return
    
    print("args.prompt: ", args.prompt)

    with PostgresManager(DB_URL) as db:

        db.connect_with_url()

        table_definitions = db.get_table_definition_for_prompt()

        print("table_definitions: ", table_definitions)

        prompt = llm.add_cap_ref(
            args.prompt, f"Use the {POSTGRES_TABLE_DEFINITIONS_CAP_REF} to satisfy the database query.", 
            POSTGRES_TABLE_DEFINITIONS_CAP_REF, 
            table_definitions)
        
        print("prompt v2: ", prompt)
        
        prompt = llm.add_cap_ref(
            prompt, f"Respond in this format {TABLE_RESPONSE_FORMAT_CAP_REF}", 
            TABLE_RESPONSE_FORMAT_CAP_REF, 
            f"""<explanation of the sql query>
            {SQL_DELIMITER}
            <sql query exclusivly as raw text>
            """)

        prompt_response = llm.prompt(prompt)

        print("prompt_response: ", prompt_response)

        # Use regex to find the SQL block, ignoring case
        try:
            # This regex pattern looks for a SQL code block, ignoring the case of the 'sql' marker
            sql_query_match = re.search(r'```[ \t]*sql(.*?)```', prompt_response, re.DOTALL | re.IGNORECASE)
            if sql_query_match:
                sql_query = sql_query_match.group(1).strip()  # Extract the SQL query
            else:
                raise ValueError("SQL code block not found in the response.")
        except ValueError as e:
            print(e)
            return

        print("sql_query: ", sql_query)


        result = db.run_sql(sql_query)

        print("------ POSTGRES DATA ANALYTICS AI AGENT RESPONSE ------")

        print(result)

if __name__ == "__main__":
    main()
