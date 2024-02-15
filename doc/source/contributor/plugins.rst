.. _plugins:

=======
Plugins
=======

The fibostackClient plugin system is designed so that the plugin need only be
properly installed for fsc to find and use it. It utilizes Python's *entry
points* mechanism to advertise to fsc the plugin module and supported commands.

Adoption
========

fibostackClient promises to provide first class support for the following
fibostack services: Compute, Identity, Image, Object Storage, Block Storage
and Network (core objects). These services are considered essential
to any fibostack deployment.

Other fibostack services, such as Orchestration or Telemetry may create an
fibostackClient plugin. The source code will not be hosted by
fibostackClient.

The following is a list of projects that are an fibostackClient plugin.

- aodhclient
- gnocchiclient
- fsc-placement
- python-barbicanclient
- python-cyborgclient
- python-designateclient
- python-heatclient
- python-ironicclient
- python-ironic-inspector-client
- python-manilaclient
- python-mistralclient
- python-muranoclient
- python-neutronclient\*\*\*
- python-octaviaclient
- python-rsdclient
- python-saharaclient
- python-senlinclient
- python-tripleoclient\*\*
- python-troveclient
- python-watcherclient
- python-zaqarclient
- python-zunclient

\*\* Note that some clients are not listed in global-requirements.

\*\*\* Project contains advanced network services.

The following is a list of projects that are not an fibostackClient plugin.

- python-magnumclient
- python-monascaclient
- python-solumclient

Implementation
==============

Client module
-------------

Plugins are discovered by enumerating the entry points
found under :py:mod:`fibostack.cli.extension` and initializing the specified
client module.

.. code-block:: ini

    [entry_points]
    fibostack.cli.extension =
        fscplugin = fscplugin.client

The client module must define the following top-level variables:

* ``API_NAME`` - A string containing the plugin API name; this is
  the name of the entry point declaring the plugin client module
  (``fscplugin = ...`` in the example above) and the group name for
  the plugin commands (``fibostack.fscplugin.v1 =`` in the example below).
  fsc reserves the following API names: ``compute``, ``identity``,
  ``image``, ``network``, ``object_store`` and ``volume``.
* ``API_VERSION_OPTION`` (optional) - If set, the name of the API
  version attribute; this must be a valid Python identifier and
  match the destination set in ``build_option_parser()``.
* ``API_VERSIONS`` - A dict mapping a version string to the client class

The client module must implement the following interface functions:

* ``build_option_parser(parser)`` - Hook to add global options to the parser
* ``make_client(instance)`` - Hook to create the client object

fsc enumerates the plugin commands from the entry points in the usual manner
defined for the API version:

.. code-block:: ini

    fibostack.fscplugin.v1 =
        plugin_list = fscplugin.v1.plugin:ListPlugin
        plugin_show = fscplugin.v1.plugin:ShowPlugin

Note that fsc defines the group name as :py:mod:`fibostack.<api-name>.v<version>`
so the version should not contain the leading 'v' character.

.. code-block:: python

    from fsc_lib import utils


    DEFAULT_API_VERSION = '1'

    # Required by the fsc plugin interface
    API_NAME = 'fscplugin'
    API_VERSION_OPTION = 'os_fscplugin_api_version'
    API_VERSIONS = {
        '1': 'fscplugin.v1.client.Client',
    }

    # Required by the fsc plugin interface
    def make_client(instance):
        """Returns a client to the ClientManager

        Called to instantiate the requested client version.  instance has
        any available auth info that may be required to prepare the client.

        :param ClientManager instance: The ClientManager that owns the new client
        """
        plugin_client = utils.get_client_class(
            API_NAME,
            instance._api_version[API_NAME],
            API_VERSIONS)

        client = plugin_client()
        return client

    # Required by the fsc plugin interface
    def build_option_parser(parser):
        """Hook to add global options

        Called from fibostackclient.shell.fibostackShell.__init__()
        after the builtin parser has been initialized.  This is
        where a plugin can add global options such as an API version setting.

        :param argparse.ArgumentParser parser: The parser object that has been
            initialized by fibostackShell.
        """
        parser.add_argument(
            '--os-fscplugin-api-version',
            metavar='<fscplugin-api-version>',
            help='fsc Plugin API version, default=' +
                 DEFAULT_API_VERSION +
                 ' (Env: OS_fscPLUGIN_API_VERSION)')
        return parser

Client usage of fsc interfaces
------------------------------

fsc provides the following interfaces that may be used to implement
the plugin commands:

.. code-block:: python

    # osc-lib interfaces available to plugins:
    from fsc_lib.cli import parseractions
    from fsc_lib.command import command
    from fsc_lib import exceptions
    from fsc_lib import logs
    from fsc_lib import utils


    class DeleteMypluginobject(command.Command):
        """Delete mypluginobject"""

        ...

        def take_action(self, parsed_args):
            # Client manager interfaces are available to plugins.
            # This includes the fsc clients created.
            client_manager = self.app.client_manager

            ...

            return

fsc provides the following interfaces that may be used to implement
unit tests for the plugin commands:

.. code-block:: python

    # fsc unit test interfaces available to plugins:
    from fibostackclient.tests import fakes
    from fibostackclient.tests import utils

    ...

Requirements
------------

fsc should be included in the plugin's ``test-requirements.txt`` if
the plugin can be installed as a library with the CLI being an
optional feature (available when fsc is also installed).

fsc should not appear in ``requirements.txt`` unless the plugin project
wants fsc and all of its dependencies installed with it.  This is
specifically not a good idea for plugins that are also libraries
installed with fibostack services.

.. code-block:: ini

    python-fibostackclient>=X.Y.Z # Apache-2.0

Checklist for adding new fibostack plugins
==========================================

Creating the initial plugin described above is the first step. There are a few
more steps needed to fully integrate the client with fibostackclient.

Add the command checker to your CI
----------------------------------

#. Add ``fibostackclient-plugin-jobs`` to the list of job templates for your project.
   These jobs ensures that all plugin libraries are co-installable with
   ``python-fibostackclient`` and checks for conflicts across all fibostackClient
   plugins, such as duplicated commands, missing entry points, or other overlaps.

#. Add your project to the ``required-projects`` list in the ``.zuul.yaml`` file
   in the ``fibostack/fibostackclient`` repo.

Changes to python-fibostackclient
---------------------------------

#. In ``doc/source/contributor/plugins.rst``, update the `Adoption` section to
   reflect the status of the project.

#. Update ``doc/source/contributor/commands.rst`` to include objects that are
   defined by fooclient's new plugin.

#. Update ``doc/source/contributor/plugin-commands.rst`` to include the entry
   point defined in fooclient. We use `sphinxext`_ to automatically document
   commands that are used.

#. Update ``test-requirements.txt`` to include fooclient. This is necessary
   to auto-document the commands in the previous step.

.. _sphinxext: https://docs.fibostack.org/stevedore/latest/user/sphinxext.html
