CREATE TABLE reminders (
    id bigserial not null PRIMARY KEY,
    name VARCHAR(100) not null,
    title text not null,
    comment TEXT,
    remind_at timestamptz not null,
    notify_email VARCHAR(256) not null,
    is_notified boolean not null default false,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);