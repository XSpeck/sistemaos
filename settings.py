import streamlit as st
import pandas as pd

def show_settings(manager):
    """Configurações específicas para fibra óptica"""
    st.header("⚙️ Configurações do Sistema")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Clientes", "🔧 Serviços", "👨‍🔧 Técnicos", "📦 Equipamentos"])
    
    with tab1:
        st.subheader("Gerenciar Clientes")
        
        # Adicionar novo cliente
        with st.expander("➕ Adicionar Novo Cliente"):
            with st.form("new_client_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("👤 Nome/Razão Social")
                    phone = st.text_input("📞 Telefone")
                    email = st.text_input("📧 Email")
                with col2:
                    address = st.text_area("📍 Endereço Completo", height=100)
                    cto = st.text_input("🌐 CTO", placeholder="Ex: CTO-001")
                    plan = st.selectbox("📊 Plano", ["50MB", "100MB", "200MB", "300MB", "500MB", "1GB"])
                
                if st.form_submit_button("➕ Adicionar Cliente"):
                    if name and phone and address:
                        new_client = {
                            "name": name,
                            "phone": phone,
                            "email": email,
                            "address": address,
                            "cto": cto,
                            "plan": plan
                        }
                        result = manager.add_client(new_client)
                        if result:
                            st.success("✅ Cliente adicionado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao adicionar cliente")
        
        # Lista de clientes
        clients = manager.get_all_clients()
        if clients:
            clients_df = pd.DataFrame(clients)
            clients_df = clients_df[["name", "phone", "email", "cto", "plan"]]
            clients_df.columns = ["Nome", "Telefone", "Email", "CTO", "Plano"]
            st.dataframe(clients_df, use_container_width=True)
    
    with tab2:
        st.subheader("Gerenciar Tipos de Serviço")
        
        # Adicionar novo serviço
        with st.expander("➕ Adicionar Novo Serviço"):
            with st.form("new_service_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("🔧 Nome do Serviço")
                    service_type = st.selectbox("📋 Categoria", 
                                              ["Instalação", "Reparo", "Manutenção", "Upgrade", "Diagnóstico", "Cancelamento"])
                with col2:
                    price = st.number_input("💰 Preço (R$)", min_value=0.0)
                    duration = st.number_input("⏱️ Duração (horas)", min_value=1, value=2)
                
                if st.form_submit_button("➕ Adicionar Serviço"):
                    if name:
                        new_service = {
                            "name": name,
                            "type": service_type,
                            "price": price,
                            "duration": duration
                        }
                        result = manager.add_service(new_service)
                        if result:
                            st.success("✅ Serviço adicionado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao adicionar serviço")
        
        # Lista de serviços
        services = manager.get_all_services()
        if services:
            services_df = pd.DataFrame(services)
            services_df = services_df[["name", "type", "price", "duration"]]
            services_df.columns = ["Nome", "Categoria", "Preço (R$)", "Duração (h)"]
            st.dataframe(services_df, use_container_width=True)
    
    with tab3:
        st.subheader("Gerenciar Técnicos")
        
        # Adicionar novo técnico
        with st.expander("➕ Adicionar Novo Técnico"):
            with st.form("new_technician_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("👨‍🔧 Nome do Técnico")
                    specialty = st.selectbox("🎯 Especialidade", 
                                           ["Instalação", "Reparo", "Manutenção", "Geral"])
                with col2:
                    region = st.selectbox("🌍 Região", 
                                        ["Centro", "Zona Sul", "Zona Norte", "Zona Oeste", "Zona Leste"])
                    level = st.selectbox("⭐ Nível", ["Júnior", "Pleno", "Sênior"])
                
                if st.form_submit_button("➕ Adicionar Técnico"):
                    if name:
                        new_tech = {
                            "name": name,
                            "specialty": specialty,
                            "region": region,
                            "level": level
                        }
                        result = manager.add_technician(new_tech)
                        if result:
                            st.success("✅ Técnico adicionado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao adicionar técnico")
        
        # Lista de técnicos
        technicians = manager.get_all_technicians()
        if technicians:
            techs_df = pd.DataFrame(technicians)
            techs_df = techs_df[["name", "specialty", "region", "level"]]
            techs_df.columns = ["Nome", "Especialidade", "Região", "Nível"]
            st.dataframe(techs_df, use_container_width=True)
    
    with tab4:
        st.subheader("Gerenciar Equipamentos")
        
        # Adicionar novo equipamento
        with st.expander("➕ Adicionar Novo Equipamento"):
            with st.form("new_equipment_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("📦 Nome do Equipamento")
                    equipment_type = st.selectbox("🔧 Tipo", 
                                                ["ONT", "Router", "Switch", "Splitter", "Cabo", "Conector", "Cordão", "Outros"])
                with col2:
                    price = st.number_input("💰 Preço (R$)", min_value=0.0)
                
                if st.form_submit_button("➕ Adicionar Equipamento"):
                    if name:
                        new_equipment = {
                            "name": name,
                            "type": equipment_type,
                            "price": price
                        }
                        result = manager.add_equipment(new_equipment)
                        if result:
                            st.success("✅ Equipamento adicionado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao adicionar equipamento")
        
        # Lista de equipamentos
        equipment = manager.get_all_equipment()
        if equipment:
            equipment_df = pd.DataFrame(equipment)
            equipment_df = equipment_df[["name", "type", "price"]]
            equipment_df.columns = ["Nome", "Tipo", "Preço (R$)"]
            st.dataframe(equipment_df, use_container_width=True)
    
    # Configurações do sistema
    st.markdown("---")
    st.subheader("🔧 Configurações do Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🗄️ **Banco de Dados**\nConectado ao Supabase")
        if st.button("🔄 Recarregar Dados", help="Recarrega todos os dados do banco"):
            st.rerun()
    
    with col2:
        st.info("📊 **Estatísticas**\nDados em tempo real")
        orders = manager.get_all_orders()
        clients = manager.get_all_clients()
        st.metric("Total de Registros", len(orders) + len(clients))
    
    with col3:
        st.info("🔗 **Integração**\nGoogle Calendar habilitado")
        if st.button("📤 Exportar Relatório", help="Exporta dados para análise"):
            st.info("📋 Funcionalidade em desenvolvimento")