-- Crea la tabla donde se guardan los calculos de impuestos
create table if not exists calculos (
  id_calculo serial primary key,
  categoria varchar(20) not null,
  valor decimal not null check (valor >= 0),
  mililitros decimal not null default 0 check (mililitros >= 0),
  impuesto decimal not null check (impuesto >= 0),
  fecha timestamp not null default now()
);
