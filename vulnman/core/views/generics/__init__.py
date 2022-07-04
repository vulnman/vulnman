from vulnman.core.views.generics.vulnman import (
    VulnmanDeleteView, VulnmanUpdateView, VulnmanCreateView, VulnmanDetailView, VulnmanListView,
    VulnmanAuthListView, VulnmanAuthCreateView, VulnmanAuthDeleteView, VulnmanAuthUpdateView,
    VulnmanAuthDetailView,
    VulnmanAuthCreateWithInlinesView, VulnmanAuthUpdateWithInlinesView, VulnmanAuthTemplateView, VulnmanAuthFormView,
    VulnmanAuthRedirectView
)

from vulnman.core.views.generics.project import (
    ProjectListView, ProjectUpdateView, ProjectCreateView, ProjectDetailView,
    ProjectDeleteView, ProjectCreateWithInlinesView, ProjectTemplateView, ProjectRedirectView,
    ProjectFormView
)
