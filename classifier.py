import joblib
import re

# ── Load the trained ML model ──────────────────────────────
model = joblib.load('chichewa_noun_classifier.pkl')

# ── Noun class information ──────────────────────────────────
CLASS_INFO = {
    'mu-a': {
        'full_name':    'Mu-A Class (Class 1/2)',
        'description':  'Nouns referring to people, human beings, and animate beings.',
        'singular_prefix': 'mu- / m-',
        'plural_prefix':   'a-',
        'examples':     ['munthu/anthu', 'mwana/ana', 'mtsikana/atsikana',
                         'mnyamata/anyamata', 'mlimi/alimi', 'mphunzitsi/aphunzitsi',
                         'mbusa/abusa', 'mlendo/alendo'],
    },
    'mu-mi': {
        'full_name':    'Mu-Mi Class (Class 3/4)',
        'description':  'Nouns referring to trees, plants, body parts, and some objects.',
        'singular_prefix': 'mu- / m-',
        'plural_prefix':   'mi-',
        'examples':     ['mtengo/mitengo', 'munda/minda', 'mutu/mitu',
                         'mudzi/midzi', 'mtsinje/mitsinje', 'msika/misika',
                         'mpando/mipando', 'mkono/mikono'],
    },
    'li-ma': {
        'full_name':    'Li-Ma Class (Class 5/6)',
        'description':  'Nouns referring to various objects, body parts, and abstract things.',
        'singular_prefix': 'li- / zero prefix',
        'plural_prefix':   'ma-',
        'examples':     ['buku/mabuku', 'dzina/maina', 'phiri/mapiri',
                         'boma/maboma', 'gulu/magulu', 'tsiku/masiku',
                         'diso/maso', 'fupa/mafupa'],
    },
    'chi-zi': {
        'full_name':    'Chi-Zi Class (Class 7/8)',
        'description':  'Nouns referring to things, concepts, and inanimate objects.',
        'singular_prefix': 'chi- / ch-',
        'plural_prefix':   'zi-',
        'examples':     ['chimbuzi/zimbuzi', 'chovala/zovala', 'chipinda/ziphinda',
                         'chipatala/zipatala', 'chitupa/zitupa', 'chaka/zaka',
                         'chibaluwa/zibaluwa', 'chombo/zombo'],
    },
    'i-zi': {
        'full_name':    'I-Zi Class (Class 9/10)',
        'description':  'Nouns referring to animals, loanwords, and many common nouns. Singular and plural are often the same.',
        'singular_prefix': 'n- / ny- / ng- / zero prefix',
        'plural_prefix':   'same as singular',
        'examples':     ['nyumba/nyumba', 'mbuzi/mbuzi', 'njovu/njovu',
                         'nkhuku/nkhuku', 'galimoto/galimoto', 'mbalame/mbalame',
                         'nyimbo/nyimbo', 'nsima/nsima'],
    },
    'u-ma': {
        'full_name':    'U-Ma Class (Class 11/6)',
        'description':  'Nouns referring to abstract concepts, qualities, and states.',
        'singular_prefix': 'u-',
        'plural_prefix':   'ma-',
        'examples':     ['udindo/maudindo', 'ulendo/maulendo', 'ufulu/maufulu',
                         'umoyo/maumoyo', 'ubale/maubale', 'ulimi/maulimi',
                         'uthenga/mauthenga', 'ululu/ululu'],
    },
    'ka-ti': {
        'full_name':    'Ka-Ti Class (Class 12/13)',
        'description':  'Diminutive nouns — small versions of things or beings.',
        'singular_prefix': 'ka-',
        'plural_prefix':   'ti-',
        'examples':     ['kamwana/tiana', 'kanthu/tinthu', 'kabuku/tibuku',
                         'kanyumba/tinyumba', 'kamunda/timunda', 'kaphiri/tiphiri',
                         'kachirombo/tichirombo', 'kakasu/tikasu'],
    },
    'ku-pa-mu': {
        'full_name':    'Ku-Pa-Mu Class (Class 17/18)',
        'description':  'Locative nouns — nouns referring to places and locations.',
        'singular_prefix': 'ku- / pa- / mu-',
        'plural_prefix':   'same as singular',
        'examples':     ['kumunda/kumunda', 'kunyumba/kunyumba', 'pamsika/pamsika',
                         'pabwalo/pabwalo', 'm\'nyumba/m\'nyumba', 'm\'mudzi/m\'mudzi',
                         'pachipinda/pachipinda', 'kumadzi/kumadzi'],
    },
    'ku+tsinde la mneni': {
        'full_name':    'Ku+Tsinde La Mneni (Infinitive Class)',
        'description':  'Verbal nouns — infinitive forms of verbs used as nouns.',
        'singular_prefix': 'ku-',
        'plural_prefix':   'same as singular',
        'examples':     ['kulima/kulima', 'kuphika/kuphika', 'kusewera/kusewera',
                         'kugona/kugona', 'kudya/kudya', 'kuimba/kuimba',
                         'kuyenda/kuyenda', 'kupita/kupita'],
    },
}

