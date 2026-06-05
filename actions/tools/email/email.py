from actions.tools.email.draft_model import Draft

class EmailTool:
    
    name = "email"


    def __init__(self):
        self.drafts = []


    def send_email(self):
        return NotImplementedError("Connect email provider later")


    def draft_email(self, recipient, subject, body):
        email = Draft(
            recipient=recipient,
            subject=subject,
            body=body,
        )
        
        self.drafts.append(email)
        
        return email


    def read_email(self):
        return []