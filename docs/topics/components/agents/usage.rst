======
Agents
======

Vulnman-Agents allow your pentest automation to scale.

There are some scenarios where you may want to run different command from different hosts.

You can also define a set of commands that you usually run at the enumeration phase and queue them to be executed and parsed by the :ref:`Plugin System<plugin-system>`.

There is a `vulnman-agent <https://github.com/blockomat2100/vulnman-agent>`_ in development which does exactly that.

The agent is kept as simple as possible.

**The agent linked above is currently a proof of concept implementation and is not meant to be production-ready.**

Agents are polling a REST-API endpoint that contains a list of commands that need to be executed.

The results of the command is uploaded through another REST-API endpoint after the command results are available.


Create an Agent
===============

In the current state only vulnman administrators are allowed to create agents.

You can create a new agent using the following management command:

.. code-block:: bash

    python manage.py create_agent admin testagent

You need to replace "admin" with the username this agent belongs to.
Replace "testagent" with the desired agent name.
