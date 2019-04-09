import unittest
from libtera.db.Base import db
from libtera.db.DBManager import DBManager
from libtera.db.models.TeraDevice import TeraDevice
from libtera.db.models.TeraUser import TeraUser
from libtera.db.models.TeraParticipant import TeraParticipant
from libtera.db.models.TeraParticipantGroup import TeraParticipantGroup
from libtera.db.models.TeraSite import TeraSite
from libtera.db.models.TeraProject import TeraProject
from libtera.db.models.TeraSiteAccess import TeraSiteAccess
from libtera.db.models.TeraProjectAccess import TeraProjectAccess
from libtera.db.Base import db
import uuid
import os
from passlib.hash import bcrypt


class TeraDeviceTest(unittest.TestCase):

    filename = 'TeraDeviceTest.db'

    SQLITE = {
        'filename': filename
    }

    db_man = DBManager()

    def setUp(self):
        if os.path.isfile(self.filename):
            print('removing database')
            os.remove(self.filename)

        self.db_man.open_local(self.SQLITE)
        # Creating default users / tests.
        self.db_man.create_defaults()

    def test_defaults(self):
        pass


