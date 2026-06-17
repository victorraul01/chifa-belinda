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
            background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.45)), url('data:image/jpeg;base64,{img_b64}') !important;
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
# 3. DICCIONARIO MAESTRO DE DISTRIBUCION DE PAGINAS
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
def abrir_modal_agregar_plato(id_plato, nombre_plato, precio_plato, categoria_plato):
    st.markdown(f"### {nombre_plato}")
    st.markdown(f"**Precio Unitario:** S/. {precio_plato:.2f}")
    st.write("---")

    cantidad = st.number_input("Cantidad:", min_value=1, max_value=20, value=1, step=1)

    st.markdown("**Selecciona tus Cremas / Salsas:**")
    
    c_aji = st.checkbox("Ají Chi Chon San 🌶️")
    c_mayo = st.checkbox("Mayonesa ⚪")
    c_ketchup = st.checkbox("Ketchup 🍅")
    c_tamarindo = st.checkbox("Salsa Tamarindo 🍯")
    
    mostrar_limon = any(keyword in categoria_plato for keyword in ["ALITAS", "BROASTER"])
    c_limon = False
    if mostrar_limon:
        c_limon = st.checkbox("Limón 🍋")

    st.write("")
    notas = st.text_input("Notas / Observaciones (Opcional):", placeholder="Ej: Sin cebolla, bien frito...")

    st.write("")
    
    st.markdown(f"""
    <style>
    div[data-testid="stDialog"] div.stButton > button {{
        background-color: #FFEB3B !important;
        color: #8B0000 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        width: 100% !important;
        height: 45px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: none !important;
        box-shadow: 0px 3px 5px rgba(0,0,0,0.3) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    if st.button("🛒 AGREGAR AL PEDIDO", use_container_width=True, key=f"modal_add_{id_plato}"):
        cremas_list = []
        if c_aji: cremas_list.append("Ají")
        if c_mayo: cremas_list.append("Mayo")
        if c_ketchup: cremas_list.append("Ketchup")
        if c_tamarindo: cremas_list.append("Tamarindo")
        if mostrar_limon and c_limon: cremas_list.append("Limón")

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
# 5. CSS MAESTRO: ENCABEZADO FIJO Y SOLUCIÓN DE ALINEACIÓN
# =========================================================
st.markdown("""
<style>
html, body, [data-testid="stApp"] {
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 0px !important;
    padding-bottom: 0px !important;
}

.main .block-container {
    padding-top: 0px !important;
    max-width: 100% !important;
}

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

div[data-testid="stTabs"] {
    margin-top: 95px !important; 
}

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
    background-color: rgba(0, 0, 0, 0.3) !important;
    backdrop-filter: blur(2px);
    padding: 10px !important;
    border: 1px solid #FFEB3B !important;
    border-radius: 8px !important;
    margin-bottom: 15px !important;
}

div[data-testid="stRadio"] label {
    color: #FFFFFF !important;
    font-weight: bold !important;
    text-shadow: 2px 2px 2px #000000 !important;
}

/* CONTENEDOR EXCLUSIVO PARA FORZAR ALINEACIÓN EN EL CARRITO */
.fila-carrito-ajustada {
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    padding: 10px 0px;
}

.bloque-texto-carrito {
    flex-grow: 1 !important;
    padding-right: 10px !important;
}

/* CLASE ESPECÍFICA PARA LOS BOTONES REDONDOS "+" DE LA CARTA */
div.boton-agregar-carta button {
    background-color: #FFEB3B !important;
    color: #8B0000 !important;
    font-size: 20px !important;
    font-weight: bold !important;
    border-radius: 50% !important;
    width: 38px !important;
    height: 38px !important;
    min-width: 38px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: none !important;
    box-shadow: 0px 3px 5px rgba(0,0,0,0.5) !important;
    padding: 0px !important;
}

/* BOTONES GENERALES DE ANCHO COMPLETO (ENVIAR Y VACIAR) */
div.boton-normal-ancho button {
    background-color: #FFEB3B !important;
    color: #8B0000 !important;
    font-size: 15px !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    width: 100% !important;
    height: 45px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: none !important;
    box-shadow: 0px 3px 5px rgba(0,0,0,0.3) !important;
}

/* REPARACIÓN DEFINITIVA DEL BOTÓN DE ELIMINAR */
div.boton-eliminar-carrito button {
    background-color: #FFEB3B !important;
    color: #8B0000 !important;
    font-size: 16px !important;
    border-radius: 8px !important;
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: none !important;
    padding: 0px !important;
    box-shadow: 0px 2px 4px rgba(0,0,0,0.4) !important;
}

