from __future__ import annotations

import json
from typing import Any, Callable

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QSplitter,
    QListWidget, QListWidgetItem, QPushButton, QTextEdit, QLabel,
    QLineEdit, QSpinBox, QCheckBox, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QDateEdit
)

from schemas import FieldSpec


# ---------- small helpers for nested dict keys like "contact.location.city" ----------

def get_path(d: dict[str, Any], dotted: str, default: Any = "") -> Any:
    cur: Any = d
    for part in dotted.split("."):
        if not isinstance(cur, dict):
            return default
        cur = cur.get(part, default)
    return cur

def set_path(d: dict[str, Any], dotted: str, value: Any) -> None:
    parts = dotted.split(".")
    cur: Any = d
    for p in parts[:-1]:
        if p not in cur or not isinstance(cur[p], dict):
            cur[p] = {}
        cur = cur[p]
    cur[parts[-1]] = value


def label_for_item(item: dict[str, Any]) -> str:
    for key in ("name", "title", "company"):
        if isinstance(item.get(key), str) and item[key].strip():
            return item[key].strip()
    return "(unnamed)"


# ---------- Field widgets ----------

class LinksTable(QTableWidget):
    """Edits list of {"label","url"}."""
    def __init__(self) -> None:
        super().__init__(0, 2)
        self.setHorizontalHeaderLabels(["Label", "URL"])
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def set_links(self, links: list[dict[str, str]]) -> None:
        self.setRowCount(0)
        for link in links:
            self._add_row(link.get("label", ""), link.get("url", ""))

    def links(self) -> list[dict[str, str]]:
        out: list[dict[str, str]] = []
        for r in range(self.rowCount()):
            label_item = self.item(r, 0)
            url_item = self.item(r, 1)
            label = (label_item.text() if label_item else "").strip()
            url = (url_item.text() if url_item else "").strip()
            if label or url:
                out.append({"label": label, "url": url})
        return out

    def _add_row(self, label: str = "", url: str = "") -> None:
        r = self.rowCount()
        self.insertRow(r)
        self.setItem(r, 0, QTableWidgetItem(label))
        self.setItem(r, 1, QTableWidgetItem(url))

    def add_empty(self) -> None:
        self._add_row("", "")

    def remove_selected(self) -> None:
        rows = sorted({i.row() for i in self.selectedIndexes()}, reverse=True)
        for r in rows:
            self.removeRow(r)


