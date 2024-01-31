==============
network flavor
==============

A **network flavor** extension allows the user selection of operator-curated
flavors during resource creations. It allows administrators to create network
service flavors.

Network v2

.. NOTE(efried): have to list these out one by one; 'network flavor' pulls in
                 ... profile *.

.. autoprogram-cliff:: fibostack.network.v2
   :command: network flavor add profile

.. autoprogram-cliff:: fibostack.network.v2
   :command: network flavor create

.. autoprogram-cliff:: fibostack.network.v2
   :command: network flavor delete

.. autoprogram-cliff:: fibostack.network.v2
   :command: network flavor list

.. autoprogram-cliff:: fibostack.network.v2
   :command: network flavor remove profile

.. autoprogram-cliff:: fibostack.network.v2
   :command: network flavor set

.. autoprogram-cliff:: fibostack.network.v2
   :command: network flavor show
