import streamlit as st
import pandas as pd
import urllib.parse
import os

# CONFIGURACIÓN DE LA PÁGINA (Optimizada estrictamente para celulares)
st.set_page_config(
    page_title="Chifa D' Belinda",
    page_icon="🍜",
    layout="centered"
)

# INICIALIZACIÓN DE ESTADOS DEL CARRITO
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "mensaje_exito" not in st.session_state:
    st.session_state.mensaje_exito = None

# CAPTURAR CLICKS DESDE LOS ENLACES HTML EN LA URL
query_params = st.query_params
if "add_id" in query_params:
    id_elegido = query_params["add_id"]
    nombre_elegido = query_params.get("add_name", "Plato")
    precio_elegido = float(query_params.get("add_price", 0))
    
    st.session_state.carrito.append({
        "nombre": nombre_elegido,
        "precio": precio_elegido,
        "cant": 1,
        "nota": ""
    })
    st.session_state.mensaje_exito = f"¡{nombre_elegido} agregado! 🛒✅"
    st.query_params.clear()
    st.rerun()

# MOSTRAR MENSAJE FLOTANTE DE ÉXITO (TOAST)
if st.session_state.mensaje_exito:
    st.toast(st.session_state.mensaje_exito)
    st.session_state.mensaje_exito = None

# BASE DE DATOS COMPLETA Y CORREGIDA (Evita errores de longitud despareja)
def obtener_carta_completa_pdf():
    # PÁGINA 2: COMBOS, ALITAS Y BROASTER (21 platos)
    p2 = pd.DataFrame({
        "Name": [
            "COMBO 1 (Chi Jau Kay + Pollo)", "COMBO 2 (Tipa Kay + Pollo)", 
            "COMBO 3 (Enrollado + Pollo)", "COMBO 4 (Alitas + Chaufa/Papas)",
            "Alitas Rebozadas 3 Pzs", "Alitas Rebozadas 4 Pzs", "Alitas Rebozadas 5 Pzs", "Alitas Rebozadas 6 Pzs",
            "Alitas BBQ", "Alitas Bravas", "Alitas con Verduras", "Alitas con Tamarindo", 
            "Alitas con Piña", "Alitas Ostión", "Alitas Tausi", "Alitas con Durazno", 
            "Alitas Piña y Durazno", "Alitas Beli Beli", "Alitas Salsa Blanca",
            "1/8 Pollo Broaster", "1/4 Pollo Broaster"
        ],
        "Price": [37.00, 37.00, 37.00, 35.00, 14.00, 18.00, 20.00, 25.00, 22.00, 22.00, 22.00, 22.00, 22.00, 22.00, 22.00, 22.00, 26.00, 25.00, 28.00, 13.00, 21.00],
        "Page": 2
    })
    
    # PÁGINA 3: SOPAS Y CHAUFAS (9 platos)
    p3 = pd.DataFrame({
        "Name": [
            "Sopa Wantán Especial", "Sopa Fuchifú", "Sopa de Wantán Simple",
            "Chaufa de Pollo", "Chaufa de Chancho", "Chaufa de Res", 
            "Chaufa de Langostinos", "Chaufa Especial", "Chaufa Beli Beli (Salvaje)"
        ],
        "Price": [16.00, 16.00, 10.00, 14.00, 18.00, 18.00, 25.00, 22.00, 26.00],
        "Page": 3
    })
    
    # PÁGINA 4: AEROPUERTOS, COMBINADOS Y LOMOS (9 platos)
    p4 = pd.DataFrame({
        "Name": [
            "Aeropuerto de Pollo", "Aeropuerto de Carne / Chancho", "Aeropuerto Especial",
            "Combinado de Pollo", "Combinado de Carne / Chancho", "Combinado Especial",
            "Lomo Saltado de Pollo", "Lomo Saltado de Res", "Lomo Saltado Especial Chifa"
        ],
        "Price": [16.00, 19.00, 22.00, 16.00, 19.00, 22.00, 17.00, 20.00, 24.00],
        "Page": 4
    })
    
    # PÁGINA 5: TALLARINES, WOK SALADO Y DULCE (8 platos)
    p5 = pd.DataFrame({
        "Name": [
            "Tallarín Saltado de Pollo", "Tallarín Saltado de Res / Chancho", "Tallarín Especial",
            "Pollo con Verduras (Wok)", "Chi Jau Kay (Plato)", "Tipa Kay (Plato)",
            "Pollo con Tamarindo", "Pollo con Piña"
        ],
        "Price": [16.00, 19.00, 22.00, 18.00, 20.00, 20.00, 18.00, 19.00],
        "Page": 5
    })
    
    # Fusionamos todas las páginas de forma segura y creamos IDs correlativos automáticos
    df_unido = pd.concat([p2, p3, p4, p5], ignore_index=True)
    df_unido["ID"] = [f"P{i+1}" for i in df_unido.index]
    return df_unido

df_carta = obtener_carta_completa_pdf()

# BASE DE DATOS DEL MENÚ DIARIO
df_menu_diario = pd.DataFrame({
    "Name": ["Chaufa de Pollo", "Alita Rebozada", "1/8 Broaster", "Aeropuerto de Pollo", "Combinado de Pollo"],
    "Price": [14.00, 15.00, 14.00, 17.00, 17.00]
})

# ESTILOS CSS (Garantiza una sola línea compacta por plato)
st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 5px !important;
}

