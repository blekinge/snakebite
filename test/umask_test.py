# -*- coding: utf-8 -*-
# Copyright (c) 2014 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

from snakebite.errors import DirectoryException, FileException
from minicluster_testbase import MiniClusterTestBase

class UmaskTest(MiniClusterTestBase):
    counter = 0


    def setUp(self):
        self.client.umask = 0o077

    @classmethod
    def get_fresh_filename(cls, prefix="/"):
        cls.counter+=1
        return "%sumask_foobar%d" % (prefix, cls.counter)

    def test_touchz_umask(self):
        f1 = self.get_fresh_filename()
        result = all([ r['result'] for r in self.client.touchz([f1]) ])
        self.assertTrue(result)
        perm = self.cluster.ls([f1])[0]['permission']
        # 0o600 == 0o666 & ~self.client.umask
        self.assertEqual(perm, 0o600)

    def test_touchz_mkdir(self):
        parent_dir = '/'
        d1 = self.get_fresh_filename(parent_dir)
        result = all([ r['result'] for r in self.client.mkdir([d1]) ])
        self.assertTrue(result)
        perms = [entry['permission'] for entry in self.cluster.ls([parent_dir]) if entry['path'] == d1]
        # 0o700 == 0o777 & ~self.client.umask
        self.assertEqual(perms[0], 0o700)
