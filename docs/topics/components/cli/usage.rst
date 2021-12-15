.. _vulnman-cli-usage:

===========
Vulnman CLI
===========

If you are into the vulnman-cli, you first want to log into your server, by entering the following command.

.. code-block:: bash

    login <username> <password>

You can specify an optional server using the ``--server`` flag.


Load a project using the following command.

.. code-block:: bash

    load_project <project_id>

At the current state, you must get the uuid from the :ref:`REST-API<rest-api>` or :ref:`web interface<web-interface>`.

All commands that you are prefixing with ``vman`` are processed by the vulnman server.


.. figure:: ../../../assets/cli/example_usage_intro.png
  :width: 800
  :alt: CLI usage example
