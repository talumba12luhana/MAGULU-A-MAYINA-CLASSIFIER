-- ============================================================
-- Chichewa Noun Classifier — SQLite Schema
-- ============================================================

-- noun_classes: one row per Chichewa noun class (9 total)
CREATE TABLE IF NOT EXISTS noun_classes (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    class_key        TEXT NOT NULL UNIQUE,   -- e.g. 'mu-a'
    full_name        TEXT NOT NULL,          -- e.g. 'Mu-A Class (Class 1/2)'
    description      TEXT NOT NULL,
    singular_prefix  TEXT NOT NULL,
    plural_prefix    TEXT NOT NULL,
    colour           TEXT NOT NULL           -- hex colour used in the UI
);

-- nouns: migrated from chichewa_noun_dataset.csv (1,016 rows)
CREATE TABLE IF NOT EXISTS nouns (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    singular    TEXT NOT NULL,
    plural      TEXT NOT NULL,
    class_key   TEXT NOT NULL REFERENCES noun_classes(class_key)
);

-- Indexes for fast lookup
CREATE INDEX IF NOT EXISTS idx_nouns_class_key  ON nouns (class_key);
CREATE INDEX IF NOT EXISTS idx_nouns_singular   ON nouns (singular);

-- class_examples: hand-curated examples shown in the UI (from CLASS_INFO)
CREATE TABLE IF NOT EXISTS class_examples (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    class_key   TEXT NOT NULL REFERENCES noun_classes(class_key),
    example     TEXT NOT NULL    -- e.g. 'munthu/anthu'
);
