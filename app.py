import streamlit as st
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import json
import uuid
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go

# Configurações da página
st.set_page_config(
    page_title="Sistema de OS - Fibra Óptica",
    page_icon="🌐",
    layout="wide"
)

# Classe para gerenciar ordens de serviço de fibra óptica
class FiberOpticServiceManager:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Inicializa o estado da sessão com dados específicos de fibra óptica"""
        if 'service_orders' not in st.session_state:
            st.session_state.service_orders = []
        
        if 'clients' not in st.session_state:
            st.session_state.clients = [
                {"id": "1", "name": "João Silva", "phone": "(11) 99999-1111", "email": "joao@email.com", 
                 "address": "Rua das Flores, 123 - Vila Madalena", "cto": "CTO-001", "plan": "100MB"},
                {"id": "2", "name": "Empresa ABC Ltda", "phone": "(11) 99999-2222", "email": "contato@abc.com", 
                 "address": "Av. Paulista, 1000 - Bela Vista", "cto": "CTO-002", "plan": "500MB"},
                {"id": "3", "name": "Maria Santos", "phone": "(11) 99999-3333", "email": "maria@email.com", 
                 "address": "Rua Augusta, 456 - Consolação", "cto": "CTO-003", "plan": "200MB"}
            ]
        
        if 'services' not in st.session_state:
            st.session_state.services = [
                {"id": "1", "name": "Instalação Residencial", "price": 0.00, "duration": 3, "type": "Instalação"},
                {"id": "2", "name": "Instalação Empresarial", "price": 0.00, "duration": 4, "type": "Instalação"},
                {"id": "3", "name": "Reparo de Cabo Rompido", "price": 150.00, "duration": 2, "type": "Reparo"},
                {"id": "4", "name": "Troca de Equipamento ONT", "price": 80.00, "duration": 1, "type": "Manutenção"},
                {"id": "5", "name": "Mudança de Endereço", "price": 100.00, "duration": 3, "type": "Mudança"},
                {"id": "6", "name": "Upgrade de Plano", "price": 0.00, "duration": 1, "type": "Upgrade"},
                {"id": "7", "name": "Reparo em CTO", "price": 200.00, "duration": 4, "type": "Reparo"},
                {"id": "8", "name": "Verificação de Sinal", "price": 50.00, "duration": 1, "type": "Diagnóstico"},
                {"id": "9", "name": "Emenda de Fibra", "price": 120.00, "duration": 2, "type": "Reparo"},
                {"id": "10", "name": "Cancelamento", "price": 0.00, "duration": 1, "type": "Cancelamento"}
            ]
        
        if 'technicians' not in st.session_state:
            st.session_state.technicians = [
                {"id": "1", "name": "Carlos Fibra", "specialty": "Instalação", "region": "Zona Sul", "level": "Sênior"},
                {"id": "2", "name": "Ana Conecta", "specialty": "Reparo", "region": "Centro", "level": "Pleno"},
                {"id": "3", "name": "Roberto Rede", "specialty": "Manutenção", "region": "Zona Norte", "level": "Júnior"},
                {"id": "4", "name": "Mariana Link", "specialty": "Instalação", "region": "Zona Oeste", "level": "Sênior"},
                {"id": "5", "name": "Pedro Optical", "specialty": "Reparo", "region": "Zona Leste", "level": "Pleno"}
            ]
        
        if 'equipment' not in st.session_state:
            st.session_state.equipment = [
                {"id": "1", "name": "ONT Huawei HG8010H", "type": "ONT", "price": 150.00},
                {"id": "2", "name": "ONT Nokia G-010G-A", "type": "ONT", "price": 120.00},
                {"id": "3", "name": "Router Wi-Fi AC1200", "type": "Router", "price": 200.00},
                {"id": "4", "name": "Splitter 1x8", "type": "Splitter", "price": 25.00},
                {"id": "5", "name": "Cabo Drop 100m", "type": "Cabo", "price": 80.00},
                {"id": "6", "name": "Conector SC/APC", "type": "Conector", "price": 5.00},
                {"id": "7", "name": "Cordão Óptico 3m", "type": "Cordão", "price": 15.00}
            ]
    
    def generate_id(self):
        """Gera um ID único"""
        return str(uuid.uuid4())[:8].upper()
    
    def create_service_order(self, order_data: Dict):
        """Cria uma nova ordem de serviço"""
        order = {
            "id": f"OS{self.generate_id()}",
            "client_id": order_data["client_id"],
            "service_id": order_data["service_id"],
            "technician_id": order_data["technician_id"],
            "scheduled_date": order_data["scheduled_date"].strftime("%Y-%m-%d"),
            "scheduled_time": order_data["scheduled_time"].strftime("%H:%M"),
            "description": order_data["description"],
            "status": "Agendado",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "priority": order_data["priority"],
            "estimated_cost": order_data["estimated_cost"],
            "equipment_used": order_data.get("equipment_used", []),
            "signal_level": order_data.get("signal_level", ""),
            "observations": order_data.get("observations", ""),
            "region": order_data.get("region", ""),
            "cto_reference": order_data.get("cto_reference", "")
        }
        st.session_state.service_orders.append(order)
        return order
    
    def update_order_status(self, order_id: str, new_status: str, completion_data: Dict = None):
        """Atualiza o status de uma ordem"""
        for order in st.session_state.service_orders:
            if order["id"] == order_id:
                order["status"] = new_status
                if new_status == "Concluído" and completion_data:
                    order["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    order["signal_level"] = completion_data.get("signal_level", "")
                    order["equipment_used"] = completion_data.get("equipment_used", [])
                    order["observations"] = completion_data.get("observations", "")
                    order["customer_satisfaction"] = completion_data.get("customer_satisfaction", "")
                break
    
    def get_orders_dataframe(self):
        """Retorna DataFrame com as ordens enriquecidas"""
        if not st.session_state.service_orders:
            return pd.DataFrame()
        
        orders = []
        for order in st.session_state.service_orders:
            # Busca informações do cliente
            client = next((c for c in st.session_state.clients if c["id"] == order["client_id"]), {})
            # Busca informações do serviço
            service = next((s for s in st.session_state.services if s["id"] == order["service_id"]), {})
            # Busca informações do técnico
            technician = next((t for t in st.session_state.technicians if t["id"] == order["technician_id"]), {})
            
            orders.append({
                "OS": order["id"],
                "Cliente": client.get("name", "N/A"),
                "Serviço": service.get("name", "N/A"),
                "Tipo": service.get("type", "N/A"),
                "Técnico": technician.get("name", "N/A"),
                "Região": technician.get("region", "N/A"),
                "Data": order["scheduled_date"],
                "Hora": order["scheduled_time"],
                "Status": order["status"],
                "Prioridade": order["priority"],
                "CTO": client.get("cto", "N/A"),
                "Plano": client.get("plan", "N/A"),
                "Valor": f"R$ {order['estimated_cost']:.2f}",
                "Sinal (dBm)": order.get("signal_level", "-")
            })
        
        return pd.DataFrame(orders)

# Classe para integração com Google Agenda (específica para fibra óptica)
class FiberOpticCalendarIntegration:
    @staticmethod
    def create_calendar_event(order_data: Dict):
        """Simula criação de evento no Google Agenda para serviços de fibra óptica"""
        event_details = {
            "title": f"OS: {order_data['service_name']} - {order_data['client_name']}",
            "description": f"""Ordem de Serviço #{order_data['id']}
