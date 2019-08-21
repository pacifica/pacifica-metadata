#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test script to run the command interface for testing.

We need to actually run the tests here using pytest.


- pip install pacifica-metadata==0.3.1 'elasticsearch<7'
- export METADATA_CPCONFIG="$PWD/server.conf"
- export PEEWEE_URL="postgres://postgres:@localhost/pacifica_metadata_upgrade"
- pacifica-metadata-cmd dbsync
- >
  pushd $(mktemp -d);
  pacifica-metadata --stop-after-a-moment & METADATA_PID=$!;
  curl -Lo data.zip https://github.com/pacifica/pacifica-metadata/archive/v0.3.1.zip;
  unzip data.zip; pushd pacifica-metadata-0.3.1;
  curl --connect-timeout 10 localhost:8121/users;
  python tests/test_files/loadit_test.py; wait $METADATA_PID;
  popd; popd; sudo service elasticsearch stop;
- cd tests
- pip install ..
- >
  coverage run --include='*/site-packages/pacifica/metadata/*' core/cmd_test.py dbchk --equal;
  ret_val=$?;
  if [[ $ret_val == 0 ]] ; then exit -1; fi;
- >
  coverage run --include='*/site-packages/pacifica/metadata/*' -a core/cmd_test.py dbchk;
  ret_val=$?;
  if [[ $ret_val == 0 ]] ; then exit -1; fi;
- coverage run --include='*/site-packages/pacifica/metadata/*' -a core/cmd_test.py dbsync;
- coverage run --include='*/site-packages/pacifica/metadata/*' -a core/cmd_test.py dbchk;
- coverage run --include='*/site-packages/pacifica/metadata/*' -a core/cmd_test.py dbchk --equal;
- >
  export PEEWEE_URL="sqliteext:///db.sqlite3";
  coverage run --include='*/site-packages/pacifica/metadata/*' -a core/cmd_test.py dbsync;
  export PEEWEE_URL="postgres://postgres:@localhost/pacifica_metadata";
- coverage run --include='*/site-packages/pacifica/metadata/*' -a core/cmd_test.py dbsync;
- coverage run --include='*/site-packages/pacifica/metadata/*' -a core/cmd_test.py dbsync;
- coverage run --include='*/site-packages/pacifica/metadata/*' -a core/cmd_test.py dbchk;

