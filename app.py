import streamlit as st
import pandas as pd
import urllib.parse
import os
import base64

# CONFIGURACIÓN DE LA PÁGINA (Optimizada para móviles)
st.set_page_config(
    page_title="Chifa D' Belinda",
    page_icon="🍜",
    layout="centered"
)

# MANEJO DE HORARIOS Y DISPONIBILIDAD
restaurante_abierto = True  
menu_disponible = True      

# LECTURA DEL EXCEL CON CACHÉ INTELIGENTE
@st.cache_data(ttl=300)
def cargar_productos():
    if os.path.exists("Catalogo_Productos.xlsx"):
        return pd.read_excel("Catalogo_Productos.xlsx")
    return pd.DataFrame(columns=["ID", "Name", "Price", "Category", "Description"])

df_productos = cargar_productos()

# BASE DE DATOS DEL MENÚ DIARIO
def obtener_menu_diario_real():
    datos_menu = {
        "Name": [
            "Chaufa de Pollo", "Alita Rebozada", "1/8 Broaster",
            "Aeropuerto de Pollo", "Combinado de Pollo", "Pollo con Verdura",
            "Tallarín Saltado de Pollo", "Pollo con Tamarindo", "Alita con Tamarindo",
            "Lomo Saltado de Pollo", "Alitas (4 Pzs)", "Tortilla de Verdura",
            "Alitas con Piña", "Pollo con Piña", "Chaufa de Chancho",
            "Chaufa de Res", "Chaufa de Molleja", "Chicharrón de Pollo",
            "Chi Jau Kay", "Kam Lu Wantán", "Enrollado de Pollo",
            "Tipa Kay", "Tallarín de Res", "Combinado de Res",
            "Chancho con Piña", "Chancho con Tamarindo", "¼ Broaster"
        ],
        "Price": [
            14.00, 15.00, 14.00, 17.00, 17.00, 17.00, 17.00, 17.00, 17.00,
            17.00, 18.00, 19.00, 18.00, 19.00, 20.00, 20.00, 20.00, 20.00,
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 22.00
        ]
    }
    return pd.DataFrame(datos_menu)

df_menu_diario = obtener_menu_diario_real()

# LOGO EN BASE64 PARA EL FONDO GENERAL
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    return ""

img_base64 = get_base64_image("Logo.jpeg")

# ESTILOS CSS REVISADOS Y COMPATIBLES CON IPHONE (SAFARI/iOS)
st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    background-image: linear-gradient(
        rgba(255,255,255,0.88),
        rgba(255,255,255,0.88)
    ), url("data:image/jpeg;base64,{img_base64}");
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

h1, h2, h3, h4, h5, h6, p, label, span {{
    color: #111111 !important;
}}

/* MENU PRINCIPAL ESTÁTICO (Las 3 pestañas globales) */
button[data-baseweb="tab"] {{
    font-size: 15px !important;
    font-weight: bold !important;
    color: #555555 !important;
    border-bottom: 2px solid transparent !important;
    padding: 12px 10px !important;
    flex-grow: 1 !important;
    text-align: center !important;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: #d32f2f !important;
    border-bottom: 3px solid #d32f2f !important;
    background-color: rgba(211, 47, 47, 0.05) !important;
}}

/* FILA DE CONTENIDO DE PLATOS - Flexible para móviles */
.tarjeta-menu-contenido {{
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    background: rgba(255, 255, 255, 0.98) !important;
    border-left: 5px solid #d32f2f;
    padding: 10px 14px !important;
    border-radius: 6px;
    box-shadow: 0px 2px 4px rgba(0,0,0,0.04);
    width: 100% !important;
    box-sizing: border-box !important;
    margin-bottom: 4px;
}}

.texto-plato-nombre {{
    font-weight: bold !important;
    color: #111111 !important;
    font-size: 14px !important;
    text-align: left !important;
}}

.texto-plato-precio {{
    font-weight: bold !important;
    color: #d32f2f !important;
    font-size: 14px !important;
    white-space: nowrap !important;
    text-align: right;
    margin-left: auto;
    padding-right: 15px;
}}

/* BOTONES NATIVOS DE AGREGAR */
div.stButton > button {{
    background-color: #d32f2f !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: bold !important;
    padding: 6px 10px !important;
    font-size: 12px !important;
    width: 100% !important;
}}

/* BOTÓN DE ENVIAR WHATSAPP */
div[data-testid="stLinkButton"] a {{
    background-color: #25D366 !important;
    color: white !important;
    font-weight: bold !important;
    font-size: 16px !important;
    border-radius: 8px !important;
    padding: 12px !important;
    text-align: center !important;
    text-decoration: none !important;
    display: inline-block !important;
    width: 100% !important;
    box-shadow: 0px 4px 12px rgba(37, 211, 102, 0.4) !important;
}}

