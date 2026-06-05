import json
from pathlib import Path


class IdentityService:

    def __init__(self):
        identity_file = Path(__file__).parents[2] / "mind" / "self_model" / "identity.json"

        with open(identity_file, "r") as f:
            self.identity = json.load(f)

    @property
    def name(self):
        return self.identity["name"]

    @property
    def version(self):
        return self.identity["version"]

    def system_prompt(self) -> str:
        principles = "\n".join(f"- {p}" for p in self.identity["principles"])
        personality = "\n".join(f"- {k}: {v}" for k, v in self.identity["personality"].items())
        behavior = "\n".join(f"- {b}" for b in self.identity["behavior"])

        return f"""
            You are {self.name}.

            Version:
            {self.version}

            Purpose:
            {self.identity["identity"]["purpose"]}

            Mission:
            {self.identity["identity"]["mission"]}

            Principles:
            {principles}

            Personality:
            {personality}

            Behavior:
            {behavior}

            Tool Usage Instructions:
                You have access to tools.

                When a tool is required:
                - Call the appropriate tool.
                - Never claim an action succeeded until the tool succeeds.
                - Use tool results when generating your response.

                Never pretend an action was completed.
                Always call the tool first.
                Only confirm completion after tool execution succeeds.
            """