class FormEditor(QWidget):
    """Builds a form from FieldSpecs; can load/apply to dicts."""
    def __init__(self, fields: list[FieldSpec], on_change: Callable[[], None]) -> None:
        super().__init__()
        self.fields = fields
        self.on_change = on_change

        self.widgets: dict[str, QWidget] = {}

        layout = QGridLayout()
        row = 0

        for fs in fields:
            layout.addWidget(QLabel(fs.label), row, 0)

            w: QWidget

            if fs.ftype in ("str", "nullable_str"):
                le = QLineEdit()
                le.textChanged.connect(self.on_change)
                w = le

            elif fs.ftype == "date_ym":
                de = QDateEdit()
                de.setCalendarPopup(True)
                de.setDisplayFormat("yyyy-MM")
                de.dateChanged.connect(self.on_change)
                w = de

            elif fs.ftype == "nullable_date_ym":
                container = QWidget()
                rowlay = QHBoxLayout()
                rowlay.setContentsMargins(0, 0, 0, 0)

                de = QDateEdit()
                de.setCalendarPopup(True)
                de.setDisplayFormat("yyyy-MM")
                de.dateChanged.connect(self.on_change)

                blank = QCheckBox("Blank")
                blank.stateChanged.connect(self.on_change)

                def _toggle_blank() -> None:
                    de.setEnabled(not blank.isChecked())

                blank.stateChanged.connect(_toggle_blank)

                rowlay.addWidget(de, 1)
                rowlay.addWidget(blank)
                container.setLayout(rowlay)

                w = container
                self.widgets[fs.key + ".__date__"] = de
                self.widgets[fs.key + ".__blank__"] = blank

            elif fs.ftype == "int":
                sb = QSpinBox()
                sb.setRange(0, 200)
                sb.valueChanged.connect(self.on_change)
                w = sb

            elif fs.ftype == "bool":
                cb = QCheckBox()
                cb.stateChanged.connect(self.on_change)
                w = cb

            elif fs.ftype == "text":
                te = QTextEdit()
                te.textChanged.connect(self.on_change)
                te.setMinimumHeight(110)
                w = te

            elif fs.ftype == "list_str_lines":
                te = QTextEdit()
                te.textChanged.connect(self.on_change)
                te.setMinimumHeight(110)
                w = te

            elif fs.ftype == "links_label_url":
                container = QWidget()
                v = QVBoxLayout()
                v.setContentsMargins(0, 0, 0, 0)
                table = LinksTable()
                btns = QHBoxLayout()
                add_btn = QPushButton("Add Link")
                rm_btn = QPushButton("Remove Selected")
                add_btn.clicked.connect(table.add_empty)
                rm_btn.clicked.connect(table.remove_selected)
                add_btn.clicked.connect(self.on_change)
                rm_btn.clicked.connect(self.on_change)
                btns.addWidget(add_btn)
                btns.addWidget(rm_btn)
                btns.addStretch(1)
                v.addWidget(table)
                v.addLayout(btns)
                container.setLayout(v)
                w = container
                self.widgets[fs.key + ".__table__"] = table

            else:
                le = QLineEdit()
                le.textChanged.connect(self.on_change)
                w = le

            layout.addWidget(w, row, 1)
            self.widgets[fs.key] = w
            row += 1

        layout.setColumnStretch(1, 1)
        self.setLayout(layout)

    def load_dict(self, data: dict[str, Any]) -> None:
        for fs in self.fields:
            if fs.ftype == "links_label_url":
                table = self.widgets.get(fs.key + ".__table__")
                assert isinstance(table, LinksTable)
                links = get_path(data, fs.key, [])
                table.set_links(links if isinstance(links, list) else [])
                continue

            if fs.ftype == "date_ym":
                w = self.widgets[fs.key]
                assert isinstance(w, QDateEdit)
                val = get_path(data, fs.key, "")
                qd = QDate.currentDate()
                if isinstance(val, str) and val.strip():
                    try:
                        y, m = val.strip().split("-", 1)
                        qd = QDate(int(y), int(m), 1)
                    except Exception:
                        qd = QDate.currentDate()
                w.blockSignals(True)
                w.setDate(qd)
                w.blockSignals(False)
                continue

            if fs.ftype == "nullable_date_ym":
                de = self.widgets.get(fs.key + ".__date__")
                blank = self.widgets.get(fs.key + ".__blank__")
                assert isinstance(de, QDateEdit)
                assert isinstance(blank, QCheckBox)

                val = get_path(data, fs.key, None)
                is_blank = (val is None) or (isinstance(val, str) and not val.strip())

                blank.blockSignals(True)
                blank.setChecked(is_blank)
                blank.blockSignals(False)

                if not is_blank and isinstance(val, str):
                    qd = QDate.currentDate()
                    try:
                        y, m = val.strip().split("-", 1)
                        qd = QDate(int(y), int(m), 1)
                    except Exception:
                        qd = QDate.currentDate()
                    de.blockSignals(True)
                    de.setDate(qd)
                    de.blockSignals(False)

                de.setEnabled(not blank.isChecked())
                continue

            w = self.widgets[fs.key]
            val = get_path(data, fs.key, "")

            if fs.ftype in ("str", "nullable_str"):
                assert isinstance(w, QLineEdit)
                w.blockSignals(True)
                w.setText("" if val is None else str(val))
                w.blockSignals(False)

            elif fs.ftype == "int":
                assert isinstance(w, QSpinBox)
                w.blockSignals(True)
                w.setValue(int(val) if isinstance(val, (int, float, str)) and str(val).strip() else 0)
                w.blockSignals(False)

            elif fs.ftype == "bool":
                assert isinstance(w, QCheckBox)
                w.blockSignals(True)
                w.setChecked(bool(val))
                w.blockSignals(False)

            elif fs.ftype == "text":
                assert isinstance(w, QTextEdit)
                w.blockSignals(True)
                w.setPlainText("" if val is None else str(val))
                w.blockSignals(False)

            elif fs.ftype == "list_str_lines":
                assert isinstance(w, QTextEdit)
                lines = val if isinstance(val, list) else []
                w.blockSignals(True)
                w.setPlainText("\n".join(str(x) for x in lines if str(x).strip()))
                w.blockSignals(False)

    def apply_to_dict(self, data: dict[str, Any]) -> None:
        for fs in self.fields:
            if fs.ftype == "links_label_url":
                table = self.widgets.get(fs.key + ".__table__")
                assert isinstance(table, LinksTable)
                set_path(data, fs.key, table.links())
                continue

            if fs.ftype == "date_ym":
                w = self.widgets[fs.key]
                assert isinstance(w, QDateEdit)
                d = w.date()
                set_path(data, fs.key, f"{d.year():04d}-{d.month():02d}")
                continue

            if fs.ftype == "nullable_date_ym":
                de = self.widgets.get(fs.key + ".__date__")
                blank = self.widgets.get(fs.key + ".__blank__")
                assert isinstance(de, QDateEdit)
                assert isinstance(blank, QCheckBox)

                if blank.isChecked():
                    set_path(data, fs.key, None)
                else:
                    d = de.date()
                    set_path(data, fs.key, f"{d.year():04d}-{d.month():02d}")
                continue

            w = self.widgets[fs.key]

            if fs.ftype == "nullable_str":
                assert isinstance(w, QLineEdit)
                txt = w.text().strip()
                set_path(data, fs.key, None if txt == "" else txt)

            elif fs.ftype == "str":
                assert isinstance(w, QLineEdit)
                set_path(data, fs.key, w.text().strip())

            elif fs.ftype == "int":
                assert isinstance(w, QSpinBox)
                set_path(data, fs.key, int(w.value()))

            elif fs.ftype == "bool":
                assert isinstance(w, QCheckBox)
                set_path(data, fs.key, bool(w.isChecked()))

            elif fs.ftype == "text":
                assert isinstance(w, QTextEdit)
                set_path(data, fs.key, w.toPlainText())

            elif fs.ftype == "list_str_lines":
                assert isinstance(w, QTextEdit)
                lines = [ln.strip() for ln in w.toPlainText().splitlines()]
                lines = [ln for ln in lines if ln]
                set_path(data, fs.key, lines)


