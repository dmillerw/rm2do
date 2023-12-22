from pathlib import Path

import util.func
from remarkable.cloud import validate_rmapi_binary, download_rmapi_binary, invoke_rmapi, list_files, download_file

util.func.ensure_directories_exist()
download_file("/Google Tasks")

