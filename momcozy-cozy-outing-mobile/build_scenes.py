#!/usr/bin/env python3
"""Regenerate scenes.json from products.json (run after updating products.json)."""
import json

with open("products.json") as f:
    products = json.load(f)["products"]


def img_url(src, w=720):
    if not src:
        return ""
    s = src.replace("\\/", "/")
    return f"{s}{'&' if '?' in s else '?'}width={w}"


def minmax_price(p):
    prices = [float(v["price"]) for v in p["variants"]]
    if not prices:
        return None, None
    return min(prices), max(prices)


def price_label(p):
    lo, hi = minmax_price(p)
    if lo is None:
        return ""
    if lo == hi:
        return f"${lo:.2f}"
    return f"From ${lo:.2f}"


def card(p):
    im = p["images"][0]["src"] if p.get("images") else ""
    return {
        "title": p["title"],
        "price": price_label(p),
        "url": f"https://momcozy.com/products/{p['handle']}",
        "image": img_url(im),
    }


def assign_scene(p):
    h = p["handle"].lower()
    t = (p.get("product_type") or "").lower()
    title = p["title"].lower()

    if "bundle" in h or "bunlde" in t or "bundle" in t:
        if "sound" in h or "sound" in title:
            return "soothe"
        if "warmer" in h or "pump" in title or "milk" in title or "m6" in h:
            return "feed"
        return "stroller"

    if "sound" in h or "sound machine" in t:
        return "soothe"

    if "stroller" in h or t == "baby stroller":
        return "stroller"
    if "organizer" in h or ("bag" in t and "stroller" in title):
        return "stroller"
    if "stroller-fan" in h or ("clip-on" in h and "stroller" in title):
        return "stroller"

    if t == "carriers" or "carrier" in h or "wrap" in h or "hip-seat" in h:
        return "wear"

    if "warmer" in h or "cooler" in h or "bottle" in h or "nursing cover" in t or "nursing" in h:
        return "feed"

    if "wipe" in h or "all-in-1" in h or "baby kit" in h or "kit" in h or "tank" in h:
        return "care"
    if "fan" in h and "stroller" not in h:
        return "care"

    return "care"


buckets = {k: [] for k in ["stroller", "wear", "soothe", "feed", "care"]}
for p in products:
    buckets[assign_scene(p)].append(p)

for k in buckets:
    seen = set()
    uniq = []
    for p in buckets[k]:
        if p["id"] in seen:
            continue
        seen.add(p["id"])
        uniq.append(p)
    buckets[k] = uniq

scene_meta = [
    ("stroller", "Stroll-ready setup", "Strollers, organizers, and clip-ons for smoother walks and errands."),
    ("wear", "Wear them close", "Carriers, wraps, and hip seats for park loops and transit."),
    ("soothe", "Calm on the move", "Portable sound for naps in the car or stroller."),
    ("feed", "Nursing & bottles outside", "Covers, coolers, warmers, and bottle bags built for outings."),
    ("care", "Freshness & quick fixes", "Wipes, kits, and travel-friendly helpers."),
]

scenes = []
for key, title, desc in scene_meta:
    prods = buckets[key]
    if not prods:
        continue
    if key == "stroller":
        prods = sorted(prods, key=lambda x: (0 if "changego" in x["handle"] else 1, x["title"]))
    hero_src = prods[0]["images"][0]["src"] if prods[0].get("images") else ""
    scenes.append(
        {
            "id": key,
            "title": title,
            "description": desc,
            "hero": img_url(hero_src, 900),
            "products": [card(p) for p in prods],
        }
    )

out = {"source": "https://momcozy.com/collections/cozy-outing", "scenes": scenes}
with open("scenes.json", "w") as f:
    json.dump(out, f, indent=2)

for s in scenes:
    print(s["id"], len(s["products"]))
