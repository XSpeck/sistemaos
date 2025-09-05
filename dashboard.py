import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def show_dashboard(manager):
    """Dashboard específico para fibra óptica"""
    st.header("📊 Dashboard - Fibra Óptica")
    
    # Busca dados do banco
    orders = manager.get_all_orders()
    services = manager.get_all_services()
    technicians = manager.get_all_technicians()
    
    # Métricas principais
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
        installations = len([o for o in orders if any(s["id"] == o["service_id"] and s["type"] == "Instalação" for s in services)])
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
                service = next((s for s in services if s["id"] == order["service_id"]), {})
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
                technician = next((t for t in technicians if t["id"] == order["technician_id"]), {})
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