import streamlit as st
import pandas as pd
import urllib.parse
import os
import base64

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Chifa D' Belinda",
    page_icon="🍜",
    layout="centered"
)

# MANEJO DE HORARIOS
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

# LOGO EN BASE64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    return ""

img_base64 = get_base64_image("Logo.jpeg")

# FUNCIÓN PARA BUSCAR IMÁGENES
def buscar_imagen_plato(id_plato):
    extensiones = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"]
    try:
        id_limpio = str(int(float(id_plato)))
    except:
        id_limpio = str(id_plato).strip()

    for ext in extensiones:
        ruta = f"images/{id_limpio}{ext}"
        if os.path.exists(ruta):
            return ruta
    return None

# ESTILOS CSS REVISADOS
st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    background-image: linear-gradient(
        rgba(255,255,255,0.85),
        rgba(255,255,255,0.85)
    ), url("data:image/jpeg;base64,{img_base64}");
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

h1, h2, h3, h4, h5, h6, p, label, span {{
    color: #111111 !important;
}}

/* PESTAÑAS SUPERIORES */
button[data-baseweb="tab"] {{
    font-size: 13px !important;
    font-weight: bold !important;
    color: #555555 !important;
    border-bottom: 2px solid transparent !important;
    padding: 10px 6px !important;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: #d32f2f !important;
    border-bottom: 3px solid #d32f2f !important;
    background-color: rgba(211, 47, 47, 0.05) !important;
}}

/* ARREGLAR MÓVILES */
@media (max-width: 768px) {{
    div[data-testid="stFormSubmitButton"] + div,
    .element-container:has(.tarjeta-menu-contenido) + .element-container {{
        margin-top: 0px !important;
    }}
    
    div[data-testid="stHorizontalBlock"]:has(.tarjeta-menu-contenido) {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        gap: 8px !important;
    }}
    
    div[data-testid="stHorizontalBlock"]:has(.tarjeta-menu-contenido) > div:nth-child(1) {{
        width: 78% !important;
        min-width: 78% !important;
    }}
    
    div[data-testid="stHorizontalBlock"]:has(.tarjeta-menu-contenido) > div:nth-child(2) {{
        width: 20% !important;
        min-width: 20% !important;
        text-align: right !important;
    }}
}}

/* FILA DE MENÚ */
.tarjeta-menu-contenido {{
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    background: rgba(255, 255, 255, 0.98) !important;
    border-left: 5px solid #d32f2f;
    padding: 14px 16px !important;
    border-radius: 8px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.06);
    width: 100% !important;
    box-sizing: border-box !important;
}}

.texto-plato-nombre {{
    font-weight: bold !important;
    color: #111111 !important;
    font-size: 14.5px !important;
    text-align: left !important;
    padding-right: 8px;
}}

.texto-plato-precio {{
    font-weight: bold !important;
    color: #d32f2f !important;
    font-size: 14.5px !important;
    white-space: nowrap !important;
    text-align: right !important;
}}

/* PLATOS A LA CARTA */
.product-box {{
    background: #ffffff !important;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 6px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.12);
    border: 1px solid #eeeeee;
    text-align: center;
}}

.product-title {{
    font-size: 14px !important;
    font-weight: bold !important;
    color: #111111 !important;
    margin-bottom: 4px;
}}

.product-description {{
    font-size: 11px !important;
    color: #555555 !important;
    margin-bottom: 8px;
    font-style: italic;
    line-height: 1.3;
}}

.product-price {{
    color: #d32f2f !important;
    font-size: 16px !important;
    font-weight: bold !important;
    margin-bottom: 8px;
}}

