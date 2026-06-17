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

# =========================================================
# CARRITO
# =========================================================
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# =========================================================
# DISTRIBUCIÓN
# =========================================================
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

# =========================================================
# MODAL
# =========================================================
@st.dialog("Configura tu Plato 🍜")
def abrir_modal_agregar_plato(id_plato, nombre_plato, precio_plato):
    st.markdown(f"### {nombre_plato}")
    st.markdown(f"**Precio Unitario:** S/. {precio_plato:.2f}")
    st.write("---")

    cantidad = st.number_input("Cantidad:", min_value=1, max_value=20, value=1)

    notas = st.text_input("Notas / Observaciones")

    if st.button("🛒 AGREGAR AL PEDIDO", use_container_width=True):
        st.session_state.carrito.append({
            "id": id_plato,
            "nombre": nombre_plato,
            "precio": float(precio_plato),
            "cant": int(cantidad),
            "notas": notas if notas else "Ninguna"
        })
        st.rerun()

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
html, body, [data-testid="stApp"] {
    margin: 0 !important;
    padding: 0 !important;
}

.main .block-container {
    padding-top: 0px !important;
}

/* CUADRO DEL TÍTULO */
.cabecera-fija-chifa {
    position: fixed !important;
    top: 0px;
    left: 0px;
    right: 0px;
    z-index: 999999;
    background-color: rgba(0,0,0,0.55);
    backdrop-filter: blur(5px);
    padding: 15px 10px;
    text-align: center;
}

/* NUEVO CUADRO PARA PESTAÑAS */
.barra-tabs-fija {
    position: fixed !important;
    top: 82px;
    left: 0px;
    right: 0px;
    z-index: 999998;
    background-color: rgba(0,0,0,0.55);
    backdrop-filter: blur(5px);
    padding: 12px 10px;
    text-align: center;
    border-bottom: 2px solid #FFEB3B;
}

/* BAJA EL CONTENIDO */
div[data-testid="stTabs"] {
    margin-top: 150px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# ENCABEZADO
# =========================================================
st.markdown("""
<div class="cabecera-fija-chifa">
    <h2 style="margin:0;color:#FFEB3B;">🍜 CHIFA D' BELINDA</h2>
    <p style="margin:3px 0 0 0;color:white;">
        Pedidos en línea rápidos y directos a nuestro WhatsApp
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# NUEVO CUADRO DE PESTAÑAS
# =========================================================
items_en_carrito = sum(item["cant"] for item in st.session_state.carrito)

st.markdown(f"""
<div class="barra-tabs-fija">
    <div style="
        display:flex;
        justify-content:center;
        gap:40px;
        font-size:16px;
        font-weight:bold;
        color:#FFFFFF;
    ">
        <span>📖 Nuestra Carta</span>
        <span>🛒 Mi Pedido ({items_en_carrito})</span>
    </div>
</div>
""", unsafe_allow_html=True)

# TABS REALES
tab_carta, tab_pedido = st.tabs([
    "📖 Nuestra Carta",
    f"🛒 Mi Pedido ({items_en_carrito})"
])

# =========================================================
# CARTA
# =========================================================
with tab_carta:
    if df_carta.empty:
        st.warning("⚠️ Carga tu catálogo.")
    else:
        pag_seleccionada = st.radio(
            "Selecciona una Página de la Carta:",
            options=[1,2,3,4,5,6],
            format_func=lambda x: f"Pág. {x}",
            horizontal=True
        )

        imagen_de_esta_pagina = IMAGENES_POR_PAGINA.get(pag_seleccionada, "pag1.jpeg")
        aplicar_fondo(imagen_de_esta_pagina, pag_seleccionada)

        categorias_permitidas = DISTRIBUCION_PAGINAS.get(pag_seleccionada, [])

        for cat_name in categorias_permitidas:
            df_filtrado_cat = df_carta[df_carta["Category"] == cat_name]

            if not df_filtrado_cat.empty:
                st.subheader(cat_name)

                for idx, row in df_filtrado_cat.iterrows():
                    col1, col2 = st.columns([0.85, 0.15])

                    with col1:
                        st.write(f"**{row['Name']}** — S/. {float(row['Price']):.2f}")

                    with col2:
                        if st.button("＋", key=f"btn_{row['ID']}"):
                            abrir_modal_agregar_plato(
                                row['ID'],
                                row['Name'],
                                row['Price']
                            )

# =========================================================
# PEDIDO
# =========================================================
with tab_pedido:
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío.")
    else:
        total = 0

        for item in st.session_state.carrito:
            subtotal = item["precio"] * item["cant"]
            total += subtotal
            st.write(f"{item['cant']}x {item['nombre']} - S/. {subtotal:.2f}")

        st.divider()

        nombre_cliente = st.text_input("Nombre")
        telefono_cliente = st.text_input("Teléfono")

        if nombre_cliente and telefono_cliente:
            mensaje = f"Pedido de {nombre_cliente}\n"

            for item in st.session_state.carrito:
                mensaje += f"{item['cant']}x {item['nombre']}\n"

            mensaje += f"TOTAL: S/. {total:.2f}"

            link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje)}"

            st.link_button(
                "📲 ENVIAR PEDIDO A WHATSAPP",
                link_final,
                use_container_width=True
            )