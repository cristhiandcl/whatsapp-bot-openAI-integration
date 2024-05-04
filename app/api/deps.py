from fastapi import Request, Depends
from typing import Annotated
from app.database.mongo_config import mongo_collection
from openai_tools_gpt import ToolsGPT

context = [{"role"   : "system",
            "content": """You are Jarvis, my personal assistant expert on coding stuff, 
            I work on a mac with python most of the time, so unless the language is specified, 
            assume you are always asked about an implementation in python, you also answer question about general topics"""}]


async def get_whatsapp_data(request: Request):
    body = await request.json()
    container = body["entry"][0]["changes"][0]["value"]

    if container.get("messages"):
        contact: str = container["messages"][0]["from"]
        message: str = container["messages"][0]["text"]["body"]
        return {"contact": contact, "message": message}

    return None


ContactData = Annotated[dict | None, Depends(get_whatsapp_data)]


async def get_mongo_data(contact_data: ContactData):
    if contact_data:
        contact_historical = []

        pipeline = [
            {"$match": {"contact": contact_data["contact"]}},  # Filter by client_id
            {"$sort": {"_id": -1}},  # Sort by _id in descending order to get the latest documents
            {"$limit": 4},  # Limit to the last two documents
            {"$sort": {"_id": 1}}  # Sort by _id in ascending order to reverse the order of the last two documents
        ]

        async for record in mongo_collection.aggregate(pipeline):
            contact_historical.append({"role": "user", "content": record["query"]})
            contact_historical.append({"role": "assistant", "content": record["answer"]})

        return {"history": contact_historical} | contact_data

    return None


MongoData = Annotated[dict | None, Depends(get_mongo_data)]


async def jarvis_gpt(contact_data: MongoData):
    if contact_data:
        if contact_data["history"]:
            context.extend(contact_data["history"])

        return {"gpt"    : ToolsGPT(memory=context, with_memory=True),
                "contact": contact_data["contact"],
                "message": contact_data["message"]}

    return None


GPT = Annotated[ToolsGPT, Depends(jarvis_gpt)]
