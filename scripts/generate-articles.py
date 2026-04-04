#!/usr/bin/env python3
"""
generate-articles.py - Boot Craft Archive 記事自動生成スクリプト

データソース: boots.json, leathers.json, constructions.json, brands.json
カテゴリ: review, leather, construction, comparison, care, beginner

使い方:
  python scripts/generate-articles.py --category review
  python scripts/generate-articles.py --category leather
  python scripts/generate-articles.py --category construction
  python scripts/generate-articles.py --category comparison
  python scripts/generate-articles.py --category care
"""

import json
import os
import random
import argparse
from datetime import datetime

# プロジェクトルートのパスを計算
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# データファイルの読み込み
def load_json(filename):
    """JSONデータファイルを読み込む"""
    filepath = os.path.join(PROJECT_ROOT, "src", "data", filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# 記事の保存先ディレクトリ
ARTICLES_DIR = os.path.join(PROJECT_ROOT, "src", "content", "articles")

def ensure_articles_dir():
    """記事ディレクトリが存在することを確認"""
    os.makedirs(ARTICLES_DIR, exist_ok=True)

def save_article(slug, content):
    """記事をMarkdownファイルとして保存"""
    filepath = os.path.join(ARTICLES_DIR, f"{slug}.md")
    # 既存記事は上書きしない
    if os.path.exists(filepath):
        print(f"  スキップ（既存）: {slug}.md")
        return False
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  生成完了: {slug}.md")
    return True

def today_str():
    """今日の日付をYYYY-MM-DD形式で返す"""
    return datetime.now().strftime("%Y-%m-%d")

# === カテゴリ別の記事生成関数 ===

def generate_review(boots, brands):
    """レビュー記事を生成（ランダムにブーツを1つ選択）"""
    boot = random.choice(boots)
    brand = next((b for b in brands if b["id"] == boot["brand"]), None)
    brand_name = brand["name"] if brand else boot["brand"]
    slug = f"{boot['id']}-review"

    # カテゴリ表示名
    category_label = " ".join(
        w.capitalize() for w in boot["category"].split("-")
    )

    content = f"""---
title: "{boot['name']} — In-Depth Review"
description: "A comprehensive review of the {boot['name']} by {brand_name}. We cover leather quality, construction, fit, break-in, and long-term value."
category: "review"
tags: ["{boot['brand']}", "{boot['category']}", "{boot['leather']}", "review"]
publishedAt: "{today_str()}"
relatedBoots: {json.dumps(boot.get('relatedBoots', []))}
articleType: "review"
---

## Overview

The {boot['name']} is a {category_label.lower()} from {brand_name}, made in {boot['madeIn']}. Priced at ${boot['price']}, it features {boot['leather']} leather with {boot['construction'].replace('-', ' ')} construction.

{boot['description']}

## Construction & Materials

- **Leather**: {boot['leather'].replace('-', ' ').title()}
- **Construction**: {boot['construction'].replace('-', ' ').title()}
- **Sole**: {boot['sole'].capitalize()}
- **Last Shape**: {boot['lastShape']}
- **Made In**: {boot['madeIn']}

## Key Features

{chr(10).join(f'- {f}' for f in boot['features'])}

## Fit & Sizing

As with most {boot['construction'].replace('-', ' ')} boots, we recommend trying the {boot['name']} in your Brannock size and potentially sizing down by half a size. The {boot['lastShape']} last provides a balanced fit that accommodates most foot shapes.

## Value Assessment

At ${boot['price']}, the {boot['name']} sits in the {boot['priceRange']} price range. For a {boot['construction'].replace('-', ' ')} boot made in {boot['madeIn']} with {boot['leather']} leather, this represents solid value in today's market.

## Verdict

The {boot['name']} is a worthy addition to any footwear collection. {brand_name}'s commitment to quality materials and proven construction methods ensures this is a boot that will serve you well for years to come.
"""
    return slug, content

def generate_leather_article(leathers):
    """レザーガイド記事を生成"""
    leather = random.choice(leathers)
    slug = f"{leather['id']}-leather-deep-dive"

    content = f"""---
title: "{leather['name']} Leather: Everything You Need to Know"
description: "A deep dive into {leather['name']} leather — tanning process, properties, care tips, and the best boots made with this leather."
category: "leather"
tags: ["{leather['id']}", "leather-guide", "{leather['tannery'].lower()}"]
publishedAt: "{today_str()}"
articleType: "guide"
---

## What Is {leather['name']}?

{leather['description']}

## Properties at a Glance

- **Durability**: {leather['properties']['durability']}/5
- **Water Resistance**: {leather['properties']['waterResistance']}/5
- **Patina Development**: {leather['properties']['patina']}/5
- **Suppleness**: {leather['properties']['suppleness']}/5
- **Ease of Maintenance**: {leather['properties']['maintenance']}/5

## Tanning Process

{leather['name']} is produced using {leather['tanningMethod']} tanning methods by {leather['tannery']}. This process gives the leather its distinctive character and determines how it ages over time.

## Care Recommendations

To maintain {leather['name']} leather:

1. Brush regularly with a horsehair brush after each wear
2. Condition every 4-8 weeks depending on wear frequency
3. Use shoe trees to maintain shape and absorb moisture
4. Avoid direct heat sources when drying

## Best Boots in {leather['name']}

{leather['name']} is popular among heritage boot makers for its unique combination of properties. Look for offerings from brands that source from {leather['tannery']} for the highest quality specimens.

## Conclusion

{leather['name']} remains one of the most beloved leathers in the footwear world. Whether you prioritize patina, durability, or ease of care, understanding this leather will help you make a more informed purchase decision.
"""
    return slug, content

def generate_construction_article(constructions):
    """製法ガイド記事を生成"""
    construction = random.choice(constructions)
    slug = f"{construction['id']}-construction-explained"

    content = f"""---
title: "{construction['name']} Construction: A Complete Explanation"
description: "Everything you need to know about {construction['name']} construction — how it works, its advantages and disadvantages, and which boots use this method."
category: "construction"
tags: ["{construction['id']}", "construction", "guide"]
publishedAt: "{today_str()}"
articleType: "guide"
---

## What Is {construction['name']}?

{construction['description']}

## Properties

- **Durability**: {construction['properties']['durability']}/5
- **Water Resistance**: {construction['properties']['waterResistance']}/5
- **Resolability**: {construction['properties']['resolability']}/5
- **Flexibility**: {construction['properties']['flexibility']}/5
- **Lightweight**: {construction['properties']['weight']}/5

## Advantages

{construction['name']} construction offers several key benefits that make it a popular choice among quality footwear manufacturers. Its balance of durability and resolability ensures long-term value for the wearer.

## Disadvantages

No construction method is perfect. {construction['name']} has trade-offs that buyers should consider, particularly regarding flexibility and weight compared to other methods.

## Who Should Choose {construction['name']}?

This construction method is ideal for those who value durability and are willing to invest in footwear that can be maintained and resoled over many years.

## Conclusion

Understanding {construction['name']} construction helps you make smarter footwear purchases. The method you choose should align with your priorities — whether that's maximum durability, supreme comfort, or elegant aesthetics.
"""
    return slug, content

def generate_comparison(boots, brands):
    """比較記事を生成（ランダムに2つのブーツを選択）"""
    pair = random.sample(boots, 2)
    boot_a, boot_b = pair

    brand_a = next((b for b in brands if b["id"] == boot_a["brand"]), None)
    brand_b = next((b for b in brands if b["id"] == boot_b["brand"]), None)

    name_a_short = boot_a["name"].split()[-1] if len(boot_a["name"].split()) > 2 else boot_a["name"]
    name_b_short = boot_b["name"].split()[-1] if len(boot_b["name"].split()) > 2 else boot_b["name"]

    slug = f"{boot_a['brand']}-{name_a_short.lower()}-vs-{boot_b['brand']}-{name_b_short.lower()}"
    slug = slug.replace(" ", "-").replace("'", "")

    content = f"""---
title: "{boot_a['name']} vs {boot_b['name']}: Which Should You Buy?"
description: "A head-to-head comparison of the {boot_a['name']} and {boot_b['name']}. We compare leather, construction, price, and overall value."
category: "comparison"
tags: ["{boot_a['brand']}", "{boot_b['brand']}", "comparison"]
publishedAt: "{today_str()}"
relatedBoots: ["{boot_a['id']}", "{boot_b['id']}"]
articleType: "comparison"
---

## Overview

Choosing between the {boot_a['name']} (${boot_a['price']}) and the {boot_b['name']} (${boot_b['price']}) is a common dilemma. Both are excellent options, but they cater to different preferences and priorities.

## {boot_a['name']}

- **Brand**: {brand_a['name'] if brand_a else boot_a['brand']}
- **Leather**: {boot_a['leather'].replace('-', ' ').title()}
- **Construction**: {boot_a['construction'].replace('-', ' ').title()}
- **Made In**: {boot_a['madeIn']}
- **Price**: ${boot_a['price']}

{boot_a['description']}

## {boot_b['name']}

- **Brand**: {brand_b['name'] if brand_b else boot_b['brand']}
- **Leather**: {boot_b['leather'].replace('-', ' ').title()}
- **Construction**: {boot_b['construction'].replace('-', ' ').title()}
- **Made In**: {boot_b['madeIn']}
- **Price**: ${boot_b['price']}

{boot_b['description']}

## Head-to-Head Comparison

### Leather Quality
Both boots use quality leather, but {boot_a['leather'].replace('-', ' ')} and {boot_b['leather'].replace('-', ' ')} offer different characteristics in terms of patina, durability, and maintenance requirements.

### Construction
{boot_a['construction'].replace('-', ' ').title()} vs {boot_b['construction'].replace('-', ' ').title()} — each method has its strengths. Consider your priorities around resolability, water resistance, and break-in comfort.

### Value
At ${boot_a['price']} vs ${boot_b['price']}, the price difference of ${abs(boot_a['price'] - boot_b['price'])} may be a factor in your decision. Consider the long-term cost-per-wear rather than just the upfront price.

## Verdict

Both are excellent choices. The {boot_a['name']} edges ahead for those who prioritize its specific attributes, while the {boot_b['name']} is the better choice for those who value what it uniquely offers. You genuinely cannot go wrong with either.
"""
    return slug, content

def generate_care_article():
    """ケアガイド記事を生成"""
    topics = [
        {
            "slug": "seasonal-boot-maintenance-guide",
            "title": "Seasonal Boot Maintenance: A Complete Calendar",
            "description": "How to care for your leather boots through every season — from spring conditioning to winter waterproofing.",
            "content_body": """## Spring

Spring is the perfect time for a thorough cleaning after winter. Remove salt stains with a vinegar-water solution, deep condition the leather, and inspect soles for wear.

## Summer

In warmer months, focus on letting boots breathe. Rotate pairs frequently, use cedar shoe trees, and condition less often as leather doesn't dry out as quickly.

## Fall

Prepare your boots for winter by applying a heavier conditioner and considering a waterproofing treatment. Inspect welts and soles for separation.

## Winter

Winter is the harshest season for leather. Wipe off salt and moisture after each wear. Allow boots to dry naturally — never near a radiator. Condition more frequently."""
        },
        {
            "slug": "boot-sole-care-and-replacement-guide",
            "title": "Boot Sole Care & When to Resole",
            "description": "How to know when your boot soles need replacement, how to maintain them, and what to expect from a resole.",
            "content_body": """## Signs You Need a Resole

- The outsole is worn through to the midsole
- You can feel the ground through the sole
- Water seeps through the bottom
- The heel is worn down unevenly

## Maintaining Your Soles

- Leather soles benefit from occasional conditioning with sole guard
- Rotate your boots to allow soles to dry completely
- Consider adding rubber half-soles for extra protection

## The Resoling Process

A quality cobbler can resole Goodyear welted boots for $100-$200. The process takes 2-4 weeks and essentially gives you a new boot from the sole up."""
        },
    ]

    topic = random.choice(topics)
    content = f"""---
title: "{topic['title']}"
description: "{topic['description']}"
category: "care"
tags: ["care", "maintenance", "leather-care"]
publishedAt: "{today_str()}"
articleType: "guide"
---

{topic['content_body']}

## Essential Products

Keep these products in your boot care kit:
- Horsehair brush (daily brushing)
- Quality leather conditioner
- Cedar shoe trees (one per pair)
- Clean cotton cloths
- Waterproofing spray (for wet climates)

## Conclusion

Regular maintenance is the key to boot longevity. A few minutes of care each day will keep your boots looking great and lasting for decades.
"""
    return topic["slug"], content


def main():
    """メイン関数: コマンドライン引数に基づいて記事を生成"""
    parser = argparse.ArgumentParser(description="Boot Craft Archive 記事生成")
    parser.add_argument(
        "--category",
        choices=["review", "leather", "construction", "comparison", "care"],
        required=True,
        help="生成する記事のカテゴリ",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="生成する記事の数（デフォルト: 1）",
    )
    args = parser.parse_args()

    print(f"Boot Craft Archive 記事生成")
    print(f"カテゴリ: {args.category}")
    print(f"生成数: {args.count}")
    print("-" * 40)

    # データの読み込み
    boots = load_json("boots.json")
    brands = load_json("brands.json")
    leathers = load_json("leathers.json")
    constructions = load_json("constructions.json")

    ensure_articles_dir()

    generated = 0
    for i in range(args.count):
        try:
            if args.category == "review":
                slug, content = generate_review(boots, brands)
            elif args.category == "leather":
                slug, content = generate_leather_article(leathers)
            elif args.category == "construction":
                slug, content = generate_construction_article(constructions)
            elif args.category == "comparison":
                slug, content = generate_comparison(boots, brands)
            elif args.category == "care":
                slug, content = generate_care_article()
            else:
                print(f"未対応カテゴリ: {args.category}")
                continue

            if save_article(slug, content):
                generated += 1
        except Exception as e:
            print(f"  エラー: {e}")

    print("-" * 40)
    print(f"完了: {generated}件の記事を生成しました")


if __name__ == "__main__":
    main()
