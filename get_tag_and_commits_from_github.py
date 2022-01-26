import os
from datetime import datetime, timedelta
from statistics import mean
from typing import List, NamedTuple

import requests
from dotenv import load_dotenv

Commit = NamedTuple("Commit", [("sha", str), ("datetime", datetime)])
Tag = NamedTuple(
    "Tag",
    [("name", str), ("datetime", datetime), ("commits", List[Commit])],
)


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


def get_all_tags_with_commits(response) -> List[Tag]:
    return [
        Tag(
            edge["tag"]["name"],
            datetime.strptime(
                edge["tag"]["target"]["tagger"]["date"], "%Y-%m-%dT%H:%M:%S%z"
            ),
            [
                Commit(
                    commit["oid"],
                    datetime.strptime(commit["committedDate"], "%Y-%m-%dT%H:%M:%S%z"),
                )
                for commit in edge["tag"]["target"]["target"]["history"]["nodes"]
            ],
        )
        for edge in response["data"]["repository"]["tags"]["edges"]
    ]


def retrieve_hotfixes_tags(tags: List[Tag]) -> List[Tag]:
    return [tag for tag in tags if not tag.name.endswith("0")]


def compute_mean_time_to_repair(tags: List[Tag]) -> timedelta:
    span_between_hotfix_prod = [
        (tag.datetime - tag.commits[-1].datetime).total_seconds() for tag in tags
    ]
    return timedelta(seconds=mean(span_between_hotfix_prod))


def main():
    query = get_query_from_file("graphql_tag_and_commits_query.txt")
    response = execute_query(query)
    tags = get_all_tags_with_commits(response)
    hotfixes_tags = retrieve_hotfixes_tags(tags)
    mean_time_to_repair = compute_mean_time_to_repair(hotfixes_tags)
    print(f"{mean_time_to_repair = !s}")


if __name__ == "__main__":
    load_dotenv()
    main()
