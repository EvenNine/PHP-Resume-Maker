from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
import os

TabMode = Literal["object", "collection", "multi_collection"]

# ====== Compute base directory from this file's location ======
# config.py is in: Resume/GUI_editor/config.py
# base_dir becomes: Resume/
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(THIS_DIR, os.pardir))

# ====== Default working directory for JSON files ======
# Resume/html/json
DEFAULT_WORKDIR = os.path.join(BASE_DIR, "html", "json")


@dataclass(frozen=True)
class TabSpec:
    tab_name: str
    filename: str
    mode: TabMode
    # For "collection": one key like "jobs"
    # For "multi_collection": multiple keys like ("skills", "experience")
    collection_keys: tuple[str, ...] = ()
    # Schema keys used by schemas.py
    schema_key: str = ""