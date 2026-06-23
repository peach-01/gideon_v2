class AdvisorRouter:

    TASK_ADVISORS = {
        "reasoning":        "gemini",
        "planning":         "gemini",
        "coding":           "gemini",
        "memory":           "gemini",
        "summarization":    "gemini",
        "tool_use":         "gemini",
        "vision":           "gemini",
        "critic":           "gemini",
        "extraction":       "gemini",
    }

    def choose(self, task: str) -> str:
        return self.TASK_ADVISORS.get(task, "gemini")