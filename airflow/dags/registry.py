from sys import path
import yaml


class Registry:
    hospitals: list[dict[str, any]]

    def __init__(self) -> None:
        self.hospitals = {}

    def register(self) -> None:
        with open(f"{path[0]}/manifest.yaml", "r") as manifest_file:
            manifest = yaml.safe_load(manifest_file)
        self.hospitals = manifest["hospitals"]
