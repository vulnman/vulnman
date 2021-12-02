Welcome to Vulnman's documentation!
===================================

Vulnman is a vulnerability management application written in `Django <https://www.djangoproject.com/>`_.

It provides a web interface to create pentesting projects, manage the associated hosts, services and applications, vulnerabilities and reports.

The reports are generated using `LaTeX <https://www.latex-project.org/>`_ and are served as PDF.

.. warning::

    This project is in an very early stage. You may not want to use it in production.


Features
========
- Multiple Projects

  - Manage found Hosts, Services, Webapps, ...
- Report generation (requires LaTeX environment on host)

  - PDF export

  - Multiple revisions with changelogs

  - Edit raw LaTeX source, if needed

- Vulnerability Management

  - Project Dashboard with charts

  - Vulnerability Templates

  - CVSS Calculator

  - Write vulnerability information Markdown

- Import vulnerability templates from CSV files

- Command Builder

  - Organize your commonly used commands and build them to match your target


.. toctree::
   :maxdepth: 9
   :caption: Contents:


First Steps
===========

.. toctree::
    :caption: First Steps
    :hidden:

    introduction/install
    introduction/configuration

:doc:`introduction/install`
    Install instructions for Vulnman.
:doc:`introduction/configuration`
    List of settings.


Vulnerability Management
========================

.. toctree::
    :caption: Vulnerability Management
    :hidden:

    topics/vuln_management/templates
    topics/vuln_management/external_tools


:doc:`topics/vuln_management/templates`
    Describe the usage of vulnerability templates

:doc:`topics/vuln_management/external_tools`
    Import external tool reports into vulnman


Customization
=============

.. toctree::
    :caption: Customization
    :hidden:

    topics/customization/report
    topics/customization/css

:doc:`topics/customization/report`
    How to customize report

:doc:`topics/customization/css`
    How to customize CSS theme


Misc
====

.. toctree::
    :caption: Misc
    :hidden:

    topics/misc/other_products

:doc:`topics/misc/other_products`
    Other products in use



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
