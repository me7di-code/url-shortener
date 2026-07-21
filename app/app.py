from ssl import ALERT_DESCRIPTION_UNSUPPORTED_EXTENSION
from pydantic import functional_serializers
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from typing import Annotated, Literal
from pydantic import BaseModel, Field
import secrets
import string

class Shortener(BaseModel):
    url: str


app = FastAPI()
urls = {
}

@app.post("/short")
def shorten(url :Shortener):
    base62_chars = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(base62_chars) for _ in range(6))

    if url.url in urls.values():
        return "Link already assigned"
    urls[code] = url.url
    return urls

@app.post("/update/{code}")
def update_link(code:str, url:str):
    if code not in urls:
        return "This code isnt available to update"
    urls[code] = url
    return f"Code update to URL {url}"



@app.get("/all")
def fetch():
    return urls

@app.get("/{code}")
def redirect(code :str):
    if code not in urls:
        return "Link doesnt exist. Short it first"
    url = urls[code]
    return RedirectResponse(f"https://{url}")

@app.delete("/delete/{code}")
def delete_link(code: str):
    url = urls[code]
    if code not in urls:
        return "Link doesnt exist"
    urls.pop(code)
    return f"URL deleted {url}"




    

