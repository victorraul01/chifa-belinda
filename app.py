import streamlit as st
import pandas as pd
import urllib.parse
import base64

# --------------------------------
# CONFIG
# --------------------------------
st.set_page_config(
    page_title="Chifa D' Belinda",
    layout="wide"
)

# --------------------------------
# BASE64
# --------------------------------
def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --------------------------------
# CARRITO
# --------------------------------
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# --------------------------------
# EXCEL
# --------------------------------
df = pd.read_excel("Catalogo_Productos.xlsx")

# --------------------------------
# PAGINAS
# --------------------------------
paginas = {
    "Página 1": {
        "imagen": "pag2.jpg",
        "categorias": ["COMBOS","ALITAS REBOZADAS","ALITAS ESPECIALES","BROASTER"]
    },
    "Página 2": {
        "imagen": "pag3.jpg",
        "categorias": ["SOPAS","CHAUFAS"]
    },
    "Página 3": {
        "imagen": "pag4.jpg",
        "categorias": ["AEROPUERTO","COMBINADOS","LOMOS SALTADOS"]
    },
    "Página 4": {
        "imagen": "pag5.jpg",
        "categorias": ["TALLARINES SALTADOS","PLATOS SALADOS","PLATOS DULCES","TORTILLAS"]
    },
    "Página 5": {
        "imagen": "pag6.jpg",
        "categorias": ["ENROLLADOS","TAYPA","RES","LANGOSTINOS","PATO","CHICHARRONES"]
    },
    "Página 6": {
        "imagen": "pag7.jpg",
        "categorias": ["CHANCHO","COSTILLAS","PORCIONES","BEBIDAS CALIENTES","BEBIDAS FRÍAS"]
    }
}

# --------------------------------
# SELECTOR PAGINA
# --------------------------------
pagina_actual = st.selectbox(
    "Selecciona página",
    list(paginas.keys())
)

config = paginas[pagina_actual]
productos = df[df["Category"].isin(config["categorias"])]

fondo = get_base64(config["imagen"])

# --------------------------------
# CSS GLOBAL
# --------------------------------
st.markdown(f"""
<style>
html, body {{
    overflow: hidden !important;
}}

.stApp {{
    background-image: url("data:image/jpeg;base64,{fondo}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

header[data-testid="stHeader"] {{
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
}}

.main .block-container {{
    padding-top: 80px;
    max-width: 100%;
}}

.panel-derecho {{
    margin-left: 45%;
    width: 52%;
    height: 75vh;
    overflow-y: auto;
    padding: 5px;
}}

.categoria {{
    color: yellow;
    font-size: 15px;
    font-weight: bold;
    margin-top: 8px;
    margin-bottom: 4px;
}}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# HEADER
# --------------------------------
st.markdown("""
<h2 style="color:white; margin-bottom:10px;">
🍜 Chifa D' Belinda
</h2>
""", unsafe_allow_html=True)

tabs = st.tabs(["📖 Carta", "🛒 Pedido"])

# --------------------------------
# TAB CARTA
# --------------------------------
with tabs[0]:

    st.markdown('<div class="panel-derecho">', unsafe_allow_html=True)

    for categoria in config["categorias"]:

        grupo = productos[productos["Category"] == categoria]

        if not grupo.empty:

            st.markdown(
                f"<div class='categoria'>{categoria}</div>",
                unsafe_allow_html=True
            )

            for i, row in grupo.iterrows():

                # Más compactos y juntos
                c1, c2, c3 = st.columns([0.70, 0.18, 0.12])

                c1.markdown(
                    f"""
                    <div style="
                    color:white;
                    font-size:12px;
                    white-space:nowrap;
                    overflow:hidden;
                    text-overflow:ellipsis;">
                    {row['Name']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                c2.markdown(
                    f"""
                    <div style="
                    color:white;
                    font-size:12px;
                    text-align:right;">
                    S/. {row['Price']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if c3.button("➕", key=f"{pagina_actual}_{i}"):

                    st.session_state.carrito.append({
                        "nombre": row["Name"],
                        "precio": row["Price"]
                    })

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------
# TAB PEDIDO
# --------------------------------
with tabs[1]:

    st.subheader("🛒 Mi Pedido")

    if not st.session_state.carrito:
        st.write("Tu carrito está vacío")

    else:
        total = 0

        for item in st.session_state.carrito:
            st.write(
                f"✅ {item['nombre']} - S/. {item['precio']}"
            )
            total += item["precio"]

        st.markdown(f"### Total: S/. {total}")

        detalle = "\n".join([
            f"- {x['nombre']}: S/. {x['precio']}"
            for x in st.session_state.carrito
        ])

        mensaje = f"Hola, quiero pedir:\n{detalle}\n\nTotal: S/. {total}"

        st.link_button(
            "📲 Enviar pedido",
            f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje)}"
        )

        if st.button("🗑 Limpiar carrito"):
            st.session_state.carrito = []
            st.rerun()