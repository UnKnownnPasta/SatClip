"""Generate question -> intent JSON pairs for LoRA fine-tuning of SatClip's language layer.

Every pair is built from the district gazetteer (735 districts) and hand-written templates in English,
Hinglish (romanised Hindi) and Hindi, with Indian date styles (DD/MM/YYYY, "11 July 2024", "11 जुलाई 2024"),
typos in place names, missing details and out-of-scope questions. Targets follow training/lora/schema.py.

Districts are split 80/10/10 by a stable hash, so the test set measures generalisation to districts the
model never saw. Output: data/intents/{train,val,test}.jsonl with {"messages": [...], "target": {...}}.

    python training/lora/build_intent_data.py --n-train 12000 --seed 7
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema import ROOT, SYSTEM_PROMPT, dumps  # noqa: E402

OUT = ROOT / "training" / "data" / "intents"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
HI_MONTHS = ["जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"]

T = {  # {p} place, {d} date, {a} before date, {b} after date
    "water_extent": {
        "en": ["How much of {p} was under water on {d}?", "Show flooded area in {p} on {d}",
               "What area of {p} district was inundated around {d}?", "flood extent {p} {d}",
               "Was {p} flooded on {d}? How many sq km?", "Map the standing water in {p} for {d}.",
               "How much land was submerged in {p}, {d}?", "Give me the flood map of {p} district on {d}"],
        "hinglish": ["{p} mein {d} ko kitna area paani mein tha?", "{d} ko {p} me baadh ka area batao",
                     "{p} district flood kitna tha {d} ko", "{p} me {d} ko kitni zameen doobi thi?"],
        "hi": ["{d} को {p} में कितना इलाका पानी में डूबा था?", "{p} ज़िले में {d} को बाढ़ का क्षेत्र दिखाओ",
               "{d} को {p} में कितनी ज़मीन जलमग्न थी?"],
    },
    "water_change": {
        "en": ["Did the flood spread in {p} between {a} and {b}?", "How much new water appeared in {p} from {a} to {b}?",
               "Compare flooding in {p}: {a} vs {b}", "newly flooded area {p} {a} to {b}",
               "Has the water in {p} receded between {a} and {b}?", "Flood change in {p} district, {a} compared with {b}"],
        "hinglish": ["{p} mein {a} se {b} tak baadh kitni badhi?", "{a} aur {b} ke beech {p} me naya paani kitna aaya?",
                     "{p} flood {a} vs {b} compare karo"],
        "hi": ["{a} से {b} तक {p} में बाढ़ कितनी फैली?", "{p} में {a} और {b} के बीच नया जलभराव कितना हुआ?"],
    },
    "vegetation_change": {
        "en": ["Did the crop decline in {p} between {a} and {b}?", "How did vegetation change in {p} from {a} to {b}?",
               "Crop loss in {p} district, {a} vs {b}", "NDVI change {p} {a} {b}",
               "Has greenness dropped in {p} between {a} and {b}?", "Show crop damage in {p} from {a} to {b}"],
        "hinglish": ["{p} me {a} se {b} tak fasal kitni kharab hui?", "{a} aur {b} ke beech {p} ki hariyali kaise badli?"],
        "hi": ["{a} से {b} के बीच {p} में फ़सल कितनी घटी?", "{p} में {a} और {b} के बीच हरियाली में क्या बदलाव आया?"],
    },
    "land_cover": {
        "en": ["What is the land cover of {p} on {d}?", "Classify the land use in {p} district around {d}",
               "Is {p} mostly farmland or forest? ({d})", "land cover {p} {d}"],
        "hinglish": ["{p} me {d} ko zameen kis type ki hai?", "{p} ka land use kya hai {d} ko"],
        "hi": ["{d} को {p} की भूमि किस प्रकार की है?"],
    },
    "describe": {
        "en": ["Describe the land in {p} on {d}", "Give a short description of {p} district from the image of {d}",
               "What does {p} look like on {d}?", "summary of the scene over {p} {d}"],
        "hinglish": ["{p} ka {d} ka scene describe karo", "{d} ko {p} kaisa dikh raha tha?"],
        "hi": ["{d} की तस्वीर में {p} का वर्णन करो"],
    },
}
REFUSALS = {
    "counting": ["How many houses were damaged in {p} on {d}?", "Count the boats in {p}", "{p} me kitne ghar doobe?",
                 "How many cattle died in the {p} floods?", "{p} में कितने घर टूटे?"],
    "forecast": ["Will {p} flood next week?", "Predict the rainfall in {p} tomorrow", "{p} me agle mahine baadh aayegi kya?",
                 "Forecast crop yield for {p} this season", "क्या कल {p} में बाढ़ आएगी?"],
    "identity": ["Who owns the farm near {p}?", "Which family lives by the river in {p}?", "{p} me ye zameen kiski hai?"],
    "other": ["What is the population of {p}?", "Write a poem about {p}", "Which party won in {p}?",
              "What is the GDP of {p} district?", "{p} ki best hotel kaunsi hai?"],
}


def fmt_date(d: date, style: str, rng: random.Random) -> str:
    if style == "hi":
        return f"{d.day} {HI_MONTHS[d.month - 1]} {d.year}"
    choice = rng.choice(["iso", "dmy_slash", "long", "us_long", "short", "dmy_dash"])
    return {"iso": d.isoformat(), "dmy_slash": f"{d.day:02d}/{d.month:02d}/{d.year}",
            "long": f"{d.day} {MONTHS[d.month - 1]} {d.year}", "us_long": f"{MONTHS[d.month - 1]} {d.day}, {d.year}",
            "short": f"{d.day} {MONTHS[d.month - 1][:3]} {d.year}", "dmy_dash": f"{d.day:02d}-{d.month:02d}-{d.year}"}[choice]


def typo(name: str, rng: random.Random) -> str:
    if len(name) < 6:
        return name
    i = rng.randrange(1, len(name) - 2)
    op = rng.choice(["swap", "drop", "double"])
    if op == "swap":
        return name[:i] + name[i + 1] + name[i] + name[i + 2:]
    if op == "drop":
        return name[:i] + name[i + 1:]
    return name[:i] + name[i] + name[i:]


def split_of(key: str) -> str:
    h = int(hashlib.sha1(key.encode()).hexdigest(), 16) % 10
    return "test" if h == 0 else "val" if h == 1 else "train"


def rand_date(rng: random.Random) -> date:
    return date(2017, 1, 1) + timedelta(days=rng.randrange(0, (date(2026, 9, 30) - date(2017, 1, 1)).days))


def make(district: dict, rng: random.Random, dupes: set[str]) -> dict:
    name, state = district["name"], district["state"]
    style = rng.choices(["en", "hinglish", "hi"], weights=[6, 3, 2])[0]
    r = rng.random()
    if r < 0.12:  # out of scope
        reason = rng.choice(list(REFUSALS))
        tpl = rng.choice(REFUSALS[reason])
        intent, n_dates = "unsupported", 1
    else:
        intent = rng.choices(list(T), weights=[30, 22, 22, 8, 8])[0]
        tpl = rng.choice(T[intent][style])
        reason, n_dates = None, (2 if intent in ("water_change", "vegetation_change") else 1)
    a = rand_date(rng)
    b = a + timedelta(days=rng.randrange(6, 120))
    dates = [a, b] if n_dates == 2 else [a]
    dstyle = "hi" if any("\u0900" <= ch <= "\u097f" for ch in tpl) else "en"
    shown_place = name
    with_state = name.lower() in dupes or rng.random() < 0.15
    if with_state:
        shown_place = f"{name}, {state}" if style != "hi" else f"{name} ({state})"
    if rng.random() < 0.08:
        shown_place = shown_place.replace(name, typo(name, rng), 1)
    if rng.random() < 0.15:
        shown_place = shown_place.lower()
    drop = rng.random()
    place_out, state_out = name, (state if with_state else None)
    if drop < 0.05:  # no place given
        shown_place, place_out, state_out = "this area" if style != "hi" else "इस इलाके", None, None
    q = tpl.replace("{p}", shown_place)
    if drop > 0.95 and "{d}" in q:  # date missing
        q = q.replace(" on {d}", "").replace(" around {d}", "").replace(" ({d})", "").replace(" {d}", "")
        q = q.replace("{d} ko ", "").replace("{d} को ", "").replace("{d}", "")
        dates = []
    q = q.replace("{d}", fmt_date(dates[0], dstyle, rng) if dates else "")
    if "{a}" in q:
        q = q.replace("{a}", fmt_date(dates[0], dstyle, rng)).replace("{b}", fmt_date(dates[1], dstyle, rng))
    dates_out = [d.isoformat() for d in dates] if any(k in tpl for k in ("{d}", "{a}")) else []
    target = {"intent": intent, "place": place_out, "state": state_out, "dates": dates_out, "refuse_reason": reason}
    return {"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": q.strip()},
                         {"role": "assistant", "content": dumps(target)}],
            "target": target, "meta": {"style": style, "district": f"{name}|{state}"}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-train", type=int, default=12000)
    ap.add_argument("--n-eval", type=int, default=1500)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    districts = json.loads((ROOT / "backend/satclip/resources/districts.json").read_text())["districts"]
    names = [d["name"].lower() for d in districts]
    dupes = {n for n in names if names.count(n) > 1}
    by_split: dict[str, list[dict]] = {"train": [], "val": [], "test": []}
    for d in districts:
        by_split[split_of(f"{d['name']}|{d['state']}")].append(d)
    OUT.mkdir(parents=True, exist_ok=True)
    for split, n in (("train", args.n_train), ("val", args.n_eval), ("test", args.n_eval)):
        rows = [make(rng.choice(by_split[split]), rng, dupes) for _ in range(n)]
        with open(OUT / f"{split}.jsonl", "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"{split}: {n} pairs from {len(by_split[split])} districts -> {(OUT / f'{split}.jsonl').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
