from actions.tools.filesystem.filesystem import FileSystemTool
from actions.tools.notes.notes import NotesTool
from actions.tools.reminders.reminders import ReminderTool
from actions.tools.calendar.calendar import CalendarTool
from actions.tools.email.email import EmailTool
from actions.tools.system_monitor.system_monitor import SystemMonitorTool
from actions.tools.web_search.web_search import WebSearchTool
from brain.frontal_lobe.goal_management.goals import GoalTool


class ToolService:

    def __init__(self):
        self.tools = {
            "filesystem": FileSystemTool(),
            "goals": GoalTool(),
            "notes": NotesTool(),
            "reminders": ReminderTool(),
            "calendar": CalendarTool(),
            "email": EmailTool(),
            "system_monitor": SystemMonitorTool(),
            "web_search": WebSearchTool(),
        }

    def get_tool(self, name):
        return self.tools.get(name)
    
    def get_func_map(self):
        routes = {}

        for tool in self.tools.values():
            for attr in dir(tool):
                if attr.startswith("_"):
                    continue

                func = getattr(tool, attr)

                if callable(func):
                    routes[attr] = func

        return routes