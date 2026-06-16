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

# INICIALIZACIÓN DE ESTADOS
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "mensaje_exito" not in st.session_state:
    st.session_state.mensaje_exito = None

# MOSTRAR METADATO DE ÉXITO TIPO TOAST
if st.session_state.mensaje_exito:
    st.toast(st.session_state.mensaje_exito)
    st.session_state.mensaje_exito = None

# ESTRUCTURA DE DATOS REALES EXTRAÍDOS DIRECTAMENTE DE TU PDF
def obtener_carta_completa_pdf():
    # Mapeo exacto de categorías y precios según tu documento oficial
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
        "Price": [
            37.00, 37.00, 37.00, 35.00,
            14.00, 18.00, 20.00, 25.00,
            22.00, 22.00, 22.00, 22.00, 22.00, 22.00, 22.00, 22.00, 26.00, 25.00, 28.00,
            13.00, 21.00
        ],
        "Category": [
            "COMBOS", "COMBOS", "COMBOS", "COMBOS",
            "REBOZADAS", "REBOZADAS", "REBOZADAS", "REBOZADAS",
            "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES", "ESPECIALES",
            "BROASTER", "BROASTER"
        ]
    }
    return pd.DataFrame(datos)

df_carta = obtener_carta_completa_pdf()

# BASE DE DATOS DEL MENÚ DIARIO
df_menu_diario = pd.DataFrame({
    "Name": ["Chaufa de Pollo", "Alita Rebozada", "1/8 Broaster", "Aeropuerto de Pollo", "Combinado de Pollo"],
    "Price": [14.00, 15.00, 14.00, 17.00, 17.00]
})

