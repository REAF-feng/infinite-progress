"""
JSON-based storage for test records and quiz progress.
"""
import json
import os
from typing import List, Optional

from config import RECORDS_FILE, PROGRESS_FILE
from models.test_record import TestRecord


class JSONStorage:
    """Persistent JSON storage for TestRecord objects."""

    def __init__(self):
        self._records: List[TestRecord] = []
        self._loaded = False

    def _ensure_loaded(self):
        if not self._loaded:
            self._records = self._load_from_disk()
            self._loaded = True

    def _load_from_disk(self) -> List[TestRecord]:
        if not os.path.exists(RECORDS_FILE):
            return []
        try:
            with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [TestRecord.from_dict(item) for item in data]
        except (json.JSONDecodeError, IOError):
            return []

    def _flush(self):
        os.makedirs(os.path.dirname(RECORDS_FILE), exist_ok=True)
        with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump([r.to_dict() for r in self._records], f, ensure_ascii=False, indent=2)

    def load_all(self) -> List[TestRecord]:
        """Return all stored test records."""
        self._ensure_loaded()
        return list(self._records)

    def save(self, record):
        """Persist a single test record (appended to the list).
        Accepts TestRecord or dict."""
        self._ensure_loaded()
        if isinstance(record, dict):
            record = TestRecord.from_dict(record)
        self._records.append(record)
        self._flush()

    def delete(self, record_id: str) -> bool:
        """Remove a record by its id. Returns True if found and deleted."""
        self._ensure_loaded()
        before = len(self._records)
        self._records = [r for r in self._records if r.id != record_id]
        if len(self._records) < before:
            self._flush()
            return True
        return False

    def get_by_id(self, record_id: str) -> Optional[TestRecord]:
        """Return a single record by id, or None."""
        self._ensure_loaded()
        for r in self._records:
            if r.id == record_id:
                return r
        return None

    @property
    def record_count(self) -> int:
        """Number of stored test records."""
        self._ensure_loaded()
        return len(self._records)


# ---------------------------------------------------------------------------
# Quiz progress helpers (separate file, preserves in-progress state)
# ---------------------------------------------------------------------------

def save_progress(progress_data: dict):
    """Persist quiz progress so it can be resumed later."""
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)


def load_progress() -> Optional[dict]:
    """Load saved quiz progress, or None if no progress exists."""
    if not os.path.exists(PROGRESS_FILE):
        return None
    try:
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def clear_progress():
    """Remove saved quiz progress (e.g. after completion or reset)."""
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
