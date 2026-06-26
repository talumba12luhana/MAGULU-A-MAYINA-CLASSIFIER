# ── Class rules and explanations ────────────────────────────
CLASS_RULES = {
    'mu-a': {
        'singular_prefixes': ['mu', 'm', 'mw'],
        'plural_prefixes':   ['a'],
        'semantic':          'people, human beings, animate beings',
        'rule_explanation':  (
            "In Chichewa, the mu-a class (Class 1/2) contains nouns that refer to "
            "people and animate beings. The singular form takes the prefix mu- or m- "
            "and the plural form takes the prefix a-."
            #  For example: munthu (person) "
            # "becomes anthu (people), mwana (child) becomes ana (children), "
            # "mtsikana (girl) becomes atsikana (girls), mnyamata (boy) becomes "
            # "anyamata (boys), mlimi (farmer) becomes alimi (farmers), "
            # "mphunzitsi (teacher) becomes aphunzitsi (teachers)."
        ),
        'prefix_rule': "starts with mu-, m-, or mw- in singular form",
        'plural_rule': "takes a- prefix in plural form",
    },
    'mu-mi': {
        'singular_prefixes': ['mu', 'm', 'mw'],
        'plural_prefixes':   ['mi'],
        'semantic':          'trees, plants, body parts, some objects',
        'rule_explanation':  (
            "In Chichewa, the mu-mi class (Class 3/4) contains nouns that refer to "
            "trees, plants, body parts, and some objects. The singular form takes "
            "the prefix mu- or m- and the plural form takes the prefix mi-. "
            # "For example: mtengo (tree) becomes mitengo (trees), munda (garden) "
            # "becomes minda (gardens), mutu (head) becomes mitu (heads), "
            # "mudzi (village) becomes midzi (villages), mkono (hand) becomes "
            # "mikono (hands), mpando (chair) becomes mipando (chairs)."
        ),
        'prefix_rule': "starts with mu- or m- in singular form",
        'plural_rule': "takes mi- prefix in plural form",
    },
    'li-ma': {
        'singular_prefixes': ['li', 'l', ''],
        'plural_prefixes':   ['ma'],
        'semantic':          'various objects, body parts, abstract things',
        'rule_explanation':  (
            "In Chichewa, the li-ma class (Class 5/6) is one of the largest noun "
            "classes. It contains various objects, body parts, and abstract nouns. "
            "The singular form may have a li- prefix or no prefix at all (zero prefix) "
            "and the plural form takes ma-. "
            # For example: buku (book) becomes "
            # "mabuku (books), dzina (name) becomes maina (names), phiri (mountain) "
            # "becomes mapiri (mountains), tsiku (day) becomes masiku (days), "
            # "diso (eye) becomes maso (eyes), fupa (bone) becomes mafupa (bones), "
            # "boma (government) becomes maboma, gulu (group) becomes magulu."
        ),
        'prefix_rule': "may start with li-, l-, or have no prefix (zero prefix)",
        'plural_rule': "takes ma- prefix in plural form",
    },
    'chi-zi': {
        'singular_prefixes': ['chi', 'ch'],
        'plural_prefixes':   ['zi', 'z'],
        'semantic':          'things, concepts, inanimate objects',
        'rule_explanation':  (
            "In Chichewa, the chi-zi class (Class 7/8) contains nouns that refer to "
            "things, concepts, and inanimate objects. The singular form takes the "
            "prefix chi- and the plural form takes the prefix zi-. "
            # For example: "
            # "chimanga (maize) becomes zimanga, chovala (clothes) becomes zovala, "
            # "chipinda (room) becomes ziphinda, chipatala (hospital) becomes "
            # "zipatala, chaka (year) becomes zaka, chibaluwa (letter) becomes "
            # "zibaluwa, chombo (vessel) becomes zombo, chitupa (ID) becomes zitupa."
        ),
        'prefix_rule': "starts with chi- or ch- in singular form",
        'plural_rule': "takes zi- prefix in plural form",
    },
    'i-zi': {
        'singular_prefixes': ['ny', 'n', 'ng', 'nk', 'nd', 'nj', 'mb', 'mp', 'mf'],
        'plural_prefixes':   ['same as singular'],
        'semantic':          'animals, loanwords, common nouns',
        'rule_explanation':  (
            "In Chichewa, the i-zi class (Class 9/10) is a very common class that "
            "contains animals, loanwords, and many everyday nouns. A key feature of "
            "this class is that the singular and plural forms are often identical — "
            "the noun does not change. The class typically starts with nasal consonant "
            "clusters such as ny-, n-, ng-, nk-, nd-, nj-, mb-, or mp-. "
            # "For example: nyumba (house) stays nyumba in plural, mbuzi (goat) "
            # "stays mbuzi, njovu (elephant) stays njovu, nkhuku (chicken) stays "
            # "nkhuku, galimoto (car) stays galimoto, mbalame (bird) stays mbalame, "
            # "nyimbo (song) stays nyimbo, nsima (nsima) stays nsima."
        ),
        'prefix_rule': "starts with ny-, n-, ng-, nk-, nd-, nj-, mb-, or mp-",
        'plural_rule': "singular and plural forms are the same (no change)",
    },
    'u-ma': {
        'singular_prefixes': ['u'],
        'plural_prefixes':   ['ma'],
        'semantic':          'abstract concepts, qualities, states',
        'rule_explanation':  (
            "In Chichewa, the u-ma class (Class 11/6) contains abstract nouns that "
            "represent concepts, qualities, and states. The singular form takes the "
            "prefix u- and the plural form takes ma-. "
            # For example: udindo "
            # "(responsibility) becomes maudindo, ulendo (journey) becomes maulendo, "
            # "ufulu (freedom) becomes maufulu, umoyo (life) becomes maumoyo, "
            # "ubale (relationship) becomes maubale, ulimi (farming/tongue) becomes "
            # "maulimi, uthenga (message) becomes mauthenga, ululu (pain) stays ululu."
        ),
        'prefix_rule': "starts with u- in singular form",
        'plural_rule': "takes ma- prefix in plural form",
    },
    'ka-ti': {
        'singular_prefixes': ['ka'],
        'plural_prefixes':   ['ti'],
        'semantic':          'diminutives — small versions of things or beings',
        'rule_explanation':  (
            "In Chichewa, the ka-ti class (Class 12/13) is the diminutive class. "
            "It contains nouns that refer to small versions of things or beings. "
            "The singular form takes the prefix ka- and the plural form takes ti-. "
            # "For example: kamwana (small child) becomes tiana, kanthu (small thing) "
            # "becomes tinthu, kabuku (small book) becomes tibuku, kanyumba (small house) "
            # "becomes tinyumba, kamunda (small garden) becomes timunda, kaphiri "
            # "(small hill) becomes tiphiri, kachirombo (small creature) becomes "
            # "tichirombo, kakasu (small hoe) becomes tikasu."
        ),
        'prefix_rule': "starts with ka- in singular form",
        'plural_rule': "takes ti- prefix in plural form",
    },
    'ku-pa-mu': {
        'singular_prefixes': ['ku', 'pa', 'mu', "m'"],
        'plural_prefixes':   ['same as singular'],
        'semantic':          'locative — places and locations',
        'rule_explanation':  (
            "In Chichewa, the ku-pa-mu class (Class 17/18) is the locative class. "
            "It contains nouns that refer to places and locations. The class uses "
            "three locative prefixes: ku- (general location or direction), "
            "pa- (specific point or surface), and mu- or m'- (inside a place). "
            # "For example: kumunda (at the garden), kunyumba (at home), "
            # "pamsika (at the market), pabwalo (at the courtyard), "
            # "m'nyumba (inside the house), m'mudzi (inside the village), "
            # "pachipinda (inside the room), kumadzi (at the water)."
        ),
        'prefix_rule': "starts with ku-, pa-, mu-, or m'- as a locative marker",
        'plural_rule': "locative nouns do not change form",
    },
    'ku+tsinde la mneni': {
        'singular_prefixes': ['ku'],
        'plural_prefixes':   ['same as singular'],
        'semantic':          'verbal nouns — infinitive forms of verbs',
        'rule_explanation':  (
            "In Chichewa, the ku+tsinde la mneni class is the infinitive class. "
            "It contains verbal nouns — these are infinitive forms of verbs that "
            "are used as nouns. The defining feature is the ku- prefix at the "
            "start of every noun in this class. These nouns do not change in "
            "plural form. "
            # For example: kulima (farming/to farm), kuphika "
            # "(cooking/to cook), kusewera (playing/to play), kugona (sleeping/to sleep), "
            # "kudya (eating/to eat), kuimba (singing/to sing), kuyenda "
            # "(walking/to walk), kupita (going/to go), kubwera (coming/to come), "
            # "kulemba (writing/to write), kuwerenga (reading/to read)."
        ),
        'prefix_rule': "starts with ku- — the infinitive marker in Chichewa",
        'plural_rule': "verbal nouns do not change form in plural",
    },
}


