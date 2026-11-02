-- Exemplo para projeto novo; revise antes de executar no SQL Editor.
-- Uma tabela existente não é alterada por CREATE TABLE IF NOT EXISTS.
create table if not exists public.historico_pesquisas (
  id bigint generated always as identity primary key,
  nome_operador text not null,
  departamento text not null,
  termo_pesquisado text not null,
  data_hora text not null default to_char(now() at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"Z"')
);

-- Configure políticas RLS adequadas antes de disponibilizar os dados.
alter table public.historico_pesquisas enable row level security;

select departamento, count(*) as total_pesquisas
from public.historico_pesquisas
group by departamento
order by total_pesquisas desc;
