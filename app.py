import streamlit as st
import pandas as pd
import urllib.parse
import base64
import os
import time

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Chifa D' Belinda",
    page_icon="🍜",
    layout="centered"
)

# 2. INICIALIZACIÓN DEL CARRITO
if "carrito" not in st.session_state:
    st.session_state["carrito"] = []

if "mostrar_modal" not in st.session_state:
    st.session_state["mostrar_modal"] = False
    st.session_state["modal_plato_info"] = None
    st.session_state["modal_origen"] = "Carta"
    st.session_state["modal_categoria"] = "GENERAL"

# Opciones del Menú del Día
PLATOS_MENU_INTERNO = [
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
    {"ID": "M23", "Name": "Tallarín de Res", "Price": 20.00},
    {"ID": "M24", "Name": "Combinado de Res", "Price": 20.00},
    {"ID": "M25", "Name": "Chancho con Piña", "Price": 20.00},
    {"ID": "M26", "Name": "Chancho con Tamarindo", "Price": 20.00},
    {"ID": "M27", "Name": "¼ Broaster", "Price": 22.00},
    {"ID": "M28", "Name": "Alitas a la BBQ (3 piezas)", "Price": 18.00},
    {"ID": "M29", "Name": "Alitas Acevichadas (3 piezas)", "Price": 18.00}
]

