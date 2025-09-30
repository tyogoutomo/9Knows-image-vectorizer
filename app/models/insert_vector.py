from pydantic import BaseModel
from fastapi import UploadFile, File, Form

class VectorizeItem(BaseModel):
    file: UploadFile = File(...),
    label: str = Form("NOT 99 Group Related")