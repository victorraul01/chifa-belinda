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

# Mapeo página -> archivo de imagen de fondo
IMAGENES_POR_PAGINA = {
    1: "pag1.jpg",
    2: "pag2.jpg",
    3: "pag3.jpg",
    4: "pag4.jpg",
    5: "pag5.jpg",
    6: "pag6.jpg",
}

def aplicar_fondo(nombre_imagen):
    img_b64 = cargar_imagen_b64(nombre_imagen)
    if img_b64:
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url('data:image/jpeg;base64,{img_b64}') !important;
            background-size: cover !important;
            background-repeat: no-repeat !important;
            background-position: center center !important;
            background-attachment: fixed !important;
        }}
        </style>
        """, unsafe_allow_html=True)

# 2. INICIALIZACIÓN DEL CARRITO Y ESTADO DE PÁGINA
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = 1

# 3. CARGA DE DATOS (CACHEADA)
@st.cache_data
def cargar_catalogo_con_paginas_corregido():
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

    def mapear_fila_a_pagina(cat):
        if cat in ['COMBOS', 'ALITAS REBOZADAS', 'ALITAS ESPECIALES', 'POLLO BROASTER']:
            return 1
        elif cat in ['SOPAS', 'CHAUFA']:
            return 2
        elif cat in ['AEROPUERTO', 'COMBINADOS', 'LOMOS SALTADOS']:
            return 3
        elif cat in ['TALLARINES SALTADOS', 'PLATOS SALADOS', 'PLATOS DULCE', 'TORTILLAS']:
            return 4
        elif cat in ['ENROLLADOS', 'TAYPA', 'RES', 'LANGOSTINOS', 'PATO', 'CHICHARRONES']:
            return 5
        elif cat in ['CHANCHO', 'COSTILLAS', 'PORCIONES', 'BEBIDAS CALIENTES', 'BEBIDAS FRÍAS']:
            return 6
        return 1

    df['Page_Num'] = df['Category'].apply(mapear_fila_a_pagina)
    return df

df_carta = cargar_catalogo_con_paginas_corregido()

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

# 5. CSS GLOBAL: HEADER Y TABS FIJOS, LISTA CON SCROLL
st.markdown("""
<style>
html, body, [data-testid="stApp"] {
    overflow-y: auto !important;
    height: auto !important;
}

.block-container {
    padding-left: 0px !important;
    padding-right: 0px !important;
    padding-top: 0px !important;
    max-width: 100% !important;
}

/* ENCABEZADO FIJO (NO SE MUEVE CON EL SCROLL) */
.encabezado-fijo-global {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    background-color: #8B0000 !important;
    z-index: 999999 !important;
    text-align: center !important;
    padding: 12px 0 6px 0 !important;
    border-bottom: 2px solid #FFEB3B !important;
}

/* PESTAÑAS (CARTA / PEDIDO) FIJAS DEBAJO DEL ENCABEZADO */
div[data-testid="stTabs"] > div:first-child {
    position: fixed !important;
    top: 48px !important;
    left: 0 !important;
    width: 100% !important;
    background-color: #8B0000 !important;
    z-index: 999998 !important;
    padding: 2px 10px !important;
}

button[data-baseweb="tab"] {
    color: #FFAAAA !important;
    font-weight: bold !important;
}
button[aria-selected="true"] {
    color: #FFEB3B !important;
    border-bottom-color: #FFEB3B !important;
}

/* SELECTOR DE PÁGINAS FIJO, JUSTO DEBAJO DE LAS PESTAÑAS */
.bloque-paginas-estatico {
    position: fixed !important;
    top: 94px !important;
    left: 0 !important;
    width: 100% !important;
    background-color: #8B0000 !important;
    z-index: 999997 !important;
    padding: 5px 14px 12px 14px !important;
    box-shadow: 0px 6px 12px rgba(0,0,0,0.6) !important;
    border-bottom: 3px solid #FFEB3B !important;
}

/* ESPACIADOR: empuja el contenido scrolleable debajo de toda la cabecera fija */
.compensar-cabecera-bloqueada {
    height: 160px !important;
    width: 100% !important;
}

.contenedor-menu-platos {
    padding: 10px 14px 60px 14px !important;
    box-sizing: border-box !important;
}

.titulo-categoria-resaltado {
    background: linear-gradient(90deg, #8B0000 0%, rgba(140,7,18,0.95) 100%) !important;
    color: #FFEB3B !important;
    font-size: 13px !important;
    font-weight: bold !important;
    padding: 10px 14px !important;
    border-radius: 6px !important;
    margin: 20px 0 12px 0 !important;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.9) !important;
    border-left: 5px solid #FFEB3B !important;
}

