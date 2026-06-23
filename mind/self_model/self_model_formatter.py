class SelfModelFormatter:

    @staticmethod
    def format(snapshot: dict):
        beliefs = "\n".join(
            f"- {b.content} ({b.confidence:.2f})"
            for b in snapshot.beliefs[:25]    
        )

        experiences = "\n".join(
            f"- {e.content}"
            for e in snapshot.experiences[-10:]    
        )

        identity = snapshot.identity

        values = "\n".join(
            f"- {k}: {v}"
            for k, v in snapshot.values    
        )


        return f"""
            IDENTITY
                Name: {identity["identity"]["name"]}
                Version: {identity["identity"]["version"]}

            PURPOSE
                {identity["purpose"]}

            MISSION
                {identity["mission"]}

            CORE VALUES
                {values}

            BELIEFS
                {beliefs or "None"}

            RECENT EXPERIENCES
                {experiences or "None"}
        """