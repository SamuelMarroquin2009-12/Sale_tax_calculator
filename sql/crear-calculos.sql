-- Crea la tabla donde se guardan los calculos de impuestos
-- El id es un uuid (un codigo unico que genera la base de datos) y no un numero autoincremental:
-- los autonumericos (serial) se evitan porque causan problemas cuando el sistema crece
-- gen_random_uuid() viene incluido en PostgreSQL 13 o superior
create table if not exists calculos (
  id_calculo uuid primary key default gen_random_uuid(),
  categoria varchar(20) not null,
  valor decimal not null check (valor >= 0),
  mililitros decimal not null default 0 check (mililitros >= 0),
  impuesto decimal not null check (impuesto >= 0),
  fecha timestamp not null default now()
);
