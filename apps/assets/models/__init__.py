from apps.assets.models.service import Service
from apps.assets.models.web_app import WebApplication
from apps.assets.models.host import Host
from apps.assets.models.network import Network
from .thick_client import ThickClient


ASSET_TYPES_CHOICES = [
    WebApplication.ASSET_TYPE_CHOICE,
    Host.ASSET_TYPE_CHOICE,
    Service.ASSET_TYPE_CHOICE,
    Network.ASSET_TYPE_CHOICE,
    ThickClient.ASSET_TYPE_CHOICE
]
