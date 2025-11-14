from datetime import datetime
import pytz
import pandas as pd
from rapidfuzz import fuzz
from fastapi import HTTPException,status
import smtplib
from email.message import EmailMessage
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_time():
     return (
         datetime.utcnow()
         .replace(tzinfo=pytz.utc)
         .astimezone(pytz.timezone("Asia/Kolkata"))
     )


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)