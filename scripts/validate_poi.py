# -*- coding: utf-8 -*-
import json, sys

REQUIRED = {"id", "name", "lat", "lng", "course", "order", "desc"}

def main():
    with open("poi.json", encoding="utf-8") as f:
        data = json.load(f)
    courses = data["courses"]
    pois = data["pois"]
    errors = []
    ids = set()
    for p in pois:
        missing = REQUIRED - set(p)
        if missing:
            errors.append(f"{p.get('id','?')}: 필드 누락 {missing}")
            continue
        if p["id"] in ids:
            errors.append(f"{p['id']}: id 중복")
        ids.add(p["id"])
        if p["course"] not in courses:
            errors.append(f"{p['id']}: 미정의 course '{p['course']}'")
        if not (37.2 < p["lat"] < 37.8 and 126.8 < p["lng"] < 127.2):
            errors.append(f"{p['id']}: 좌표가 서울·수원 범위 밖 ({p['lat']}, {p['lng']})")
    for cid, c in courses.items():
        if not c.get("name") or not c.get("color", "").startswith("#"):
            errors.append(f"course {cid}: name/color 형식 오류")
    if errors:
        print("\n".join(errors)); sys.exit(1)
    print(f"OK: courses={len(courses)} pois={len(pois)}")

main()
