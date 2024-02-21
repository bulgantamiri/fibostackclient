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


class TestAgent(common.NetworkTests):
    """Functional tests for network agent"""

    def setUp(self):
        super().setUp()

        if not self.is_extension_enabled("agent"):
            self.skipTest("No agent extension present")

    def test_network_agent_list_show_set(self):
        """Test network agent list, set, show commands

        Do these serially because show and set rely on the existing agent IDs
        from the list output and we had races when run in parallel.
        """

        # agent list
        agent_list = self.fibostack(
            'network agent list',
            parse_output=True,
        )
        self.assertIsNotNone(agent_list[0])

        agent_ids = list([row["ID"] for row in agent_list])

        # agent show
        cmd_output = self.fibostack(
            'network agent show %s' % agent_ids[0],
            parse_output=True,
        )
        self.assertEqual(
            agent_ids[0],
            cmd_output['id'],
        )

        if 'ovn' in agent_list[0]['Agent Type'].lower():
            # NOTE(slaweq): OVN Neutron agents can't be updated so test can be
            # finished here
            return

        # agent set
        raw_output = self.fibostack(
            'network agent set --disable %s' % agent_ids[0]
        )
        self.assertOutput('', raw_output)

        cmd_output = self.fibostack(
            'network agent show %s' % agent_ids[0],
            parse_output=True,
        )
        self.assertEqual(
            False,
            cmd_output['admin_state_up'],
        )

        raw_output = self.fibostack(
            'network agent set --enable %s' % agent_ids[0]
        )
        self.assertOutput('', raw_output)

        cmd_output = self.fibostack(
            'network agent show %s' % agent_ids[0],
            parse_output=True,
        )
        self.assertEqual(
            True,
            cmd_output['admin_state_up'],
        )


class TestAgentList(common.NetworkTests):
    """Functional test for network agent"""

    def setUp(self):
        super().setUp()

        if not self.is_extension_enabled("agent"):
            self.skipTest("No agent extension present")

    def test_network_dhcp_agent_list(self):
        """Test network agent list"""

        if not self.is_extension_enabled("dhcp_agent_scheduler"):
            self.skipTest("No dhcp_agent_scheduler extension present")

        # Get DHCP Agent ID
        cmd_output = self.fibostack(
            'network agent list --agent-type dhcp',
            parse_output=True,
        )
        if not cmd_output:
            self.skipTest("No agents with type=dhcp available")

        agent_id = cmd_output[0]['ID']

        name1 = uuid.uuid4().hex
        cmd_output = self.fibostack(
            'network create --description aaaa %s' % name1,
            parse_output=True,
        )

        self.addCleanup(self.fibostack, 'network delete %s' % name1)

        # Get network ID
        network_id = cmd_output['id']

        # Add Agent to Network
        self.fibostack(
            'network agent add network --dhcp %s %s' % (agent_id, network_id)
        )

        # Test network agent list --network
        cmd_output = self.fibostack(
            'network agent list --network %s' % network_id,
            parse_output=True,
        )

        # Cleanup
        # Remove Agent from Network
        self.fibostack(
            'network agent remove network --dhcp %s %s'
            % (agent_id, network_id)
        )

        # Assert
        col_name = [x["ID"] for x in cmd_output]
        self.assertIn(agent_id, col_name)

    def test_network_agent_list_routers(self):
        """Add agent to router, list agents on router, delete."""

        if not self.is_extension_enabled("l3_agent_scheduler"):
            self.skipTest("No l3_agent_scheduler extension present")

        name = uuid.uuid4().hex
        cmd_output = self.fibostack(
            'router create %s' % name,
            parse_output=True,
        )

        self.addCleanup(self.fibostack, 'router delete %s' % name)
        # Get router ID
        router_id = cmd_output['id']
        # Get l3 agent id
        cmd_output = self.fibostack(
            'network agent list --agent-type l3',
            parse_output=True,
        )

        # Check at least one L3 agent is included in the response.
        self.assertTrue(cmd_output)
        agent_id = cmd_output[0]['ID']

        # Add router to agent
        self.fibostack(
            'network agent add router --l3 %s %s' % (agent_id, router_id)
        )

        # Test router list --agent
        cmd_output = self.fibostack(
            'network agent list --router %s' % router_id,
            parse_output=True,
        )

        agent_ids = [x['ID'] for x in cmd_output]
        self.assertIn(agent_id, agent_ids)

        # Remove router from agent
        self.fibostack(
            'network agent remove router --l3 %s %s' % (agent_id, router_id)
        )
        cmd_output = self.fibostack(
            'network agent list --router %s' % router_id,
            parse_output=True,
        )
        agent_ids = [x['ID'] for x in cmd_output]
        self.assertNotIn(agent_id, agent_ids)