from brain.cortex.state_manager import SessionState

class StateManager:

    def __init__(self):
        self.sessions = {}

    def get_state(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState()

        return self.sessions[session_id]

    def update(self, session_id: str, **updates):
        state = self.get_state(session_id=session_id)

        for k, v in updates.items():
            if hasattr(state, k):
                setattr(state, k, v)

        return state