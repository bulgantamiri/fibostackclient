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

import fixtures

from fibostackclient.tests.functional.volume import base as volume_base


class BaseVolumeTests(volume_base.BaseVolumeTests):
    """Base class for Volume functional tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.haz_volume_v1 = cls.is_service_enabled('block-storage', '1.0')

    def setUp(self):
        super().setUp()

        if not self.haz_volume_v1:
            self.skipTest("No Volume v1 service present")

        ver_fixture = fixtures.EnvironmentVariable(
            'OS_VOLUME_API_VERSION', '1'
        )
        self.useFixture(ver_fixture)
