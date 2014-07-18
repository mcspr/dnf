# Copyright (C) 2014  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import dnf.exceptions
import dnf.pycomp
import dnf.cli.commands.updateinfo
import shutil
import tempfile
import tests.mock
import tests.support
import unittest


class UpdateInfoCommandTest(unittest.TestCase):

    """Test case validating updateinfo commands."""

    def setUp(self):
        """Prepare the test fixture."""
        super(UpdateInfoCommandTest, self).setUp()
        cachedir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, cachedir)
        self.cli = tests.support.MockBase().mock_cli()
        self.cli.base.add_test_dir_repo('rpm', cachedir)
        self._stdout = dnf.pycomp.StringIO()
        self.addCleanup(tests.mock.patch.stopall)
        tests.support.mock.patch(
            'dnf.cli.commands.updateinfo._',
            dnf.pycomp.NullTranslations().ugettext).start()
        tests.support.mock.patch(
            'dnf.cli.commands.updateinfo.print',
            self._stub_print, create=True).start()

    def _stub_print(self, *objects):
        """Pretend to print to standard output."""
        print(*objects, file=self._stdout)

    def test_run_available(self):
        """Test running with available advisories."""
        cmd = dnf.cli.commands.updateinfo.UpdateInfoCommand(self.cli)
        cmd.run([])
        self.assertEqual(self._stdout.getvalue(),
                         'Updates Information Summary: available\n'
                         '    1 Security notice(s)\n',
                         'incorrect output')

    def test_run_list(self):
        """Test running the list sub-command."""
        cmd = dnf.cli.commands.updateinfo.UpdateInfoCommand(self.cli)
        cmd.run(['list'])
        self.assertEqual(self._stdout.getvalue(),
                         'DNF-2014-3 security tour-5-1.noarch\n',
                         'incorrect output')

    def test_run_info(self):
        """Test running the info sub-command."""
        cmd = dnf.cli.commands.updateinfo.UpdateInfoCommand(self.cli)
        cmd.run(['info'])
        updated = datetime.datetime.fromtimestamp(1404841143)
        self.assertEqual(self._stdout.getvalue(),
                         '========================================'
                         '=======================================\n'
                         '  tour-5-1\n'
                         '========================================'
                         '=======================================\n'
                         '  Update ID : DNF-2014-3\n'
                         '       Type : security\n'
                         '    Updated : ' + str(updated) + '\n'
                         'Description : testing advisory\n'
                         '\n',
                         'incorrect output')

    def test_run_invalid(self):
        """Test running with invalid arguments."""
        cmd = dnf.cli.commands.updateinfo.UpdateInfoCommand(self.cli)
        self.assertRaises(dnf.exceptions.Error, cmd.run, ['fail'])