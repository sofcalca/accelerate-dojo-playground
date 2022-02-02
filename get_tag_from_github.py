import os
from datetime import datetime, timedelta
from statistics import mean
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


def get_all_commits(response) -> List[Commit]:
    return [
        Commit(
            edge["node"]["oid"],
            datetime.strptime(edge["node"]["committedDate"], "%Y-%m-%dT%H:%M:%S%z"),
        )
        for edge in response["data"]["repository"]["defaultBranchRef"]["target"][
            "history"
        ]["edges"]
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


def compute_lead_time(commits: List[Commit], tags: List[Tag]) -> timedelta:
    production_tags = retrieve_production_tags(tags)
    production_tags.reverse()
    commits_already_processed = []
    delta_sum = 0

    for tag in production_tags:
        tag_date = tag.datetime

        for commit in commits:
            if commit.datetime < tag_date and commit not in commits_already_processed:
                delta_sum += (tag_date - commit.datetime).total_seconds()
                commits_already_processed.append(commit)

    return timedelta(seconds=delta_sum / len(commits))


def main():
    query_tags = get_query_from_file("graphql_tag_query.txt")
    response_tags = execute_query(query_tags)
    tags = get_all_tags(response_tags)

    change_failure_rate = compute_change_failure_rate(tags)
    print(f"{change_failure_rate = }")

    deployment_frequency = compute_deployment_frequency(tags)
    print(f"{deployment_frequency = !s}")

    query_commits = get_query_from_file("graphql_commits_query.txt")
    response_commits = execute_query(query_commits)
    commits = get_all_commits(response_commits)

    lead_time = compute_lead_time(commits, tags)
    print(f"{lead_time = !s}")


if __name__ == "__main__":
    load_dotenv()
    main()
