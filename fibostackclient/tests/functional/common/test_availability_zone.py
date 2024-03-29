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

from fibostackclient.tests.functional import base


class AvailabilityZoneTests(base.TestCase):
    """Functional tests for availability zone."""

    def test_availability_zone_list(self):
        cmd_output = self.fibostack(
            'availability zone list',
            parse_output=True,
        )
        zones = [x['Zone Name'] for x in cmd_output]
        self.assertIn('internal', zones)
        self.assertIn('nova', zones)
