"""Milestone 1 - Estimate storage for one photo shoot."""

# a) Accept the inputs (input() always returns text)
photographer = input("Photographer name: ").strip().title()
shoot_type = input("Shoot type: ").strip().title()
photo_count = input("Number of photos: ")
avg_size_mb = input("Average image size (MB): ")
card_gb = input("Memory-card capacity (GB): ")
duration_min = input("Session duration (minutes): ")

# b) Convert to suitable numeric types
photo_count = int(photo_count)
avg_size_mb = float(avg_size_mb)
card_gb = float(card_gb)
duration_min = int(duration_min)

# c) Storage calculations (1 GB = 1024 MB)
total_mb = photo_count * avg_size_mb
total_gb = total_mb / 1024
remaining_gb = card_gb - total_gb

# d) Duration with // and %, session code with slicing
hours = duration_min // 60
minutes = duration_min % 60
session_code = photographer[:3].upper() + "-" + shoot_type[:3].upper()

print("\n===== SHOOT STORAGE ESTIMATE =====")
print("Photographer        :", photographer)
print("Shoot type          :", shoot_type)
print("Type of photo count :", type(photo_count))
print("Type of image size  :", type(avg_size_mb))
print(f"Total storage       : {total_mb:.2f} MB = {total_gb:.2f} GB")
print(f"Remaining on card   : {remaining_gb:.2f} GB")
print(f"Duration            : {hours} h {minutes} min")
print("Session code        :", session_code)
