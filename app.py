from flask import Flask, render_template, request, jsonify
import joblib
import re
import pandas as pd
from detector import detect_language
from explainer import get_full_explanation, get_class_comparison
import os
import pandas as pd

app = Flask(__name__)

# ── Load model and dataset ───────────────────────────────────
model   = joblib.load('chichewa_noun_classifier.pkl')
dataset = pd.read_csv('chichewa_noun_dataset.csv')
dataset = dataset[['singular nouns', 'plural nouns', 'class']].dropna()
dataset['singular nouns'] = dataset['singular nouns'].str.lower().str.strip()
dataset['plural nouns']   = dataset['plural nouns'].str.lower().str.strip()
dataset['class']          = dataset['class'].str.lower().str.strip()

# fix typos in dataset
dataset.loc[dataset['class'] == 'mumi',    'class'] = 'mu-mi'
dataset.loc[dataset['class'] == 'i--zi',   'class'] = 'i-zi'
dataset.loc[dataset['class'] == 'lima',    'class'] = 'li-ma'
dataset.loc[dataset['class'] == 'u-',      'class'] = 'u-ma'
dataset.loc[dataset['class'] == 'chii-zi', 'class'] = 'chi-zi'

# ── Class full information ───────────────────────────────────
CLASS_INFO = {
    'mu-a': {
        'full_name':   'Mu-A Class (Class 1/2)',
        'description': 'People and animate beings',
        'singular_prefix': 'mu- / m- / mw-',
        'plural_prefix':   'a-',
        'colour':      '#1A5C20',
        'examples':    ['munthu/anthu', 'mwana/ana', 'mtsikana/atsikana',
                        'mnyamata/anyamata', 'mlimi/alimi',
                        'mphunzitsi/aphunzitsi', 'mbusa/abusa', 'mlendo/alendo'],
    },
    'mu-mi': {
        'full_name':   'Mu-Mi Class (Class 3/4)',
        'description': 'Trees, plants, body parts',
        'singular_prefix': 'mu- / m-',
        'plural_prefix':   'mi-',
        'colour':      '#0D6B6E',
        'examples':    ['mtengo/mitengo', 'munda/minda', 'mutu/mitu',
                        'mudzi/midzi', 'mtsinje/mitsinje', 'msika/misika',
                        'mpando/mipando', 'mkono/mikono'],
    },
    'li-ma': {
        'full_name':   'Li-Ma Class (Class 5/6)',
        'description': 'Various objects and abstract things',
        'singular_prefix': 'li- / zero prefix',
        'plural_prefix':   'ma-',
        'colour':      '#6B2D8B',
        'examples':    ['buku/mabuku', 'dzina/maina', 'phiri/mapiri',
                        'boma/maboma', 'gulu/magulu', 'tsiku/masiku',
                        'diso/maso', 'fupa/mafupa'],
    },
    'chi-zi': {
        'full_name':   'Chi-Zi Class (Class 7/8)',
        'description': 'Things and inanimate objects',
        'singular_prefix': 'chi- / ch-',
        'plural_prefix':   'zi-',
        'colour':      '#B54708',
        'examples':    ['chimanga/zimanga', 'chovala/zovala',
                        'chipinda/ziphinda', 'chipatala/zipatala',
                        'chaka/zaka', 'chibaluwa/zibaluwa',
                        'chombo/zombo', 'chitupa/zitupa'],
    },
    'i-zi': {
        'full_name':   'I-Zi Class (Class 9/10)',
        'description': 'Animals, loanwords, common nouns',
        'singular_prefix': 'ny- / n- / ng- / nk- / nd- / zero prefix',
        'plural_prefix':   'same as singular',
        'colour':      '#1565C0',
        'examples':    ['nyumba/nyumba', 'mbuzi/mbuzi', 'njovu/njovu',
                        'nkhuku/nkhuku', 'galimoto/galimoto',
                        'mbalame/mbalame', 'nyimbo/nyimbo', 'nsima/nsima'],
    },
    'u-ma': {
        'full_name':   'U-Ma Class (Class 11/6)',
        'description': 'Abstract concepts and qualities',
        'singular_prefix': 'u-',
        'plural_prefix':   'ma-',
        'colour':      '#7B1FA2',
        'examples':    ['udindo/maudindo', 'ulendo/maulendo',
                        'ufulu/maufulu', 'umoyo/maumoyo',
                        'ubale/maubale', 'ulimi/maulimi',
                        'uthenga/mauthenga', 'ululu/ululu'],
    },
    'ka-ti': {
        'full_name':   'Ka-Ti Class (Class 12/13)',
        'description': 'Diminutives — small versions of things',
        'singular_prefix': 'ka-',
        'plural_prefix':   'ti-',
        'colour':      '#2D6A1F',
        'examples':    ['kamwana/tiana', 'kanthu/tinthu',
                        'kabuku/tibuku', 'kanyumba/tinyumba',
                        'kamunda/timunda', 'kaphiri/tiphiri',
                        'kachirombo/tichirombo', 'kakasu/tikasu'],
    },
    'ku-pa-mu': {
        'full_name':   'Ku-Pa-Mu Class (Class 17/18)',
        'description': 'Locative — places and locations',
        'singular_prefix': 'ku- / pa- / mu- / m\'-',
        'plural_prefix':   'same as singular',
        'colour':      '#C62828',
        'examples':    ['kumunda/kumunda', 'kunyumba/kunyumba',
                        'pamsika/pamsika', 'pabwalo/pabwalo',
                        "m'nyumba/m'nyumba", "m'mudzi/m'mudzi",
                        'pachipinda/pachipinda', 'kumadzi/kumadzi'],
    },
    'ku+tsinde la mneni': {
        'full_name':   'Ku+Tsinde La Mneni (Infinitive)',
        'description': 'Verbal nouns — infinitive forms of verbs',
        'singular_prefix': 'ku-',
        'plural_prefix':   'same as singular',
        'colour':      '#4E342E',
        'examples':    ['kulima/kulima', 'kuphika/kuphika',
                        'kusewera/kusewera', 'kugona/kugona',
                        'kudya/kudya', 'kuimba/kuimba',
                        'kuyenda/kuyenda', 'kupita/kupita'],
    },
}

