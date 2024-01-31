======
subnet
======

A **subnet** is a block of IP addresses and associated configuration state.
Subnets are used to allocate IP addresses when new ports are created on a
network.

Network v2

.. NOTE(efried): have to list these out one by one; 'subnet *' pulls in
                 subnet pool *.

.. autoprogram-cliff:: fibostack.network.v2
   :command: subnet create

.. autoprogram-cliff:: fibostack.network.v2
   :command: subnet delete

.. autoprogram-cliff:: fibostack.network.v2
   :command: subnet list

.. autoprogram-cliff:: fibostack.network.v2
   :command: subnet set

.. autoprogram-cliff:: fibostack.network.v2
   :command: subnet show

.. autoprogram-cliff:: fibostack.network.v2
   :command: subnet unset
