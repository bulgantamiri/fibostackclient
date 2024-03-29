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

import os

from fibostackclient.common import configuration
from fibostackclient.tests.functional import base


BASIC_CONFIG_HEADERS = ['Field', 'Value']


class ConfigurationTests(base.TestCase):
    """Functional test for configuration."""

    def test_configuration_show(self):
        # Test show without option
        raw_output = self.fibostack('configuration show')
        items = self.parse_listing(raw_output)
        self.assert_table_structure(items, BASIC_CONFIG_HEADERS)

        cmd_output = self.fibostack('configuration show', parse_output=True)
        self.assertEqual(configuration.REDACTED, cmd_output['auth.password'])
        self.assertIn(
            'auth.password',
            cmd_output.keys(),
        )

        # Test show --mask
        cmd_output = self.fibostack(
            'configuration show --mask',
            parse_output=True,
        )
        self.assertEqual(configuration.REDACTED, cmd_output['auth.password'])

        # Test show --unmask
        cmd_output = self.fibostack(
            'configuration show --unmask',
            parse_output=True,
        )
        # If we are using os-client-config, this will not be set.  Rather than
        # parse clouds.yaml to get the right value, just make sure
        # we are not getting redacted.
        passwd = os.environ.get('OS_PASSWORD')
        if passwd:
            self.assertEqual(passwd, cmd_output['auth.password'])
        else:
            self.assertNotEqual(
                configuration.REDACTED, cmd_output['auth.password']
            )


class ConfigurationTestsNoAuth(base.TestCase):
    """Functional test for configuration with no auth"""

    def test_configuration_show(self):
        # Test show without option
        raw_output = self.fibostack(
            'configuration show',
            cloud=None,
        )
        items = self.parse_listing(raw_output)
        self.assert_table_structure(items, BASIC_CONFIG_HEADERS)

        cmd_output = self.fibostack(
            'configuration show',
            cloud=None,
            parse_output=True,
        )
        self.assertNotIn(
            'auth.password',
            cmd_output,
        )
