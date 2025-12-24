from core.database import engine
from core.models import Base
from core.checkpoints import BaseCheckpoint


def init_db():
    Base.metadata.create_all(bind=engine)
    BaseCheckpoint.metadata.create_all(bind=engine)

