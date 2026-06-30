import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página de Streamlit
st.set_page_config(page_title="Dashboard Citas Médicas", layout="wide")

# Título Principal
st.title('Hospital de Lima Norte - Dashboard de Gestión de Citas Médicas')
st.markdown("---")

# Cargar los datos distribuidos en el repositorio
@st.cache_data
def cargar_datos():
    data = pd.read_csv('citas_medicas.csv')
    data['fecha'] = pd.to_datetime(data['fecha'])
    data['mes'] = data['fecha'].dt.month
    return data

df = cargar_datos()

# Distribución en Columnas para Mejor Estética Visual
col1, col2 = st.columns(2)

with col1:
    st.subheader('🎯 Citas por Especialidad')
    df_especialidad = df['especialidad'].value_counts().reset_index()
    df_especialidad.columns = ['Especialidad', 'Cantidad']
    
    fig1 = px.bar(
        df_especialidad,
        x='Especialidad',
        y='Cantidad',
        labels={'Especialidad': 'Especialidad', 'Cantidad': 'Cantidad de Citas'},
        color='Especialidad'
    )
    st.plotly_chart(fig1, width="stretch")

with col2:
    st.subheader('📊 Estado Operativo de las Citas')
    fig2 = px.pie(
        df,
        names='estado',
        color='estado',
        color_discrete_map={'Atendida': '#2ca02c', 'Cancelada': '#d62728', 'No asistió': '#ff7f0e'}
    )
    st.plotly_chart(fig2, width="stretch")

st.markdown("---")

# Línea de tendencia mensual
st.subheader('📈 Evolución y Tendencia de Citas por Mes')
citas_mes = df.groupby('mes').size().reset_index(name='cantidad').sort_values('mes')

fig3 = px.line(
    citas_mes,
    x='mes',
    y='cantidad',
    markers=True,
    labels={'mes': 'Número de Mes', 'cantidad': 'Total Citas'},
    line_shape='linear'
)
fig3.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1))

st.plotly_chart(fig3, width="stretch")
