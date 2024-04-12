# routes/__init__.py

# third party libraries

# routes/my_route.py
from fastapi import APIRouter, Depends, Header

from databases import Database
from config.db.database import get_database
from services.db_connection_service import get_ledger_service, check_group_service
from services.fields_checker import check_ledger_name, check_group
from services.llm_calling_service import chat_output, json_extractor
from dotenv import load_dotenv
import os

load_dotenv()

TogetherAPIKEY = os.environ["TOGETHER_API_KEY"]
MODEL_NAME = os.environ["MODEL_NAME"]

# Create a central router
router = APIRouter()

@router.post("/create_ledger/{user_prompt}")
async def read_item(
    user_prompt: str,
    org_id: int | None = Header(),
    db: Database = Depends(get_database),
):
    try:
        org_data = await check_group_service(db, org_id)
        ledger_data = await get_ledger_service(db, org_id)
        model_json_data = json_extractor(
            chat_output(TogetherAPIKEY, MODEL_NAME, user_prompt)
        )
        try:
            group_data = check_group(org_data, model_json_data)
            ledger_name = model_json_data["ledger_name"]
            if group_data is not True:
                if check_ledger_name(ledger_data, ledger_name) is False:
                    return f"Group name does not exist. Choose group name from: {group_data}. Ledger name {ledger_name} already exists." # Hit required API
                return f"Group name does not exist. Choose group name from: {group_data}" # Hit required API
            else: 
                if check_ledger_name(ledger_data, ledger_name) is False:
                    return f"Ledger name {ledger_name} already exists." # Hit required API
                else:
                    return "Ledger Created"
        except Exception as e:
            raise ValueError(f"Error: {e}")
    except Exception as e:
        raise str(e)
    
@router.post("/group_option_choices/")
async def check_item(ledger_name: str, 
                     group_name: str, 
                     org_id: int | None = Header(),
                     db: Database = Depends(get_database)
                     ):
    try:
        if ledger_name: 
            ledger_data = await get_ledger_service(db, org_id)
            if check_ledger_name(ledger_data, ledger_name):
                if group_name:
                    return("Ledger Created") #Group name passed from front end to tbe returned
            else:
                return "Enter ledger name again."
    except Exception as e:
        raise e

        


# Export the central router
__all__ = ["router"]
