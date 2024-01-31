#!/bin/bash
# Copyright (c) 2020 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This is an example script that can be installed somewhere, such as
# /usr/local/bin/fibostack, that will allow using python-fibostackclient
# via the container image instead of via a direct installation. It
# bind-mounts in clouds.yaml files, so it should behave like a directly
# installed fsc.

if type podman 2>/dev/null ; then
  RUNTIME=podman
else
  RUNTIME=docker
fi

exec $RUNTIME run -it --rm \
  -v/etc/fibostack:/etc/fibostack \
  -v$HOME/.config/fibostack:/root/.config/fibostack \
  fsclient/fibostackclient \
  fibostack $@
