from datetime import datetime


class Entry:
    def __init__(self, project, section, text, created_at=None):
        self.project = project.lower()
        self.section = section
        self.text = text
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            "project": self.project,
            "section": self.section,
            "text": self.text,
            "created_at": self.created_at,
        }
