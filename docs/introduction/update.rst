.. _introduction-update:

========
Updating
========


Vulnman Server
==============

To update `vulnman` you just need to follow the steps in this section.

Update the codebase:

.. code-block:: bash

    git pull


You should check the :ref:`local_settings.template.py<introduction-configuration>` file for new settings you need to apply.

Get the new database changes:

.. code-block:: bash

    python manage.py migrate
