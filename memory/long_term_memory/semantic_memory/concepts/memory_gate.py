import re
from dataclasses import dataclass


@dataclass
class MemoryGate:

    min_len: int = 20

    high_priority_patterns = {
        "remember", "always remember",
        "don't forget", "do not forget", "never forget",
        "important",
        "my name is",
        "i started",
        "i was diagnosed",
    }

    keywords = {
        "my",
        "i am", "i'm",
        "i like", "i love", "i hate", "i prefer", "i think", "i believe",
        "remember",
        "goal", "project",
        "always", "never",
        "family",
        "work", "job", "career",
        "mission", "task", "objective",
    }

    trivial_messages = {
        "hi", "hello", "hey",
        "thanks", "thank you",
        "good morning", "good night", "good afternoon",
        "cool", "awesome", "nice",
        "ok", "okay", "yes", "no", "maybe",
    }


    def should_extract(self, user_msg: str, gideon_msg: str | None = None) -> bool:
        text = user_msg.strip().lower()

        if text in self.high_priority_patterns:
            return True

        if text in self.trivial_messages:
            return False
        
        if len(text) < self.min_len:
            return False
        
        if any(keyword in text for keyword in self.keywords):
            return True
        
        if "?" in text:
            return False
        
        # extract personal statements
        if re.search(r"\bi\s+(have|want|need|use|own|live|work|study)\b", text):
            return True
        
        return False