# ---------- Editors ----------

class ObjectEditor(QWidget):
    """Edits a single JSON object (Contact)."""
    def __init__(
        self,
        fields: list[FieldSpec],
        load_cb: Callable[[], dict[str, Any]],
        save_cb: Callable[[dict[str, Any]], None],
        title: str,
        filename: str,
    ) -> None:
        super().__init__()
        self._load_cb = load_cb
        self._save_cb = save_cb
        self._data: dict[str, Any] = {}

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setFont(QFont("monospace"))

        self.form = FormEditor(fields, on_change=self.refresh_preview)

        reload_btn = QPushButton("Reload from File")
        save_btn = QPushButton("Save (Overwrite)")
        reload_btn.clicked.connect(self.reload)
        save_btn.clicked.connect(self.save)

        header = QHBoxLayout()
        header.addWidget(QLabel(f"{title}  —  {filename}"))
        header.addStretch(1)
        header.addWidget(reload_btn)
        header.addWidget(save_btn)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.form)
        splitter.addWidget(self.preview)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        root = QVBoxLayout()
        root.addLayout(header)
        root.addWidget(splitter)
        self.setLayout(root)

        self.reload()

    def reload(self) -> None:
        self._data = self._load_cb() or {}
        self.form.load_dict(self._data)
        self.refresh_preview()

    def save(self) -> None:
        self.form.apply_to_dict(self._data)
        try:
            self._save_cb(self._data)
        except Exception as e:
            QMessageBox.critical(self, "Save failed", str(e))
            return
        QMessageBox.information(self, "Saved", "File overwritten successfully.")
        self.refresh_preview()

    def refresh_preview(self) -> None:
        tmp = json.loads(json.dumps(self._data))
        self.form.apply_to_dict(tmp)
        self.preview.setPlainText(json.dumps(tmp, indent=2, ensure_ascii=False))


