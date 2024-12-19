from sqlalchemy import TIMESTAMP, VARCHAR, Column, Integer
from config.database import Base

app_name = "bot"


class LogModel(Base):
    __tablename__ = "log"

    id = Column(
        Integer, nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    created_at = Column(TIMESTAMP, nullable=False)
    user_request = Column(VARCHAR, nullable=False)
    bot_response = Column(VARCHAR, nullable=False)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)
