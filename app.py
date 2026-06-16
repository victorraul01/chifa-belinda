import streamlit as st
import pandas as pd
import urllib.parse
import base64
import os

# 1. CONFIGURACIÓN DE LA PÁGINA (Aprovechamiento total en pantallas de celular)
st.set_page_config(
    page_title="Chifa D' Belinda",
    page_icon="🍜",
    layout="centered"
)

# Función para cargar la imagen de fondo de la página actual (pag2.jpg, pag3.jpg, etc.)
def cargar_imagen_fondo_pagina(numero_pagina):
    nombre_imagen = f"pag{numero_pagina}.jpg"
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

# 2. INICIALIZACIÓN DE ESTADOS DEL CARRITO
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "mensaje_exito" not in st.session_state:
    st.session_state.mensaje_exito = None

# 3. PROCESAR CLICKS DE AGREGAR PLATOS DE FORMA INSTANTÁNEA
query_params = st.query_params
if "add_id" in query_params:
    id_elegido = query_params["add_id"]
    nombre_elegido = query_params.get("add_name", "Plato")
    precio_elegido = float(query_params.get("add_price", 0))
    
    st.session_state.carrito.append({
        "nombre": nombre_elegido,
        "precio": precio_elegido,
        "cant": 1
    })
    st.session_state.mensaje_exito = f"¡{nombre_elegido} agregado! 🛒"
    st.query_params.clear()
    st.rerun()

if st.session_state.mensaje_exito:
    st.toast(st.session_state.mensaje_exito)
    st.session_state.mensaje_exito = None

# 4. CARGA AUTOMÁTICA DESDE TU EXCEL REAL (Mapeo exacto por páginas)
@st.cache_data
def cargar_catalogo_con_paginas():
    nombre_archivo = "Catalogo_Productos.xlsx"
    if os.path.exists(nombre_archivo):
        df = pd.read_excel(nombre_archivo)
    else:
        # Respaldo por si se lee la versión CSV en el servidor
        nombre_csv = "Catalogo_Productos.xlsx - in.csv"
        if os.path.exists(nombre_csv):
            df = pd.read_csv(nombre_csv)
        else:
            st.error(f"❌ No se encontró el archivo '{nombre_archivo}'.")
            return pd.DataFrame()

    df.columns = df.columns.str.strip()
    
    # Definimos las categorías que van en cada página según tu instrucción exacta
    mapeo_paginas = {
        2: ['COMBOS', 'ALITAS REBOZADAS', 'ALITAS ESPECIALES', 'POLLO BROASTER'],
        3: ['SOPAS', 'CHAUFA'],
        4: ['AEROPUERTO', 'COMBINADOS', 'LOMOS SALTADOS'],
        5: ['TALLARINES SALTADOS', 'PLATOS SALADOS', 'PLATOS DULCE', 'TORTILLAS'],
        6: ['ENROLLADOS', 'TAYPA', 'RES', 'LANGOSTINOS', 'PATO', 'CHICHARRONES'],
        7: ['CHANCHO', 'COSTILLAS', 'PORCIONES', 'BEBIDAS CALIENTES', 'BEBIDAS FRÍAS']
    }
    
    # Asignamos el número de página a cada fila basándonos en su columna 'Category'
    def asignar_pagina(cat):
        cat_upper = str(cat).strip().upper()
        for num_pag, categorias in mapeo_paginas.items():
            if cat_upper in categorias:
                return num_pag
        return 2 # Por defecto si hubiera alguna variación

    df['Page'] = df['Category'].apply(asignar_pagina)
    return df

df_carta = cargar_catalogo_con_paginas()

