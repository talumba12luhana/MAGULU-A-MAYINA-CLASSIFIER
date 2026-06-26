"""
database/migrate.py
-------------------
One-shot migration: CSV → SQLite.

Run from the project root:
    python -m database.migrate

Safe to re-run — uses INSERT OR IGNORE so existing rows are skipped.
The script seeds:
  1. noun_classes  — 9 rows of class metadata
  2. class_examples — curated examples for each class (from original CLASS_INFO)
  3. nouns         — all rows from chichewa_noun_dataset.csv (with typo fixes)
"""

import csv
import os
import pathlib

from sqlalchemy import text

# ── Locate files relative to this script ─────────────────────────────────────
BASE_DIR = pathlib.Path(__file__).parent.parent   # project root
SCHEMA    = pathlib.Path(__file__).parent / "schema.sql"
CSV_PATH  = BASE_DIR / "chichewa_noun_dataset.csv"

# ── Known class-column typos in the CSV ──────────────────────────────────────
TYPO_MAP = {
    "mumi":     "mu-mi",
    "i--zi":    "i-zi",
    "lima":     "li-ma",
    "u-":       "u-ma",
    "u":        "u-ma",
    "chii-zi":  "chi-zi",
    "chizi":    "chi-zi",
    "chu-zi":   "chi-zi",
    "ch-zi":    "chi-zi",
}

# ── Valid class keys (anything else is skipped) ───────────────────────────────
VALID_CLASSES = {
    "mu-a", "mu-mi", "li-ma", "chi-zi",
    "i-zi", "u-ma", "ka-ti", "ku-pa-mu",
    "ku+tsinde la mneni",
}

# ── Class metadata seed data (from CLASS_INFO in app.py) ─────────────────────
CLASS_SEED = [
    {
        "class_key":       "mu-a",
        "full_name":       "Mu-A Class (Class 1/2)",
        "description":     "People and animate beings",
        "singular_prefix": "mu- / m- / mw-",
        "plural_prefix":   "a-",
        "colour":          "#1A5C20",
        "examples": [
            "munthu/anthu", "mwana/ana", "mtsikana/atsikana",
            "mnyamata/anyamata", "mlimi/alimi",
            "mphunzitsi/aphunzitsi", "mbusa/abusa", "mlendo/alendo",
        ],
    },
    {
        "class_key":       "mu-mi",
        "full_name":       "Mu-Mi Class (Class 3/4)",
        "description":     "Trees, plants, body parts",
        "singular_prefix": "mu- / m-",
        "plural_prefix":   "mi-",
        "colour":          "#0D6B6E",
        "examples": [
            "mtengo/mitengo", "munda/minda", "mutu/mitu",
            "mudzi/midzi", "mtsinje/mitsinje", "msika/misika",
            "mpando/mipando", "mkono/mikono",
        ],
    },
    {
        "class_key":       "li-ma",
        "full_name":       "Li-Ma Class (Class 5/6)",
        "description":     "Various objects and abstract things",
        "singular_prefix": "li- / zero prefix",
        "plural_prefix":   "ma-",
        "colour":          "#6B2D8B",
        "examples": [
            "buku/mabuku", "dzina/maina", "phiri/mapiri",
            "boma/maboma", "gulu/magulu", "tsiku/masiku",
            "diso/maso", "fupa/mafupa",
        ],
    },
    {
        "class_key":       "chi-zi",
        "full_name":       "Chi-Zi Class (Class 7/8)",
        "description":     "Things and inanimate objects",
        "singular_prefix": "chi- / ch-",
        "plural_prefix":   "zi-",
        "colour":          "#B54708",
        "examples": [
            "chimanga/zimanga", "chovala/zovala",
            "chipinda/ziphinda", "chipatala/zipatala",
            "chaka/zaka", "chibaluwa/zibaluwa",
            "chombo/zombo", "chitupa/zitupa",
        ],
    },
    {
        "class_key":       "i-zi",
        "full_name":       "I-Zi Class (Class 9/10)",
        "description":     "Animals, loanwords, common nouns",
        "singular_prefix": "ny- / n- / ng- / nk- / nd- / zero prefix",
        "plural_prefix":   "same as singular",
        "colour":          "#1565C0",
        "examples": [
            "nyumba/nyumba", "mbuzi/mbuzi", "njovu/njovu",
            "nkhuku/nkhuku", "galimoto/galimoto",
            "mbalame/mbalame", "nyimbo/nyimbo", "nsima/nsima",
        ],
    },
    {
        "class_key":       "u-ma",
        "full_name":       "U-Ma Class (Class 11/6)",
        "description":     "Abstract concepts and qualities",
        "singular_prefix": "u-",
        "plural_prefix":   "ma-",
        "colour":          "#7B1FA2",
        "examples": [
            "udindo/maudindo", "ulendo/maulendo",
            "ufulu/maufulu", "umoyo/maumoyo",
            "ubale/maubale", "ulimi/maulimi",
            "uthenga/mauthenga", "ululu/ululu",
        ],
    },
    {
        "class_key":       "ka-ti",
        "full_name":       "Ka-Ti Class (Class 12/13)",
        "description":     "Diminutives — small versions of things",
        "singular_prefix": "ka-",
        "plural_prefix":   "ti-",
        "colour":          "#2D6A1F",
        "examples": [
            "kamwana/tiana", "kanthu/tinthu",
            "kabuku/tibuku", "kanyumba/tinyumba",
            "kamunda/timunda", "kaphiri/tiphiri",
            "kachirombo/tichirombo", "kakasu/tikasu",
        ],
    },
    {
        "class_key":       "ku-pa-mu",
        "full_name":       "Ku-Pa-Mu Class (Class 17/18)",
        "description":     "Locative — places and locations",
        "singular_prefix": "ku- / pa- / mu- / m'-",
        "plural_prefix":   "same as singular",
        "colour":          "#C62828",
        "examples": [
            "kumunda/kumunda", "kunyumba/kunyumba",
            "pamsika/pamsika", "pabwalo/pabwalo",
            "m'nyumba/m'nyumba", "m'mudzi/m'mudzi",
            "pachipinda/pachipinda", "kumadzi/kumadzi",
        ],
    },
    {
        "class_key":       "ku+tsinde la mneni",
        "full_name":       "Ku+Tsinde La Mneni (Infinitive)",
        "description":     "Verbal nouns — infinitive forms of verbs",
        "singular_prefix": "ku-",
        "plural_prefix":   "same as singular",
        "colour":          "#4E342E",
        "examples": [
            "kulima/kulima", "kuphika/kuphika",
            "kusewera/kusewera", "kugona/kugona",
            "kudya/kudya", "kuimba/kuimba",
            "kuyenda/kuyenda", "kupita/kupita",
        ],
    },
]


