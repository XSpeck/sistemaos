class FiberOpticCalendarIntegration:
    @staticmethod
    def create_calendar_event(order_data):
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