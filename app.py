import streamlit as st
import pandas as pd
import urllib.parse
import os

# CONFIGURACIÓN DE LA PÁGINA (Optimizada estrictamente para celulares)
st.set_page_config(
    page_title="Chifa D' Belinda",
    page_icon="🍜",
    layout="centered"
)

# INICIALIZACIÓN DE ESTADOS DEL CARRITO
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "mensaje_exito" not in st.session_state:
    st.session_state.mensaje_exito = None

# CAPTURAR CLICKS DESDE LOS ENLACES HTML EN LA URL
query_params = st.query_params
if "add_id" in query_params:
    id_elegido = query_params["add_id"]
    nombre_elegido = query_params.get("add_name", "Plato")
    precio_elegido = float(query_params.get("add_price", 0))
    
    st.session_state.carrito.append({
        "nombre": nombre_elegido,
        "precio": precio_elegido,
        "cant": 1,
        "nota": ""
    })
    st.session_state.mensaje_exito = f"¡{nombre_elegido} agregado! 🛒✅"
    st.query_params.clear()
    st.rerun()

# MOSTRAR MENSAJE FLOTANTE DE ÉXITO (TOAST)
if st.session_state.mensaje_exito:
    st.toast(st.session_state.mensaje_exito)
    st.session_state.mensaje_exito = None

# BASE DE DATOS COMPLETA DE TODA LA CARTA (Páginas 2, 3, 4 y 5 de tu PDF)
def obtener_carta_completa_pdf():
    datos = {
        "ID": [f"P{i}" for i in range(1, 46)],
        "Name": [
            # --- PÁGINA 2: COMBOS, ALITAS Y BROASTER ---
            "COMBO 1 (Chi Jau Kay + Pollo)", "COMBO 2 (Tipa Kay + Pollo)", 
            "COMBO 3 (Enrollado + Pollo)", "COMBO 4 (Alitas + Chaufa/Papas)",
            "Alitas Rebozadas 3 Pzs", "Alitas Rebozadas 4 Pzs", "Alitas Rebozadas 5 Pzs", "Alitas Rebozadas 6 Pzs",
            "Alitas BBQ", "Alitas Bravas", "Alitas con Verduras", "Alitas con Tamarindo", 
            "Alitas con Piña", "Alitas Ostión", "Alitas Tausi", "Alitas con Durazno", 
            "Alitas Piña y Durazno", "Alitas Beli Beli", "Alitas Salsa Blanca",
            "1/8 Pollo Broaster", "1/4 Pollo Broaster",
            
            # --- PÁGINA 3: SOPAS Y CHAUFAS ---
            "Sopa Wantán Especial", "Sopa Fuchifú", "Sopa de Wantán Simple",
            "Chaufa de Pollo", "Chaufa de Chancho", "Chaufa de Res", 
            "Chaufa de Langostinos", "Chaufa Especial", "Chaufa Beli Beli (Salvaje)",
            
            # --- PÁGINA 4: AEROPUERTOS, COMBINADOS Y LOMOS ---
            "Aeropuerto de Pollo", "Aeropuerto de Carne / Chancho", "Aeropuerto Especial",
            "Combinado de Pollo", "Combinado de Carne / Chancho", "Combinado Especial",
            "Lomo Saltado de Pollo", "Lomo Saltado de Res", "Lomo Saltado Especial Chifa",
            
            # --- PÁGINA 5: TALLARINES, WOK SALADO Y DULCE ---
            "Tallarín Saltado de Pollo", "Tallarín Saltado de Res / Chancho", "Tallarín Especial",
            "Pollo con Verduras (Wok)", "Chi Jau Kay (Plato)", "Tipa Kay (Plato)",
            "Pollo con Tamarindo", "Pollo con Piña"
        ],
        "Price": [
            # Precios Página 2
            37.00, 37.00, 37.00, 35.00, 14.00, 18.00, 20.00, 25.00, 22.00, 22.00, 22.00, 22.00, 22.00, 22.00, 22.00, 22.00, 26.00, 25.00, 28.00, 13.00, 21.00,
            # Precios Página 3
            16.00, 16.00, 10.00, 14.00, 18.00, 18.00, 25.00, 22.00, 26.00,
            # Precios Página 4
            16.00, 19.00, 22.00, 16.00, 19.00, 22.00, 17.00, 20.00, 24.00,
            # Precios Página 5
            16.00, 19.00, 22.00, 18.00, 20.00, 20.00, 18.00, 19.00
        ],
        "Page": [
            # Mapeo de a qué página física pertenece cada plato
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, # Pág 2
            3, 3, 3, 3, 3, 3, 3, 3, 3,                                     # Pág 3
            4, 4, 4, 4, 4, 4, 4, 4, 4,                                     # Pág 4
            5, 5, 5, 5, 5, 5, 5, 5                                         # Pág 5
        ]
    }
    return pd.DataFrame(datos)

df_carta = obtener_carta_completa_pdf()

# BASE DE DATOS DEL MENÚ DIARIO
df_menu_diario = pd.DataFrame({
    "Name": ["Chaufa de Pollo", "Alita Rebozada", "1/8 Broaster", "Aeropuerto de Pollo", "Combinado de Pollo"],
    "Price": [14.00, 15.00, 14.00, 17.00, 17.00]
})

# ESTILOS CSS (Garantiza una sola línea compacta por plato)
st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 5px !important;
}

.contenedor-menu-rojo {
    background-color: #8B0000 !important;
    padding: 8px 5px !important;
    border-radius: 6px;
    display: flex !important;
    flex-direction: column !important;
    gap: 5px !important;
    width: 100%;
}

.fila-plato-unica-linea {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
    padding: 3px 0px !important;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.btn-agregar-inline {
    background-color: #FFFFFF !important;
    color: #8B0000 !important;
    text-decoration: none !important;
    font-size: 11px !important;
    font-weight: bold !important;
    border-radius: 50% !important;
    width: 18px !important;
    height: 18px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
}

.texto-plato-inline {
    color: #FFFFFF !important;
    font-size: 10px !important;
    font-weight: bold !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    margin-left: 6px !important;
    margin-right: auto !important;
    text-align: left !important;
}

.precio-plato-inline {
    color: #FFEB3B !important;
    font-size: 11px !important;
    font-weight: bold !important;
    white-space: nowrap !important;
    flex-shrink: 0 !important;
    margin-left: 4px !important;
}

.titulo-seccion-carta {
    color: #8B0000;
    font-size: 14px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 2px;
    border-bottom: 2px solid #8B0000;
}
</style>
""", unsafe_allow_html=True)

# ENCABEZADO PRINCIPAL
st.markdown("<h2 style='text-align:center; color:#8B