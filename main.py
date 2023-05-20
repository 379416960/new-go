from typing import Optional, List
from fastapi import FastAPI, File, UploadFile,Request
from pydantic import BaseModel
import uvicorn
import easydlsdk as edl
import datetime
import os
verifyCode  = edl.easyCode()

class Req(BaseModel):
    srcimg: str
    tsimg: str
    
class Result(BaseModel):
    err_code: int
    pos_right: int

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Name":"cindy"}

@app.post("/get_pos")
async def get_pos(*,request:Req, response_mode = Result):
    pos = verifyCode.getPos(request.srcimg, request.tsimg)
    if pos is True:
        return {"err_code":0, "pos_right":pos}
    return {"err_code":0, "pos_right":0}

@app.post("/send_images")
#async def update_item(request: Request,files: List[UploadFile] = File(...),response_mode = Result):
async def update_item(request: Request,file1: UploadFile,file2: UploadFile,response_mode = Result):
    dt_ms = datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f')
    lists = ['','']
    lists[0] = 'srcImgs/' + dt_ms + '.png'
    lists[1] = 'keyImgs/' + dt_ms + '.png'
    print(lists)
    with open(f'{lists[0]}','wb') as f:
       f.write(await file1.read())
    with open(f'{lists[1]}','wb') as f:
       f.write(await file2.read())
    # for i,file in enumerate(files):
    #     with open(f'{lists[i]}','wb') as f:
    #         f.write(await file.read())
    pos = verifyCode.getPos(lists[0],lists[1])
    for file in lists:
        os.unlink(file)
    print(pos)
    if pos:
        return {"err_code":0, "pos_right":pos}
    return {"err_code":1, "pos_right":0}


if __name__=="__main__":
     uvicorn.run("main:app", host="127.0.0.1", reload=True, port=8800, workers=20)
     #uvicorn main:app --reload --host=192.168.88.252 --port=8000  