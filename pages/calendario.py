# pages/calendario.py
import streamlit as st
from datetime import datetime, timedelta
from utils.auth import check_login
from utils.database import get_actividades
from utils.helpers import generate_activity_calendar
from streamlit_calendar import calendar
import plotly.express as px

def main():
    check_login()
    st.title("Calendario de Actividades")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        mes = st.selectbox("Mes", list(range(1, 13)), index=datetime.now().month-1)
    with col2:
        año = st.selectbox("Año", list(range(datetime.now().year-1, datetime.now().year+3)), index=1)
    with col3:
        vista = st.selectbox("Vista", ["Mensual", "Semanal", "Diaria"])
        
    if vista == "Mensual":
        fecha_inicio = datetime(año, mes, 1)
        if mes == 12:
            fecha_fin = datetime(año+1, 1, 1) - timedelta(days=1)
        else:
            fecha_fin = datetime(año, mes+1, 1) - timedelta(days=1)
    elif vista == "Semanal":
        fecha_inicio = datetime(año, mes, 1)
        fecha_fin = fecha_inicio + timedelta(days=6)
    else:  # Diaria
        fecha_inicio = datetime(año, mes, 1)
        fecha_fin = fecha_inicio
    
    filtros = {"fecha_inicio": fecha_inicio.isoformat(), "fecha_fin": fecha_fin.isoformat()}
    df = get_actividades(filtros)
    
    if not df.empty:
        eventos = []
        for _, row in df.iterrows():
            # Procesar la fecha: convertir cadena a date si es necesario
            fecha = row["fecha"]
            if isinstance(fecha, str):
                fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            
            # Extraer de manera segura la información del tipo de actividad
            tipo_act = row.get("tipos_actividad")
            if isinstance(tipo_act, dict) and "nombre" in tipo_act:
                tipo_nombre = tipo_act["nombre"]
            else:
                tipo_nombre = "Tipo no definido"
            
            # Extraer de forma segura la información del usuario
            usuario_data = row.get("usuarios")
            if isinstance(usuario_data, dict):
                usuario_nombre = usuario_data.get("nombre", "Nombre desconocido")
                usuario_nip = usuario_data.get("nip", "NIP no definido")
                usuario_apellidos = usuario_data.get("apellidos", "")
            else:
                usuario_nombre = "Nombre desconocido"
                usuario_nip = "NIP no definido"
                usuario_apellidos = ""
            
            # Asignar color basado en el nombre del tipo de actividad
            color = "#FF5733" if tipo_nombre == "Defensa Personal" else "#33A1FF"
            
            # Definir hora de inicio y fin según el turno
            if row.get("turno") == "Mañana":
                inicio = "09:00"
                fin = "11:00"
            elif row.get("turno") == "Tarde":
                inicio = "15:00"
                fin = "17:00"
            else:
                inicio = "20:00"
                fin = "22:00"
                
            # Agregar el evento a la lista
            eventos.append({
                "id": row.get("id"),
                "title": f"{tipo_nombre} - {usuario_nombre}",
                "start": f"{fecha.isoformat()}T{inicio}",
                "end": f"{fecha.isoformat()}T{fin}",
                "backgroundColor": color,
                "description": f"Usuario: {usuario_nip} - {usuario_nombre} {usuario_apellidos}"
            })
            
        calendar_options = {
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,timeGridWeek,timeGridDay"
            },
            "initialDate": fecha_inicio.isoformat(),
            "initialView": "dayGridMonth" if vista=="Mensual" else "timeGridWeek" if vista=="Semanal" else "timeGridDay",
            "selectable": True,
            "editable": False,
            "eventLimit": True,
            "height": 800
        }
        st.subheader("Calendario de Actividades")
        cal_data = calendar(events=eventos, options=calendar_options, key="cal")
        if cal_data.get("eventClick"):
            event_id = cal_data["eventClick"]["event"]["id"]
            evento = next((e for e in eventos if e["id"] == event_id), None)
            if evento:
                st.info(f"Detalles:\n{evento['description']}")
            
        st.subheader("Visualización gráfica")
        fig = generate_activity_calendar(df)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay actividades en este período")
        
if __name__ == "__main__":
    main()
