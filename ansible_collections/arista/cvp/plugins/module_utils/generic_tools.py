#!/usr/bin/env python
# coding: utf-8 -*-
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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class CvElement(object):

    def __init__(self, cv_data: dict):
        self.__cv_data = cv_data

    @property
    def name(self):
        if 'name' in self.__cv_data:
            return self.__cv_data['name']
        return None

    @property
    def key(self):
        if 'key' in self.__cv_data:
            return self.__cv_data['key']

    @property
    def data(self):
        return self.__cv_data
