# utils/helpers.py
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def format_date(date_str):
    """Formatea una fecha en formato AAAA-MM-DD a DD/MM/AAAA."""
    if isinstance(date_str, str):
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    return date_str.strftime('%d/%m/%Y')

def generate_activity_calendar(activities_df):
    """Genera un heatmap interactivo con Plotly para visualizar la distribución de actividades."""
    if activities_df.empty:
        return go.Figure()
    # Agrupar por fecha y turno
    activities_count = activities_df.groupby(['fecha', 'turno']).size().reset_index(name='count')
    fig = px.density_heatmap(
        activities_count,  
        x='fecha',  
        y='turno',
        z='count',
        color_continuous_scale='Viridis',
        title='Distribución de Actividades'
    )
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Turno',
        height=400
    )
    return fig

def generate_activity_stats(activities_df):
    """Genera gráficos estadísticos de actividades.
       Se crean columnas aplanadas a partir de los datos anidados para usar en Plotly."""
    if activities_df.empty:
        return None, None, None

    # Extraer el nombre del tipo de actividad
    activities_df["tipo_nombre"] = activities_df["tipos_actividad"].apply(
        lambda x: x.get("nombre") if isinstance(x, dict) and "nombre" in x else "Desconocido"
    )
    # Extraer la sección del usuario
    activities_df["usuario_seccion"] = activities_df["usuarios"].apply(
        lambda x: x.get("seccion") if isinstance(x, dict) and "seccion" in x else "Desconocido"
    )
    # Gráfico de pastel: distribución por tipo de actividad
    fig1 = px.pie(
        activities_df,
        names="tipo_nombre",
        title="Distribución por Tipo de Actividad"
    )
    # Gráfico de barras: actividades por turno
    agrup_turno = activities_df.groupby("turno").size().reset_index(name="count")
    fig2 = px.bar(
        agrup_turno,
        x="turno", y="count",
        title="Actividades por Turno",
        color="turno"
    )
    # Gráfico de barras: actividades por sección
    agrup_seccion = activities_df.groupby("usuario_seccion").size().reset_index(name="count")
    fig3 = px.bar(
        agrup_seccion,
        x="usuario_seccion", y="count",
        title="Actividades por Sección",
        color="usuario_seccion"
    )
    return fig1, fig2, fig3
