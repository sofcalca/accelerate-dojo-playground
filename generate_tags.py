import subprocess

commits_metadata = [
    {
        "date": "2021-03-31T11:15:00",
        "message": "message",
        "tags": [
            {
                "name": "s1.0.0",
                "date": "2021-04-01T16:15:00"
            },
            {
                "name": "p1.0.0",
                "date": "2021-04-05T10:15:00"
            }
        ]
    },
    {
        "date": "2021-04-02T14:15:00",
        "message": "message",
        "tags": []
    },
    {
        "date": "2021-04-06T12:15:00",
        "message": "message",
        "tags": []
    },
    {
        "date": "2021-04-08T12:10:00",
        "message": "message",
        "tags": [
            {
                "name": "s1.1.0",
                "date": "2021-04-08T14:15:00"
            }
        ]
    },
    {
        "date": "2021-04-12T09:46:00",
        "message": "message",
        "tags": []
    },
    {
        "date": "2021-04-14T16:15:00",
        "message": "message",
        "tags": [
            {
                "name": "s1.2.0",
                "date": "2021-04-15T17:15:00"
            },
            {
                "name": "p1.2.0",
                "date": "2021-04-19T09:45:00"
            }
        ]
    },
    {
        "date": "2021-04-16T17:15:00",
        "message": "message",
        "tags": []
    },
    {
        "date": "2021-04-19T14:25:00",
        "message": "message",
        "tags": []
    },
    {
        "date": "2021-04-21T10:02:00",
        "message": "message",
        "tags": [
            {
                "name": "s1.3.0",
                "date": "2021-04-22T16:25:00"
            },
            {
                "name": "p1.3.0",
                "date": "2021-04-26T10:05:00"
            }
        ]
    },
    {
        "date": "2021-04-23T11:15:00",
        "message": "message",
        "tags": []
    },
    {
        "date": "2021-04-26T13:05:00",
        "message": "message",
        "tags": [
            {
                "name": "p1.3.1",
                "date": "2021-04-26T13:35:00"
            }
        ]
    },
    {
        "date": "2021-04-26T17:55:00",
        "message": "message",
        "tags": [
            {
                "name": "p1.3.2",
                "date": "2021-04-26T18:35:00"
            }
        ]
    },
    {
        "date": "2021-04-28T15:55:00",
        "message": "message",
        "tags": [
            {
                "name": "s1.4.0",
                "date": "2021-04-29T15:35:00"
            }
        ]
    },
    {
        "date": "2021-04-30T10:12:00",
        "message": "message",
        "tags": []
    },
]


def create_tag_command(tag: str):
    tag_commit = f'''git tag -a {tag} -m "{tag}"'''
    return tag_commit.split()


def create_commit_command(date: str, message: str):
    commit_with_date = f'''git commit --allow-empty -m"{message}" --date "{date}"'''
    return commit_with_date.split()


if __name__ == '__main__':
    for commit in commits_metadata:
        git_env = {
            'GIT_COMMITTER_DATE': commit["date"],
            'GIT_COMMITTER_NAME': 'skooler',
            'GIT_COMMITTER_EMAIL': 'skooler@octo.com'
        }
        commit_command = create_commit_command(commit["date"], commit["message"])
        subprocess.call(commit_command, env=git_env)

        for tag in commit["tags"]:
            git_env = {
                'GIT_COMMITTER_DATE': tag["date"],
                'GIT_COMMITTER_NAME': 'skooler',
                'GIT_COMMITTER_EMAIL': 'skooler@octo.com'
            }
            tag_command = create_tag_command(tag["name"])
            subprocess.call(tag_command, env=git_env)
