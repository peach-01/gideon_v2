class AdvisorRouter:

    TASK_ADVISORS = {
        "reasoning":        "gpt",
        "planning":         "gpt",
        "coding":           "gpt",
        "memory":           "gpt",
        "summarization":    "gpt",
        "tool_use":         "gpt",
        "vision":           "gpt",
        "critic":           "gpt",
        "extraction":       "gpt",
    }

    def choose(self, task: str) -> str:
        return self.TASK_MODELS.get(task, "gpt")