import os
from dotenv import load_dotenv
import logging
load_dotenv()

class config:
  # Supabase Authentication Settings
  SUPABASE_URL = os.getenv("SUPABASE_URL")
  SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY") 
  SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
  VERIFY_JWT_SIGNATURE = os.getenv("VERIFY_JWT_SIGNATURE", "True").lower() == "true"
    
 # MongoDB connection
  DATABASE_URL = os.getenv("MONGO_URI") 
  DATABASE_NAME = os.getenv('DATABASE_NAME');
  # App Settings
  DEBUG = os.getenv("DEBUG", "True").lower() == "true"
  HOST = os.getenv("HOST", "0.0.0.0")
  PORT = int(os.getenv("PORT", "8000"))
  CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

print("=== CONFIG DEBUG ===")
print(f"DATABASE_URL: {config.DATABASE_URL}")
print(f"DATABASE_NAME: {config.DATABASE_NAME}")
print(f"SUPABASE_URL: {config.SUPABASE_URL}")
print(f"SUPABASE_JWT_SECRET: {'SET' if config.SUPABASE_JWT_SECRET else 'NOT SET'}")
print(f"DEBUG: {config.DEBUG}")
print(f"CORS_ORIGINS: {config.CORS_ORIGINS}")
print("==================")

config = config()

