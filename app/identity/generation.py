# -*- coding: utf-8 -*-
import random
from sqlmodel import Session, select
from app.database import GeneratedId
from .constants import ID_CHARACTERS

# Generates random 7 character human-readable ID
class TradeIdGenerator:
    def __init__(self):
        self._cached_ids = set()

    def generate(self, session: Session):
        generated_id = ''
        is_unique = False
        while not is_unique:
            for _ in range(7):
                generated_id = generated_id + random.choice(ID_CHARACTERS)
            if not self._is_id_unique(generated_id, session):
                self._store_id(generated_id, session)
                is_unique = True
            else:
                generated_id = ''
        return generated_id

    # Generates unique 7 character human-readable ID in bulk
    def generate_bulk(self, bulk_size, session: Session):
        generated_ids = set()
        for _ in range(bulk_size):
            generated_ids.add(self.generate(session))
        return generated_ids

    # Persists trade id in database
    def _store_id(self, trade_id: str, session: Session):
        new_trade_id = GeneratedId(trade_id)
        session.add(new_trade_id)
        session.commit()
        # add to set fo cached ids
        self._cached_ids.add(trade_id)

    # Check if the trade id is unique in the database
    def _is_id_unique(self, trade_id: str, session: Session) -> bool:
        statement = select(GeneratedId).where(GeneratedId.id == trade_id)
        result = session.exec(statement).first()
        return result is None