def get_full_explanation(noun, predicted_class, method, confidence,
                         morphology, is_chichewa, lang_reason):
    """
    Generates a full structured explanation for why a noun
    belongs to a particular class.
    """
    info = CLASS_RULES.get(predicted_class, {})
    noun = noun.lower().strip()

    # ── build explanation sections ──────────────────────────
    sections = {}

    # 1. Summary
    sections['summary'] = (
        f"The noun '{noun}' has been classified as "
        f"<strong>{predicted_class}</strong> "
        f"({info.get('full_name', predicted_class)}) "
        f"with a confidence of <strong>{confidence}%</strong>. "
        # f"Classification was done using the "
        # f"<strong>{method}</strong> component of the hybrid system."
    )

    # 2. Why this class
    sections['why'] = info.get('rule_explanation', '')

    # 3. Prefix rule
    sections['prefix_rule'] = (
        f"Prefix pattern: This noun {info.get('prefix_rule', 'follows the expected prefix pattern')}."
    )

    # 4. Plural rule
    sections['plural_rule'] = (
        f"Plural pattern: In this class, the noun {info.get('plural_rule', 'follows the expected plural pattern')}."
    )

    # 5. Semantic category
    sections['semantic'] = (
        f"Semantic category: This class contains nouns referring to "
        f"{info.get('semantic', 'various nouns')}."
    )

    # 6. Morphological analysis
    sections['morphology'] = (
        f"Breaking down '{noun}': "
        f"Prefix = '{morphology['prefix']}', "
        f"Root = '{morphology['root']}', "
        f"Suffix = '{morphology['suffix']}'."
    )

    # 7. Method explanation
    if method == 'Rule-Based':
        sections['method_note'] = (
            f"This noun was classified using the rule-based component "
            f"because its prefix '{morphology['prefix']}' clearly matches "
            f"the morphological rules for the {predicted_class} class "
            f"with high confidence ({confidence}%). "
            # f"Rule-based classification is used when the noun follows "
            f"a clear and unambiguous morphological pattern."
        )
    else:
        sections['method_note'] = (
            # f"This noun was classified using the machine learning component "
            # f"because its morphological pattern was ambiguous or did not "
            # f"match a clear rule with high confidence. "
            # f"The Random Forest model analysed character n-gram patterns "
            f"in the noun and assigned it to the {predicted_class} class "
            f"with {confidence}% confidence based on patterns learned "
            f"from 1,000+ annotated Chichewa nouns."
        )

    # 8. Language verification
    if is_chichewa:
        sections['language'] = (
            f"Language check: '{noun}' was verified as a Chichewa word. "
            f"{lang_reason}"
        )
    else:
        sections['language'] = (
            f"Language warning: '{noun}' could not be verified as a "
            f"Chichewa word. {lang_reason} "
            f"Classification results may not be accurate."
        )

    return sections


