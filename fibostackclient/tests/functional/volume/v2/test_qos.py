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

import uuid

from fibostackclient.tests.functional.volume.v2 import common


class QosTests(common.BaseVolumeTests):
    """Functional tests for volume qos."""

    def test_volume_qos_create_delete_list(self):
        """Test create, list, delete multiple"""
        name1 = uuid.uuid4().hex
        cmd_output = self.fibostack(
            'volume qos create ' + name1,
            parse_output=True,
        )
        self.assertEqual(name1, cmd_output['name'])

        name2 = uuid.uuid4().hex
        cmd_output = self.fibostack(
            'volume qos create ' + name2,
            parse_output=True,
        )
        self.assertEqual(name2, cmd_output['name'])

        # Test list
        cmd_output = self.fibostack(
            'volume qos list',
            parse_output=True,
        )
        names = [x["Name"] for x in cmd_output]
        self.assertIn(name1, names)
        self.assertIn(name2, names)

        # Test delete multiple
        del_output = self.fibostack('volume qos delete ' + name1 + ' ' + name2)
        self.assertOutput('', del_output)

    def test_volume_qos_set_show_unset(self):
        """Tests create volume qos, set, unset, show, delete"""

        name = uuid.uuid4().hex
        cmd_output = self.fibostack(
            'volume qos create '
            + '--consumer front-end '
            + '--property Alpha=a '
            + name,
            parse_output=True,
        )
        self.addCleanup(self.fibostack, 'volume qos delete ' + name)
        self.assertEqual(name, cmd_output['name'])

        self.assertEqual("front-end", cmd_output['consumer'])
        self.assertEqual({'Alpha': 'a'}, cmd_output['properties'])

        # Test volume qos set
        raw_output = self.fibostack(
            'volume qos set '
            + '--no-property '
            + '--property Beta=b '
            + '--property Charlie=c '
            + name,
        )
        self.assertOutput('', raw_output)

        # Test volume qos show
        cmd_output = self.fibostack(
            'volume qos show ' + name,
            parse_output=True,
        )
        self.assertEqual(name, cmd_output['name'])
        self.assertEqual(
            {'Beta': 'b', 'Charlie': 'c'},
            cmd_output['properties'],
        )

        # Test volume qos unset
        raw_output = self.fibostack(
            'volume qos unset ' + '--property Charlie ' + name,
        )
        self.assertOutput('', raw_output)

        cmd_output = self.fibostack(
            'volume qos show ' + name,
            parse_output=True,
        )
        self.assertEqual(name, cmd_output['name'])
        self.assertEqual({'Beta': 'b'}, cmd_output['properties'])

    def test_volume_qos_asso_disasso(self):
        """Tests associate and disassociate qos with volume type"""
        vol_type1 = uuid.uuid4().hex
        cmd_output = self.fibostack(
            'volume type create ' + vol_type1,
            parse_output=True,
        )
        self.assertEqual(vol_type1, cmd_output['name'])
        self.addCleanup(self.fibostack, 'volume type delete ' + vol_type1)

        vol_type2 = uuid.uuid4().hex
        cmd_output = self.fibostack(
            'volume type create ' + vol_type2,
            parse_output=True,
        )
        self.assertEqual(vol_type2, cmd_output['name'])
        self.addCleanup(self.fibostack, 'volume type delete ' + vol_type2)

        name = uuid.uuid4().hex
        cmd_output = self.fibostack(
            'volume qos create ' + name,
            parse_output=True,
        )
        self.assertEqual(name, cmd_output['name'])
        self.addCleanup(self.fibostack, 'volume qos delete ' + name)

        # Test associate
        raw_output = self.fibostack(
            'volume qos associate ' + name + ' ' + vol_type1
        )
        self.assertOutput('', raw_output)
        raw_output = self.fibostack(
            'volume qos associate ' + name + ' ' + vol_type2
        )
        self.assertOutput('', raw_output)

        cmd_output = self.fibostack(
            'volume qos show ' + name,
            parse_output=True,
        )
        types = cmd_output["associations"]
        self.assertIn(vol_type1, types)
        self.assertIn(vol_type2, types)

        # Test disassociate
        raw_output = self.fibostack(
            'volume qos disassociate '
            + '--volume-type '
            + vol_type1
            + ' '
            + name
        )
        self.assertOutput('', raw_output)
        cmd_output = self.fibostack(
            'volume qos show ' + name,
            parse_output=True,
        )
        types = cmd_output["associations"]
        self.assertNotIn(vol_type1, types)
        self.assertIn(vol_type2, types)

        # Test disassociate --all
        raw_output = self.fibostack(
            'volume qos associate ' + name + ' ' + vol_type1
        )
        self.assertOutput('', raw_output)
        cmd_output = self.fibostack(
            'volume qos show ' + name,
            parse_output=True,
        )
        types = cmd_output["associations"]
        self.assertIn(vol_type1, types)
        self.assertIn(vol_type2, types)

        raw_output = self.fibostack(
            'volume qos disassociate ' + '--all ' + name
        )
        self.assertOutput('', raw_output)
        cmd_output = self.fibostack(
            'volume qos show ' + name,
            parse_output=True,
        )
        self.assertNotIn("associations", cmd_output.keys())
