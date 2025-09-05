import streamlit as st
from fiber_service_manager import FiberOpticServiceManager
from fiber_calendar import FiberOpticCalendarIntegration
from dashboard import show_dashboard
from new_order import show_new_order
from manage_orders import show_manage_orders
from calendar_view import show_calendar
from reports import show_reports
from settings import show_settings
from schema import show_database_schema

def main():
    st.set_page_config(page_title="Sistema de OS - Fibra Óptica", page_icon="🌐", layout="wide")
    st.title("🌐 Sistema de OS - Fibra Óptica")
    st.markdown("**Sistema de Gestão de Ordens de Serviço para Técnicos de Fibra Óptica**")
    st.markdown("---")

    manager = FiberOpticServiceManager()
    if not manager.supabase:
        st.error("❌ Não foi possível conectar ao banco de dados. Verifique as configurações do Supabase.")
        return

    st.sidebar.title("🔧 Navegação")
    st.sidebar.markdown("**Fibra Óptica OS**")
    page = st.sidebar.selectbox(
        "Selecione uma página",
        ["📊 Dashboard", "📝 Nova OS", "🔧 Gerenciar OS", "📅 Calendário", "📈 Relatórios", "⚙️ Configurações"]
    )

    with st.sidebar.expander("ℹ️ Status do Sistema"):
        orders = manager.get_all_orders()
        total_os = len(orders)
        pending_os = len([o for o in orders if o["status"] == "Agendado"])
        st.metric("Total OS", total_os)
        st.metric("OS Pendentes", pending_os)
        st.success("✅ Conectado ao Supabase")
    
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

    if st.sidebar.checkbox("🗄️ Mostrar Schema SQL"):
        show_database_schema()

if __name__ == "__main__":
    main()