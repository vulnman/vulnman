import io
import base64
import matplotlib.pyplot as plt
from apps.findings.models import Vulnerability, get_severity_by_name, SEVERITY_CHOICES
from django.db.models import Q


SEVERITY_COLORS = {
    "Critical": "#9c1720",
    "High": "#d13c0f", "Medium": "#e8971e", "Low": "#2075f5", "Informational": "#059D1D"
}


class SeverityDonutChart:
 
    def create_image(self, project):
        text = str(project.vulnerability_set.count()) + "\nVulnerabilities"
        s = io.BytesIO()
        data = []
        colors = []
        labels = []
        for sev in ["Critical", "High", "Medium", "Low", "Informational"]:
            amount = Vulnerability.objects.filter(severity=get_severity_by_name(sev), project=project).exclude(status=Vulnerability.STATUS_TO_REVIEW).count()
            if amount > 0:
                data.append(amount)
                # labels.append(sev.capitalize())
                labels.append(amount)
                colors.append(SEVERITY_COLORS[sev])
        fig, ax = plt.subplots(figsize=(8,8), dpi=100)
        ax.axis('equal')
        width = 0.35
        total = Vulnerability.objects.filter(project=project).exclude(status=Vulnerability.STATUS_TO_REVIEW).count()
        outside, labels = ax.pie(data, radius=1, labels=labels, 
            colors=colors, startangle=180, pctdistance=1-width/2)
        if labels:
            for label in labels:
                label.set_fontsize(20)
        plt.setp(outside, width=width, edgecolor='white')
        ax.text(0, 0, text, ha="center", size=20, fontweight="bold", va="center")
        #fig.set_size_inches(10.5, 10.5)
        plt.savefig(s, format="png", bbox_inches="tight")#, dpi=300)
        plt.close()
        s = base64.b64encode(s.getvalue()).decode().replace("\n", "")
        return "data:image/png;base64,{data}".format(data=s)
