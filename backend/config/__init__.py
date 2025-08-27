from django.urls import include, path

# Define app configurations
APP_CONFIGS = [
    "users",
    "dictionary",
    "order",
    "payment",
]


def get_urlpatterns():
    """
    Dynamically imports and combines URL patterns from multiple apps.
    Returns consolidated URL patterns using lazy loading.
    """
    return [path("", include(f"apps.{app_name}.views")) for app_name in APP_CONFIGS]
