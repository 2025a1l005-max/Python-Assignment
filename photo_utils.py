"""photo_utils.py - reusable helper functions (Milestone 4).

Used by main.py and models.py in the Digital Photography Shoot and
Memory Storage Manager.  1 GB is treated as 1024 MB throughout.
"""
import math

# Valid shoot types and their short codes (also used in Milestone 2)
SHOOT_TYPES = {
    "Portrait": "POR",
    "Event": "EVT",
    "Landscape": "LND",
    "Product": "PRD",
    "Sports": "SPT",
}


def calculate_storage(photo_count, avg_size_mb):
    """Return the total storage needed in GB."""
    return photo_count * avg_size_mb / 1024


def cards_required(storage_gb, card_capacity_gb=16):
    """Return how many memory cards are needed (always rounded up)."""
    if card_capacity_gb <= 0:
        raise ValueError("Card capacity must be greater than zero.")
    return math.ceil(storage_gb / card_capacity_gb)


def backup_storage(storage_gb, copies=2):
    """Return the total space (GB) needed to keep several backup copies."""
    return storage_gb * copies


def summarize_sessions(sessions):
    """Take a collection of PhotoSession objects and return
    (total photos, total storage in GB)."""
    total_photos = sum(s.photo_count for s in sessions)
    total_gb = sum(s.storage_required() for s in sessions)
    return total_photos, total_gb


def total_storage(*session_sizes):
    """Add any number of session sizes (variable arguments)."""
    return sum(session_sizes)


def classify_storage(storage_gb):
    """Light (<4 GB), Moderate (4-8 GB) or Heavy (>8 GB)."""
    if storage_gb < 4:
        return "Light"
    if storage_gb <= 8:
        return "Moderate"
    return "Heavy"


def make_session_code(photographer, shoot_type):
    """Short code such as ADI-POR from the name and shoot type."""
    return photographer.strip()[:3].upper() + "-" + shoot_type.strip()[:3].upper()
