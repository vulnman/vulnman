.. _plugin-system:

=============
Plugin System
=============
Vulnman has a plugin system that is used to process external tool reports.

The :ref:`vulnman-cli<vulnman-cli-install>` is rewriting the commands to match the required format for later processing in the background.

The :ref:`vulnamn-server<server-install>` finally processes all incoming tool results and maps the findings into its database models.


Available Plugins
=================
The "Example Commands" provided below are only required, if you upload the results directly without using the :ref:`vulnman-cli<vulnman-cli-install>`.


:Tool: nmap
:Example Command:
    nmap -sV -sC -oX example.xml example.com

:Tool: Subfinder
:Example Command:
    subfinder -d example.com | tee subfinder.txt

:Tool: Gobuster (DNS)
:Example Command:
    gobuster dns -d example.com -w subdomains.txt | tee gobuster.dns.txt

:Tool: Gobuster (Dir)
:Example Command:
    gobuster dir -u http://example.com -w common.txt | tee gobuster.dir.txt

:Tool: Gobuster (Vhost)
:Example Command:
    gobuster vhost -u http://example.com -w subdomains.txt | tee gobuster.vhost.txt

:Tool: aiodnsbrute
:Example Command:
    aiodnsbrute -w wordlist.txt example.com | tee aiodnsbrute.txt

:Tool: fierce
:Example command:
    fierce -domain tesla.com | tee fierce.txt

:Tool:
    infoga
:Example Command:
    ìnfoga --domain example.com -r infoga.txt

:Tool:
    BurpSuite (Pro)
:Example Command:
    None
:Description:
    Export Issues in XML format through the BurpSuite application

:Tool:
    nuclei
:Example Command:
    nuclei -json -nc -o results.json -u http://localhost -t nuclei-templates

:Tool:
    testssl
:Example Command:
    testssl -oj results.json https://example.com


Writing a Plugin
================
The plugin consists of two parts: The part that processes the (raw) output of the tool.
This is currently happening on the server (see `#60 <https://github.com/vulnman/vulnman/issues/60>`_).
The second part is the plugin that handles the command rewrite and ensures all required arguments exist.
This part is currently really lightweight and easy to write.


Part 1
======

The parent class for the server side part looks like this:

.. autoclass:: vulnman.utils.tools.ToolResultParser
    :members:
    :undoc-members:
    :private-members:


This example uses the gobuster vhost plugin.

First of all you need to create a python package. This example uses the default location
of the built-in tool importers (`tools/parsers/`).

Add your tool to your :ref:`local_settings.py<introduction-configuration>` file like shown below:

.. code-block:: python

    CUSTOM_EXTERNAL_TOOLS = {
        "gobuster-vhost": "tools.parsers.gobuster.GobusterVhost"
    }


This is how the final plugin looks like:


.. literalinclude:: ../../../apps/external_tools/parsers/gobuster.py
    :language: python
    :start-after: vhost plugin
    :end-before: dir plugin


Part 2
======

This is the most easy part in writing your own plugins.

If your plugin can be processed without writing the results to a temporary file and does not need any special flags to be set, this is how a plugin will look:

.. code-block:: python

    from vulnman_plugins import plugin

    class Subfinder(plugin.Plugin):
        _alias_ = 'subfinder'

        def setup(self):
            pass

The nuclei plugin for example, requires some special flags to be set, to write the results to a json file.
The following code shows how you can enforce such a command rewrite.

.. code-block:: python

    from vulnman_plugins import plugin

    class Nuclei(plugin.Plugin):
        _alias_ = 'nuclei'

        def setup(self):
            self.required_arguments = [
                plugin.Argument("-json", has_value=False), plugin.Argument("-o", is_filepath=True),
                plugin.Argument("-nc", has_value=False)
            ]
            self.filename = self.create_temp_file()

This part of the plugin needs to be added to the ``vulnman_plugins`` package.
