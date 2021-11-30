==============
External Tools
==============
Vulnman has support for external tool report imports.


API
===

.. automodule:: vulnman.utils.tools.ToolResultParser
   :members:
   :undoc-members:


Writing a custom tool importer
==============================
This example will walk you through the process of writing your own tool importer.
We will use the gobuster vhosts results for this.

First of all you need to create a python package. This example uses the default location
of the built-in tool importers (tools/parsers/).

Add your tool to your "local_settings.py" file like shown below:

.. code-block:: python

    EXTERNAL_TOOLS = {
        "gobuster-vhost": "tools.parsers.gobuster.GobusterVhost"
    }


This is the final plugin:

.. code-block:: python

    import socket
    from vulnman.utils.tools import ToolResultParser
    from vulns.models import Host, Hostname


    class GobusterVhost(ToolResultParser):
        def parse(self, result, project, creator):
            for line in result.split("\n"):
                if "Found: " in line:
                    subdomain = line.split(" ")[1]
                    try:
                        host_ip = socket.gethostbyname(subdomain)
                    except socket.error:
                        print("Could not resolve subdomain %s" % subdomain)
                        continue
                    host, _created = self._get_or_create_host(host_ip, project, creator)
                    self._get_or_create_hostname(subdomain, host)

