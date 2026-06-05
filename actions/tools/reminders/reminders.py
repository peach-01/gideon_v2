import uuid
from datetime import datetime

from actions.tools.reminders.reminder_model import Reminder


class ReminderTool:

    name = "reminders"

    def __init__(self):
        self.reminders = []

    def create_reminder(self, title, message, due_at):
        reminder = Reminder(
            id=str(uuid.uuid4()),
            title=title,
            message=message,
            due_at=due_at,
            completed=False,
        )

        self.reminders.append(reminder)

        return reminder

    def list_reminders(self):
        return self.reminders
    
    def delete_reminder(self, reminder_id):
        self.reminders = [
            r for r in self.reminders
            if r.id != reminder_id
        ]

        return True