# 5. CSS AVANZADO: FIJAR ELEMENTOS SUPERIORES Y ALINEAR FILAS UNIFICADAS
st.markdown("""
<style>
/* Eliminar márgenes laterales nativos de Streamlit */
.block-container {
    padding-left: 0px !important;
    padding-right: 0px !important;
    padding-top: 0px !important;
    max-width: 100% !important;
}

/* Fijar el selector de navegación por páginas */
div[data-testid="stRadio"] > div {
    padding: 0 10px !important;
}

/* ENCABEZADO SUPERIOR 100% FIJO */
.encabezado-fijo-global {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    background-color: #8B0000 !important;
    z-index: 999999 !important;
    text-align: center !important;
    padding: 12px 0 6px 0 !important;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.6) !important;
    border-bottom: 3px solid #FFEB3B !important;
}

/* Forzar que las pestañas de Streamlit queden fijas justo debajo del título principal */
div[data-testid="stTabs"] > div:first-child {
    position: fixed !important;
    top: 48px !important;
    left: 0 !important;
    width: 100% !important;
    background-color: #8B0000 !important;
    z-index: 999998 !important;
    box-shadow: 0px 3px 6px rgba(0,0,0,0.3) !important;
    padding: 0 5px !important;
}

/* Espacio exacto de compensación para que el catálogo empiece abajo de las pestañas fijas */
.compensar-cabecera-fija {
    margin-top: 105px !important;
}

/* CONTENEDOR PRINCIPAL CON SCROLL VERTICAL INDEPENDIENTE */
.scroller-carta-completa {
    width: 100% !important;
    height: 550px !important; 
    background-size: cover !important;
    background-repeat: no-repeat !important;
    background-position: center center !important;
    background-attachment: local !important;
    overflow-y: auto !important; 
    padding: 10px 12px 40px 12px !important;
    box-sizing: border-box !important;
}

/* RESALTE PARA LOS TÍTULOS DE LAS CATEGORÍAS */
.titulo-categoria-resaltado {
    background: linear-gradient(90deg, #8B0000 0%, rgba(140,7,18,0.95) 100%) !important;
    color: #FFEB3B !important;
    font-size: 13px !important;
    font-weight: bold !important;
    padding: 9px 12px !important;
    border-radius: 6px !important;
    margin-top: 10px !important;
    margin-bottom: 12px !important;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.9) !important;
    border-left: 5px solid #FFEB3B !important;
    width: 100% !important;
    box-sizing: border-box;
}

/* FILA HORIZONTAL DE ANCHO COMPLETO: Botón | Nombre | Precio */
.fila-plato-unificada {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    width: 100% !important;
    background: rgba(0, 0, 0, 0.78) !important; 
    padding: 11px 14px !important;
    margin-bottom: 8px !important;
    border-radius: 8px !important;
    box-sizing: border-box !important;
    border: 1px solid rgba(255,255,255,0.12);
}

.btn-agregar-directo {
    background-color: #FFEB3B !important;
    color: #8B0000 !important;
    text-decoration: none !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border-radius: 50% !important;
    width: 28px !important;
    height: 28px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.5) !important;
    margin-right: 14px !important;
}

.nombre-plato-unificado {
    color: #FFFFFF !important;
    font-size: 12.5px !important;
    font-weight: bold !important;
    line-height: 1.3 !important;
    text-align: left !important;
    margin-right: 8px !important;
    flex-grow: 1 !important; 
}

.precio-plato-unificado {
    color: #FFEB3B !important;
    font-size: 14px !important;
    font-weight: bold !important;
    white-space: nowrap !important;
    flex-shrink: 0 !important;
    text-align: right !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
}
</style>
""", unsafe_allow_html=True)

