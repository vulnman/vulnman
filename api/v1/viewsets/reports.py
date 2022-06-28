from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from django_celery_results.models import TaskResult
from vulnman.api import viewsets
from apps.reporting import models
from apps.reporting import tasks
from api.v1.serializers import reports as serializers


class ReportViewSet(viewsets.ProjectRelatedObjectRetrieveViewSet):
    queryset = models.PentestReport.objects.all()
    serializer_class = serializers.ReportSerializer

    @action(detail=False, methods=["post"])
    def create_report(self, request, pk=None):
        if not request.data.get("name"):
            serializer = serializers.PentestReportDraftCreateSerializer(
                data=request.data, context={"request": request})
        else:
            serializer = serializers.PentestReportSerializer(
                data=request.data, context={"request": request})
        if serializer.is_valid():
            report_task = tasks.do_create_report.delay(
                serializer.validated_data["project"].reportinformation.pk,
                serializer.validated_data["report_type"],
                name=serializer.validated_data.get("name", None),
                creator=self.request.user.username,
                language=serializer.validated_data.get("language"),
                report_template=serializer.validated_data.get(
                    'report_template', 'default'))
            serializer.validated_data["project"] = serializer.validated_data[
                "project"].pk
            return Response({"task_id": report_task.task_id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportTaskResultViewSet(RetrieveModelMixin, GenericViewSet):
    # TODO: make this more generic.
    # do not use this one just for report tasks but all tasks
    queryset = TaskResult.objects.all()
    serializer_class = serializers.ReportTaskSerializer
    lookup_field = "task_id"


class ReportInformationViewSet(viewsets.ProjectRelatedObjectViewSet):
    # TODO: do not allow delete
    queryset = models.ReportInformation
    serializer_class = serializers.PentestReportInformationSerializer
