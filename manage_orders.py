import streamlit as st
import pandas as pd

def show_manage_orders(manager):
    """Página para gerenciar ordens de fibra óptica"""
    st.header("🔧 Gerenciar OS - Fibra Óptica")
    
    # Filtros específicos para fibra óptica
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.selectbox("Status", ["Todos", "Agendado", "Em Campo", "Aguardando Peças", "Concluído", "Cancelado"])
    with col2:
        priority_filter = st.selectbox("Prioridade", ["Todas", "Baixa", "Normal", "Alta", "Urgente"])
    with col3:
        service_type_filter = st.selectbox("Tipo", ["Todos", "Instalação", "Reparo", "Manutenção", "Upgrade", "Cancelamento"])
    with col4:
        region_filter = st.selectbox("Região", ["Todas", "Centro", "Zona Sul", "Zona Norte", "Zona Oeste", "Zona Leste"])
    
    # DataFrame das ordens
    df = manager.get_orders_dataframe()
    
    if not df.empty:
        # Aplicar filtros
        if status_filter != "Todos":
            df = df[df["Status"] == status_filter]
        if priority_filter != "Todas":
            df = df[df["Prioridade"] == priority_filter]
        if service_type_filter != "Todos":
            df = df[df["Tipo"] == service_type_filter]
        if region_filter != "Todas":
            df = df[df["Região"] == region_filter]
        
        st.dataframe(df, use_container_width=True)
        
        # Atualização de status
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Atualizar Status da OS")
            if len(df) > 0:
                # Busca aprimorada para seleção de OS
                st.markdown("**🔍 Buscar OS para Atualizar:**")
                
                # Opções de busca
                search_method = st.radio("Método de Busca:", 
                                       ["📋 Por Lista", "🔍 Por Pesquisa", "📱 Por Número"], 
                                       horizontal=True)
                
                selected_order_id = None
                selected_order_display = None
                
                if search_method == "📋 Por Lista":
                    # Lista suspensa tradicional
                    order_options = []
                    for _, row in df.iterrows():
                        display_text = f"{row['OS']} | {row['Cliente']} | {row['Status']} | {row['Data']}"
                        order_options.append(display_text)
                    
                    if order_options:
                        selected_order_display = st.selectbox("Selecionar OS:", order_options)
                        selected_order_id = df[df["OS"] == selected_order_display.split(" | ")[0]]["ID"].iloc[0]
                
                elif search_method == "🔍 Por Pesquisa":
                    # Busca com autocomplete simulado
                    search_term = st.text_input("Digite nome do cliente ou OS:", 
                                              placeholder="Ex: João Silva ou OS123")
                    
                    if search_term:
                        # Filtra opções baseado na busca
                        filtered_df = df[
                            df["Cliente"].str.contains(search_term, case=False, na=False) |
                            df["OS"].str.contains(search_term, case=False, na=False)
                        ]
                        
                        if not filtered_df.empty:
                            search_options = []
                            for _, row in filtered_df.iterrows():
                                display_text = f"{row['OS']} | {row['Cliente']} | {row['Status']} | {row['Data']}"
                                search_options.append(display_text)
                            
                            selected_order_display = st.selectbox("Resultados da Busca:", search_options)
                            selected_order_id = filtered_df[filtered_df["OS"] == selected_order_display.split(" | ")[0]]["ID"].iloc[0]
                        else:
                            st.warning("❌ Nenhuma OS encontrada com este termo")
                
                elif search_method == "📱 Por Número":
                    # Busca direta por número da OS
                    os_number = st.text_input("Número da OS:", placeholder="Ex: OS12345678")
                    
                    if os_number:
                        matching_rows = df[df["OS"] == os_number.upper()]
                        if not matching_rows.empty:
                            row = matching_rows.iloc[0]
                            selected_order_display = f"{row['OS']} | {row['Cliente']} | {row['Status']} | {row['Data']}"
                            selected_order_id = row["ID"]
                            st.success(f"✅ OS encontrada: {row['Cliente']}")
                        else:
                            st.error("❌ OS não encontrada")
                
                # Se uma OS foi selecionada, mostra opções de atualização
                if selected_order_id and selected_order_display:
                    st.markdown("---")
                    st.markdown(f"**📋 OS Selecionada:** `{selected_order_display.split(' | ')[0]}`")
                    st.markdown(f"**👤 Cliente:** {selected_order_display.split(' | ')[1]}")
                    st.markdown(f"**📊 Status Atual:** {selected_order_display.split(' | ')[2]}")
                    
                    # Seleção do novo status
                    current_status = selected_order_display.split(' | ')[2]
                    status_options = ["Agendado", "Em Campo", "Aguardando Peças", "Concluído", "Cancelado"]
                    
                    # Remove o status atual das opções ou destaca
                    new_status = st.selectbox("🔄 Novo Status:", 
                                            status_options,
                                            index=status_options.index(current_status) if current_status in status_options else 0)
                    
                    # Se concluindo, pedir informações adicionais
                    completion_data = {}
                    if new_status == "Concluído":
                        st.markdown("**📊 Dados de Conclusão:**")
                        col_a, col_b = st.columns(2)
                        with col_a:
                            completion_data["signal_level"] = st.text_input("📶 Nível de Sinal Final (dBm)", 
                                                                          placeholder="Ex: -18.5")
                            completion_data["customer_satisfaction"] = st.select_slider("😊 Satisfação do Cliente", 
                                                                                       options=[1, 2, 3, 4, 5], 
                                                                                       value=5,
                                                                                       format_func=lambda x: f"{x} {'⭐' * x}")
                        with col_b:
                            completion_data["observations"] = st.text_area("📋 Observações Finais",
                                                                         height=80,
                                                                         placeholder="Observações sobre o atendimento...")
                            equipment_used_text = st.text_area("📦 Equipamentos Utilizados",
                                                             height=80,
                                                             placeholder="Ex: ONT Nokia, Cabo Drop 50m")
                            completion_data["equipment_used"] = equipment_used_text.split(',') if equipment_used_text else []
                    
                    # Botão de atualização
                    if st.button("🔄 Atualizar Status", type="primary", use_container_width=True):
                        result = manager.update_order_status(selected_order_id, new_status, 
                                                           completion_data if new_status == "Concluído" else None)
                        if result:
                            st.success(f"✅ Status da OS atualizado para: **{new_status}**")
                            if new_status == "Concluído":
                                st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Erro ao atualizar status")
        
        with col2:
            st.subheader("🔍 Detalhes da OS")
            
            # Busca aprimorada para visualização de detalhes
            st.markdown("**🔍 Buscar OS para Ver Detalhes:**")
            
            # Métodos de busca para detalhes
            detail_search_method = st.radio("Método de Busca:", 
                                          ["📋 Lista Completa", "🎯 Busca Rápida", "🔢 Por Número"], 
                                          horizontal=True,
                                          key="detail_search")
            
            detail_order_id = None
            detail_display = None
            
            if detail_search_method == "📋 Lista Completa":
                # Lista com mais informações
                detail_options = []
                for _, row in df.iterrows():
                    status_icon = "🟢" if row['Status'] == "Concluído" else "🟡" if row['Status'] == "Em Campo" else "⚪"
                    priority_icon = "🚨" if row['Prioridade'] == "Urgente" else "🔴" if row['Prioridade'] == "Alta" else "🔵"
                    display_text = f"{status_icon} {priority_icon} {row['OS']} - {row['Cliente']} ({row['Tipo']})"
                    detail_options.append(display_text)
                
                if detail_options:
                    detail_display = st.selectbox("Selecionar OS:", detail_options, key="detail_list")
                    # Extrai o número da OS
                    os_number = detail_display.split(" - ")[0].split(" ")[-1]
    id = df[df["OS"] == detail_order_row.split(" - ")[0]]["ID"].iloc[0]
                
                # Busca dados completos da ordem
                orders = manager.get_all_orders()
                selected_order_data = next((o for o in orders if o["id"] == detail_order_id), None)
                
                if selected_order_data:
                    clients = manager.get_all_clients()
                    services = manager.get_all_services()
                    technicians = manager.get_all_technicians()
                    
                    client = next((c for c in clients if c["id"] == selected_order_data["client_id"]), {})
                    service = next((s for s in services if s["id"] == selected_order_data["service_id"]), {})
                    technician = next((t for t in technicians if t["id"] == selected_order_data["technician_id"]), {})
                    
                    with st.expander(f"📋 Detalhes - {selected_order_data['order_number']}", expanded=True):
                        st.markdown(f"""
                        **🏠 Cliente:** {client.get('name', 'N/A')}
                        **📍 Endereço:** {client.get('address', 'N/A')}
                        **🌐 CTO:** {client.get('cto', 'N/A')}
                        **📊 Plano:** {client.get('plan', 'N/A')}
                        **🔧 Serviço:** {service.get('name', 'N/A')}
                        **👨‍🔧 Técnico:** {technician.get('name', 'N/A')}
                        **🌍 Região:** {technician.get('region', 'N/A')}
                        **📅 Data:** {selected_order_data.get('scheduled_date', 'N/A')}
                        **🕐 Hora:** {selected_order_data.get('scheduled_time', 'N/A')}
                        **⚡ Prioridade:** {selected_order_data.get('priority', 'N/A')}
                        **📊 Status:** {selected_order_data.get('status', 'N/A')}
                        **💰 Valor:** R$ {selected_order_data.get('estimated_cost', 0):.2f}
                        """)
                        
                        if selected_order_data.get('signal_level'):
                            st.markdown(f"**📶 Sinal:** {selected_order_data['signal_level']} dBm")
                        
                        if selected_order_data.get('equipment_used'):
                            equipment_str = ', '.join(selected_order_data['equipment_used']) if isinstance(selected_order_data['equipment_used'], list) else selected_order_data['equipment_used']
                            st.markdown(f"**📦 Equipamentos:** {equipment_str}")
                        
                        st.markdown(f"**📝 Descrição:** {selected_order_data.get('description', 'N/A')}")
                        
                        if selected_order_data.get('observations'):
                            st.markdown(f"**📋 Observações:** {selected_order_data['observations']}")
    else:
        st.info("📝 Nenhuma OS encontrada com os filtros aplicados")id = df[df["OS"] == os_number]["ID"].iloc[0]
            
            elif detail_search_method == "🎯 Busca Rápida":
                # Busca com filtro dinâmico
                detail_search = st.text_input("🔍 Buscar:", placeholder="Cliente, OS, CTO...", key="detail_search_input")
                
                if detail_search:
                    detail_filtered = df[
                        df["Cliente"].str.contains(detail_search, case=False, na=False) |
                        df["OS"].str.contains(detail_search, case=False, na=False) |
                        df["CTO"].str.contains(detail_search, case=False, na=False)
                    ]
                    
                    if not detail_filtered.empty:
                        # Mostra resultados em formato compacto
                        for _, row in detail_filtered.head(5).iterrows():  # Limita a 5 resultados
                            if st.button(f"👁️ {row['OS']} - {row['Cliente']}", key=f"detail_btn_{row['ID']}"):
                                detail_order_id = row["ID"]
                                detail_display = f"{row['OS']} - {row['Cliente']}"
                    else:
                        st.info("🔍 Nenhum resultado encontrado")
            
            elif detail_search_method == "🔢 Por Número":
                # Busca direta por número
                detail_os_number = st.text_input("📱 Número da OS:", placeholder="Ex: OS12345678", key="detail_os_input")
                
                if detail_os_number:
                    detail_match = df[df["OS"] == detail_os_number.upper()]
                    if not detail_match.empty:
                        row = detail_match.iloc[0]
                        detail_order_id = row["ID"]
                        detail_display = f"{row['OS']} - {row['Cliente']}"
                        st.info(f"📋 OS encontrada: {row['Cliente']}")
            
            # Mostra detalhes da OS selecionada
            if detail_order_id:
                # Busca dados completos da ordem
                orders = manager.get_all_orders()
                selected_order_data = next((o for o in orders if o["id"] == detail_order_id), None)
                
                if selected_order_data:
                    clients = manager.get_all_clients()
                    services = manager.get_all_services()
                    technicians = manager.get_all_technicians()
                    
                    client = next((c for c in clients if c["id"] == selected_order_data["client_id"]), {})
                    service = next((s for s in services if s["id"] == selected_order_data["service_id"]), {})
                    technician = next((t for t in technicians if t["id"] == selected_order_data["technician_id"]), {})
                    
                    # Detalhes expandidos
                    with st.container():
                        st.markdown(f"### 📋 {selected_order_data['order_number']}")
                        
                        # Status com cor
                        status = selected_order_data.get('status', 'N/A')
                        if status == "Concluído":
                            st.success(f"✅ **Status:** {status}")
                        elif status == "Em Campo":
                            st.warning(f"🔄 **Status:** {status}")
                        elif status == "Urgente":
                            st.error(f"🚨 **Status:** {status}")
                        else:
                            st.info(f"📊 **Status:** {status}")
                        
                        # Informações em abas
                        tab1, tab2, tab3, tab4 = st.tabs(["👤 Cliente", "🔧 Serviço", "👨‍🔧 Técnico", "📊 Detalhes"])
                        
                        with tab1:
                            st.markdown(f"""
                            **🏠 Nome:** {client.get('name', 'N/A')}
                            **📞 Telefone:** {client.get('phone', 'N/A')}
                            **📧 Email:** {client.get('email', 'N/A')}
                            **📍 Endereço:** {client.get('address', 'N/A')}
                            **🌐 CTO:** {client.get('cto', 'N/A')}
                            **📊 Plano:** {client.get('plan', 'N/A')}
                            """)
                        
                        with tab2:
                            st.markdown(f"""
                            **🔧 Serviço:** {service.get('name', 'N/A')}
                            **📋 Categoria:** {service.get('type', 'N/A')}
                            **⏱️ Duração:** {service.get('duration', 'N/A')} horas
                            **💰 Preço Base:** R$ {service.get('price', 0):.2f}
                            **💰 Custo Total:** R$ {selected_order_data.get('estimated_cost', 0):.2f}
                            """)
                        
                        with tab3:
                            st.markdown(f"""
                            **👨‍🔧 Nome:** {technician.get('name', 'N/A')}
                            **🎯 Especialidade:** {technician.get('specialty', 'N/A')}
                            **🌍 Região:** {technician.get('region', 'N/A')}
                            **⭐ Nível:** {technician.get('level', 'N/A')}
                            """)
                        
                        with tab4:
                            st.markdown(f"""
                            **📅 Data Agendamento:** {selected_order_data.get('scheduled_date', 'N/A')}
                            **🕐 Hora:** {selected_order_data.get('scheduled_time', 'N/A')}
                            **⚡ Prioridade:** {selected_order_data.get('priority', 'N/A')}
                            **📝 Descrição:** {selected_order_data.get('description', 'N/A')}
                            """)
                            
                            if selected_order_data.get('signal_level'):
                                st.markdown(f"**📶 Sinal:** {selected_order_data['signal_level']} dBm")
                            
                            if selected_order_data.get('equipment_used'):
                                equipment_str = ', '.join(selected_order_data['equipment_used']) if isinstance(selected_order_data['equipment_used'], list) else selected_order_data['equipment_used']
                                st.markdown(f"**📦 Equipamentos:** {equipment_str}")
                            
                            if selected_order_data.get('observations'):
                                st.markdown(f"**📋 Observações:** {selected_order_data['observations']}")
                            
                            if selected_order_data.get('completed_at'):
                                st.markdown(f"**✅ Concluído em:** {selected_order_data['completed_at']}")
                            
                            if selected_order_data.get('customer_satisfaction'):
                                satisfaction = selected_order_data['customer_satisfaction']
                                stars = "⭐" * satisfaction
                                st.markdown(f"**😊 Satisfação:** {satisfaction}/5 {stars}")
    else:
        st.info("📝 Nenhuma OS encontrada no sistema")id = df[df["OS"] == detail_order_row.split(" - ")[0]]["ID"].iloc[0]
                
                # Busca dados completos da ordem
                orders = manager.get_all_orders()
                selected_order_data = next((o for o in orders if o["id"] == detail_order_id), None)
                
                if selected_order_data:
                    clients = manager.get_all_clients()
                    services = manager.get_all_services()
                    technicians = manager.get_all_technicians()
                    
                    client = next((c for c in clients if c["id"] == selected_order_data["client_id"]), {})
                    service = next((s for s in services if s["id"] == selected_order_data["service_id"]), {})
                    technician = next((t for t in technicians if t["id"] == selected_order_data["technician_id"]), {})
                    
                    with st.expander(f"📋 Detalhes - {selected_order_data['order_number']}", expanded=True):
                        st.markdown(f"""
                        **🏠 Cliente:** {client.get('name', 'N/A')}
                        **📍 Endereço:** {client.get('address', 'N/A')}
                        **🌐 CTO:** {client.get('cto', 'N/A')}
                        **📊 Plano:** {client.get('plan', 'N/A')}
                        **🔧 Serviço:** {service.get('name', 'N/A')}
                        **👨‍🔧 Técnico:** {technician.get('name', 'N/A')}
                        **🌍 Região:** {technician.get('region', 'N/A')}
                        **📅 Data:** {selected_order_data.get('scheduled_date', 'N/A')}
                        **🕐 Hora:** {selected_order_data.get('scheduled_time', 'N/A')}
                        **⚡ Prioridade:** {selected_order_data.get('priority', 'N/A')}
                        **📊 Status:** {selected_order_data.get('status', 'N/A')}
                        **💰 Valor:** R$ {selected_order_data.get('estimated_cost', 0):.2f}
                        """)
                        
                        if selected_order_data.get('signal_level'):
                            st.markdown(f"**📶 Sinal:** {selected_order_data['signal_level']} dBm")
                        
                        if selected_order_data.get('equipment_used'):
                            equipment_str = ', '.join(selected_order_data['equipment_used']) if isinstance(selected_order_data['equipment_used'], list) else selected_order_data['equipment_used']
                            st.markdown(f"**📦 Equipamentos:** {equipment_str}")
                        
                        st.markdown(f"**📝 Descrição:** {selected_order_data.get('description', 'N/A')}")
                        
                        if selected_order_data.get('observations'):
                            st.markdown(f"**📋 Observações:** {selected_order_data['observations']}")
    else:
        st.info("📝 Nenhuma OS encontrada com os filtros aplicados")
