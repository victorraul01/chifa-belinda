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
# Opciones del Menú del Día (Limpios, sin texto repetitivo)
# =========================================================
PLATOS_MENU_INTERNO = [
    # --- Platos de la primera sección de la imagen ---
    {"ID": "M01", "Name": "Chaufa de Pollo", "Price": 14.00},
    {"ID": "M02", "Name": "Alita Rebozada", "Price": 15.00},
    {"ID": "M03", "Name": "1/8 Broaster", "Price": 14.00},
    {"ID": "M04", "Name": "Aeropuerto de Pollo", "Price": 17.00},
    {"ID": "M05", "Name": "Combinado de Pollo", "Price": 17.00},
    {"ID": "M06", "Name": "Pollo con Verdura", "Price": 17.00},
    {"ID": "M07", "Name": "Tallarín Saltado de Pollo", "Price": 17.00},
    {"ID": "M08", "Name": "Pollo con Tamarindo", "Price": 17.00},
    {"ID": "M09", "Name": "Alita con Tamarindo", "Price": 17.00},
    {"ID": "M10", "Name": "Lomo Saltado de Pollo", "Price": 17.00},
    {"ID": "M11", "Name": "Alitas 4 Pzs", "Price": 18.00},
    {"ID": "M12", "Name": "Tortilla de Verdura", "Price": 19.00},
    {"ID": "M13", "Name": "Alitas con Piña", "Price": 18.00},
    {"ID": "M14", "Name": "Pollo con Piña", "Price": 19.00},
    {"ID": "M15", "Name": "Chaufa de Chancho", "Price": 20.00},
    {"ID": "M16", "Name": "Chaufa de Res", "Price": 20.00},
    {"ID": "M17", "Name": "Chaufa de Molleja", "Price": 20.00},
    {"ID": "M18", "Name": "Chicharrón de Pollo", "Price": 20.00},
    {"ID": "M19", "Name": "Chi Jau Kay", "Price": 20.00},
    {"ID": "M20", "Name": "Kam Lu Wantan", "Price": 20.00},
    {"ID": "M21", "Name": "Enrollado de Pollo", "Price": 20.00},
    {"ID": "M22", "Name": "Tipa Kay", "Price": 20.00},
    
    # --- Platos de la segunda sección de la imagen ---
    {"ID": "M23", "Name": "Tallarín de Res", "Price": 20.00},
    {"ID": "M24", "Name": "Combinado de Res", "Price": 20.00},
    {"ID": "M25", "Name": "Chancho con Piña", "Price": 20.00},
    {"ID": "M26", "Name": "Chancho con Tamarindo", "Price": 20.00},
    {"ID": "M27", "Name": "¼ Broaster", "Price": 22.00},
    
    # --- Nuevos platos agregados ---
    {"ID": "M28", "Name": "Alitas a la BBQ (3 piezas)", "Price": 18.00},
    {"ID": "M29", "Name": "Alitas Acevichadas (3 piezas)", "Price": 18.00}
]

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
    1: "pag1.jpeg", 2: "pag2.jpeg", 3: "pag3.jpeg",
    4: "pag4.jpeg", 5: "pag5.jpeg", 6: "pag6.jpeg",
    "menu": "pag1.jpeg"
}

def aplicar_fondo(nombre_imagen, pagina_id):
    img_b64 = cargar_imagen_b64(nombre_imagen)
    if img_b64:
        st.markdown(f"""
        <style id="fondo-pagina-{pagina_id}">
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.45)), url('data:image/jpeg;base64,{img_b64}') !important;
            background-size: cover !important;
            background-repeat: no-repeat !important;
            background-position: center center !important;
            background-attachment: fixed !important;
        }}
        .main, [data-testid="stCanvas"], [data-testid="stTabPanel"], div[role="tabpanel"], 
        div[data-testid="stVerticalBlock"], [data-testid="stApp"], [data-testid="stHeader"] {{
            background-color: transparent !important;
            background: transparent !important;
            box-shadow: none !important;
        }}
        </style>
        """, unsafe_allow_html=True)

