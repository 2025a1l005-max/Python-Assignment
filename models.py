"""models.py - MemoryCard and PhotoSession classes (Milestone 3)."""
import photo_utils


class MemoryCard:
    """A memory card with a fixed capacity and some space already used."""

    def __init__(self, card_id, capacity_gb, used_gb=0.0):
        self.card_id = card_id
        self.capacity_gb = capacity_gb
        self.used_gb = used_gb

    def available_space(self):
        """Free space left on the card (GB)."""
        return self.capacity_gb - self.used_gb

    def can_store(self, required_gb):
        """True if the card has enough free space for required_gb."""
        return required_gb <= self.available_space()


class PhotoSession:
    """One photography shoot. It HAS-A MemoryCard (composition)."""

    def __init__(self, session_id, photographer_name, shoot_type,
                 photo_count, average_size_mb, card):
        self.session_id = session_id
        self.photographer_name = photographer_name
        self.shoot_type = shoot_type
        self.photo_count = photo_count
        self.average_size_mb = average_size_mb
        self.card = card                      # a MemoryCard object

    def storage_required(self):
        """Storage needed by this shoot in GB."""
        return photo_utils.calculate_storage(self.photo_count, self.average_size_mb)

    def fits_on_assigned_card(self):
        """Ask the card object whether this shoot fits on it."""
        return self.card.can_store(self.storage_required())

    def session_summary(self):
        """Multi-line summary of the session."""
        needed = self.storage_required()
        verdict = "Yes" if self.fits_on_assigned_card() else "No"
        return (f"Session ID      : {self.session_id}\n"
                f"Photographer    : {self.photographer_name}\n"
                f"Shoot type      : {self.shoot_type}\n"
                f"Photos          : {self.photo_count}\n"
                f"Storage needed  : {needed:.2f} GB\n"
                f"Card            : {self.card.card_id} "
                f"({self.card.available_space():.2f} GB free of "
                f"{self.card.capacity_gb} GB)\n"
                f"Fits on card?   : {verdict}")

    def __str__(self):
        return (f"{self.session_id}: {self.photographer_name} - "
                f"{self.shoot_type} shoot, {self.photo_count} photos, "
                f"{self.storage_required():.2f} GB")
