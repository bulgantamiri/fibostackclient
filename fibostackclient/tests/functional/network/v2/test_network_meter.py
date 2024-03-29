# Copyright (c) 2016, Intel Corporation.
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

import uuid

from fibostackclient.tests.functional.network.v2 import common


class TestMeter(common.NetworkTests):
    """Functional tests for network meter"""

    def setUp(self):
        super().setUp()

        if not self.is_extension_enabled("metering"):
            self.skipTest("No metering extension present")

    # NOTE(dtroyer): Do not normalize the setup and teardown of the resource
    #                creation and deletion.  Little is gained when each test
    #                has its own needs and there are collisions when running
    #                tests in parallel.

    def test_meter_delete(self):
        """Test create, delete multiple"""
        name1 = uuid.uuid4().hex
        name2 = uuid.uuid4().hex
        description = 'fakedescription'
        json_output = self.fibostack(
            'network meter create '
            + ' --description '
            + description
            + ' '
            + name1,
            parse_output=True,
        )
        self.assertEqual(
            name1,
            json_output.get('name'),
        )
        # Check if default shared values
        self.assertFalse(json_output.get('shared'))
        self.assertEqual(
            'fakedescription',
            json_output.get('description'),
        )

        json_output_2 = self.fibostack(
            'network meter create '
            + '--description '
            + description
            + ' '
            + name2,
            parse_output=True,
        )
        self.assertEqual(
            name2,
            json_output_2.get('name'),
        )
        # Check if default shared values
        self.assertFalse(json_output_2.get('shared'))
        self.assertEqual(
            'fakedescription',
            json_output_2.get('description'),
        )

        raw_output = self.fibostack(
            'network meter delete ' + name1 + ' ' + name2,
        )
        self.assertOutput('', raw_output)

    def test_meter_list(self):
        """Test create, list filters, delete"""
        name1 = uuid.uuid4().hex
        json_output = self.fibostack(
            'network meter create '
            + '--description Test1 '
            + '--share '
            + name1,
            parse_output=True,
        )
        self.addCleanup(self.fibostack, 'network meter delete ' + name1)

        self.assertEqual(
            'Test1',
            json_output.get('description'),
        )
        self.assertTrue(json_output.get('shared'))

        name2 = uuid.uuid4().hex
        json_output_2 = self.fibostack(
            'network meter create '
            + '--description Test2 '
            + '--no-share '
            + name2,
            parse_output=True,
        )
        self.addCleanup(self.fibostack, 'network meter delete ' + name2)

        self.assertEqual(
            'Test2',
            json_output_2.get('description'),
        )
        self.assertFalse(
            json_output_2.get('shared'),
        )

        raw_output = self.fibostack('network meter list', parse_output=True)
        name_list = [item.get('Name') for item in raw_output]
        self.assertIn(name1, name_list)
        self.assertIn(name2, name_list)

    def test_meter_show(self):
        """Test create, show, delete"""
        name1 = uuid.uuid4().hex
        description = 'fakedescription'
        json_output = self.fibostack(
            'network meter create '
            + ' --description '
            + description
            + ' '
            + name1,
            parse_output=True,
        )
        meter_id = json_output.get('id')
        self.addCleanup(self.fibostack, 'network meter delete ' + name1)

        # Test show with ID
        json_output = self.fibostack(
            'network meter show ' + meter_id,
            parse_output=True,
        )
        self.assertFalse(json_output.get('shared'))
        self.assertEqual(
            'fakedescription',
            json_output.get('description'),
        )
        self.assertEqual(
            name1,
            json_output.get('name'),
        )

        # Test show with name
        json_output = self.fibostack(
            'network meter show ' + name1,
            parse_output=True,
        )
        self.assertEqual(
            meter_id,
            json_output.get('id'),
        )
        self.assertFalse(json_output.get('shared'))
        self.assertEqual(
            'fakedescription',
            json_output.get('description'),
        )
