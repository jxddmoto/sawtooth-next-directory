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
"""Addresses and accesses proposal objects on the blockchain"""
from rbac.common import addresser
from rbac.common.base.base_address import AddressBase


class ProposalAddress(AddressBase):
    """Addresses and accesses proposal objects on the blockchain"""

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return addresser.AddressSpace.PROPOSALS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return addresser.ObjectType.PROPOSAL

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.ObjectType.SELF

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return addresser.RelationshipType.ATTRIBUTES


PROPOSAL_ADDRESS = ProposalAddress()

__all__ = ["PROPOSAL_ADDRESS"]
