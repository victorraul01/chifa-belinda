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

# Función para cargar la imagen de fondo según la página del menú gráfico
def cargar_imagen_fondo_pagina(numero_pagina):
    # Traducir el número de página al nombre de tu archivo físico real
    # Pagina 1 -> pag2.jpg, Pagina 2 -> pag3.jpg, etc.
    mapeo_archivos = {1: "pag2.jpg", 2: "pag3.jpg", 3: "pag4.jpg", 4: "pag5.jpg", 5: "pag6.jpg", 6: "pag7.jpg"}
    nombre_imagen = mapeo_archivos.get(numero_pagina, "pag2.jpg")
    
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

# 2. INICIALIZACIÓN DE ESTADOS GLOBAL DE CARRITO (Persistente y acumulativo)
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# 3. CARGA Y ASIGNACIÓN ESTRICTA DE CATEGORÍAS POR PÁGINA
def cargar_catalogo_con_paginas_corregido():
    nombre_archivo = "Catalogo_Productos.xlsx"
    nombre_csv = "Catalogo_Productos.xlsx - in.csv"
    
    if os.path.exists(nombre_archivo):
        df = pd.read_excel(nombre_archivo)
    elif os.path.exists(nombre_csv):
        df = pd.read_csv(nombre_csv)
    else:
        st.error(f"❌ No se encontró el archivo del catálogo.")
        return pd.DataFrame()

    df.columns = df.columns.str.strip()
    df['Category'] = df['Category'].astype(str).str.strip().str.upper()
    
    # Tu distribución exacta solicitada
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

# 4. VENTANA EMERGENTE INTERACTIVA (MODAL) PARA PERSONALIZAR EL PLATO
@st.dialog("Configura tu Plato 🍜")
def abrir_modal_agregar_plato(id_plato, nombre_plato, precio_plato):
    st.markdown(f"### {nombre_plato}")
    st.markdown(f"**Precio Unitario:** S/. {precio_plato:.2f}")
    st.write("---")
    
    # Selección de cantidad
    cantidad = st.number_input("Cantidad:", min_value=1, max_value=20, value=1, step=1)
    
    # Opciones de cremas
    st.markdown("**Selecciona tus Cremas / Salsas:**")
    col1, col2 = st.columns(2)
    with col1:
        c_aji = st.checkbox("Ají Chi Chon San 🌶️")
        c_mayo = st.checkbox("Mayonesa ⚪")
    with col2:
        c_ketchup = st.checkbox("Ketchup 🍅")
        c_tamarindo = st.checkbox("Salsa Tamarindo 🍯")
        
    # Campo de notas opcional
    st.write("")
    notas = st.text_input("Notas / Observaciones del plato (Opcional):", placeholder="Ej: Sin cebolla, tarta extra...")
    
    st.write("")
    if st.button("🛒 AGREGAR AL PEDIDO", use_container_width=True):
        # Procesar cremas seleccionadas
        cremas_list = []
        if c_aji: cremas_list.append("Ají")
        if c_mayo: cremas_list.append("Mayo")
        if c_ketchup: cremas_list.append("Ketchup")
        if c_tamarindo: cremas_list.append("Tamarindo")
        
        cremas_texto = ", ".join(cremas_list) if cremas_list else "Ninguna"
        
        # Guardar en la lista acumulativa sin borrar lo anterior
        st.session_state.carrito.append({
            "id": id_plato,
            "nombre": nombre_plato,
            "precio": float(precio_plato),
            "cant": int(cantidad),
            "cremas": cremas_texto,
            "notas": notas if notas.strip() != "" else "Ninguna"
        })
        st.toast(f"¡{cantidad}x {nombre_plato} agregado con éxito!")
        st.rerun()

# 5. CSS AVANZADO: FIJAR ENCABEZADO Y CONFIGURAR CONTENEDORES DE ANCHO COMPLETO
st.markdown("""
<style>
.block-container {
    padding-left: 0px !important;
    padding-right: 0px !important;
    padding-top: 0px !important;
    max-width: 100% !important;
}

div[data-testid="stRadio"] > div {
    padding: 0 10px !important;
}

/* ENCABEZADO SUPERIOR FIJO */
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

/* PESTAÑAS FIJAS */
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

.compensar-cabecera-fija {
    margin-top: 105px !important;
}

/* CONTENEDOR CON FONDO DINÁMICO */
.scroller-carta-completa {
    width: 100% !important;
    height: 540px !important; 
    background-size: cover !important;
    background-repeat: no-repeat !important;
    background-position: center center !important;
    background-attachment: local !important;
    overflow-y: auto !important; 
    padding: 10px 12px 40px 12px !important;
    box-sizing: border-box !important;
}

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

.fila-plato-unificada {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    width: 100% !important;
    background: rgba(0, 0, 0, 0.82) !important; 
    padding: 11px 14px !important;
    margin-bottom: 8px !important;
    border-radius: 8px !important;
    box-sizing: border-box !important;
    border: 1px solid rgba(255,255,255,0.12);
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
    font-weight: bold !important; white-space: nowrap !important;
    flex-shrink: 0 !important; text-align: right !important;
    margin-right: 5px;
}
</style>
""", unsafe_allow_html=True)

