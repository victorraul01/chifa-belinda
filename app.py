import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Chifa D' Belinda", layout="wide")

# Estado carrito
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# Cargar catálogo Excel
df = pd.read_excel("Catalogo_Productos.xlsx")

# Relación de páginas
paginas = {
    "Página 1": {
        "imagen": "pag2.jpg",
        "categorias": ["COMBOS", "ALITAS REBOZADAS", "ALITAS ESPECIALES", "BROASTER"]
    },
    "Página 2": {
        "imagen": "pag3.jpg",
        "categorias": ["SOPAS", "CHAUFAS"]
    },
    "Página 3": {
        "imagen": "pag4.jpg",
        "categorias": ["AEROPUERTO", "COMBINADOS", "LOMOS SALTADOS"]
    },
    "Página 4": {
        "imagen": "pag5.jpg",
        "categorias": ["TALLARINES SALTADOS", "PLATOS SALADOS", "PLATOS DULCES", "TORTILLAS"]
    },
    "Página 5": {
        "imagen": "pag6.jpg",
        "categorias": ["ENROLLADOS", "TAYPA", "RES", "LANGOSTINOS", "PATO", "CHICHARRONES"]
    },
    "Página 6": {
        "imagen": "pag7.jpg",
        "categorias": ["CHANCHO", "COSTILLAS", "PORCIONES", "BEBIDAS CALIENTES", "BEBIDAS FRÍAS"]
    }
}

st.title("🍜 Chifa D' Belinda")

tabs = st.tabs([
    "📖 Carta",
    "🛒 Mi Pedido"
])

with tabs[0]:

    pagina_actual = st.selectbox("Selecciona una página", list(paginas.keys()))

    config = paginas[pagina_actual]
    categorias_actuales = config["categorias"]

    productos = df[df["Category"].isin(categorias_actuales)]

    col1, col2 = st.columns([1, 2])

    # Imagen fija
    with col1:
        st.image(config["imagen"], use_container_width=True)

    # Lista scroll
    with col2:
        st.markdown("""
        <style>
        .scroll-area{
            height:900px;
            overflow-y:auto;
            background:#9b1111;
            padding:20px;
            border-radius:10px;
        }
        .categoria{
            color:yellow;
            font-size:28px;
            font-weight:bold;
            margin-top:20px;
            margin-bottom:10px;
        }
        .plato{
            color:white;
            font-size:20px;
            font-weight:bold;
        }
        .precio{
            color:white;
            font-size:18px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="scroll-area">', unsafe_allow_html=True)

        for categoria in categorias_actuales:

            grupo = productos[productos["Category"] == categoria]

            if not grupo.empty:

                st.markdown(
                    f"<div class='categoria'>{categoria}</div>",
                    unsafe_allow_html=True
                )

                for i, row in grupo.iterrows():

                    c1, c2, c3 = st.columns([0.65, 0.2, 0.15])

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

with tabs[1]:

    st.subheader("🛒 Mi Pedido")

    if not st.session_state.carrito:
        st.write("Tu carrito está vacío.")
    else:

        total = 0

        for item in st.session_state.carrito:
            st.write(f"✅ {item['nombre']} - S/. {item['precio']}")
            total += item["precio"]

        st.markdown(f"### Total: S/. {total}")

        detalle = "\n".join(
            [f"- {item['nombre']}: S/. {item['precio']}" for item in st.session_state.carrito]
        )

        mensaje = f"Hola, quiero realizar este pedido:\n{detalle}\n\nTotal: S/. {total}"

        st.link_button(
            "📲 Enviar a WhatsApp",
            f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje)}"
        )

        if st.button("Limpiar carrito"):
            st.session_state.carrito = []
            st.rerun()