div[data-testid="stLinkButton"] a p, 
div[data-testid="stLinkButton"] a span {{
    color: white !important;
    font-weight: bold !important;
}}

.detalle-carrito {{
    font-size: 13px;
    color: #555555;
    margin-left: 15px;
    display: block;
    font-style: italic;
}}

div[data-testid="stHorizontalBlock"] {{
    align-items: center !important;
    margin-bottom: 2px !important;
}}
</style>
""", unsafe_allow_html=True)

# INICIALIZACIÓN DE ESTADOS
if "carrito" not in st.session_state:
    st.session_state.carrito = []

if "num_pagina" not in st.session_state:
    st.session_state.num_pagina = 2

if "mensaje_exito" not in st.session_state:
    st.session_state.mensaje_exito = None

# SISTEMA ROBUSTO DE TOASTS ANTES DEL LOGUEO DE PÁGINA
if st.session_state.mensaje_exito:
    st.toast(st.session_state.mensaje_exito)
    st.session_state.mensaje_exito = None

# MODAL DINÁMICO DE CONFIGURACIÓN
@st.dialog("🛒 Configura tu pedido")
def modal_agregar_con_detalles(nombre_plato, precio_plato, categoria_plato="", es_menu=False):
    st.markdown(f"""
    <div style='text-align:center;'>
        <span style='color: white; font-size: 17px;'>Estás agregando:</span>
        <span style='color: #ffeb3b; font-size: 21px; font-weight: bold; display: block;'>{"Menú: " if es_menu else ""}{nombre_plato}</span>
        <span style='color: #b3b3b3; font-size:14px;'>Precio unitario: S/. {precio_plato:.2f}</span>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    cantidad = st.number_input("Cantidad a ordenar:", min_value=1, value=1, key="modal_cant")
    
    entrada_seleccionada = None
    if es_menu:
        st.markdown("<p style='font-weight:bold; margin-bottom:2px; color:white !important;'>Selecciona tu entrada (Incluida):</p>", unsafe_allow_html=True)
        entrada_seleccionada = st.radio(
            "",
            ["🥣 Sopa Wantán", "🥟 Wantán Frito"],
            index=0,
            horizontal=True,
            key="modal_entrada"
        )
        st.markdown("<br>", unsafe_allow_html=True)

    # Lógica de cremas filtrada según tus indicaciones
    st.markdown("<p style='font-weight:bold; margin-bottom:2px; color:white !important;'>Selecciona tus cremas:</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        aji = st.checkbox("Ají")
        mayo = st.checkbox("Mayonesa")
    with c2:
        tamarindo = st.checkbox("Tamarindo")
        ketchup = st.checkbox("Ketchup")
        
    # Condición especial: Solo si es de la categoría de Alitas Especiales se habilita el Limón
    limon = False
    if categoria_plato == "ALITAS ESPECIALES":
        st.markdown("<p style='font-weight:bold; margin-bottom:2px; color:white !important;'>Opciones de Alitas:</p>", unsafe_allow_html=True)
        limon = st.checkbox("🍋 Agregar Limón")
        
    notas = st.text_input("Notas adicionales:", placeholder="Ej: Sin cebollita...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Confirmar y Agregar", key="btn_confirmar_modal", use_container_width=True):
        cremas_list = []
        if aji: cremas_list.append("Ají")
        if mayo: cremas_list.append("Mayonesa")
        if tamarindo: cremas_list.append("Tamarindo")
        if ketchup: cremas_list.append("Ketchup")
        if limon: cremas_list.append("Limón")
        
        st.session_state.carrito.append({
            "nombre": f"Menú: {nombre_plato}" if es_menu else nombre_plato,
            "precio": precio_plato,
            "cant": cantidad,
            "entrada": entrada_seleccionada,
            "cremas": cremas_list,
            "nota": notas.strip()
        })
        st.session_state.mensaje_exito = f"¡{nombre_plato} añadido al carrito! 🛒✅"
        st.rerun()

# ENCABEZADO
st.markdown("<h1 style='text-align:center; margin-bottom: 0px;'>🍜 CHIFA D' BELINDA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-weight: bold; font-size: 14px; color: #d32f2f; margin-top: 0px;'>🕒 Pedidos rápidos directos a nuestro WhatsApp</p>", unsafe_allow_html=True)

items_carrito = sum(item["cant"] for item in st.session_state.carrito)

# --- LAS 3 PESTAÑAS PRINCIPALES TOTALMENTE ESTÁTICAS ---
tab_carta, tab_menu, tab_pedido = st.tabs([
    "📖 Platos a la Carta", "📋 Menú Diario", f"🛒 Mi Pedido ({items_carrito})"
])

# FUNCIÓN AUXILIAR PARA MOSTRAR LA HOJA E INTERACTUAR
def renderizar_hoja_carta(nombre_imagen, lista_categorias):
    ruta_jpg = f"images/{nombre_imagen}.jpg"
    if os.path.exists(ruta_jpg):
        st.image(ruta_jpg, use_container_width=True)
    else:
        st.info(f"📸 Vista de la carta física del PDF ({nombre_imagen}.jpg)")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    df_filtrado = df_productos[df_productos["Category"].isin(lista_categorias)] if not df_productos.empty else pd.DataFrame()
    if df_filtrado.empty:
        st.warning("No hay productos cargados para esta página en el Excel.")
    else:
        for idx, data in df_filtrado.iterrows():
            col_izq, col_der = st.columns([4.2, 0.8])
            with col_izq:
                st.markdown(f"""
                <div class="tarjeta-menu-contenido">
                    <span class="texto-plato-nombre">{data['Name']}</span>
                    <span class="texto-plato-precio">S/. {data['Price']:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
            with col_der:
                if st.button("➕", key=f"btn_lista_{data['ID']}"):
                    # REGLA EXCEPCIONAL PARA BEBIDAS: Agregar directo sin abrir modal de cremas
                    if data["Category"] in ["BEBIDAS FRÍAS", "BEBIDAS CALIENTES"]:
                        st.session_state.carrito.append({
                            "nombre": data["Name"],
                            "precio": data["Price"],
                            "cant": 1,
                            "entrada": None,
                            "cremas": [],
                            "nota": ""
                        })
                        st.session_state.mensaje_exito = f"¡{data['Name']} añadido! 🥤✅"
                        st.rerun()
                    else:
                        modal_agregar_con_detalles(data["Name"], data["Price"], categoria_plato=data["Category"], es_menu=False)

# =========================================================
# 1. PESTAÑA: PLATOS A LA CARTA (CON CAMBIO DE HOJA TIPO PDF)
# =========================================================
with tab_carta:
    st.markdown(f"<h4 style='text-align:center; color:#d32f2f;'>📖 Viendo Página {st.session_state.num_pagina} de 7</h4>", unsafe_allow_html=True)
    
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("◀ Hoja Anterior", disabled=(st.session_state.num_pagina == 2), use_container_width=True):
            st.session_state.num_pagina -= 1
            st.rerun()
    with col_next:
        if st.button("Hoja Siguiente ▶", disabled=(st.session_state.num_pagina == 7), use_container_width=True):
            st.session_state.num_pagina += 1
            st.rerun()
            
    st.divider()

    if st.session_state.num_pagina == 2:
        renderizar_hoja_carta("pag2", ["COMBOS", "ALITAS REBOZADAS", "ALITAS ESPECIALES", "POLLO BROASTER"])
    elif st.session_state.num_pagina == 3:
        renderizar_hoja_carta("pag3", ["SOPAS", "CHAUFA"])
    elif st.session_state.num_pagina == 4:
        renderizar_hoja_carta("pag4", ["AEROPUERTO", "COMBINADOS", "LOMOS SALTADOS"])
    elif st.session_state.num_pagina == 5:
        renderizar_hoja_carta("pag5", ["TALLARINES SALTADOS", "PLATOS SALADOS", "PLATOS DULCE"])
    elif st.session_state.num_pagina == 6:
        renderizar_hoja_carta("pag6", ["TORTILLAS", "ENROLLADOS", "TAYPA", "RES", "LANGOSTINOS"])
    elif st.session_state.num_pagina == 7:
        renderizar_hoja_carta("pag7", ["PATO", "CHICHARRONES", "CHANCHO", "COSTILLAS", "PORCIONES", "BEBIDAS FRÍAS", "BEBIDAS CALIENTES"])

    st.divider()
    col_prev2, col_next2 = st.columns(2)
    with col_prev2:
        if st.button("◀ Anterior Hoja", key="prev_inf", disabled=(st.session_state.num_pagina == 2), use_container_width=True):
            st.session_state.num_pagina -= 1
            st.rerun()
    with col_next2:
        if st.button("Siguiente Hoja ▶", key="next_inf", disabled=(st.session_state.num_pagina == 7), use_container_width=True):
            st.session_state.num_pagina += 1
            st.rerun()

# =========================================================
# 2. PESTAÑA: MENÚ DIARIO (ESTÁTICA)
# =========================================================
with tab_menu:
    st.markdown("<p style='text-align:center; font-style: italic; color: #555555; margin-bottom:15px;'>Todos los menús incluyen refresco y entrada a elección al ordenar.</p>", unsafe_allow_html=True)
    for idx, data in df_menu_diario.iterrows():
        col_izq, col_der = st.columns([4.2, 0.8])
        with col_izq:
            st.markdown(f"""
            <div class="tarjeta-menu-contenido">
                <span class="texto-plato-nombre">{data['Name']}</span>
                <span class="texto-plato-precio">S/. {data['Price']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_der:
            if st.button("➕", key=f"btn_menu_lista_{idx}"):
                # El menú diario abre el modal configurado como Menú para pedir entradas y cremas estándar
                modal_agregar_con_detalles(data["Name"], data["Price"], categoria_plato="MENU DIARIO", es_menu=True)

# =========================================================
# 3. PESTAÑA: MI PEDIDO / CARRITO COMPLETO (ESTÁTICA)
# =========================================================
with tab_pedido:
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío")
    else:
        st.subheader("📋 Resumen de tu pedido")
        total_platos = 0

        for item in st.session_state.carrito:
            subtotal = item["precio"] * item["cant"]
            total_platos += subtotal
            st.markdown(f"🔹 **{item['cant']}   {item['nombre']}** — S/. {subtotal:.2f}")
            
            detalles = []
            if "entrada" in item and item["entrada"]:
                detalles.append(f"Entrada: {item['entrada']}")
            if item["cremas"]:
                detalles.append(f"Cremas: {', '.join(item['cremas'])}")
            if item["nota"]:
                detalles.append(f"Nota: {item['nota']}")
                
            if detalles:
                for det in detalles:
                    st.markdown(f"<span class='detalle-carrito'>↳ {det}</span>", unsafe_allow_html=True)

        st.divider()

        nombre = st.text_input("Tu nombre completo")
        tipo_entrega = st.radio("Entrega", ["🛵 Delivery", "🏪 Recojo en Local"], horizontal=True)

        direccion = ""
        if tipo_entrega == "🛵 Delivery":
            direccion = st.text_input("Dirección exacta")
            st.warning("📍 *Nota sobre el Delivery:* El costo de envío no está sumado en el total actual de la pantalla. Se calculará y agregará manualmente al abrir tu WhatsApp. Por favor, comparte tu ubicación en tiempo real en el chat.")
        elif tipo_entrega == "🏪 Recojo en Local":
            st.info("🏪 **Recojo listo:** Tu pedido se empezará a preparar de inmediato. Puedes pasar a recogerlo en aproximadamente **20 a 30 minutos**.")

        st.markdown(f"### Total platos: S/. {total_platos:.2f}")
        if tipo_entrega == "🛵 Delivery":
            st.markdown("### Total final: S/. {:.2f} *(Monto de delivery pendiente)*".format(total_platos))
        else:
            st.markdown(f"### Total final: S/. {total_platos:.2f}")

        pago = st.radio("Método de pago", ["💵 Efectivo", "📱 Yape"], horizontal=True)

        # ARMADO EXACTO DEL TEXTO DE WHATSAPP
        lineas = [
            "🍜 *CHIFA D' BELINDA*",
            ""
        ]
        if nombre.strip():
            lineas.append(f"👤 Cliente: {nombre.strip()}")
        lineas.append(f"🚚 Entrega: {tipo_entrega}")

        if tipo_entrega == "🛵 Delivery":
            if direccion.strip():
                lineas.append(f"🏠 Dirección ingresada: {direccion.strip()}")
            lineas.append("⚠️ *Nota:* Queda pendiente la suma manual del costo de delivery al total.")
            lineas.append("📌 *¡Enseguida te comparto mi ubicación en tiempo real por aquí!* 🌍")
        elif tipo_entrega == "🏪 Recojo en Local":
            lineas.append("🕒 *Pasaré a recogerlo en 20-30 minutos*")

        lineas.append(f"💳 Método de Pago: {pago.upper()}")
        lineas.append("-------------------------")

        for item in st.session_state.carrito:
            subtotal_item = item['precio'] * item['cant']
            lineas.append(f"✅ {item['cant']}  {item['nombre']} — S/. {subtotal_item:.2f}")
            if "entrada" in item and item["entrada"]:
                lineas.append(f"       ↳ {item['entrada']}")
            if item["cremas"]:
                lineas.append(f"       ↳ Cremas: {', '.join(item['cremas'])}")
            if item["nota"]:
                lineas.append(f"       ↳ Nota: {item['nota']}")

        lineas.append("-------------------------")
        lineas.append(f"TOTAL PRODUCTOS: S/. {total_platos:.2f}")
        if tipo_entrega == "🛵 Delivery":
            lineas.append("DELIVERY: ¡Pendiente de suma manual por WhatsApp!")
            lineas.append(f"TOTAL GENERAL PREVIO: S/. {total_platos:.2f}")
        else:
            lineas.append(f"TOTAL FINAL: S/. {total_platos:.2f}")

        texto = "\n".join(lineas)
        link = f"https://wa.me/51923860158?text={urllib.parse.quote(texto)}"
        st.link_button("📲 ENVIAR PEDIDO POR WHATSAPP", link, use_container_width=True)

        if st.button("🧹 Vaciar carrito", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()