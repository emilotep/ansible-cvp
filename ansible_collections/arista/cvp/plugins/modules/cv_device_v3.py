#!/usr/bin/python
# coding: utf-8 -*-
# pylint: disable=bare-except
# pylint: disable=dangerous-default-value
# flake8: noqa: W503
#
# GNU General Public License v3.0+
#
# Copyright 2019 Arista Networks AS-EMEA
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
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: cv_container
version_added: "2.9"
author: EMEA AS Team (@aristanetworks)
short_description: Manage Provisioning topology.
description:
  - CloudVision Portal Configlet configuration requires a dictionary of containers with their parent,
    to create and delete containers on CVP side.
  - Returns number of created and/or deleted containers
options:
  topology:
    description: Yaml dictionary to describe intended containers
    required: true
    type: dict
  cvp_facts:
    description: Facts from CVP collected by cv_facts module
    required: true
    type: dict
'''

EXAMPLES = r'''
- name: Create container topology on CVP
  hosts: cvp
  connection: local
  gather_facts: no
  vars:
    verbose: False
    containers:
        Fabric:
            parent_container: Tenant
        Spines:
            parent_container: Fabric
            configlets:
                - container_configlet
            images:
                - 4.22.0F
            devices:
                - veos01
  tasks:
    - name: "Build Container topology on {{inventory_hostname}}"
      cv_container:
        topology: "{{containers}}"
        state: present
      register: CVP_CONTAINERS_RESULT
'''

import logging
import traceback
import ansible_collections.arista.cvp.plugins.module_utils.logger   # noqa # pylint: disable=unused-import
from ansible.module_utils.basic import AnsibleModule
import ansible_collections.arista.cvp.plugins.module_utils.tools_cv as tools_cv
import ansible_collections.arista.cvp.plugins.module_utils.schema as schema
from ansible_collections.arista.cvp.plugins.module_utils.device_tools import CvDeviceTools, DeviceInventory
try:
    from cvprac.cvp_client_errors import CvpClientError, CvpApiError, CvpRequestError  # noqa # pylint: disable=unused-import
    HAS_CVPRAC = True
except ImportError:
    HAS_CVPRAC = False
    CVPRAC_IMP_ERR = traceback.format_exc()


# Ansible module preparation
ansible_module: AnsibleModule

MODULE_LOGGER = logging.getLogger('arista.cvp.cv_device_v3')
MODULE_LOGGER.info('Start cv_device_v3 module execution')


def check_import():
    """
    check_import Check all imports are resolved
    """
    if HAS_CVPRAC is False:
        ansible_module.fail_json(
            msg='cvprac required for this module. Please install using pip install cvprac')

    if not schema.HAS_JSONSCHEMA:
        ansible_module.fail_json(
            msg="JSONSCHEMA is required. Please install using pip install jsonschema")


if __name__ == '__main__':
    """
    Main entry point for module execution.
    """
    argument_spec = dict(
        # Topology to configure on CV side.
        devices=dict(type='list', required=True),
        state=dict(type='str',
                   required=False,
                   default='present',
                   choices=['present', 'absent'])
    )

    # Make module global to use it in all functions when required
    ansible_module = AnsibleModule(argument_spec=argument_spec,
                                   supports_check_mode=True)
    # Instantiate ansible results
    result = dict(changed=False, data={}, failed=False)
    result['data']['taskIds'] = list()
    result['data']['tasks'] = list()

    if ansible_module.params['state'] == 'absent':
        ansible_module.fail_json(msg='State==absent is not yet supported !')

    # Test all libs are correctly installed
    check_import()

    # Test user input against schema definition
    user_topology = DeviceInventory(data=ansible_module.params['devices'])

    if user_topology.is_valid:
        ansible_module.fail_json(
            msg='Error, your input is not valid against current schema:\n {}'.format(ansible_module.params['devices']))

    # Create CVPRAC client
    cv_client = tools_cv.cv_connect(ansible_module)

    # Instantiate data
    cv_topology = CvDeviceTools(
        cv_connection=cv_client, ansible_module=ansible_module, check_mode=ansible_module.check_mode)

    result['data'] = cv_topology.manager(user_inventory=user_topology)
    result['changed'] = result['data']['changed']


    ansible_module.exit_json(**result)