# ── Chichewa character patterns ─────────────────────────────
CHICHEWA_PATTERNS = [
    r'^(m|mu|mi|ma|chi|zi|ku|ka|ti|u|n|ny|ng|nk|nd|nj|mb|mp|mf|ph|th|kh|bv|dz|ts|ps|fw|pw|sw|tw|chw|khw|ngw|ndw|nyw|tsw).',
    r'(mba|mbo|mbu|mbi|nda|ndo|ndu|ndi|nja|njo|nju|nji|nka|nko|nku|nki|nga|ngo|ngu|ngi)',
    r'(ula|ulo|ulu|uli|ima|imo|imu|imi|ana|ano|anu|ani|ira|iro|iru|iri)',
    r'(tsa|tso|tsu|tsi|dza|dzo|dzu|dzi|pha|pho|phu|phi|tha|tho|thu|thi)',
    r'(wana|wira|wera|wala|wina|wika|wita|wiya)',
]

CHICHEWA_VOWEL_PATTERN = re.compile(r'^[aeiou]', re.IGNORECASE)
CHICHEWA_PREFIXES = [
    'mu', 'mi', 'ma', 'chi', 'zi', 'ku', 'ka', 'ti',
    'mw', 'ny', 'nk', 'nd', 'nj', 'ng', 'mb', 'mp',
    'mf', 'ph', 'th', 'kh', 'bv', 'dz', 'ts', 'ps',
    'ch', 'fw', 'pw', 'sw', 'tw', 'li', 'lo', 'la'
]

NON_CHICHEWA_PATTERNS = [
    r'[qx]',
    r'(tion|ness|ment|ling|ful|less|ous|ive|ble|ack|eck|ick|ock|uck)',
    r'^(the|and|for|was|his|her|are|but|not|you|all|can|had|her|was)',
    r'(aa|ee|ii|oo|uu)',
    r'(ck|ph|wh|gh|sh(?!a|e|i|o|u))',
    r'^[bcdfghjklmnpqrstvwxyz]{3,}(?![aeiou])',
]

KNOWN_CHICHEWA_WORDS = set()


# ── Rule-based classifier ────────────────────────────────────
def rule_based_classify(noun):
    noun = noun.lower().strip()
    confidence = 0
    predicted_class = None
    rule_used = None

    # Rule 1: starts with ku- + verb stem (infinitive)
    if noun.startswith('ku') and len(noun) > 4:
        predicted_class = 'ku+tsinde la mneni'
        confidence = 0.95
        rule_used = f"The noun starts with the prefix 'ku-' which is the infinitive marker in Chichewa. All verbal nouns (infinitives) belong to this class."

    # Rule 2: starts with ka- (diminutive)
    elif noun.startswith('ka') and len(noun) > 3:
        predicted_class = 'ka-ti'
        confidence = 0.90
        rule_used = f"The noun starts with the prefix 'ka-' which is the diminutive prefix in Chichewa. This class contains small versions of things."

    # Rule 3: starts with chi- or ch-
    elif noun.startswith('chi') or (noun.startswith('ch') and len(noun) > 3):
        predicted_class = 'chi-zi'
        confidence = 0.92
        rule_used = f"The noun starts with the prefix 'chi-' which is the class 7 singular prefix in Chichewa. This class contains things and inanimate objects."

    # Rule 4: starts with zi- (chi-zi plural)
    elif noun.startswith('zi') and len(noun) > 3:
        predicted_class = 'chi-zi'
        confidence = 0.88
        rule_used = f"The noun starts with the prefix 'zi-' which is the class 8 plural prefix in Chichewa. This is the plural form of chi-zi class."

    # Rule 5: starts with u- (u-ma abstract)
    elif noun.startswith('u') and not noun.startswith('um') and len(noun) > 3:
        predicted_class = 'u-ma'
        confidence = 0.85
        rule_used = f"The noun starts with the prefix 'u-' which marks abstract nouns in Chichewa. This class contains concepts, qualities, and states."

    # Rule 6: starts with ku- pa- mu- (locative)
    elif noun.startswith('pa') or noun.startswith('ku') and len(noun) <= 4:
        predicted_class = 'ku-pa-mu'
        confidence = 0.80
        rule_used = f"The noun starts with a locative prefix ('pa-' or 'ku-') indicating a place or location in Chichewa."

    return predicted_class, confidence, rule_used


