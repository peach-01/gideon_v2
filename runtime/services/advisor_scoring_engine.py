class ModelScorer:

    WEIGHTS = {
        "quality":  0.55,
        "latency":  0.25,
        "cost":     0.20,
    }


    @staticmethod
    def score(task: str, model_name: str , registry: dict, preferences: dict):
        m = registry[model_name]

        task_match = 1.0 if task in m["strengths"] else 0.6

        quality = m["quality"] * task_match
        latency = 1.0 - m["latency"]        # lower latency == better
        cost = 1.0 - m["cost"]            # lower cost == better

        # user/system preferences override
        w = preferences.get("weights", ModelScorer.WEIGHTS)

        score = (
            w["quality"] * quality +
            w["latency"] * latency +
            w["cost"] * cost
        )

        return score