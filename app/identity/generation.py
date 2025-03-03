# -*- coding: utf-8 -*-
import random
import time
from typing import List, Set
from sqlmodel import Session, select
from app.database import GeneratedId
from .constants import ID_CHARACTERS
from app.dependencies import cached_ids

# Generates unique human-readable ID
class TradeIdGenerator:
    def __init__(self):
        
        # Pre-calculate character set length for optimization
        self.valid_char_length = len(ID_CHARACTERS)
        self.id_length = 7
        """retry logic for concurrent access."""
        self.max_retries = 10
        self.retry_count = 0
    

    def generate(self, session: Session) -> str:
        for _ in range(self.max_retries):
            generated_id = ''
            for _ in range(self.id_length):
                generated_id = generated_id + random.choice(ID_CHARACTERS)
            if self._is_id_unique(generated_id, session):
                self._save_id(generated_id, session)
                return generated_id
        # If we've exhausted retries, raise an error
        raise RuntimeError(f"Failed to generate a unique trade ID after {self.max_retries} attempts")

    # Generates unique human-readable IDs in bulk
    def generate_bulk(self, bulk_size, session: Session) -> list[str]:
        if (len(ID_CHARACTERS) ** self.id_length) < bulk_size:
            return []

        if bulk_size > 9999:
            return self._generate_bulk_optimized(bulk_size=bulk_size, session=session)

        generated_ids = []
        for _ in range(bulk_size):
            generated_ids.append(self.generate(session))
        return generated_ids
    
    """Optmized method for generating large numbers of IDs"""
    def _generate_bulk_optimized(self, bulk_size: int, session: Session) -> list[str]:
        result_ids = []

        # Use multiple timestamp patterns to distribute IDs
        timestamp_patterns = []
        base_ms = int(time.time() * 1000) % 1000

        """Create several timestamp patterns based on the current time
        and a range of offsets to distribute IDs better"""
        for offset in range(min(100, bulk_size // 10000 + 1)):
            ms = (base_ms + offset) % 1000
            timestamp_patterns.append(self._encode_timestamp(ms))
        
        # Generate batches of candidate IDs
        batch_size = min(100000, bulk_size)
        remaining = bulk_size

        while remaining > 0 and timestamp_patterns:
            # Take the next timestamp pattern
            ts_pattern = timestamp_patterns.pop(0)

            # Generate a batch of candidate IDs with this timestamp pattern
            candidates = set()
            for _ in range(min(batch_size, remaining * 2)):
                random_part = ''.join(random.choice(ID_CHARACTERS) for _ in range(5))
                candidate_id = ts_pattern + random_part
                candidates.add(candidate_id[:self.id_length])

            # Filter out IDs that are already used by checking against DB
            new_ids = []
            for candidate in candidates:
                if self._is_id_unique(trade_id=candidate, session=session):
                    new_ids.append(candidate)
                if len(new_ids) >= remaining:
                    break

            # Store the new IDs in the database in a batch operation
            if new_ids:
                for id in new_ids:
                    session.add(GeneratedId(id=id))
                session.commit()
            
                # Update local cache
                cached_ids.update(new_ids)

                # Add to results
                result_ids.extend(new_ids)
                remaining -= len(new_ids)

            """ If this timestamp pattern didn't yield enough IDs,
            generate a new timestamp pattern """
            if remaining > 0 and not timestamp_patterns:
                new_ms = (base_ms + random.randint(100,999)) % 1000
                timestamp_patterns.append(self._encode_timestamp(new_ms))

        if len(result_ids) < bulk_size:
            raise RuntimeError(f"Could only generate {len(result_ids)} unique IDs out of {bulk_size} requested")
            
        return result_ids
    
    # Encode a timestamp into a short alphanumeric string
    def _encode_timestamp(self, timestamp_ms: int) -> str:
        # Use modulo to ensure we stay within our character set
        first_char = ID_CHARACTERS[timestamp_ms % self.valid_char_length]
        second_char = ID_CHARACTERS[(timestamp_ms // self.valid_char_length) % self.valid_char_length]
        return first_char + second_char



    # Persists trade id in database
    def _save_id(self, trade_id: str, session: Session) -> GeneratedId:
        new_trade_id = GeneratedId(id=trade_id)
        session.add(new_trade_id)
        session.commit()
        # add to set fo cached ids
        cached_ids.add(trade_id)
        return new_trade_id

    # Check if the trade id is unique
    def _is_id_unique(self, trade_id: str, session: Session) -> bool:
        # first check local cached ids
        if trade_id in cached_ids:
            return False
        # if trade id is not in the cache, query the database
        statement = select(GeneratedId).where(GeneratedId.id == trade_id)
        result = session.exec(statement).first()
        return result is None