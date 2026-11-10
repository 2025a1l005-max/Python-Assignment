"""main.py - Digital Photography Shoot and Memory Storage Manager.

Final program (Milestones 4 and 5).  Start it with:  python main.py
"""
import time
from pathlib import Path

import photo_utils as pu
from models import MemoryCard, PhotoSession

LOG_DIR = Path(__file__).with_name("photo_logs")
LOG_FILE = LOG_DIR / "shoot_log.txt"


# ------------------------------------------------------------------
# Milestone 4 - weekly storage report
# ------------------------------------------------------------------
def build_sample_sessions():
    """Five sample sessions, each with its own memory card."""
    return [
        PhotoSession("S001", "Aditi", "Portrait", 320, 18.5, MemoryCard("C1", 16)),
        PhotoSession("S002", "Rohan", "Event", 1200, 22, MemoryCard("C2", 64)),
        PhotoSession("S003", "Meera", "Landscape", 150, 30, MemoryCard("C3", 32)),
        PhotoSession("S004", "Kabir", "Product", 80, 12, MemoryCard("C4", 16)),
        PhotoSession("S005", "Simran", "Sports", 900, 15, MemoryCard("C5", 32)),
    ]


def weekly_report():
    start = time.perf_counter()

    sessions = build_sample_sessions()
    total_photos, total_gb = pu.summarize_sessions(sessions)
    sizes = [s.storage_required() for s in sessions]
    combined_gb = pu.total_storage(*sizes)                    # *args
    cards_default = pu.cards_required(total_gb)               # default 16 GB
    cards_32 = pu.cards_required(storage_gb=total_gb, card_capacity_gb=32)  # keywords
    backup_gb = pu.backup_storage(total_gb, copies=3)         # keyword argument

    elapsed = time.perf_counter() - start

    print("\n===== WEEKLY STORAGE REPORT =====")
    for s in sessions:
        print(f"{s}  [{pu.classify_storage(s.storage_required())}]")
    print("-" * 60)
    print("Total photos                  :", total_photos)
    print(f"Total storage                 : {total_gb:.2f} GB")
    print(f"total_storage(*sizes)         : {combined_gb:.2f} GB")
    print("Cards needed (16 GB default)  :", cards_default)
    print("Cards needed (32 GB, keyword) :", cards_32)
    print(f"Backup space, 3 copies        : {backup_gb:.2f} GB")
    print(f"Report generated in {elapsed:.6f} seconds")


# ------------------------------------------------------------------
# Milestone 5 - validation, log file and error handling
# ------------------------------------------------------------------
def read_positive_number(text, field, kind=float):
    """Convert text to a positive number or raise ValueError."""
    try:
        value = kind(text)
    except ValueError:
        raise ValueError(f"{field} must be a valid number, but got '{text}'.") from None
    if value <= 0:
        raise ValueError(f"{field} must be greater than zero, but got {value}.")
    return value


def read_log():
    """Return (valid records, number skipped). Handles a missing file."""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
    except FileNotFoundError:
        print("FileNotFoundError: shoot_log.txt is not available yet.")
        return [], 0

    records, skipped = [], 0
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        parts = line.split("|")
        try:
            if len(parts) != 10:
                raise ValueError("wrong number of fields")
            int(parts[3]); float(parts[4]); float(parts[5])
            int(parts[6]); float(parts[7])
        except ValueError:
            skipped += 1
            print(f"Skipped malformed record on line {number}: {line!r}")
            continue
        records.append(parts)
    return records, skipped


def view_log():
    records, skipped = read_log()
    if LOG_FILE.exists():
        print("\n===== SAVED SHOOT LOG =====")
        print("ID | Photographer | Type | Photos | MB/photo | Card GB | "
              "Minutes | Storage GB | Class | Fits")
        for record in records:
            print(" | ".join(record))
        print("Valid stored sessions :", len(records))
        print("Malformed records     :", skipped)
        print("Log file size         :", LOG_FILE.stat().st_size, "bytes")


def add_session():
    count_so_far = len(read_log()[0]) if LOG_FILE.exists() else 0
    name = input("Photographer name: ").strip().title()
    shoot_type = input("Shoot type (" + ", ".join(pu.SHOOT_TYPES) + "): ").strip().title()
    if shoot_type not in pu.SHOOT_TYPES:
        print("Rejected: unknown shoot type.")
        return
    try:
        photos = read_positive_number(input("Number of photos: "), "Photo count", int)
        size_mb = read_positive_number(input("Average image size (MB): "), "Image size")
        card_gb = read_positive_number(input("Card capacity (GB): "), "Card capacity")
        minutes = read_positive_number(input("Duration (minutes): "), "Duration", int)
    except ValueError as error:
        print("ValueError:", error)
        print("Session not saved. Please try again.")
        return

    session_id = f"{pu.make_session_code(name, shoot_type)}-{count_so_far + 1:02d}"
    session = PhotoSession(session_id, name, shoot_type, photos, size_mb,
                           MemoryCard("CARD", card_gb))
    storage = session.storage_required()
    fits = "Yes" if session.fits_on_assigned_card() else "No"
    print()
    print(session.session_summary())

    record = "|".join([session_id, name, shoot_type, str(photos), str(size_mb),
                       str(card_gb), str(minutes), f"{storage:.2f}",
                       pu.classify_storage(storage), fits])
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(record + "\n")
    print("Session appended to shoot_log.txt")


def main():
    LOG_DIR.mkdir(exist_ok=True)                  # create photo_logs if needed
    print("===== DIGITAL PHOTOGRAPHY SHOOT AND MEMORY STORAGE MANAGER =====")
    while True:
        print("\n1. Weekly storage report   2. Add shoot session"
              "   3. View shoot log   4. Exit")
        choice = input("Choose option: ").strip()
        if choice == "1":
            weekly_report()
        elif choice == "2":
            add_session()
        elif choice == "3":
            view_log()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Choose 1-4.")


if __name__ == "__main__":
    main()
