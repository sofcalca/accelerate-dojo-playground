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
    return response.json()


def get_all_tag_names(response) -> list:
    return [
        edge["tag"]["name"] for edge in response["data"]["repository"]["tags"]["edges"]
    ]


def compute_change_failure_rate(production_tags: list) -> float:
    hotfix_tags = [tag for tag in production_tags if not tag.endswith("0")]
    return len(hotfix_tags) / len(production_tags)


def main():
    query = get_query_from_file("graphql_tag_query.txt")
    response = execute_query(query)
    tags = get_all_tag_names(response)
    production_tags = [tag for tag in tags if "p" in tag]
    change_failure_rate = compute_change_failure_rate(production_tags)
    print(change_failure_rate)


if __name__ == "__main__":
    load_dotenv()
    main()
