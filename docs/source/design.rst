Design Philosophy
=================

The idea is to provide a way for quick deployment for Flask applications,
and to provide out-of-the-box functionality for many use cases. With the same
code base you can deploy many different applications The design philosophy
behind biffy is better described with an example:

.. code-block:: bash

    $ biffy-create-app.py blog --blueprints blog,contact

This command tells biffy to create an application called blog with the
blueprints blog and contact form. Now let's take a look at something a little
more complex.

.. code-block:: bash

    $ biffy-create-app.py blog --blueprints blog,contact --database-config
    database.ini

So suppose you want to use a boilerplate configuration because you have
several sites that will look exactly the same. That is made easy by

.. code-block:: bash

    $ biffy-create-app.py blog --biffy-config recipe.ini
