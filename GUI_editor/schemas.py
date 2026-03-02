from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Literal

FieldType = Literal[
    "str",
    "int",
    "bool",
    "date_ym",            # "YYYY-MM" via calendar picker
    "nullable_date_ym",   # "YYYY-MM" or None via calendar + Blank checkbox
    "text",               # long text
    "list_str_lines",     # list[str] edited as one-per-line
    "links_label_url",    # list[{"label","url"}]
    "nullable_str",
]


@dataclass(frozen=True)
class FieldSpec:
    key: str
    label: str
    ftype: FieldType


# ---------- Schemas ----------

CONTACT_SCHEMA = [
    FieldSpec("name.first", "First Name", "str"),
    FieldSpec("name.last", "Last Name", "str"),
    FieldSpec("headline", "Headline", "str"),
    FieldSpec("contact.email", "Email", "str"),
    FieldSpec("contact.phone", "Phone", "str"),
    FieldSpec("contact.location.city", "City", "str"),
    FieldSpec("contact.location.state", "State", "str"),
    FieldSpec("contact.location.zip", "Zip", "str"),
    FieldSpec("links", "Links", "links_label_url"),
    FieldSpec("aboutme", "about me", "text"),
]

SKILL_ITEM_SCHEMA = [
    FieldSpec("name", "Skill Name", "str"),
    FieldSpec("years", "Years", "int"),
    FieldSpec("focused", "Focused", "bool"),
    FieldSpec("specifics", "Specifics (one per line)", "list_str_lines"),
]

EXPERIENCE_ITEM_SCHEMA = [
    FieldSpec("title", "Title", "str"),
    FieldSpec("years", "Years", "int"),
]

JOB_ITEM_SCHEMA = [
    FieldSpec("company", "Company", "str"),
    FieldSpec("title", "Title", "str"),
    FieldSpec("start", "Start (YYYY-MM)", "date_ym"),
    FieldSpec("end", "End (YYYY-MM or blank)", "nullable_date_ym"),
    FieldSpec("location", "Location", "str"),
    FieldSpec("description", "Description", "text"),
    FieldSpec("highlights", "Highlights (one per line)", "list_str_lines"),
    FieldSpec("skills", "Skills (one per line)", "list_str_lines"),
]

PROJECT_ITEM_SCHEMA = [
    FieldSpec("name", "Project Name", "str"),
    FieldSpec("type", "Type", "str"),
    FieldSpec("start", "Start (YYYY-MM)", "date_ym"),
    FieldSpec("end", "End (YYYY-MM or blank)", "nullable_date_ym"),
    FieldSpec("summary", "Summary", "text"),
    FieldSpec("stack", "Stack (one per line)", "list_str_lines"),
    FieldSpec("highlights", "Highlights (one per line)", "list_str_lines"),
    FieldSpec("links", "Links", "links_label_url"),
    FieldSpec("what_i_learned", "What I Learned (one per line)", "list_str_lines"),
]

SCHEMAS: dict[str, list[FieldSpec]] = {
    "contact": CONTACT_SCHEMA,
    "skill_item": SKILL_ITEM_SCHEMA,
    "experience_item": EXPERIENCE_ITEM_SCHEMA,
    "job_item": JOB_ITEM_SCHEMA,
    "project_item": PROJECT_ITEM_SCHEMA,
}