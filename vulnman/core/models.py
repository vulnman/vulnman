from django.db import models


class AssetModelMixin:
    # assets
    on_asset_webapp = models.ForeignKey('assets.WebApplication', null=True, blank=True, on_delete=models.CASCADE)
    on_asset_service = models.ForeignKey('assets.Service', null=True, blank=True, on_delete=models.CASCADE)
    on_asset_host = models.ForeignKey('assets.Host', null=True, blank=True, on_delete=models.CASCADE)
