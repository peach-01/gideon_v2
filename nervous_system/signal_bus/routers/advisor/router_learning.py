class RouterLearningStore:

    def __init__(self): 
        self.history = []        # replace w/ a DB later


    def record(self, task, model, score, success, latency):
        reward = 0.0

        # simple reward function
        if success:
            reward += 1.0
        if latency < 1.0:
            reward += 0.2
        if score > 0.8:
            reward += 0.3

        self.history.append({
            "task": task,
            "model": model,
            "reward": reward,
        })

        return reward