from datetime import datetime, timedelta
import random

def random_date(start_date="2000-01-01", end_date="2030-12-31"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    random_days = random.randint(0, (end - start).days)
    return str((start + timedelta(days=random_days)).date())  # Return only the date part