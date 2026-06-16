import streamlit as st
import pandas as pd
import urllib.parse
import os

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Chifa D' Belinda",
    page_icon="🍜",
    layout="centered"
)

# INICIALIZACIÓN DE ESTADOS
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "mensaje_exito" not in st.session_state:
    st.session_state.mensaje_exito = None

# CAPTURAR CLICKS DESDE LOS BOTONES HTML EN LA URL
query_params = st.query_params
if "add_id" in query_params:
    id_elegido = query_params["add_id"]
    nombre_elegido = query_params.get("add_name", "Plato")
    precio_elegido = float(query_params.get("add_price", 0))
    
    # Agregar directo al carrito
    st.session_state.carrito.append({
        "nombre": nombre_elegido,
        "precio": precio_elegido,
        "cant": 1,
        "nota": ""
    })
    st.session_state.mensaje_exito = f"¡{nombre_elegido} agregado! 🛒✅"
    # Limpiar la URL para evitar que se agregue doble al recargar
    st.query_params.clear()
    st.rerun()

# MOSTRAR MENSAJE DE ÉXITO
if st.session_state.mensaje_exito:
    st.toast(st.session_state.mensaje_exito)
    st.session_state.mensaje_exito = None

# DATOS REALES DE TU HOJA 2
def obtener_carta_completa_pdf():
    datos = {
        "ID": [f"P{i}" for i in range(1, 22)],
        "Name": [
            "COMBO 1 (Chi Jau Kay + Pollo Tamarindo)", 
            "COMBO 2 (Tipa Kay + Pollo Verdura)", 
            "COMBO 3 (Enrollado Ostión + Pollo Durazno)",
            "COMBO 4 (Alitas Verduras + Chaufa/Papas)",
            "Alitas Rebozadas 3 Pzs", "Alitas Rebozadas 4 Pzs", 
            "Alitas Rebozadas 5 Pzs", "Alitas Rebozadas 6 Pzs",
            "Alitas en Salsa BBQ", "Alitas Bravas", 
            "Alitas con Verduras", "Alitas con Tamarindo", 
            "Alitas con Piña", "Alitas en Salsa Ostión", 
            "Alitas Tausi", "Alitas con Durazno", 
            "Alitas con Piña y Durazno", "Alitas Beli Beli", 
            "Alitas en Salsa Blanca",
            "1/8 Pollo Broaster", "1/4 Pollo Broaster"
        ],
        "Price": [37.00, 37.00, 37.00, 35.00, 14.00, 18.00, 20.00, 25.00, 22.00, 22.00, 22.00, 22.00, 22.00, 22.00, 22.00, 22.00, 26.00, 25.00, 28.00, 13.00, 21.00],
        "Category": ["COMBOS", "COMBOS", "COMBOS", "COMBOS", "REBOZADAS", "REBOZADAS", "REBOZADAS", "REBOZADAS", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "BROASTER", "BROASTER"]
    }
    return pd.DataFrame(datos)

df_carta = obtener_carta_completa_pdf()

# ESTILOS CSS REVISADOS: OBLIGAN A UNA SOLA LÍNEA SIN ROMPERSE
st.markdown("""
<style>
/* Forzar columnas de la App para que queden lado a lado en celulares */
div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 5px !important;
}

/* CAJA REDONDEADA QUE CONTIENE TODO EL MENÚ DIGITAL DE LA DERECHA */
.contenedor-menu-rojo {
    background-color: #8B0000 !important; /* Rojo idéntico a tu carta */
    padding: 8px 5px !important;
    border-radius: 6px;
    display: flex !important;
    flex-direction: column !important;
    gap: 5px !important;
    width: 100%;
}

/* FILA ULTRA COMPACTA */
.fila-plato-unica-linea {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
    padding: 3px 0px !important;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

/* BOTÓN REDONDO "+" ENLACE */
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

/* TEXTO DEL PLATO RECORTE */
.texto-plato-inline {
    color: #FFFFFF !important;
    font-size: 10.5px !important;
    font-weight: bold !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    margin-left: 6px !important;
    margin-right: auto !important;
    text-align: left !important;
}

/* PRECIO AMARILLO */
.precio-plato-inline {
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
st.markdown("<h2 style='text-align:center; color:#8B0000; margin-bottom:0;'>🍜 CHIFA D' BELINDA</h2>", unsafe_allow_html=True)

items_en_carrito = sum(item["cant"] for item in st.session_state.carrito)
tab_carta, tab_pedido = st.tabs(["📖 Nuestra Carta", f"🛒 Mi Pedido ({items_en_carrito})"])

with tab_carta:
    # Dividimos la pantalla en 2 columnas fijas (45% foto de la izquierda, 55% carta digital derecha)
    col_izq, col_der = st.columns([4.5, 5.5])
    
    with col_izq:
        if os.path.exists("images/pag2_lateral.jpg"):
            st.image("images/pag2_lateral.jpg", use_container_width=True)
        else:
            st.info("📸 [Recorte Izquierdo]")
            
    with col_der:
        # Iniciamos el contenedor rojo oriental para que se vea como un pergamino integrado
        html_filas = ""
        categorias_hoja = ["COMBOS", "REBOZADAS", "ESPECIALES", "BROASTER"]
        df_hoja = df_carta[df_carta["Category"].isin(categorias_hoja)]
        
        for _, row in df_hoja.iterrows():
            p_id = row['ID']
            p_name = row['Name']
            p_price = row['Price']
            
            # Crear los parámetros seguros para el link URL
            params = urllib.parse.urlencode({"add_id": p_id, "add_name": p_name, "add_price": p_price})
            link_url = f"?{params}"
            
            # Construcción estricta de una sola línea HTML limpia
            html_filas += f"""
            <div class="fila-plato-unica-linea">
                <a class="btn-agregar-inline" href="{link_url}" target="_self">＋</a>
                <span class="texto-plato-inline">{p_name}</span>
                <span class="precio-plato-inline">{int(p_price)}</span>
            </div>
            """
            
        # Imprimimos todo el bloque junto dentro del contenedor para que no se desarme jamás en celulares
        st.markdown(f"""
        <div class="contenedor-menu-rojo">
            {html_filas}
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# PESTAÑA: PEDIDO / WHATSAPP
# =========================================================
with tab_pedido:
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío.")
    else:
        st.subheader("📋 Tu Pedido")
        total = 0
        for item in st.session_state.carrito:
            subtotal = item["precio"] * item["cant"]
            total += subtotal
            st.markdown(f"💥 **{item['cant']}x {item['nombre']}** — S/. {subtotal:.2f}")
            
        st.divider()
        nombre_cliente = st.text_input("Tu Nombre")
        
        mensaje_wa = f"🍜 *CHIFA D' BELINDA*\n\n👤 *Cliente:* {nombre_cliente}\n-------------------------\n"
        for item in st.session_state.carrito:
            mensaje_wa += f"✅ {item['cant']}x {item['nombre']} - S/. {item['precio'] * item['cant']:.2f}\n"
        mensaje_wa += f"-------------------------\n💰 *TOTAL:* S/. {total:.2f}"
        
        link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"
        st.link_button("📲 ENVIAR PEDIDO POR WHATSAPP", link_final, use_container_width=True)
        
        if st.button("🧹 Vaciar Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()