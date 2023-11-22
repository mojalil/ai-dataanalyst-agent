import argparse
import psycopg2

def main():
    # parse arguments using argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    args = parser.parse_args()

    print(args)



    # connect to db using statement and create a db manager

    # call db_manager.get_table_definition_for_prompt() to get the tables in prompt form

    # create two black calls to llm.add_cap_ref and update that update our current prompt from the cli

    pass

if __name__ == "__main__":
    main()