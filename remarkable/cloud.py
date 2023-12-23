import os.path
import platform
import shutil
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import List

import requests
from rmapy.api import Client

from remarkable.classes import RMCloudFile
from util.constants import BIN_DIRECTORY
from util.func import get_bin_file


class CloudAuth:
    def __init__(self):
        self.client = Client()

    def is_auth(self) -> bool:
        return self.client.is_auth()

    def register_device(self, token: str) -> bool:
        try:
            return self.client.register_device(token)
        except:
            return False

    def renew_token(self) -> bool:
        try:
            return self.client.renew_token()
        except:
            return False


def get_archive_name() -> str:
    system = platform.system()
    machine = platform.machine()

    if system == "Darwin":
        return "rmapi-macosx.zip"
    elif system == "Linux":
        if machine == "x86_64":
            return "rmapi-linuxx86-64.tar.gz"
    elif system == "Windows":
        if machine == "AMD64":
            return "rmapi-win64.zip"

    return ""


def get_rmapi_binary_path() -> str:
    if platform.system() == "Windows":
        return get_bin_file("rmapi.exe")
    else:
        return get_bin_file("rmapi")


def validate_rmapi_binary_exists() -> bool:
    return os.path.exists(get_rmapi_binary_path())


def validate_rmapi_binary() -> bool:
    if not validate_rmapi_binary_exists():
        return False

    output = invoke_rmapi(["version"])
    if output.returncode != 0:
        return False

    return True


def download_rmapi_binary() -> bool:
    archive = get_archive_name()
    if archive == "":
        print("Wasn't able to determine the appropriate version to download")
        return False

    latest_version = requests.get("https://api.github.com/repos/juruen/rmapi/releases/latest",
                                  headers={"X-GitHub-Api-Version": "2022-11-28"}).json()

    for asset in latest_version["assets"]:
        if asset["name"] == archive:
            archive_file = get_bin_file(archive)
            file_resp = requests.get(asset["browser_download_url"])
            with open(archive_file, 'wb') as f:
                f.write(file_resp.content)

            shutil.unpack_archive(archive_file, BIN_DIRECTORY)
            os.remove(archive_file)

            return True

    return False


def invoke_rmapi(args: List[str]) -> CompletedProcess[bytes]:
    if not isinstance(args, List):
        args = [args]
    args.insert(0, get_rmapi_binary_path())
    return subprocess.run(args, capture_output=True)


def list_files(remote_path: str) -> List[RMCloudFile]:
    remote_path = f"/{remote_path}" if not remote_path.startswith("/") else remote_path
    process = invoke_rmapi(["-ni", "ls", remote_path])
    if process.returncode != 0:
        return []

    output = []

    lines = process.stdout.decode().splitlines()
    for line in lines:
        if line.startswith("[f]"):
            output.append(RMCloudFile(line.split("\t")[1], False))
        elif line.startswith("[d]"):
            output.append(RMCloudFile(line.split("\t")[1], True))

    return output


def file_exists(remote_path: str) -> bool:
    output = invoke_rmapi(["stat", remote_path])
    return output.returncode == 0


def download_file(remote_path: str, local_path: str = ".") -> bool:
    filename = remote_path.split("/")[-1] + ".zip"
    # if os.path.isdir(local_path):
    #     local_path = os.path.join(local_path, filename)

    output = invoke_rmapi(["get", remote_path])
    if output.returncode != 0:
        if os.path.exists(filename):
            os.remove(filename)
        return False

    # shutil.move(get_bin_file(filename), local_path)

    return True


def upload_file(local_path: str, remote_dir: str, replace=False) -> bool:
    #TODO Need to re-think the args for this func

    # local_path = Path(local_path).absolute()
    filename = Path(local_path).stem

    if replace:
        remote_path = f"{remote_dir}/{filename}"
        # That'd be awkward...
        if remote_path != "/":
            delete_file(remote_path)

    output = invoke_rmapi(["-ni", "put", local_path, remote_dir])
    return output.returncode == 0


def delete_file(remote_path: str) -> bool:
    output = invoke_rmapi(["-ni", "rm", remote_path])
    return output.returncode == 0
