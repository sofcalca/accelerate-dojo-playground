import os

import requests
from dotenv import load_dotenv


def get_query_from_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def execute_query(query: str):
    headers = {
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://api.github.com/graphql", json={"query": query}, headers=headers
    )
    response.raise_for_status()
    response_json = response.json()
    print(response_json)


def main():
    query = get_query_from_file("graphql_tag_query.txt")
    execute_query(query)


if __name__ == "__main__":
    load_dotenv()
    main()
