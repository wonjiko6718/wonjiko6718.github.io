# wonjiko6718.github.io

개인 블로그 레포지토리입니다.

---

## 📁 폴더 구조

```
wonjiko6718.github.io/
├── index.html                  # 메인 (글 목록 + 검색)
├── post.html                   # 글 뷰어
├── .nojekyll                   # Jekyll 비활성화
├── update_list.py              # list.json 자동 생성 스크립트
├── assets/
│   ├── css/style.css           # 스타일시트
│   └── images/                 # 이미지 파일
└── posts/
    ├── list.json               # 글 목록 (자동 생성)
    └── YYYY-MM-DD-제목.md      # 블로그 글
```

---

## ✏️ 새 글 작성 방법

### 1. MD 파일 생성

`posts/` 폴더 안에 아래 규칙에 맞게 파일을 만듭니다.

### 2. list.json 자동 업데이트

```bash
python update_list.py
```

### 3. Push

```bash
git add .
git commit -m "새 글 추가: 글 제목"
git push origin main
```

---

## 📄 파일명 규칙

| 항목 | 규칙 |
|------|------|
| 형식 | `YYYY-MM-DD-제목.md` |
| 날짜 | 작성일 기준 (예: `2026-05-10`) |
| 제목 | 영문 소문자, 숫자, 하이픈(`-`)만 사용 |
| 확장자 | 반드시 `.md` (소문자) |

**올바른 예시:**
```
2026-05-10-hello-world.md
2026-05-10-my-first-post.md
2026-05-10-til-javascript.md
```

**잘못된 예시:**
```
2026-05-10-안녕하세요.md     ❌ 한글 사용
2026-05-10_hello_world.md   ❌ 언더스코어 사용
hello-world.md              ❌ 날짜 없음
2026-05-10-Hello-World.MD   ❌ 대문자 사용
```

---

## 📝 Front Matter 규칙

모든 MD 파일 최상단에 아래 형식으로 작성합니다.

```markdown
---
title: 글 제목
date: YYYY-MM-DD
category: 카테고리명
thumbnail: /assets/images/파일명.jpg
---
```

| 항목 | 필수 여부 | 설명 |
|------|----------|------|
| `title` | ✅ 필수 | 글 목록과 페이지 제목에 표시 |
| `date` | ✅ 필수 | `YYYY-MM-DD` 형식 |
| `category` | 선택 | 검색 및 분류에 사용 |
| `thumbnail` | 선택 | 추후 썸네일 기능용 |

---

## 📖 마크다운 문법 기본

### 제목

```markdown
# 제목 1 (h1)
## 제목 2 (h2)
### 제목 3 (h3)
```

---

### 텍스트 강조

```markdown
**굵게**
*기울임*
~~취소선~~
`인라인 코드`
```

**굵게** / *기울임* / ~~취소선~~ / `인라인 코드`

---

### 목록

```markdown
# 순서 없는 목록
- 항목 1
- 항목 2
  - 하위 항목

# 순서 있는 목록
1. 첫 번째
2. 두 번째
3. 세 번째
```

---

### 링크 & 이미지

```markdown
# 링크
[표시할 텍스트](https://example.com)

# 이미지
![대체 텍스트](/assets/images/파일명.jpg)

# 이미지 링크
[![대체 텍스트](/assets/images/파일명.jpg)](https://example.com)
```

---

### 인용구

```markdown
> 인용할 내용을 여기에 씁니다.
> 여러 줄도 가능합니다.
```

---

### 코드 블록

````markdown
# 언어 지정 (문법 강조)
```javascript
console.log("Hello, World!");
```

```python
print("Hello, World!")
```

```bash
git push origin main
```
````

---

### 표

```markdown
| 헤더 1 | 헤더 2 | 헤더 3 |
|--------|--------|--------|
| 내용 1 | 내용 2 | 내용 3 |
| 내용 4 | 내용 5 | 내용 6 |
```

---

### 구분선

```markdown
---
```

---

### 줄바꿈

마크다운에서 줄바꿈은 문장 끝에 **공백 2칸** 또는 **빈 줄**을 넣습니다.

```markdown
첫 번째 줄  
두 번째 줄 (위에 공백 2칸)

세 번째 줄 (빈 줄로 구분)
```

---

## 🖼️ 이미지 업로드 방법

1. `assets/images/` 폴더에 이미지 파일 복사
2. MD 파일에서 참조:

```markdown
![설명](/assets/images/파일명.jpg)
```

> 이미지 파일명도 영문 소문자와 하이픈만 사용을 권장합니다.
