# =========================================================
# PESTAÑA 2: MI PEDIDO (CARRITO OPTIMIZADO PARA MÓVILES)
# =========================================================
with tab_pedido:
    st.markdown('<div style="padding: 10px 5px; margin-top: 15px;">', unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.markdown('<h3 style="color: white; text-shadow: 2px 2px 2px black;">Tu carrito está vacío. ¡Explora la carta!</h3>', unsafe_allow_html=True)
    else:
        st.markdown('<h2 style="color: #FFEB3B; text-shadow: 2px 2px 3px black; font-size:22px;">📋 Resumen Total del Pedido</h2>', unsafe_allow_html=True)
        total = 0

        for idx, item in enumerate(st.session_state.carrito):
            subtotal = item["precio"] * item["cant"]
            total += subtotal

            detalles_lista = []
            if item['cremas']:
                detalles_lista.append(f"🧂 {item['cremas']}")
            if item['notas']:
                detalles_lista.append(f"📝 {item['notas']}")
            
            detalles_html = ""
            if detalles_lista:
                texto_detalles = " | ".join(detalles_lista)
                detalles_html = f'<span class="texto-detalles-resaltados">{texto_detalles}</span>'

            st.markdown(f"""
            <div class="fila-carrito-ordenada">
                <div class="linea-principal-carrito">
                    <span style="display: flex; align-items: center;">
                        <a href="?eliminar_idx={idx}" target="_self" class="btn-tacho-mini">🗑️</a>
                        <span class="texto-plato-carrito">💥 {item['cant']}x {item['nombre']}</span>
                    </span>
                    <span class="texto-precio-carrito">S/. {subtotal:.2f}</span>
                </div>
                {detalles_html}
            </div>
            """, unsafe_allow_html=True)

        # TOTAL DEL PEDIDO
        st.markdown(f"""
        <div class="recuadro-total-final">
            <span style="color: #FFFFFF; font-size: 17px; font-weight: bold; text-shadow: 1px 1px 2px #000000;">💵 TOTAL DEL PEDIDO:</span>
            <span style="color: #FFEB3B; font-size: 20px; font-weight: 900; text-shadow: 1px 1px 3px #000000;">S/. {total:.2f}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Formulario de Envío
        st.markdown('<span style="color: white; font-weight: bold; text-shadow: 1px 1px 2px black; font-size: 16px;">Ingresa tu Nombre Completo:</span>', unsafe_allow_html=True)
        nombre_cliente = st.text_input("", label_visibility="collapsed", key="nom_cli")
        
        st.write("")
        st.markdown('<span style="color: white; font-weight: bold; text-shadow: 1px 1px 2px black; font-size: 16px;">Método de Entrega:</span>', unsafe_allow_html=True)
        metodo_entrega = st.radio("", ["Delivery Moto 🏍️", "Recojo en Local 🏪"], horizontal=True, label_visibility="collapsed", key="met_ent")

        direccion_cliente = ""
        if metodo_entrega == "Delivery Moto 🏍️":
            st.write("")
            st.markdown('<span style="color: white; font-weight: bold; text-shadow: 1px 1px 2px black; font-size: 14px;">Dirección de Envío:</span>', unsafe_allow_html=True)
            direccion_cliente = st.text_input("", placeholder="Ej: Av. Perú 123, dpto 402...", label_visibility="collapsed", key="dir_cli")
            
            st.markdown("""
            <div class="alerta-delivery-destacada">
                🚨 <span style="color: #FFEB3B; font-weight: bold; font-size: 15px;">¡AVISO IMPORTANTE DE DELIVERY!</span><br>
                1️⃣ Después de enviar el mensaje, <b>compártenos tu ubicación actual por WhatsApp</b> para que el motorizado llegue rápido.<br>
                2️⃣ <b>Costo de envío:</b> Se calculará y te lo enviaremos inmediatamente después de recibir tu lista de platos.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alerta-delivery-destacada" style="border-color: #4CAF50;">
                🏪 <span style="color: #4CAF50; font-weight: bold; font-size: 15px;">PEDIDO PARA RECOJO EN LOCAL</span><br>
                ⏳ Su comida estará lista y empacada con cuidado en aproximadamente <b>20 a 30 minutos</b>. ¡Te esperamos!
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown('<span style="color: white; font-weight: bold; text-shadow: 1px 1px 2px black; font-size: 16px;">Método de Pago:</span>', unsafe_allow_html=True)
        metodo_pago = st.radio("", ["Yape 📱", "Efectivo 💵"], horizontal=True, label_visibility="collapsed", key="met_pag")

        st.write("")
        
        # Estilos CSS extra específicos insertados directo para forzar el color verde en cualquier teléfono
        st.markdown("""
        <style>
        div.stButton > button {
            background-color: #25D366 !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 16px !important;
            border-radius: 8px !important;
            height: 50px !important;
            border: none !important;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.3) !important;
        }
        div.stButton > button p {
            color: white !important;
            font-weight: bold !important;
        }
        .boton-whatsapp-celular {
            display: block !important;
            background-color: #25D366 !important;
            color: white !important;
            text-align: center !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 12px 20px !important;
            border-radius: 8px !important;
            text-decoration: none !important;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.4) !important;
            margin: 15px 0px !important;
            border: 2px solid #ffffff !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # Botón inicial para procesar la información
        click_enviar = st.button("🔄 PROCESAR DATOS DEL PEDIDO", use_container_width=True)

        if click_enviar:
            # Comprobación estricta de campos obligatorios
            if not nombre_cliente.strip():
                st.error("⚠️ No se puede procesar el pedido: Por favor, ingresa tu Nombre Completo.")
            elif metodo_entrega == "Delivery Moto 🏍️" and not direccion_cliente.strip():
                st.error("⚠️ No se puede procesar el pedido: Seleccionaste Delivery Moto, debes ingresar una Dirección de Envío.")
            else:
                # Construcción del mensaje limpio para WhatsApp
                mensaje_wa = f"🍜 *CHIFA D' BELINDA*\n\n"
                mensaje_wa += f"👤 *Cliente:* {nombre_cliente}\n"
                mensaje_wa += f"🛵 *Entrega:* {metodo_entrega}\n"
                if metodo_entrega == "Delivery Moto 🏍️": 
                    mensaje_wa += f"📍 *Dirección:* {direccion_cliente.strip()}\n"
                mensaje_wa += f"💳 *Pago:* {metodo_pago}\n"
                mensaje_wa += f"-------------------------\n"
                
                for item in st.session_state.carrito:
                    mensaje_wa += f"✅ {item['cant']}x {item['nombre']} - S/. {item['precio'] * item['cant']:.2f}\n"
                    detalles_wa = []
                    if item['cremas']: detalles_wa.append(f"{item['cremas']}")
                    if item['notas']: detalles_wa.append(f"{item['notas']}")
                    if detalles_wa:
                        mensaje_wa += f"  • {" | ".join(detalles_wa)}\n"
                
                mensaje_wa += f"-------------------------\n"
                mensaje_wa += f"💰 *TOTAL A PAGAR:* S/. {total:.2f}\n"
                if metodo_entrega == "Delivery Moto 🏍️": 
                    mensaje_wa += f"ℹ️ _El costo de delivery se sumará en breve._"

                # Link optimizado para que los navegadores móviles lo abran nativamente sin bloqueos
                link_final = f"https://wa.me/51923860158?text={urllib.parse.quote(mensaje_wa)}"
                
                st.success("🎯 ¡Datos validados con éxito!")
                # Renderizamos un elemento HTML nativo que el celular JAMÁS bloqueará al pulsar
                st.markdown(f"""
                    <a href="{link_final}" target="_blank" class="boton-whatsapp-celular">
                        📲 PRESIONA AQUÍ PARA ENVIAR A WHATSAPP
                    </a>
                """, unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="boton-normal-ancho">', unsafe_allow_html=True)
        if st.button("🧹 Vaciar Todo el Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)