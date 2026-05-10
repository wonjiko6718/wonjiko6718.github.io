import os
import json
import re

POSTS_DIR = os.path.join(os.path.dirname(__file__), "posts")
LIST_JSON  = os.path.join(POSTS_DIR, "list.json")


def parse_front_matter(filepath):
    """MD 파일에서 Front Matter(--- ... ---) 파싱"""
    meta = {}
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", content)
    if match:
        for line in match.group(1).splitlines():
            if ":" in line:
                key, _, val = line.partition(":")
                meta[key.strip()] = val.strip()
    return meta


def get_post_id(filename):
    """파일명에서 .md 제거해 id 반환"""
    return os.path.splitext(filename)[0]


def build_list():
    if not os.path.isdir(POSTS_DIR):
        print(f"[오류] posts 폴더를 찾을 수 없습니다: {POSTS_DIR}")
        return

    posts = []
    for filename in sorted(os.listdir(POSTS_DIR), reverse=True):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(POSTS_DIR, filename)
        meta     = parse_front_matter(filepath)
        post_id  = get_post_id(filename)

        posts.append({
            "id":        post_id,
            "title":     meta.get("title", post_id),
            "date":      meta.get("date", ""),
            "category":  meta.get("category", ""),
            "thumbnail": meta.get("thumbnail", ""),
        })
        print(f"  ✔ {filename}")

    with open(LIST_JSON, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"\n✅ list.json 업데이트 완료 ({len(posts)}개 글)")


if __name__ == "__main__":
    print("📝 list.json 생성 중...\n")
    build_list()