# ESTILOS CSS CORREGIDOS: CERO CÓDIGO HTML EXPUESTO, INTEGRACIÓN NATIVA LIMPIA
st.markdown("""
<style>
/* Forzar que las columnas de Streamlit no tengan márgenes gigantes en teléfonos */
div[data-testid="stHorizontalBlock"] {
    gap: 4px !important;
    background-color: #7A0A0A !important; /* Rojo oscuro oriental idéntico al de tu carta */
    padding: 3px 6px !important;
    border-radius: 4px;
    margin-bottom: 3px !important;
    display: flex !important;
    align-items: center !important;
}

/* Estilo para los textos de los platos */
.label-plato-blanco {
    color: #FFFFFF !important;
    font-size: 11px !important;
    font-weight: bold !important;
    white-space: nowrap !important;
}

/* Estilo para los precios */
.label-precio-amarillo {
    color: #FFEB3B !important; /* Amarillo brillante para contrastar en el fondo rojo */
    font-size: 11px !important;
    font-weight: bold !important;
    text-align: right;
}

/* Rediseño total de los botones nativos de agregar */
div.stButton > button {
    background-color: #FFFFFF !important;
    color: #7A0A0A !important;
    border: 1px solid #FFFFFF !important;
    border-radius: 50% !important; /* Circular impecable */
    width: 22px !important;
    height: 22px !important;
    padding: 0px !important;
    font-size: 12px !important;
    font-weight: bold !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

div.stButton > button:hover {
    background-color: #FFEB3B !important;
    color: #7A0A0A !important;
}

/* Ocultar elementos globales innecesarios en móviles */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# MODAL DE SELECCIÓN DE DETALLES
@st.dialog("🛒 Detalles del Pedido")
def modal_pedido(nombre, precio):
    st.write(f"### {nombre}")
    st.write(f"Precio: S/. {precio:.2f}")
    cant = st.number_input("Cantidad", min_value=1, value=1)
    notas = st.text_input("Notas adicionales (Sin cebolla, etc.)")
    
    if st.button("Agregar al carrito", use_container_width=True):
        st.session_state.carrito.append({
            "nombre": nombre,
            "precio": precio,
            "cant": cant,
            "nota": notas
        })
        st.session_state.mensaje_exito = f"¡{nombre} agregado! 🛒"
        st.rerun()

# CUERPO DE LA APLICACIÓN
st.markdown("<h2 style='text-align:center; color:#7A0A0A; margin-bottom:0;'>🍜 CHIFA D' BELINDA</h2>", unsafe_allow_html=True)

items_en_carrito = sum(item["cant"] for item in st.session_state.carrito)
tab_carta, tab_menu, tab_pedido = st.tabs([
    "📖 Nuestra Carta", "📋 Menú Diario", f"🛒 Mi Pedido ({items_en_carrito})"
])

# =========================================================
# 1. PESTAÑA: NUESTRA CARTA (DISEÑO DE PÁGINA 2)
# =========================================================
with tab_carta:
    # Columna izquierda: Tu imagen real recortada / Columna derecha: El menú digital integrado en bloque rojo
    col_izq_foto, col_der_menu = st.columns([4.5, 5.5])
    
    with col_izq_foto:
        # Aquí se carga de forma nativa la foto lateral que enviaste
        if os.path.exists("images/pag2_lateral.jpg"):
            st.image("images/pag2_lateral.jpg", use_container_width=True)
        else:
            # Cuadro de muestra temporal por si no encuentra el archivo físico
            st.info("📸 [Aquí va el recorte de tus imágenes de la izquierda]")
            
    with col_der_menu:
        # Agrupamos consecutivamente todo lo que me dijiste que va en esa hoja real (Página 2)
        categorias_hoja = ["COMBOS", "REBOZADAS", "ESPECIALES", "BROASTER"]
        df_hoja = df_carta[df_carta["Category"].isin(categorias_hoja)]
        
        for _, row in df_hoja.iterrows():
            # Creamos 3 microcolumnas internas nativas: Botón (1.5) | Nombre (7.0) | Precio (1.5)
            c_btn, c_name, c_price = st.columns([1.5, 7.0, 1.5])
            
            with c_btn:
                # El botón "+" real de Streamlit, limpio y posicionado perfectamente a la izquierda
                if st.button("＋", key=f"add_{row['ID']}"):
                    modal_pedido(row["Name"], row["Price"])
            
            with c_name:
                st.markdown(f"<span class='label-plato-blanco'>{row['Name']}</span>", unsafe_allow_html=True)
                
            with c_price:
                st.markdown(f"<span class='label-precio-amarillo'>{int(row['Price'])}</span>", unsafe_allow_html=True)

# =========================================================
# 2. PESTAÑA: MENÚ DIARIO
# =========================================================
with tab_menu:
    st.caption("Los menús diarios están disponibles en el local de lunes a viernes.")
    for idx, row in df_menu_diario.iterrows():
        c_btn, c_name = st.columns([1.5, 8.5])
        with c_btn:
            if st.button("＋", key=f"menu_{idx}"):
                modal_pedido(row["Name"], row["Price"])
        with c_name:
            st.write(f"**{row['Name']}** — S/. {row['Price']:.2f}")

# =========================================================
# 3. PESTAÑA: MI PEDIDO / FINALIZAR POR WHATSAPP
# =========================================================
with tab_pedido:
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío. ¡Explora la carta para agregar deliciosos platos!")
    else:
        st.subheader("📋 Resumen de Compra")
        total = 0
        for item in st.session_state.carrito:
            subtotal = item["precio"] * item["cant"]
            total += subtotal
            st.markdown(f"💥 **{item['cant']}x {item['nombre']}** — S/. {subtotal:.2f}")
            if item["nota"]:
                st.caption(f"   ↳ Nota: {item['nota']}")
        
        st.divider()
        nombre_cliente = st.text_input("Ingresa tu Nombre")
        metodo_pago = st.radio("Método de pago preferido", ["Yape", "Efectivo"])
        
        st.markdown(f"### Total a pagar: S/. {total:.2f}")
        
        # Formateo del mensaje automático para enviar directamente al dueño del Chifa
        mensaje_wa = f"🍜 *CHIFA D' BELINDA*\n\n"
        mensaje_wa += f"👤 *Cliente:* {nombre_cliente}\n"
        mensaje_wa += f"💳 *Pago:* {metodo_pago}\n"
        mensaje_wa += "-------------------------\n"
        for item in st.session_state.carrito:
            mensaje_wa += f"✅ {item['cant']}x {item['nombre']} - S/. {item['precio'] * item['cant']:.2f}\n"
        mensaje_wa += "-------------------------\n"
        mensaje_wa += f"💰 *TOTAL PRODUCTOS:* S/. {total:.2f}"
        
        link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"
        
        st.link_button("📲 ENVIAR MI PEDIDO POR WHATSAPP", link_final, use_container_width=True)
        
        if st.button("🧹 Vaciar Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()