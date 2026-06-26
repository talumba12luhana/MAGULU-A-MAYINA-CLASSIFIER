import re

# ── Known Chichewa word endings ──────────────────────────────
CHICHEWA_ENDINGS = [
    'a', 'o', 'e', 'i',
    'la', 'lo', 'li', 'le',
    'ra', 'ro', 'ri', 're',
    'na', 'no', 'ni', 'ne',
    'ma', 'mo', 'mi', 'me',
    'wa', 'wo', 'wi', 'we',
    'ka', 'ko', 'ki', 'ke',
    'ta', 'to', 'ti', 'te',
    'ba', 'bo', 'bi', 'be',
    'pa', 'po', 'pi', 'pe',
    'za', 'zo', 'zi', 'ze',
    'sa', 'so', 'si', 'se',
    'da', 'do', 'di', 'de',
    'ga', 'go', 'gi', 'ge',
    'fa', 'fo', 'fi', 'fe',
    'nda', 'ndo', 'ndi', 'nde',
    'mba', 'mbo', 'mbi', 'mbe',
    'nja', 'njo', 'nji', 'nje',
    'nga', 'ngo', 'ngi', 'nge',
    'nka', 'nko', 'nki', 'nke',
    'pha', 'pho', 'phi', 'phe',
    'tha', 'tho', 'thi', 'the',
    'kha', 'kho', 'khi', 'khe',
    'tsa', 'tso', 'tsi', 'tse',
    'dza', 'dzo', 'dzi', 'dze',
    'bva', 'bvo', 'bvi', 'bve',
    'wera', 'wira', 'wala', 'wina',
    'rana', 'rona', 'rina', 'rena',
    'lana', 'lona', 'lina', 'lena',
    'tana', 'tona', 'tina', 'tena',
    'kana', 'kona', 'kina', 'kena',
    'nana', 'nona', 'nina', 'nena',
    'sama', 'soma', 'sima', 'sema',
    'zana', 'zona', 'zina', 'zena',
]

# ── Known Chichewa prefixes ──────────────────────────────────
CHICHEWA_PREFIXES = [
    'mu', 'mi', 'ma', 'chi', 'zi',
    'ku', 'ka', 'ti', 'mw', 'ny',
    'nk', 'nd', 'nj', 'ng', 'mb',
    'mp', 'mf', 'ph', 'th', 'kh',
    'bv', 'dz', 'ts', 'ps', 'ch',
    'fw', 'pw', 'sw', 'tw', 'li',
    'lo', 'la', 'nkh', 'ndz', 'chw',
    'khw', 'ngw', 'ndw', 'nyw', 'tsw',
    'mphw', 'nthw', 'mtsw', 'ntch', 'm',
    'n', 'u', 'a', 'e', 'i', 'o',
]

# ── Chichewa phonological patterns ──────────────────────────
CHICHEWA_PHONOLOGY = [
    r'(mb[aeiou])',
    r'(nd[aeiou])',
    r'(nj[aeiou])',
    r'(ng[aeiou])',
    r'(nk[aeiou])',
    r'(mp[aeiou])',
    r'(mf[aeiou])',
    r'(ny[aeiou])',
    r'(ph[aeiou])',
    r'(th[aeiou])',
    r'(kh[aeiou])',
    r'(ts[aeiou])',
    r'(dz[aeiou])',
    r'(bv[aeiou])',
    r'(ch[aeiou])',
    r'(mw[aeiou])',
    r'(nkh[aeiou])',
    r'(ntch[aeiou])',
    r'(mph[aeiou])',
    r'(nth[aeiou])',
    r'([aeiou]w[aeiou])',
    r'([aeiou]y[aeiou])',
    r'(w[aeiou]n[aeiou])',
    r'(w[aeiou]r[aeiou])',
    r'(l[aeiou]l[aeiou])',
    r'(r[aeiou]r[aeiou])',
]

# ── Non-Chichewa patterns ────────────────────────────────────
NON_CHICHEWA_PATTERNS = [
    (r'[qx]',                    "Contains letters q, or x which do not exist in Chichewa"),
    (r'(tion|sion|ness)',          "Contains English suffix -tion, -sion, or -ness"),
    (r'(ment|ling|ful|less)',      "Contains English suffix -ment, -ling, -ful, or -less"),
    (r'(ous|ive|ble|able|ible)',   "Contains English suffix -ous, -ive, -ble, -able, or -ible"),
    (r'(ack|eck|ick|ock|uck)',     "Contains English consonant cluster pattern -ack, -eck, -ick, -ock, or -uck"),
    (r'(ck|wh|gh)',                "Contains English consonant cluster ck, wh, or gh"),
    (r'(sch|str|spl|spr)',         "Contains English consonant cluster sch, str, spl, or spr"),
    (r'(tt|pp|ss|ff|ll|rr|nn)',    "Contains double consonants which do not occur in Chichewa"),
    (r'(aa|ee|ii|oo|uu)',          "Contains double vowels which do not occur in Chichewa"),
    (r'^[bcdfghjklmnpqrstvwxyz]{4,}', "Starts with 4 or more consonants which is impossible in Chichewa"),
]

