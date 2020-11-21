# This script will read enUS strings and copy them into another locales if it doesn't have them. If there are available
# translations from another mods (mainly from Blizz), it would correctly refer the string and copy them instead.
#
# Running the script:
#
# 1. Download required modfiles in _loose_ form:
# - (Basegame storage) mods/core.sc2mod
# - (Basegame storage) mods/starcoop/starcoop.sc2mod
# - Maguro's Coop mod
# The basegame modfiles can be extracted with CASCView tool (http://www.zezula.net/en/casc/main.html).
# Maguro's coop mod can be downloaded via Galaxy Editor. Save it with SC2Components form (= loose files).
#
# Note that all of these mods should have all supported locales available. In CASCView use "Open Online" feature to
# download all of them, not "Game Storage" which only extracts what you have.
#
# 2. Modify the @references@ path below to point them.
#
# 3. Run it.

from pathlib import Path
import shutil
import re

references = [
    '../../../Reference/mods/core.sc2mod',
    '../../../Reference/mods/starcoop/starcoop.sc2mod',
    '../../../MaguroReference/CoopMod-1.22.SC2Mod'
]

exclude_reference_patterns = [
    r'DocInfo/.*',
    r'MapInfo/.*',
    r'Variant[0-9]+/.*',
    r'Attribute[0-9]+/.*'
]

non_enus_locales = [
    'deDE',
    'esES',
    'esMX',
    'frFR',
    'itIT',
    'koKR',
    'plPL',
    'ptBR',
    'ruRU',
    'zhCN',
    'zhTW',
]

def parse_gamestrings_file(f, use_exclude_reference_patterns):
    ret = []
    for line in f.readlines():
        line = line.strip()

        if '=' not in line:
            ret.append(('', line))
            continue

        key = line.split('=')[0]
        val = '='.join(line.split('=')[1:])

        if use_exclude_reference_patterns and any(re.fullmatch(pattern, key) for pattern in exclude_reference_patterns):
            continue

        ret.append((key, val))
    return ret


src = Path('enUS.SC2Data/LocalizedData/GameStrings.txt')
with src.open('r', encoding='utf-8-sig') as f:
    stringlist = parse_gamestrings_file(f, False)

for locale in non_enus_locales:
    dst = Path(f'{locale}.SC2Data/LocalizedData/GameStrings.txt')
    
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        dst.touch()

    dstdic = {}    
    for ref in references:
        try:
            with Path(f'{ref}/{locale}.SC2Data/LocalizedData/GameStrings.txt').open('r', encoding='utf-8-sig') as f:
                newtrans = {k: v for k, v in parse_gamestrings_file(f, True) if k}
                dstdic.update(newtrans)
        except FileNotFoundError:
            pass
    with Path(f'{locale}.SC2Data/LocalizedData/GameStrings.txt').open('r', encoding='utf-8-sig') as f:
        newtrans = {k: v for k, v in parse_gamestrings_file(f, False) if k}
        dstdic.update(newtrans)

    with dst.open('w', encoding='utf-8-sig') as f:
        for k, v in stringlist:
            v = dstdic.get(k, v)
            if k:
                f.writelines(f'{k}={v}\n')
            else:
                f.writelines(f'{v}\n')
