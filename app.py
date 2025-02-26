# app.py
import streamlit as st
from utils.auth import login, logout

from config import APP_NAME

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title(f"🏋️ {APP_NAME}")

    # Sidebar para login o información del monitor
    with st.sidebar:
        if 'logged_in' in st.session_state and st.session_state.logged_in:
            st.success(f"Sesión iniciada como: {st.session_state.user['nombre']} {st.session_state.user['apellidos']}")
            if st.button("Cerrar Sesión"):
                logout()
                st.experimental_rerun()
        else:
            st.subheader("Iniciar Sesión")
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Contraseña", type="password")
                submit = st.form_submit_button("Iniciar Sesión")
                if submit:
                    success, message = login(email, password)
                    if success:
                        st.success(message)
                        st.experimental_rerun()
                    else:
                        st.error(message)

    # Navegación a las páginas (se muestra el contenido según la pestaña seleccionada)
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        pages = {
            "Usuarios": "pages/usuarios.py",
            "Actividades": "pages/actividades.py",
            "Calendario": "pages/calendario.py",
            "Reportes": "pages/reportes.py",
            "Configuración": "pages/configuracion.py"
        }
        selection = st.sidebar.radio("Navegar", list(pages.keys()))
        page = pages[selection]
        with open(page, "r", encoding="utf8") as f:
            code = compile(f.read(), page, 'exec')
            exec(code, globals())
    else:
        st.info("Por favor inicie sesión para acceder al sistema.")

if __name__ == "__main__":
    main()
