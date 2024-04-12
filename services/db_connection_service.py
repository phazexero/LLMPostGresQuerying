# services/my_service.py
from databases import Database
from repositories.print_settings_repository import get_ledger, get_group

async def get_ledger_service(db: Database, item_id: int):
    return await get_ledger(db, item_id)


async def check_group_service(db: Database, item_id: int):
    return await get_group(db, item_id)