"""
import sys
import os
import zipfile
from unittest import TestCase
from tempfile import mkdtemp
from shutil import rmtree
try:
    import sh
except ImportError:
    import pbs

    class Sh(object):
        """Sh style wrapper."""

        def __getattr__(self, attr):
            """Return command object like sh."""
            return pbs.Command(attr)

        # pylint: disable=invalid-name
        @staticmethod
        def Command(attr):
            """Return command object like sh."""
            return pbs.Command(attr)
    sh = Sh()
import peewee
import requests
from pacifica.metadata.admin_cmd import main
from pacifica.metadata.orm.globals import DB
from pacifica.metadata.orm.sync import MetadataSystem
from pacifica.metadata.orm import ORM_OBJECTS, Relationships


class AdminCmdBase(object):
    """Test base class for setting up update environments."""

    virtualenv_dir = mkdtemp()
    testdata_dir = mkdtemp()
    virtualenv_bindir = 'Scripts' if sys.platform == 'win32' else 'bin'
    python_venv_cmd = os.path.join(virtualenv_dir, virtualenv_bindir, os.path.basename(sys.executable))
    python_cmd = sh.Command(sys.executable)

    # this is for unittest and pytest
    # pylint: disable=invalid-name
    @classmethod
    def setUpClass(cls):
        """Setup the datadir so we can import data."""
        resp = requests.get('https://github.com/pacifica/pacifica-metadata/archive/v0.3.1.zip')
        assert resp.status_code == 200
        if not os.path.isdir(cls.testdata_dir):
            os.makedirs(cls.testdata_dir)
        zip_path = os.path.join(cls.testdata_dir, 'data.zip')
        dest_path = os.path.join(cls.testdata_dir, 'src')
        with open(zip_path, 'wb') as data_fd:
            data_fd.write(resp.content)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_path)

    @classmethod
    def tearDownClass(cls):
        """Undo all the state we have."""
        rmtree(cls.testdata_dir)

    def setUp(self):
        """Setup a virtualenv and install the original version."""
        self.python_cmd('-m', 'virtualenv', '--python', sys.executable,
                        self.virtualenv_dir, _out=sys.stdout, _err=sys.stderr)

    def tearDown(self):
        """Undo all the state we have."""
        rmtree(self.virtualenv_dir)
        DB.drop_tables(ORM_OBJECTS)
        DB.drop_tables([MetadataSystem])
        DB.close()
    # pylint: enable=invalid-name

    @classmethod
    def _install_package(cls, *pkg_names):
        """Install a package into virtualenv."""
        sh.Command(cls.python_venv_cmd)('-m', 'pip', 'install', *pkg_names, _out=sys.stdout, _err=sys.stderr)

    @classmethod
    def _upgrade_package(cls, *pkg_names):
        """Install a package into virtualenv."""
        sh.Command(cls.python_venv_cmd)('-m', 'pip', 'install', '--upgrade',
                                        *pkg_names, _out=sys.stdout, _err=sys.stderr)

    @classmethod
    def _install_metadata(cls, version, update=True):
        cls._install_package('pacifica-metadata=={}'.format(version))
        if update:
            cls._update_db()

    @classmethod
    def _update_db(cls):
        sh.Command(cls.python_venv_cmd)(
            '-c', 'import sys; from pacifica.metadata.admin_cmd import main; sys.exit(main())', 'dbsync')

    @classmethod
    def _load_metadata(cls):
        """Start CherryPy and load the data."""
        sh.Command(cls.python_venv_cmd)('-m', 'pacifica.metadata',
                                        '--stop-after-a-moment', _bg=True, _out=sys.stdout, _err=sys.stderr)

    @classmethod
    def _upgrade_path(cls, *versions):
        cls._upgrade_package('pip', 'setuptools', 'wheel')
        cls._install_package('elasticsearch<7')
        for version in versions:
            cls._install_metadata(version)

    @classmethod
    def setup_upgrade_path(cls, *versions, **kwargs):
        """Decorator to execute an upgrade path to setup a test."""
        dbsync = kwargs.get('dbsync', True)

        def real_decorator(func):
            """real decorator we use on the function."""
            def wrapper(*args, **kwargs):
                """Apply the upgrade path specified and update database models."""
                cls._upgrade_path(*versions)
                if dbsync:
                    main('dbsync')
                return func(*args, **kwargs)
            return wrapper
        return real_decorator


class TestUpgradePaths(AdminCmdBase, TestCase):
    """Test some upgrade paths."""

    @AdminCmdBase.setup_upgrade_path('0.3.1')
    def test_full_upgrade(self):
        """Test the full upgrade."""
        with self.assertRaises(peewee.DoesNotExist):
            Relationships.select().where(Relationships.name == 'something_not_there').get()
        self.assertEqual(Relationships.select().where(Relationships.name == 'principal_investigator').get().name, 'principal_investigator')

    @AdminCmdBase.setup_upgrade_path('0.3.1', '0.10.3')
    def test_partial_upgrade(self):
        """Test the full upgrade."""
        with self.assertRaises(peewee.DoesNotExist):
            Relationships.select().where(Relationships.name == 'principle_investigator').get()
        self.assertEqual(Relationships.select().where(Relationships.name == 'principal_investigator').get().name, 'principal_investigator')


class TestAdminChk(AdminCmdBase, TestCase):
    """Test the admin chk commands to get coverage."""

    @AdminCmdBase.setup_upgrade_path('0.3.1', dbsync=False)
    def test_admin_chk(self):
        """Check the database and admin commands return values."""
        self.assertEqual(main('dbchk'), -1, 'the dbchk command should exit -1 with out of date db')
        self.assertEqual(main('dbchk', '--equal'), -1, 'the dbchk equal command should exit -1 with out of date db')
        self.assertEqual(main('dbsync'), 0, 'The return code for dbsync should be success')
        self.assertEqual(main('dbsync'), 0, 'The return code for dbsync a second time is also good')
        self.assertEqual(main('dbchk'), 0, 'The return code for dbchk should be success')
        self.assertEqual(main('dbchk', '--equal'), 0, 'The return code for dbchk should be success')
        self.assertEqual(Relationships.select().where(Relationships.name == 'principal_investigator').get().name, 'principal_investigator')