# ── ML classifier ────────────────────────────────────────────
def ml_classify(noun):
    text = f"{noun} {noun} {noun[:2]} {noun[:3]} {noun[:4]} {noun[-2:]} {noun[-3:]}"
    prediction   = model.predict([text])[0]
    proba        = model.predict_proba([text])[0]
    classes_list = model.classes_
    confidence   = float(max(proba))
    return prediction, confidence, dict(zip(classes_list, proba))


# ── Non-Chichewa detector ────────────────────────────────────
def is_chichewa(noun):
    noun = noun.lower().strip()

    # very short words are inconclusive
    if len(noun) < 3:
        return True, "Word is too short to determine language"

    # check known non-Chichewa patterns
    for pattern in NON_CHICHEWA_PATTERNS:
        if re.search(pattern, noun, re.IGNORECASE):
            return False, f"The word contains the pattern '{re.search(pattern, noun, re.IGNORECASE).group()}' which is not found in Chichewa words"

    # check if it starts with a Chichewa prefix
    starts_with_chichewa = any(noun.startswith(p) for p in CHICHEWA_PREFIXES)

    # check if it matches Chichewa phonological patterns
    matches_chichewa = any(re.search(p, noun, re.IGNORECASE) for p in CHICHEWA_PATTERNS)

    if not starts_with_chichewa and not matches_chichewa:
        return False, "The word does not match any known Chichewa morphological or phonological patterns"

    return True, "Word matches Chichewa morphological patterns"


# ── Main hybrid classifier ───────────────────────────────────
def classify_noun(noun):
    noun = noun.lower().strip()

    # Step 1: check if Chichewa
    is_chi, lang_reason = is_chichewa(noun)

    # Step 2: rule-based classification
    rule_class, rule_conf, rule_explanation = rule_based_classify(noun)

    # Step 3: ML classification
    ml_class, ml_conf, all_proba = ml_classify(noun)

    # Step 4: hybrid decision
    if rule_class and rule_conf >= 0.88:
        final_class  = rule_class
        final_conf   = rule_conf
        method_used  = 'Rule-Based'
        explanation  = rule_explanation
    else:
        final_class  = ml_class
        final_conf   = ml_conf
        method_used  = 'Machine Learning'
        explanation  = generate_ml_explanation(noun, ml_class)

    # Step 5: get class info
    class_info = CLASS_INFO.get(final_class, {})

    # Step 6: morphological breakdown
    morphology = get_morphology(noun, final_class)

    return {
        'noun':         noun,
        'predicted':    final_class,
        'confidence':   round(final_conf * 100, 1),
        'method':       method_used,
        'explanation':  explanation,
        'is_chichewa':  is_chi,
        'lang_warning': None if is_chi else lang_reason,
        'class_info':   class_info,
        'morphology':   morphology,
        'all_scores':   {k: round(v*100, 1) for k, v in sorted(
                            all_proba.items(), key=lambda x: x[1], reverse=True)},
    }