.contenedor-menu-rojo {
    background-color: #8B0000 !important;
    padding: 8px 5px !important;
    border-radius: 6px;
    display: flex !important;
    flex-direction: column !important;
    gap: 5px !important;
    width: 100%;
}

.fila-plato-unica-linea {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
    padding: 3px 0px !important;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.btn-agregar-inline {
    background-color: #FFFFFF !important;
    color: #8B0000 !important;
    text-decoration: none !important;
    font-size: 11px !important;
    font-weight: bold !important;
    border-radius: 50% !important;
    width: 18px !important;
    height: 18px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
}

.texto-plato-inline {
    color: #FFFFFF !important;
    font-size: 10px !important;
    font-weight: bold !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    margin-left: 6px !important;
    margin-right: auto !important;
    text-align: left !important;
}

.precio-plato-inline {
    color: #FFEB3B !important;
    font-size: 11px !important;
    font-weight: bold !important;
    white-space: nowrap !important;
    flex-shrink: 0 !important;
    margin-left: 4px !important;
}

.titulo-seccion-carta {
    color: #8B0000;
    font-size: 14px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 2px;
    border-bottom: 2px solid #8B0000;
}
</style>
""", unsafe_allow_html=True)

# ENCABEZADO PRINCIPAL
st.markdown("<h2 style='text-align:center; color:#8B0000; margin-bottom:0;'>🍜 CHIFA D' BELINDA</h2>", unsafe_allow_html=True)

items_en_carrito = sum(item["cant"] for item in st.session_state.carrito)
tab_carta, tab_menu, tab_pedido = st.tabs([
    "📖 Nuestra Carta", "📋 Menú Diario", f"🛒 Mi Pedido ({items_en_carrito})"
])

# FUNCIÓN REUTILIZABLE PARA GENERAR PÁGINAS DE LA CARTA
def renderizar_hoja_carta(numero_pagina, nombre_imagen):
    col_izq, col_der = st.columns([4.5, 5.5])
    
    with col_izq:
        ruta_foto = f"images/{nombre_imagen}"
        if os.path.exists(ruta_foto):
            st.image(ruta_foto, use_container_width=True)
        else:
            st.info(f"📸 [Falta {ruta_foto}]")
            
    with col_der:
        html_filas = ""
        df_filtrado = df_carta[df_carta["Page"] == numero_pagina]
        
        for _, row in df_filtrado.iterrows():
            p_id = row['ID']
            p_name = row['Name']
            p_price = row['Price']
            
            params = urllib.parse.urlencode({"add_id": p_id, "add_name": p_name, "add_price": p_price})
            link_url = f"?{params}"
            
            html_filas += f"""
            <div class="fila-plato-unica-linea">
                <a class="btn-agregar-inline" href="{link_url}" target="_self">＋</a>
                <span class="texto-plato-inline">{p_name}</span>
                <span class="precio-plato-inline">{int(p_price)}</span>
            </div>
            """
            
        st.markdown(f"""
        <div class="contenedor-menu-rojo">
            {html_filas}
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# 1. PESTAÑA: NUESTRA CARTA (TODAS LAS HOJAS MAPPED)
# =========================================================
with tab_carta:
    st.markdown('<div class="titulo-seccion-carta">🔥 COMBOS & ALITAS ESPECIALES</div>', unsafe_allow_html=True)
    renderizar_hoja_carta(2, "pag2.jpg")
    
    st.markdown('<div class="titulo-seccion-carta">🥣 SOPAS & ARROZ CHAUFA</div>', unsafe_allow_html=True)
    renderizar_hoja_carta(3, "pag3.jpg")
    
    st.markdown('<div class="titulo-seccion-carta">✈️ AEROPUERTOS & LOMOS</div>', unsafe_allow_html=True)
    renderizar_hoja_carta(4, "pag4.jpg")
    
    st.markdown('<div class="titulo-seccion-carta">🔥 TALLARINES & PLATOS AL WOK</div>', unsafe_allow_html=True)
    renderizar_hoja_carta(5, "pag5.jpg")

# =========================================================
# 2. PESTAÑA: MENÚ DIARIO
# =========================================================
with tab_menu:
    st.write("### 📋 Platos de Menú del Día")
    for idx, row in df_menu_diario.iterrows():
        params_menu = urllib.parse.urlencode({"add_id": f"M{idx}", "add_name": f"Menú: {row['Name']}", "add_price": row['Price']})
        
        st.markdown(f"""
        <div style="background-color:#8B0000; padding:6px; margin-bottom:4px; border-radius:4px; display:flex; align-items:center;">
            <a class="btn-agregar-inline" href="?{params_menu}" target="_self">＋</a>
            <span style="color:white; font-size:12px; font-weight:bold; margin-left:8px; flex-grow:1;">{row['Name']}</span>
            <span style="color:#FFEB3B; font-size:12px; font-weight:bold;">S/. {row['Price']:.2f}</span>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# 3. PESTAÑA: MI PEDIDO / WHATSAPP
# =========================================================
with tab_pedido:
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío. Ve a la sección de la carta para añadir tus platos favoritos.")
    else:
        st.subheader("📋 Resumen de tu pedido")
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
        mensaje_wa += f"-------------------------\n💰 *TOTAL PRODUCTOS:* S/. {total:.2f}"
        
        link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"
        st.link_button("📲 ENVIAR PEDIDO POR WHATSAPP", link_final, use_container_width=True)
        
        if st.button("🧹 Vaciar Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()