create extension if not exists pgcrypto;

create table if not exists billing_customers (
    id uuid primary key default gen_random_uuid(),
    user_id text not null unique,
    email text,
    country text,
    currency text,
    provider text,
    provider_customer_id text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists subscriptions (
    id uuid primary key default gen_random_uuid(),
    user_id text not null,
    provider text not null,
    provider_subscription_id text,
    product_id text not null,
    status text not null default 'pending',
    currency text,
    amount numeric(18,2),
    current_period_start timestamptz,
    current_period_end timestamptz,
    cancel_at_period_end boolean not null default false,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique(provider, provider_subscription_id)
);

create table if not exists payments (
    id uuid primary key default gen_random_uuid(),
    user_id text not null,
    provider text not null,
    provider_payment_id text,
    product_id text,
    amount numeric(18,2),
    currency text,
    status text not null default 'pending',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique(provider, provider_payment_id)
);

create table if not exists billing_events (
    id uuid primary key default gen_random_uuid(),
    provider text not null,
    event_id text not null,
    event_type text,
    payload jsonb not null,
    processed boolean not null default false,
    created_at timestamptz not null default now(),
    processed_at timestamptz,
    unique(provider, event_id)
);

create index if not exists idx_billing_customers_user
    on billing_customers(user_id);

create index if not exists idx_subscriptions_user
    on subscriptions(user_id);

create index if not exists idx_payments_user
    on payments(user_id);

create index if not exists idx_billing_events_provider
    on billing_events(provider);
