TOOL_SCHEMAS = [

    # --------------- NOTES ----------------
    {
        "type": "function",
        "function": {
            "name": "create_note",
            "description": "Create a note",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                    "category": {"type": "string"},
                },
                "required": ["title", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_note",
            "description": "Read a note",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "category": {"type": "string"},
                },
                "required": ["title", "category"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_notes",
            "description": "Search notes by text query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                },
                "required": ["query"]
            }
        }
    },

    # --------------- REMINDERS ----------------
    {
        "type": "function",
        "function": {
            "name": "create_reminder",
            "description": "Create a reminder",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "message": {"type": "string"},
                    "due_at": {"type": "string"},
                },
                "required": ["title", "due_at"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_reminders",
            "description": "List all reminders",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_reminder",
            "description": "Delete a reminder",
            "parameters": {
                "type": "object",
                "properties": {
                    "reminder_id": {"type": "string"},
                },
                "required": ["reminder_id"]
            }
        }
    },

    # --------------- CALENDAR ----------------
    {
        "type": "function",
        "function": {
            "name": "create_event",
            "description": "Create a calendar event",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "start": {"type": "string"},
                    "end": {"type": "string"},
                },
                "required": ["title", "start", "end"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_events",
            "description": "List calendar events",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_event",
            "description": "Update an existing event",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string"},
                    "title": {"type": "string"},
                    "start": {"type": "string"},
                    "end": {"type": "string"},
                },
                "required": ["event_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_event",
            "description": "Delete a calendar event",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string"},
                },
                "required": ["event_id"]
            }
        }
    },

    # --------------- GOALS ----------------
    {
        "type": "function",
        "function": {
            "name": "create_goal",
            "description": "Create a goal",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {"type": "number"},
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_goals",
            "description": "List goals",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_goal",
            "description": "Mark a goal as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal_id": {"type": "string"},
                },
                "required": ["goal_id"]
            }
        }
    },

    # --------------- EMAIL ----------------
    {
        "type": "function",
        "function": {
            "name": "draft_email",
            "description": "Create an email draft",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["recipient", "subject", "body"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_email",
            "description": "Read emails",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },

    # --------------- FILE SYSTEM ----------------
    {
        "type": "function",
        "function": {
            "name": "save_document",
            "description": "Save a structured project document",
            "parameters": {
                "type": "object",
                "properties": {
                    "project": {"type": "string"},
                    "discipline": {"type": "string"},
                    "doc_type": {"type": "string"},
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                    "revision": {"type": "string"},
                    "ext": {"type": "string"}
                },
                "required": [
                    "project",
                    "discipline",
                    "doc_type",
                    "title",
                    "content"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List directory contents",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "exists",
            "description": "Check whether a file exists",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Delete a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        }
    },

    # --------------- TIMERS ----------------
    {
        "type": "function",
        "function": {
            "name": "start_timer",
            "description": "Start a timer",
            "parameters": {
                "type": "object",
                "properties": {
                    "seconds": {"type": "number"}
                },
                "required": ["seconds"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_timer",
            "description": "Cancel a timer",
            "parameters": {
                "type": "object",
                "properties": {
                    "timer_id": {"type": "string"}
                },
                "required": ["timer_id"]
            }
        }
    },

    # --------------- SYSTEM MONITOR ----------------
    {
        "type": "function",
        "function": {
            "name": "get_cpu_usage",
            "description": "Get current CPU utilization percentage",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ram_usage",
            "description": "Get current RAM utilization percentage",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_disk_usage",
            "description": "Get current disk utilization percentage",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_battery",
            "description": "Get battery status",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_network",
            "description": "Get network I/O statistics",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "full_status",
            "description": "Get full system status",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
]