import os
import sys

from sqlmodel import SQLModel, Session, StaticPool, create_engine

from app.identity.generation import TradeIdGenerator

trade_id_generator = TradeIdGenerator()

sqlite_file_name = "testing.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool)

SQLModel.metadata.create_all(engine)
with Session(engine) as session:
    while True:
        for id in trade_id_generator.generate_bulk(bulk_size=10, session=session):
            sys.stdout.write('%s\n' % id)
