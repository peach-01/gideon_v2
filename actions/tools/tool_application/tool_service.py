from actions.system.filesystem.filesystem import FileSystemTool
from actions.productivity.notes.notes import NotesTool
from actions.productivity.reminders.reminders import ReminderTool
from actions.productivity.calendar.calendar import CalendarTool
from actions.communication.email.email import EmailTool
from actions.system.system_monitor.system_monitor import SystemMonitorTool
from actions.system.web_search.web_search import WebSearchTool
from brain.frontal_lobe.goal_management.goals import GoalTool


class ToolService:

    def __init__(self, memory_service):
        self.memory = memory_service

        self.tools = {
            "filesystem": FileSystemTool(),
            "goals": GoalTool(memory_service=self.memory),
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