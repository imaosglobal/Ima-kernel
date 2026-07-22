create table if not exists users (
 id uuid primary key,
 email text unique,
 created_at timestamp default now()
);

create table if not exists conversations (
 id uuid primary key,
 user_id uuid references users(id),
 message text,
 response text,
 created_at timestamp default now()
);

create table if not exists memory (
 id uuid primary key,
 user_id uuid references users(id),
 data jsonb,
 created_at timestamp default now()
);

create table if not exists preferences (
 id uuid primary key,
 user_id uuid references users(id),
 data jsonb
);
