import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
from supabase import create_client, Client

@st.cache_resource
def init_supabase():
    try:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]
        supabase: Client = create_client(supabase_url, supabase_key)
        return supabase
    except Exception as e:
        st.error(f"Erro ao conectar com Supabase: {e}")
        return None

class FiberOpticServiceManager:
    def __init__(self):
        self.supabase = init_supabase()
        if self.supabase:
            self.initialize_database()
    
    def initialize_database(self):
        try:
            clients_result = self.supabase.table('clients').select('*').limit(1).execute()
            if not clients_result.data:
                default_clients = [
                    {
                        "name": "João Silva",
                        "phone": "(11) 99999-1111",
                        "email": "joao@email.com",
                        "address": "Rua das Flores, 123 - Vila Madalena",
                        "cto": "CTO-001",
                        "plan": "100MB"
                    },
                    {
                        "name": "Empresa ABC Ltda",
                        "phone": "(11) 99999-2222",
                        "email": "contato@abc.com",
                        "address": "Av. Paulista, 1000 - Bela Vista",
                        "cto": "CTO-002",
                        "plan": "500MB"
                    },
                    {
                        "name": "Maria Santos",
                        "phone": "(11) 99999-3333",
                        "email": "maria@email.com",
                        "address": "Rua Augusta, 456 - Consolação",
                        "cto": "CTO-003",
                        "plan": "200MB"
                    }
                ]
                self.supabase.table('clients').insert(default_clients).execute()
            
            services_result = self.supabase.table('services').select('*').limit(1).execute()
            if not services_result.data:
                default_services = [
                    {"name": "Instalação Residencial", "price": 0.00, "duration": 3, "type": "Instalação"},
                    {"name": "Instalação Empresarial", "price": 0.00, "duration": 4, "type": "Instalação"},
                    {"name": "Reparo de Cabo Rompido", "price": 150.00, "duration": 2, "type": "Reparo"},
                    {"name": "Troca de Equipamento ONT", "price": 80.00, "duration": 1, "type": "Manutenção"},
                    {"name": "Mudança de Endereço", "price": 100.00, "duration": 3, "type": "Mudança"},
                    {"name": "Upgrade de Plano", "price": 0.00, "duration": 1, "type": "Upgrade"},
                    {"name": "Reparo em CTO", "price": 200.00, "duration": 4, "type": "Reparo"},
                    {"name": "Verificação de Sinal", "price": 50.00, "duration": 1, "type": "Diagnóstico"},
                    {"name": "Emenda de Fibra", "price": 120.00, "duration": 2, "type": "Reparo"},
                    {"name": "Cancelamento", "price": 0.00, "duration": 1, "type": "Cancelamento"}
                ]
                self.supabase.table('services').insert(default_services).execute()
            
            technicians_result = self.supabase.table('technicians').select('*').limit(1).execute()
            if not technicians_result.data:
                default_technicians = [
                    {"name": "Carlos Fibra", "specialty": "Instalação", "region": "Zona Sul", "level": "Sênior"},
                    {"name": "Ana Conecta", "specialty": "Reparo", "region": "Centro", "level": "Pleno"},
                    {"name": "Roberto Rede", "specialty": "Manutenção", "region": "Zona Norte", "level": "Júnior"},
                    {"name": "Mariana Link", "specialty": "Instalação", "region": "Zona Oeste", "level": "Sênior"},
                    {"name": "Pedro Optical", "specialty": "Reparo", "region": "Zona Leste", "level": "Pleno"}
                ]
                self.supabase.table('technicians').insert(default_technicians).execute()
            
            equipment_result = self.supabase.table('equipment').select('*').limit(1).execute()
            if not equipment_result.data:
                default_equipment = [
                    {"name": "ONT Huawei HG8010H", "type": "ONT", "price": 150.00},
                    {"name": "ONT Nokia G-010G-A", "type": "ONT", "price": 120.00},
                    {"name": "Router Wi-Fi AC1200", "type": "Router", "price": 200.00},
                    {"name": "Splitter 1x8", "type": "Splitter", "price": 25.00},
                    {"name": "Cabo Drop 100m", "type": "Cabo", "price": 80.00},
                    {"name": "Conector SC/APC", "type": "Conector", "price": 5.00},
                    {"name": "Cordão Óptico 3m", "type": "Cordão", "price": 15.00}
                ]
                self.supabase.table('equipment').insert(default_equipment).execute()
        
        except Exception as e:
            st.error(f"Erro ao inicializar dados: {e}")
    
    def generate_id(self):
        return str(uuid.uuid4())[:8].upper()
    
    def create_service_order(self, order_data):
        try:
            order = {
                "order_number": f"OS{self.generate_id()}",
                "client_id": order_data["client_id"],
                "service_id": order_data["service_id"],
                "technician_id": order_data["technician_id"],
                "scheduled_date": order_data["scheduled_date"].strftime("%Y-%m-%d"),
                "scheduled_time": order_data["scheduled_time"].strftime("%H:%M"),
                "description": order_data["description"],
                "status": "Agendado",
                "priority": order_data["priority"],
                "estimated_cost": order_data["estimated_cost"],
                "equipment_used": order_data.get("equipment_used", []),
                "signal_level": order_data.get("signal_level", ""),
                "observations": order_data.get("observations", ""),
                "cto_reference": order_data.get("cto_reference", "")
            }
            result = self.supabase.table('service_orders').insert(order).execute()
            if result.data:
                return result.data[0]
            else:
                st.error("Erro ao criar ordem de serviço")
                return None
        except Exception as e:
            st.error(f"Erro ao criar OS: {e}")
            return None
    
    def update_order_status(self, order_id, new_status, completion_data=None):
        try:
            update_data = {"status": new_status}
            if new_status == "Concluído" and completion_data:
                update_data.update({
                    "completed_at": datetime.now().isoformat(),
                    "signal_level": completion_data.get("signal_level", ""),
                    "equipment_used": completion_data.get("equipment_used", []),
                    "observations": completion_data.get("observations", ""),
                    "customer_satisfaction": completion_data.get("customer_satisfaction", "")
                })
            result = self.supabase.table('service_orders').update(update_data).eq('id', order_id).execute()
            return result.data
        except Exception as e:
            st.error(f"Erro ao atualizar status: {e}")
            return None
    
    def get_all_clients(self):
        try:
            result = self.supabase.table('clients').select('*').execute()
            return result.data
        except Exception as e:
            st.error(f"Erro ao buscar clientes: {e}")
            return []
    
    def get_all_services(self):
        try:
            result = self.supabase.table('services').select('*').execute()
            return result.data
        except Exception as e:
            st.error(f"Erro ao buscar serviços: {e}")
            return []
    
    def get_all_technicians(self):
        try:
            result = self.supabase.table('technicians').select('*').execute()
            return result.data
        except Exception as e:
            st.error(f"Erro ao buscar técnicos: {e}")
            return []
    
    def get_all_equipment(self):
        try:
            result = self.supabase.table('equipment').select('*').execute()
            return result.data
        except Exception as e:
            st.error(f"Erro ao buscar equipamentos: {e}")
            return []
    
    def get_all_orders(self):
        try:
            result = self.supabase.table('service_orders').select('*').execute()
            return result.data
        except Exception as e:
            st.error(f"Erro ao buscar ordens: {e}")
            return []
            
    def delete_order(self, order_id):
        try:
            result = self.supabase.table('service_orders').delete().eq('id', order_id).execute()
            # Retorna True se deletou ao menos uma linha
            return bool(result.data)
        except Exception as e:
            st.error(f"Erro ao excluir OS: {e}")
            return False
        
    def get_orders_dataframe(self):
        orders = self.get_all_orders()
        if not orders:
            return pd.DataFrame()
        
        clients = {c['id']: c for c in self.get_all_clients()}
        services = {s['id']: s for s in self.get_all_services()}
        technicians = {t['id']: t for t in self.get_all_technicians()}
        
        orders_list = []
        for order in orders:
            client = clients.get(order["client_id"], {})
            service = services.get(order["service_id"], {})
            technician = technicians.get(order["technician_id"], {})
            orders_list.append({
                "ID": order["id"],
                "OS": order["order_number"],
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
        return pd.DataFrame(orders_list)
    
    def add_client(self, client_data):
        try:
            result = self.supabase.table('clients').insert(client_data).execute()
            return result.data
        except Exception as e:
            st.error(f"Erro ao adicionar cliente: {e}")
            return None
    
    def add_service(self, service_data):
        try:
            result = self.supabase.table('services').insert(service_data).execute()
            return result.data
        except Exception as e:
            st.error(f"Erro ao adicionar serviço: {e}")
            return None
    
    def add_technician(self, technician_data):
        try:
            result = self.supabase.table('technicians').insert(technician_data).execute()
            return result.data
        except Exception as e:
            st.error(f"Erro ao adicionar técnico: {e}")
            return None
    
    def add_equipment(self, equipment_data):
        try:
            result = self.supabase.table('equipment').insert(equipment_data).execute()
            return result.data
        except Exception as e:
            st.error(f"Erro ao adicionar equipamento: {e}")
            return None
