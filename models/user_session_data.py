import random

class UserSessionData(object):

    def __init__(self, user_id):
        self.user_id = user_id
    
        self.example_vad_note_buffer = []
        self.example_vad_chat_buffer = []
        # connect to trident, ...

        self.joined_room = None
        self.username = "default_" + user_id

    def do_stt_for_long_chat(self, audio_chunk: bytes):
        # call VAD STT models here
        return random.random()

    def do_stt_for_take_note(self, audio_chunk: bytes):
        # call VAD STT models here
        n = random.random()
        return n, n >= 0.9

    def on_clean(self):
        # clean data
        # disconnect to trident, ...
        pass

    def join_room(self, room, username):
        self.joined_room = room
        self.username = username

    def leave_room(self):
        self.joined_room = None
        self.username = "default_" + self.user_id


class UserSesssionDataManager(object):

    def __init__(self):
        self.user_to_data = {}

    def get(self, user_id):
        if user_id in self.user_to_data:
            return self.user_to_data[user_id]
        return None

    def create(self, user_id):
        self.user_to_data[user_id] = UserSessionData(user_id)

    def clean(self, user_id):
        if user_id in self.user_to_data:
            self.user_to_data[user_id].on_clean()
            del self.user_to_data[user_id]