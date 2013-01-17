Design Philosophy
=================

The idea is to provide a way for quick deployment for Flask applications,
and to provide out-of-the-box functionality for many use cases. With the same
code base you can deploy many different applications.

Every developer wishes that they could have that magic bullet framework that
would solve most of their problems. Unfortunately that magic bullet doesn't
and probably will never exist, but we can try to get close. The spirit of
Biffy is that frameworks should be modular, come with tons of features,
and (most important) easy to use.

Modular
-------

Flask implements modularity in the form of Blueprints_. Biffy takes this
concept and bolts on the following capabilities:

* Plug and play according to what you need at deployment
* Blueprints can advertise and offer services to other blueprints
* Consistent layout for ease of development

Tons of Features
----------------

This is the "Batteries-Included" part of Biffy. A good web framework should
be able to get you up and running with some sort of base functionality right
out of the box. Planned blueprints include a blog, a contact form,
a twitter client, a facebook client, a calendar, and maybe a few more.

Easy to Use: Extending
----------------------

It should be simple to add to the Biffy base without a lot of work and it
should be able to be done very quickly. Biffy comes with blueprint creator.

.. code-block:: bash

    $ biffy-create-blueprint.py my_custom_blueprint

Easy to Use: Deployment
-----------------------

Deployment can be a frustrating task. Biffy wants to make that easy for you,
and is best demonstrated by an example:

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

    $ biffy-create-app.py blog --biffy-recipe recipe.ini


So right now you're probably thinking that the goal is to reinvent Django_.
Well, maybe a little bit. The Flask internals are so much more lightweight
and if you know anything about Django's history it's that the ORM hasn't
always been as portable or flexible (though, it is getting better). This
project seeks to fulfill those needs and more.

.. _Blueprints: http://flask.pocoo.org/docs/blueprints/
.. _Django: https://djangoproject.com