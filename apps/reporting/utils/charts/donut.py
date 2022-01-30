import io
import base64
import matplotlib.pyplot as plt
from apps.findings.models import Vulnerability, get_severity_by_name, SEVERITY_CHOICES


SEVERITY_COLORS = {
    "critical": "#9c1720",
    "high": "#d13c0f", "medium": "#e8971e", "low": "#2075f5", "informational": "#059D1D"
}


class SeverityDonutChart:
 
    def create_image(self, project):
        text = project.vulnerability_set.count()
        s = io.BytesIO()
        data = []
        colors = []
        labels = []
        for sev in ["critical", "high", "medium", "low", "informational"]:
            amount = Vulnerability.objects.filter(verified=True, template__severity=get_severity_by_name(sev), project=project).count()
            if amount > 0:
                data.append(amount)
                labels.append(sev.capitalize())
                colors.append(SEVERITY_COLORS[sev])
        fig, ax = plt.subplots()
        ax.axis('equal')
        width = 0.35
        outside, labels, _ = ax.pie(data, radius=1, autopct='%.2f', labels=labels, colors=colors, startangle=180, pctdistance=1-width/2)
        plt.setp(outside, width=width, edgecolor='white')
        ax.text(0, 0, text, ha="center", size=20, fontweight="bold", va="center")
        fig.set_size_inches(10.5, 10.5)
        plt.savefig(s, format="png", bbox_inches="tight", dpi=100)
        plt.close()
        s = base64.b64encode(s.getvalue()).decode().replace("\n", "")
        return "data:image/png;base64,{data}".format(data=s)
