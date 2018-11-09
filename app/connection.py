
class Connection:

    def __init__(_, socket):
        _.socket = socket
        _.history_id = None

    # Emits data to a socket's unique room
    def emit(self, event, data):
        emit(event, data, room=self.sid)