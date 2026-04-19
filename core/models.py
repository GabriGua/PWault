from dataclasses import dataclass, field
import uuid

@dataclass
class Entry:
   name: str
   password: str
   id: uuid.UUID = field(default_factory=uuid.uuid4)
   username: str = None
   notes: str = None