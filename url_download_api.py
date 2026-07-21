from fastapi import FastAPI
from url_download import file_download
app = FastAPI()

@app.post("/upload/")
async def upload_and_downoad(url:str):
    result = file_download(url)
    return {"status":"success","data":result}
@app.get("/")
async def health_check():
    return {"status":"online","message":"Server is live and running."}