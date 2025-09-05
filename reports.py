import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_reports(manager):
    """Relatórios específicos para fibra óptica"""
    st.header("📈 Relatórios - Fibra Óptica")
    
    orders = manager.get_all_orders()
    services = manager.get_all_services()
    technicians = manager.get_all_technicians()
    
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
                                               for s in services)])
                st.metric("Instalações", installations_period)
            
            # Relatório por tipo de serviço
            st.subheader("📋 Relatório por Tipo de Serviço")
            service_analysis = {}
            for order in period_orders:
                service = next((s for s in services if s["id"] == order["service_id"]), {})
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
                technician = next((t for t in technicians if t["id"] == tech_id), {})
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
                service = next((s for s in services if s["id"] == order["service_id"]), {})
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
                    tech = next((t for t in technicians if t["id"] == order["technician_id"]), {})
                    service = next((s for s in services if s["id"] == order["service_id"]), {})
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
        else:
            st.info("📅 Nenhuma OS encontrada no período selecionado")
    else:
        st.info("📊 Nenhum dado disponível para relatórios")