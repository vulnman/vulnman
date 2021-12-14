===================
Install Vulnman CLI
===================
The Vulnman command line interface allows you to execute your commands with a UX similar to the one you would have without.

All you have to do is to add the "shell" command in front of your command.
The command, the return code and the results will be pushed into your current active project command history.

If there is a plugin for the tool you used, the output will be parsed and hosts, services and vulnerabilities will be created according to the results.


Arch-Linux
==========

.. code-block:: bash

    git clone https://vulnman.github.com/vulnman-cli.git
    cd vulnman-cli
    python setup.py install

You can now run vulnman-cli by running ``vulnman-cli``.
