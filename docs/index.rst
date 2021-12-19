Welcome to Vulnman's documentation!
===================================

Vulnman is a vulnerability and pentesting management application written using `Django <https://www.djangoproject.com/>`_.

It provides a web interface to create pentesting projects, manage the associated hosts, services and applications, vulnerabilities and reports.

The reports are generated using `LaTeX <https://www.latex-project.org/>`_ and are served as PDF.

.. warning::

    This project is in an very early stage. You may not want to use it in production.
    The Web-UI will be polished once a backend functionality is more stable and complete.


Features
========
- Multiple Projects

  - Manage found Hosts, Services, Vulnerabilities and other Findings during a scan

  - Collaborate with other users on the same project with different permission roles

- Report generation

  - HTML Report Templates (recommended)

  - LaTeX Report Templates (requires LaTeX environment on host; some issues rendering Markdown!)

  - PDF export

  - Multiple revisions with changelogs

  - Edit Report after creation

- Vulnerability Management

  - Project Dashboard with charts

  - Vulnerability Templates

    - Import from CWE XML files

    - Import from JSON files

  - CVSS Calculator

  - Write vulnerability information Markdown

- Command Builder

  - Organize your commonly used commands and build them to match your target

- Track credentials found during an engagement

- Command Line Interface to send commands directly to your vulnman server.

- Manage Tasks during a pentest (create tasks from templates)

- REST-API


.. toctree::
   :maxdepth: 9
   :caption: Contents:


Installation
============

.. toctree::
    :caption: Installation
    :hidden:

    topics/components/server/installation
    topics/components/cli/installation

:doc:`topics/components/server/installation`
    Install instructions for the vulnman server.

:doc:`topics/components/cli/installation`
    Describe steps to install the vulnman-cli


First Steps
===========

.. toctree::
    :caption: First Steps
    :hidden:

    introduction/configuration
    introduction/update

:doc:`introduction/configuration`
    List of settings.
:doc:`introduction/update`
    Common tasks to keep vulnman up to date


Component Usage
===============

.. toctree::
    :caption: Component Usage
    :hidden:

    topics/components/server/usage
    topics/components/cli/usage

:doc:`topics/components/server/usage`
    How to use the vulnman server
:doc:`topics/components/cli/usage`
    How to use the vulnman cli


Vulnerability Management
========================

.. toctree::
    :caption: Vulnerability Management
    :hidden:

    topics/vuln_management/templates
    topics/vuln_management/reporting


:doc:`topics/vuln_management/templates`
    Describe the usage of vulnerability templates

:doc:`topics/vuln_management/reporting`
    More information about the reporting feature


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


Advanced Topics
===============

.. toctree::
    :caption: Advanced Topics
    :hidden:

    topics/components/agents/usage
    topics/advanced/rest_api
    topics/advanced/plugin_system

:doc:`topics/components/agents/usage`
    Talk about vulnman agents
:doc:`topics/advanced/rest_api`
    More about the REST-API
:doc:`topics/advanced/plugin_system`
    Explain the plugin system used to process reports from external tools (e.g. nmap, nuclei, ...)


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
