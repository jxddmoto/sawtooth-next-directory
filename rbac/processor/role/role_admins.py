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
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from rbac.common import addresser

from rbac.common.protobuf import proposal_state_pb2
from rbac.common.protobuf import role_transaction_pb2

from rbac.processor.role import role_validator
from rbac.processor import proposal_validator, state_change

from rbac.processor.role import role_operation

LOGGER = logging.getLogger(__name__)


def apply_propose(header, payload, state):
    role_admins_payload = role_transaction_pb2.ProposeAddRoleAdmin()
    role_admins_payload.ParseFromString(payload.content)

    role_admins_address = addresser.role.admin.address(
        role_admins_payload.role_id, role_admins_payload.user_id
    )

    proposal_address = addresser.proposal.address(
        object_id=role_admins_payload.role_id, target_id=role_admins_payload.user_id
    )

    state_entries = role_validator.validate_role_rel_proposal(
        header, role_admins_payload, role_admins_address, state
    )

    if not proposal_validator.has_no_open_proposal(
        state_entries=state_entries,
        object_id=role_admins_payload.role_id,
        related_id=role_admins_payload.user_id,
        proposal_address=proposal_address,
        proposal_type=proposal_state_pb2.Proposal.ADD_ROLE_ADMIN,
    ):
        raise InvalidTransaction(
            "There is already an open proposal for ADD_ROLE_ADMIN "
            "with role id {} and user id {}".format(
                role_admins_payload.role_id, role_admins_payload.user_id
            )
        )

    state_change.propose_role_action(
        state_entries=state_entries,
        header=header,
        payload=role_admins_payload,
        address=proposal_address,
        proposal_type=proposal_state_pb2.Proposal.ADD_ROLE_ADMIN,
        state=state,
    )


def apply_propose_remove(header, payload, state):
    role_admins_payload = role_transaction_pb2.ProposeRemoveRoleAdmin()
    role_admins_payload.ParseFromString(payload.content)

    role_admins_address = addresser.role.admin.address(
        role_admins_payload.role_id, role_admins_payload.user_id
    )

    proposal_address = addresser.proposal.address(
        object_id=role_admins_payload.role_id, target_id=role_admins_payload.user_id
    )

    state_entries = role_validator.validate_role_rel_proposal(
        header, role_admins_payload, role_admins_address, state, True
    )

    if not proposal_validator.has_no_open_proposal(
        state_entries=state_entries,
        object_id=role_admins_payload.role_id,
        related_id=role_admins_payload.user_id,
        proposal_address=proposal_address,
        proposal_type=proposal_state_pb2.Proposal.REMOVE_ROLE_ADMIN,
    ):
        raise InvalidTransaction(
            "There is already an open proposal for REMOVE_ROLE_ADMIN "
            "with role id {} and user id {}".format(
                role_admins_payload.role_id, role_admins_payload.user_id
            )
        )

    state_change.propose_role_action(
        state_entries=state_entries,
        header=header,
        payload=role_admins_payload,
        address=proposal_address,
        proposal_type=proposal_state_pb2.Proposal.REMOVE_ROLE_ADMIN,
        state=state,
    )


def apply_confirm(header, payload, state):

    confirm_payload = role_transaction_pb2.ConfirmAddRoleAdmin()
    confirm_payload.ParseFromString(payload.content)

    role_admin_address = addresser.role.admin.address(
        confirm_payload.role_id, confirm_payload.user_id
    )

    txn_signer_admin_address = addresser.role.admin.address(
        confirm_payload.role_id, header.signer_public_key
    )

    state_entries = role_validator.get_state_entries(
        header=header,
        confirm=confirm_payload,
        txn_signer_rel_address=txn_signer_admin_address,
        state=state,
    )

    state_change.confirm_role_action(
        state_entries=state_entries,
        header=header,
        confirm=confirm_payload,
        role_rel_address=role_admin_address,
        state=state,
    )


def apply_reject(header, payload, state):
    reject_payload = role_transaction_pb2.RejectAddRoleAdmin()
    reject_payload.ParseFromString(payload.content)

    txn_signer_admin_address = addresser.role.admin.address(
        reject_payload.role_id, header.signer_public_key
    )

    state_entries = role_validator.get_state_entries(
        header=header,
        confirm=reject_payload,
        txn_signer_rel_address=txn_signer_admin_address,
        state=state,
    )

    state_change.reject_role_action(
        state_entries, header, reject=reject_payload, state=state
    )


def apply_confirm_remove(header, payload, state):
    raise RuntimeError(
        "apply_confirm_remove not implemented! Args: {0},{1},{2}".format(
            header, payload, state
        )
    )


def apply_reject_remove(header, payload, state):
    raise RuntimeError(
        "apply_reject_remove not implemented! Args: {0},{1},{2}".format(
            header, payload, state
        )
    )


def hierarchical_approve(header, payload, state):
    hierarchical_decide(header, payload, state, True)


def hierarchical_reject(header, payload, state):
    hierarchical_decide(header, payload, state, False)


def hierarchical_decide(header, payload, state, isApproval):
    confirm = role_transaction_pb2.ConfirmAddRoleAdmin()
    confirm.ParseFromString(payload.content)

    txn_signer_admin_address = addresser.role.admin.address(
        confirm.role_id, confirm.on_behalf_id
    )

    role_operation.hierarchical_decide(
        header, confirm, state, txn_signer_admin_address, isApproval
    )
