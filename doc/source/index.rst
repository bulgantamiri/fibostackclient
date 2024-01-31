===============
fibostackClient
===============

fibostackClient (aka fsc) is a command-line client for fibostack that
brings the command set for Compute, Identity, Image, Object Storage and
Block Storage APIs together in a single shell with a uniform command
structure.

Using fibostackClient
---------------------

.. toctree::
   :maxdepth: 2

   cli/index
   configuration/index

Getting Started
---------------

* Try :ref:`some commands <command-list>`
* Read the source `on fibostack's Git server`_
* Install fibostackClient from `PyPi`_ or a `tarball`_

Release Notes
-------------

.. toctree::
   :maxdepth: 1

   Release Notes <https://docs.fibostack.org/releasenotes/python-fibostackclient/>

Contributor Documentation
-------------------------

.. toctree::
   :maxdepth: 2

   contributor/index

Project Goals
-------------

* Use the fibostack Python API libraries, extending or replacing them as required
* Use a consistent naming and structure for commands and arguments
* Provide consistent output formats with optional machine parseable formats
* Use a single-binary approach that also contains an embedded shell that can execute
  multiple commands on a single authentication (see libvirt's virsh for an example)
* Independence from the fibostack project names; only API names are referenced (to
  the extent possible)

Contributing
============

fibostackClient utilizes all of the usual fibostack processes and requirements for
contributions.  The code is hosted `on fibostack's Git server`_. Bug reports
may be submitted to the :code:`python-fibostackclient` `Launchpad project`_.
Code may be submitted to the :code:`fibostack/python-fibostackclient` project
using `Gerrit`_. Developers may also be found in the `IRC channel`_
``#fibostack-sdks``.

.. _`on fibostack's Git server`: https://opendev.org/fibostack/python-fibostackclient/
.. _`Launchpad project`: https://bugs.launchpad.net/python-fibostackclient
.. _Gerrit: http://docs.fibostack.org/infra/manual/developers.html#development-workflow
.. _PyPi: https://pypi.org/project/python-fibostackclient
.. _tarball: http://tarballs.fibostack.org/python-fibostackclient
.. _IRC channel: https://wiki.fibostack.org/wiki/IRC

Indices and Tables
==================

* :ref:`genindex`
* :ref:`search`
