import os.path
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from util.classes import GoogleTask
from util.func import get_config_file

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/tasks"]

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(get_config_file("token.json")):
        creds = Credentials.from_authorized_user_file(get_config_file("token.json"), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                get_config_file("credentials.json"), SCOPES
            )
            creds = flow.run_local_server(port=60968)
        # Save the credentials for the next run
        with open(get_config_file("token.json"), "w") as token:
            token.write(creds.to_json())

    return creds


def get_task_list():
    service = build("tasks", "v1", credentials=get_credentials())
    task_lists = service.tasklists().list().execute()

    remarkable_list = next(filter(lambda l: l["title"] == "Remarkable", task_lists['items']), None)
    if remarkable_list is None:
        remarkable_list = service.tasklists().insert(body={"title": "Remarkable"}).execute()

    return remarkable_list


def get_google_tasks() -> List[GoogleTask]:
    service = build("tasks", "v1", credentials=get_credentials())
    task_list = get_task_list()

    tasks = []

    tasks_req = service.tasks().list(tasklist=task_list['id'], showCompleted=False, showHidden=False)
    tasks_resp = tasks_req.execute()

    while tasks_resp is not None:
        for task in tasks_resp['items']:
            tasks.append(task)

        if 'nextPageToken' in tasks_resp:
            tasks_req = service.tasks().list_next(previous_request=tasks_req, previous_response=tasks_resp)
            tasks_resp = tasks_req.execute()
        else:
            tasks_resp = None

    return list(
        map(lambda task: GoogleTask(id=task['id'], parent=task['parent'] if 'parent' in task else None,
                                    status=task['status'],
                                    title=task['title']), tasks))


def mark_complete(tasks: List[str]):
    if len(tasks) == 0:
        return

    service = build("tasks", "v1", credentials=get_credentials())

    task_list = get_task_list()

    for id in tasks:
        service.tasks().update(tasklist=task_list['id'], task=id, body={"id": id, "status": "completed"}).execute()
