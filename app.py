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
            background-image: url('data:image/jpeg;base64,{img_b64}') !important;
            background-size: cover !important;
            background-repeat: no-repeat !important;
            background-position: center center !important;
            background-attachment: fixed !important;
        }}
        /* Forzar transparencia total para eliminar bloques o parches blancos */
        .main, [data-testid="stCanvas"], [data-testid="stTabPanel"], div[role="tabpanel"] {{
            background-color: transparent !important;
            background: transparent !important;
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

# 4. VENTANA EMERGENTE (MODAL) PARA DETALLES DEL PLATO
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

    st.write("")
    notas = st.text_input("Notas / Observaciones (Opcional):", placeholder="Ej: Sin cebolla, bien frito...")

    st.write("")
    if st.button("🛒 AGREGAR AL PEDIDO", use_container_width=True):
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
# 5. CSS MAESTRO: ENCABEZADO FIJO SIN PARCHES BLANCOS
# =========================================================
st.markdown("""
<style>
/* 1. Congelar la pantalla exterior para controlar el scroll interno */
html, body, [data-testid="stApp"] {
    overflow: hidden !important;
    height: 100vh !important;
}

/* Eliminar márgenes por defecto de Streamlit arriba */
.main .block-container {
    padding-top: 0px !important;
    padding-bottom: 0px !important;
    padding-left: 0px !important;
    padding-right: 0px !important;
    max-width: 100% !important;
}

/* 2. ENCABEZADO FIJO BLANCO DE TU DISEÑO ORIGINAL */
.encabezado-fijo-contenedor {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    background-color: #FFFDF9 !important; /* Beige/Blanco claro original */
    z-index: 999999 !important;
    padding: 14px 16px 6px 16px !important;
    border-bottom: 2px solid #8B0000 !important;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.15) !important;
    text-align: center;
}

/* 3. FORZAR QUE LAS PESTAÑAS NATIVAS SE QUEDEN FIJAS JUSTO ABAJO */
div[data-testid="stTabs"] > div:first-child {
    position: fixed !important;
    top: 72px !important;
    left: 0 !important;
    width: 100% !important;
    background-color: #FFFDF9 !important;
    z-index: 999998 !important;
    padding: 0px 16px !important;
    border-bottom: 1px solid #E0E0E0 !important;
}

/* Ajustar los textos de las pestañas nativas */
div[data-testid="stTabs"] button p {
    font-size: 14px !important;
    font-weight: bold !important;
}

/* 4. CREAR ÁREA DE SCROLL SÓLO PARA LOS PLATOS (Evita que el menú se mueva) */
div[data-testid="stTabs"] > div:nth-child(2) {
    height: calc(100vh - 125px) !important;
    overflow-y: auto !important;
    -webkit-overflow-scrolling: touch !important;
    margin-top: 125px !important;
    padding: 10px 16px 120px 16px !important;
}

/* Estilo limpio para el Radio Horizontal (Botones de Página flotando) */
div[data-testid="stRadio"] div[role="radiogroup"] {
    background-color: rgba(255, 255, 255, 0.9) !important;
    padding: 8px !important;
    border-radius: 8px !important;
    border: 1px solid #8B0000 !important;
    margin-bottom: 15px !important;
}
div[data-testid="stRadio"] label {
    color: #222222 !important;
    font-weight: bold !important;
}

/* Botón redondo amarillo "＋" */
div.stButton > button {
    background-color: #FFEB3B !important;
    color: #8B0000 !important;
    font-size: 22px !important;
    font-weight: bold !important;
    border-radius: 50% !important;
    width: 44px !important;
    height: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: 2px solid #8B0000 !important;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.4) !important;
}

/* Categorías */
.titulo-categoria-chifa {
    color: #FFEB3B !important;
    font-size: 16px !important;
    font-weight: bold !important;
    background-color: #8B0000 !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    margin-top: 15px !important;
    margin-bottom: 12px !important;
    border-left: 5px solid #FFEB3B !important;
}

/* Filas transparentes directamente sobre la imagen roja */
.fila-plato-limpia {
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    padding: 12px 4px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.25) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 6. ESTRUCTURA FIJA REAL EN LA PARTE SUPERIOR
# =========================================================
st.markdown("""
<div class="encabezado-fijo-contenedor">
    <h3 style="margin: 0; padding: 0; font-size: 22px; color: #8B0000; font-family: sans-serif; font-weight: bold;">🍜 CHIFA D' BELINDA</h3>
    <p style="margin: 3px 0 0 0; padding: 0; font-size: 13px; color: #444444; font-family: sans-serif;"> pedidos en línea rápidos y directos a nuestro WhatsApp</p>
</div>
""", unsafe_allow_html=True)

items_en_carrito = sum(item["cant"] for item in st.session_state.carrito)

tab_carta, tab_pedido = st.tabs([
    "📖 Nuestra Carta", f"🛒 Mi Pedido ({items_en_carrito})"
])

# =========================================================
# PESTAÑA 1: NUESTRA CARTA
# =========================================================
with tab_carta:
    if df_carta.empty:
        st.warning("⚠️ Por favor, carga tu archivo del catálogo para visualizar el menú.")
    else:
        # Selector de cambio de página
        pag_seleccionada = st.radio(
            "Selecciona una Página:",
            options=[1, 2, 3, 4, 5, 6],
            format_func=lambda x: f"Pág. {x}",
            horizontal=True,
            key="pagina_actual"
        )

        # Cargar el fondo correspondiente de forma limpia detrás de los platos
        imagen_de_esta_pagina = IMAGENES_POR_PAGINA.get(pag_seleccionada, "pag1.jpeg")
        aplicar_fondo(imagen_de_esta_pagina, pag_seleccionada)

        categorias_permitidas = DISTRIBUCION_PAGINAS.get(pag_seleccionada, [])

        # Lista de platos fluyendo directamente sobre tu imagen
        for cat_name in categorias_permitidas:
            df_filtrado_cat = df_carta[df_carta["Category"] == cat_name]
            
            if not df_filtrado_cat.empty:
                st.markdown(f'<div class="titulo-categoria-chifa">📂 {cat_name}</div>', unsafe_allow_html=True)
                
                for idx, row in df_filtrado_cat.iterrows():
                    col_btn, col_txt = st.columns([0.18, 0.82])
                    with col_btn:
                        if st.button("＋", key=f"btn_{row['ID']}"):
                            abrir_modal_agregar_plato(row['ID'], row['Name'], row['Price'])
                    with col_txt:
                        # 🌟 MÁXIMA VISIBILIDAD: Letras blancas, precios amarillos, con sombra negra fuerte para resaltar en tu fondo
                        st.markdown(f"""
                        <div class="fila-plato-limpia">
                            <span style="color: #FFFFFF !important; font-size: 16px !important; font-weight: bold !important; text-align: left !important; font-family: sans-serif !important; text-shadow: 2px 2px 5px rgba(0,0,0,1), -1px -1px 3px rgba(0,0,0,1) !important;">
                                {row['Name']}
                            </span>
                            <span style="color: #FFEB3B !important; font-size: 17px !important; font-weight: bold !important; white-space: nowrap !important; font-family: sans-serif !important; text-shadow: 2px 2px 5px rgba(0,0,0,1) !important; padding-left: 10px;">
                                S/. {float(row['Price']):.2f}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

# =========================================================
# PESTAÑA 2: MI PEDIDO (CARRITO)
# =========================================================
with tab_pedido:
    st.markdown('<div style="background-color: #FFFFFF; padding: 20px; border-radius: 12px; color: #222222; margin-top: 10px; border: 1px solid #E0E0E0;">', unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío. ¡Explora las páginas de la carta y arma tu orden!")
    else:
        st.subheader("📋 Resumen Total del Pedido")
        total = 0

        for idx, item in enumerate(st.session_state.carrito):
            subtotal = item["precio"] * item["cant"]
            total += subtotal

            col_a, col_b = st.columns([0.85, 0.15])
            with col_a:
                st.markdown(f"💥 **{item['cant']}x {item['nombre']}** — S/. {subtotal:.2f}")
                st.markdown(f"<span style='color: #8B0000; font-size: 13px;'>└ 🧂 Salsas: {item['cremas']} | 📝 Nota: {item['notas']}</span>", unsafe_allow_html=True)
            with col_b:
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.carrito.pop(idx)
                    st.rerun()
            st.write("")

        st.divider()
        nombre_cliente = st.text_input("Ingresa tu Nombre Completo:")
        telefono_cliente = st.text_input("Tu número de contacto:")

        if nombre_cliente.strip() and telefono_cliente.strip():
            phone = telefono_cliente.strip()
            mensaje_wa = f"🍜 *CHIFA D' BELINDA*\n\n👤 *Cliente:* {nombre_cliente}\n📞 *Contacto:* {phone}\n-------------------------\n"
            for item in st.session_state.carrito:
                mensaje_wa += f"✅ {item['cant']}x {item['nombre']} - S/. {item['precio'] * item['cant']:.2f}\n"
                if item['cremas'] != "Ninguna":
                    mensaje_wa += f"  • Salsas: {item['cremas']}\n"
                if item['notas'] != "Ninguna":
                    mensaje_wa += f"  • Nota: {item['notas']}\n"
            mensaje_wa += f"-------------------------\n💰 *TOTAL DEL PEDIDO:* S/. {total:.2f}"

            link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"
            st.write("")
            st.link_button("📲 ENVIAR PEDIDO A WHATSAPP", link_final, use_container_width=True)
        else:
            st.write("")
            st.warning("⚠️ Completa tu nombre y número de contacto para poder enviar el pedido.")

        st.write("")
        if st.button("🧹 Vaciar Todo el Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)