from dataclasses import dataclass


class RMCloudFile:
    def __init__(self, name, is_dir):
        self.name = name
        self.is_dir = is_dir

    def is_directory(self):
        return self.is_dir

    def is_file(self):
        return not self.is_dir

    def __str__(self):
        return f"RMCloudFile(name: {self.name}, type: {"DIRECTORY" if self.is_dir else "FILE"})"

    def __repr__(self):
        return f"RMCloudFile(name: {self.name}, type: {"DIRECTORY" if self.is_dir else "FILE"})"
