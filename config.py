import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env (si existe)
load_dotenv()

# Configuración de Supabase usando los valores proporcionados como valor por defecto
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://piahnkbbkxtbvmvzxtqa.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpYWhua2Jia3h0YnZtdnp4dHFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA1NTQ2NzcsImV4cCI6MjA1NjEzMDY3N30.oOjENjB2bUileOHelp138Gg6l2JDzP7YuuNHArhapa8")

# Configuración de la aplicación
APP_NAME = "Gestión de Gimnasio"