# 2. INICIALIZACIÓN DEL CARRITO
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# Manejo de la acción de eliminar mediante query params
query_params = st.query_params
if "eliminar_idx" in query_params:
    idx_eliminar = int(query_params["eliminar_idx"])
    if 0 <= idx_eliminar < len(st.session_state.carrito):
        st.session_state.carrito.pop(idx_eliminar)
    st.query_params.clear()
    st.rerun()

# 3. DISTRIBUCION DE PAGINAS (PLATOS A LA CARTA)
DISTRIBUCION_PAGINAS = {
    1: ['COMBOS', 'ALITAS REBOZADAS', 'ALITAS ESPECIALES', 'POLLO BROASTER'],
    2: ['SOPAS', 'CHAUFA'], 3: ['AEROPUERTO', 'COMBINADOS', 'LOMOS SALTADOS'],
    4: ['TALLARINES SALTADOS', 'PLATOS SALADOS', 'PLATOS DULCES', 'TORTILLAS'],
    5: ['ENROLLADOS', 'TAYPA', 'RES', 'LANGOSTINOS', 'PATO', 'CHICHARRONES'],
    6: ['CHANCHO', 'COSTILLAS', 'PORCIONES', 'BEBIDAS FRÍAS', 'BEBIDAS CALIENTES']
}

@st.cache_data
def cargar_catalogo_limpio():
    nombre_archivo = "Catalogo_Productos.xlsx"
    nombre_csv = "Catalogo_Productos.xlsx - in.csv"
    if os.path.exists(nombre_archivo): df = pd.read_excel(nombre_archivo)
    elif os.path.exists(nombre_csv): df = pd.read_csv(nombre_csv)
    else: return pd.DataFrame()
    df.columns = df.columns.str.strip()
    df['Category'] = df['Category'].astype(str).str.strip().str.upper()
    return df

df_carta = cargar_catalogo_limpio()

