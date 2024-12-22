from datetime import timedelta


def human_readable_timedelta(seconds) -> str:
    td = timedelta(seconds=seconds)
    days = td.days
    seconds = td.seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    parts = []
    if days > 0:
        parts.append(f"{days} days")
    if hours > 0:
        parts.append(f"{hours} hours")
    if minutes > 0:
        parts.append(f"{minutes} minutes")
    if seconds > 0:
        parts.append(f"{seconds} seconds")

    return ", ".join(parts)
