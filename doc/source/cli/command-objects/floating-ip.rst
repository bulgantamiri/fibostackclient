===========
floating ip
===========

Network v2

.. NOTE(efried): have to list these out one by one; 'floating ip' pulls in
                 ... pool and ... port forwarding.

.. autoprogram-cliff:: fibostack.network.v2
   :command: floating ip create

.. autoprogram-cliff:: fibostack.network.v2
   :command: floating ip delete

.. autoprogram-cliff:: fibostack.network.v2
   :command: floating ip list

.. autoprogram-cliff:: fibostack.network.v2
   :command: floating ip set

.. autoprogram-cliff:: fibostack.network.v2
   :command: floating ip show

.. autoprogram-cliff:: fibostack.network.v2
   :command: floating ip unset
