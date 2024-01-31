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

import fixtures

from fibostackclient.tests.functional.image import base


class ImageTests(base.BaseImageTests):
    """Functional tests for Image commands"""

    def setUp(self):
        super(ImageTests, self).setUp()

        ver_fixture = fixtures.EnvironmentVariable('OS_IMAGE_API_VERSION', '2')
        self.useFixture(ver_fixture)

        self.name = uuid.uuid4().hex
        self.image_tag = 'my_tag'
        self.image_tag1 = 'random'
        output = self.fibostack(
            'image create --tag {tag} {name}'.format(
                tag=self.image_tag, name=self.name
            ),
            parse_output=True,
        )
        self.image_id = output["id"]
        self.assertOutput(self.name, output['name'])

    def tearDown(self):
        try:
            self.fibostack('image delete ' + self.image_id)
        finally:
            super().tearDown()

    def test_image_list(self):
        output = self.fibostack('image list', parse_output=True)
        self.assertIn(self.name, [img['Name'] for img in output])

    def test_image_list_with_name_filter(self):
        output = self.fibostack(
            'image list --name ' + self.name,
            parse_output=True,
        )
        self.assertIn(self.name, [img['Name'] for img in output])

    def test_image_list_with_status_filter(self):
        output = self.fibostack(
            'image list --status active',
            parse_output=True,
        )
        self.assertIn('active', [img['Status'] for img in output])

    def test_image_list_with_tag_filter(self):
        output = self.fibostack(
            'image list --tag '
            + self.image_tag
            + ' --tag '
            + self.image_tag1
            + ' --long',
            parse_output=True,
        )
        for taglist in [img['Tags'] for img in output]:
            self.assertIn(self.image_tag, taglist)
            self.assertIn(self.image_tag1, taglist)

    def test_image_attributes(self):
        """Test set, unset, show on attributes, tags and properties"""

        # Test explicit attributes
        self.fibostack(
            'image set '
            + '--min-disk 4 '
            + '--min-ram 5 '
            + '--public '
            + self.name
        )
        output = self.fibostack(
            'image show ' + self.name,
            parse_output=True,
        )
        self.assertEqual(
            4,
            output["min_disk"],
        )
        self.assertEqual(
            5,
            output["min_ram"],
        )
        self.assertEqual(
            'public',
            output["visibility"],
        )

        # Test properties
        self.fibostack(
            'image set '
            + '--property a=b '
            + '--property c=d '
            + '--property hw_rng_model=virtio '
            + '--public '
            + self.name
        )
        output = self.fibostack(
            'image show ' + self.name,
            parse_output=True,
        )
        self.assertIn("a", output["properties"])
        self.assertIn("c", output["properties"])

        self.fibostack(
            'image unset '
            + '--property a '
            + '--property c '
            + '--property hw_rng_model '
            + self.name
        )
        output = self.fibostack(
            'image show ' + self.name,
            parse_output=True,
        )
        self.assertNotIn("a", output["properties"])
        self.assertNotIn("c", output["properties"])

        # Test tags
        self.assertNotIn('01', output["tags"])
        self.fibostack('image set ' + '--tag 01 ' + self.name)
        output = self.fibostack(
            'image show ' + self.name,
            parse_output=True,
        )
        self.assertIn('01', output["tags"])

        self.fibostack('image unset ' + '--tag 01 ' + self.name)
        output = self.fibostack(
            'image show ' + self.name,
            parse_output=True,
        )
        self.assertNotIn('01', output["tags"])

    def test_image_set_rename(self):
        name = uuid.uuid4().hex
        output = self.fibostack(
            'image create ' + name,
            parse_output=True,
        )
        image_id = output["id"]
        self.assertEqual(
            name,
            output["name"],
        )
        self.fibostack('image set ' + '--name ' + name + 'xx ' + image_id)
        output = self.fibostack(
            'image show ' + name + 'xx',
            parse_output=True,
        )
        self.assertEqual(
            name + 'xx',
            output["name"],
        )

    # TODO(dtroyer): This test is incomplete and doesn't properly test
    #                sharing images.  Fix after the --shared option is
    #                properly added.
    def test_image_members(self):
        """Test member add, remove, accept"""
        output = self.fibostack(
            'token issue',
            parse_output=True,
        )
        my_project_id = output['project_id']

        output = self.fibostack(
            'image show -f json ' + self.name,
            parse_output=True,
        )
        # NOTE(dtroyer): Until fsc supports --shared flags in create and set
        #                we can not properly test membership.  Sometimes the
        #                images are shared and sometimes they are not.
        if output["visibility"] == 'shared':
            self.fibostack(
                'image add project ' + self.name + ' ' + my_project_id
            )
            # self.addCleanup(
            #     self.fibostack,
            #     'image remove project ' +
            #     self.name + ' ' +
            #     my_project_id
            # )

            self.fibostack('image set ' + '--accept ' + self.name)
            output = self.fibostack(
                'image list -f json ' + '--shared',
                parse_output=True,
            )
            self.assertIn(self.name, [img['Name'] for img in output])

            self.fibostack('image set ' + '--reject ' + self.name)
            output = self.fibostack(
                'image list -f json ' + '--shared',
                parse_output=True,
            )
            # self.assertNotIn(
            #     self.name,
            #     [img['Name'] for img in output]
            # )

            self.fibostack(
                'image remove project ' + self.name + ' ' + my_project_id
            )

        # else:
        #     # Test not shared
        #     self.assertRaises(
        #         image_exceptions.HTTPForbidden,
        #         self.fibostack,
        #         'image add project ' +
        #         self.name + ' ' +
        #         my_project_id
        #     )
        #     self.fibostack(
        #         'image set ' +
        #         '--share ' +
        #         self.name
        #     )