# 6. ENCABEZADO FIJO DE LA APLICACIÓN
st.markdown('<div class="encabezado-fijo-global"><span style="color:#FFFFFF; font-size:19px; font-weight:bold;">🍜 CHIFA D\' BELINDA</span></div>', unsafe_allow_html=True)
st.markdown('<div class="compensar-cabecera-fija"></div>', unsafe_allow_html=True)

items_en_carrito = sum(item["cant"] for item in st.session_state.carrito)

# PESTAÑAS DE NAVEGACIÓN
tab_carta, tab_pedido = st.tabs([
    "📖 Nuestra Carta", f"🛒 Mi Pedido ({items_en_carrito})"
])

# =========================================================
# PESTAÑA 1: NUESTRA CARTA
# =========================================================
with tab_carta:
    if df_carta.empty:
        st.warning("⚠️ Carga el archivo del catálogo para inicializar los datos.")
    else:
        # Menú de selección corregido con nombres "Página X" tal cual me pediste
        pag_seleccionada = st.radio(
            "Selecciona una Página:",
            options=[1, 2, 3, 4, 5, 6],
            format_func=lambda x: (
                "Página 1 (Combos/Alitas)" if x==1 else
                "Página 2 (Sopas/Chaufas)" if x==2 else
                "Página 3 (Aeropuertos/Lomos)" if x==3 else
                "Página 4 (Tallarines/Woks)" if x==4 else
                "Página 5 (Especialidades)" if x==5 else
                "Página 6 (Chancho/Bebidas)"
            ),
            horizontal=True
        )
        
        # Filtrado estricto por el número de página asignado
        df_filtrado = df_carta[df_carta["Page_Num"] == pag_seleccionada]
        
        # Renderizado del catálogo completo usando botones nativos incrustados de forma limpia
        imagen_b64 = cargar_imagen_fondo_pagina(pag_seleccionada)
        
        # Iniciamos bloque contenedor visual de la carta
        st.write("")
        categoria_actual = ""
        
        # Usamos columnas nativas controladas para simular el formato de lista compacta sobre el fondo
        with st.container():
            for idx, row in df_filtrado.iterrows():
                if str(row['Category']).strip() != categoria_actual:
                    categoria_actual = str(row['Category']).strip()
                    st.markdown(f'<div class="titulo-categoria-resaltado">📂 {categoria_actual}</div>', unsafe_allow_html=True)
                
                # Formato de fila unificada: Botón de suma, Nombre y Precio derecho
                col_btn, col_txt = st.columns([0.15, 0.85])
                with col_btn:
                    # El botón gatilla el pop-up interactivo directamente sin perder el estado del carrito
                    if st.button("＋", key=f"btn_{row['ID']}_{idx}"):
                        abrir_modal_agregar_plato(row['ID'], row['Name'], row['Price'])
                with col_txt:
                    st.markdown(f"""
                    <div class="fila-plato-unificada" style="margin-top:-5px;">
                        <span class="nombre-plato-unificado">{row['Name']}</span>
                        <span class="precio-plato-unificado">S/. {float(row['Price']):.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)

        # Inyección dinámica de fondo usando estilos CSS controlados para que cambie según la página activa
        if imagen_b64:
            st.markdown(f"""
            <style>
            .stMainBlockContainer {{
                background-image: url('data:image/jpeg;base64,{imagen_b64}') !important;
                background-size: cover !important;
                background-position: center center !important;
                background-attachment: fixed !important;
            }}
            </style>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""<style>.stMainBlockContainer { background-color: #8C0712 !important; }</style>""", unsafe_allow_html=True)

# =========================================================
# PESTAÑA 2: MI PEDIDO (ACUMULATIVO)
# =========================================================
with tab_pedido:
    st.markdown("<div style='padding: 10px;'>", unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío. ¡Explora las páginas de la carta y arma tu orden!")
    else:
        st.subheader("📋 Resumen Total del Pedido")
        total = 0
        
        for idx, item in enumerate(st.session_state.carrito):
            subtotal = item["precio"] * item["cant"]
            total += subtotal
            
            # Formato claro mostrando cremas y notas asociadas a cada plato
            st.markdown(f"💥 **{item['cant']}x {item['nombre']}** — S/. {subtotal:.2f}")
            st.markdown(f"<span style='color:#FFEB3B; font-size:12px;'>└ 🧂 Cremas: {item['cremas']} | 📝 Nota: {item['notas']}</span>", unsafe_allow_html=True)
            st.write("")
            
        st.divider()
        nombre_cliente = st.text_input("Ingresa tu Nombre Completo:")
        
        # Estructura del mensaje de WhatsApp incluyendo las especificaciones completas
        mensaje_wa = f"🍜 *CHIFA D' BELINDA*\n\n👤 *Cliente:* {nombre_cliente}\n-------------------------\n"
        for item in st.session_state.carrito:
            mensaje_wa += f"✅ {item['cant']}x {item['nombre']} - S/. {item['precio'] * item['cant']:.2f}\n"
            if item['cremas'] != "Ninguna": mensaje_wa += f"  • Salsas: {item['cremas']}\n"
            if item['notas'] != "Ninguna": mensaje_wa += f"  • Nota: {item['notas']}\n"
        mensaje_wa += f"-------------------------\n💰 *TOTAL DEL PEDIDO:* S/. {total:.2f}"
        
        link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"
        st.write("")
        st.link_button("📲 ENVIAR PEDIDO A WHATSAPP", link_final, use_container_width=True)
        
        st.write("")
        if st.button("🧹 Vaciar Todo el Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)