Tipo: {order_data['service_type']}
Cliente: {order_data['client_name']}
Endereço: {order_data.get('address', 'N/A')}
CTO: {order_data.get('cto', 'N/A')}
Plano: {order_data.get('plan', 'N/A')}
Técnico: {order_data['technician_name']}
Região: {order_data.get('region', 'N/A')}
Descrição: {order_data['description']}""",
            "start_time": f"{order_data['scheduled_date']} {order_data['scheduled_time']}",
            "duration": order_data.get('duration', 2),
            "attendees": [order_data.get('client_email', ''), order_data.get('technician_email', '')]
        }
        return {"status": "success", "event_id": f"cal_{order_data['id']}", "details": event_details}

def main():
    st.title("🌐 Sistema de OS - Fibra Óptica")
    st.markdown("**Sistema de Gestão de Ordens de Serviço para Técnicos de Fibra Óptica**")
    st.markdown("---")
    
    # Inicializa o gerenciador
    manager = FiberOpticServiceManager()
    
    # Sidebar para navegação
    st.sidebar.title("🔧 Navegação")
    st.sidebar.markdown("**Fibra Óptica OS**")
    page = st.sidebar.selectbox(
        "Selecione uma página",
        ["📊 Dashboard", "📝 Nova OS", "🔧 Gerenciar OS", "📅 Calendário", "📈 Relatórios", "⚙️ Configurações"]
    )
    
    # Status do sistema
    with st.sidebar.expander("ℹ️ Status do Sistema"):
        total_os = len(st.session_state.service_orders)
        pending_os = len([o for o in st.session_state.service_orders if o["status"] == "Agendado"])
        st.metric("Total OS", total_os)
        st.metric("OS Pendentes", pending_os)
    
    if page == "📊 Dashboard":
        show_dashboard(manager)
    elif page == "📝 Nova OS":
        show_new_order(manager)
    elif page == "🔧 Gerenciar OS":
        show_manage_orders(manager)
    elif page == "📅 Calendário":
        show_calendar(manager)
    elif page == "📈 Relatórios":
        show_reports(manager)
    elif page == "⚙️ Configurações":
        show_settings(manager)

def show_dashboard(manager):
    """Dashboard específico para fibra óptica"""
    st.header("📊 Dashboard - Fibra Óptica")
    
    # Métricas principais
    orders = st.session_state.service_orders
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_orders = len(orders)
        st.metric("Total OS", total_orders, delta=None)
    
    with col2:
        pending_orders = len([o for o in orders if o["status"] == "Agendado"])
        st.metric("OS Pendentes", pending_orders)
    
    with col3:
        in_progress = len([o for o in orders if o["status"] == "Em Campo"])
        st.metric("Em Campo", in_progress)
    
    with col4:
        completed_orders = len([o for o in orders if o["status"] == "Concluído"])
        st.metric("Concluídas", completed_orders)
    
    with col5:
        installations = len([o for o in orders if any(s["id"] == o["service_id"] and s["type"] == "Instalação" for s in st.session_state.services)])
        st.metric("Instalações", installations)
    
    # Métricas de receita e SLA
    st.markdown("### 💰 Indicadores Financeiros e SLA")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = sum([o["estimated_cost"] for o in orders if o["status"] == "Concluído"])
        st.metric("Receita Total", f"R$ {total_revenue:.2f}")
    
    with col2:
        avg_resolution_time = 2.5  # Simulado
        st.metric("Tempo Médio (h)", f"{avg_resolution_time:.1f}")
    
    with col3:
        sla_compliance = 95.2  # Simulado
        st.metric("SLA (%)", f"{sla_compliance:.1f}%", delta="2.1%")
    
    with col4:
        customer_satisfaction = 4.8  # Simulado
        st.metric("Satisfação", f"{customer_satisfaction:.1f}/5.0", delta="0.3")
    
    # Gráficos específicos de fibra óptica
    if orders:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 OS por Tipo de Serviço")
            service_types = {}
            for order in orders:
                service = next((s for s in st.session_state.services if s["id"] == order["service_id"]), {})
                service_type = service.get("type", "Outros")
                service_types[service_type] = service_types.get(service_type, 0) + 1
            
            if service_types:
                fig = px.pie(
                    values=list(service_types.values()),
                    names=list(service_types.keys()),
                    title="Distribuição por Tipo de Serviço",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🌍 OS por Região")
            region_counts = {}
            for order in orders:
                technician = next((t for t in st.session_state.technicians if t["id"] == order["technician_id"]), {})
                region = technician.get("region", "N/A")
                region_counts[region] = region_counts.get(region, 0) + 1
            
            if region_counts:
                fig = px.bar(
                    x=list(region_counts.keys()),
                    y=list(region_counts.values()),
                    title="OS por Região de Atendimento",
                    color=list(region_counts.values()),
                    color_continuous_scale="viridis"
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    # Timeline das próximas OS
    st.subheader("🗓️ Próximas OS Agendadas")
    df = manager.get_orders_dataframe()
    if not df.empty:
        today = datetime.now().date()
        df_future = df[df["Status"] == "Agendado"].sort_values("Data").head(8)
        if not df_future.empty:
            st.dataframe(df_future[["OS", "Cliente", "Serviço", "Técnico", "Região", "Data", "Hora", "CTO"]], 
                        use_container_width=True)
        else:
            st.info("✅ Nenhuma OS pendente encontrada")
    else:
        st.info("📝 Nenhuma OS cadastrada no sistema")

def show_new_order(manager):
    """Formulário para criar nova OS de fibra óptica"""
    st.header("📝 Nova Ordem de Serviço - Fibra Óptica")
    
    with st.form("new_fiber_order_form"):
        # Informações do cliente
        st.subheader("👤 Informações do Cliente")
        col1, col2 = st.columns(2)
        
        with col1:
            clients = st.session_state.clients
            client_options = {f"{c['name']} - {c['cto']} ({c['plan']})": c['id'] for c in clients}
            selected_client = st.selectbox("🏠 Cliente", options=list(client_options.keys()))
            client_id = client_options[selected_client]
            
            # Mostra informações do cliente selecionado
            client = next(c for c in clients if c['id'] == client_id)
            st.info(f"📍 **Endereço:** {client['address']}\n\n📞 **Tel:** {client['phone']}")
        
        with col2:
            st.text_input("🌐 CTO", value=client['cto'], disabled=True)
            st.text_input("📊 Plano Atual", value=client['plan'], disabled=True)
        
        # Informações do serviço
        st.subheader("🔧 Informações do Serviço")
        col1, col2 = st.columns(2)
        
        with col1:
            services = st.session_state.services
            service_options = {f"{s['name']} ({s['type']}) - R$ {s['price']:.2f}": s['id'] for s in services}
            selected_service = st.selectbox("⚙️ Tipo de Serviço", options=list(service_options.keys()))
            service_id = service_options[selected_service]
            
            service = next(s for s in services if s['id'] == service_id)
            
            # Técnico responsável (filtrado por tipo de serviço se possível)
            technicians = st.session_state.technicians
            if service['type'] in ['Instalação', 'Reparo', 'Manutenção']:
                filtered_techs = [t for t in technicians if service['type'].lower() in t['specialty'].lower()]
                if not filtered_techs:
                    filtered_techs = technicians
            else:
                filtered_techs = technicians
            
            tech_options = {f"{t['name']} - {t['region']} ({t['level']})": t['id'] for t in filtered_techs}
            selected_tech = st.selectbox("👨‍🔧 Técnico Responsável", options=list(tech_options.keys()))
            technician_id = tech_options[selected_tech]
        
        with col2:
            # Prioridade baseada no tipo de serviço
            default_priority = "Alta" if service['type'] == "Reparo" else "Normal"
            priority = st.selectbox("⚡ Prioridade", 
                                   ["Baixa", "Normal", "Alta", "Urgente"], 
                                   index=["Baixa", "Normal", "Alta", "Urgente"].index(default_priority))
            
            # Estimativa de custo
            service_price = service['price']
            estimated_cost = st.number_input("💰 Custo Estimado (R$)", value=service_price, min_value=0.0)
        
        # Agendamento
        st.subheader("📅 Agendamento")
        col1, col2 = st.columns(2)
        
        with col1:
            scheduled_date = st.date_input("📅 Data do Agendamento", 
                                         min_value=datetime.now().date())
        with col2:
            scheduled_time = st.time_input("🕐 Hora do Agendamento", value=dt.time(8, 0))
        
        # Informações técnicas específicas
        st.subheader("🔍 Informações Técnicas")
        col1, col2 = st.columns(2)
        
        with col1:
            description = st.text_area("📝 Descrição do Problema/Serviço", 
                                     height=80,
                                     placeholder="Ex: Cliente sem sinal, ONT offline, instalação de novo ponto...")
            
            cto_reference = st.text_input("🌐 Referência CTO", 
                                        value=client['cto'],
                                        placeholder="Ex: CTO-001-P1")
        
        with col2:
            signal_level = st.text_input("📶 Nível de Sinal (dBm)", 
                                       placeholder="Ex: -15.5")
            
            observations = st.text_area("📋 Observações", 
                                      height=80,
                                      placeholder="Observações adicionais...")
        
        # Equipamentos (se aplicável)
        if service['type'] in ['Instalação', 'Manutenção', 'Reparo']:
            st.subheader("📦 Equipamentos Necessários")
            equipment = st.session_state.equipment
            equipment_options = [f"{e['name']} - R$ {e['price']:.2f}" for e in equipment]
            selected_equipment = st.multiselect("Selecione os equipamentos", equipment_options)
        else:
            selected_equipment = []
        
        # Botão de submissão
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("🚀 Criar Ordem de Serviço", 
                                            type="primary", 
                                            use_container_width=True)
        
        if submitted:
            if description.strip():
                # Calcula custo com equipamentos
                equipment_cost = 0
                equipment_list = []
                for eq_desc in selected_equipment:
                    eq_name = eq_desc.split(" - R$")[0]
                    eq = next((e for e in equipment if e['name'] == eq_name), None)
                    if eq:
                        equipment_cost += eq['price']
                        equipment_list.append(eq['name'])
                
                final_cost = estimated_cost + equipment_cost
                
                order_data = {
                    "client_id": client_id,
                    "service_id": service_id,
                    "technician_id": technician_id,
                    "scheduled_date": scheduled_date,
                    "scheduled_time": scheduled_time,
                    "description": description,
                    "priority": priority,
                    "estimated_cost": final_cost,
                    "equipment_used": equipment_list,
                    "signal_level": signal_level,
                    "observations": observations,
                    "cto_reference": cto_reference
                }
                
                # Cria a ordem
                new_order = manager.create_service_order(order_data)
                
                # Prepara dados para o Google Agenda
                technician = next(t for t in technicians if t['id'] == technician_id)
                calendar_data = {
                    "id": new_order["id"],
                    "client_name": client["name"],
                    "client_email": client["email"],
                    "address": client["address"],
                    "cto": client["cto"],
                    "plan": client["plan"],
                    "service_name": service["name"],
                    "service_type": service["type"],
                    "technician_name": technician["name"],
                    "region": technician["region"],
                    "scheduled_date": scheduled_date.strftime("%Y-%m-%d"),
                    "scheduled_time": scheduled_time.strftime("%H:%M"),
                    "description": description,
                    "duration": service.get("duration", 2)
                }
                
                calendar_result = FiberOpticCalendarIntegration.create_calendar_event(calendar_data)
                
                st.success(f"✅ **Ordem de Serviço {new_order['id']} criada com sucesso!**")
                
                # Mostra resumo da OS criada
                with st.expander("📋 Resumo da OS Criada", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                        **📋 OS:** {new_order['id']}
                        **👤 Cliente:** {client['name']}
                        **🏠 Endereço:** {client['address']}
                        **🌐 CTO:** {client['cto']}
                        **📊 Plano:** {client['plan']}
                        """)
                    with col2:
                        st.markdown(f"""
                        **🔧 Serviço:** {service['name']}
                        **👨‍🔧 Técnico:** {technician['name']}
                        **🌍 Região:** {technician['region']}
                        **📅 Agendamento:** {scheduled_date.strftime('%d/%m/%Y')} às {scheduled_time.strftime('%H:%M')}
                        **💰 Custo Total:** R$ {final_cost:.2f}
                        """)
                    
                    if equipment_list:
                        st.markdown(f"**📦 Equipamentos:** {', '.join(equipment_list)}")
                
                if calendar_result["status"] == "success":
                    st.success("📅 Evento agendado no Google Agenda!")
                
            else:
                st.error("⚠️ Por favor, preencha a descrição do serviço.")

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
                selected_order = st.selectbox("Selecionar OS", df["OS"].tolist())
                new_status = st.selectbox("Novo Status", ["Agendado", "Em Campo", "Aguardando Peças", "Concluído", "Cancelado"])
                
                # Se concluindo, pedir informações adicionais
                completion_data = {}
                if new_status == "Concluído":
                    with st.expander("📊 Dados de Conclusão"):
                        completion_data["signal_level"] = st.text_input("Nível de Sinal Final (dBm)")
                        completion_data["equipment_used"] = st.text_area("Equipamentos Utilizados").split(',') if st.text_area("Equipamentos Utilizados") else []
                        completion_data["observations"] = st.text_area("Observações Finais")
                        completion_data["customer_satisfaction"] = st.select_slider("Satisfação do Cliente", 
                                                                                   options=[1, 2, 3, 4, 5], 
                                                                                   value=5)
                
                if st.button("🔄 Atualizar Status", type="primary"):
                    manager.update_order_status(selected_order, new_status, completion_data if new_status == "Concluído" else None)
                    st.success(f"✅ Status da OS {selected_order} atualizado para: **{new_status}**")
                    st.rerun()
        
        with col2:
            st.subheader("🔍 Detalhes da OS")
            if len(df) > 0:
                detail_order = st.selectbox("Ver Detalhes da OS", df["OS"].tolist(), key="detail_select")
                
                # Encontra a ordem selecionada
                selected_order_data = next((o for o in st.session_state.service_orders if o["id"] == detail_order), None)
                if selected_order_data:
                    client = next((c for c in st.session_state.clients if c["id"] == selected_order_data["client_id"]), {})
                    service = next((s for s in st.session_state.services if s["id"] == selected_order_data["service_id"]), {})
                    technician = next((t for t in st.session_state.technicians if t["id"] == selected_order_data["technician_id"]), {})
                    
                    with st.expander(f"📋 Detalhes - {detail_order}", expanded=True):
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
                            st.markdown(f"**📦 Equipamentos:** {', '.join(selected_order_data['equipment_used'])}")
                        
                        st.markdown(f"**📝 Descrição:** {selected_order_data.get('description', 'N/A')}")
                        
                        if selected_order_data.get('observations'):
                            st.markdown(f"**📋 Observações:** {selected_order_data['observations']}")
    else:
        st.info("📝 Nenhuma OS encontrada com os filtros aplicados")

