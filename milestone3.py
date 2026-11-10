"""Milestone 3 - Two PhotoSession objects composed with MemoryCard objects."""
from models import MemoryCard, PhotoSession

card1 = MemoryCard("CARD-01", 16)
card2 = MemoryCard("CARD-02", 16, used_gb=2)       # already 2 GB used

session1 = PhotoSession("S001", "Aditi", "Portrait", 320, 18.5, card1)
session2 = PhotoSession("S002", "Rohan", "Event", 1200, 22, card2)

for session in (session1, session2):
    print(session)                                  # uses __str__()
    print(session.session_summary())
    print()
