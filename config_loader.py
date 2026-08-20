"""Hand-rolled config reader for settings.cfg."""

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict[str, str]:
    """Parse settings.cfg and return a dict of known key-value pairs."""
    if path is None:
        path = SETTINGS_FILE
    settings: dict[str, str] = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            parts = line.split("=")
            key = parts[0].strip()
            value = parts[1].strip()
            if key in KNOWN_KEYS:
                settings[key] = value
    return settings


def get_int(settings: dict[str, str], key: str, fallback: int) -> int:
    """Read a setting as int, returning *fallback* on failure."""
    try:
        return int(settings.get(key, fallback))
    except (ValueError, TypeError):
        return fallback
