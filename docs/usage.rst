=====
Usage
=====

To use Python client for Degreed API in a project::

    from degreedClient import DegreedApiClient


The degreed api has got various modules which this client made available, however each module requires a specific ``scope`` for that module. The scope is something similar to this: ``users:read`` it may also look like this: ``users_read`` Degreed confirmed through their `documentation`_ that all methods will be supported, well at least for now but l recommend the first method of using a colon as a dimiliter.

.. _documentation: https://api.degreed.com/docs/#release-april-2019


To be able to use Degreed's api you will need the ``client_id`` , ``client_secret`` and also the ``host`` .The client id and client secret are given by Degreed Technical Solutions Specialist. The host has got a development host as well as production host. The hostname uses the format ``degreed.com`` and for betatest(development) it is in the format ``betatest.degreed.com`` .You get all these from Degreed. The API uses OAuth 2.0 protocol’s Client Credentials Flow, you can get more information via `Degreed`_ official documentation.

.. _Degreed: https://api.degreed.com/docs/#authentication


101 usage
---------

.. code-block:: python

    from degreedClient import DegreedApiClient
    import yaml
    from pprint import pprint

    with open('.profile.yml', 'r') as profile_yml:
        config = yaml.load(profile_yml)

    client = DegreedApiClient(config['host'], config['client_id'], config['client_secret'], config['scope'] )



Users Module
------------

Getting started with user module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from degreedClient import DegreedApiClient
    from pprint import pprint
    client = DegreedApiClient(...)

    pprint(client.users.all())

    # You can also get a single user via ID as an object
    # This means you can get all the user attributes
    a_user = client.users.get('<ID>')
    user_firstname = a_user.attributes.first_name

    print(user_firstname)



Content Module
--------------

Content Management
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from degreedClient import DegreedApiClient
    from pprint import pprint
    client = DegreedApiClient(...)

    pprint(client.content.all())




