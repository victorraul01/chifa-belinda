import streamlit as st
import pandas as pd
import urllib.parse
import base64
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Chifa D' Belinda", page_icon="🍜", layout="centered")

# --- Datos del Menú ---
PLATOS_MENU_INTERNO = [
    {"ID": "M01", "Name": "Chaufa de Pollo", "Price": 14.00},
    {"ID": "M02", "Name": "Alita Rebozada", "Price": 15.00},
    {"ID": "M03", "Name": "1/8 Broaster", "Price": 14.00},
    {"ID": "M04", "Name": "Aeropuerto de Pollo", "Price": 17.00},
    {"ID": "M05", "Name": "Combinado de Pollo", "Price": 17.00},
    {"ID": "M06", "Name": "Pollo con Verdura", "Price": 17.00},
    {"ID": "M07", "Name": "Tallarín Saltado de Pollo", "Price": 17.00},
    {"ID": "M08", "Name": "Pollo con Tamarindo", "Price": 17.00}
]

# --- CSS INTEGRADO PARA EL DISEÑO DE FILA ---
st.markdown("""
<style>
/* Diseño de fila */
.fila-contenedor { 
    display: flex; align-items: center; justify-content: space-between; 
    padding: 8px 0; position: relative; height: 50px;
}
.texto-info { flex: 1; display: flex; justify-content: space-between; align-items: center; padding-right: 50px; }
.nombre-plato { color: white; font-weight: bold; font-size: 16px; }
.precio-plato { color: #FFEB3B; font-weight: 900; font-size: 16px; }

/* Botón flotante alineado a la derecha */
.btn-wrapper { position: absolute; right: 0; top: 8px; }
div[data-testid="stButton"] button { 
    background-color: #FFEB3B !important; color: #8B0000 !important; 
    border-radius: 6px !important; border: none !important; width: 35px; height: 35px;
}
</style>
""", unsafe_allow_html=True)

# --- Funciones Auxiliares ---
if "carrito" not in st.session_state: st.session_state.carrito = []

@st.dialog("Configurar Plato")
def abrir_modal(p_info, p_orig):
    st.write(f"### {p_info['Name']}")
    cantidad = st.number_input("Cantidad:", 1, 20, 1)
    if st.button("🛒 AGREGAR"):
        st.session_state.carrito.append({"nombre": p_info['Name'], "precio": p_info['Price'], "cant": cantidad})
        st.rerun()

# --- Interfaz ---
tab1, tab2, tab3 = st.tabs(["🍱 Menú", "📖 Carta", "🛒 Pedido"])

with tab1:
    st.header("Menú del día")
    for plato in PLATOS_MENU_INTERNO:
        st.markdown(f"""
        <div class="fila-contenedor">
            <div class="texto-info">
                <span class="nombre-plato">{plato['Name']}</span>
                <span class="precio-plato">S/. {plato['Price']:.2f}</span>
            </div>
            <div class="btn-wrapper"></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("＋", key=f"btn_{plato['ID']}"):
            abrir_modal(plato, "Menú")
        st.divider()

with tab2:
    st.write("Catálogo a la carta aquí...")

with tab3:
    st.write(f"Carrito: {len(st.session_state.carrito)} ítems")
    if st.button("Enviar Pedido"):
        st.write("Generando link de WhatsApp...")