class CollectionEditor(QWidget):
    """
    Edits a JSON file with one list collection key (jobs/projects) OR one selected key (skills vs experience).
    """
    def __init__(
        self,
        fields: list[FieldSpec],
        load_file_cb: Callable[[], dict[str, Any]],
        save_file_cb: Callable[[dict[str, Any]], None],
        title: str,
        filename: str,
        collection_keys: list[str],
        default_key: str,
        new_item_factory: Callable[[str], dict[str, Any]],
    ) -> None:
        super().__init__()
        self._load_file_cb = load_file_cb
        self._save_file_cb = save_file_cb
        self._file_data: dict[str, Any] = {}
        self._fields_map: dict[str, list[FieldSpec]] = {}
        self._new_item_factory = new_item_factory

        self._fields_map[default_key] = fields

        self.collection_keys = collection_keys
        self.current_key = default_key

        self.key_dropdown = QComboBox()
        self.key_dropdown.addItems(collection_keys)
        self.key_dropdown.setCurrentText(default_key)
        self.key_dropdown.currentTextChanged.connect(self._switch_key)

        self.listw = QListWidget()
        self.listw.currentRowChanged.connect(self._on_select)

        add_btn = QPushButton("Add")
        rm_btn = QPushButton("Remove")
        add_btn.clicked.connect(self.add_item)
        rm_btn.clicked.connect(self.remove_item)

        left = QWidget()
        lv = QVBoxLayout()
        top = QHBoxLayout()
        top.addWidget(QLabel("Section:"))
        top.addWidget(self.key_dropdown, 1)
        lv.addLayout(top)
        lv.addWidget(self.listw, 1)
        btns = QHBoxLayout()
        btns.addWidget(add_btn)
        btns.addWidget(rm_btn)
        btns.addStretch(1)
        lv.addLayout(btns)
        left.setLayout(lv)

        self.form = FormEditor(fields, on_change=self._on_form_change)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setFont(QFont("monospace"))

        reload_btn = QPushButton("Reload from File")
        save_btn = QPushButton("Save (Overwrite)")
        reload_btn.clicked.connect(self.reload)
        save_btn.clicked.connect(self.save)

        header = QHBoxLayout()
        header.addWidget(QLabel(f"{title}  —  {filename}"))
        header.addStretch(1)
        header.addWidget(reload_btn)
        header.addWidget(save_btn)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(self.form)
        splitter.addWidget(self.preview)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 2)

        root = QVBoxLayout()
        root.addLayout(header)
        root.addWidget(splitter)
        self.setLayout(root)

        self.reload()

    def set_schema_for_key(self, key: str, fields: list[FieldSpec]) -> None:
        self._fields_map[key] = fields
        if self.current_key == key:
            self._rebuild_form(fields)

    def _rebuild_form(self, fields: list[FieldSpec]) -> None:
        parent_splitter = self.form.parent()
        idx = parent_splitter.indexOf(self.form)  # type: ignore[attr-defined]

        self.form.setParent(None)
        self.form.deleteLater()

        self.form = FormEditor(fields, on_change=self._on_form_change)
        parent_splitter.insertWidget(idx, self.form)  # type: ignore[attr-defined]

        self._populate_list(keep_selection=False)
        self._on_select(self.listw.currentRow())
        self._refresh_preview()

    def reload(self) -> None:
        self._file_data = self._load_file_cb() or {}
        for k in self.collection_keys:
            if k not in self._file_data or not isinstance(self._file_data.get(k), list):
                self._file_data[k] = []
        self._populate_list()
        self._refresh_preview()

    def save(self) -> None:
        self._apply_current_form_to_item()
        try:
            self._save_file_cb(self._file_data)
        except Exception as e:
            QMessageBox.critical(self, "Save failed", str(e))
            return
        QMessageBox.information(self, "Saved", "File overwritten successfully.")
        self._refresh_preview()
        self._populate_list(keep_selection=True)

    def _switch_key(self, key: str) -> None:
        self._apply_current_form_to_item()
        self.current_key = key

        # Update list for the new collection key
        self._populate_list(keep_selection=False)

        fields = self._fields_map.get(key)
        if fields:
            self._rebuild_form(fields)
        else:
            self._on_select(self.listw.currentRow())
            self._refresh_preview()

    def _items(self) -> list[dict[str, Any]]:
        v = self._file_data.get(self.current_key, [])
        return v if isinstance(v, list) else []

    def _populate_list(self, keep_selection: bool = False) -> None:
        old = self.listw.currentRow() if keep_selection else -1
        self.listw.blockSignals(True)
        self.listw.clear()
        for it in self._items():
            self.listw.addItem(QListWidgetItem(label_for_item(it)))
        self.listw.blockSignals(False)

        if self.listw.count() > 0:
            self.listw.setCurrentRow(old if (keep_selection and 0 <= old < self.listw.count()) else 0)
        else:
            self.form.load_dict({})

    def _on_select(self, row: int) -> None:
        items = self._items()
        if 0 <= row < len(items):
            self.form.load_dict(items[row])
        else:
            self.form.load_dict({})
        self._refresh_preview()

    def _on_form_change(self) -> None:
        # Update the underlying in-memory JSON for the selected item
        self._apply_current_form_to_item()

        # Update ONLY the current row label; do NOT repopulate the whole list
        self._update_current_list_item_label()

        # Refresh preview (does not touch the editor widgets)
        self._refresh_preview()

    def _apply_current_form_to_item(self) -> None:
        row = self.listw.currentRow()
        items = self._items()
        if 0 <= row < len(items):
            self.form.apply_to_dict(items[row])

    def add_item(self) -> None:
        items = self._items()
        items.append(self._new_item_factory(self.current_key))
        self._file_data[self.current_key] = items
        self._populate_list()
        self.listw.setCurrentRow(len(items) - 1)
        self._refresh_preview()

    def remove_item(self) -> None:
        row = self.listw.currentRow()
        items = self._items()
        if not (0 <= row < len(items)):
            return
        del items[row]
        self._file_data[self.current_key] = items
        self._populate_list()
        self._refresh_preview()

    def _refresh_preview(self) -> None:
        self.preview.setPlainText(json.dumps(self._file_data, indent=2, ensure_ascii=False))

    def _update_current_list_item_label(self) -> None:
        row = self.listw.currentRow()
        items = self._items()
        if not (0 <= row < len(items)):
            return
        item_widget = self.listw.item(row)
        if item_widget is None:
            return
        item_widget.setText(label_for_item(items[row]))