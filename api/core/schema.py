from django.http import HttpRequest
from rest_framework.schemas import SchemaGenerator
from rest_framework.request import Request


class MockedSchemaGenerator(SchemaGenerator):

    def get_schema(self, request=None, public=False):

        mock_request = Request(HttpRequest())

        # mock_request.auth = ...

        return super().get_schema(request=mock_request)