# 6. ENCABEZADO FIJO DE LA APLICACIÓN
st.markdown("""
<div class="encabezado-fijo-global">
    <span style='color:#FFFFFF; font-size:19px; font-weight:bold; letter-spacing:0.5px;'>🍜 CHIFA D' BELINDA</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="compensar-cabecera-fija"></div>', unsafe_allow_html=True)

items_en_carrito = sum(item["cant"] for item in st.session_state.carrito)

# PESTAÑAS PRINCIPALES NATIVAS
tab_carta, tab_pedido = st.tabs([
    "📖 Nuestra Carta", f"🛒 Mi Pedido ({items_en_carrito})"
])

# =========================================================
# PESTAÑA: NUESTRA CARTA (CON FILTRADO POR PÁGINA)
# =========================================================
with tab_carta:
    if df_carta.empty:
        st.warning("⚠️ Asegúrate de tener tu archivo 'Catalogo_Productos.xlsx' cargado.")
    else:
        # Control horizontal por páginas tal como especificaste
        pag_seleccionada = st.radio(
            "Sección de la carta:",
            options=[2, 3, 4, 5, 6, 7],
            format_func=lambda x: (
                "Pág. 2 (Combos/Alitas/Broaster)" if x==2 else
                "Pág. 3 (Sopas/Chaufa)" if x==3 else
                "Pág. 4 (Aeropuertos/Lomos)" if x==4 else
                "Pág. 5 (Tallarines/Wok/Tortillas)" if x==5 else
                "Pág. 6 (Especialidades/Enrollados)" if x==6 else
                "Pág. 7 (Chancho/Bebidas)"
            ),
            horizontal=True
        )
        
        # Filtramos los platos que corresponden únicamente a esta página
        df_filtrado = df_carta[df_carta["Page"] == pag_seleccionada]
        
        html_items = ""
        categoria_actual = ""
        
        # Construimos las filas de platos correspondientes
        for _, row in df_filtrado.iterrows():
            if str(row['Category']).strip() != categoria_actual:
                categoria_actual = str(row['Category']).strip()
                html_items += f'<div class="titulo-categoria-resaltado">📂 {categoria_actual.upper()}</div>'
                
            p_id = row['ID']
            p_name = row['Name']
            p_price = float(row['Price'])
            
            params = urllib.parse.urlencode({"add_id": p_id, "add_name": p_name, "add_price": p_price})
            
            html_items += f"""
            <div class="fila-plato-unificada">
                <a class="btn-agregar-directo" href="?{params}" target="_self">＋</a>
                <span class="nombre-plato-unificado">{p_name}</span>
                <span class="precio-plato-unificado">S/. {p_price:.2f}</span>
            </div>
            """
            
        # CARGAMOS LA IMAGEN DE FONDO RESPECTIVA A LA PÁGINA (pag2.jpg, pag3.jpg, etc.)
        imagen_b64 = cargar_imagen_fondo_pagina(pag_seleccionada)
        
        if imagen_b64:
            html_carta_completa = f"""
            <div class="scroller-carta-completa" style="background-image: url('data:image/jpeg;base64,{imagen_b64}');">
                {html_items}
            </div>
            """
            st.markdown(html_carta_completa, unsafe_allow_html=True)
        else:
            st.info(f"💡 Mostrando platos. Si deseas el fondo gráfico real de esta sección, guarda tu imagen como 'pag{pag_seleccionada}.jpg'")
            html_carta_sin_foto = f"""
            <div class="scroller-carta-completa" style="background-color: #8C0712;">
                {html_items}
            </div>
            """
            st.markdown(html_carta_sin_foto, unsafe_allow_html=True)

# =========================================================
# PESTAÑA: MI PEDIDO (CARRITO Y ENVÍO A WHATSAPP)
# =========================================================
with tab_pedido:
    st.markdown("<div style='padding: 15px;'>", unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío. ¡Explora el menú y empieza a armar tu orden!")
    else:
        st.subheader("📋 Resumen del Pedido")
        total = 0
        for item in st.session_state.carrito:
            subtotal = item["precio"] * item["cant"]
            total += subtotal
            st.markdown(f"💥 **{item['cant']}x {item['nombre']}** — S/. {subtotal:.2f}")
            
        st.divider()
        nombre_cliente = st.text_input("Ingresa tu Nombre Completo:")
        
        mensaje_wa = f"🍜 *CHIFA D' BELINDA*\n\n👤 *Cliente:* {nombre_cliente}\n-------------------------\n"
        for item in st.session_state.carrito:
            mensaje_wa += f"✅ {item['cant']}x {item['nombre']} - S/. {item['precio'] * item['cant']:.2f}\n"
        mensaje_wa += f"-------------------------\n💰 *TOTAL PEDIDO:* S/. {total:.2f}"
        
        link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"
        st.write("")
        st.link_button("📲 ENVIAR PEDIDO A WHATSAPP", link_final, use_container_width=True)
        
        st.write("")
        if st.button("🧹 Vaciar Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)