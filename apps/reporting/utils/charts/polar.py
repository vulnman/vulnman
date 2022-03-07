import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from apps.findings.models import Vulnerability, VulnerabilityCategory, Template
from django.db.models import Q, Count


class VulnCategoryPolarChart:
 
    def create_image(self, project):
        s = io.BytesIO()
        categories = VulnerabilityCategory.objects.all()
        labels = []
        amount = []
        for cat in categories:
            labels.append(cat.name)
            amount.append(Vulnerability.objects.filter(project=project, template__categories__name=cat.name).count())
        amount.append(amount[0])
        # Initialise the spider plot by setting figure size and polar projection
        plt.figure(figsize=(10, 6))
        plt.subplot(polar=True)
        theta = np.linspace(0, 2 * np.pi, len(amount))
        # Arrange the grid into number of sales equal parts in degrees
        lines, labels = plt.thetagrids(range(0, 360, int(360/len(labels))), (labels))
        # Plot graph
        plt.plot(theta, amount)
        plt.fill(theta, amount, 'b', alpha=0.1)
        plt.savefig(s, format="png", bbox_inches="tight")#, dpi=300)
        plt.close()
        s = base64.b64encode(s.getvalue()).decode().replace("\n", "")
        return "data:image/png;base64,{data}".format(data=s)