/* ESTILIZACIÓN DE BOTONES NATIVOS */
div.stButton > button {{
    background-color: #d32f2f !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: bold !important;
    padding: 10px 12px !important;
    font-size: 13.5px !important;
    width: 100% !important;
    white-space: nowrap !important;
    box-shadow: 0px 2px 5px rgba(211, 47, 47, 0.15) !important;
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

/* MODALES DE DETALLE */
div[role="dialog"] {{
    background-color: #1e1e1e !important;
    border: 1px solid #333333;
}}

div[role="dialog"] h2 {{
    color: white !important;
}}

div[role="dialog"] p, div[role="dialog"] label, div[role="dialog"] span {{
    color: #e0e0e0 !important;
}}

/* ARREGLAR COLOR DE TEXTO DENTRO DE LOS CUADROS INFORMATIVOS */
div[data-testid="stNotification"] p, div[data-testid="stNotification"] span {{
    color: #1e4620 !important;
}}

.texto-modal {{
    color: white !important;
    font-size: 18px !important;
}}

.plato-modal {{
    color: #ffeb3b !important;
    font-size: 22px !important;
    font-weight: bold;
    display: block;
}}

.detalle-carrito {{
    font-size: 13px;
    color: #555555;
    margin-left: 15px;
    display: block;
    font-style: italic;
}}

.frase-carta {{
    text-align: center;
    font-style: italic;
    color: #777777;
    margin-bottom: 20px;
    font-size: 15px;
}}
</style>
""", unsafe_allow_html=True)

# MANEJO DEL CARRITO
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# MODAL DE CONFIGURACIÓN
@st.dialog("🛒 Configura tu pedido")
def modal_agregar_con_detalles(nombre_plato, precio_plato, es_menu=False):
    st.markdown(f"""
    <div style='text-align:center;'>
        <span class='texto-modal'>Estás agregando:</span>
        <span class='plato-modal'>{"Menú: " if es_menu else ""}{nombre_plato}</span>
        <span style='color: #b3b3b3; font-size:15px;'>Precio unitario: S/. {precio_plato:.2f}</span>
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

    st.markdown("<p style='font-weight:bold; margin-bottom:2px; color:white !important;'>Selecciona tus cremas:</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        mayo = st.checkbox("Mayonesa")
        aji = st.checkbox("Ají de Pollería")
    with c2:
        ket = st.checkbox("Ketchup")
        rocoto = st.checkbox("Rocoto")
        
    notas = st.text_input("Notas adicionales:", placeholder="Ej: Sin cebollita...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Confirmar y Agregar", key="btn_confirmar_modal"):
        cremas_list = []
        if mayo: cremas_list.append("Mayonesa")
        if ket: cremas_list.append("Ketchup")
        if aji: cremas_list.append("Ají")
        if rocoto: cremas_list.append("Rocoto")
        
        st.session_state.carrito.append({
            "nombre": f"Menú: {nombre_plato}" if es_menu else nombre_plato,
            "precio": precio_plato,
            "cant": cantidad,
            "entrada": entrada_seleccionada,
            "cremas": cremas_list,
            "nota": notas.strip()
        })
        st.toast(f"¡{nombre_plato} agregado! 🛒✅")
        st.rerun()

# ENCABEZADO
st.markdown("<h1 style='text-align:center; margin-bottom: 0px;'>🍜 CHIFA D' BELINDA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-weight: bold; font-size: 14px; color: #d32f2f; margin-top: 0px;'>🕒 Menú Chifa disponible hasta las 04:30 P.M.</p>", unsafe_allow_html=True)

items_carrito = sum(item["cant"] for item in st.session_state.carrito)

# DEFINICIÓN DE PESTAÑAS BASADAS EN LAS PÁGINAS DEL PDF
tab_pag1, tab_pag2, tab_pag3, tab_pag4, tab_pag5, tab_menu, tab_pedido = st.tabs([
    "📄 Pág 1", 
    "📄 Pág 2", 
    "📄 Pág 3", 
    "📄 Pág 4", 
    "📄 Pág 5",
    "📋 Menú Diario", 
    f"🛒 Pedido ({items_carrito})"
])

# FUNCIÓN AUXILIAR PARA COMPONENTES DE LA CARTA
def renderizar_productos_por_categorias(lista_categorias):
    st.markdown("<style>div[data-testid='stHorizontalBlock'] {display: grid !important; grid-template-columns: repeat(2,1fr) !important; gap: 10px;}</style>", unsafe_allow_html=True)
    df_filtrado = df_productos[df_productos["Category"].isin(lista_categorias)] if not df_productos.empty else pd.DataFrame()
    
    if df_filtrado.empty:
        st.warning("No hay productos cargados en esta página.")
    else:
        for i in range(0, len(df_filtrado), 2):
            fila = df_filtrado.iloc[i:i+2]
            cols = st.columns(2)
            for idx, (_, data) in enumerate(fila.iterrows()):
                with cols[idx]:
                    ruta_imagen = buscar_imagen_plato(data['ID'])
                    if ruta_imagen:
                        st.image(ruta_imagen, use_container_width=True)
                    
                    desc_plato = data.get('Description', '') if not pd.isna(data.get('Description', '')) else ""
                    st.markdown(f"""
                    <div class="product-box">
                        <div class="product-title">{data['Name']}</div>
                        <div class="product-description">{desc_plato}</div>
                        <div class="product-price">S/. {data['Price']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("🛒 Agregar", key=f"btn_carta_{data['ID']}"):
                        modal_agregar_con_detalles(data["Name"], data["Price"], es_menu=False)

# --- PÁGINA 1: COMBOS / ALITAS / BROASTER ---
with tab_pag1:
    st.markdown("<p class='frase-carta'>\"DONDE HAY COMIDA HAY FELICIDAD\"</p>", unsafe_allow_html=True)
    renderizar_productos_por_categorias(["COMBOS", "ALITAS REBOZADAS", "ALITAS ESPECIALES", "POLLO BROASTER"])

# --- PÁGINA 2: SOPAS / CHAUFA ---
with tab_pag2:
    st.markdown("<p class='frase-carta'>\"A FALTA DE AMOR ... UN COMBINADO POR FAVOR\"</p>", unsafe_allow_html=True)
    renderizar_productos_por_categorias(["SOPAS", "CHAUFA"])

# --- PÁGINA 3: AEROPUERTO / COMBINADOS / LOMOS ---
with tab_pag3:
    st.markdown("<p class='frase-carta'>\"NO DEJES PARA MAÑANA LO QUE PUEDES COMER HOY\"</p>", unsafe_allow_html=True)
    renderizar_productos_por_categorias(["AEROPUERTO", "COMBINADOS", "LOMOS SALTADOS"])

# --- PÁGINA 4: TALLARINES / PLATOS SALADOS / DULCES ---
with tab_pag4:
    st.markdown("<p class='frase-carta'>\"SI QUIERES SER FELIZ A CHIFA D' BELINDA DEBES VENIR\"</p>", unsafe_allow_html=True)
    renderizar_productos_por_categorias(["TALLARINES SALTADOS", "PLATOS SALADOS", "PLATOS DULCE"])

# --- PÁGINA 5: TORTILLAS / ENROLLADOS / TAYPA / RES / LANGOSTINOS / PATO / CHICHARRONES / CHANCHO / PORCIONES / BEBIDAS ---
with tab_pag5:
    st.markdown("<p class='frase-carta'>\"YO VOY A DONDE SEA SI ES CONTIGO HAY CHIFITA\" <br> \"UN CHIFA SIEMPRE ES UNA BUENA IDEA\"</p>", unsafe_allow_html=True)
    renderizar_productos_por_categorias([
        "TORTILLAS", "ENROLLADOS", "TAYPA", "RES", "LANGOSTINOS", 
        "PATO", "CHICHARRONES", "CHANCHO", "COSTILLAS", "PORCIONES", 
        "BEBIDAS FRÍAS", "BEBIDAS CALIENTES"
    ])

# --- TAB: MENÚ DIARIO COMPLETO ---
with tab_menu:
    st.markdown("<p style='text-align:center; font-style: italic; color: #555555; margin-bottom:15px;'>Todos los menús incluyen refresco y entrada a elección al ordenar.</p>", unsafe_allow_html=True)
    for idx, data in df_menu_diario.iterrows():
        col_izq, col_der = st.columns([4.0, 1.0])
        with col_izq:
            st.markdown(f"""
            <div class="tarjeta-menu-contenido">
                <span class="texto-plato-nombre">{data['Name']}</span>
                <span class="texto-plato-precio">S/. {data['Price']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_der:
            if st.button("Pedir", key=f"btn_menu_lista_{idx}"):
                modal_agregar_con_detalles(data["Name"], data["Price"], es_menu=True)

# --- CONTENIDO DE LA PESTAÑA: PEDIDO (CARRITO) ---
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
            
            # NUEVO CUADRO INFORMATIVO PARA DELIVERY MANUAL
            st.warning("📍 **Nota sobre el Delivery:** El costo de envío **no está sumado en el total actual** de la app. Este será calculado y agregado de manera manual al abrir tu WhatsApp. Por favor, comparte también tu ubicación en tiempo real dentro del chat.")
        
        elif tipo_entrega == "🏪 Recojo en Local":
            st.info("🏪 **Recojo listo:** Tu pedido se empezará a preparar de inmediato. Puedes pasar a recogerlo al local en aproximadamente **20 a 30 minutos**.")

        # PRESENTACIÓN DEL TOTAL EN LA INTERFAZ
        st.markdown(f"### Total platos: S/. {total_platos:.2f}")
        if tipo_entrega == "🛵 Delivery":
            st.markdown("### Total final: S/. {:.2f} *(Monto de delivery pendiente)*".format(total_platos))
        else:
            st.markdown(f"### Total final: S/. {total_platos:.2f}")

        pago = st.radio("Método de pago", ["💵 Efectivo", "📱 Yape"], horizontal=True)

        # SELECCIÓN DE YAPE QUEDA COMPLETAMENTE LIMPIA (SIn QR NI TEXTOS)

        # ARMADO DEL TEXTO DE WHATSAPP
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
        st.link_button("📲 ENVIAR PEDIDO POR WHATSAPP", link)

        if st.button("🧹 Vaciar carrito"):
            st.session_state.carrito = []
            st.rerun()