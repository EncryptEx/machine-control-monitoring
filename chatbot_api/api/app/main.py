from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import json

app = FastAPI()


# Serve the HTML page
@app.get("/")
def root():
    return {"hi"}


# Endpoint to receive the POST request
@app.post("/send")
async def send_info(request: Request):
    data = await request.json()
    user_text = data.get("user_input")

    info_sensors = data.get("sensors_info")
    
    # query to llama

    # Prepare a JSON response to be sent back
    response_data = {
        "original_text": user_text,
        "original_sensors": info_sensors
    }

    return response_data


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")

