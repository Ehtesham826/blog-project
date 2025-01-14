import os
from datetime import datetime, timedelta
import random

# Work in current folder
if not os.path.exists(".git"):
    os.system("git init")

# Use existing files or create tracker
if not os.path.exists("activity.txt"):
    with open("activity.txt", "w") as f:
        f.write("# Activity Tracker\n")

start = input("Enter Beginning date [yyyymmdd]: ")
end = input("Enter End date [yyyymmdd]: ")

start_date = datetime.strptime(start, "%Y%m%d")
end_date = datetime.strptime(end, "%Y%m%d")

current = start_date
total_commits = 0

while current <= end_date:
    # Random commits based on day type
    if current.weekday() < 5:  # Weekday (Mon-Fri)
        # 60% chance of having commits
        if random.random() < 0.6:
            num_commits = random.randint(1, 4)  # 1-4 commits
        else:
            num_commits = 0  # Skip day
    else:  # Weekend (Sat-Sun)
        # 20% chance of commits
        if random.random() < 0.2:
            num_commits = random.randint(1, 2)
        else:
            num_commits = 0
    
    for i in range(num_commits):
        # Add small change
        with open("activity.txt", "a") as f:
            f.write(f".\n")
        
        # Random time during the day
        hour = random.randint(9, 22)
        minute = random.randint(0, 59)
        date_str = current.strftime(f"%Y-%m-%d {hour:02d}:{minute:02d}:00")
        
        os.system("git add .")
        msg = f"Update {current.strftime('%b %d, %Y')}"
        os.system(f'git commit -m "{msg}" --date="{date_str}"')
        
        total_commits += 1
    
    current += timedelta(days=1)

print(f"Done! Created {total_commits} commits with realistic gaps")