import streamlit as st

def show_database_schema():
    """Mostra o schema SQL para criar as tabelas no Supabase"""
    st.markdown("---")
    st.subheader("🗄️ Schema do Banco de Dados")
    
    tab1, tab2 = st.tabs(["📋 Schema Básico", "🔧 Schema Completo"])
    
    with tab1:
        st.markdown("**Execute primeiro este schema básico no Supabase:**")
        
        basic_sql = """
-- EXECUTE ESTE SQL PRIMEIRO NO SUPABASE

-- 1. Tabela de Clientes
CREATE TABLE IF NOT EXISTS clients (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT NOT NULL,
    cto TEXT,
    plan TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Tabela de Serviços
CREATE TABLE IF NOT EXISTS services (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    price DECIMAL(10,2) DEFAULT 0,
    duration INTEGER DEFAULT 2,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Tabela de Técnicos
CREATE TABLE IF NOT EXISTS technicians (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    region TEXT NOT NULL,
    level TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Tabela de Equipamentos
CREATE TABLE IF NOT EXISTS equipment (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    price DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Tabela de Ordens de Serviço (VERSÃO BÁSICA)
CREATE TABLE IF NOT EXISTS service_orders (
    id BIGSERIAL PRIMARY KEY,
    order_number TEXT NOT NULL UNIQUE,
    client_id BIGINT REFERENCES clients(id),
    service_id BIGINT REFERENCES services(id),
    technician_id BIGINT REFERENCES technicians(id),
    scheduled_date DATE NOT NULL,
    scheduled_time TIME NOT NULL,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'Agendado',
    priority TEXT DEFAULT 'Normal',
    estimated_cost DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Desabilitar RLS temporariamente para testes
ALTER TABLE clients DISABLE ROW LEVEL SECURITY;
ALTER TABLE services DISABLE ROW LEVEL SECURITY;
ALTER TABLE technicians DISABLE ROW LEVEL SECURITY;
ALTER TABLE equipment DISABLE ROW LEVEL SECURITY;
ALTER TABLE service_orders DISABLE ROW LEVEL SECURITY;
        """
        
        st.code(basic_sql, language="sql")
        
        st.info("⚠️ **IMPORTANTE**: Execute este SQL primeiro no Supabase SQL Editor. Depois que funcionar, você pode executar as melhorias do Schema Completo.")
    
    with tab2:
        st.markdown("**Após o básico funcionar, execute estas melhorias:**")
        
        advanced_sql = """
-- EXECUTE DEPOIS QUE O BÁSICO ESTIVER FUNCIONANDO

-- Adicionar colunas extras para funcionalidades avançadas
ALTER TABLE service_orders 
ADD COLUMN IF NOT EXISTS signal_level TEXT,
ADD COLUMN IF NOT EXISTS observations TEXT,
ADD COLUMN IF NOT EXISTS cto_reference TEXT,
ADD COLUMN IF NOT EXISTS completed_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS customer_satisfaction INTEGER,
ADD COLUMN IF NOT EXISTS equipment_used JSONB DEFAULT '[]'::jsonb,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_service_orders_status ON service_orders(status);
CREATE INDEX IF NOT EXISTS idx_service_orders_scheduled_date ON service_orders(scheduled_date);
CREATE INDEX IF NOT EXISTS idx_service_orders_client_id ON service_orders(client_id);
CREATE INDEX IF NOT EXISTS idx_service_orders_technician_id ON service_orders(technician_id);

-- Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$ language 'plpgsql';

-- Trigger para atualizar updated_at
CREATE TRIGGER update_service_orders_updated_at 
    BEFORE UPDATE ON service_orders 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """
        
        st.code(advanced_sql, language="sql")
    
    st.markdown("---")
    st.subheader("🔍 Status das Tabelas")
    
    # Verifica se as tabelas existem
    if st.button("🔍 Verificar Tabelas no Supabase"):
        manager = FiberOpticServiceManager()
        if manager.supabase:
            try:
                # Testa cada tabela
                tables_status = {}
                
                # Testa clients
                try:
                    result = manager.supabase.table('clients').select('id').limit(1).execute()
                    tables_status['clients'] = "✅ OK"
                except Exception as e:
                    tables_status['clients'] = f"❌ Erro: {str(e)[:50]}"
                
                # Testa services
                try:
                    result = manager.supabase.table('services').select('id').limit(1).execute()
                    tables_status['services'] = "✅ OK"
                except Exception as e:
                    tables_status['services'] = f"❌ Erro: {str(e)[:50]}"
                
                # Testa technicians
                try:
                    result = manager.supabase.table('technicians').select('id').limit(1).execute()
                    tables_status['technicians'] = "✅ OK"
                except Exception as e:
                    tables_status['technicians'] = f"❌ Erro: {str(e)[:50]}"
                
                # Testa equipment
                try:
                    result = manager.supabase.table('equipment').select('id').limit(1).execute()
                    tables_status['equipment'] = "✅ OK"
                except Exception as e:
                    tables_status['equipment'] = f"❌ Erro: {str(e)[:50]}"
                
                # Testa service_orders
                try:
                    result = manager.supabase.table('service_orders').select('id').limit(1).execute()
                    tables_status['service_orders'] = "✅ OK"
                except Exception as e:
                    tables_status['service_orders'] = f"❌ Erro: {str(e)[:50]}"
                
                # Mostra resultado
                for table, status in tables_status.items():
                    st.write(f"**{table}**: {status}")
                    
            except Exception as e:
                st.error(f"Erro ao verificar tabelas: {e}")