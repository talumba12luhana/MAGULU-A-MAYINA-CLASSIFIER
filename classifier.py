"""
classifier.py
-------------
Consolidated classification module for the Chichewa Noun Classifier.

Provides:
  - CLASS_INFO       : metadata dict for all 9 noun classes
  - rule_classify()  : fast prefix/pattern rule-based classifier
  - ml_classify()    : scikit-learn pipeline classifier (lazy-loaded)
  - get_morphology() : morphological breakdown (prefix / root / suffix)

The ML model is loaded lazily on first use via model_loader.get_model().
No pandas, numpy, or scipy is imported here.
"""

import re
from model_loader import get_model

# ═══════════════════════════════════════════════════════════════════════════════
# CLASS METADATA
# ═══════════════════════════════════════════════════════════════════════════════

CLASS_INFO = {
    "mu-a": {
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
    "mu-mi": {
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
    "li-ma": {
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
    "chi-zi": {
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
    "i-zi": {
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
    "u-ma": {
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
    "ka-ti": {
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
    "ku-pa-mu": {
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
    "ku+tsinde la mneni": {
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
}

# ═══════════════════════════════════════════════════════════════════════════════
# RULE-BASED CLASSIFIER
# ═══════════════════════════════════════════════════════════════════════════════

def rule_classify(noun: str):
    """
    Apply morphological prefix rules to classify a Chichewa noun.

    Returns:
        (predicted_class, confidence, reason_string)
        predicted_class is None if no rule fires.
    """
    n = noun.lower().strip()

    # Rule 1 — infinitive prefix ku- (must be > 4 chars to avoid 'ku' alone)
    if n.startswith("ku") and len(n) > 4:
        return (
            "ku+tsinde la mneni",
            0.95,
            "starts with the infinitive prefix 'ku-'",
        )

    # Rule 2 — diminutive prefix ka-
    if n.startswith("ka") and len(n) > 3:
        return "ka-ti", 0.90, "starts with the diminutive prefix 'ka-'"

    # Rule 3 — class 7 prefix chi- / ch-
    if n.startswith("chi") or (n.startswith("ch") and len(n) > 3):
        return "chi-zi", 0.92, "starts with the class 7 prefix 'chi-'"

    # Rule 4 — class 8 plural prefix zi-
    if n.startswith("zi") and len(n) > 3:
        return "chi-zi", 0.88, "starts with the class 8 plural prefix 'zi-'"

    # Rule 5 — abstract noun prefix u- (exclude um- / ul- combos handled by ML)
    if (
        n.startswith("u")
        and not n.startswith("um")
        and not n.startswith("ul")
        and len(n) > 3
    ):
        return "u-ma", 0.85, "starts with the abstract noun prefix 'u-'"

    # Rule 6 — locative prefix pa-
    if n.startswith("pa") and len(n) > 3:
        return "ku-pa-mu", 0.82, "starts with the locative prefix 'pa-'"

    return None, 0.0, None


# ═══════════════════════════════════════════════════════════════════════════════
# ML CLASSIFIER
# ═══════════════════════════════════════════════════════════════════════════════

def _extract_features(noun: str) -> str:
    """
    Build the text feature string expected by the trained pipeline.
    Matches the feature extraction used during training.
    """
    n = noun.lower().strip()
    return f"{n} {n} {n[:2]} {n[:3]} {n[:4]} {n[-2:]} {n[-3:]}"


def ml_classify(noun: str):
    """
    Classify a noun using the trained scikit-learn pipeline.
    The model is loaded lazily on first call.

    Returns:
        (predicted_class, confidence_float, all_scores_dict)
    """
    model       = get_model()
    text        = _extract_features(noun)
    prediction  = model.predict([text])[0]
    proba       = model.predict_proba([text])[0]
    classes     = model.classes_
    confidence  = float(max(proba))
    all_scores  = dict(zip(classes, proba))
    return prediction, confidence, all_scores


# ═══════════════════════════════════════════════════════════════════════════════
# MORPHOLOGICAL BREAKDOWN
# ═══════════════════════════════════════════════════════════════════════════════

# Ordered from longest to shortest so e.g. 'nkh' is tried before 'nk' / 'n'.
_PREFIX_MAP = {
    "mu-a":               ["mu", "mw", "m"],
    "mu-mi":              ["mu", "mw", "m"],
    "li-ma":              ["li", "l"],
    "chi-zi":             ["chi", "ch"],
    "i-zi":               ["nkh", "mph", "ny", "nk", "nd", "nj",
                           "ng", "mb", "mp", "mf", "n"],
    "u-ma":               ["u"],
    "ka-ti":              ["ka"],
    "ku-pa-mu":           ["ku", "pa", "m'", "mu"],
    "ku+tsinde la mneni": ["ku"],
}


def get_morphology(noun: str, predicted_class: str) -> dict:
    """
    Break a noun into prefix / root / suffix for the given class.

    Returns a dict with keys: prefix, root, suffix, full.
    """
    n      = noun.lower().strip()
    prefix = ""
    stem   = n

    for p in _PREFIX_MAP.get(predicted_class, []):
        if n.startswith(p) and len(n) > len(p):
            prefix = p
            stem   = n[len(p):]
            break

    suffix = stem[-2:] if len(stem) > 3 else ""
    root   = stem[:-2] if len(stem) > 3 else stem

    return {
        "prefix": prefix if prefix else "—",
        "root":   root   if root   else stem,
        "suffix": suffix if suffix else "—",
        "full":   n,
    }