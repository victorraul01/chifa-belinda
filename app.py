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
        .main, [data-testid="stCanvas"], [data-testid="stTabPanel"], div[role="tabpanel"] {{
            background-color: transparent !important;
            background: transparent !important;
        }}
        </style>
        """, unsafe_allow_html=True)

# 2. INICIALIZACIÓN DEL CARRITO Y ESTADO DE PÁGINA
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = 1

# =========================================================
# 3. DICCIONARIO MAESTRO DE DISTRIBUCIÓN DE PÁGINAS (ESTRICTO)
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
# 5. CSS MAESTRO: ENCABEZADO ESTÁTICO Y CORRECCIÓN DE SCROLL
# =========================================================
st.markdown("""
<style>
/* Desactivar scroll exterior en celulares */
html, body, [data-testid="stApp"] {
    overflow: hidden !important;
    height: 100vh !important;
    position: relative;
}

.main .block-container {
    padding: 0px !important;
    max-width: 100% !important;
    height: 100vh !important;
}

/* ENCABEZADO SUPERIOR FIJO (STICKY) EN BLANCO ORIGINAL */
.encabezado-fijo-blanco {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    background-color: #FFFFFF !important;
    z-index: 999999 !important;
    padding: 12px 16px 4px 16px !important;
    border-bottom: 1px solid #E0E0E0 !important;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.05) !important;
}

/* REUBICACIÓN DE LAS PESTAÑAS NATIVAS DE STREAMLIT ARRIBA */
div[data-testid="stTabs"] > div:first-child {
    position: fixed !important;
    top: 68px !important;
    left: 0 !important;
    width: 100% !important;
    background-color: #FFFFFF !important;
    z-index: 999998 !important;
    padding: 0 16px !important;
    border-bottom: 1px solid #EEEEEE !important;
}

/* REUBICACIÓN DEL SELECTOR DE PÁGINAS (RADIO) ARRIBA */
.bloque-paginas-fijo {
    position: fixed !important;
    top: 116px !important;
    left: 0 !important;
    width: 100% !important;
    background-color: #FFFFFF !important;
    z-index: 999997 !important;
    padding: 10px 16px !important;
    border-bottom: 2px solid #8B0000 !important;
    box-shadow: 0px 4px 6px rgba(0,0,0,0.05) !important;
}

/* CONTROL DE SCROLL EXCLUSIVO PARA LOS PLATOS ABAJO DEL BLOQUE FIJO */
div[data-testid="stTabs"] > div:nth-child(2) {
    height: calc(100vh - 180px) !important;
    overflow-y: auto !important;
    -webkit-overflow-scrolling: touch !important;
    margin-top: 180px !important;
}

.contenedor-scroll-platos {
    padding: 10px 16px 120px 16px !important;
    box-sizing: border-box !important;
}

/* Estilos de botones y títulos */
div.stButton > button {
    background-color: #FFEB3B !important;
    color: #8B0000 !important;
    font-size: 20px !important;
    font-weight: bold !important;
    border-radius: 50% !important;
    width: 42px !important;
    height: 42px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: none !important;
    box-shadow: 0px 3px 6px rgba(0,0,0,0.4) !important;
}

.titulo-categoria-chifa {
    color: #FFEB3B !important;
    font-size: 15px !important;
    font-weight: bold !important;
    background-color: rgba(139, 0, 0, 0.9) !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    margin-top: 16px !important;
    margin-bottom: 10px !important;
    border-left: 5px solid #FFEB3B !important;
}

.fila-plato-limpia {
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    padding: 10px 4px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 6. ESTRUCTURA FIJA SUPERIOR (STICKY ENCABEZADO)
# =========================================================
st.markdown("""
<div class="encabezado-fijo-blanco">
    <h3 style="margin: 0; padding: 0; font-size: 20px; color: #8B0000; font-family: sans-serif;">🍜 Chifa D' Belinda</h3>
    <p style="margin: 2px 0 0 0; padding: 0; font-size: 12px; color: #666666; font-family: sans-serif;">Pedidos en línea rápidos y directos a nuestro WhatsApp</p>
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
        # Bloque estático arriba para el control de páginas
        st.markdown('<div class="bloque-paginas-fijo">', unsafe_allow_html=True)
        pag_seleccionada = st.radio(
            "Selecciona una Página:",
            options=[1, 2, 3, 4, 5, 6],
            format_func=lambda x: f"Pág. {x}",
            horizontal=True,
            label_visibility="collapsed",
            key="pagina_actual"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Cargar fondo correspondiente de la página
        imagen_de_esta_pagina = IMAGENES_POR_PAGINA.get(pag_seleccionada, "pag1.jpeg")
        aplicar_fondo(imagen_de_esta_pagina, pag_seleccionada)

        # 🌟 OBTENER CATEGORÍAS ESTRICTAS DE ESTA PÁGINA (Previene el desorden)
        categorias_permitidas = DISTRIBUCION_PAGINAS.get(pag_seleccionada, [])

        st.markdown('<div class="contenedor-scroll-platos">', unsafe_allow_html=True)
        
        # Iterar en el orden exacto que me diste en la lista
        for cat_name in categorias_permitidas:
            # Filtrar del Excel solo los productos que pertenecen a esta categoría exacta
            df_filtrado_cat = df_carta[df_carta["Category"] == cat_name]
            
            if not df_filtrado_cat.empty:
                st.markdown(f'<div class="titulo-categoria-chifa">📂 {cat_name}</div>', unsafe_allow_html=True)
                
                for idx, row in df_filtrado_cat.iterrows():
                    col_btn, col_txt = st.columns([0.16, 0.84])
                    with col_btn:
                        if st.button("＋", key=f"btn_{row['ID']}"):
                            abrir_modal_agregar_plato(row['ID'], row['Name'], row['Price'])
                    with col_txt:
                        st.markdown(f"""
                        <div class="fila-plato-limpia">
                            <span style="color: #FFFFFF !important; font-size: 15px !important; font-weight: bold !important; text-align: left !important; font-family: sans-serif !important; text-shadow: 1.5px 1.5px 4px rgba(0,0,0,0.9) !important;">
                                {row['Name']}
                            </span>
                            <span style="color: #FFEB3B !important; font-size: 16px !important; font-weight: bold !important; white-space: nowrap !important; font-family: sans-serif !important; text-shadow: 1.5px 1.5px 4px rgba(0,0,0,0.9) !important; padding-left: 10px;">
                                S/. {float(row['Price']):.2f}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# PESTAÑA 2: MI PEDIDO (CARRITO)
# =========================================================
with tab_pedido:
    st.markdown('<div class="contenedor-scroll-platos" style="background-color: #FFFFFF; min-height: 100vh; color: #222222;">', unsafe_allow_html=True)
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