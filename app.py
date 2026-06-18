# PESTAÑA: 📖 PLATOS A LA CARTA
with tab_carta:
    if df_carta.empty:
        st.warning("⚠️ Por favor, carga tu archivo del catálogo.")
    else:
        st.write("")
        categorias_excel = sorted(list(df_carta["Category"].unique()))
        opciones_desplegable = ["✨ Recomendaciones del Día"] + categorias_excel
        
        cat_seleccionada = st.selectbox(
            "🔎 ¿Qué se te antoja hoy? Elige una Categoría:",
            options=opciones_desplegable,
            key="selector_categoria_carta"
        )
        
        st.markdown('<div style="padding: 5px 0px;">', unsafe_allow_html=True)
        
        if cat_seleccionada == "✨ Recomendaciones del Día":
            st.markdown('<div class="titulo-categoria-chifa">🔥 SUGERENCIAS DE LA CASA</div>', unsafe_allow_html=True)
            cats_inicio = ["CHAUFA", "AEROPUERTO", "PLATOS DULCES"]
            df_sugerencias = df_carta[df_carta["Category"].isin(cats_inicio)]
            
            if not df_sugerencias.empty:
                if "indices_aleatorios" not in st.session_state:
                    st.session_state["indices_aleatorios"] = random.sample(range(len(df_sugerencias)), min(6, len(df_sugerencias)))
                
                valid_indices = [i for i in st.session_state["indices_aleatorios"] if i < len(df_sugerencias)]
                df_aleatorio = df_sugerencias.iloc[valid_indices] if valid_indices else df_sugerencias.head(6)
                
                for idx, row in df_aleatorio.iterrows():
                    plato_dict = {"ID": row["ID"], "Name": row["Name"], "Price": row["Price"]}
                    
                    col_izq, col_der = st.columns([0.83, 0.17], gap="small")
                    with col_izq:
                        # Se eliminan espacios al inicio para evitar que Markdown lo confunda con código
                        st.markdown(f"""<div class="contenedor-fila-perfecta-col"><div class="columna-izquierda-info"><span class="texto-nombre-plato">{row["Name"]} <small style="color:#FFEB3B; font-size:9px;">({row["Category"]})</small></span></div><span class="texto-precio-plato">S/. {float(row["Price"]):.2f}</span></div>""", unsafe_allow_html=True)
                    with col_der:
                        st.markdown('<div class="btn-mas-nativo">', unsafe_allow_html=True)
                        st.button("＋", key=f"btn_sug_{row['ID']}_{idx}", on_click=click_agregar_plato, args=(plato_dict, "Carta", row["Category"]))
                        st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('<div class="divisor-plato"></div>', unsafe_allow_html=True)
                    
        else:
            df_filtrado_cat = df_carta[df_carta["Category"] == cat_seleccionada]
            if not df_filtrado_cat.empty:
                for idx, row in df_filtrado_cat.iterrows():
                    plato_dict = {"ID": row["ID"], "Name": row["Name"], "Price": row["Price"]}
                    
                    # EVALUACIÓN EXCLUSIVA PARA LA CATEGORÍA COMBOS
                    desc_html = ""
                    if cat_seleccionada == "COMBOS" and str(row["Description"]).strip():
                        desc_html = f'<span class="texto-descripcion-plato">✨ {row["Description"]}</span>'
                    
                    col_izq, col_der = st.columns([0.83, 0.17], gap="small")
                    with col_izq:
                        # Se reducen los saltos de línea e indentación interna problemática
                        st.markdown(f"""<div class="contenedor-fila-perfecta-col"><div class="columna-izquierda-info"><span class="texto-nombre-plato">{row["Name"]}</span>{desc_html}</div><span class="texto-precio-plato">S/. {float(row["Price"]):.2f}</span></div>""", unsafe_allow_html=True)
                    with col_der:
                        st.markdown('<div class="btn-mas-nativo">', unsafe_allow_html=True)
                        st.button("＋", key=f"btn_carta_{row['ID']}_{idx}", on_click=click_agregar_plato, args=(plato_dict, "Carta", cat_seleccionada))
                        st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('<div class="divisor-plato"></div>', unsafe_allow_html=True)
                    
        st.markdown('</div>', unsafe_allow_html=True)
