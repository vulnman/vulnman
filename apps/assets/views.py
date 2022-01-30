from vulnman.views import generic
from apps.assets import models


class WebApplicationList(generic.ProjectListView):
    template_name = "assets/webapp_list.html"
    context_object_name = "webapps"
    
    def get_queryset(self):
        return models.WebApplication.objects.filter(project=self.get_project())
    
