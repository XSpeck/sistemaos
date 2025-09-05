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

    # Busca rápida tipo autocomplete antes da exibição da tabela
    search_term = st.text_input("🔍 Buscar OS, Cliente, CTO...", placeholder="Ex: João, OS123, CTO-001")
    df_display = df.copy()
    if search_term:
        df_display = df_display[
            df_display["OS"].str.contains(search_term, case=False, na=False) |
            df_display["Cliente"].str.contains(search_term, case=False, na=False) |
            df_display["CTO"].str.contains(search_term, case=False, na=False)
        ]

    # Aplicar filtros
    if status_filter != "Todos":
        df_display = df_display[df_display["Status"] == status_filter]
    if priority_filter != "Todas":
        df_display = df_display[df_display["Prioridade"] == priority_filter]
    if service_type_filter != "Todos":
        df_display = df_display[df_display["Tipo"] == service_type_filter]
    if region_filter != "Todas":
        df_display = df_display[df_display["Região"] == region_filter]

    # Exibir tabela SEM a coluna ID
    if not df_display.empty:
        st.dataframe(df_display.drop(columns=["ID"]), use_container_width=True)
    else:
        st.info("📝 Nenhuma OS encontrada com os filtros aplicados ou busca.")

    # Atualização de status
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 Atualizar Status da OS")
        if len(df_display) > 0:
            st.markdown("**🔍 Buscar OS para Atualizar:**")
            search_method = st.radio("Método de Busca:",
                                    ["📋 Por Lista", "🔍 Por Pesquisa", "📱 Por Número"],
                                    horizontal=True)
            selected_order_id = None
            selected_order_display = None

            if search_method == "📋 Por Lista":
                order_options = []
                for _, row in df_display.iterrows():
                    display_text = f"{row['OS']} | {row['Cliente']} | {row['Status']} | {row['Data']}"
                    order_options.append(display_text)
                if order_options:
                    selected_order_display = st.selectbox("Selecionar OS:", order_options)
                    selected_order_id = df_display[df_display["OS"] == selected_order_display.split(" | ")[0]]["ID"].iloc[0]

            elif search_method == "🔍 Por Pesquisa":
                search_term2 = st.text_input("Digite nome do cliente ou OS:", placeholder="Ex: João Silva ou OS123")
                filtered_df2 = df_display.copy()
                if search_term2:
                    filtered_df2 = filtered_df2[
                        filtered_df2["Cliente"].str.contains(search_term2, case=False, na=False) |
                        filtered_df2["OS"].str.contains(search_term2, case=False, na=False)
                    ]
                if not filtered_df2.empty:
                    search_options = []
                    for _, row in filtered_df2.iterrows():
                        display_text = f"{row['OS']} | {row['Cliente']} | {row['Status']} | {row['Data']}"
                        search_options.append(display_text)
                    selected_order_display = st.selectbox("Resultados da Busca:", search_options)
                    selected_order_id = filtered_df2[filtered_df2["OS"] == selected_order_display.split(" | ")[0]]["ID"].iloc[0]
                elif search_term2:
                    st.warning("❌ Nenhuma OS encontrada com este termo")

            elif search_method == "📱 Por Número":
                os_number = st.text_input("Número da OS:", placeholder="Ex: OS12345678")
                if os_number:
                    matching_rows = df_display[df_display["OS"] == os_number.upper()]
                    if not matching_rows.empty:
                        row = matching_rows.iloc[0]
                        selected_order_display = f"{row['OS']} | {row['Cliente']} | {row['Status']} | {row['Data']}"
                        selected_order_id = row["ID"]
                        st.success(f"✅ OS encontrada: {row['Cliente']}")
                    else:
                        st.error("❌ OS não encontrada")

            # Se uma OS foi selecionada, mostra opções de atualização e exclusão
            if selected_order_id and selected_order_display:
                st.markdown("---")
                st.markdown(f"**📋 OS Selecionada:** `{selected_order_display.split(' | ')[0]}`")
                st.markdown(f"**👤 Cliente:** {selected_order_display.split(' | ')[1]}")
                st.markdown(f"**📊 Status Atual:** {selected_order_display.split(' | ')[2]}")

                current_status = selected_order_display.split(' | ')[2]
                status_options = ["Agendado", "Em Campo", "Aguardando Peças", "Concluído", "Cancelado"]
                new_status = st.selectbox("🔄 Novo Status:",
                                          status_options,
                                          index=status_options.index(current_status) if current_status in status_options else 0)

                completion_data = {}
                if new_status == "Concluído":
                    st.markdown("**📊 Dados de Conclusão:**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        completion_data["signal_level"] = st.text_input("📶 Nível de Sinal Final (dBm)", placeholder="Ex: -18.5")
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

                # Botão para excluir OS com confirmação extra
                confirm_delete = st.checkbox("Confirmo que desejo excluir esta OS permanentemente.", value=False)
                if st.button("🗑️ Excluir OS Selecionada", type="secondary", use_container_width=True):
                    if confirm_delete:
                        result = manager.delete_order(selected_order_id)
                        if result:
                            st.success("🗑️ OS excluída com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao excluir OS")
                    else:
                        st.warning("⚠️ Marque a caixa de confirmação para excluir a OS.")

    with col2:
        st.subheader("🔍 Detalhes da OS")
        st.markdown("**🔍 Buscar OS para Ver Detalhes:**")
        detail_search_method = st.radio("Método de Busca:",
                                        ["📋 Lista Completa", "🎯 Busca Rápida", "🔢 Por Número"],
                                        horizontal=True,
                                        key="detail_search")
        detail_order_id = None
        detail_display = None

        if detail_search_method == "📋 Lista Completa":
            detail_options = []
            for _, row in df_display.iterrows():
                status_icon = "🟢" if row['Status'] == "Concluído" else "🟡" if row['Status'] == "Em Campo" else "⚪"
                priority_icon = "🚨" if row['Prioridade'] == "Urgente" else "🔴" if row['Prioridade'] == "Alta" else "🔵"
                display_text = f"{status_icon} {priority_icon} {row['OS']} - {row['Cliente']} ({row['Tipo']})"
                detail_options.append(display_text)
            if detail_options:
                detail_display = st.selectbox("Selecionar OS:", detail_options, key="detail_list")
                os_number = detail_display.split(" - ")[0].split(" ")[-1]
                detail_order_id = df_display[df_display["OS"] == os_number]["ID"].iloc[0]

        elif detail_search_method == "🎯 Busca Rápida":
            detail_search = st.text_input("🔍 Buscar:", placeholder="Cliente, OS, CTO...", key="detail_search_input")
            detail_filtered = df_display.copy()
            if detail_search:
                detail_filtered = detail_filtered[
                    detail_filtered["Cliente"].str.contains(detail_search, case=False, na=False) |
                    detail_filtered["OS"].str.contains(detail_search, case=False, na=False) |
                    detail_filtered["CTO"].str.contains(detail_search, case=False, na=False)
                ]
            if not detail_filtered.empty:
                for _, row in detail_filtered.head(5).iterrows():
                    if st.button(f"👁️ {row['OS']} - {row['Cliente']}", key=f"detail_btn_{row['ID']}"):
                        detail_order_id = row["ID"]
                        detail_display = f"{row['OS']} - {row['Cliente']}"
            elif detail_search:
                st.info("🔍 Nenhum resultado encontrado")

        elif detail_search_method == "🔢 Por Número":
            detail_os_number = st.text_input("📱 Número da OS:", placeholder="Ex: OS12345678", key="detail_os_input")
            if detail_os_number:
                detail_match = df_display[df_display["OS"] == detail_os_number.upper()]
                if not detail_match.empty:
                    row = detail_match.iloc[0]
                    detail_order_id = row["ID"]
                    detail_display = f"{row['OS']} - {row['Cliente']}"
                    st.info(f"📋 OS encontrada: {row['Cliente']}")

        if detail_order_id:
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
                    if selected_order_data.get('completed_at'):
                        st.markdown(f"**✅ Concluído em:** {selected_order_data['completed_at']}")
                    if selected_order_data.get('customer_satisfaction'):
                        satisfaction = selected_order_data['customer_satisfaction']
                        stars = "⭐" * int(satisfaction)
                        st.markdown(f"**😊 Satisfação:** {satisfaction}/5 {stars}")

# Adicione esse método ao seu manager:
# def delete_order(self, order_id):
#     try:
#         result = self.supabase.table('service_orders').delete().eq('id', order_id).execute()
#         return result
#     except Exception as e:
#         st.error(f"Erro ao excluir OS: {e}")
#         return None