# ── Explanation generator for ML results ────────────────────
def generate_ml_explanation(noun, predicted_class):
    explanations = {
        'mu-a': (
            f"The noun '{noun}' was classified as mu-a class by the machine learning model. "
            f"This class contains nouns referring to people and animate beings. "
            f"The model detected morphological patterns in the noun that are characteristic "
            f"of class 1/2 nouns in Chichewa — typically starting with mu- or m- in singular "
            f"and taking the a- prefix in plural form."
        ),
        'mu-mi': (
            f"The noun '{noun}' was classified as mu-mi class by the machine learning model. "
            f"This class contains nouns referring to trees, plants, and body parts. "
            f"The model detected that the noun follows the mu-/m- singular prefix pattern "
            f"and takes mi- in its plural form, which is characteristic of class 3/4 nouns."
        ),
        'li-ma': (
            f"The noun '{noun}' was classified as li-ma class by the machine learning model. "
            f"This is one of the largest noun classes in Chichewa, containing various objects "
            f"and abstract things. The model detected patterns suggesting the noun takes ma- "
            f"in its plural form, which is the defining feature of class 5/6 nouns."
        ),
        'chi-zi': (
            f"The noun '{noun}' was classified as chi-zi class by the machine learning model. "
            f"This class contains things and inanimate objects in Chichewa. "
            f"The model detected the chi- prefix pattern or phonological features "
            f"typical of class 7/8 nouns that take zi- in their plural form."
        ),
        'i-zi': (
            f"The noun '{noun}' was classified as i-zi class by the machine learning model. "
            f"This class contains animals, loanwords, and many common nouns. "
            f"A key feature of this class is that singular and plural forms are often identical. "
            f"The model detected phonological patterns — such as initial n-, ny-, or ng- clusters "
            f"— that are characteristic of class 9/10 nouns."
        ),
        'u-ma': (
            f"The noun '{noun}' was classified as u-ma class by the machine learning model. "
            f"This class contains abstract nouns representing concepts, qualities, and states. "
            f"The model detected the u- prefix pattern characteristic of class 11 abstract nouns "
            f"in Chichewa, which take ma- in their plural form."
        ),
        'ka-ti': (
            f"The noun '{noun}' was classified as ka-ti class by the machine learning model. "
            f"This is the diminutive class in Chichewa — nouns referring to small versions of things. "
            f"The model detected the ka- prefix pattern which marks diminutive nouns "
            f"in class 12/13, which take ti- in their plural form."
        ),
        'ku-pa-mu': (
            f"The noun '{noun}' was classified as ku-pa-mu class by the machine learning model. "
            f"This is the locative class in Chichewa — nouns referring to places and locations. "
            f"The model detected locative prefix patterns (ku-, pa-, or mu-) "
            f"that mark class 17/18 locative nouns."
        ),
        'ku+tsinde la mneni': (
            f"The noun '{noun}' was classified as ku+tsinde la mneni class by the machine learning model. "
            f"This class contains verbal nouns — infinitive forms of verbs used as nouns. "
            f"The model detected the ku- infinitive prefix which is the defining marker "
            f"of this class. These nouns do not change form in plural."
        ),
    }
    return explanations.get(predicted_class,
        f"The noun '{noun}' was classified as {predicted_class} class "
        f"based on its morphological features detected by the machine learning model.")


# ── Morphological breakdown ──────────────────────────────────
def get_morphology(noun, predicted_class):
    noun = noun.lower().strip()
    prefix = ''
    stem   = noun

    prefix_map = {
        'mu-a':               ['mu', 'm'],
        'mu-mi':              ['mu', 'm'],
        'li-ma':              ['li', 'l'],
        'chi-zi':             ['chi', 'ch'],
        'i-zi':               ['ny', 'n', 'ng', 'nk', 'nd', 'nj', 'mb', 'mp','im'],
        'u-ma':               ['u'],
        'ka-ti':              ['ka'],
        'ku-pa-mu':           ['ku', 'pa', 'mu'],
        'ku+tsinde la mneni': ['ku'],
    }

    prefixes_to_try = prefix_map.get(predicted_class, [])
    for p in prefixes_to_try:
        if noun.startswith(p) and len(noun) > len(p):
            prefix = p
            stem   = noun[len(p):]
            break

    suffix = stem[-2:] if len(stem) > 3 else ''
    root   = stem[:-2] if len(stem) > 3 else stem

    return {
        'prefix': prefix if prefix else '—',
        'root':   root   if root   else stem,
        'suffix': suffix if suffix else '—',
        'full':   noun,
    }