from __future__ import annotations

import os
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QToolBar, QLabel, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QKeySequence, QShortcut

from config import DEFAULT_WORKDIR, TabSpec
from storage import JsonStore
from schemas import SCHEMAS
from widgets import ObjectEditor, CollectionEditor


TABS: list[TabSpec] = [
    TabSpec(tab_name="Contact", filename="contact.json", mode="object", schema_key="contact"),
    TabSpec(tab_name="Skills", filename="skills.json", mode="multi_collection", collection_keys=("skills", "experience"), schema_key="skill_item"),
    TabSpec(tab_name="Projects", filename="projects.json", mode="collection", collection_keys=("projects",), schema_key="project_item"),
    TabSpec(tab_name="Jobs", filename="jobs.json", mode="collection", collection_keys=("jobs",), schema_key="job_item"),
]


def new_item_factory(key: str) -> dict[str, Any]:
    # These “blank templates” make Add predictable.
    if key == "skills":
        return {"name": "", "years": 0, "focused": False, "specifics": []}
    if key == "experience":
        return {"title": "", "years": 0}
    if key == "jobs":
        return {
            "company": "", "title": "", "start": "", "end": None, "location": "",
            "description": "", "highlights": [], "skills": []
        }
    if key == "projects":
        return {
            "name": "", "type": "", "start": "", "end": None, "summary": "",
            "stack": [], "highlights": [], "links": [], "what_i_learned": []
        }
    return {}


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Resume JSON Editor (PyQt6)")
        self.setMinimumSize(1100, 650)

        self.store = JsonStore(DEFAULT_WORKDIR)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self._save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self._save_shortcut.activated.connect(self.save_current_tab)

        self._build_toolbar()
        self._build_tabs()
        self._update_workdir_label()
    
    def save_current_tab(self) -> None:
        w = self.tabs.currentWidget()
        if w is None:
            return
        if hasattr(w, "save") and callable(getattr(w, "save")):
            w.save()  # calls ObjectEditor.save or CollectionEditor.save

    def _build_toolbar(self) -> None:
        tb = QToolBar("Main")
        self.addToolBar(tb)

        self.workdir_label = QLabel()
        self.workdir_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        tb.addWidget(QLabel("Working directory: "))
        tb.addWidget(self.workdir_label)

        tb.addSeparator()

        act = tb.addAction("Set Working Directory…")
        act.triggered.connect(self.pick_workdir)

        act2 = tb.addAction("Open Working Directory…")
        act2.triggered.connect(self.open_workdir_hint)

    def _update_workdir_label(self) -> None:
        self.workdir_label.setText(self.store.workdir)

    def pick_workdir(self) -> None:
        d = QFileDialog.getExistingDirectory(self, "Choose working directory", self.store.workdir)
        if not d:
            return
        self.store.set_workdir(d)
        self._update_workdir_label()
        self._rebuild_tabs_reload()

    def open_workdir_hint(self) -> None:
        # We can't reliably open a file manager cross-platform without extra work.
        QMessageBox.information(self, "Working directory", f"Current working directory:\n{self.store.workdir}")

    def _build_tabs(self) -> None:
        self.tabs.clear()

        for spec in TABS:
            if spec.mode == "object":
                fields = SCHEMAS[spec.schema_key]
                editor = ObjectEditor(
                    fields=fields,
                    load_cb=lambda fn=spec.filename: self.store.load(fn),
                    save_cb=lambda data, fn=spec.filename: self.store.save(fn, data),
                    title=spec.tab_name,
                    filename=spec.filename,
                )
                self.tabs.addTab(editor, spec.tab_name)

            elif spec.mode == "collection":
                fields = SCHEMAS[spec.schema_key]
                key = spec.collection_keys[0]
                editor = CollectionEditor(
                    fields=fields,
                    load_file_cb=lambda fn=spec.filename: self.store.load(fn),
                    save_file_cb=lambda data, fn=spec.filename: self.store.save(fn, data),
                    title=spec.tab_name,
                    filename=spec.filename,
                    collection_keys=[key],
                    default_key=key,
                    new_item_factory=new_item_factory,
                )
                self.tabs.addTab(editor, spec.tab_name)

            elif spec.mode == "multi_collection":
                # Skills tab: dropdown switches between "skills" and "experience"
                # We'll set schema for each key.
                # Default shows "skills"
                skills_fields = SCHEMAS["skill_item"]
                editor = CollectionEditor(
                    fields=skills_fields,
                    load_file_cb=lambda fn=spec.filename: self.store.load(fn),
                    save_file_cb=lambda data, fn=spec.filename: self.store.save(fn, data),
                    title=spec.tab_name,
                    filename=spec.filename,
                    collection_keys=list(spec.collection_keys),
                    default_key="skills",
                    new_item_factory=new_item_factory,
                )
                editor.set_schema_for_key("skills", SCHEMAS["skill_item"])
                editor.set_schema_for_key("experience", SCHEMAS["experience_item"])
                self.tabs.addTab(editor, spec.tab_name)

            else:
                w = QWidget()
                w.setLayout(QVBoxLayout())
                self.tabs.addTab(w, spec.tab_name)

    def _rebuild_tabs_reload(self) -> None:
        cur = self.tabs.currentIndex()
        self._build_tabs()
        self.tabs.setCurrentIndex(max(0, cur))


def main() -> None:
    import sys
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()