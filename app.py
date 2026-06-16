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
        /* Imagen de fondo colocada de forma limpia en el contenedor de la app */
        [data-testid="stAppViewContainer"] {{
            background-image: url('data:image/jpeg;base64,{img_b64}') !important;
            background-size: cover !important;
            background-repeat: no-repeat !important;
            background-position: center center !important;
            background-attachment: fixed !important;
        }}
        /* Mantenemos transparencias internas para que no salgan parches grises */
        .main, [data-testid="stCanvas"], [data-testid="stTabPanel"], div[role="tabpanel"] {{
            background-color: transparent !important;
            background: transparent !important;
        }}
        </style>
        """, unsafe_allow_html=True)

# 2. INICIALIZACIÓN DEL CARRITO Y ESTADO DE PÁGINA
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = 1

# =========================================================
# 3. CARGA DE DATOS CON TU MAPEO EXACTO DE PÁGINAS
# =========================================================
@st.cache_data
def cargar_catalogo_con_paginas_exactas():
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

    # Tu distribución exacta de categorías por página
    def mapear_fila_a_pagina(cat):
        if cat in ['COMBOS', 'ALITAS REBOZADAS', 'ALITAS ESPECIALES', 'POLLO BROASTER']:
            return 1
        elif cat in ['SOPAS', 'CHAUFA']:
            return 2
        elif cat in ['AEROPUERTO', 'COMBINADOS', 'LOMOS SALTADOS']:
            return 3
        elif cat in ['TALLARINES SALTADOS', 'PLATOS SALADOS', 'PLATOS DULCES', 'TORTILLAS']:
            return 4
        elif cat in ['ENROLLADOS', 'TAYPA', 'RES', 'LANGOSTINOS', 'PATO', 'CHICHARRONES']:
            return 5
        elif cat in ['CHANCHO', 'COSTILLAS', 'PORCIONES', 'BEBIDAS FRÍAS', 'BEBIDAS CALIENTES']:
            return 6
        return 1

    df['Page_Num'] = df['Category'].apply(mapear_fila_a_pagina)
    return df

df_carta = cargar_catalogo_con_paginas_exactas()

# 4. VENTANA EMERGENTE (MODAL) PARA DETALLES DEL PLATO
@st.dialog("Configura tu Plato 🍜")
def abrir_modal_agregar_plato(id_plato, nombre_plato, precio_plato):
    st.markdown(f"### {nombre_plato}")
    st.markdown(f"**Precio Unitario:** S/. {precio_plato:.2f}")
    st.write("---")

    cantidad = st.number_input("Cantidad:", min_value=1, max_value=20, value=1, step=1)

    st.markdown("**Selecciona tus Cremas / Salsas:**")
    col1, col2 = st.columns(2)
    with col1:
        c_aji = st.checkbox("Ají Chi Chon San 🌶️")
        c_mayo = st.checkbox("Mayonesa ⚪")
    with col2:
        c_ketchup = st.checkbox("Ketchup 🍅")
        c_tamarindo = st.checkbox("Salsa Tamarindo 🍯")

    st.write("")
    notas = st.text_input("Notas / Observaciones (Opcional):", placeholder="Ej: Sin cebolla, bien frito...")

    st.write("")
    if st.button("🛒 AGREGAR AL PEDIDO", use_container_width=True):
        cremas_list = []
        if c_aji: cremas_list.append("Ají")
        if c_mayo: cremas_list.append("Mayo")
        if c_ketchup: cremas_list.append("Ketchup")
        if c_tamarindo: cremas_list.append("Tamarindo")

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
# 5. CSS GLOBAL ESTILO ORIGINAL (MENÚ CLARO / PLATOS VISIBLES)
# =========================================================
st.markdown("""
<style>
/* El bloque superior se mantiene con su fondo claro por defecto de Streamlit */
.main .block-container {
    padding-top: 20px !important;
    padding-bottom: 60px !important;
}

/* Botón redondo amarillo "＋" para agregar platos */
div.stButton > button {
    background-color: #FFEB3B !important;
    color: #8B0000 !important;
    font-size: 20px !important;
    font-weight: bold !important;
    border-radius: 50% !important;
    width: 42px !important;
    height: 42px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: none !important;
    box-shadow: 0px 3px 6px rgba(0,0,0,0.4) !important;
}

/* Títulos de categorías limpios y llamativos */
.titulo-categoria-chifa {
    color: #FFEB3B !important;
    font-size: 16px !important;
    font-weight: bold !important;
    background-color: rgba(139, 0, 0, 0.85) !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    margin-top: 20px !important;
    margin-bottom: 12px !important;
    border-left: 5px solid #FFEB3B !important;
    font-family: sans-serif !important;
}

