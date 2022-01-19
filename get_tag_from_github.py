import os
from datetime import datetime, timedelta
from statistics import mean
from typing import List, NamedTuple

import requests
from dotenv import load_dotenv

Tag = NamedTuple("Tag", [("name", str), ("datetime", datetime)])


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


def get_all_tags(response) -> List[Tag]:
    return [
        Tag(
            edge["tag"]["name"],
            datetime.strptime(
                edge["tag"]["target"]["tagger"]["date"], "%Y-%m-%dT%H:%M:%S%z"
            ),
        )
        for edge in response["data"]["repository"]["tags"]["edges"]
    ]


def retrieve_production_tags(tags: List[Tag]) -> List[Tag]:
    return [tag for tag in tags if "p" in tag.name]


def compute_change_failure_rate(tags: List[Tag]) -> float:
    production_tags = retrieve_production_tags(tags)
    hotfix_tags = [tag for tag in production_tags if not tag.name.endswith("0")]
    return len(hotfix_tags) / len(production_tags)


def compute_deployment_frequency(tags: List[Tag]) -> timedelta:
    production_tags = retrieve_production_tags(tags)
    production_tags.reverse()

    span_between_deployments = [
        (tag.datetime - previous_tag.datetime).total_seconds()
        for previous_tag, tag in zip(production_tags, production_tags[1:])
    ]

    return timedelta(seconds=mean(span_between_deployments))


def main():
    query = get_query_from_file("graphql_tag_query.txt")
    response = execute_query(query)
    tags = get_all_tags(response)

    change_failure_rate = compute_change_failure_rate(tags)
    print(f"{change_failure_rate = }")

    deployment_frequency = compute_deployment_frequency(tags)
    print(f"{deployment_frequency = !s}")


if __name__ == "__main__":
    load_dotenv()
    main()
