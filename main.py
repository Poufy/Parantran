
from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
load_dotenv()
import boto3
import os
import openai
from pydantic import BaseModel

app = FastAPI()

class TextToTranslate(BaseModel):
    text: str

openai.api_key = os.getenv("OPENAI_SECRET_KEY")

def paraphrase_text(text, format):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=(f"Please rephrase the following text {format}: {text}"),
        temperature=0.7,
        max_tokens=1000
    )
    return response["choices"][0]["text"]
   
@app.post("/translate")
async def translate(testInput: TextToTranslate, request: Request):
    if(request.headers.get("api_key") != "mysecretkey"):
        raise HTTPException(status_code=400, detail="Invalid API key")
    
    source_language = "en"
    target_language = "ar"

    paraphrased_text = paraphrase_text(testInput.text, "in a formal way")
    client = boto3.client('translate', region_name='us-east-1', aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                      aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
    try:
        response = client.translate_text(Text=paraphrased_text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error translating text")
    
    return {"result": response["TranslatedText"], "paraphrased_text": paraphrased_text}
