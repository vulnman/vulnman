==============
External Tools
==============
Vulnman has support for external tool report imports.


Current Available Tools
=======================

- `gobuster-vhost <https://github.com/OJ/gobuster#vhost-mode-options>`_
- `gobuster-dir <https://github.com/OJ/gobuster#dir-mode-options>`_
- `nmap <https://github.com/nmap/nmap>`_
- `aiodnsbrute <https://github.com/blark/aiodnsbrute>`_


API
===

.. autoclass:: vulnman.utils.tools.ToolResultParser
    :members:
    :undoc-members:
    :private-members:


Writing a custom tool importer
==============================
This example will walk you through the process of writing your own tool importer.
We will use the gobuster vhosts results for this.

First of all you need to create a python package. This example uses the default location
of the built-in tool importers (`tools/parsers/`).

Add your tool to your :ref:`local_settings.py<introduction-configuration>` file like shown below:

.. code-block:: python

    CUSTOM_EXTERNAL_TOOLS = {
        "gobuster-vhost": "tools.parsers.gobuster.GobusterVhost"
    }


This is the final plugin:


.. literalinclude:: ../../../apps/external_tools/parsers/gobuster.py
    :language: python
    :start-after: vhost plugin
    :end-before: dir plugin
