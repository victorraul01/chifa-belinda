import streamlit as st
import pandas as pd
import urllib.parse
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Chifa D' Belinda",
    page_icon="🍜",
    layout="centered"
)

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

# 4. BASE DE DATOS DETALLADA DE LA CARTA (Páginas 2 a 7)
def obtener_carta_completa_pdf():
    # PÁGINA 2: COMBOS Y ALITAS
    p2 = pd.DataFrame({
        "Name": [
            "COMBO 1 (Chi Jau Kay + Pollo)", "COMBO 2 (Tipa Kay + Pollo)", 
            "COMBO 3 (Enrollado + Pollo)", "COMBO 4 (Alitas + Chaufa/Papas)",
            "Alitas Rebozadas 3 Pzs", "Alitas Rebozadas 4 Pzs", "Alitas Rebozadas 5 Pzs", "Alitas Rebozadas 6 Pzs",
            "Alitas BBQ", "Alitas Bravas", "Alitas con Verduras", "Alitas con Tamarindo"
        ],
        "Price": [37.00, 37.00, 37.00, 35.00, 14.00, 18.00, 20.00, 25.00, 22.00, 22.00, 22.00, 22.00],
        "Page": 2
    })
    
    # PÁGINA 3: SOPAS Y CHAUFAS
    p3 = pd.DataFrame({
        "Name": [
            "Sopa Wantán Especial", "Sopa Fuchifú", "Sopa de Wantán Simple",
            "Chaufa de Pollo", "Chaufa de Chancho", "Chaufa de Res", "Chaufa Especial"
        ],
        "Price": [16.00, 16.00, 10.00, 14.00, 18.00, 18.00, 22.00],
        "Page": 3
    })
    
    # PÁGINA 4: AEROPUERTOS Y LOMOS
    p4 = pd.DataFrame({
        "Name": [
            "Aeropuerto de Pollo", "Aeropuerto Especial",
            "Combinado de Pollo", "Combinado Especial",
            "Lomo Saltado de Pollo", "Lomo Saltado de Res"
        ],
        "Price": [16.00, 22.00, 16.00, 22.00, 17.00, 20.00],
        "Page": 4
    })
    
    # PÁGINA 5: TALLARINES Y WOK
    p5 = pd.DataFrame({
        "Name": [
            "Tallarín Saltado de Pollo", "Tallarín Especial",
            "Pollo con Verduras", "Chi Jau Kay (Plato)", "Tipa Kay (Plato)"
        ],
        "Price": [16.00, 22.00, 18.00, 20.00, 20.00],
        "Page": 5
    })

    # PÁGINA 6: ENTRADAS Y EXTRAS
    p6 = pd.DataFrame({
        "Name": ["Porción Wantán Frito", "Chaufa Familiar", "Nabo Encurtido", "Papas Fritas"],
        "Price": [10.00, 25.00, 5.00, 8.00],
        "Page": 6
    })

    # PÁGINA 7: BEBIDAS
    p7 = pd.DataFrame({
        "Name": ["Gaseosa 1L", "Chicha Morada Jarra", "Gaseosa Personal", "Agua Mineral"],
        "Price": [10.00, 12.00, 4.00, 3.50],
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

# 5. ESTILOS CSS CORREGIDOS (Para evitar textos sueltos y mejorar carga en móvil)
st.markdown("""
<style>
.block-container {
    padding-left: 6px !important;
    padding-right: 6px !important;
    padding-top: 10px !important;
}

/* Tarjeta contenedora de dos columnas fijas */
.tarjeta-split-carta {
    display: flex !important;
    flex-direction: row !important;
    width: 100% !important;
    background-color: #8C0712 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4) !important;
    margin-bottom: 20px !important;
}

/* Columna izquierda para tu imagen real */
.columna-foto-carta {
    width: 45% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background-color: #70050e !important;
}
.columna-foto-carta img {
    width: 100% !important;
    height: auto !important;
    object-fit: cover !important;
}

/* Columna derecha interactiva para tus platos */
.columna-platos-interactiva {
    width: 55% !important;
    padding: 10px 6px !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 6px !important;
    box-sizing: border-box !important;
}

/* Filas de los platos individuales */
.fila-plato-interactiva {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    width: 100% !important;
    background: rgba(0, 0, 0, 0.2) !important;
    padding: 6px 4px !important;
    border-radius: 5px !important;
    box-sizing: border-box !important;
}

.btn-mas-flotante {
    background-color: #FFFFFF !important;
    color: #8B0000 !important;
    text-decoration: none !important;
    font-size: 12px !important;
    font-weight: bold !important;
    border-radius: 50% !important;
    width: 20px !important;
    height: 20px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
}

.texto-menu-flotante {
    color: #FFFFFF !important;
    font-size: 10px !important;
    font-weight: bold !important;
    line-height: 1.2 !important;
    margin-left: 6px !important;
    margin-right: auto !important;
    text-align: left !important;
}

.precio-menu-flotante {
    color: #FFEB3B !important;
    font-size: 11px !important;
    font-weight: bold !important;
    white-space: nowrap !important;
    flex-shrink: 0 !important;
    margin-left: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# ENCABEZADO
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
        format_func=lambda x: f"Pág. {x} " + ("(Combos)" if x==2 else "(Chaufas)" if x==3 else "(Lomos)" if x==4 else "(Wok)" if x==5 else "(Extras)" if x==6 else "(Bebidas)"),
        horizontal=True
    )
    
    # Construcción limpia de las filas de platos en HTML
    html_filas = ""
    df_filtrado = df_carta[df_carta["Page"] == pag_seleccionada]
    
    for _, row in df_filtrado.iterrows():
        p_id = row['ID']
        p_name = row['Name']
        p_price = row['Price']
        
        params = urllib.parse.urlencode({"add_id": p_id, "add_name": p_name, "add_price": p_price})
        html_filas += f"""
        <div class="fila-plato-interactiva">
            <a class="btn-mas-flotante" href="?{params}" target="_self">＋</a>
            <span class="texto-menu-flotante">{p_name}</span>
            <span class="precio-menu-flotante">{int(p_price)}</span>
        </div>
        """
        
    # Rutas alternativas de imágenes para evitar fallas de carga en GitHub/Streamlit Cloud
    nombre_imagen = f"pag{pag_seleccionada}.jpg"
    
    # Intentar buscar la imagen en múltiples rutas posibles del proyecto
    rutas_posibles = [
        os.path.join("images", nombre_imagen),
        os.path.join("app", "static", "images", nombre_imagen),
        nombre_imagen
    ]
    
    ruta_valida = None
    for r in rutas_posibles:
        if os.path.exists(r):
            ruta_valida = r
            break

    if ruta_valida:
        # Si encuentra la imagen, monta la estructura split perfectamente balanceada
        html_carta_completa = f"""
        <div class="tarjeta-split-carta">
            <div class="columna-foto-carta">
                <img src="app/static/{ruta_valida}" />
            </div>
            <div class="columna-platos-interactiva">
                {html_filas}
            </div>
        </div>
        """
        st.markdown(html_carta_completa, unsafe_allow_html=True)
    else:
        # Alerta amigable si la imagen no se subió o cambió de nombre
        st.info(f"💡 Mostrando platos de la Página {pag_seleccionada}. Recuerda subir '{nombre_imagen}' a tu carpeta 'images'.")
        html_carta_sin_foto = f"""
        <div class="tarjeta-split-carta">
            <div class="columna-platos-interactiva" style="width: 100% !important;">
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