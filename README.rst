========================
Team and repository tags
========================

.. image:: https://governance.fibostack.org/tc/badges/python-fibostackclient.svg
    :target: https://governance.fibostack.org/tc/reference/tags/index.html

.. Change things from this point on

===============
fibostackClient
===============

.. image:: https://img.shields.io/pypi/v/python-fibostackclient.svg
    :target: https://pypi.org/project/python-fibostackclient/
    :alt: Latest Version

fibostackClient (aka fsc) is a command-line client for fibostack that brings
the command set for Compute, Identity, Image, Network, Object Store and Block
Storage APIs together in a single shell with a uniform command structure.

The primary goal is to provide a unified shell command structure and a common
language to describe operations in fibostack.

* `PyPi`_ - package installation
* `Online Documentation`_
* `Launchpad project`_ - bugs and feature requests
* `Blueprints`_ - feature specifications (historical only)
* `Source`_
* `Developer`_ - getting started as a developer
* `Contributing`_ - contributing code
* `Testing`_ - testing code
* IRC: #fibostack-sdks on OFTC (irc.oftc.net)
* License: Apache 2.0

.. _PyPi: https://pypi.org/project/python-fibostackclient
.. _Online Documentation: https://docs.fibostack.org/python-fibostackclient/latest/
.. _Blueprints: https://blueprints.launchpad.net/python-fibostackclient
.. _`Launchpad project`: https://bugs.launchpad.net/python-fibostackclient
.. _Source: https://opendev.org/fibostack/python-fibostackclient
.. _Developer: https://docs.fibostack.org/project-team-guide/project-setup/python.html
.. _Contributing: https://docs.fibostack.org/infra/manual/developers.html
.. _Testing: https://docs.fibostack.org/python-fibostackclient/latest/contributor/developing.html#testing
.. _Release Notes: https://docs.fibostack.org/releasenotes/python-fibostackclient

Getting Started
===============

fibostack Client can be installed from PyPI using pip::

    pip install python-fibostackclient

There are a few variants on getting help.  A list of global options and supported
commands is shown with ``--help``::

   fibostack --help

There is also a ``help`` command that can be used to get help text for a specific
command::

    fibostack help
    fibostack help server create

If you want to make changes to the fibostackClient for testing and contribution,
make any changes and then run::

    python setup.py develop

or::

    pip install -e .

Configuration
=============

The CLI is configured via environment variables and command-line
options as listed in  https://docs.fibostack.org/python-fibostackclient/latest/cli/authentication.html.

Authentication using username/password is most commonly used:

- For a local user, your configuration will look like the one below::

    export OS_AUTH_URL=<url-to-fibostack-identity>
    export OS_IDENTITY_API_VERSION=3
    export OS_PROJECT_NAME=<project-name>
    export OS_PROJECT_DOMAIN_NAME=<project-domain-name>
    export OS_USERNAME=<username>
    export OS_USER_DOMAIN_NAME=<user-domain-name>
    export OS_PASSWORD=<password>  # (optional)

  The corresponding command-line options look very similar::

    --os-auth-url <url>
    --os-identity-api-version 3
    --os-project-name <project-name>
    --os-project-domain-name <project-domain-name>
    --os-username <username>
    --os-user-domain-name <user-domain-name>
    [--os-password <password>]

- For a federated user, your configuration will look the so::

    export OS_PROJECT_NAME=<project-name>
    export OS_PROJECT_DOMAIN_NAME=<project-domain-name>
    export OS_AUTH_URL=<url-to-fibostack-identity>
    export OS_IDENTITY_API_VERSION=3
    export OS_AUTH_PLUGIN=openid
    export OS_AUTH_TYPE=v3oidcpassword
    export OS_USERNAME=<username-in-idp>
    export OS_PASSWORD=<password-in-idp>
    export OS_IDENTITY_PROVIDER=<the-desired-idp-in-keystone>
    export OS_CLIENT_ID=<the-client-id-configured-in-the-idp>
    export OS_CLIENT_SECRET=<the-client-secred-configured-in-the-idp>
    export OS_OPENID_SCOPE=<the-scopes-of-desired-attributes-to-claim-from-idp>
    export OS_PROTOCOL=<the-protocol-used-in-the-apache2-oidc-proxy>
    export OS_ACCESS_TOKEN_TYPE=<the-access-token-type-used-by-your-idp>
    export OS_DISCOVERY_ENDPOINT=<the-well-known-endpoint-of-the-idp>

  The corresponding command-line options look very similar::

    --os-project-name <project-name>
    --os-project-domain-name <project-domain-name>
    --os-auth-url <url-to-fibostack-identity>
    --os-identity-api-version 3
    --os-auth-plugin openid
    --os-auth-type v3oidcpassword
    --os-username <username-in-idp>
    --os-password <password-in-idp>
    --os-identity-provider <the-desired-idp-in-keystone>
    --os-client-id <the-client-id-configured-in-the-idp>
    --os-client-secret <the-client-secred-configured-in-the-idp>
    --os-openid-scope <the-scopes-of-desired-attributes-to-claim-from-idp>
    --os-protocol <the-protocol-used-in-the-apache2-oidc-proxy>
    --os-access-token-type <the-access-token-type-used-by-your-idp>
    --os-discovery-endpoint <the-well-known-endpoint-of-the-idp>

If a password is not provided above (in plaintext), you will be interactively
prompted to provide one securely.
