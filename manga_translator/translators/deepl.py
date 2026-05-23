import deepl

from .common import CommonTranslator, MissingAPIKeyException
from .keys import DEEPL_AUTH_KEY

class DeeplTranslator(CommonTranslator):
    _LANGUAGE_CODE_MAP = {
        'CHS': 'ZH-HANS',
        'CHT': 'ZH-HANT',
        'JPN': 'JA',
        'ENG': 'EN-US',
        'CSY': 'CS',
        'NLD': 'NL',
        'FRA': 'FR',
        'DEU': 'DE',
        'HUN': 'HU',
        'ITA': 'IT',
        'POL': 'PL',
        'PTB': 'PT-BR',
        'ROM': 'RO',
        'RUS': 'RU',
        'ESP': 'ES',
        'IND': 'ID',
        'ARA': 'AR',
        'BGR': 'BG',
        'BUL': 'BG',
        'DAN': 'DA',
        'ELL': 'EL',
        'EST': 'ET',
        'FIN': 'FI',
        'KOR': 'KO',
        'LTH': 'LT',
        'LIT': 'LT',
        'LAV': 'LV',
        'NOB': 'NB',
        'SVK': 'SK',
        'SLO': 'SK',
        'SLV': 'SL',
        'SWE': 'SV',
        'TRK': 'TR',
        'TUR': 'TR',
        'UKR': 'UK'
    }

    REPLACEMENTS = {
        '\u00c6': "'",
        '\u00e0': "'",
        '\u00f9': '-',
        '\u2019': "'",
        '\u2018': "'",
        '\u201c': '"',
        '\u201d': '"',
    }

    def __init__(self):
        super().__init__()
        if not DEEPL_AUTH_KEY:
            raise MissingAPIKeyException('Please set the DEEPL_AUTH_KEY environment variable before using the deepl translator.')
        self.translator = deepl.Translator(DEEPL_AUTH_KEY)

    async def _translate(self, from_lang, to_lang, queries):
        translated = self.translator.translate_text('\n'.join(queries), target_lang=to_lang).text
        results = translated.split('\n')
        fixed = []
        for r in results:
            for src, dst in self.REPLACEMENTS.items():
                r = r.replace(src, dst)
            # Garde uniquement les caractères ASCII + latin étendu courant
            r = ''.join(c if ord(c) < 0x2000 else '' for c in r)
            fixed.append(r)
        return fixed