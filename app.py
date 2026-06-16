import streamlit as st
import pandas as pd
import urllib.parse
import base64

# --------------------------------
# CONFIGURACIÓN
# --------------------------------
st.set_page_config(
    page_title="Chifa D' Belinda",
    layout="wide"
)

# --------------------------------
# FUNCIÓN PARA IMAGEN BASE64
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
# CARGAR EXCEL
# --------------------------------
df = pd.read_excel("Catalogo_Productos.xlsx")

# --------------------------------
# CONFIGURACIÓN DE PÁGINAS
# --------------------------------
paginas = {
    "Página 1": {
        "imagen": "pag2.jpg",
        "categorias": [
            "COMBOS",
            "ALITAS REBOZADAS",
            "ALITAS ESPECIALES",
            "BROASTER"
        ]
    },
    "Página 2": {
        "imagen": "pag3.jpg",
        "categorias": [
            "SOPAS",
            "CHAUFAS"
        ]
    },
    "Página 3": {
        "imagen": "pag4.jpg",
        "categorias": [
            "AEROPUERTO",
            "COMBINADOS",
            "LOMOS SALTADOS"
        ]
    },
    "Página 4": {
        "imagen": "pag5.jpg",
        "categorias": [
            "TALLARINES SALTADOS",
            "PLATOS SALADOS",
            "PLATOS DULCES",
            "TORTILLAS"
        ]
    },
    "Página 5": {
        "imagen": "pag6.jpg",
        "categorias": [
            "ENROLLADOS",
            "TAYPA",
            "RES",
            "LANGOSTINOS",
            "PATO",
            "CHICHARRONES"
        ]
    },
    "Página 6": {
        "imagen": "pag7.jpg",
        "categorias": [
            "CHANCHO",
            "COSTILLAS",
            "PORCIONES",
            "BEBIDAS CALIENTES",
            "BEBIDAS FRÍAS"
        ]
    }
}

# --------------------------------
# HEADER FIJO + ESTILOS
# --------------------------------
st.markdown("""
<style>
/* Fondo general */
.stApp {
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Header fijo */
.header-fijo {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    padding: 10px 15px;
    z-index: 999;
}

/* Espacio del header */
.espacio-header {
    height: 80px;
}

/* Panel derecho */
.panel-derecho {
    margin-left: 42%;
    width: 58%;
    height: 72vh;
    overflow-y: auto;
    padding: 8px;
}

/* Categorías */
.categoria {
    color: yellow;
    font-size: 17px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 5px;
}

/* Nombre */
.nombre-plato {
    color: white;
    font-size: 13px;
    font-weight: bold;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Precio */
.precio {
    color: white;
    font-size: 13px;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

# Header fijo
st.markdown("""
<div class="header-fijo">
    <h2 style="margin:0;color:white;">🍜 Chifa D' Belinda</h2>
</div>
<div class="espacio-header"></div>
""", unsafe_allow_html=True)

# Tabs
tabs = st.tabs(["📖 Carta", "🛒 Mi Pedido"])

# --------------------------------
# TAB CARTA
# --------------------------------
with tabs[0]:

    pagina_actual = st.selectbox(
        "Selecciona página",
        list(paginas.keys())
    )

    config = paginas[pagina_actual]
    productos = df[df["Category"].isin(config["categorias"])]

    fondo = get_base64(config["imagen"])

    # Fondo dinámico por página
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{fondo}");
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="panel-derecho">', unsafe_allow_html=True)

    for categoria in config["categorias"]:

        grupo = productos[
            productos["Category"] == categoria
        ]

        if not grupo.empty:

            st.markdown(
                f"<div class='categoria'>{categoria}</div>",
                unsafe_allow_html=True
            )

            for i, row in grupo.iterrows():

                col1, col2, col3 = st.columns(
                    [0.65, 0.20, 0.15],
                    vertical_alignment="center"
                )

                col1.markdown(
                    f"<div class='nombre-plato'>{row['Name']}</div>",
                    unsafe_allow_html=True
                )

                col2.markdown(
                    f"<div class='precio'>S/. {row['Price']}</div>",
                    unsafe_allow_html=True
                )

                if col3.button(
                    "➕",
                    key=f"{pagina_actual}_{i}"
                ):
                    st.session_state.carrito.append({
                        "nombre": row["Name"],
                        "precio": row["Price"]
                    })

                    st.toast(
                        f"{row['Name']} agregado"
                    )

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

        st.markdown(
            f"### Total: S/. {total}"
        )

        detalle = "\n".join([
            f"- {x['nombre']}: S/. {x['precio']}"
            for x in st.session_state.carrito
        ])

        mensaje = (
            f"Hola, quiero realizar este pedido:\n"
            f"{detalle}\n\n"
            f"Total: S/. {total}"
        )

        st.link_button(
            "📲 Enviar pedido por WhatsApp",
            f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje)}"
        )

        if st.button("🗑 Limpiar carrito"):
            st.session_state.carrito = []
            st.rerun()