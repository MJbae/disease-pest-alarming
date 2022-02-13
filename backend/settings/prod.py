from .common import *

DEBUG = os.environ.get("DEBUG") in ["1", "t", "true", "T", "True"]

STATICFILES_STORAGE = "backend.storages.StaticAzureStorage"
DEFAULT_FILE_STORAGE = "backend.storages.MediaAzureStorage"

AZURE_ACCOUNT_NAME = os.environ.get("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = os.environ.get("AZURE_ACCOUNT_KEY")