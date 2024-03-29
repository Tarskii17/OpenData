
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from browser import launcher_for_data, launcher_for_table
from consts import url, json_columns_data, table_population, table_undernourishment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to allow requests from all domains (security precautions)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/maincounter-number")
async def read_main():
    res = await launcher_for_data(url, json_columns_data)
    return {"worldometer": res}


@app.get(f"/table/{table_population}")
async def read_main():
    res = await launcher_for_table(url+table_population)
    return {"result": res}


@app.get(f"/table/{table_undernourishment}")
async def read_main():
    res = await launcher_for_table(url+table_undernourishment)
    return {"result": res}
