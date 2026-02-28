-- ============================================================
-- migration_001_create_tasks.sql
-- Crea la tabla `tasks` con RLS habilitado (acceso público
-- para esta demo; ajusta las políticas según tus necesidades).
-- ============================================================
-- Ejecutar en: Supabase Dashboard → SQL Editor → New Query
-- ============================================================


-- ----------------------------------------------------------
-- 1. Extensión UUID (ya suele estar habilitada)
-- ----------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


-- ----------------------------------------------------------
-- 2. Tabla principal
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.tasks (
  id          BIGINT        GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  completed   BOOLEAN       NOT NULL DEFAULT FALSE,
  created_at  TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  description TEXT,
  priority    TEXT          NOT NULL DEFAULT 'media'
                            CHECK (priority IN ('alta', 'media', 'baja')),
  title       TEXT          NOT NULL CHECK (char_length(title) BETWEEN 1 AND 120),
  updated_at  TIMESTAMPTZ
);

-- Índices de consulta frecuente
CREATE INDEX IF NOT EXISTS idx_tasks_completed  ON public.tasks (completed);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON public.tasks (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_tasks_priority   ON public.tasks (priority);


-- ----------------------------------------------------------
-- 3. Row Level Security
-- ----------------------------------------------------------
ALTER TABLE public.tasks ENABLE ROW LEVEL SECURITY;

-- Política: cualquier usuario anónimo puede leer y escribir
-- (ideal para demo; en producción usa auth.uid())
CREATE POLICY "allow_all_anon" ON public.tasks
  FOR ALL
  TO anon
  USING      (true)
  WITH CHECK (true);


-- ----------------------------------------------------------
-- 4. Trigger para actualizar updated_at automáticamente
-- ----------------------------------------------------------
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER trg_tasks_updated_at
  BEFORE UPDATE ON public.tasks
  FOR EACH ROW
  EXECUTE FUNCTION public.set_updated_at();
