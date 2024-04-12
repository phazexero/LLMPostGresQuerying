# db/repositories/print_settings_repository.py
from databases import Database
from config.db.queries import GET_LEDGER_QUERY, GROUP_QUERY


async def get_ledger(db: Database, org_id: int):
    return await db.fetch_all(GET_LEDGER_QUERY, values={"org_id": org_id})


async def get_group(db: Database, org_id: int):
    return await db.fetch_all(GROUP_QUERY, values={"org_id": org_id})
