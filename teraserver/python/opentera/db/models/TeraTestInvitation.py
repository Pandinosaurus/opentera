import random
import time
import hashlib
from datetime import datetime, timezone

from sqlalchemy import Column, ForeignKey, Integer, String, Sequence, TIMESTAMP
from sqlalchemy.orm import relationship

from opentera.db.Base import BaseModel
from opentera.db.SoftDeleteMixin import SoftDeleteMixin


class TeraTestInvitation(BaseModel, SoftDeleteMixin):
    """
    Storing invitation keys and parameters for tests invitations.
    """
    __tablename__ = 't_tests_invitations'
    id_test_invitation = Column(Integer, Sequence('id_test_invitation_sequence'), primary_key=True, autoincrement=True)
    id_test_type = Column(Integer, ForeignKey("t_tests_types.id_test_type", ondelete='cascade'), nullable=False)
    id_session = Column(Integer, ForeignKey("t_sessions.id_session", ondelete='cascade'), nullable=True)


    id_user = Column(Integer, ForeignKey("t_users.id_user", ondelete='cascade'), nullable=True)
    id_participant = Column(Integer, ForeignKey("t_participants.id_participant", ondelete='cascade'),
                                           nullable=True)
    id_device = Column(Integer, ForeignKey("t_devices.id_device", ondelete='cascade'), nullable=True)

    test_invitation_key = Column(String(16), nullable=False, unique=True,
                                 default=lambda : TeraTestInvitation.generate_test_invitation_unique_key())
    test_invitation_max_count = Column(Integer, nullable=False, default=1)
    test_invitation_count = Column(Integer, nullable=False, default=0)

    test_invitation_creation_date = Column(TIMESTAMP(timezone=True), nullable=False,
                                           default=lambda: datetime.now(tz=timezone.utc))
    test_invitation_expiration_date = Column(TIMESTAMP(timezone=True), nullable=False)

    test_invitation_message = Column(String, nullable=True)

    # Relationships
    test_invitation_test_type = relationship("TeraTestType")
    test_invitation_session = relationship("TeraSession")
    test_invitation_user = relationship("TeraUser")
    test_invitation_participant = relationship("TeraParticipant")
    test_invitation_device = relationship("TeraDevice")

    def to_json(self, ignore_fields=None, minimal=False):
        if ignore_fields is None:
            ignore_fields = []

        ignore_fields.extend(['test_invitation_test_type',
                              'test_invitation_session'
                              'test_invitation_user',
                              'test_invitation_participant',
                              'test_invitation_device'])

        json_value =  super().to_json(ignore_fields=ignore_fields)

        # Add uuids for convenience
        json_value['test_invitation_test_type_uuid'] = None
        json_value['test_invitation_session_uuid'] = None
        json_value['test_invitation_user_uuid'] = None
        json_value['test_invitation_participant_uuid'] = None
        json_value['test_invitation_device_uuid'] = None

        if self.test_invitation_test_type:
            json_value['test_invitation_test_type_uuid'] = self.test_invitation_test_type.test_type_uuid
        if self.test_invitation_session:
            json_value['test_invitation_session_uuid'] = self.test_invitation_session.session_uuid
        if self.test_invitation_user:
            json_value['test_invitation_user_uuid'] = self.test_invitation_user.user_uuid
        if self.test_invitation_participant:
            json_value['test_invitation_participant_uuid'] = self.test_invitation_participant.participant_uuid
        if self.test_invitation_device:
            json_value['test_invitation_device_uuid'] = self.test_invitation_device.device_uuid

        return json_value


    @staticmethod
    def create_defaults(test=False):
        if test:
           pass

    @staticmethod
    def get_test_invitation_by_id(test_invitation_id: int, with_deleted: bool = False):
        return TeraTestInvitation.query.execution_options(include_deleted=with_deleted)\
            .filter_by(id_test_invitation=test_invitation_id).first()

    @staticmethod
    def get_test_invitation_by_key(invitation_key: str, with_deleted: bool = False):
        return TeraTestInvitation.query.execution_options(include_deleted=with_deleted)\
            .filter_by(test_invitation_key=invitation_key).first()

    @staticmethod
    def generate_test_invitation_unique_key() -> str:
        """
        Generate a unique key of 16 hexadecimal number for a test invitation based on current time.
        """
        timestamp = str(time.time_ns())

        # Generate a 6-digit random number
        random_seed = str(random.randint(0,999999)).zfill(6)

        # Hash the timestamp + seed using SHA-256
        # Hashing: The hashlib.sha256 function ensures that the output is evenly distributed,
        # making the key appear random.
        hash_object = hashlib.sha256((timestamp + random_seed).encode())

        # Return the first 16 characters of the hash
        # This method ensures the key is not only time-based but also includes additional randomness,
        # further reducing the likelihood of collisions.
        return hash_object.hexdigest()[:16]


    def to_json_create_event(self):
        """
        Create event is sent from DBManager to clients when a new test invitation is created.
        """
        return self.to_json(minimal=True)

    def to_json_update_event(self):
        """
        Update event is sent from DBManager to clients when a test invitation is updated.
        """
        return self.to_json(minimal=True)

    def to_json_delete_event(self):
        """
        Delete event is sent from DBManager to clients when a test invitation is deleted.
        """
        # Minimal information, delete can not be filtered
        return {'id_test_invitation': self.id_test_type, 'test_invitation_key': self.test_invitation_key}

    @classmethod
    def insert(cls, test_invitation):
        """
        Insert a new test invitation into the database. An unique key is generated for the test invitation.
        """
        # Make sure to generate a unique key
        test_invitation.test_invitation_key = TeraTestInvitation.generate_test_invitation_unique_key()
        super().insert(test_invitation)
