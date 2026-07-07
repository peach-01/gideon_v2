from runtime.services.provider_model_service.model_registry import MODEL_REGISTRY
from runtime.services.provider_model_service.model_scoring_engine import ModelScorer


class AdvisorRouter:

    def __init__(self):
        self.registry = MODEL_REGISTRY
        self.memory_bias = {}       # learned adjustments


    def _apply_learning_bias(self, model, base_score):
        bias = self.memory_bias.get(model, 0.0)
        return base_score + bias


    def choose(self, task: str, preferences: dict = None):
        preferences = preferences or {}

        scored = []

        for model_name in self.registry:
            score = ModelScorer.score(task=task, model_name=model_name, registry=self.registry, preferences=preferences)
            score = self._apply_learning_bias(model_name, score)

            scored.append((model_name, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        return scored[0], scored