# pages/actividades.py
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.auth import check_login
from utils.database import get_usuarios, get_tipos_actividad, crear_actividad, get_actividades, actualizar_actividad
from utils.helpers import format_date

def main():
    user = check_login()
    st.title("Gestión de Actividades")
    tab1, tab2 = st.tabs(["Agendar Actividad", "Listar Actividades"])

    with tab1:
        st.header("Agendar Actividad")
        with st.form("form_agendar"):
            col1, col2 = st.columns(2)
            with col1:
                usuarios_df = get_usuarios()
                if not usuarios_df.empty:
                    opciones = [f"{row['nip']} - {row['nombre']} {row['apellidos']}" for _, row in usuarios_df.iterrows()]
                    usuario_sel = st.selectbox("Seleccione Usuario", opciones)
                    usuario_nip = int(usuario_sel.split(" - ")[0])
                    usuario_id = usuarios_df[usuarios_df['nip']==usuario_nip]['id'].values[0]
                else:
                    st.error("No hay usuarios registrados.")
                    usuario_id = None
                tipos_df = get_tipos_actividad()
                if not tipos_df.empty:
                    tipo_sel = st.selectbox("Tipo de Actividad", tipos_df['nombre'].tolist())
                    tipo_id = tipos_df[tipos_df['nombre']==tipo_sel]['id'].values[0]
                else:
                    st.error("No hay tipos de actividad.")
                    tipo_id = None
            with col2:
                fecha = st.date_input("Fecha", min_value=datetime.today())
                turno = st.selectbox("Turno", ["Mañana", "Tarde", "Noche"])
                observaciones = st.text_area("Observaciones", height=100)
            if st.form_submit_button("Agendar"):
                if usuario_id and tipo_id:
                    res = crear_actividad(usuario_id, tipo_id, fecha.isoformat(), turno, st.session_state.user["id"], observaciones)
                    if res.data:
                        st.success("Actividad agendada")
                    else:
                        st.error("Error al agendar actividad")
    with tab2:
        st.header("Listado de Actividades")
        filtros = {}
        col1, col2, col3 = st.columns(3)
        with col1:
            f_inicio = st.date_input("Fecha Inicio")
            filtros["fecha_inicio"] = f_inicio.isoformat()
        with col2:
            f_fin = st.date_input("Fecha Fin")
            filtros["fecha_fin"] = f_fin.isoformat()
        with col3:
            filtros["turno"] = st.selectbox("Turno", ["", "Mañana", "Tarde", "Noche"])
        df_acts = get_actividades(filtros)
        if not df_acts.empty:
            lista = []
            for _, row in df_acts.iterrows():
                lista.append({
                    "Fecha": format_date(row["fecha"]),
                    "Turno": row["turno"],
                    "Usuario": f"{row['usuarios']['nip']} - {row['usuarios']['nombre']} {row['usuarios']['apellidos']}",
                    "Actividad": row['tipos_actividad']['nombre'],
                    "Monitor": f"{row['monitores']['nombre']} {row['monitores']['apellidos']}",
                    "Completada": "Si" if row["completada"] else "No"
                })
            st.dataframe(pd.DataFrame(lista), use_container_width=True)
            # Posibilidad de actualizar estado de actividad
            act_ids = [row['id'] for _, row in df_acts.iterrows()]
            opcion = st.selectbox("Seleccionar actividad para marcar completada/no", [None]+[f"{r['fecha']} - {r['usuarios']['nombre']}" for _, r in df_acts.iterrows()])
            if opcion:
                # Aquí podrías implementar botones para cambiar el estado de la actividad
                if st.button("Marcar como Completada"):
                    idx = [f"{r['fecha']} - {r['usuarios']['nombre']}" for _, r in df_acts.iterrows()].index(opcion)
                    act_id = act_ids[idx]
                    r = actualizar_actividad(act_id, {"completada": True})
                    if r:
                        st.success("Actividad actualizada")
                        st.experimental_rerun()
        else:
            st.warning("No se encontraron actividades")
            
if __name__ == "__main__":
    main()
