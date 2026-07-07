from runtime.services.provider_model_service.advisor_router import AdvisorRouter
from runtime.services.provider_model_service.router_learning import RouterLearningStore
from runtime.services.provider_model_service.router_updater import RouterUpdater
from runtime.services.provider_model_service.model_registry import MODEL_REGISTRY


class IntelligentRouter:

    def __init__(self):
        self.advisor_router = AdvisorRouter()
        self.store = RouterLearningStore()
        self.updater = RouterUpdater(self.advisor_router, self.store)


    def route(self, task, preferences=None):
        (best_model, score), ranked = self.advisor_router.choose(task, preferences)

        return {
            "model": best_model,
            "provider": MODEL_REGISTRY[best_model]["provider"],
            "score": score,
            "ranked": ranked,
        }
    

    def learn(self, task, model, success, latency, score):
        self.store.record(task, model, score, success, latency)
        self.updater.update_bias()