/* FILA DE PLATO: nombre + precio alineados, botón + al costado */
.bloque-fila-interactiva {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    background: rgba(0, 0, 0, 0.85) !important;
    padding: 8px 12px !important;
    margin-bottom: 10px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

.caja-texto-plato {
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    padding-left: 12px !important;
}

.nombre-plato-unificado {
    color: #FFFFFF !important;
    font-size: 13.5px !important;
    font-weight: bold !important;
    text-align: left !important;
    line-height: 1.3;
}

.precio-plato-unificado {
    color: #FFEB3B !important;
    font-size: 14.5px !important;
    font-weight: bold !important;
    white-space: nowrap !important;
}

/* Botón redondo amarillo "＋" */
div.stButton > button {
    background-color: #FFEB3B !important;
    color: #8B0000 !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: none !important;
    box-shadow: 0px 3px 6px rgba(0,0,0,0.5) !important;
}
</style>
""", unsafe_allow_html=True)

# 6. ENCABEZADO FIJO DE LA APP
st.markdown(
    '<div class="encabezado-fijo-global">'
    '<span style="color:#FFFFFF; font-size:19px; font-weight:bold;">🍜 CHIFA D\' BELINDA</span>'
    '</div>',
    unsafe_allow_html=True
)

items_en_carrito = sum(item["cant"] for item in st.session_state.carrito)

tab_carta, tab_pedido = st.tabs([
    "📖 Nuestra Carta", f"🛒 Mi Pedido ({items_en_carrito})"
])

# =========================================================
# PESTAÑA 1: NUESTRA CARTA
# =========================================================
with tab_carta:
    if df_carta.empty:
        st.warning("⚠️ Carga tu archivo del catálogo para visualizar el menú.")
    else:
        st.markdown('<div class="bloque-paginas-estatico">', unsafe_allow_html=True)
        pag_seleccionada = st.radio(
            "Selecciona una Página:",
            options=[1, 2, 3, 4, 5, 6],
            format_func=lambda x: f"Pág. {x}",
            horizontal=True,
            label_visibility="collapsed",
            key="pagina_actual"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Fondo dinámico: cambia según la página seleccionada
        imagen_de_esta_pagina = IMAGENES_POR_PAGINA.get(pag_seleccionada, "pag1.jpg")
        aplicar_fondo(imagen_de_esta_pagina)

        df_filtrado = df_carta[df_carta["Page_Num"] == pag_seleccionada]

        st.markdown('<div class="compensar-cabecera-bloqueada"></div>', unsafe_allow_html=True)

        st.markdown('<div class="contenedor-menu-platos">', unsafe_allow_html=True)
        categoria_actual = ""
        for idx, row in df_filtrado.iterrows():
            if str(row['Category']).strip() != categoria_actual:
                categoria_actual = str(row['Category']).strip()
                st.markdown(f'<div class="titulo-categoria-resaltado">📂 {categoria_actual}</div>', unsafe_allow_html=True)

            st.markdown('<div class="bloque-fila-interactiva">', unsafe_allow_html=True)
            col_btn, col_txt = st.columns([0.16, 0.84])
            with col_btn:
                if st.button("＋", key=f"btn_{row['ID']}"):
                    abrir_modal_agregar_plato(row['ID'], row['Name'], row['Price'])
            with col_txt:
                st.markdown(f"""
                <div class="caja-texto-plato">
                    <span class="nombre-plato-unificado">{row['Name']}</span>
                    <span class="precio-plato-unificado">S/. {float(row['Price']):.2f}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# PESTAÑA 2: MI PEDIDO (CARRITO)
# =========================================================
with tab_pedido:
    # Fondo sólido oscuro para facilitar lectura en esta pestaña
    st.markdown("""
    <style>
    .stApp { background-image: none !important; background-color: #111111 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="compensar-cabecera-bloqueada" style="height:100px !important;"></div>', unsafe_allow_html=True)

    st.markdown('<div class="contenedor-menu-platos" style="color:#FFFFFF;">', unsafe_allow_html=True)
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
                st.markdown(
                    f"<span style='color:#FFEB3B; font-size:12px;'>└ 🧂 Cremas: {item['cremas']} | 📝 Nota: {item['notas']}</span>",
                    unsafe_allow_html=True
                )
            with col_b:
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.carrito.pop(idx)
                    st.rerun()
            st.write("")

        st.divider()
        nombre_cliente = st.text_input("Ingresa tu Nombre Completo:")
        telefono_cliente = st.text_input("Tu número de contacto:")

        if nombre_cliente.strip() and telefono_cliente.strip():
            mensaje_wa = f"🍜 *CHIFA D' BELINDA*\n\n👤 *Cliente:* {nombre_cliente}\n📞 *Contacto:* {telefono_cliente}\n-------------------------\n"
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