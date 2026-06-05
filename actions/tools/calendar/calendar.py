import uuid
from actions.tools.calendar.event_model import Event


class CalendarTool:

    name = "calendar"

    schema = {
        "create_event": {
            "title": "string",
            "content": "string",
            "category": "string",
        }
    }

    def __init__(self):
        self.events = []


    def create_event(self, title, start, end):
        event = Event(
            id=str(uuid.uuid4()),
            title=title,
            start=start,
            end=end,
        )

        self.events.append(event)

        return event
    
    
    def list_events(self):
        return self.events
    

    def update_event(self, event_id, **updates):
        for event in self.events:
            if event.id == event_id:
                for k, v in updates.items():
                    if hasattr(event, k):
                        setattr(event, k, v)

                return event
    

    def delete_event(self, event_id):
        self.events = [
            e for e in self.events
            if e.id != event_id
        ]

        return True