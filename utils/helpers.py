# utils/helpers.py
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def format_date(date_str):
    """Formatea la fecha de AAAA-MM-DD a DD/MM/AAAA."""
    if isinstance(date_str, str):
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    return date_str.strftime('%d/%m/%Y')

def generate_activity_calendar(activities_df):
    """Genera un gráfico tipo 'heatmap' para ver la distribución de actividades."""
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
    """Genera gráficos estadísticos de las actividades."""
    if activities_df.empty:
        return None, None, None
    # Por tipo de actividad
    fig1 = px.pie(
        activities_df,  
        names='tipos_actividad.nombre',  
        title='Distribución por Tipo de Actividad'
    )
    # Por turno
    fig2 = px.bar(
        activities_df.groupby('turno').size().reset_index(name='count'),
        x='turno',  
        y='count',  
        title='Actividades por Turno',
        color='turno'
    )
    # Por sección de usuario
    fig3 = px.bar(
        activities_df.groupby('usuarios.seccion').size().reset_index(name='count'),
        x='usuarios.seccion',  
        y='count',  
        title='Actividades por Sección',
        color='usuarios.seccion'
    )
    return fig1, fig2, fig3
