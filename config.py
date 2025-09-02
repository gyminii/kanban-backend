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


app_config = config()

