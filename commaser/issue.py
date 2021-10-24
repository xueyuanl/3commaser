import json
import os

import requests


def edit_issue(body, number=1, title=None, milestone=None, labels=None, assignees=None):
    url = 'https://api.github.com/repos/xueyuanl/3commaser/issues/{}'.format(number)

    headers = {'Content-Type': 'application/json', 'Authorization': 'token ' + os.getenv('ACCESS_TOKEN')}
    request_body = {'body': body}
    result = requests.patch(url=url, json=request_body, headers=headers)

    j_str = result.text
    issue_obj = json.loads(j_str)
    print(issue_obj)
    return issue_obj
