import json
import logging
import os.path
import shutil
from typing import List, Dict

import click
from rmscene import read_blocks, SceneLineItemBlock

import util.func
from backend.google import get_credentials, mark_complete, get_google_tasks
from pdf import create_pdf
from remarkable.cloud import download_file, CloudAuth, upload_file, validate_rmapi_binary_exists, get_archive_name, \
    download_rmapi_binary, RmApiDownloadResponse, validate_rmapi_binary
from remarkable.notebook import get_draw_points
from util.classes import TaskData, XYCoordinate
from util.constants import RM_LETTER_WIDTH, RM_LETTER_HEIGHT, TEMP_DIRECTORY
from util.func import get_config_file, get_output_file


def get_and_extract(remote_directory: str = "/Folder", remote_file: str = "Google Tasks",
                    extract_dir: str = TEMP_DIRECTORY) -> bool:
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)

    seperator = "/" if not remote_directory.endswith("/") and not remote_file.endswith("/") else ""
    remote_path = remote_directory + seperator + remote_file

    click.echo(f"Downloading {remote_path}")

    if not download_file(remote_path):
        click.echo(click.style("Failed to download", fg='red'))
        return False

    click.echo(f"Extracting {remote_file}.zip to {extract_dir}")

    shutil.unpack_archive(f"{remote_file}.zip", extract_dir)
    os.remove(f"{remote_file}.zip")

    if not os.path.exists(TEMP_DIRECTORY):
        click.echo(click.style("Failed to extract", fg='red'))
        return False

    return True


def get_task_data(filename="tasks.json") -> TaskData | None:
    filename = get_config_file(filename)
    if not os.path.exists(filename):
        return None

    with open(filename, 'r') as f:
        return TaskData.from_json(f.read())


def save_task_data(tasks: TaskData, filename="tasks.json"):
    filename = get_config_file(filename)
    with open(filename, 'w') as f:
        f.write(tasks.to_json())


def get_completed_tasks(tasks: TaskData, points: Dict[int, List[XYCoordinate]]) -> List[str]:
    completed_tasks = set()
    for page in tasks.pages.keys():
        for task in tasks.pages[page]:
            for point in points[page]:
                if point.within_bounds(task.start, task.end):
                    completed_tasks.add(task.id)

    return list(completed_tasks)


def push():
    tasks = get_google_tasks()
    task_data = create_pdf(tasks)
    save_task_data(task_data)

    # if not upload_file(get_output_file("Google Tasks.pdf"), "/Folder", replace=True):
    # If the directory defined by remote_path doesn't exist, this will fail
    # TODO
    if not upload_file("Google Tasks.pdf", "/Folder", replace=True):
        click.echo(click.style("Failed to push pdf to Remarkable Cloud", fg="red"))
        return


def pull():
    tasks = get_task_data()
    if tasks is None:
        click.echo(click.style("Can't pull, no existing task data can be found.", fg="red"))
        return

    if not get_and_extract():
        #TODO This failing should kill the whole thing. What if we overwrite data?
        click.echo(click.style("Failed to download or extract the PDF from Remarkable Cloud", fg="red"))
        return

    points = get_draw_points()
    if len(points) == 0:
        click.echo(click.style("Failed to grab any data points from extracted file", fg="red"))
        return

    completed_tasks = get_completed_tasks(tasks, points)
    mark_complete(completed_tasks)


@click.command()
@click.argument('mode', type=click.Choice(['run', 'push', 'pull', 'setup-only']))
def run(mode):
    util.func.ensure_directories_exist()

    if not validate_rmapi_binary_exists():
        click.echo(f"Didn't find bin/rmapi, will try to download")
        download_response = download_rmapi_binary()

        if download_response == RmApiDownloadResponse.MissingArchitecture:
            click.echo("Wasn't able to find a version of rmapi that fits your system architecture")
            click.echo("If you believe this is in error, download it manually and place into 'bin/rmapi'")
            return

        if download_response == RmApiDownloadResponse.MissingFile:
            click.echo("We determined a version to download, but wasn't able to find it in the latest GitHub release")
            click.echo(f"Looked for '{get_archive_name()}'")
            click.echo("If you believe this is in error, download it manually and place into 'bin/rmapi'")
            return

        if not validate_rmapi_binary():
            click.echo("rmapi was retrieved, but isn't executing correctly")
            return

        click.echo("Success! rmapi successfully retrieved and functioning")

    # Ensure Google auth is setup correctly
    if not os.path.exists(get_config_file("credentials.json")):
        click.echo("You're missing the required 'credentials.json' file for Google Authentication")
        click.echo("Refer to 'https://developers.google.com/tasks/quickstart/python' for instructions")
        click.echo("* Ensure that 'http://localhost:60968' is setup as a valid redirection URL")
        click.echo("* Ensure the resulting 'credentials.json' file is placed inside the 'config/' directory")
        return

    # Try to grab creds early if the token.json isn't found to kickoff the oauth flow
    if not os.path.exists(get_config_file("token.json")):
        get_credentials()

    # Ensure we can connect to Remarkable cloud, or authenticate if possible
    auth = CloudAuth()
    if not auth.is_auth():
        click.echo("You're not authenticated with Remarkable Cloud...")
        click.echo("Get a pairing token from https://my.remarkable.com/device/desktop/connect")
        token = click.prompt("Token")
        click.echo("Thanks! Working on it...")
        auth.register_device(token)
        auth.renew_token()
        if not auth.is_auth():
            click.echo(click.style("Failed to authenticate with Remarkable...", fg='red'))
            return
        else:
            click.echo(click.style("Successfully authenticated with Remarkable!", fg='green'))

    if mode == "run" or mode == "pull":
        pull()
    if mode == "run" or mode == "push":
        push()

if __name__ == "__main__":
    run()
