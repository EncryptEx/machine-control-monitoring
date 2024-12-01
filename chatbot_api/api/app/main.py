from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import json

from llm import LLM

app = FastAPI()


from fastapi.middleware.cors import CORSMiddleware
origins = ["http://localhost:3000", None, "null"]  

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():
    return {"its working!"}



@app.post("/chatbot")
async def send_info(request: Request):

    data = await request.json()                                                                                                                                                                                                                                                                                                                                 
    question = data.get("user_input")
    info_sensors = data.get("sensors_info")
    
    llm = LLM()
    response, action, parameter = llm.ask(question, info_sensors) 

    ret = {"answer": response}
    if action:
        ret["action"] = action
        if parameter:
            ret["parameter"] = parameter
            
    return ret

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")

