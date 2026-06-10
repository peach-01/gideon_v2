from datetime import datetime, UTC

from mind.beliefs.belief_model import Belief
from mind.beliefs.belief_store import BeliefStore


class BeliefService:

    def __init__(self):
        self.store = BeliefStore()
        self.beliefs = self.store.load()


    def all(self):
        return self.beliefs
    

    def add(self, statement: str, domain: str, source: str, confidence: float=0.5, evidence: list[str] | None = None):
        belief = Belief(
            statement=statement, 
            domain=domain,
            source=source,
            confidence=confidence, 
            evidence=evidence or []
        )

        self.beliefs.append(belief)
        self.store.save(self.beliefs)

        return belief
    

    def find(self, statement: str):
        for belief in self.beliefs:
            if belief.statement == statement:
                return belief
            
        return None
    

    def reinforce(self, statement: str, evidence: str, delta: float=0.05):
        belief = self.find(statement=statement)
        if not belief:
            return None
        
        belief.confidence = min(1.0, belief.confidence + delta)
        belief.evidence.append(evidence)
        belief.last_reviewed = datetime.now(UTC)

        self.store.save(self.beliefs)

        return belief
    

    def contradict(self, statement: str, contradiction: str, delta: float=1.0):
        belief = self.find(statement=statement)
        if not belief:
            return None
        
        belief.confidence = max(0.0, belief.confidence - delta)
        belief.contradictions.append(contradiction)
        belief.last_reviewed = datetime.now(UTC)

        self.store.save(self.beliefs)

        return belief