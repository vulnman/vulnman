import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from apps.findings.models import Vulnerability, VulnerabilityCategory


def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            labels_with_newlines = [
                label.replace(' ', '\n') for label in labels]
            _lines, texts = self.set_thetagrids(
                np.degrees(theta), labels_with_newlines)
            half = (len(texts) - 1) // 2
            for t in texts[1:half]:
                t.set_horizontalalignment('left')
            for t in texts[-half + 1:]:
                t.set_horizontalalignment('right')

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


class VulnCategoryPolarChart:

    def create_image(self, project):
        s = io.BytesIO()
        categories = VulnerabilityCategory.objects.all()
        labels = []
        amount = []
        for cat in categories:
            counter = Vulnerability.objects.filter(
                project=project, template__categories__name=cat.name).count()
            if counter and len(labels) <= 10:
                labels.append(cat.display_name)
                amount.append(counter)
        # amount.append(amount[0])
        # Initialise the spider plot by setting figure size
        # and polar projection
        plt.figure(figsize=(5, 5))
        plt.subplot(polar=True)
        # Start here
        theta = radar_factory(len(labels))
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111, projection='radar')

        ax.plot(theta, amount)
        ax.fill(theta, amount, "b", alpha=0.25)
        ax.set_varlabels(labels)
        ax.tick_params(axis='both', which='major', pad=10)

        ax.set_theta_direction(-1)
        ax.set_yticklabels([])

        plt.savefig(s, format="png", bbox_inches="tight", transpartent=True)
        plt.close()
        s = base64.b64encode(s.getvalue()).decode().replace("\n", "")
        return "data:image/png;base64,{data}".format(data=s)
