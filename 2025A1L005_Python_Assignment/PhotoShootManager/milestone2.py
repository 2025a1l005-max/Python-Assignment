"""Milestone 2 - Manage multiple photography sessions."""
from photo_utils import SHOOT_TYPES

sessions = []            # list of valid sessions
unique_types = set()     # set of different shoot types seen

print("Valid shoot types:", ", ".join(f"{k}-{v}" for k, v in SHOOT_TYPES.items()))

while True:
    entered = input("\nShoot type (or DONE): ").strip().title()
    if entered == "Done":
        break

    # Reject unknown shoot types
    if entered not in SHOOT_TYPES:
        print("Rejected: unknown shoot type.")
        continue

    try:
        photo_count = int(input("Number of photos: "))
        avg_size_mb = float(input("Average image size (MB): "))
    except ValueError:
        print("Rejected: please enter numbers only.")
        continue

    # Reject non-positive values
    if photo_count <= 0 or avg_size_mb <= 0:
        print("Rejected: photo count and image size must be positive.")
        continue

    storage_gb = photo_count * avg_size_mb / 1024

    # Classify by storage requirement
    if storage_gb < 4:
        category = "Light"
    elif storage_gb <= 8:
        category = "Moderate"
    else:
        category = "Heavy"

    sessions.append({"type": entered, "photos": photo_count,
                     "storage_gb": storage_gb, "category": category})
    unique_types.add(entered)
    print(f"Accepted: {entered} - {storage_gb:.2f} GB ({category})")

# Final weekly summary
total_photos = sum(s["photos"] for s in sessions)
total_gb = sum(s["storage_gb"] for s in sessions)

print("\n===== WEEKLY SHOOT SUMMARY =====")
print("Total sessions :", len(sessions))
print("Total photos   :", total_photos)
print(f"Total storage  : {total_gb:.2f} GB")
print("Unique types   :", ", ".join(sorted(unique_types)) if sessions else "None")
print("\nSessions (highest to lowest storage):")
for s in sorted(sessions, key=lambda x: x["storage_gb"], reverse=True):
    print(f"  {s['type']:<10} {s['photos']:>5} photos  "
          f"{s['storage_gb']:>7.2f} GB  {s['category']}")
