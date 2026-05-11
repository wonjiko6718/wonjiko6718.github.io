import os
import json
import re

# posts 폴더 경로 (이 스크립트와 같은 위치에 posts 폴더가 있다고 가정)
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


def parse_categories(raw):
    """쉼표로 구분된 카테고리 문자열 → 리스트"""
    if not raw:
        return []
    return [c.strip() for c in raw.split(",") if c.strip()]


def build_list():
    if not os.path.isdir(POSTS_DIR):
        print(f"[오류] posts 폴더를 찾을 수 없습니다: {POSTS_DIR}")
        return

    posts = []
    boards = []  # 폴더(게시판) 목록

    # posts/ 루트의 MD 파일 (폴더 없이 바로 있는 글)
    root_mds = []
    for filename in sorted(os.listdir(POSTS_DIR), reverse=True):
        filepath = os.path.join(POSTS_DIR, filename)
        if os.path.isfile(filepath) and filename.endswith(".md"):
            root_mds.append((filename, filepath, None))

    # posts/ 하위 폴더 탐색
    folder_entries = []
    for entry in sorted(os.listdir(POSTS_DIR)):
        entry_path = os.path.join(POSTS_DIR, entry)
        if os.path.isdir(entry_path):
            boards.append(entry)
            print(f"\n📁 게시판: {entry}")
            for filename in sorted(os.listdir(entry_path), reverse=True):
                filepath = os.path.join(entry_path, filename)
                if os.path.isfile(filepath) and filename.endswith(".md"):
                    folder_entries.append((filename, filepath, entry))

    # 루트 MD + 폴더 MD 합치기 (폴더 글 먼저, 루트 글 나중)
    all_entries = folder_entries + root_mds

    for filename, filepath, board in all_entries:
        meta    = parse_front_matter(filepath)
        post_id = os.path.splitext(filename)[0]

        # id는 폴더가 있으면 "폴더명/파일명" 형태로 저장
        full_id = f"{board}/{post_id}" if board else post_id

        posts.append({
            "id":        full_id,
            "title":     meta.get("title", post_id),
            "date":      meta.get("date", ""),
            "category":  parse_categories(meta.get("category", "")),
            "thumbnail": meta.get("thumbnail", ""),
            "board":     board or "",  # 게시판(폴더)명
        })
        print(f"  ✔ {full_id}")

    # list.json 저장
    output = {
        "boards": boards,   # 게시판 목록
        "posts":  posts,    # 전체 글 목록
    }

    with open(LIST_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ list.json 업데이트 완료")
    print(f"   게시판 {len(boards)}개 / 글 {len(posts)}개")


if __name__ == "__main__":
    print("📝 list.json 생성 중...\n")
    build_list()
