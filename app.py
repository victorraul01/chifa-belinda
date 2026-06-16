import streamlit as st
import pandas as pd
import urllib.parse
import base64

st.set_page_config(
    page_title="Chifa D' Belinda",
    layout="wide"
)

# -----------------------------
# BASE64
# -----------------------------
def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# -----------------------------
# CARRITO
# -----------------------------
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# -----------------------------
# EXCEL
# -----------------------------
df = pd.read_excel("Catalogo_Productos.xlsx")

# -----------------------------
# PAGINAS
# -----------------------------
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

st.title("🍜 Chifa D' Belinda")

tabs = st.tabs(["📖 Carta", "🛒 Mi Pedido"])

# -----------------------------
# TAB CARTA
# -----------------------------
with tabs[0]:

    pagina_actual = st.selectbox(
        "Selecciona página",
        list(paginas.keys())
    )

    config = paginas[pagina_actual]
    productos = df[df["Category"].isin(config["categorias"])]

    fondo = get_base64(config["imagen"])

    st.markdown(f"""
    <style>
    .contenedor-principal {{
        position: relative;
        width: 100%;
        height: 85vh;
        background-image: url("data:image/jpeg;base64,{fondo}");
        background-size: cover;
        background-position: center;
        border-radius: 15px;
        overflow: hidden;
    }}

    .panel-scroll {{
        position: absolute;
        top: 0;
        right: 0;
        width: 60%;
        height: 100%;
        overflow-y: auto;
        padding: 15px;
    }}

    .categoria {{
        color: yellow;
        font-size: 24px;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 10px;
    }}

    .plato {{
        color: white;
        font-size: 15px;
        font-weight: bold;
    }}

    .precio {{
        color: white;
        font-size: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Fondo completo
    st.markdown(
        '<div class="contenedor-principal">',
        unsafe_allow_html=True
    )

    # Overlay derecho
    st.markdown(
        '<div class="panel-scroll">',
        unsafe_allow_html=True
    )

    for categoria in config["categorias"]:

        grupo = productos[productos["Category"] == categoria]

        if not grupo.empty:

            st.markdown(
                f"<div class='categoria'>{categoria}</div>",
                unsafe_allow_html=True
            )

            for i, row in grupo.iterrows():

                col1, col2, col3 = st.columns([0.55, 0.25, 0.20])

                col1.markdown(
                    f"<div class='plato'>{row['Name']}</div>",
                    unsafe_allow_html=True
                )

                col2.markdown(
                    f"<div class='precio'>S/. {row['Price']}</div>",
                    unsafe_allow_html=True
                )

                if col3.button("➕", key=f"{pagina_actual}_{i}"):

                    st.session_state.carrito.append({
                        "nombre": row["Name"],
                        "precio": row["Price"]
                    })

                    st.toast(f"{row['Name']} agregado")

    st.markdown("</div></div>", unsafe_allow_html=True)

# -----------------------------
# TAB CARRITO
# -----------------------------
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
            "📲 Enviar por WhatsApp",
            f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje)}"
        )

        if st.button("🗑 Limpiar carrito"):
            st.session_state.carrito = []
            st.rerun()