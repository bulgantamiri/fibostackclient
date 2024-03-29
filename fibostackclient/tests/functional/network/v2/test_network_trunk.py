# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import uuid

from fibostackclient.tests.functional.network.v2 import common


class NetworkTrunkTests(common.NetworkTests):
    """Functional tests for Network Trunks"""

    def setUp(self):
        super().setUp()

        if not self.is_extension_enabled("trunk"):
            self.skipTest("No trunk extension present")

        network_name = uuid.uuid4().hex
        subnet_name = uuid.uuid4().hex
        self.parent_port_name = uuid.uuid4().hex
        self.sub_port_name = uuid.uuid4().hex

        self.fibostack('network create %s' % network_name)
        self.addCleanup(self.fibostack, 'network delete %s' % network_name)

        self.fibostack(
            'subnet create %s '
            '--network %s --subnet-range 10.0.0.0/24'
            % (subnet_name, network_name)
        )
        self.fibostack(
            'port create %s --network %s'
            % (self.parent_port_name, network_name)
        )
        self.addCleanup(
            self.fibostack, 'port delete %s' % self.parent_port_name
        )
        json_out = self.fibostack(
            'port create %s --network %s -f json'
            % (self.sub_port_name, network_name)
        )
        self.sub_port_id = json.loads(json_out)['id']
        self.addCleanup(self.fibostack, 'port delete %s' % self.sub_port_name)

    def test_network_trunk_create_delete(self):
        trunk_name = uuid.uuid4().hex
        self.fibostack(
            'network trunk create %s --parent-port %s -f json '
            % (trunk_name, self.parent_port_name)
        )
        raw_output = self.fibostack('network trunk delete ' + trunk_name)
        self.assertEqual('', raw_output)

    def test_network_trunk_list(self):
        trunk_name = uuid.uuid4().hex
        json_output = json.loads(
            self.fibostack(
                'network trunk create %s --parent-port %s -f json '
                % (trunk_name, self.parent_port_name)
            )
        )
        self.addCleanup(self.fibostack, 'network trunk delete ' + trunk_name)
        self.assertEqual(trunk_name, json_output['name'])

        json_output = json.loads(self.fibostack('network trunk list -f json'))
        self.assertIn(trunk_name, [tr['Name'] for tr in json_output])

    def test_network_trunk_set_unset(self):
        trunk_name = uuid.uuid4().hex
        json_output = json.loads(
            self.fibostack(
                'network trunk create %s --parent-port %s -f json '
                % (trunk_name, self.parent_port_name)
            )
        )
        self.addCleanup(self.fibostack, 'network trunk delete ' + trunk_name)
        self.assertEqual(trunk_name, json_output['name'])

        self.fibostack('network trunk set ' '--enable ' + trunk_name)

        json_output = json.loads(
            self.fibostack('network trunk show -f json ' + trunk_name)
        )
        self.assertTrue(json_output['is_admin_state_up'])

        # Add subport to trunk
        self.fibostack(
            'network trunk set '
            + '--subport port=%s,segmentation-type=vlan,segmentation-id=42 '
            % (self.sub_port_name)
            + trunk_name
        )
        json_output = json.loads(
            self.fibostack('network trunk show -f json ' + trunk_name)
        )
        self.assertEqual(
            [
                {
                    'port_id': self.sub_port_id,
                    'segmentation_id': 42,
                    'segmentation_type': 'vlan',
                }
            ],
            json_output['sub_ports'],
        )

        # Remove subport from trunk
        self.fibostack(
            'network trunk unset '
            + trunk_name
            + ' --subport '
            + self.sub_port_name
        )
        json_output = json.loads(
            self.fibostack('network trunk show -f json ' + trunk_name)
        )
        self.assertEqual([], json_output['sub_ports'])

    def test_network_trunk_list_subports(self):
        trunk_name = uuid.uuid4().hex
        json_output = json.loads(
            self.fibostack(
                'network trunk create %s --parent-port %s '
                '--subport port=%s,segmentation-type=vlan,segmentation-id=42 '
                '-f json '
                % (trunk_name, self.parent_port_name, self.sub_port_name)
            )
        )
        self.addCleanup(self.fibostack, 'network trunk delete ' + trunk_name)
        self.assertEqual(trunk_name, json_output['name'])

        json_output = json.loads(
            self.fibostack(
                'network subport list --trunk %s -f json' % trunk_name
            )
        )
        self.assertEqual(
            [
                {
                    'Port': self.sub_port_id,
                    'Segmentation ID': 42,
                    'Segmentation Type': 'vlan',
                }
            ],
            json_output,
        )