# 4. MODAL DETALLES DEL PLATO
@st.dialog("Configura tu Plato 🍜")
def abrir_modal_agregar_plato(id_plato, nombre_plato, precio_plato, categoria_plato, tipo_origen="Carta"):
    st.markdown(f"### {nombre_plato}")
    st.markdown(f"**Tipo:** {tipo_origen}")
    st.markdown(f"**Precio Unitario:** S/. {precio_plato:.2f}")
    st.write("---")
    
    # Selector de entrada exclusivo para Menú del Día
    entrada_seleccionada = ""
    if tipo_origen == "Menú del Día":
        st.markdown("**Elige tu Entrada (Incluida):**")
        entrada_seleccionada = st.radio("", ["Sopa Wantán 🥣", "Wantán Frito 🥟"], horizontal=True, label_visibility="collapsed")
        st.write("---")

    cantidad = st.number_input("Cantidad:", min_value=1, max_value=20, value=1, step=1)
    
    st.markdown("**Selecciona tus Cremas / Salsas:**")
    c_aji = st.checkbox("Ají 🌶️")
    c_mayo = st.checkbox("Mayonesa ⚪")
    c_ketchup = st.checkbox("Ketchup 🍅")
    c_tamarindo = st.checkbox("Tamarindo 🍯")
    
    mostrar_limon = any(keyword in categoria_plato for keyword in ["ALITAS", "BROASTER"])
    c_limon = st.checkbox("Limón 🍋") if mostrar_limon else False

    st.write("")
    notas = st.text_input("Notas / Observaciones (Opcional):", placeholder="Ej: Sin cebolla, bien frito...")

    st.markdown("""
    <style>
    div[data-testid="stDialog"] div.stButton > button {
        background-color: #FFEB3B !important; color: #8B0000 !important;
        font-size: 16px !important; font-weight: bold !important;
        border-radius: 8px !important; width: 100% !important; height: 45px !important;
        box-shadow: 0px 3px 5px rgba(0,0,0,0.3) !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("🛒 AGREGAR AL PEDIDO", use_container_width=True, key=f"modal_add_{id_plato}"):
        cremas_list = []
        if c_aji: cremas_list.append("Ají")
        if c_mayo: cremas_list.append("Mayonesa")
        if c_ketchup: cremas_list.append("Ketchup")
        if c_tamarindo: cremas_list.append("Tamarindo")
        if mostrar_limon and c_limon: cremas_list.append("Limón")
        cremas_texto = ", ".join(cremas_list) if cremas_list else ""

        st.session_state.carrito.append({
            "id": id_plato, 
            "nombre": nombre_plato, 
            "precio": float(precio_plato),
            "cant": int(cantidad), 
            "cremas": cremas_texto, 
            "notas": notas.strip(),
            "tipo": tipo_origen,
            "entrada": entrada_seleccionada # Guardamos la entrada elegida
        })
        st.toast(f"¡{cantidad}x {nombre_plato} agregado!")
        st.rerun()

# =========================================================
# 5. CSS MAESTRO GLOBAL
# =========================================================
st.markdown("""
<style>
html, body, [data-testid="stApp"] { margin: 0 !important; padding: 0 !important; }
[data-testid="stMainBlockContainer"] { padding-top: 0px !important; padding-bottom: 0px !important; }
.main .block-container { padding-top: 0px !important; max-width: 100% !important; }

.cabecera-fija-chifa {
    position: fixed !important; top: 0px !important; left: 0px !important; right: 0px !important;
    z-index: 999999 !important; background-color: rgba(0, 0, 0, 0.55) !important;
    backdrop-filter: blur(5px) !important; padding: 15px 10px !important; text-align: center;
    border-bottom: 1px solid rgba(255, 235, 59, 0.2);
}

div[data-testid="stTabs"] { margin-top: 95px !important; }
div[data-testid="stTabs"] > div:first-child { background-color: transparent !important; padding: 4px 10px !important; border-bottom: 2px solid #FFEB3B !important; }
div[data-testid="stTabs"] button p { color: #FFFFFF !important; font-size: 15px !important; font-weight: bold !important; text-shadow: 2px 2px 3px #000000 !important; }

div[data-testid="stRadio"] {
    background-color: rgba(0, 0, 0, 0.4) !important; padding: 8px 12px !important;
    border: 1px solid rgba(255, 235, 59, 0.4) !important; border-radius: 8px !important; margin-bottom: 10px !important;
}
div[data-testid="stRadio"] label { color: #FFFFFF !important; font-weight: bold !important; text-shadow: 2px 2px 2px #000000 !important; }

.contenedor-plato-unico {
    display: flex !important; flex-direction: row !important; justify-content: space-between !important;
    align-items: center !important; width: 100% !important; padding: 10px 0px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.25) !important;
}
.texto-nombre-plato { color: #FFFFFF !important; font-size: 15px !important; font-weight: bold !important; text-shadow: 2px 2px 2px #000000 !important; flex-grow: 1 !important; text-align: left !important; }
.texto-precio-plato { color: #FFEB3B !important; font-size: 16px !important; font-weight: 900 !important; text-shadow: 2px 2px 2px #000000 !important; white-space: nowrap !important; padding-right: 15px !important; }

.fila-carrito-ordenada {
    padding: 12px 0px !important; border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important; width: 100%;
}
.linea-principal-carrito {
    display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: space-between !important;
    width: 100% !important; margin-bottom: 4px !important;
}
.btn-tacho-mini {
    background-color: #FFEB3B !important; color: #8B0000 !important; text-decoration: none !important;
    font-size: 11px !important; padding: 3px 5px !important; border-radius: 4px !important;
    font-weight: bold !important; margin-right: 8px !important; display: inline-block !important;
    box-shadow: 0px 1px 3px rgba(0,0,0,0.5) !important;
}
.texto-plato-carrito { color: #FFFFFF !important; font-size: 16px !important; font-weight: bold !important; text-shadow: 2px 2px 2px #000000 !important; flex-grow: 1 !important; text-align: left !important; }
.texto-precio-carrito { color: #FFFFFF !important; font-size: 16px !important; font-weight: bold !important; text-shadow: 2px 2px 2px #000000 !important; white-space: nowrap !important; }
.texto-detalles-resaltados { color: #FFFFFF !important; font-size: 13px !important; font-weight: 500 !important; text-shadow: 1px 1px 2px #000000 !important; display: block; margin-left: 30px; opacity: 0.95; }

div.boton-agregar-carta button {
    background-color: #FFEB3B !important; color: #8B0000 !important; font-size: 20px !important; font-weight: bold !important;
    border-radius: 50% !important; width: 38px !important; height: 38px !important; min-width: 38px !important;
    border: none !important; box-shadow: 0px 3px 5px rgba(0,0,0,0.5) !important; padding: 0px !important;
}

.enlace-wa-directo-siempre {
    display: block !important; background-color: #25D366 !important; color: white !important;
    text-align: center !important; font-weight: bold !important; font-size: 16px !important;
    padding: 14px 20px !important; border-radius: 8px !important; text-decoration: none !important;
    box-shadow: 0px 5px 10px rgba(0,0,0,0.4) !important; margin: 18px 0px !important; border: 1px solid #ffffff !important;
}
.enlace-wa-directo-siempre:active { background-color: #128C7E !important; }

div.boton-normal-ancho button {
    background-color: #FFEB3B !important; color: #8B0000 !important; font-size: 15px !important; font-weight: bold !important;
    border-radius: 8px !important; width: 100% !important; height: 42px !important; border: none !important; box-shadow: 0px 3px 5px rgba(0,0,0,0.3) !important;
}

.titulo-categoria-chifa { color: #FFEB3B !important; font-size: 17px !important; font-weight: bold !important; padding: 10px 4px !important; margin-top: 15px !important; margin-bottom: 5px !important; border-left: 5px solid #FFEB3B !important; text-shadow: 2px 2px 3px #000000 !important; }
.alerta-delivery-destacada { background-color: rgba(0, 0, 0, 0.75) !important; border: 2px solid #FFEB3B !important; padding: 15px !important; border-radius: 10px !important; color: #FFFFFF !important; font-size: 14px !important; line-height: 1.5 !important; text-shadow: 1px 1px 2px #000000 !important; margin-top: 10px; margin-bottom: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.5) !important; }
.recuadro-total-final {
    background-color: rgba(0, 0, 0, 0.5) !important; border: 1px solid #FFEB3B !important; border-radius: 8px !important;
    padding: 12px 15px !important; margin: 20px 0px !important; display: flex !important; justify-content: space-between !important; align-items: center !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 6. ENCABEZADO FIJO
# =========================================================
st.markdown("""
<div class="cabecera-fija-chifa">
    <h2 style="margin: 0; font-size: 25px; color: #FFEB3B; font-family: sans-serif; text-shadow: 2px 2px 4px #000000;">🍜 CHIFA D' BELINDA</h2>
    <p style="margin: 3px 0 0 0; font-size: 13px; color: #FFFFFF; text-shadow: 1px 1px 2px #000000;">Pedidos en línea rápidos y directos a nuestro WhatsApp</p>
</div>
""", unsafe_allow_html=True)

items_en_carrito = sum(item["cant"] for item in st.session_state.carrito)

# =========================================================
# 7. CREACIÓN DE PESTAÑAS
# =========================================================
tab_menu, tab_carta, tab_pedido = st.tabs([
    "🍱 Menú del Día", 
    "📖 Platos a la Carta", 
    f"🛒 Mi Pedido ({items_en_carrito})"
])

# =========================================================
# PESTAÑA: 🍱 MENÚ DEL DÍA
# =========================================================
with tab_menu:
    st.markdown('<div style="padding: 10px 5px; margin-top: 15px;">', unsafe_allow_html=True)
    aplicar_fondo("pag1.jpeg", "menu")
    
    # Texto movido al encabezado de la sección de manera vistosa
    st.markdown('<div class="titulo-categoria-chifa">🍱 MENÚ CHIFA (INCLUYE: SOPA WANTÁN O WANTÁN FRITO + REFRESCO)</div>', unsafe_allow_html=True)
    
    # Renderizado directo de los platos limpios
    for plato in PLATOS_MENU_INTERNO:
        col_info, col_btn = st.columns([0.84, 0.16])
        with col_info:
            st.markdown(f"""
            <div class="contenedor-plato-unico">
                <span class="texto-nombre-plato">{plato['Name']}</span>
                <span class="texto-precio-plato">S/. {plato['Price']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            st.markdown('<div class="boton-agregar-carta">', unsafe_allow_html=True)
            if st.button("＋", key=f"btn_menu_{plato['ID']}"):
                abrir_modal_agregar_plato(plato['ID'], plato['Name'], plato['Price'], "MENÚ", tipo_origen="Menú del Día")
            st.markdown('</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# PESTAÑA: 📖 PLATOS A LA CARTA
# =========================================================
with tab_carta:
    if df_carta.empty:
        st.warning("⚠️ Por favor, carga tu archivo del catálogo.")
    else:
        pag_seleccionada = st.radio("Selecciona una Página de la Carta:", options=[1, 2, 3, 4, 5, 6], format_func=lambda x: f"Pág. {x}", horizontal=True, key="pagina_actual")
        imagen_de_esta_pagina = IMAGENES_POR_PAGINA.get(pag_seleccionada, "pag1.jpeg")
        aplicar_fondo(imagen_de_esta_pagina, pag_seleccionada)

        categorias_permitidas = DISTRIBUCION_PAGINAS.get(pag_seleccionada, [])
        for cat_name in categorias_permitidas:
            df_filtrado_cat = df_carta[df_carta["Category"] == cat_name]
            if not df_filtrado_cat.empty:
                st.markdown(f'<div class="titulo-categoria-chifa">📂 {cat_name}</div>', unsafe_allow_html=True)
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
                        st.markdown('<div class="boton-agregar-carta">', unsafe_allow_html=True)
                        if st.button("＋", key=f"btn_{row['ID']}"):
                            abrir_modal_agregar_plato(row['ID'], row['Name'], row['Price'], cat_name, tipo_origen="Carta")
                        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# PESTAÑA: 🛒 MI PEDIDO
# =========================================================
with tab_pedido:
    st.markdown('<div style="padding: 10px 5px; margin-top: 15px;">', unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.markdown('<h3 style="color: white; text-shadow: 2px 2px 2px black;">Tu carrito está vacío. ¡Explora la carta!</h3>', unsafe_allow_html=True)
    else:
        st.markdown('<h2 style="color: #FFEB3B; text-shadow: 2px 2px 3px black; font-size:22px;">📋 Resumen Total del Pedido</h2>', unsafe_allow_html=True)
        total = 0

        for idx, item in enumerate(st.session_state.carrito):
            subtotal = item["precio"] * item["cant"]
            total += subtotal

            origen_tipo = item.get("tipo", "Carta")
            detalles_lista = [f"📌 Tipo: {origen_tipo}"]
            
            # Si el plato tiene entrada seleccionada, la mostramos en la lista de detalles
            if item.get("entrada"):
                detalles_lista.append(f"🍲 Entrada: {item['entrada']}")
                
            if item['cremas']: detalles_lista.append(f"🧂 {item['cremas']}")
            if item['notas']: detalles_lista.append(f"📝 {item['notas']}")
            
            detalles_html = f'<span class="texto-detalles-resaltados">{" | ".join(detalles_lista)}</span>'

            st.markdown(f"""
            <div class="fila-carrito-ordenada">
                <div class="linea-principal-carrito">
                    <span style="display: flex; align-items: center;">
                        <a href="?eliminar_idx={idx}" target="_self" class="btn-tacho-mini">🗑️</a>
                        <span class="texto-plato-carrito">💥 {item['cant']}x {item['nombre']}</span>
                    </span>
                    <span class="texto-precio-carrito">S/. {subtotal:.2f}</span>
                </div>
                {detalles_html}
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="recuadro-total-final">
            <span style="color: #FFFFFF; font-size: 17px; font-weight: bold; text-shadow: 1px 1px 2px #000000;">💵 TOTAL DEL PEDIDO:</span>
            <span style="color: #FFEB3B; font-size: 20px; font-weight: 900; text-shadow: 1px 1px 3px #000000;">S/. {total:.2f}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<span style="color: white; font-weight: bold; text-shadow: 1px 1px 2px black; font-size: 16px;">Ingresa tu Nombre Completo:</span>', unsafe_allow_html=True)
        nombre_cliente = st.text_input("", label_visibility="collapsed", key="nom_cli")
        
        st.write("")
        st.markdown('<span style="color: white; font-weight: bold; text-shadow: 1px 1px 2px black; font-size: 16px;">Método de Entrega:</span>', unsafe_allow_html=True)
        metodo_entrega = st.radio("", ["Delivery Moto 🏍️", "Recojo en Local 🏪"], horizontal=True, label_visibility="collapsed", key="met_ent")

        direccion_cliente = ""
        if metodo_entrega == "Delivery Moto 🏍️":
            st.write("")
            st.markdown('<span style="color: white; font-weight: bold; text-shadow: 1px 1px 2px black; font-size: 14px;">Dirección de Envío:</span>', unsafe_allow_html=True)
            direccion_cliente = st.text_input("", placeholder="Ej: Av. Perú 123, dpto 402...", label_visibility="collapsed", key="dir_cli")
            
            st.markdown("""
            <div class="alerta-delivery-destacada">
                🚨 <span style="color: #FFEB3B; font-weight: bold; font-size: 15px;">¡AVISO IMPORTANTE DE DELIVERY!</span><br>
                1️⃣ Después de enviar el mensaje, <b>compártenos tu ubicación actual por WhatsApp</b> para que el motorizado llegue rápido.<br>
                2️⃣ <b>Costo de envío:</b> Se calculará y te lo enviaremos inmediatamente después de recibir tu lista de platos.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alerta-delivery-destacada" style="border-color: #4CAF50;">
                🏪 <span style="color: #4CAF50; font-weight: bold; font-size: 15px;">PEDIDO PARA RECOJO EN LOCAL</span><br>
                ⏳ Su comida estará lista y empacada con cuidado en aproximadamente <b>20 a 30 minutos</b>. ¡Te esperamos!
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown('<span style="color: white; font-weight: bold; text-shadow: 1px 1px 2px black; font-size: 16px;">Método de Pago:</span>', unsafe_allow_html=True)
        metodo_pago = st.radio("", ["Yape 📱", "Efectivo 💵"], horizontal=True, label_visibility="collapsed", key="met_pag")

        st.write("")
        
        # 🛡️ VALIDACIÓN EN TIEMPO REAL
        error_validacion = None
        if not nombre_cliente.strip():
            error_validacion = "Completa tu nombre completo para poder enviar el pedido."
        elif metodo_entrega == "Delivery Moto 🏍️" and not direccion_cliente.strip():
            error_validacion = "Seleccionaste Delivery Moto, debes escribir una Dirección de Envío."

        # Construcción dinámica del mensaje de WhatsApp
        mensaje_wa = f"🍜 *CHIFA D' BELINDA*\n\n"
        mensaje_wa += f"👤 *Cliente:* {nombre_cliente.strip()}\n"
        mensaje_wa += f"🛵 *Entrega:* {metodo_entrega}\n"
        if metodo_entrega == "Delivery Moto 🏍️": 
            mensaje_wa += f"📍 *Dirección:* {direccion_cliente.strip()}\n"
        mensaje_wa += f"💳 *Pago:* {metodo_pago}\n"
        mensaje_wa += f"-------------------------\n"
        
        for item in st.session_state.carrito:
            tipo_item = item.get("tipo", "Carta")
            mensaje_wa += f"✅ {item['cant']}  {item['nombre']} ({tipo_item}) - S/. {item['precio'] * item['cant']:.2f}\n"
            detalles_wa = []
            if item.get("entrada"): detalles_wa.append(f"Entrada: {item['entrada']}")
            if item['cremas']: detalles_wa.append(f"{item['cremas']}")
            if item['notes' if 'notes' in item else 'notas']: detalles_wa.append(f"{item['notas']}")
            if detalles_wa:
                mensaje_wa += f"  • {" | ".join(detalles_wa)}\n"
        
        mensaje_wa += f"-------------------------\n"
        mensaje_wa += f"💰 *TOTAL A PAGAR:* S/. {total:.2f}\n"
        if metodo_entrega == "Delivery Moto 🏍️": 
            mensaje_wa += f"ℹ️ _El costo de delivery se sumará en breve._"

        link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"

        # 🟢 MOSTRAR EL BOTÓN VERDE DIRECTO
        if error_validacion:
            st.warning(f"⚠️ {error_validacion}")
            st.markdown(f"""
                <a href="#" onclick="alert('{error_validacion}'); return false;" class="enlace-wa-directo-siempre">
                     💬 ENVIAR PEDIDO A WHATSAPP
                </a>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <a href="{link_final}" target="_blank" class="enlace-wa-directo-siempre">
                    💬 ENVIAR PEDIDO A WHATSAPP
                </a>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="boton-normal-ancho">', unsafe_allow_html=True)
        if st.button("🧹 Vaciar Todo el Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)