# ── Common English words to reject immediately ───────────────
ENGLISH_WORDS = {
    'the', 'and', 'for', 'was', 'his', 'her', 'are', 'but',
    'not', 'you', 'all', 'can', 'had', 'that', 'with', 'have',
    'this', 'will', 'your', 'from', 'they', 'know', 'want',
    'been', 'good', 'much', 'some', 'time', 'very', 'when',
    'come', 'here', 'just', 'like', 'long', 'make', 'many',
    'more', 'only', 'over', 'such', 'take', 'than', 'them',
    'well', 'were', 'what', 'word', 'work', 'year', 'after',
    'also', 'back', 'call', 'down', 'each', 'even', 'find',
    'give', 'hand', 'help', 'high', 'home', 'into', 'keep',
    'last', 'left', 'life', 'live', 'look', 'move', 'need',
    'next', 'open', 'part', 'play', 'real', 'same', 'seem',
    'show', 'side', 'tell', 'think', 'those', 'three', 'through',
    'turn', 'used', 'walk', 'while', 'world', 'write', 'young',
    'school', 'water', 'place', 'large', 'small', 'right', 'every',
    'never', 'night', 'point', 'since', 'sound', 'still', 'study',
    'chair', 'table', 'house', 'light', 'black', 'white', 'green',
    'board', 'paper', 'money', 'child', 'start', 'stand', 'found',
    'heart', 'leave', 'might', 'plant', 'watch', 'under', 'along',
    'bring', 'carry', 'class', 'cover', 'cross', 'drink', 'earth',
    'eight', 'eye', 'face', 'fall', 'fast', 'feel', 'fill', 'fire',
    'five', 'four', 'free', 'full', 'girl', 'got', 'grow', 'half',
    'hard', 'hear', 'heat', 'hold', 'hope', 'hour', 'idea', 'kill',
    'kind', 'knew', 'land', 'lead', 'less', 'lose', 'love', 'main',
    'meet', 'mind', 'mine', 'miss', 'moon', 'most', 'name', 'near',
    'news', 'note', 'once', 'once', 'road', 'rock', 'room', 'rose',
    'rule', 'said', 'ship', 'shop', 'sing', 'skin', 'slow', 'soft',
    'sold', 'soon', 'sort', 'step', 'stop', 'sure', 'test', 'than',
    'that', 'then', 'they', 'thin', 'thus', 'till', 'told', 'tone',
    'took', 'tree', 'true', 'type', 'upon', 'wait', 'wake', 'warm',
    'wave', 'weak', 'wear', 'week', 'west', 'wide', 'wife', 'wild',
    'wind', 'wine', 'wing', 'wire', 'wise', 'wish', 'with', 'wolf',
    'wood', 'wool', 'word', 'wore', 'worm', 'worn', 'wove', 'wrap',
}

# ── Known Chichewa words (from common vocabulary) ────────────
KNOWN_CHICHEWA = {
    'mwana', 'ana', 'munthu', 'anthu', 'nyumba', 'mtengo',
    'mitengo', 'madzi', 'moto', 'mpweya', 'dziko', 'mlengalenga',
    'dzuwa', 'mwezi', 'nyenyezi', 'usiku', 'masana', 'mawa',
    'lero', 'dzulo', 'tsiku', 'masiku', 'sabata', 'mwezi',
    'chaka', 'zaka', 'nthawi', 'malo', 'panja', 'mkati',
    'kumwamba', 'pansi', 'pambali', 'pamaso', 'mbuzi', 'nkhuku',
    'ng\'ombe', 'njovu', 'mkango', 'nkhandwe', 'fisi', 'galu',
    'mphaka', 'nsomba', 'mbalame', 'njuchi', 'nzeru', 'chikondi',
    'chisomo', 'mtendere', 'chimwemwe', 'chisoni', 'mkwiyo',
    'chilungamo', 'chowonadi', 'uthenga', 'nkhani', 'mawu',
    'kulankhula', 'kumva', 'kuona', 'kudya', 'kumwa', 'kugona',
    'kuuka', 'kuyenda', 'kubwera', 'kupita', 'kulima', 'kuphika',
    'kulemba', 'kuwerenga', 'kusewera', 'kuimba', 'kutchula',
    'chimanga', 'mchele', 'ufa', 'nsima', 'ndiwo', 'mchezo',
    'sukulu', 'chipatala', 'boma', 'msika', 'mudzi', 'mzinda',
    'buku', 'kalata', 'pepala', 'bolopo', 'galimoto', 'sitima',
    'ndege', 'boti', 'njinga', 'chipanda', 'mtsuko', 'mbiya',
    'bakuli', 'mbale', 'mano', 'mphuno', 'maso', 'makutu',
    'mkono', 'mawonekedwe', 'thupi', 'mutu', 'khosi', 'mtima',
    'chiwuno', 'mwendo', 'phazi', 'chala', 'liwiro', 'mphamvu',
    'bvuto', 'vuto', 'mavuto', 'chitukuko', 'chuma', 'ndalama',
    'ntchito', 'ntchito', 'mwini', 'akazi', 'amuna', 'achimwene',
    'achemwali', 'abale', 'alongo', 'agogo', 'makolo', 'mfumu',
    'mtsogoleri', 'nduna', 'mphunzitsi', 'dokotala', 'namwino',
    'mlimi', 'mwalamuzi', 'mbuye', 'atsikana', 'anyamata',
    'mwamuna', 'mkazi', 'mnyamata', 'mtsikana', 'mwana',
    'chovala', 'zovala', 'malaya', 'bulangete', 'nsapato',
    'chipewa', 'zipewa', 'mphasa', 'kachisi', 'tchalitchi',
    'msikiti', 'minda', 'munda', 'dimba', 'thabwa', 'matabwa',
    'mpando', 'mipando', 'kochi', 'makochi', 'chipinda', 'ziphinda',
    'khomo', 'makhomo', 'zenera', 'mazenera', 'denga', 'madenga',
    'udindo', 'maudindo', 'ulendo', 'maulendo', 'ufulu', 'maufulu',
    'chilichonse', 'kanthu', 'china', 'chake', 'chanu', 'changa',
    'wake', 'wanu', 'wanga', 'ake', 'anu', 'anga', 'lake', 'lanu',
}


