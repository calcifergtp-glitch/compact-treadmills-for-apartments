#!/usr/bin/env python3
import os
import json
import datetime
import pathlib
import re


def slugify(text):
    return re.sub(r'[^a-zA-Z0-9]+','-', text.lower()).strip('-')


def load_affiliates():
    data = os.getenv('AFFILIATE_JSON')
    if not data:
        return {}
    try:
        return json.loads(data)
    except Exception:
        return {}


def get_niche():
    niche = os.getenv('NICHE')
    if niche:
        return niche
    cwd = os.getcwd()
    return os.path.basename(cwd).replace('-', ' ')


def get_products(niche, affiliates):
    products = []
    words = niche.split()
    base_key = words[-1] if words else 'product'
    for i in range(3):
        name = f"{base_key.title()} Option {i+1}"
        description = f"{name} is a recommended choice for {niche} enthusiasts."
        pros = ["Affordable", "Popular choice"] if i % 2 == 0 else ["Premium quality", "Great reviews"]
        cons = ["Limited colors"] if i % 2 == 0 else ["Higher price"]
        link = ""
        if affiliates:
            vendor, base_url = next(iter(affiliates.items()))
            link = base_url
        products.append({"name": name, "description": description, "pros": pros, "cons": cons, "link": link})
    return products


def create_post(niche, products):
    today = datetime.date.today()
    slug = slugify(f"{niche}-{today.isoformat()}")
    filename = f"{today.isoformat()}-{slug}.md"
    post_dir = pathlib.Path('_posts')
    post_dir.mkdir(parents=True, exist_ok=True)
    with open(post_dir / filename, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: post\n")
        f.write(f"title: Top {len(products)} {niche.title()} Products for {today.year}\n")
        f.write(f"date: {today.isoformat()}\n")
        f.write("---\n\n")
        f.write(f"Looking for the best {niche} products? Here are some recommendations:\n\n")
        for p in products:
            f.write("## " + p['name'] + "\n")
            f.write(p['description'] + "\n\n")
            f.write("*Pros:* " + ", ".join(p['pros']) + "\n\n")
            f.write("*Cons:* " + ", ".join(p['cons']) + "\n\n")
            if p['link']:
                f.write("[View product here](" + p['link'] + ")\n\n")


def main():
    niche = get_niche()
    affiliates = load_affiliates()
    products = get_products(niche, affiliates)
    create_post(niche, products)


if __name__ == "__main__":
    main()
