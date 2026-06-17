import streamlit as st
import pandas as pd
import urllib.parse
import base64
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Chifa D' Belinda",
    page_icon="🍜",
    layout="centered"
)

# =========================================================
# CARGA DE IMÁGENES DE FONDO
# =========================================================
@st.cache_data
def cargar_imagen_b64(nombre_imagen):
    rutas_posibles = [
        os.path.join("images", nombre_imagen),
        os.path.join("app", "static", "images", nombre_imagen),
        nombre_imagen
    ]
    for r in rutas_posibles:
        if os.path.exists(r):
            with open(r, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
    return None


IMAGENES_POR_PAGINA = {
    1: "pag1.jpeg",
    2: "pag2.jpeg",
    3: "pag3.jpeg",
    4: "pag4.jpeg",
    5: "pag5.jpeg",
    6: "pag6.jpeg",
}


def aplicar_fondo(nombre_imagen, pagina_id):
    img_b64 = cargar_imagen_b64(nombre_imagen)
    if img_b64:
        st.markdown(f"""
        <style id="fondo-pagina-{pagina_id}">
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)),
            url('data:image/jpeg;base64,{img_b64}') !important;
            background-size: cover !important;
            background-repeat: no-repeat !important;
            background-position: center center !important;
            background-attachment: fixed !important;
        }}

        .main,
        [data-testid="stCanvas"],
        [data-testid="stTabPanel"],
        div[role="tabpanel"],
        div[data-testid="stVerticalBlock"],
        [data-testid="stApp"],
        [data-testid="stHeader"],
        [data-testid="stTabPanel"] div {{
            background-color: transparent !important;
            background: transparent !important;
            box-shadow: none !important;
        }}
        </style>
        """, unsafe_allow_html=True)


# CARRITO
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# DISTRIBUCIÓN
DISTRIBUCION_PAGINAS = {
    1: ['COMBOS', 'ALITAS REBOZADAS', 'ALITAS ESPECIALES', 'POLLO BROASTER'],
    2: ['SOPAS', 'CHAUFA'],
    3: ['AEROPUERTO', 'COMBINADOS', 'LOMOS SALTADOS'],
    4: ['TALLARINES SALTADOS', 'PLATOS SALADOS', 'PLATOS DULCES', 'TORTILLAS'],
    5: ['ENROLLADOS', 'TAYPA', 'RES', 'LANGOSTINOS', 'PATO', 'CHICHARRONES'],
    6: ['CHANCHO', 'COSTILLAS', 'PORCIONES', 'BEBIDAS FRÍAS', 'BEBIDAS CALIENTES']
}


@st.cache_data
def cargar_catalogo_limpio():
    nombre_archivo = "Catalogo_Productos.xlsx"
    nombre_csv = "Catalogo_Productos.xlsx - in.csv"

    if os.path.exists(nombre_archivo):
        df = pd.read_excel(nombre_archivo)
    elif os.path.exists(nombre_csv):
        df = pd.read_csv(nombre_csv)
    else:
        return pd.DataFrame()

    df.columns = df.columns.str.strip()
    df['Category'] = df['Category'].astype(str).str.strip().str.upper()
    return df


df_carta = cargar_catalogo_limpio()

# MODAL
@st.dialog("Configura tu Plato 🍜")
def abrir_modal_agregar_plato(id_plato, nombre_plato, precio_plato):
    st.markdown(f"### {nombre_plato}")
    st.markdown(f"**Precio Unitario:** S/. {precio_plato:.2f}")
    st.write("---")

    cantidad = st.number_input("Cantidad:", min_value=1, max_value=20, value=1)

    notas = st.text_input(
        "Notas / Observaciones (Opcional):",
        placeholder="Ej: Sin cebolla"
    )

    if st.button("🛒 AGREGAR AL PEDIDO", use_container_width=True):
        st.session_state.carrito.append({
            "id": id_plato,
            "nombre": nombre_plato,
            "precio": float(precio_plato),
            "cant": int(cantidad),
            "cremas": "Ninguna",
            "notas": notas if notas.strip() != "" else "Ninguna"
        })
        st.toast(f"¡{cantidad}x {nombre_plato} agregado!")
        st.rerun()


# =========================================================
# CSS ORIGINAL + NUEVO CUADRO FIJO
# =========================================================
st.markdown("""
<style>
html, body, [data-testid="stApp"] {
    margin: 0 !important;
    padding: 0 !important;
}

.main .block-container {
    padding-top: 170px !important;
    max-width: 100% !important;
}

/* TU TITULO ORIGINAL */
.cabecera-fija-chifa {
    position: fixed !important;
    top: 0px !important;
    left: 0px !important;
    right: 0px !important;
    z-index: 999999 !important;
    background-color: rgba(0, 0, 0, 0.55) !important;
    backdrop-filter: blur(5px) !important;
    padding: 15px 10px !important;
    text-align: center;
    border-bottom: 1px solid rgba(255, 235, 59, 0.2);
}

/* NUEVO CUADRO INDEPENDIENTE */
.barra-control-fija {
    position: fixed !important;
    top: 78px !important;
    left: 0px !important;
    right: 0px !important;
    z-index: 999998 !important;
    background-color: rgba(0, 0, 0, 0.55) !important;
    backdrop-filter: blur(5px) !important;
    padding: 8px 10px !important;
    border-bottom: 1px solid rgba(255, 235, 59, 0.2);
}

/* TODO TU ESTILO ORIGINAL */
div[data-testid="stTabs"] > div:first-child {
    background-color: transparent !important;
    padding: 4px 10px !important;
    border-bottom: 2px solid #FFEB3B !important;
}

div[data-testid="stTabs"] button p {
    color: #FFFFFF !important;
    font-size: 15px !important;
    font-weight: bold !important;
    text-shadow: 2px 2px 3px #000000, -2px -2px 3px #000000 !important;
}

div[data-testid="stRadio"] {
    background-color: rgba(0, 0, 0, 0.2) !important;
    backdrop-filter: blur(2px);
    padding: 8px !important;
    border: 1px solid #FFEB3B !important;
    border-radius: 8px !important;
    margin-bottom: 20px !important;
}

div[data-testid="stRadio"] label {
    color: #FFFFFF !important;
    font-weight: bold !important;
    text-shadow: 2px 2px 2px #000000, -2px -2px 2px #000000 !important;
}

.contenedor-plato-unico {
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    padding: 10px 0px !important;
    border-bottom: 1px solid rgba(255,255,255,0.25) !important;
}

.texto-nombre-plato {
    color: #FFFFFF !important;
    font-size: 15px !important;
    font-weight: bold !important;
    text-shadow: 2px 2px 2px #000000, -2px -2px 2px #000000 !important;
}

.texto-precio-plato {
    color: #FFEB3B !important;
    font-size: 16px !important;
    font-weight: 900 !important;
    text-shadow: 2px 2px 2px #000000, -2px -2px 2px #000000 !important;
}

.titulo-categoria-chifa {
    color: #FFEB3B !important;
    font-size: 17px !important;
    font-weight: bold !important;
    padding: 10px 4px !important;
    margin-top: 15px !important;
    margin-bottom: 5px !important;
    border-left: 5px solid #FFEB3B !important;
    text-shadow: 2px 2px 3px #000000, -2px -2px 3px #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# CABECERA ORIGINAL
st.markdown("""
<div class="cabecera-fija-chifa">
    <h2 style="margin: 0; font-size: 25px; color: #FFEB3B; font-family: sans-serif; text-shadow: 2px 2px 4px #000000, -2px -2px 4px #000000;">
        🍜 CHIFA D' BELINDA
    </h2>
    <p style="margin: 3px 0 0 0; font-size: 13px; color: #FFFFFF; text-shadow: 1px 1px 2px #000000, -1px -1px 2px #000000;">
        Pedidos en línea rápidos y directos a nuestro WhatsApp
    </p>
</div>
""", unsafe_allow_html=True)

# NUEVO CUADRO VACÍO DE CONTROL
st.markdown("""
<div class="barra-control-fija"></div>
""", unsafe_allow_html=True)

items_en_carrito = sum(item["cant"] for item in st.session_state.carrito)

# TABS
tab_carta, tab_pedido = st.tabs([
    "📖 Nuestra Carta",
    f"🛒 Mi Pedido ({items_en_carrito})"
])

# SELECTOR FIJO
pag_seleccionada = st.radio(
    "Selecciona una Página de la Carta:",
    options=[1, 2, 3, 4, 5, 6],
    format_func=lambda x: f"Pág. {x}",
    horizontal=True,
    key="pagina_actual"
)

# TAB CARTA
with tab_carta:
    if df_carta.empty:
        st.warning("⚠️ Por favor carga tu catálogo.")
    else:
        imagen_de_esta_pagina = IMAGENES_POR_PAGINA.get(
            pag_seleccionada,
            "pag1.jpeg"
        )
        aplicar_fondo(imagen_de_esta_pagina, pag_seleccionada)

        categorias_permitidas = DISTRIBUCION_PAGINAS.get(
            pag_seleccionada, []
        )

        for cat_name in categorias_permitidas:
            df_filtrado_cat = df_carta[df_carta["Category"] == cat_name]

            if not df_filtrado_cat.empty:
                st.markdown(
                    f'<div class="titulo-categoria-chifa">📂 {cat_name}</div>',
                    unsafe_allow_html=True
                )

                for idx, row in df_filtrado_cat.iterrows():
                    col_info, col_btn = st.columns([0.84, 0.16])

                    with col_info:
                        st.markdown(f"""
                        <div class="contenedor-plato-unico">
                            <span class="texto-nombre-plato">{row['Name']}</span>
                            <span class="texto-precio-plato">S/. {float(row['Price']):.2f}</span>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_btn:
                        if st.button("＋", key=f"btn_{row['ID']}"):
                            abrir_modal_agregar_plato(
                                row['ID'],
                                row['Name'],
                                row['Price']
                            )

# TAB PEDIDO
with tab_pedido:
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío.")
    else:
        total = 0
        for item in st.session_state.carrito:
            subtotal = item["precio"] * item["cant"]
            total += subtotal
            st.markdown(
                f"💥 **{item['cant']}x {item['nombre']}** — S/. {subtotal:.2f}"
            )