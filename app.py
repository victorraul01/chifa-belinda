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

# LECTURA DEL EXCEL CON CACHÉ
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

# ESTILOS CSS AVANZADOS: CAPAS SUPERPUESTAS (OVERLAYS) PARA MÓVILES
st.markdown("""
<style>
/* PESTAÑAS GLOBALES */
button[data-baseweb="tab"] {
    font-size: 14px !important;
    font-weight: bold !important;
    color: #555555 !important;
    padding: 10px 5px !important;
    flex-grow: 1 !important;
    text-align: center !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #d32f2f !important;
    border-bottom: 3px solid #d32f2f !important;
}

/* CONTENEDOR CONTRA EL DESCUADRE (Mantiene la proporción de la carta física) */
.contenedor-carta-real {
    position: relative !important;
    width: 100% !important;
    max-width: 450px; /* Tamaño estándar de pantalla móvil */
    margin: 0 auto !important;
    overflow: hidden;
}

.imagen-fondo-carta {
    width: 100% !important;
    display: block !important;
    height: auto !important;
}

/* EL ESPACIO ROJO DIGITAL (Capa transparente encima del recuadro rojo de tu foto) */
.capa-overlay-platos {
    position: absolute !important;
    top: 5%;      /* Ajustable para que empiece exactamente donde abre el recuadro rojo */
    right: 4%;    /* Margen derecho interno del marco oriental */
    width: 54%;   /* Ocupa exactamente el ancho de tu espacio rojo derecho */
    height: 90%;  /* Alto máximo para que no se salga de la hoja */
    display: flex !important;
    flex-direction: column !important;
    gap: 4px !important; /* Separación milimétrica entre filas */
    z-index: 10 !important;
}

/* CADA LÍNEA DE PLATO (Súper delgada, fondo invisible o sutil) */
.fila-plato-sobre-foto {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    background: rgba(0, 0, 0, 0.15) !important; /* Sombreado ligero para leer bien sobre el rojo */
    padding: 2px 4px !important;
    border-radius: 3px;
    width: 100% !important;
    box-sizing: border-box !important;
}

/* TEXTOS DELGADOS EN UNA SOLA LÍNEA */
.nombre-plato-encima {
    color: #ffffff !important;
    font-size: 10.5px !important; /* Letras pequeñas para que no hagan doble línea */
    font-weight: bold !important;
    text-align: left !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important; /* Si el nombre es muy largo, pone '...' al final */
    flex-grow: 1 !important;
    margin-left: 5px !important;
}

.precio-plato-encima {
    color: #ffeb3b !important; /* Amarillo brillante para resaltar en el fondo rojo */
    font-size: 11px !important;
    font-weight: bold !important;
    white-space: nowrap !important;
    margin-left: 4px !important;
}

/* BOTÓN MÓVIL ESTILO INLINE (IZQUIERDA) */
.boton-agregar-izquierda {
    background-color: #ffffff !important;
    color: #d32f2f !important;
    border: none !important;
    font-size: 11px !important;
    font-weight: bold !important;
    border-radius: 50% !important; /* Redondito e integrado */
    width: 16px !important;
    height: 16px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    padding: 0 !important;
    box-shadow: 0px 1px 3px rgba(0,0,0,0.3);
}

.detalle-carrito {
    font-size: 12px;
    color: #555555;
    margin-left: 10px;
    display: block;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# INICIALIZACIÓN DE ESTADOS
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "mensaje_exito" not in st.session_state:
    st.session_state.mensaje_exito = None

if st.session_state.mensaje_exito:
    st.toast(st.session_state.mensaje_exito)
    st.session_state.mensaje_exito = None

# MODAL DINÁMICO DE CREMAS Y ADICIONALES
@st.dialog("🛒 Configura tu pedido")
def modal_agregar_con_detalles(nombre_plato, precio_plato, categoria_plato="", es_menu=False):
    st.markdown(f"<h3 style='text-align:center; color:white;'>{nombre_plato}</h3>", unsafe_allow_html=True)
    cantidad = st.number_input("Cantidad:", min_value=1, value=1)
    
    entrada_seleccionada = None
    if es_menu:
        entrada_seleccionada = st.radio("Entrada:", ["🥣 Sopa Wantán", "🥟 Wantán Frito"], horizontal=True)

    st.markdown("**Cremas:**")
    c1, c2 = st.columns(2)
    with c1:
        aji = st.checkbox("Ají")
        mayo = st.checkbox("Mayonesa")
    with c2:
        tamarindo = st.checkbox("Tamarindo")
        ketchup = st.checkbox("Ketchup")
        
    limon = False
    if categoria_plato == "ALITAS ESPECIALES":
        limon = st.checkbox("🍋 Agregar Limón")
        
    notas = st.text_input("Notas adicionales:")
    
    if st.button("Confirmar", use_container_width=True):
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
        st.session_state.mensaje_exito = f"¡{nombre_plato} añadido! 🛒"
        st.rerun()

# INTERFAZ PRINCIPAL
st.markdown("<h2 style='text-align:center; margin-bottom:0;'>🍜 CHIFA D' BELINDA</h2>", unsafe_allow_html=True)

items_carrito = sum(item["cant"] for item in st.session_state.carrito)
tab_carta, tab_menu, tab_pedido = st.tabs([
    "📖 Carta Digital", "📋 Menú Diario", f"🛒 Pedido ({items_carrito})"
])

# FUNCIÓN REVOLUCIONARIA: RENDERIZA EL HTML DONDE LOS PLATOS FLOTAN SOBRE EL RECUADRO ROJO
def generar_pagina_con_platos_superpuestos(nombre_imagen_archivo, lista_categorias, id_pagina_unica):
    # Convertimos la imagen de la carta local a Base64 para que el navegador la pinte directo de fondo
    ruta_img = f"images/{nombre_imagen_archivo}.jpg"
    img_b64 = ""
    if os.path.exists(ruta_img):
        with open(ruta_img, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
            
    df_filtrado = df_productos[df_productos["Category"].isin(lista_categorias)] if not df_productos.empty else pd.DataFrame()
    
    # Construcción del bloque HTML de la carta física con el espacio rojo interactivo
    html_platos = ""
    if not df_filtrado.empty:
        for idx, row in df_filtrado.iterrows():
            id_plato = row['ID']
            nombre = row['Name']
            precio = f"{row['Price']:.2f}"
            
            # Cada fila tiene: El botón "+" (izquierda), Nombre (centro) y Precio (derecha) en 1 sola línea
            html_platos += f"""
            <div class="fila-plato-sobre-foto">
                <button class="boton-agregar-izquierda" onclick="window.parent.postMessage({{type: 'click_plato', id: '{id_plato}'}}, '*')">＋</button>
                <span class="nombre-plato-encima">{nombre}</span>
                <span class="precio-plato-encima">S/.{precio}</span>
            </div>
            """
            
            # Detectamos de manera invisible el click del botón nativo del HTML mediante Streamlit alterno
            if st.button("", key=f"hidden_btn_{id_pagina_unica}_{id_plato}", help=f"Agregar {nombre}", use_container_width=False):
                if row["Category"] in ["BEBIDAS FRÍAS", "BEBIDAS CALIENTES"]:
                    st.session_state.carrito.append({"nombre": nombre, "precio": row["Price"], "cant": 1, "entrada": None, "cremas": [], "nota": ""})
                    st.session_state.mensaje_exito = f"¡{nombre} añadido! 🥤✅"
                    st.rerun()
                else:
                    modal_agregar_con_detalles(nombre, row["Price"], categoria_plato=row["Category"])

    # Renderizado final combinado (Imagen real de fondo + textos flotando a la derecha)
    if img_b64:
        st.markdown(f"""
        <div class="contenedor-carta-real">
            <img class="imagen-fondo-carta" src="data:image/jpeg;base64,{img_b64}">
            <div class="capa-overlay-platos">
                {html_platos}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"Falta archivo: images/{nombre_imagen_archivo}.jpg")