def detect_language(noun):
    """
    Returns a dict with:
      is_chichewa: True/False
      confidence:  high / medium / low
      reason:      explanation string
      warnings:    list of warning strings
    """
    noun_lower = noun.lower().strip()
    warnings   = []

    # 1. known Chichewa word — immediate pass
    if noun_lower in KNOWN_CHICHEWA:
        return {
            'is_chichewa': True,
            'confidence':  'high',
            'reason':      f"'{noun}' is a recognised Chichewa word.",
            'warnings':    [],
        }

    # 2. known English word — immediate fail
    if noun_lower in ENGLISH_WORDS:
        return {
            'is_chichewa': False,
            'confidence':  'high',
            'reason':      f"'{noun}' is a common English word, not a Chichewa word.",
            'warnings':    [f"'{noun}' appears to be an English word. Please enter a Chichewa noun."],
        }

    # 3. too short
    if len(noun_lower) < 3:
        return {
            'is_chichewa': True,
            'confidence':  'low',
            'reason':      "Word is too short to determine its language with confidence.",
            'warnings':    ["The word is very short. Results may not be accurate."],
        }

    # 4. check non-Chichewa patterns
    for pattern, reason in NON_CHICHEWA_PATTERNS:
        match = re.search(pattern, noun_lower, re.IGNORECASE)
        if match:
            return {
                'is_chichewa': False,
                'confidence':  'high',
                'reason':      f"The word '{noun}' does not appear to be Chichewa. {reason} (found: '{match.group()}').",
                'warnings':    [
                    f"⚠ Warning: '{noun}' does not appear to be a Chichewa word.",
                    f"Reason: {reason}.",
                    "Please enter a valid Chichewa noun."
                ],
            }

    # 5. check Chichewa prefix
    starts_chichewa = any(noun_lower.startswith(p) for p in CHICHEWA_PREFIXES)

    # 6. check Chichewa phonology
    matches_phonology = any(
        re.search(p, noun_lower, re.IGNORECASE) for p in CHICHEWA_PHONOLOGY
    )

    # 7. check Chichewa ending
    ends_chichewa = any(noun_lower.endswith(e) for e in CHICHEWA_ENDINGS)

    # 8. score the word
    score = 0
    if starts_chichewa:  score += 2
    if matches_phonology: score += 2
    if ends_chichewa:    score += 1

    if score >= 3:
        return {
            'is_chichewa': True,
            'confidence':  'high' if score >= 4 else 'medium',
            'reason':      f"'{noun}' matches Chichewa morphological and phonological patterns.",
            'warnings':    [],
        }
    elif score == 2:
        return {
            'is_chichewa': True,
            'confidence':  'medium',
            'reason':      f"'{noun}' partially matches Chichewa patterns but could not be fully verified.",
            'warnings':    [f"'{noun}' could not be fully verified as a Chichewa word. Results may vary."],
        }
    elif score == 1:
        return {
            'is_chichewa': False,
            'confidence':  'medium',
            'reason':      f"'{noun}' does not clearly match Chichewa morphological patterns.",
            'warnings':    [
                f"⚠ Warning: '{noun}' does not clearly match Chichewa word patterns.",
                "Please verify this is a valid Chichewa noun."
            ],
        }
    else:
        return {
            'is_chichewa': False,
            'confidence':  'high',
            'reason':      f"'{noun}' does not match any known Chichewa morphological or phonological patterns.",
            'warnings':    [
                f"⚠ Warning: '{noun}' does not appear to be a Chichewa word.",
                "Please enter a valid Chichewa noun."
            ],
        }