# Copyright 2018 Contributors to Hyperledger Sawtooth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

import logging
import unittest
from uuid import uuid4
import pytest
from rbac.legacy import addresser
from rbac.legacy.addresser import AddressSpace

LOGGER = logging.getLogger(__name__)


@pytest.mark.library
@pytest.mark.addressing
class TestSysAdminAdminsAddresser(unittest.TestCase):
    def test_det_sysadmin_admin_addr(self):
        """Tests that a specific admin_id generates the expected
        sysadmin admin address, and thus is probably deterministic.
        """

        admin_id = "966ab67317234df489adb4bc1f517b88"
        expected_address = "9f4448000000000000000000000000\
00000000000000000000000000000000000000f7"
        address = addresser.make_sysadmin_admins_address(admin_id)

        self.assertEqual(
            len(address), addresser.ADDRESS_LENGTH, "The address is 70 characters"
        )

        self.assertTrue(
            addresser.is_address(address), "The address is 70 character hexidecimal"
        )

        self.assertTrue(
            addresser.namespace_ok(address), "The address has correct namespace prefix"
        )

        self.assertTrue(
            addresser.is_family_address(address),
            "The address is 70 character hexidecimal with family prefix",
        )

        self.assertEqual(
            address, expected_address, "The address is the one we expected it to be"
        )

        self.assertEqual(
            addresser.address_is(address),
            AddressSpace.SYSADMIN_ADMINS,
            "The address created must be a SysAdmin Attributes address.",
        )

    def test_gen_sysadmin_admin_addr(self):
        """Tests the sysadmin admin address creation function as well as the
        address_is function.
        """

        admin_id = uuid4().hex
        address = addresser.make_sysadmin_admins_address(admin_id)

        self.assertEqual(
            len(address), addresser.ADDRESS_LENGTH, "The address is 70 characters"
        )

        self.assertTrue(
            addresser.is_address(address), "The address is 70 character hexidecimal"
        )

        self.assertTrue(
            addresser.namespace_ok(address), "The address has correct namespace prefix"
        )

        self.assertTrue(
            addresser.is_family_address(address),
            "The address is 70 character hexidecimal with family prefix",
        )

        self.assertEqual(
            addresser.address_is(address),
            AddressSpace.SYSADMIN_ADMINS,
            "The address created must be a SysAdmin Attributes address.",
        )
