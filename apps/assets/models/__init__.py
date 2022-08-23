from apps.assets.models.service import Service
from apps.assets.models.web_app import WebApplication
from apps.assets.models.web_request import WebRequest
from apps.assets.models.host import Host
from apps.assets.models.web_url import WebURL


ASSET_TYPES_CHOICES = [
    WebApplication.ASSET_TYPE_CHOICE,
    WebRequest.ASSET_TYPE_CHOICE,
    Host.ASSET_TYPE_CHOICE,
    Service.ASSET_TYPE_CHOICE,
    WebURL.ASSET_TYPE_CHOICE
]