# ── Rule-based classifier ────────────────────────────────────
def rule_classify(noun):
    n = noun.lower().strip()
    if n.startswith('ku') and len(n) > 4:
        return 'ku+tsinde la mneni', 0.95, \
               f"starts with the infinitive prefix 'ku-'"
    if n.startswith('ka') and len(n) > 3:
        return 'ka-ti', 0.90, \
               f"starts with the diminutive prefix 'ka-'"
    if n.startswith('chi') or (n.startswith('ch') and len(n) > 3):
        return 'chi-zi', 0.92, \
               f"starts with the class 7 prefix 'chi-'"
    if n.startswith('zi') and len(n) > 3:
        return 'chi-zi', 0.88, \
               f"starts with the class 8 plural prefix 'zi-'"
    if (n.startswith('u') and not n.startswith('um')
            and not n.startswith('ul') and len(n) > 3):
        return 'u-ma', 0.85, \
               f"starts with the abstract noun prefix 'u-'"
    if n.startswith('pa') and len(n) > 3:
        return 'ku-pa-mu', 0.82, \
               f"starts with the locative prefix 'pa-'"
    return None, 0.0, None


# ── Feature extraction ────────────────────────────────────────
def extract_text(noun):
    n = noun.lower().strip()
    return (f"{n} {n} {n[:2]} {n[:3]} {n[:4]} "
            f"{n[-2:]} {n[-3:]}")


# ── ML classifier ─────────────────────────────────────────────
def ml_classify(noun):
    text        = extract_text(noun)
    prediction  = model.predict([text])[0]
    proba       = model.predict_proba([text])[0]
    classes     = model.classes_
    confidence  = float(max(proba))
    all_scores  = dict(zip(classes, proba))
    return prediction, confidence, all_scores


