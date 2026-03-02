#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QMessageBox,
)

OUTPUT_PATH = os.path.abspath("~/test/json")
# Example:

def build_payload(values: dict[str, str]) -> dict[str, Any]:
    links = []
    for i in (1, 2, 3):
        label = values.get(f"link{i}_label", "").strip()
        url = values.get(f"link{i}_url", "").strip()
        if label or url:
            links.append({"label": label, "url": url})

    return {
        "name": {
            "first": values.get("first", "").strip(),
            "last": values.get("last", "").strip(),
        },
        "headline": values.get("headline", "").strip(),
        "contact": {
            "email": values.get("email", "").strip(),
            "phone": values.get("phone", "").strip(),
            "location": {
                "city": values.get("city", "").strip(),
                "state": values.get("state", "").strip(),
                "zip": values.get("zip", "").strip(),
            },
        },
        "links": links,
    }


def write_json(path: str, payload: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")


def read_json(path: str) -> dict[str, Any] | None:
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


class JsonProfileEditor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("JSON Profile Editor (Overwrite + Import)")
        self.setMinimumWidth(950)

        self.inputs: dict[str, QLineEdit] = {}

        # Output path label
        path_label = QLabel(f"Output file: {OUTPUT_PATH}")
        path_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        # Groups
        name_group = QGroupBox("Name")
        name_layout = QGridLayout()
        self._add_field(name_layout, "First", "first", 0, 0)
        self._add_field(name_layout, "Last", "last", 0, 2)
        name_group.setLayout(name_layout)

        headline_group = QGroupBox("Headline")
        headline_layout = QGridLayout()
        self._add_field(headline_layout, "Professional Title", "headline", 0, 0, col_span=4)
        headline_group.setLayout(headline_layout)

        contact_group = QGroupBox("Contact")
        contact_layout = QGridLayout()
        self._add_field(contact_layout, "Email", "email", 0, 0, col_span=2)
        self._add_field(contact_layout, "Phone", "phone", 0, 2, col_span=2)
        self._add_field(contact_layout, "City", "city", 1, 0)
        self._add_field(contact_layout, "State", "state", 1, 2)
        self._add_field(contact_layout, "Zip", "zip", 2, 0)
        contact_group.setLayout(contact_layout)

        links_group = QGroupBox("Links (up to 3)")
        links_layout = QGridLayout()
        for idx, row in enumerate((0, 1, 2), start=1):
            self._add_field(links_layout, f"Label {idx}", f"link{idx}_label", row, 0, col_span=2)
            self._add_field(links_layout, f"URL {idx}", f"link{idx}_url", row, 2, col_span=2)
        links_group.setLayout(links_layout)

        # Preview
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setFont(QFont("monospace"))
        self.preview.setMinimumHeight(300)

        # Buttons
        save_btn = QPushButton("Save (Overwrite)")
        save_btn.clicked.connect(self.save_overwrite)

        reload_btn = QPushButton("Reload from File")
        reload_btn.clicked.connect(self.load_from_file)

        clear_btn = QPushButton("Clear Fields")
        clear_btn.clicked.connect(self.clear_fields)

        btn_row = QHBoxLayout()
        btn_row.addWidget(save_btn)
        btn_row.addWidget(reload_btn)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch(1)

        # Layout
        left = QVBoxLayout()
        left.addWidget(path_label)
        left.addWidget(name_group)
        left.addWidget(headline_group)
        left.addWidget(contact_group)
        left.addWidget(links_group)
        left.addLayout(btn_row)

        right = QVBoxLayout()
        right.addWidget(QLabel("Preview (what will be written):"))
        right.addWidget(self.preview, 1)

        main = QHBoxLayout()
        main.addLayout(left, 2)
        main.addLayout(right, 3)
        self.setLayout(main)

        # Load existing data on startup
        self.load_from_file()

    def _add_field(self, layout: QGridLayout, label: str, key: str, row: int, col: int, col_span: int = 1) -> None:
        lab = QLabel(label)
        edit = QLineEdit()
        edit.textChanged.connect(self.update_preview)
        self.inputs[key] = edit

        layout.addWidget(lab, row, col)
        layout.addWidget(edit, row, col + 1, 1, col_span)

    def current_values(self) -> dict[str, str]:
        return {k: w.text() for k, w in self.inputs.items()}

    def update_preview(self) -> None:
        payload = build_payload(self.current_values())
        self.preview.setPlainText(json.dumps(payload, indent=2, ensure_ascii=False))

    def clear_fields(self) -> None:
        for w in self.inputs.values():
            w.clear()
        self.update_preview()

    def save_overwrite(self) -> None:
        payload = build_payload(self.current_values())
        try:
            write_json(OUTPUT_PATH, payload)
        except Exception as e:
            QMessageBox.critical(self, "Error writing file", str(e))
            return

        QMessageBox.information(self, "Saved", f"Overwrote:\n{OUTPUT_PATH}")

    def load_from_file(self) -> None:
        data = read_json(OUTPUT_PATH)
        if not data:
            self.update_preview()
            return

        # Safely populate fields
        self.inputs["first"].setText(data.get("name", {}).get("first", ""))
        self.inputs["last"].setText(data.get("name", {}).get("last", ""))
        self.inputs["headline"].setText(data.get("headline", ""))

        contact = data.get("contact", {})
        location = contact.get("location", {})

        self.inputs["email"].setText(contact.get("email", ""))
        self.inputs["phone"].setText(contact.get("phone", ""))
        self.inputs["city"].setText(location.get("city", ""))
        self.inputs["state"].setText(location.get("state", ""))
        self.inputs["zip"].setText(location.get("zip", ""))

        links = data.get("links", [])
        for i in range(3):
            if i < len(links):
                self.inputs[f"link{i+1}_label"].setText(links[i].get("label", ""))
                self.inputs[f"link{i+1}_url"].setText(links[i].get("url", ""))
            else:
                self.inputs[f"link{i+1}_label"].setText("")
                self.inputs[f"link{i+1}_url"].setText("")

        self.update_preview()


def main() -> None:
    import sys
    app = QApplication(sys.argv)
    w = JsonProfileEditor()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":

    main()
