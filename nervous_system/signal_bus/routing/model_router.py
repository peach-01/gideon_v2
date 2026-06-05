class ModelRouter:

    TASK_MODELS = {
        "reasoning":        "o3",
        "planning":         "o3",
        "coding":           "gpt-4.1",
        "memory":           "gpt-4o-mini",
        "summarization":    "gpt-4o-mini",
        "tool_use":         "gpt-4.1",
        "vision":           "gpt-4.1",
        "critic":           "o3",
    }

    def choose(self, task: str) -> str:
        return self.TASK_MODELS.get(task, "gpt-4.1")