def show_calendar(manager):
    """Visualização em calendário para fibra óptica"""
    st.header("📅 Calendário de Agendamentos - Fibra Óptica")
    
    # Seleção do período
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_month = st.selectbox("📅 Mês", range(1, 13), index=datetime.now().month-1)
    with col2:
        selected_year = st.selectbox("📅 Ano", range(2024, 2027), index=1)
    with col3:
        view_type = st.selectbox("🔍 Visualização", ["Por Região", "Por Tipo de Serviço", "Por Técnico"])
    
    # Mostra agendamentos do mês
    orders = st.session_state.service_orders
    month_orders = []
    
    for order in orders:
        order_date = datetime.strptime(order["scheduled_date"], "%Y-%m-%d")
        if order_date.month == selected_month and order_date.year == selected_year:
            client = next((c for c in st.session_state.clients if c["id"] == order["client_id"]), {})
            service = next((s for s in st.session_state.services if s["id"] == order["service_id"]), {})
            technician = next((t for t in st.session_state.technicians if t["id"] == order["technician_id"]), {})
            
            month_orders.append({
                "OS": order["id"],
                "Data": order["scheduled_date"],
                "Hora": order["scheduled_time"],
                "Cliente": client.get("name", "N/A"),
                "CTO": client.get("cto", "N/A"),
                "Serviço": service.get("name", "N/A"),
                "Tipo": service.get("type", "N/A"),
                "Técnico": technician.get("name", "N/A"),
                "Região": technician.get("region", "N/A"),
                "Status": order["status"],
                "Prioridade": order["priority"]
            })
    
    if month_orders:
        df = pd.DataFrame(month_orders)
        df = df.sort_values(["Data", "Hora"])
        
        # Métricas do mês
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 Total OS", len(month_orders))
        with col2:
            installations = len([o for o in month_orders if o["Tipo"] == "Instalação"])
            st.metric("🏠 Instalações", installations)
        with col3:
            repairs = len([o for o in month_orders if o["Tipo"] == "Reparo"])
            st.metric("🔧 Reparos", repairs)
        with col4:
            urgent = len([o for o in month_orders if o["Prioridade"] == "Urgente"])
            st.metric("🚨 Urgentes", urgent)
        
        st.dataframe(df, use_container_width=True)
        
        # Gráfico baseado na visualização selecionada
        col1, col2 = st.columns(2)
        
        with col1:
            if view_type == "Por Região":
                region_counts = df.groupby("Região").size().reset_index(name="Quantidade")
                fig = px.bar(region_counts, x="Região", y="Quantidade", 
                           title="Agendamentos por Região",
                           color="Quantidade", color_continuous_scale="viridis")
                st.plotly_chart(fig, use_container_width=True)
            
            elif view_type == "Por Tipo de Serviço":
                type_counts = df.groupby("Tipo").size().reset_index(name="Quantidade")
                fig = px.pie(type_counts, values="Quantidade", names="Tipo", 
                           title="Distribuição por Tipo de Serviço")
                st.plotly_chart(fig, use_container_width=True)
            
            else:  # Por Técnico
                tech_counts = df.groupby("Técnico").size().reset_index(name="Quantidade")
                fig = px.bar(tech_counts, x="Técnico", y="Quantidade", 
                           title="Agendamentos por Técnico",
                           color="Quantidade", color_continuous_scale="plasma")
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico de agendamentos por dia
            daily_counts = df.groupby("Data").size().reset_index(name="Agendamentos")
            daily_counts["Data"] = pd.to_datetime(daily_counts["Data"])
            fig = px.line(daily_counts, x="Data", y="Agendamentos", 
                         title="Agendamentos por Dia", markers=True)
            fig.update_layout(xaxis_title="Data", yaxis_title="Número de Agendamentos")
            st.plotly_chart(fig, use_container_width=True)
        
        # Agenda detalhada por dia
        st.subheader("🗓️ Agenda Detalhada")
        selected_date = st.date_input("Selecionar Data", value=datetime.now().date())
        date_str = selected_date.strftime("%Y-%m-%d")
        day_orders = df[df["Data"] == date_str]
        
        if not day_orders.empty:
            day_orders = day_orders.sort_values("Hora")
            st.dataframe(day_orders[["OS", "Hora", "Cliente", "Serviço", "Técnico", "Região", "Status"]], 
                        use_container_width=True)
        else:
            st.info(f"📅 Nenhum agendamento para {selected_date.strftime('%d/%m/%Y')}")
            
    else:
        st.info("📅 Nenhum agendamento encontrado para este mês")