def get_class_comparison(predicted_class, all_scores):
    """
    Generates a comparison note explaining why the noun
    was not classified into the other top classes.
    """
    sorted_scores = sorted(
        all_scores.items(), key=lambda x: x[1], reverse=True
    )

    comparison = []
    for cls, score in sorted_scores[:4]:
        if cls == predicted_class:
            comparison.append({
                'class':  cls,
                'score':  score,
                'note':   'Selected — highest confidence score',
                'status': 'selected',
            })
        elif score >= 15:
            comparison.append({
                'class':  cls,
                'score':  score,
                'note':   get_rejection_reason(predicted_class, cls),
                'status': 'close',
            })
        else:
            comparison.append({
                'class':  cls,
                'score':  score,
                'note':   'Low probability — morphological patterns do not match',
                'status': 'low',
            })

    return comparison


def get_rejection_reason(selected, other):
    """
    Explains why the other class was not selected.
    """
    reasons = {
        ('mu-a', 'mu-mi'): (
            "Not mu-mi because mu-mi nouns refer to trees and plants "
            "and take mi- in plural, while this noun refers to a person "
            "or animate being and takes a- in plural."
        ),
        ('mu-mi', 'mu-a'): (
            "Not mu-a because mu-a nouns refer to people and animate beings "
            "and take a- in plural, while this noun refers to a tree, plant, "
            "or object and takes mi- in plural."
        ),
        ('li-ma', 'i-zi'): (
            "Not i-zi because i-zi nouns typically have identical singular "
            "and plural forms, while this noun changes in plural by adding ma-."
        ),
        ('i-zi', 'li-ma'): (
            "Not li-ma because li-ma nouns take ma- in plural, "
            "while this noun keeps the same form in both singular and plural."
        ),
        ('chi-zi', 'i-zi'): (
            "Not i-zi because this noun starts with chi- which is the "
            "class 7 singular prefix, not a nasal cluster typical of i-zi."
        ),
        ('u-ma', 'mu-mi'): (
            "Not mu-mi because mu-mi nouns refer to trees and plants, "
            "while this noun starting with u- refers to an abstract concept."
        ),
        ('ku+tsinde la mneni', 'ku-pa-mu'): (
            "Not ku-pa-mu because this ku- noun is a verbal noun "
            "(infinitive form of a verb) not a locative place name."
        ),
        ('ku-pa-mu', 'ku+tsinde la mneni'): (
            "Not ku+tsinde la mneni because this noun refers to a place "
            "or location, not a verbal noun or infinitive form."
        ),
    }
    key = (selected, other)
    return reasons.get(
        key,
        f"Not {other} because the morphological features of this noun "
        f"more closely match the {selected} class pattern."
    )