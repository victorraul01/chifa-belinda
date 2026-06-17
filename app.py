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
# CARGA DE IMÁGENES DE FONDO (UNA POR PÁGINA, CACHEADAS)
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
            background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.45)),
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

# 2. INICIALIZACIÓN DEL CARRITO
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# =========================================================
# 3. DICCIONARIO MAESTRO DE DISTRIBUCIÓN DE PÁGINAS
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
# 4. MODAL PARA DETALLES DEL PLATO
# =========================================================
@st.dialog("Configura tu Plato 🍜")
def abrir_modal_agregar_plato(id_plato, nombre_plato, precio_plato):
    st.markdown(f"### {nombre_plato}")
    st.markdown(f"**Precio Unitario:** S/. {precio_plato:.2f}")
    st.write("---")

    cantidad = st.number_input("Cantidad:", min_value=1, max_value=20, value=1, step=1)

    st.markdown("**Selecciona tus Cremas / Salsas:**")
    col1, col2 = st.columns(2)
    with col1:
        c_aji = st.checkbox("Ají Chi Chon San 🌶️")
        c_mayo = st.checkbox("Mayonesa ⚪")
    with col2:
        c_ketchup = st.checkbox("Ketchup 🍅")
        c_tamarindo = st.checkbox("Salsa Tamarindo 🍯")

    notas = st.text_input(
        "Notas / Observaciones (Opcional):",
        placeholder="Ej: Sin cebolla, bien frito..."
    )

    if st.button("🛒 AGREGAR AL PEDIDO", use_container_width=True, key=f"modal_add_{id_plato}"):
        cremas_list = []
        if c_aji: cremas_list.append("Ají")
        if c_mayo: cremas_list.append("Mayo")
        if c_ketchup: cremas_list.append("Ketchup")
        if c_tamarindo: cremas_list.append("Tamarindo")

        cremas_texto = ", ".join(cremas_list) if cremas_list else "Ninguna"

        st.session_state.carrito.append({
            "id": id_plato,
            "nombre": nombre_plato,
            "precio": float(precio_plato),
            "cant": int(cantidad),
            "cremas": cremas_texto,
            "notas": notas if notas.strip() != "" else "Ninguna"
        })
        st.toast(f"¡{cantidad}x {nombre_plato} agregado!")
        st.rerun()

# =========================================================
# 5. CSS
# =========================================================
st.markdown("""
<style>
html, body, [data-testid="stApp"] {
    margin: 0 !important;
    padding: 0 !important;
}

.main .block-container {
    padding-top: 0px !important;
    max-width: 100% !important;
}

/* CUADRO DEL TÍTULO */
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

/* NUEVO CUADRO FIJO PARA PESTAÑAS */
.barra-tabs-fija {
    position: fixed !important;
    top: 82px !important;
    left: 0px !important;
    right: 0px !important;
    z-index: 999998 !important;
    background-color: rgba(0, 0, 0, 0.55) !important;
    backdrop-filter: blur(5px) !important;
    padding: 10px 10px !important;
    text-align: center;
    border-bottom: 1px solid rgba(255, 235, 59, 0.2);
}

/* ESPACIO PARA QUE NO TAPE CONTENIDO */
div[data-testid="stTabs"] {
    margin-top: 145px !important;
}

/* ESTILO TABS REALES */
div[data-testid="stTabs"] > div:first-child {
    background-color: transparent !important;
    padding: 4px 10px !important;
    border-bottom: 2px solid #FFEB3B !important;
}

div[data-testid="stTabs"] button p {
    color: #FFFFFF !important;
    font-size: 15px !important;
    font-weight: bold !important;
}

/* SELECTOR DE PÁGINAS */
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
}

/* FILA DE PLATOS */
.contenedor-plato-unico {
    display: flex !important;
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
}

.texto-precio-plato {
    color: #FFEB3B !important;
    font-size: 16px !important;
    font-weight: 900 !important;
}

.titulo-categoria-chifa {
    color: #FFEB3B !important;
    font-size: 17px !important;
    font-weight: bold !important;
    padding: 10px 4px !important;
    margin-top: 15px !important;
    border-left: 5px solid #FFEB3B !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 6. ENCABEZADO
# =========================================================
st.markdown("""
<div class="cabecera-fija-chifa">
    <h2 style="margin:0; font-size:25px; color:#FFEB3B;">🍜 CHIFA D' BELINDA</h2>
    <p style="margin:3px 0 0 0; font-size:13px; color:#FFFFFF;">
        Pedidos en línea rápidos y directos a nuestro WhatsApp
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 7. NUEVO CUADRO DE PESTAÑAS
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

# Tabs reales
tab_carta, tab_pedido = st.tabs([
    "📖 Nuestra Carta",
    f"🛒 Mi Pedido ({items_en_carrito})"
])

# =========================================================
# PESTAÑA 1: NUESTRA CARTA
# =========================================================
with tab_carta:
    if df_carta.empty:
        st.warning("⚠️ Por favor, carga tu archivo del catálogo.")
    else:
        pag_seleccionada = st.radio(
            "Selecciona una Página de la Carta:",
            options=[1, 2, 3, 4, 5, 6],
            format_func=lambda x: f"Pág. {x}",
            horizontal=True,
            key="pagina_actual"
        )

        imagen_de_esta_pagina = IMAGENES_POR_PAGINA.get(pag_seleccionada, "pag1.jpeg")
        aplicar_fondo(imagen_de_esta_pagina, pag_seleccionada)

        categorias_permitidas = DISTRIBUCION_PAGINAS.get(pag_seleccionada, [])

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

# =========================================================
# PESTAÑA 2: MI PEDIDO
# =========================================================
with tab_pedido:
    st.markdown(
        '<div style="background-color:#FFFFFF;padding:20px;border-radius:12px;color:#222;">',
        unsafe_allow_html=True
    )

    if not st.session_state.carrito:
        st.info("Tu carrito está vacío. ¡Explora la carta!")
    else:
        st.subheader("📋 Resumen Total del Pedido")
        total = 0

        for idx, item in enumerate(st.session_state.carrito):
            subtotal = item["precio"] * item["cant"]
            total += subtotal

            st.markdown(
                f"💥 **{item['cant']}x {item['nombre']}** — S/. {subtotal:.2f}"
            )

        st.divider()

        nombre_cliente = st.text_input("Ingresa tu Nombre Completo:")
        telefono_cliente = st.text_input("Tu número de contacto:")

        if nombre_cliente.strip() and telefono_cliente.strip():
            phone = telefono_cliente.strip()
            mensaje_wa = f"🍜 *CHIFA D' BELINDA*\n\n👤 {nombre_cliente}\n📞 {phone}\n"

            for item in st.session_state.carrito:
                mensaje_wa += f"✅ {item['cant']}x {item['nombre']}\n"

            mensaje_wa += f"\n💰 TOTAL: S/. {total:.2f}"

            link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"

            st.link_button(
                "📲 ENVIAR PEDIDO A WHATSAPP",
                link_final,
                use_container_width=True
            )

    st.markdown("</div>", unsafe_allow_html=True)