def run():
    # Import here so the script can be run standalone without a Flask app.
    from database.db import get_engine
    engine = get_engine()

    print("=" * 55)
    print("  Chichewa Classifier — Database Migration")
    print("=" * 55)

    with engine.begin() as conn:
        # ── 1. Create tables ─────────────────────────────────
        print("\n[1/3] Creating tables from schema.sql ...")
        schema_sql = SCHEMA.read_text(encoding="utf-8")
        # SQLAlchemy executes one statement at a time
        for statement in schema_sql.split(";"):
            stmt = statement.strip()
            if stmt:
                conn.execute(text(stmt))
        print("      Tables created (or already exist).")

        # ── 2. Seed noun_classes + class_examples ─────────────
        print("\n[2/3] Seeding noun_classes and class_examples ...")
        classes_inserted  = 0
        examples_inserted = 0

        for cls in CLASS_SEED:
            result = conn.execute(
                text("""
                    INSERT OR IGNORE INTO noun_classes
                        (class_key, full_name, description,
                         singular_prefix, plural_prefix, colour)
                    VALUES
                        (:class_key, :full_name, :description,
                         :singular_prefix, :plural_prefix, :colour)
                """),
                {k: cls[k] for k in
                 ("class_key", "full_name", "description",
                  "singular_prefix", "plural_prefix", "colour")},
            )
            if result.rowcount:
                classes_inserted += 1

            for example in cls["examples"]:
                result = conn.execute(
                    text("""
                        INSERT OR IGNORE INTO class_examples (class_key, example)
                        VALUES (:ck, :ex)
                    """),
                    {"ck": cls["class_key"], "ex": example},
                )
                if result.rowcount:
                    examples_inserted += 1

        print(f"      noun_classes : {classes_inserted} inserted "
              f"(skipped existing)")
        print(f"      class_examples: {examples_inserted} inserted "
              f"(skipped existing)")

        # ── 3. Migrate CSV → nouns table ──────────────────────
        print(f"\n[3/3] Migrating CSV: {CSV_PATH} ...")

        if not CSV_PATH.exists():
            print(f"      ERROR: CSV not found at {CSV_PATH}")
            return

        nouns_inserted = 0
        nouns_skipped  = 0
        nouns_invalid  = 0

        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                singular = row.get("singular nouns", "").strip().lower()
                plural   = row.get("plural nouns",   "").strip().lower()
                cls_raw  = row.get("class",           "").strip().lower()

                # Skip blank rows
                if not singular or not plural or not cls_raw:
                    nouns_skipped += 1
                    continue

                # Fix typos
                cls_key = TYPO_MAP.get(cls_raw, cls_raw)

                # Skip rows with unrecognised class
                if cls_key not in VALID_CLASSES:
                    print(f"      WARN: unknown class '{cls_raw}' "
                          f"for '{singular}' — skipped")
                    nouns_invalid += 1
                    continue

                result = conn.execute(
                    text("""
                        INSERT OR IGNORE INTO nouns (singular, plural, class_key)
                        VALUES (:s, :p, :ck)
                    """),
                    {"s": singular, "p": plural, "ck": cls_key},
                )
                if result.rowcount:
                    nouns_inserted += 1
                else:
                    nouns_skipped += 1

        print(f"      nouns inserted : {nouns_inserted}")
        print(f"      nouns skipped  : {nouns_skipped}  (duplicates)")
        print(f"      nouns invalid  : {nouns_invalid}  (bad class label)")

    print("\n[OK] Migration complete.")
    print(f"  Database: {os.path.abspath('chichewa.db')}\n")


if __name__ == "__main__":
    run()
