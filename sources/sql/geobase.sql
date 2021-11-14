create table regions (
    id serial not null primary key,
    parent_id integer references regions (id) on delete restrict,
    name text
);

create table cities (
    id serial not null primary key,
    name text,
    region_id integer not null references regions (id) on delete restrict
);