@st.cache_data
def cargar_imagen_b64(nombre_imagen):
    rutas_posibles = [os.path.join("images", nombre_imagen), os.path.join("app", "static", "images", nombre_imagen), nombre_imagen]
    for r in rutas_posibles:
        if os.path.exists(r):
            with open(r, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

IMAGENES_POR_PAGINA = {1: "pag1.jpeg", 2: "pag2.jpeg", 3: "pag3.jpeg", 4: "pag5.jpeg", 5: "pag5.jpeg", 6: "pag6.jpeg", "menu": "pag1.jpeg"}

def aplicar_fondo(nombre_imagen, pagina_id):
    img_b64 = cargar_imagen_b64(nombre_imagen)
    if img_b64:
        st.markdown(f"""
        <style id="fondo-pagina-{pagina_id}">
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.45)), url('data:image/jpeg;base64,{img_b64}') !important;
            background-size: cover !important; background-repeat: no-repeat !important; background-position: center center !important; background-attachment: fixed !important;
        }}
        .main, [data-testid="stCanvas"], [data-testid="stTabPanel"], div[role="tabpanel"], div[data-testid="stVerticalBlock"], [data-testid="stApp"], [data-testid="stHeader"] {{
            background-color: transparent !important; background: transparent !important; box-shadow: none !important;
        }}
        </style>
        """, unsafe_allow_html=True)

# Distribución estructural
DISTRIBUCION_PAGINAS = {
    1: ['COMBOS', 'ALITAS REBOZADAS', 'ALITAS ESPECIALES', 'POLLO BROASTER'],
    2: ['SOPAS', 'CHAUFA'], 
    3: ['AEROPUERTO', 'COMBINADOS', 'LOMOS SALTADOS'],
    4: ['TALLARINES SALTADOS', 'PLATOS SALADOS', 'PLATOS DULCES', 'TORTILLAS'], 
    5: ['ENROLLADOS', 'TAYPA', 'RES', 'LANGOSTINOS', 'PATO', 'CHICHARRONES'],
    6: ['CHANCHO', 'COSTILLAS', 'PORCIONES', 'BEBIDAS FRÍAS', 'BEBIDAS CALIENTES']
}

@st.cache_data(ttl=10)
def cargar_catalogo_limpio():
    nombre_archivo = "Catalogo_Productos.xlsx"
    nombre_csv = "Catalogo_Productos.xlsx - in.csv"
    if os.path.exists(nombre_archivo): df = pd.read_excel(nombre_archivo)
    elif os.path.exists(nombre_csv): df = pd.read_csv(nombre_csv)
    else: return pd.DataFrame()
    
    df.columns = df.columns.str.strip()
    
    if 'Category' in df.columns:
        df['Category'] = df['Category'].astype(str).str.strip().str.upper()
    
    if 'Description' not in df.columns:
        df['Description'] = ""
    else:
        df['Description'] = df['Description'].fillna("").astype(str).str.strip()
        
    return df

df_carta = cargar_catalogo_limpio()

# =========================================================
# MODAL DE CONFIGURACIÓN
# =========================================================
@st.dialog("Configura tu Plato 🍜")
def abrir_modal_dinamico():
    p_info = st.session_state["modal_plato_info"]
    p_orig = st.session_state["modal_origen"]
    p_cat_name = st.session_state["modal_categoria"]
    
    st.markdown(f"### {p_info['Name']}")
    st.markdown(f"*Tipo:* {p_orig} | *Precio Unitario:* S/. {p_info['Price']:.2f}")
    st.write("---")
    
    entrada_sel = ""
    if p_orig == "Menú del Día":
        st.markdown("*Elige tu Entrada (Incluida):*")
        entrada_sel = st.radio("", ["Sopa Wantán 🥣", "Wantán Frito 🥟"], horizontal=True, label_visibility="collapsed")
        st.write("---")

    cantidad = st.number_input("Cantidad:", min_value=1, max_value=20, value=1, step=1)
    st.markdown("*Selecciona tus Cremas / Salsas:*")
    c_aji = st.checkbox("Ají Chi Chon San 🌶️")
    c_mayo = st.checkbox("Mayonesa ⚪")
    c_ketchup = st.checkbox("Ketchup 🍅")
    c_tamarindo = st.checkbox("Salsa Tamarindo 🍯")
    
    mostrar_limon = any(k in p_cat_name for k in ["ALITAS", "BROASTER"])
    c_limon = st.checkbox("Limón 🍋") if mostrar_limon else False

    notas = st.text_input("Notas / Observaciones (Opcional):", placeholder="Ej: Sin cebolla...")

    if st.button("🛒 AGREGAR AL PEDIDO", use_container_width=True, key="btn_guardar_modal_real"):
        cremas_list = [c for c, val in [("Ají", c_aji), ("Mayonesa", c_mayo), ("Ketchup", c_ketchup), ("Tamarindo", c_tamarindo)] if val]
        if mostrar_limon and c_limon: cremas_list.append("Limón")
        
        nuevo_item = {
            "uid": time.time(), "id": p_info["ID"], "nombre": p_info["Name"], "precio": float(p_info["Price"]),
            "cant": int(cantidad), "cremas": ", ".join(cremas_list), "notas": notas.strip(), "tipo": p_orig, "entrada": entrada_sel
        }
        st.session_state["carrito"].append(nuevo_item)
        st.session_state["mostrar_modal"] = False
        st.rerun()

# =========================================================
# CSS MAESTRO DEFINITIVO
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

.fila-plato-flex {
    display: flex !important; justify-content: space-between !important; align-items: flex-start !important;
    width: 100% !important; padding: 2px 0px !important; box-sizing: border-box !important;
}
.bloque-izq-nombre { flex-grow: 1 !important; text-align: left !important; padding-right: 10px !important; }
.texto-nombre-plato { color: #FFFFFF !important; font-size: 16px !important; font-weight: bold !important; text-shadow: 2px 2px 2px #000000 !important; display: block; }
.texto-descripcion-plato { color: #E0E0E0 !important; font-size: 12.5px !important; font-style: italic !important; margin-top: 2px; display: block; text-shadow: 1px 1px 2px #000000 !important; line-height: 1.2; }
.texto-precio-plato { color: #FFEB3B !important; font-size: 16px !important; font-weight: 900 !important; text-shadow: 2px 2px 2px #000000 !important; white-space: nowrap !important; }

.titulo-categoria-chifa { 
    color: #FFEB3B !important; 
    font-size: 21px !important; 
    font-weight: 900 !important; 
    padding: 12px 10px !important; 
    margin-top: 25px !important; 
    margin-bottom: 12px !important;
    border-left: 6px solid #FFEB3B !important; 
    background-color: rgba(0, 0, 0, 0.7) !important;
    border-radius: 0 8px 8px 0;
    text-shadow: 2px 2px 4px #000000 !important; 
    letter-spacing: 0.5px;
}

div[data-testid="stHorizontalBlock"] div.stButton > button {
    background-color: #FFEB3B !important; color: #8B0000 !important;
    font-size: 22px !important; font-weight: bold !important;
    border-radius: 8px !important; width: 42px !important; height: 42px !important;
    padding: 0px !important; border: none !important;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.5) !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
}

div[data-testid="stDialog"] div.stButton > button, 
div.boton-vaciar-pedido div.stButton > button {
    width: 100% !important; height: 45px !important;
    background-color: #FFEB3B !important; color: #8B0000 !important;
    font-size: 16px !important; font-weight: bold !important;
    border-radius: 8px !important; display: block !important; border: none !important;
}

div.boton-tacho-contenedor div.stButton > button {
    background-color: #FFEB3B !important; color: #8B0000 !important;
    font-size: 14px !important; width: 32px !important; height: 32px !important;
    border-radius: 6px !important; padding: 0px !important; display: flex !important;
}

.fila-carrito-ordenada { padding: 8px 0px !important; border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important; width: 100%; }
.linea-principal-carrito { display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: space-between !important; width: 100% !important; }
.texto-plato-carrito { color: #FFFFFF !important; font-size: 16px !important; font-weight: bold !important; text-shadow: 2px 2px 2px #000000 !important; }
.texto-precio-carrito { color: #FFFFFF !important; font-size: 16px !important; font-weight: bold !important; text-shadow: 2px 2px 2px #000000 !important; }
.texto-detalles-resaltados { color: #FFFFFF !important; font-size: 13px !important; font-weight: 500 !important; display: block; margin-left: 36px; opacity: 0.95; }

.enlace-wa-directo-siempre { 
    display: block !important; background-color: #25D366 !important; color: white !important; 
    text-align: center !important; font-weight: bold !important; font-size: 16px !important; 
    padding: 14px 20px !important; border-radius: 8px !important; text-decoration: none !important; 
    box-shadow: 0px 5px 10px rgba(0,0,0,0.4) !important; margin: 18px 0px !important; border: 1px solid #ffffff !important; 
}
.alerta-delivery-destacada { background-color: rgba(0, 0, 0, 0.75) !important; border: 2px solid #FFEB3B !important; padding: 15px !important; border-radius: 10px !important; color: #FFFFFF !important; margin-bottom: 15px; }
.recuadro-total-final { background-color: rgba(0, 0, 0, 0.5) !important; border: 1px solid #FFEB3B !important; border-radius: 8px !important; padding: 12px 15px !important; margin: 20px 0px !important; display: flex !important; justify-content: space-between !important; }
</style>
""", unsafe_allow_html=True)

# 3. ENCABEZADO FIJO
st.markdown("""
<div class="cabecera-fija-chifa">
    <h2 style="margin: 0; font-size: 25px; color: #FFEB3B; font-family: sans-serif; text-shadow: 2px 2px 4px #000000;">🍜 CHIFA D' BELINDA</h2>
    <p style="margin: 3px 0 0 0; font-size: 13px; color: #FFFFFF; text-shadow: 1px 1px 2px #000000;">Pedidos en línea rápidos y directos a nuestro WhatsApp</p>
</div>
""", unsafe_allow_html=True)

items_en_carrito = sum(item["cant"] for item in st.session_state.carrito)

# 4. CREACIÓN DE PESTAÑAS
tab_menu, tab_carta, tab_pedido = st.tabs(["🍱 Menú del Día", "📖 Platos a la Carta", f"🛒 Mi Pedido ({items_en_carrito})"])

# PESTAÑA: 🍱 MENÚ DEL DÍA
with tab_menu:
    st.markdown('<div style="padding: 10px 5px; margin-top: 15px;">', unsafe_allow_html=True)
    aplicar_fondo("pag1.jpeg", "menu")
    st.markdown('<div class="titulo-categoria-chifa">🍱 MENÚ CHIFA DEL DÍA</div>', unsafe_allow_html=True)
    
    for plato in PLATOS_MENU_INTERNO:
        col_txt, col_btn = st.columns([0.82, 0.18])
        with col_txt:
            st.markdown(f'<div class="fila-plato-flex"><div class="bloque-izq-nombre"><span class="texto-nombre-plato">{plato["Name"]}</span></div><div><span class="texto-precio-plato">S/. {plato["Price"]:.2f}</span></div></div>', unsafe_allow_html=True)
        with col_btn:
            if st.button("＋", key=f"btn_menu_{plato['ID']}"):
                st.session_state["modal_plato_info"] = plato
                st.session_state["modal_origen"] = "Menú del Día"
                st.session_state["modal_categoria"] = "MENÚ"
                st.session_state["mostrar_modal"] = True
                st.rerun()
        st.markdown('<hr style="border:0; border-top: 1px solid rgba(255, 255, 255, 0.18); margin: 2px 0 4px 0;">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# PESTAÑA: 📖 PLATOS A LA CARTA
with tab_carta:
    if df_carta.empty:
        st.warning("⚠️ Por favor, carga tu archivo del catálogo.")
    else:
        pag_seleccionada = st.radio("Selecciona una Página:", options=[1, 2, 3, 4, 5, 6], format_func=lambda x: f"Pág. {x}", horizontal=True, key="pagina_actual")
        aplicar_fondo(IMAGENES_POR_PAGINA.get(pag_seleccionada, "pag1.jpeg"), pag_seleccionada)

        for cat_name in DISTRIBUCION_PAGINAS.get(pag_seleccionada, []):
            df_filtrado_cat = df_carta[df_carta["Category"].str.upper().str.strip() == cat_name.upper().strip()]
            
            if not df_filtrado_cat.empty:
                st.markdown(f'<div class="titulo-categoria-chifa">📂 {cat_name}</div>', unsafe_allow_html=True)
                for idx, row in df_filtrado_cat.iterrows():
                    col_txt, col_btn = st.columns([0.82, 0.18])
                    
                    desc_html = f'<span class="texto-descripcion-plato">{row["Description"]}</span>' if row["Description"] else ''
                    
                    with col_txt:
                        st.markdown(f"""
                        <div class="fila-plato-flex">
                            <div class="bloque-izq-nombre">
                                <span class="texto-nombre-plato">{row["Name"]}</span>
                                {desc_html}
                            </div>
                            <div>
                                <span class="texto-precio-plato">S/. {float(row["Price"]):.2f}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_btn:
                        if st.button("＋", key=f"btn_carta_{row['ID']}_{idx}"):
                            st.session_state["modal_plato_info"] = {"ID": row['ID'], "Name": row['Name'], "Price": row['Price']}
                            st.session_state["modal_origen"] = "Carta"
                            st.session_state["modal_categoria"] = cat_name
                            st.session_state["mostrar_modal"] = True
                            st.rerun()
                    st.markdown('<hr style="border:0; border-top: 1px solid rgba(255, 255, 255, 0.18); margin: 4px 0 6px 0;">', unsafe_allow_html=True)

# PESTAÑA: 🛒 MI PEDIDO
with tab_pedido:
    st.markdown('<div style="padding: 10px 5px; margin-top: 15px;">', unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.markdown('<h3 style="color: white; text-shadow: 2px 2px 2px black;">Tu carrito está vacío. ¡Explora la carta!</h3>', unsafe_allow_html=True)
    else:
        st.markdown('<h2 style="color: #FFEB3B; text-shadow: 2px 2px 3px black; font-size:22px;">📋 Resumen Total del Pedido</h2>', unsafe_allow_html=True)
        total = 0

        for i, item in enumerate(st.session_state.carrito):
            subtotal = item["precio"] * item["cant"]
            total += subtotal
            detalles_lista = [f"📌 {item.get('tipo','Carta')}"]
            if item.get("entrada"): detalles_lista.append(f"🍲 {item['entrada']}")
            if item.get('cremas'): detalles_lista.append(f"🧂 {item['cremas']}")
            if item.get('notas'): detalles_lista.append(f"📝 {item['notas']}")

            st.markdown('<div class="fila-carrito-ordenada">', unsafe_allow_html=True)
            col_tacho, col_info = st.columns([0.12, 0.88])
            with col_tacho:
                st.markdown('<div class="boton-tacho-contenedor">', unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_{item['uid']}_{i}"):
                    st.session_state.carrito.pop(i)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with col_info:
                st.markdown(f'<div class="linea-principal-carrito"><span class="texto-plato-carrito">💥 {item["cant"]}x {item["nombre"]}</span><span class="texto-precio-carrito">S/. {subtotal:.2f}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<span class="texto-detalles-resaltados">{" | ".join(detalles_lista)}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="recuadro-total-final"><span style="color:#FFF; font-size:17px; font-weight:bold;">💵 TOTAL:</span><span style="color:#FFEB3B; font-size:20px; font-weight:900;">S/. {total:.2f}</span></div>', unsafe_allow_html=True)
        
        nombre_cliente = st.text_input("Ingresa tu Nombre Completo:", key="nom_cli")
        metodo_entrega = st.radio("Método de Entrega:", ["Delivery Moto 🏍️", "Recojo en Local 🏪"], horizontal=True, key="met_ent")

        direccion_cliente = ""
        if metodo_entrega == "Delivery Moto 🏍️":
            direccion_cliente = st.text_input("Dirección de Envío:", placeholder="Ej: Av. Perú 123...", key="dir_cli")
            st.markdown('<div class="alerta-delivery-destacada">🚨 <b>AVISO:</b> Compartir ubicación por WhatsApp. Costo de envío variable.</div>', unsafe_allow_html=True)

        metodo_pago = st.radio("Método de Pago:", ["Yape 📱", "Efectivo 💵"], horizontal=True, key="met_pag")

        # CONSTRUCCIÓN DEL MENSAJE DE WHATSAPP CON DETALLE CARTA/MENÚ
        mensaje_wa = f"🍜 CHIFA D' BELINDA\n\n👤 Cliente: {nombre_cliente.strip()}\n♻️ Entrega: {metodo_entrega}\n"
        if metodo_entrega == "Delivery Moto 🏍️": 
            mensaje_wa += f"📍 Dirección: {direccion_cliente.strip()}\n"
        mensaje_wa += f"💳 Pago: {metodo_pago}\n-------------------------\n"
        
        for item in st.session_state.carrito:
            # Determinamos el tipo para el texto de WhatsApp brevemente: (MENÚ) o (CARTA)
            tipo_txt = "(MENÚ)" if item.get('tipo') == "Menú del Día" else "(CARTA)"
            
            mensaje_wa += f"✅ {item['cant']}x {item['nombre']} {tipo_txt} - S/. {item['precio'] * item['cant']:.2f}\n"
            if item.get("entrada"): 
                mensaje_wa += f"   ↳ Entrada: {item['entrada']}\n"
            if item.get('cremas'): 
                mensaje_wa += f"   ↳ Cremas: {item['cremas']}\n"
            if item.get('notas'): 
                mensaje_wa += f"   ↳ Obs: {item['notas']}\n"
                
        mensaje_wa += f"-------------------------\n💰 TOTAL: S/. {total:.2f}"
        link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"

        error_msg = ""
        if not nombre_cliente.strip():
            error_msg = "Por favor ingrese su Nombre."
        elif metodo_entrega == "Delivery Moto 🏍️" and not direccion_cliente.strip():
            error_msg = "Por favor ingrese su Dirección."

        if error_msg:
            st.markdown(f'<a href="#" onclick="alert(\'{error_msg}\'); return false;" class="enlace-wa-directo-siempre">💬 ENVIAR PEDIDO A WHATSAPP</a>', unsafe_allow_html=True)
        else:
            st.markdown(f'<a href="{link_final}" target="_blank" class="enlace-wa-directo-siempre">💬 ENVIAR PEDIDO A WHATSAPP</a>', unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="boton-vaciar-pedido">', unsafe_allow_html=True)
        if st.button("🗑️ Vaciar Todo el Carrito", use_container_width=True, key="btn_vaciar_pedido_real"):
            st.session_state.carrito = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state["mostrar_modal"]:
    abrir_modal_dinamico()