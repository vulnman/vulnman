import io
import base64
import matplotlib as mpl
import matplotlib.pyplot as plt
from django.db.models import Q
from apps.findings.models import Vulnerability, SEVERITY_CHOICES


class SeverityDonutChart:

    def create_image(self, project):
        text = str(project.vulnerability_set.exclude(
            Q(status=Vulnerability.STATUS_FIXED)).count()) + "\nVulnerabilities"
        s = io.BytesIO()
        data = []
        colors = []
        labels = []
        for sev in SEVERITY_CHOICES:
            amount = Vulnerability.objects.filter(
                severity=sev[0], project=project).exclude(
                    status=Vulnerability.STATUS_FIXED).count()
            if amount > 0:
                data.append(amount)
                # labels.append(sev.capitalize())
                labels.append(amount)
                colors.append(Vulnerability.SEVERITY_COLORS[sev[1]])
        plt.rcParams['svg.fonttype'] = "none"
        mpl.rcParams['text.usetex'] = False
        fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
        ax.axis('equal')
        width = 0.35
        outside, labels = ax.pie(
            data, radius=1, labels=labels, colors=colors, startangle=180,
            pctdistance=1-width/2)
        if labels:
            for label in labels:
                label.set_fontsize(20)
        plt.setp(outside, width=width, edgecolor='white')
        ax.text(
            0, 0, text, ha="center", size=20, fontweight="bold", va="center")
        plt.tight_layout(pad=1.0)
        plt.savefig(s, format="png", bbox_inches="tight", transparent=True)
        plt.close()
        s = base64.b64encode(s.getvalue()).decode().replace("\n", "")
        return "<img id='severity-chart' src=data:image/png;base64,{data}>".format(data=s)

