CREATE TABLE reminders (
    id bigserial not null PRIMARY KEY,
    title text not null,
    comment TEXT,
    remind_at timestamptz not null,
    notify_email VARCHAR(256) not null,
    is_notified boolean not null default false,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

INSERT INTO reminders (id, title, comment, remind_at, notify_email, is_notified)
VALUES
    ('001', '帰りに〇〇へ行く', '〇分前には会社を出る', '2026-06-01 18:00:00', 'sample@sample.co.jp', '1'),
    ('002', '〇〇を買う', NULL, '2026-06-02 9:00:00', 'sample@sample.co.jp', '0');