import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

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
    
    # Busca dados do banco
    orders = manager.get_all_orders()
    clients = {c['id']: c for c in manager.get_all_clients()}
    services = {s['id']: s for s in manager.get_all_services()}
    technicians = {t['id']: t for t in manager.get_all_technicians()}
    
    # Filtra ordens do mês selecionado
    month_orders = []
    
    for order in orders:
        order_date = datetime.strptime(order["scheduled_date"], "%Y-%m-%d")
        if order_date.month == selected_month and order_date.year == selected_year:
            client = clients.get(order["client_id"], {})
            service = services.get(order["service_id"], {})
            technician = technicians.get(order["technician_id"], {})
            
            month_orders.append({
                "OS": order["order_number"],
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