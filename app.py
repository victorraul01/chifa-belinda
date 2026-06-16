import streamlit as st
import pandas as pd
import urllib.parse
import base64

st.set_page_config(
    page_title="Chifa D' Belinda",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# FUNCIÓN BASE64
# -----------------------------
def get_base64(imagen):
    with open(imagen, "rb") as f:
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
# PÁGINAS
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

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"]{
    overflow:hidden !important;
}

.main .block-container{
    padding:0rem;
    max-width:100%;
}

.left-panel{
    position:fixed;
    top:60px;
    left:0;
    width:38%;
    height:calc(100vh - 60px);
    z-index:1;
}

.right-panel{
    position:fixed;
    top:60px;
    right:0;
    width:62%;
    height:calc(100vh - 60px);
    overflow-y:auto;
    padding:15px;
    z-index:2;
}

.categoria{
    color:yellow;
    font-size:22px;
    font-weight:bold;
    margin-top:15px;
}

.plato{
    color:white;
    font-size:15px;
    font-weight:bold;
}

.precio{
    color:white;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# APP
# -----------------------------
st.title("🍜 Chifa D' Belinda")

tabs = st.tabs(["📖 Carta", "🛒 Mi Pedido"])

# -----------------------------
# CARTA
# -----------------------------
with tabs[0]:

    pagina_actual = st.selectbox(
        "Selecciona página",
        list(paginas.keys())
    )

    config = paginas[pagina_actual]
    productos = df[df["Category"].isin(config["categorias"])]

    img_base64 = get_base64(config["imagen"])

    # Imagen fija izquierda
    st.markdown(
        f"""
        <div class="left-panel">
            <img src="data:image/jpeg;base64,{img_base64}" 
                 style="width:100%;height:100%;object-fit:cover;">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Contenedor derecho
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)

    for categoria in config["categorias"]:

        grupo = productos[productos["Category"] == categoria]

        if not grupo.empty:

            st.markdown(
                f"<div class='categoria'>{categoria}</div>",
                unsafe_allow_html=True
            )

            for i, row in grupo.iterrows():

                c1, c2, c3 = st.columns([0.55, 0.25, 0.20])

                c1.markdown(
                    f"<div class='plato'>{row['Name']}</div>",
                    unsafe_allow_html=True
                )

                c2.markdown(
                    f"<div class='precio'>S/. {row['Price']}</div>",
                    unsafe_allow_html=True
                )

                if c3.button("➕", key=f"{pagina_actual}_{i}"):

                    st.session_state.carrito.append({
                        "nombre": row["Name"],
                        "precio": row["Price"]
                    })

                    st.toast(f"{row['Name']} agregado")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# CARRITO
# -----------------------------
with tabs[1]:

    st.subheader("Mi Pedido")

    if not st.session_state.carrito:
        st.write("Tu carrito está vacío")

    else:

        total = 0

        for item in st.session_state.carrito:
            st.write(f"✅ {item['nombre']} - S/. {item['precio']}")
            total += item["precio"]

        st.markdown(f"### Total: S/. {total}")

        detalle = "\n".join(
            [f"- {x['nombre']}: S/. {x['precio']}" for x in st.session_state.carrito]
        )

        mensaje = f"Hola, quiero pedir:\n{detalle}\n\nTotal: S/. {total}"

        st.link_button(
            "📲 Enviar por WhatsApp",
            f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje)}"
        )

        if st.button("Limpiar carrito"):
            st.session_state.carrito = []
            st.rerun()