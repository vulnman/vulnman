"""vulnman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('apps.account.urls')),
    path('api/', include('apps.api.urls')),
    path('projects/', include('apps.projects.urls.projects')),
    path('clients/', include('apps.projects.urls.clients')),
    path('vulnerability-templates/', include('apps.findings.urls.global')),
    path('methodologies/', include('apps.methodologies.urls.global')),
    path('api-token-auth', include('apps.account.api.v1.urls')),
    # path('agents/', include('apps.agents.urls')),
    path('', include('apps.dashboard.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
