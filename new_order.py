import streamlit as st
from fiber_calendar import FiberOpticCalendarIntegration
from datetime import datetime, time
import pandas as pd

def show_new_order(manager):
    """Formulário para criar nova OS de fibra óptica"""
    st.header("📝 Nova Ordem de Serviço - Fibra Óptica")

    clients = manager.get_all_clients()
    services = manager.get_all_services()
    technicians = manager.get_all_technicians()
    equipment = manager.get_all_equipment()

    if not all([clients, services, technicians]):
        st.error("❌ Erro ao carregar dados do banco. Verifique a conexão.")
        return

    with st.form("new_fiber_order_form"):
        st.subheader("👤 Informações do Cliente")
        col1, col2 = st.columns(2)

        with col1:
            client_options = {f"{c['name']} - {c['cto']} ({c['plan']})": c['id'] for c in clients}
            selected_client = st.selectbox("🏠 Cliente", options=list(client_options.keys()))
            client_id = client_options[selected_client]
            client = next(c for c in clients if c['id'] == client_id)
            st.info(f"📍 **Endereço:** {client['address']}\n\n📞 **Tel:** {client['phone']}")

        with col2:
            st.text_input("🌐 CTO", value=client['cto'], disabled=True)
            st.text_input("📊 Plano Atual", value=client['plan'], disabled=True)

        st.subheader("🔧 Informações do Serviço")
        col1, col2 = st.columns(2)

        with col1:
            service_options = {f"{s['name']} ({s['type']}) - R$ {s['price']:.2f}": s['id'] for s in services}
            selected_service = st.selectbox("⚙️ Tipo de Serviço", options=list(service_options.keys()))
            service_id = service_options[selected_service]
            service = next(s for s in services if s['id'] == service_id)
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
            default_priority = "Alta" if service['type'] == "Reparo" else "Normal"
            priority = st.selectbox("⚡ Prioridade",
                                   ["Baixa", "Normal", "Alta", "Urgente"],
                                   index=["Baixa", "Normal", "Alta", "Urgente"].index(default_priority))
            service_price = service['price']
            estimated_cost = st.number_input("💰 Custo Estimado (R$)", value=service_price, min_value=0.0)

        st.subheader("📅 Agendamento")
        col1, col2 = st.columns(2)
        with col1:
            scheduled_date = st.date_input("📅 Data do Agendamento", min_value=datetime.now().date())
        with col2:
            scheduled_time = st.time_input("🕐 Hora do Agendamento", value=time(8, 0))

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
            signal_level = st.text_input("📶 Nível de Sinal (dBm)", placeholder="Ex: -15.5")
            observations = st.text_area("📋 Observações", height=80, placeholder="Observações adicionais...")

        if service['type'] in ['Instalação', 'Manutenção', 'Reparo']:
            st.subheader("📦 Equipamentos Necessários")
            if equipment:
                equipment_options = [f"{e['name']} - R$ {e['price']:.2f}" for e in equipment]
                selected_equipment = st.multiselect("Selecione os equipamentos", equipment_options)
            else:
                selected_equipment = []
        else:
            selected_equipment = []

        submitted = st.form_submit_button("🚀 Criar Ordem de Serviço")
        if submitted:
            if description.strip():
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
                new_order = manager.create_service_order(order_data)
                if new_order:
                    technician = next(t for t in technicians if t['id'] == technician_id)
                    calendar_data = {
                        "id": new_order["order_number"],
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
                    st.success(f"✅ **Ordem de Serviço {new_order['order_number']} criada com sucesso!**")
                    with st.expander("📋 Resumo da OS Criada", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"""
                            **📋 OS:** {new_order['order_number']}
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
                    st.balloons()
                else:
                    st.error("❌ Erro ao criar ordem de serviço")
            else:
                st.error("⚠️ Por favor, preencha a descrição do serviço.")
