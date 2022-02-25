from vulnman.api import viewsets
from apps.reporting import models
from apps.reporting import tasks
from rest_framework.response import Response
from apps.reporting.api.v1 import serializers
from rest_framework.decorators import action
from rest_framework import status


class ReportViewSet(viewsets.ProjectRelatedObjectRetrieveViewSet):
    queryset = models.PentestReport.objects.all()
    serializer_class = serializers.ReportSerializer

    @action(detail=False, methods=["post"])
    def create_report(self, request, pk=None):
        serializer = serializers.PentestReportCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.validated_data["project"] = serializer.validated_data["project"].pk
            report_task = tasks.do_create_pentest_report.delay(serializer.validated_data)
            return Response({"task_id": report_task.task_id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def get_task_status(self, request, pk=None):
        # TODO: implement
        pass

    @action(detail=True, methods=["patch"], url_name="update", url_path="update")
    def update_report(self, request, pk=None):
        obj = self.get_object()
        serializer = serializers.PentestReportUpdateSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