/* Contenedor de cada plato (Línea invisible, solo texto flotando sobre tu fondo) */
.fila-plato-limpia {
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    padding: 10px 6px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.15) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 6. ENCABEZADO ORIGINAL DE LA APP
# =========================================================
st.title("🍜 Chifa D' Belinda")
st.caption("Pedidos en línea rápidos y directos a nuestro WhatsApp")

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
        # Selector de páginas horizontal nativo (Estilo de tu primera foto)
        pag_seleccionada = st.radio(
            "Selecciona una Página:",
            options=[1, 2, 3, 4, 5, 6],
            format_func=lambda x: f"Pág. {x}",
            horizontal=True,
            key="pagina_actual"
        )

        # Cargar automáticamente tu fondo respectivo según la distribución acordada
        imagen_de_esta_pagina = IMAGENES_POR_PAGINA.get(pag_seleccionada, "pag1.jpeg")
        aplicar_fondo(imagen_de_esta_pagina, pag_seleccionada)

        df_filtrado = df_carta[df_carta["Page_Num"] == pag_seleccionada]

        categoria_actual = ""
        for idx, row in df_filtrado.iterrows():
            if str(row['Category']).strip() != categoria_actual:
                categoria_actual = str(row['Category']).strip()
                st.markdown(f'<div class="titulo-categoria-chifa">📂 {categoria_actual}</div>', unsafe_allow_html=True)

            # Contenedor limpio por cada plato
            col_btn, col_txt = st.columns([0.15, 0.85])
            with col_btn:
                if st.button("＋", key=f"btn_{row['ID']}"):
                    abrir_modal_agregar_plato(row['ID'], row['Name'], row['Price'])
            with col_txt:
                # 🌟 FUERZA DE TEXTO COMPLETO: Letras blancas y precios amarillos sobre tu fondo real
                st.markdown(f"""
                <div class="fila-plato-limpia">
                    <span style="color: #FFFFFF !important; font-size: 15px !important; font-weight: bold !important; text-align: left !important; font-family: sans-serif !important; text-shadow: 1px 1px 4px rgba(0,0,0,0.8) !important;">
                        {row['Name']}
                    </span>
                    <span style="color: #FFEB3B !important; font-size: 16px !important; font-weight: bold !important; white-space: nowrap !important; font-family: sans-serif !important; text-shadow: 1px 1px 4px rgba(0,0,0,0.8) !important; padding-left: 10px;">
                        S/. {float(row['Price']):.2f}
                    </span>
                </div>
                """, unsafe_allow_html=True)

# =========================================================
# PESTAÑA 2: MI PEDIDO (CARRITO)
# =========================================================
with tab_pedido:
    # Quitamos el fondo para la pestaña del pedido para que se pueda rellenar con comodidad en blanco/negro
    st.markdown("""
    <style>
    div[role="tabpanel"] { background-color: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

    if not st.session_state.carrito:
        st.info("Tu carrito está vacío. ¡Explora las páginas de la carta y arma tu orden!")
    else:
        st.subheader("📋 Resumen Total del Pedido")
        total = 0

        for idx, item in enumerate(st.session_state.carrito):
            subtotal = item["precio"] * item["cant"]
            total += subtotal

            col_a, col_b = st.columns([0.85, 0.15])
            with col_a:
                st.markdown(f"💥 **{item['cant']}x {item['nombre']}** — S/. {subtotal:.2f}")
                st.markdown(f"└ 🧂 Salsas: {item['cremas']} | 📝 Nota: {item['notas']}")
            with col_b:
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.carrito.pop(idx)
                    st.rerun()
            st.write("")

        st.divider()
        nombre_cliente = st.text_input("Ingresa tu Nombre Completo:")
        telefono_cliente = st.text_input("Tu número de contacto:")

        if nombre_cliente.strip() and telefono_cliente.strip():
            mensaje_wa = f"🍜 *CHIFA D' BELINDA*\n\n👤 *Cliente:* {nombre_cliente}\n📞 *Contacto:* {telefono_cliente}\n-------------------------\n"
            for item in st.session_state.carrito:
                mensaje_wa += f"✅ {item['cant']}x {item['nombre']} - S/. {item['precio'] * item['cant']:.2f}\n"
                if item['cremas'] != "Ninguna":
                    mensaje_wa += f"  • Salsas: {item['cremas']}\n"
                if item['notas'] != "Ninguna":
                    mensaje_wa += f"  • Nota: {item['notas']}\n"
            mensaje_wa += f"-------------------------\n💰 *TOTAL DEL PEDIDO:* S/. {total:.2f}"

            link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"
            st.write("")
            st.link_button("📲 ENVIAR PEDIDO A WHATSAPP", link_final, use_container_width=True)
        else:
            st.write("")
            st.warning("⚠️ Completa tu nombre y número de contacto para poder enviar el pedido.")

        st.write("")
        if st.button("🧹 Vaciar Todo el Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()