# =========================================================
# 1. PESTAÑA: CARTA DIGITAL (TEXTOS EXACTOS DENTRO DEL RECUADRO ROJO)
# =========================================================
with tab_carta:
    st.info("💡 Haz clic en el símbolo ＋ a la izquierda del nombre del plato para ordenar.")
    
    # PÁGINA 2 COMPLETA: Muestra la foto de la página y mete Combos, Alitas y Broaster dentro del recuadro rojo
    generar_pagina_con_platos_superpuestos("pag2", ["COMBOS", "ALITAS REBOZADAS", "ALITAS ESPECIALES", "POLLO BROASTER"], "p2")
    
    # PÁGINA 3 COMPLETA: Sopas y Chaufas dentro del recuadro rojo de su respectiva foto
    generar_pagina_con_platos_superpuestos("pag3", ["SOPAS", "CHAUFA"], "p3")
    
    # PÁGINA 4 COMPLETA: Aeropuertos, Combinados y Lomos
    generar_pagina_con_platos_superpuestos("pag4", ["AEROPUERTO", "COMBINADOS", "LOMOS SALTADOS"], "p4")
    
    # PÁGINA 5 COMPLETA: Tallarines y Platos Wok
    generar_pagina_con_platos_superpuestos("pag5", ["TALLARINES SALTADOS", "PLATOS SALADOS", "PLATOS DULCE"], "p5")

# =========================================================
# 2. PESTAÑA: MENÚ DIARIO 
# =========================================================
with tab_menu:
    for idx, data in df_menu_diario.iterrows():
        col_btn, col_txt = st.columns([1.5, 8.5])
        with col_btn:
            if st.button("➕", key=f"btn_menu_{idx}"):
                modal_agregar_con_detalles(data["Name"], data["Price"], categoria_plato="MENU DIARIO", es_menu=True)
        with col_txt:
            st.markdown(f"**{data['Name']}** — S/. {data['Price']:.2f}")

# =========================================================
# 3. PESTAÑA: MI PEDIDO / WHATSAPP
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
            st.markdown(f"🔹 **{item['cant']} x {item['nombre']}** — S/. {subtotal:.2f}")
            if item["cremas"]: st.markdown(f"<span class='detalle-carrito'>↳ Cremas: {', '.join(item['cremas'])}</span>", unsafe_allow_html=True)
            if item["nota"]: st.markdown(f"<span class='detalle-carrito'>↳ Nota: {item['nota']}</span>", unsafe_allow_html=True)

        st.divider()
        nombre = st.text_input("Tu nombre completo")
        tipo_entrega = st.radio("Entrega", [" Delivery", " Recojo en Local"])
        pago = st.radio("Método de pago", [" Efectivo", " Yape"])

        # Generador de link de WhatsApp
        texto = f"🍜 *CHIFA D' BELINDA*\nCliente: {nombre}\nEntrega: {tipo_entrega}\nPago: {pago}\nTotal Productos: S/. {total_platos:.2f}"
        link = f"https://wa.me/51923860158?text={urllib.parse.quote(texto)}"
        st.link_button("📲 ENVIAR PEDIDO POR WHATSAPP", link, use_container_width=True)