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

INSERT INTO reminders (title, comment, remind_at, notify_email, is_notified)
VALUES
    ('帰りに〇〇へ行く', '〇分前には会社を出る', '2026-06-01 18:00:00+09', 'sample@sample.co.jp', '1'),
    ('〇〇を買う', NULL, '2026-06-02 09:00:00+09', 'sample@sample.co.jp', '0');