def show_reports(manager):
    """Relatórios específicos para fibra óptica"""
    st.header("📈 Relatórios - Fibra Óptica")
    
    orders = st.session_state.service_orders
    
    if orders:
        # Seletor de período para relatórios
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("📅 Data Início", value=datetime.now().date() - timedelta(days=30))
        with col2:
            end_date = st.date_input("📅 Data Fim", value=datetime.now().date())
        
        # Filtra ordens por período
        period_orders = []
        for order in orders:
            order_date = datetime.strptime(order["scheduled_date"], "%Y-%m-%d").date()
            if start_date <= order_date <= end_date:
                period_orders.append(order)
        
        if period_orders:
            # Métricas principais do período
            st.subheader(f"📊 Indicadores do Período ({start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')})")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_period = len(period_orders)
                st.metric("Total OS", total_period)
            
            with col2:
                completed_period = len([o for o in period_orders if o["status"] == "Concluído"])
                completion_rate = (completed_period / total_period * 100) if total_period > 0 else 0
                st.metric("Taxa Conclusão", f"{completion_rate:.1f}%")
            
            with col3:
                total_revenue_period = sum([o["estimated_cost"] for o in period_orders if o["status"] == "Concluído"])
                st.metric("Receita", f"R$ {total_revenue_period:.2f}")
            
            with col4:
                installations_period = len([o for o in period_orders 
                                          if any(s["id"] == o["service_id"] and s["type"] == "Instalação" 
                                               for s in st.session_state.services)])
                st.metric("Instalações", installations_period)
            
            # Relatório por tipo de serviço
            st.subheader("📋 Relatório por Tipo de Serviço")
            service_analysis = {}
            for order in period_orders:
                service = next((s for s in st.session_state.services if s["id"] == order["service_id"]), {})
                service_type = service.get("type", "Outros")
                
                if service_type not in service_analysis:
                    service_analysis[service_type] = {
                        "total": 0, "concluidas": 0, "receita": 0, "pendentes": 0
                    }
                
                service_analysis[service_type]["total"] += 1
                if order["status"] == "Concluído":
                    service_analysis[service_type]["concluidas"] += 1
                    service_analysis[service_type]["receita"] += order["estimated_cost"]
                elif order["status"] in ["Agendado", "Em Campo"]:
                    service_analysis[service_type]["pendentes"] += 1
            
            service_report = []
            for service_type, data in service_analysis.items():
                completion_rate = (data["concluidas"] / data["total"] * 100) if data["total"] > 0 else 0
                service_report.append({
                    "Tipo de Serviço": service_type,
                    "Total": data["total"],
                    "Concluídas": data["concluidas"],
                    "Pendentes": data["pendentes"],
                    "Taxa Conclusão (%)": f"{completion_rate:.1f}%",
                    "Receita (R$)": f"{data['receita']:.2f}"
                })
            
            st.dataframe(pd.DataFrame(service_report), use_container_width=True)
            
            # Relatório de produtividade por técnico
            st.subheader("👨‍🔧 Produtividade por Técnico")
            tech_analysis = {}
            for order in period_orders:
                tech_id = order["technician_id"]
                technician = next((t for t in st.session_state.technicians if t["id"] == tech_id), {})
                tech_name = technician.get("name", "N/A")
                region = technician.get("region", "N/A")
                
                if tech_id not in tech_analysis:
                    tech_analysis[tech_id] = {
                        "name": tech_name, "region": region, "total": 0, 
                        "concluidas": 0, "receita": 0, "instalacoes": 0, "reparos": 0
                    }
                
                tech_analysis[tech_id]["total"] += 1
                if order["status"] == "Concluído":
                    tech_analysis[tech_id]["concluidas"] += 1
                    tech_analysis[tech_id]["receita"] += order["estimated_cost"]
                
                # Conta tipos específicos
                service = next((s for s in st.session_state.services if s["id"] == order["service_id"]), {})
                if service.get("type") == "Instalação":
                    tech_analysis[tech_id]["instalacoes"] += 1
                elif service.get("type") == "Reparo":
                    tech_analysis[tech_id]["reparos"] += 1
            
            tech_report = []
            for tech_id, data in tech_analysis.items():
                completion_rate = (data["concluidas"] / data["total"] * 100) if data["total"] > 0 else 0
                avg_revenue = data["receita"] / data["concluidas"] if data["concluidas"] > 0 else 0
                
                tech_report.append({
                    "Técnico": data["name"],
                    "Região": data["region"],
                    "Total OS": data["total"],
                    "Concluídas": data["concluidas"],
                    "Instalações": data["instalacoes"],
                    "Reparos": data["reparos"],
                    "Taxa Conclusão (%)": f"{completion_rate:.1f}%",
                    "Receita Total (R$)": f"{data['receita']:.2f}",
                    "Receita Média (R$)": f"{avg_revenue:.2f}"
                })
            
            st.dataframe(pd.DataFrame(tech_report), use_container_width=True)
            
            # Gráficos de análise
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de instalações vs reparos por região
                region_analysis = {}
                for order in period_orders:
                    tech = next((t for t in st.session_state.technicians if t["id"] == order["technician_id"]), {})
                    service = next((s for s in st.session_state.services if s["id"] == order["service_id"]), {})
                    region = tech.get("region", "N/A")
                    service_type = service.get("type", "Outros")
                    
                    if region not in region_analysis:
                        region_analysis[region] = {"Instalação": 0, "Reparo": 0, "Outros": 0}
                    
                    if service_type in region_analysis[region]:
                        region_analysis[region][service_type] += 1
                    else:
                        region_analysis[region]["Outros"] += 1
                
                region_df = pd.DataFrame(region_analysis).T.fillna(0)
                if not region_df.empty:
                    fig = px.bar(region_df, title="Instalações vs Reparos por Região", 
                               color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c'])
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Gráfico de evolução temporal
                daily_analysis = {}
                for order in period_orders:
                    date = order["scheduled_date"]
                    if date not in daily_analysis:
                        daily_analysis[date] = 0
                    daily_analysis[date] += 1
                
                if daily_analysis:
                    dates = sorted(daily_analysis.keys())
                    counts = [daily_analysis[date] for date in dates]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=dates, y=counts, mode='lines+markers', 
                                           name='OS por Dia', line=dict(color='#1f77b4')))
                    fig.update_layout(title="Evolução das OS no Período",
                                    xaxis_title="Data", yaxis_title="Número de OS")
                    st.plotly_chart(fig, use_container_width=True)
            
            # Relatório de SLA e qualidade
            st.subheader("📊 Indicadores de SLA e Qualidade")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Simular dados de SLA
                on_time_completion = 85.5
                st.metric("SLA Cumprimento", f"{on_time_completion:.1f}%", delta="3.2%")
            
            with col2:
                # Simular satisfação do cliente
                avg_satisfaction = 4.7
                st.metric("Satisfação Média", f"{avg_satisfaction:.1f}/5.0", delta="0.2")
            
            with col3:
                # Tempo médio de resolução
                avg_resolution_time = 2.3
                st.metric("Tempo Médio (h)", f"{avg_resolution_time:.1f}h", delta="-0.5h")
            
        else:
            st.info("📅 Nenhuma OS encontrada no período selecionado")
    else:
        st.info("📊 Nenhum dado disponível para relatórios")

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
                            "id": manager.generate_id(),
                            "name": name,
                            "phone": phone,
                            "email": email,
                            "address": address,
                            "cto": cto,
                            "plan": plan
                        }
                        st.session_state.clients.append(new_client)
                        st.success("✅ Cliente adicionado com sucesso!")
                        st.rerun()
        
        # Lista de clientes
        if st.session_state.clients:
            clients_df = pd.DataFrame(st.session_state.clients)
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
                            "id": manager.generate_id(),
                            "name": name,
                            "type": service_type,
                            "price": price,
                            "duration": duration
                        }
                        st.session_state.services.append(new_service)
                        st.success("✅ Serviço adicionado com sucesso!")
                        st.rerun()
        
        # Lista de serviços
        if st.session_state.services:
            services_df = pd.DataFrame(st.session_state.services)
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
                            "id": manager.generate_id(),
                            "name": name,
                            "specialty": specialty,
                            "region": region,
                            "level": level
                        }
                        st.session_state.technicians.append(new_tech)
                        st.success("✅ Técnico adicionado com sucesso!")
                        st.rerun()
        
        # Lista de técnicos
        if st.session_state.technicians:
            techs_df = pd.DataFrame(st.session_state.technicians)
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
                            "id": manager.generate_id(),
                            "name": name,
                            "type": equipment_type,
                            "price": price
                        }
                        st.session_state.equipment.append(new_equipment)
                        st.success("✅ Equipamento adicionado com sucesso!")
                        st.rerun()
        
        # Lista de equipamentos
        if st.session_state.equipment:
            equipment_df = pd.DataFrame(st.session_state.equipment)
            equipment_df = equipment_df[["name", "type", "price"]]
            equipment_df.columns = ["Nome", "Tipo", "Preço (R$)"]
            st.dataframe(equipment_df, use_container_width=True)
    
    # Configurações do sistema
    st.markdown("---")
    st.subheader("🔧 Configurações do Sistema")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Limpar Todas as OS", type="secondary"):
            if st.button("⚠️ Confirmar Limpeza", type="secondary"):
                st.session_state.service_orders = []
                st.success("✅ Todas as OS foram removidas!")
                st.rerun()
    
    with col2:
        if st.button("📤 Exportar Dados", type="secondary"):
            # Simular exportação
            st.info("📋 Funcionalidade de exportação será implementada")

if __name__ == "__main__":
    main()
