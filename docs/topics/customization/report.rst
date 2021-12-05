.. _customization-report:

========================
Custom Report generation
========================

Change Report Template
======================
Change the ``REPORT_TEMPLATE`` setting in your :ref:`local_settings.py<introduction-configuration>` file.


Report Assets
=============
If you need to include custom graphics into your report, you should add them to the ``templates/custom/report/assets`` directory.

Proof of concept files are included by default.


Context Variables
=================
You have access to the following classes, methods and attributes inside the report context.

Project
*******

.. autoclass:: apps.projects.models.Project
    :members:
    :undoc-members:

Report
******

.. autoclass:: apps.reporting.models.Report
    :members:
    :undoc-members: