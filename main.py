import os
from datetime import datetime
from typing import List, NamedTuple

import requests
from dotenv import load_dotenv

Tag = NamedTuple("Tag", [("name", str), ("datetime", datetime)])
Commit = NamedTuple("Commit", [("sha", str), ("datetime", datetime)])


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


def parse_datetime(field: str) -> datetime:
    return datetime.strptime(field, "%Y-%m-%dT%H:%M:%S%z")


def parse_response_for_tags(response: dict) -> List[Tag]:
    raise NotImplementedError()


def parse_response_for_commits(response: dict) -> List[Commit]:
    raise NotImplementedError()


def compute_deployment_frequency():
    raise NotImplementedError()


def compute_change_failure_rate():
    raise NotImplementedError()


def compute_mean_time_to_repair():
    raise NotImplementedError()


def compute_lead_time():
    raise NotImplementedError()


def main():
    tags_query = get_query_from_file("graphql_tag_query.txt")
    tags_response = execute_query(tags_query)
    print(tags_response)

    commits_query = get_query_from_file("graphql_commits_query.txt")
    commits_response = execute_query(commits_query)
    print(commits_response)


if __name__ == "__main__":
    load_dotenv()
    main()
