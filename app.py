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

# Función optimizada para convertir imágenes locales a Base64
def cargar_imagen_base64(ruta_relativa):
    rutas_posibles = [
        os.path.join("images", ruta_relativa),
        os.path.join("app", "static", "images", ruta_relativa),
        ruta_relativa
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

# 3. CAPTURAR CLICKS PARA AGREGAR PLATOS
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
    st.session_state.mensaje_exito = f"¡{nombre_elegido} agregado! 🛒✅"
    st.query_params.clear()
    st.rerun()

if st.session_state.mensaje_exito:
    st.toast(st.session_state.mensaje_exito)
    st.session_state.mensaje_exito = None

# 4. BASE DE DATOS ACTUALIZADA SEGÚN TU CARTA REAL
def obtener_carta_completa_pdf():
    # PÁGINA 2: COMBOS Y ALITAS HASTA POLLO BROASTER
    p2 = pd.DataFrame({
        "Name": [
            "COMBO 1 (Chi Jau Kay + Pollo)", "COMBO 2 (Tipa Kay + Pollo)", 
            "COMBO 3 (Enrollado + Pollo)", "COMBO 4 (Alitas + Chaufa/Papas)",
            "Alitas Rebozadas 6 Pzs", "Alitas BBQ", "Alitas Bravas", 
            "Pollo Broaster 1/4", "Pollo Broaster 1/8"
        ],
        "Price": [37.00, 37.00, 37.00, 35.00, 25.00, 22.00, 22.00, 18.00, 14.00],
        "Page": 2
    })
    
    # PÁGINA 3: SOPAS HASTA CHAUFA
    p3 = pd.DataFrame({
        "Name": [
            "Sopa Wantán Especial", "Sopa Fuchifú", "Sopa Wantán Simple",
            "Chaufa de Pollo", "Chaufa de Chancho", "Chaufa de Res", "Chaufa Especial"
        ],
        "Price": [16.00, 16.00, 10.00, 14.00, 18.00, 18.00, 22.00],
        "Page": 3
    })
    
    # PÁGINA 4: AEROPUERTOS, COMBINADOS Y LOMOS SALTADOS
    p4 = pd.DataFrame({
        "Name": [
            "Aeropuerto de Pollo", "Aeropuerto Especial",
            "Combinado de Pollo", "Combinado Especial",
            "Lomo Saltado de Pollo", "Lomo Saltado de Res"
        ],
        "Price": [16.00, 22.00, 16.00, 22.00, 17.00, 20.00],
        "Page": 4
    })
    
    # PÁGINA 5: TALLARINES, PLATOS SALADOS, DULCES Y TORTILLAS
    p5 = pd.DataFrame({
        "Name": [
            "Tallarín Saltado de Pollo", "Tallarín Especial",
            "Pollo con Verduras (Salado)", "Chi Jau Kay (Salado)", 
            "Tipa Kay (Dulce)", "Pollo con Piña (Dulce)", "Tortilla de Pollo"
        ],
        "Price": [16.00, 22.00, 18.00, 20.00, 20.00, 20.00, 15.00],
        "Page": 5
    })

    # PÁGINA 6: ENROLLADOS, TAYPA, RES, LANGOSTINOS, PATO, CHICHARRONES
    p6 = pd.DataFrame({
        "Name": [
            "Enrollado de Pollo", "Taypa Especial", "Res con Verduras",
            "Langostinos al Tausi", "Pato al Horno", "Chicharrón de Pollo"
        ],
        "Price": [22.00, 26.00, 22.00, 25.00, 28.00, 18.00],
        "Page": 6
    })

    # PÁGINA 7: CHANCHO, COSTILLAS, PORCIONES, BEBIDAS CALIENTES Y FRÍAS
    p7 = pd.DataFrame({
        "Name": [
            "Chancho asado con Tamarindo", "Costillas Agridulces", "Porción Wantán Frito",
            "Té de Jengibre Kion (Caliente)", "Gaseosa 1L (Fría)", "Chicha Jarrón"
        ],
        "Price": [22.00, 24.00, 10.00, 4.00, 10.00, 12.00],
        "Page": 7
    })
    
    df = pd.concat([p2, p3, p4, p5, p6, p7], ignore_index=True)
    df["ID"] = [f"P{i+1}" for i in df.index]
    return df

df_carta = obtener_carta_completa_pdf()

df_menu_diario = pd.DataFrame({
    "Name": ["Chaufa de Pollo", "Alita Rebozada", "1/8 Broaster", "Aeropuerto de Pollo"],
    "Price": [14.00, 15.00, 14.00, 17.00]
})

# 5. CSS AVANZADO PROFESIONAL: IMAGEN FIJA + CONTENEDOR DE PLATOS SCROLLABLE
st.markdown("""
<style>
.block-container {
    padding-left: 6px !important;
    padding-right: 6px !important;
    padding-top: 10px !important;
}

/* Estructura Split tipo Libro */
.tarjeta-split-container {
    display: flex !important;
    flex-direction: row !important;
    width: 100% !important;
    height: 480px !important; /* Altura fija para controlar el scroll del lado derecho */
    background-color: #8C0712 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.5) !important;
    margin-bottom: 15px !important;
}

/* Columna Izquierda: Completamente fija con la imagen de fondo */
.columna-carta-fija {
    width: 45% !important;
    height: 100% !important;
    background-size: cover !important;
    background-repeat: no-repeat !important;
    background-position: center center !important;
    flex-shrink: 0 !important;
    border-right: 2px solid #70050e !important;
}

/* Columna Derecha: Contenedor con Scroll independiente para deslizar los platos */
.columna-platos-scroll {
    width: 55% !important;
    height: 100% !important;
    padding: 12px 6px !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 8px !important;
    box-sizing: border-box !important;
    overflow-y: auto !important; /* Habilita el desplazamiento vertical en esta lista */
    background-color: #990b16 !important;
}

/* Diseño elegante de las filas de los platos */
.fila-plato-bloque {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    width: 100% !important;
    background: rgba(0, 0, 0, 0.35) !important;
    padding: 8px 6px !important;
    border-radius: 6px !important;
    box-sizing: border-box;
    border: 1px solid rgba(255,255,255,0.05);
}

.btn-mas-flotante {
    background-color: #FFFFFF !important;
    color: #8B0000 !important;
    text-decoration: none !important;
    font-size: 13px !important;
    font-weight: bold !important;
    border-radius: 50% !important;
    width: 22px !important;
    height: 22px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.4) !important;
}

.texto-menu-flotante {
    color: #FFFFFF !important;
    font-size: 10.5px !important;
    font-weight: bold !important;
    line-height: 1.2 !important;
    margin-left: 6px !important;
    margin-right: auto !important;
    text-align: left !important;
    text-shadow: 1px 1px 1px rgba(0,0,0,0.5);
}

.precio-menu-flotante {
    color: #FFEB3B !important;
    font-size: 11.5px !important;
    font-weight: bold !important;
    white-space: nowrap !important;
    flex-shrink: 0 !important;
    margin-left: 4px !important;
    text-shadow: 1px 1px 1px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# ENCABEZADO PRINCIPAL
st.markdown("<h2 style='text-align:center; color:#8B0000; margin-bottom:0; font-size:24px;'>🍜 CHIFA D' BELINDA</h2>", unsafe_allow_html=True)

items_en_carrito = sum(item["cant"] for item in st.session_state.carrito)

# PESTAÑAS PRINCIPALES
tab_carta, tab_menu, tab_pedido = st.tabs([
    "📖 Nuestra Carta", "📋 Menú Diario", f"🛒 Mi Pedido ({items_en_carrito})"
])

# =========================================================
# 1. PESTAÑA: NUESTRA CARTA (CON SELECTOR DE PÁGINAS)
# =========================================================
with tab_carta:
    pag_seleccionada = st.radio(
        "📖 Selecciona una página de la carta:",
        options=[2, 3, 4, 5, 6, 7],
        format_func=lambda x: f"Pág. {x} " + ("(Combos)" if x==2 else "(Chaufas)" if x==3 else "(Lomos)" if x==4 else "(Wok)" if x==5 else "(Especiales)" if x==6 else "(Bebidas/Extras)"),
        horizontal=True
    )
    
    # Construcción de la lista de platos de la página activa
    html_filas = ""
    df_filtrado = df_carta[df_carta["Page"] == pag_seleccionada]
    
    for _, row in df_filtrado.iterrows():
        p_id = row['ID']
        p_name = row['Name']
        p_price = row['Price']
        
        params = urllib.parse.urlencode({"add_id": p_id, "add_name": p_name, "add_price": p_price})
        html_filas += f"""
        <div class="fila-plato-bloque">
            <a class="btn-mas-flotante" href="?{params}" target="_self">＋</a>
            <span class="texto-menu-flotante">{p_name}</span>
            <span class="precio-menu-flotante">S/. {p_price:.2f}</span>
        </div>
        """
        
    # Intentar cargar la imagen correspondiente en Base64 para inyección directa e infalible
    nombre_imagen = f"pag{pag_seleccionada}.jpg"
    imagen_b64 = cargar_imagen_base64(nombre_imagen)
    
    if imagen_b64:
        # Renderizado Split perfecto: Izquierda fija en CSS por Base64, Derecha con scroll interactivo
        html_carta_completa = f"""
        <div class="tarjeta-split-container">
            <div class="columna-carta-fija" style="background-image: url('data:image/jpeg;base64,{imagen_b64}');"></div>
            <div class="columna-platos-scroll">
                {html_filas}
            </div>
        </div>
        """
        st.markdown(html_carta_completa, unsafe_allow_html=True)
    else:
        # Respaldo visual estilizado por si la imagen aún no está cargada en el repositorio
        st.info(f"💡 Cargando lista de platos. Asegúrate de añadir '{nombre_imagen}' en tu carpeta 'images' de GitHub.")
        html_carta_sin_foto = f"""
        <div class="tarjeta-split-container">
            <div class="columna-carta-fija" style="background-color: #70050e; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; padding: 10px; text-align: center;">📖 Fondo Pág. {pag_seleccionada}</div>
            <div class="columna-platos-scroll" style="width: 55% !important;">
                {html_filas}
            </div>
        </div>
        """
        st.markdown(html_carta_sin_foto, unsafe_allow_html=True)

# =========================================================
# 2. PESTAÑA: MENÚ DIARIO
# =========================================================
with tab_menu:
    st.write("### 📋 Menú Especial del Día")
    for idx, row in df_menu_diario.iterrows():
        params_menu = urllib.parse.urlencode({"add_id": f"M{idx}", "add_name": f"Menú: {row['Name']}", "add_price": row['Price']})
        st.markdown(f"""
        <div style="background-color:#8B0000; padding:10px; margin-bottom:6px; border-radius:6px; display:flex; align-items:center;">
            <a class="btn-mas-flotante" href="?{params_menu}" target="_self">＋</a>
            <span style="color:white; font-size:13px; font-weight:bold; margin-left:10px; flex-grow:1;">{row['Name']}</span>
            <span style="color:#FFEB3B; font-size:13px; font-weight:bold;">S/. {row['Price']:.2f}</span>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# 3. PESTAÑA: MI PEDIDO
# =========================================================
with tab_pedido:
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío. ¡Explora las páginas de la carta y añade tus platos favoritos!")
    else:
        st.subheader("📋 Resumen del Pedido")
        total = 0
        for item in st.session_state.carrito:
            subtotal = item["precio"] * item["cant"]
            total += subtotal
            st.markdown(f"💥 **{item['cant']}x {item['nombre']}** — S/. {subtotal:.2f}")
            
        st.divider()
        nombre_cliente = st.text_input("Tu nombre completo:")
        
        mensaje_wa = f"🍜 *CHIFA D' BELINDA*\n\n👤 *Cliente:* {nombre_cliente}\n-------------------------\n"
        for item in st.session_state.carrito:
            mensaje_wa += f"✅ {item['cant']}x {item['nombre']} - S/. {item['precio'] * item['cant']:.2f}\n"
        mensaje_wa += f"-------------------------\n💰 *TOTAL PRODUCTOS:* S/. {total:.2f}"
        
        link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"
        st.link_button("📲 ENVIAR PEDIDO A WHATSAPP", link_final, use_container_width=True)
        
        if st.button("🧹 Limpiar Todo", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()