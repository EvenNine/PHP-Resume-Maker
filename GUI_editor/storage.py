from __future__ import annotations
import json
import os
from typing import Any


class JsonStore:
    def __init__(self, workdir: str) -> None:
        self.workdir = os.path.abspath(workdir)

    def set_workdir(self, workdir: str) -> None:
        self.workdir = os.path.abspath(workdir)

    def path_for(self, filename: str) -> str:
        return os.path.join(self.workdir, filename)

    def load(self, filename: str) -> dict[str, Any]:
        path = self.path_for(filename)
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, filename: str, data: dict[str, Any]) -> None:
        os.makedirs(self.workdir, exist_ok=True)
        path = self.path_for(filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")