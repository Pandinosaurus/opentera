from modules.EventManager import EventManager
from libtera.db.models.TeraDevice import TeraDevice
from modules.DatabaseModule.DBManagerTeraDeviceAccess import DBManagerTeraDeviceAccess
import messages.python as messages


class DeviceEventManager(EventManager):
    def __init__(self, device: TeraDevice):
        EventManager.__init__(self)
        self.device = device
        self.accessManager = DBManagerTeraDeviceAccess(self.device)

    def filter_device_event(self, event: messages.DeviceEvent):
        # Only accept event for current device
        if event.device_uuid == self.device.device_uuid:
            return True

        # Not accessible
        return False

    def filter_join_session_event(self, event: messages.JoinSessionEvent):
        # TODO how do we verify the invitation
        return True

    def filter_participant_event(self, event: messages.ParticipantEvent):
        # TODO not sure what to do here...
        for participant in self.device.device_participants:
            if participant.participant_uuid == event.participant_uuid:
                return True

        # Not accessible
        return False

    def filter_stop_session_event(self, event: messages.StopSessionEvent):
        # TODO How to we keep track of session ids?
        return True

    def filter_user_event(self, event: messages.UserEvent):
        # Not accessible
        return False
