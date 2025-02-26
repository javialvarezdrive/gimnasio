# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Esto cargará variables del archivo .env si lo tienes localmente

# Si estamos en Streamlit Cloud usaremos st.secrets, de lo contrario usaremos .env o valores por defecto
try:
    import streamlit as st
    SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
except Exception as e:
    SUPABASE_URL = os.getenv("SUPABASE_URL", "https://piahnkbbkxtbvmvzxtqa.supabase.co")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpYWhua2Jia3h0YnZtdnp4dHFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA1NTQ2NzcsImV4cCI6MjA1NjEzMDY3N30.oOjENjB2bUileOHelp138Gg6l2JDzP7YuuNHArhapa8")
    
APP_NAME = "Gestión de Gimnasio"
