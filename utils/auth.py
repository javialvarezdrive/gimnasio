# utils/auth.py
import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Inicializar cliente de Supabase para autenticación
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_login():
    """Verifica si hay un monitor autenticado."""
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("Por favor inicie sesión para acceder a esta página")
        st.stop()
    return st.session_state.user

def login(email, password):
    """Inicia sesión del monitor."""
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        # Si la autenticación es correcta, buscamos también el monitor en la tabla
        monitor_response = supabase.table("monitores").select("*").eq("email", email).execute()
        if monitor_response.data:
            st.session_state.user = {
                "id": monitor_response.data[0]["id"],
                "nombre": monitor_response.data[0]["nombre"],
                "apellidos": monitor_response.data[0]["apellidos"],
                "email": email
            }
            st.session_state.logged_in = True
            return True, "Inicio de sesión exitoso"
        return False, "No se encontró información del monitor"
    except Exception as e:
        return False, f"Error de inicio de sesión: {str(e)}"

def logout():
    """Cierra la sesión."""
    supabase.auth.sign_out()
    st.session_state.logged_in = False
    if 'user' in st.session_state:
        del st.session_state.user

def register_monitor(nombre, apellidos, email, password):
    """Registra un nuevo monitor en el sistema."""
    try:
        # Crear usuario en el sistema de autenticación
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        # Crear registro del monitor en la tabla
        supabase.table("monitores").insert({
            "nombre": nombre,
            "apellidos": apellidos,
            "email": email
        }).execute()
        return True, "Monitor registrado exitosamente"
    except Exception as e:
        return False, f"Error al registrar: {str(e)}"