# ── Morphology breakdown ──────────────────────────────────────
def get_morphology(noun, predicted_class):
    n = noun.lower().strip()
    prefix_map = {
        'mu-a':               ['mu', 'mw', 'm'],
        'mu-mi':              ['mu', 'mw', 'm'],
        'li-ma':              ['li', 'l'],
        'chi-zi':             ['chi', 'ch'],
        'i-zi':               ['ny', 'nkh', 'nk', 'nd', 'nj',
                                'ng', 'mb', 'mp', 'mf', 'n'],
        'u-ma':               ['u'],
        'ka-ti':              ['ka'],
        'ku-pa-mu':           ['ku', 'pa', "m'", 'mu'],
        'ku+tsinde la mneni': ['ku'],
    }
    for p in prefix_map.get(predicted_class, []):
        if n.startswith(p) and len(n) > len(p):
            stem   = n[len(p):]
            suffix = stem[-2:] if len(stem) > 3 else ''
            root   = stem[:-2] if len(stem) > 3 else stem
            return {'prefix': p, 'root': root,
                    'suffix': suffix, 'full': n}
    return {'prefix': '—', 'root': n, 'suffix': '—', 'full': n}


# ── Get dataset examples for predicted class ──────────────────
def get_examples(predicted_class, noun, n=6):
    subset = dataset[dataset['class'] == predicted_class]
    subset = subset[subset['singular nouns'] != noun.lower().strip()]
    sample = subset.sample(
        min(n, len(subset)), random_state=42
    ) if len(subset) > 0 else subset
    return [
        f"{row['singular nouns']} / {row['plural nouns']}"
        for _, row in sample.iterrows()
    ]


# ══════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/classify', methods=['POST'])
def classify():
    noun = request.form.get('noun', '').strip()

    if not noun:
        return render_template('index.html',
                               error="Please enter a Chichewa noun.")

    if len(noun) < 2:
        return render_template('index.html',
                               error="Please enter a longer noun.")

    # ── language detection ──
    lang_result = detect_language(noun)

    if not lang_result['is_chichewa']:
        return render_template(
            'index.html',
            error=f'"{noun}" is not a valid Chichewa noun.'
        )

    # ── rule-based classification ──
    rule_class, rule_conf, rule_reason = rule_classify(noun)

    # ── ML classification ──
    ml_class, ml_conf, all_scores = ml_classify(noun)

    # ── hybrid decision ──
    if rule_class and rule_conf >= 0.88:
        predicted   = rule_class
        confidence  = round(rule_conf * 100, 1)
        method      = 'Rule-Based'
    else:
        predicted   = ml_class
        confidence  = round(ml_conf * 100, 1)
        method      = 'Machine Learning'

    # ── morphology ──
    morphology = get_morphology(noun, predicted)

    # ── full explanation ──
    explanation = get_full_explanation(
        noun, predicted, method, confidence,
        morphology, lang_result['is_chichewa'],
        lang_result['reason']
    )

    # ── class comparison ──
    all_scores_pct = {
        k: round(v * 100, 1) for k, v in all_scores.items()
    }
    comparison = get_class_comparison(predicted, all_scores_pct)

    # ── examples from dataset ──
    examples = get_examples(predicted, noun)

    # ── class info ──
    class_info = CLASS_INFO.get(predicted, {})

    return render_template('result.html',
        noun        = noun,
        predicted   = predicted,
        confidence  = confidence,
        method      = method,
        explanation = explanation,
        morphology  = morphology,
        comparison  = comparison,
        examples    = examples,
        class_info  = class_info,
        lang_result = lang_result,
        all_scores  = all_scores_pct,
    )


@app.route('/classes')
def classes():
    return render_template('classes.html',
                           class_info=CLASS_INFO,
                           dataset=dataset)


@app.route('/api/classify', methods=['POST'])
def api_classify():
    data = request.get_json()
    noun = data.get('noun', '').strip()
    if not noun:
        return jsonify({'error': 'No noun provided'}), 400
    lang_result              = detect_language(noun)
    rule_class, rule_conf, _ = rule_classify(noun)
    ml_class, ml_conf, scores = ml_classify(noun)
    if rule_class and rule_conf >= 0.88:
        predicted  = rule_class
        confidence = round(rule_conf * 100, 1)
        method     = 'Rule-Based'
    else:
        predicted  = ml_class
        confidence = round(ml_conf * 100, 1)
        method     = 'Machine Learning'
    return jsonify({
        'noun':        noun,
        'predicted':   predicted,
        'confidence':  confidence,
        'method':      method,
        'is_chichewa': lang_result['is_chichewa'],
        'warning':     lang_result['warnings'],
        'class_info':  CLASS_INFO.get(predicted, {}),
    })


if __name__ == '__main__':
    print("=" * 50)
    print(" ChiNgeli — Chichewa Noun Classifier")
    print(" Open browser: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)