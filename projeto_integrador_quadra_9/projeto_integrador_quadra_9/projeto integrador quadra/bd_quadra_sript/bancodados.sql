create database if not exists db_quadra;
use db_quadra;
create table if not exists usuarios(id integer , 
								  nome varchar(250) not null,
								  cpf varchar(11) primary key not null ,
								  telefone varchar(20) not null,
								  email varchar(80) unique not null,
								  senha varchar(256) not null,
                                  grupo integer not null) ;
select * from usuarios;

create table if not exists agenda(id integer auto_increment primary key,
								 tipo_quadra varchar(100) ,
								  data date,
								  horario varchar(30),
								  valor double);
create table if not exists pagamentos(id integer auto_increment primary key ,
                                      valor_pagamento double,
                                      data date,
                                      id_agendamento integer,
                                      foreign key (id_agendamento) references agenda(id));

select * from pagamentos;
select * from agenda;
alter table agenda add column email varchar(80);
alter table agenda add foreign key (email) references usuarios(email);
alter table agenda add column pagamento boolean default false;




# administrador email: admin@admin.com  senha:123456