.texto-detalles-carrito {
    color: #FFFFFF !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-shadow: 1px 1px 2px #000000, -1px -1px 2px #000000 !important;
    display: block;
    margin-top: 2px;
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

/* AVISO LLAMATIVO PARA EL DELIVERY */
.alerta-delivery-personalizada {
    background-color: rgba(255, 235, 59, 0.15) !important;
    border: 1px solid #FFEB3B !important;
    padding: 12px !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
    text-shadow: 1px 1px 2px #000000 !important;
    margin-top: 10px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 6. ENCABEZADO CON CUADRO OSCURO FIJO TOTALMENTE
# =========================================================
st.markdown("""
<div class="cabecera-fija-chifa">
    <h2 style="margin: 0; font-size: 25px; color: #FFEB3B; font-family: sans-serif; text-shadow: 2px 2px 4px #000000, -2px -2px 4px #000000;">🍜 CHIFA D' BELINDA</h2>
    <p style="margin: 3px 0 0 0; font-size: 13px; color: #FFFFFF; text-shadow: 1px 1px 2px #000000, -1px -1px 2px #000000;">Pedidos en línea rápidos y directos a nuestro WhatsApp</p>
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
                            abrir_modal_agregar_plato(row['ID'], row['Name'], row['Price'], cat_name)
                        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# PESTAÑA 2: MI PEDIDO (CARRITO)
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

            # Usamos columnas nativas de Streamlit combinadas con contenedores limpios
            col_resumen, col_accion = st.columns([0.84, 0.16])
            
            with col_resumen:
                st.markdown(f"""
                <div class="bloque-texto-carrito">
                    <span style='color: #FFFFFF; font-size: 16px; font-weight: bold; text-shadow: 2px 2px 2px #000000;'>💥 {item['cant']}x {item['nombre']} — S/. {subtotal:.2f}</span>
                    <span class='texto-detalles-carrito'>🧂 Salsas: {item['cremas']} | 📝 Nota: {item['notes' if 'notes' in item else 'notas']}</span>
                </div>
                """, unsafe_allow_html=True)
                
            with col_accion:
                st.markdown('<div class="boton-eliminar-carrito">', unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.carrito.pop(idx)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        st.divider()
        
        # Formulario de Envío Renovado
        st.markdown('<span style="color: white; font-weight: bold; text-shadow: 1px 1px 2px black; font-size: 16px;">Ingresa tu Nombre Completo:</span>', unsafe_allow_html=True)
        nombre_cliente = st.text_input("", label_visibility="collapsed", key="nom_cli")
        
        st.write("")
        st.markdown('<span style="color: white; font-weight: bold; text-shadow: 1px 1px 2px black; font-size: 16px;">Método de Entrega:</span>', unsafe_allow_html=True)
        metodo_entrega = st.radio("", ["Delivery Moto 🏍️", "Recojo en Local 🏪"], label_visibility="collapsed", key="met_ent")

        direccion_cliente = ""
        if metodo_entrega == "Delivery Moto 🏍️":
            st.write("")
            st.markdown('<span style="color: white; font-weight: bold; text-shadow: 1px 1px 2px black; font-size: 14px;">Dirección de Envío:</span>', unsafe_allow_html=True)
            direccion_cliente = st.text_input("", placeholder="Ej: Av. Perú 123, dpto 402...", label_visibility="collapsed", key="dir_cli")
            
            st.markdown("""
            <div class="alerta-delivery-personalizada">
                📌 <b>NOTA DE DELIVERY:</b> Al finalizar y enviar el mensaje por WhatsApp, por favor <b>compártenos tu ubicación actual</b> en el chat para que el motorizado llegue rápido.<br><br>
                💰 El costo del delivery se calculará y se lo enviaremos inmediatamente después de confirmar su pedido.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alerta-delivery-personalizada" style="border-color: #4CAF50;">
                🏪 <b>RECOJO EN LOCAL:</b> Tu pedido estará listo y empacado para recoger en aproximadamente <b>20 a 30 minutos</b>. ¡Te esperamos!
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown('<span style="color: white; font-weight: bold; text-shadow: 1px 1px 2px black; font-size: 16px;">Método de Pago:</span>', unsafe_allow_html=True)
        metodo_pago = st.radio("", ["Yape 📱", "Efectivo 💵"], label_visibility="collapsed", key="met_pag")

        # Validación y armado del mensaje final de WhatsApp
        if nombre_cliente.strip() and (metodo_entrega == "Recojo en Local 🏪" or direccion_cliente.strip()):
            mensaje_wa = f"🍜 *CHIFA D' BELINDA*\n\n"
            mensaje_wa += f"👤 *Cliente:* {nombre_cliente}\n"
            mensaje_wa += f"🛵 *Entrega:* {metodo_entrega}\n"
            if metodo_entrega == "Delivery Moto 🏍️":
                mensaje_wa += f"📍 *Dirección:* {direccion_cliente.strip()}\n"
            mensaje_wa += f"💳 *Pago:* {metodo_pago}\n"
            mensaje_wa += f"-------------------------\n"
            
            for item in st.session_state.carrito:
                mensaje_wa += f"✅ {item['cant']}x {item['nombre']} - S/. {item['precio'] * item['cant']:.2f}\n"
                if item['cremas'] != "Ninguna":
                    mensaje_wa += f"  • Salsas: {item['cremas']}\n"
                if item['notas'] != "Ninguna":
                    mensaje_wa += f"  • Nota: {item['notas']}\n"
            
            mensaje_wa += f"-------------------------\n"
            mensaje_wa += f"💰 *SUBTOTAL:* S/. {total:.2f}\n"
            if metodo_entrega == "Delivery Moto 🏍️":
                mensaje_wa += f"ℹ️ _El costo de delivery se sumará en breve._"

            link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"
            st.write("")
            st.markdown('<div class="boton-normal-ancho">', unsafe_allow_html=True)
            st.link_button("📲 ENVIAR PEDIDO A WHATSAPP", link_final, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write("")
            st.warning("⚠️ Por favor, ingresa tu nombre completo y dirección (si seleccionaste delivery) para habilitar el envío.")

        st.write("")
        st.markdown('<div class="boton-normal-ancho">', unsafe_allow_html=True)
        if st.button("🧹 Vaciar Todo el Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)