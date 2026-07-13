class RouterUpdater:

    def __init__(self, advisor_router, store):
        self.advisor_router = advisor_router
        self.store = store


    def update_bias(self):
        totals = {}

        for h in self.store.history:
            model = h["model"]
            totals.setdefault(model, 0)
            totals[model] += h["reward"]

        for model, val in totals.items():
            self.advisor_router.memory_bias[model] = val * 0.01