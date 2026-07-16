from models.python.working_state.state import SessionState
import pickle

class StateManager:

    def __init__(self):
        self.sessions = {}


    async def boot(self):
        print("[STATE-MANAGER] Ready.")


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
    

    # ------------ SLEEP / WAKE SUPPORT ------------
    async def save_runtime_state(self, runtime_state):
        with open("runtime_state.pkl", "wb") as f:
            pickle.dump(runtime_state, f)        

        print("[STATE-MANAGER] Runtime snapshot saved.")


    async def load_runtime_state(self):
        try:
            with open("runtime_state.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None