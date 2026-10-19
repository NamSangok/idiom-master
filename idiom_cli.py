#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IdiomMaster CLI - 터미널용 다빈도 영어 숙어 암기장
"""

import json
import os
import random
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

DATA_FILE = os.path.join(os.path.dirname(__file__), "idioms_data.json")

def load_idioms():
    if not os.path.exists(DATA_FILE):
        print(f"데이터 파일({DATA_FILE})이 존재하지 않습니다.")
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"데이터 로드 에러: {e}")
        return []

def save_idioms(idioms):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(idioms, f, ensure_ascii=False, indent=2)
        print("\n✅ 데이터가 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"\n❌ 저장 중 오류 발생: {e}")

def print_banner():
    print("=" * 60)
    print("      🌟 IdiomMaster - 나만의 다빈도 영어 숙어 암기장 🌟")
    print("=" * 60)

def show_stats(idioms):
    total = len(idioms)
    mastered = sum(1 for i in idioms if i.get("status") == "mastered")
    learning = total - mastered
    fav = sum(1 for i in idioms if i.get("favorite"))
    pct = round((mastered / total) * 100) if total > 0 else 0

    print(f"\n📊 [학습 통계]")
    print(f" • 총 숙어 수: {total}개")
    print(f" • 암기 완료: {mastered}개 ({pct}%)")
    print(f" • 복습 필요: {learning}개")
    print(f" • ⭐ 즐겨찾기: {fav}개")
    print("-" * 60)

def flashcard_mode(idioms):
    if not idioms:
        print("등록된 숙어가 없습니다.")
        return

    print("\n📇 [플래시카드 학습 모드]")
    print("1. 전체 숙어 학습")
    print("2. 📖 복습 필요한 숙어만")
    print("3. ⭐ 즐겨찾기한 숙어만")
    choice = input("선택하세요 (기본: 1): ").strip()

    deck = idioms
    if choice == "2":
        deck = [i for i in idioms if i.get("status") != "mastered"]
    elif choice == "3":
        deck = [i for i in idioms if i.get("favorite")]

    if not deck:
        print("해당 조건의 숙어가 없습니다.")
        return

    deck = deck.copy()
    random.shuffle(deck)

    print(f"\n총 {len(deck)}개의 카드로 학습을 시작합니다. (중단하려면 'q' 입력)")
    
    for idx, item in enumerate(deck, 1):
        print("\n" + "=" * 50)
        fav_icon = "★" if item.get("favorite") else "☆"
        print(f"[{idx}/{len(deck)}] [{item.get('category', '일상')}] {fav_icon}")
        print(f"\n👉 숙어: \033[1m{item['idiom']}\033[0m")
        if item.get("pronunciation"):
            print(f"   발음: {item['pronunciation']}")
        
        user_input = input("\n[Enter]를 누르면 뜻과 유래가 나타납니다 (종료: q): ").strip()
        if user_input.lower() == 'q':
            break

        print("\n---------------- [뒷면 확인] ----------------")
        print(f"💡 뜻: \033[32;1m{item['meaning']}\033[0m")
        if item.get("origin"):
            print(f"\n📜 [유래 & 암기팁]\n   {item['origin']}")
        if item.get("example"):
            print(f"\n📖 [실전 예문]\n   {item['example']}")
            print(f"   {item.get('exampleKo', '')}")
        if item.get("dialogue") and item["dialogue"].get("speakerA"):
            dlg = item["dialogue"]
            print(f"\n💬 [대화 예시]\n   A: {dlg['speakerA']}\n   B: {dlg['speakerB']}")

        print("\n--------------------------------------------")
        status_choice = input("이 숙어를 외우셨나요? [1] 외웠어요(완료)  [2] 다시 볼래요(유지)  [Enter: 다음]: ").strip()
        if status_choice == "1":
            item["status"] = "mastered"
            print("🎉 '암기 완료'로 표시되었습니다!")
        elif status_choice == "2":
            item["status"] = "learning"
            print("📖 '복습 필요'로 표시되었습니다.")
    
    save_idioms(idioms)

def quiz_mode(idioms):
    if len(idioms) < 4:
        print("퀴즈를 풀기 위해 최소 4개 이상의 숙어가 필요합니다.")
        return

    print("\n🎯 [실전 숙어 퀴즈 모드]")
    count_str = input("풀고 싶은 문제 수를 입력하세요 (기본: 5): ").strip()
    try:
        count = int(count_str) if count_str else 5
    except ValueError:
        count = 5

    count = min(count, len(idioms))
    sample_pool = random.sample(idioms, count)
    score = 0
    mistakes = []

    for idx, q in enumerate(sample_pool, 1):
        print("\n" + "=" * 50)
        print(f"문제 {idx}/{count}")
        print(f"👉 다음 숙어의 올바른 의미는 무엇일까요?")
        print(f"\n   \033[1m\"{q['idiom']}\"\033[0m")
        if q.get("example"):
            hint_ex = q["example"].replace(q["idiom"], "[ ... ]")
            print(f"   (힌트 예문: {hint_ex})")

        correct_ans = q["meaning"]
        wrong_candidates = [i["meaning"] for i in idioms if i["id"] != q["id"] and i["meaning"] != correct_ans]
        options = random.sample(wrong_candidates, min(3, len(wrong_candidates))) + [correct_ans]
        random.shuffle(options)

        for opt_idx, opt in enumerate(options, 1):
            print(f"   [{opt_idx}] {opt}")

        while True:
            user_choice = input("\n정답 번호를 입력하세요 (1~4, 종료: q): ").strip()
            if user_choice.lower() == 'q':
                return
            if user_choice in ["1", "2", "3", "4"]:
                selected_opt = options[int(user_choice) - 1]
                if selected_opt == correct_ans:
                    print("\n🎉 정답입니다!")
                    score += 1
                else:
                    print(f"\n❌ 아쉽습니다! 정답은: \033[32m{correct_ans}\033[0m")
                    mistakes.append(q)
                break
            print("올바른 번호를 입력해 주세요.")

    pct = round((score / count) * 100)
    print("\n" + "=" * 50)
    print(f"🏁 퀴즈 결과: {count}문제 중 {score}문제 정답 ({pct}%)")
    if mistakes:
        print("\n📝 [오답 복습 노트]")
        for m in mistakes:
            print(f" • {m['idiom']} : {m['meaning']}")
            print(f"   (예: {m.get('example', '')})")

def search_and_list(idioms):
    query = input("\n검색할 키워드를 입력하세요 (전체 보기는 Enter): ").strip().lower()
    results = []
    for item in idioms:
        if not query:
            results.append(item)
        else:
            in_idiom = query in item["idiom"].lower()
            in_meaning = query in item["meaning"].lower()
            in_tags = any(query in t.lower() for t in item.get("tags", []))
            if in_idiom or in_meaning or in_tags:
                results.append(item)

    print(f"\n총 {len(results)}개의 숙어가 검색되었습니다.\n")
    for idx, item in enumerate(results, 1):
        status_mark = "✅" if item.get("status") == "mastered" else "📖"
        fav_mark = "★" if item.get("favorite") else " "
        print(f"{idx:2d}. {status_mark} {fav_mark} \033[1m{item['idiom']:<26}\033[0m : {item['meaning']}")

    detail_idx = input("\n상세보기를 원하는 번호를 입력하세요 (엔터: 메뉴로 복귀): ").strip()
    if detail_idx.isdigit() and 1 <= int(detail_idx) <= len(results):
        item = results[int(detail_idx) - 1]
        print("\n" + "=" * 50)
        print(f"📌 숙어: {item['idiom']} {item.get('pronunciation', '')}")
        print(f"카테고리: {item.get('category', '일상')} | 상태: {item.get('status', 'learning')}")
        print(f"💡 뜻: {item['meaning']}")
        if item.get("origin"):
            print(f"📜 유래: {item['origin']}")
        if item.get("example"):
            print(f"📖 예문: {item['example']}")
            print(f"   {item.get('exampleKo', '')}")
        input("\n계속하려면 Enter를 누르세요...")

def add_custom_idiom(idioms):
    print("\n➕ [나만의 새로운 숙어 추가]")
    idiom_text = input("영어 숙어 입력 (예: piece of cake): ").strip()
    if not idiom_text:
        print("숙어는 비어 있을 수 없습니다.")
        return

    meaning_text = input("한글 뜻 입력 (예: 식은 죽 먹기): ").strip()
    if not meaning_text:
        print("뜻은 비어 있을 수 없습니다.")
        return

    category = input("카테고리 (1: 일상회화, 2: 비즈니스, 3: 감정·태도, 기본: 일상회화): ").strip()
    cat_map = {"1": "일상회화", "2": "비즈니스", "3": "감정·태도"}
    category_val = cat_map.get(category, "일상회화")

    pron = input("발음 기호/힌트 (선택): ").strip()
    origin = input("외우는 꿀팁 / 어원 유래 (선택): ").strip()
    example = input("영문 실전 예문 (선택): ").strip()
    example_ko = input("예문 한글 해석 (선택): ").strip()
    tags = input("태그 (쉼표로 구분, 선택): ").strip()

    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    new_entry = {
        "id": f"custom_{int(random.random()*1000000)}",
        "idiom": idiom_text,
        "meaning": meaning_text,
        "pronunciation": pron,
        "category": category_val,
        "origin": origin,
        "example": example,
        "exampleKo": example_ko,
        "tags": tag_list,
        "status": "learning",
        "favorite": False
    }

    idioms.append(new_entry)
    save_idioms(idioms)
    print(f"\n🎉 '{idiom_text}' 숙어가 성공적으로 추가되었습니다!")

def main():
    idioms = load_idioms()
    while True:
        print_banner()
        show_stats(idioms)
        print("  1. 📇 플래시카드 암기 학습 (추천)")
        print("  2. 🎯 실전 숙어 퀴즈 챌린지")
        print("  3. 🔍 숙어 검색 및 상세 목록 보기")
        print("  4. ➕ 나만의 숙어 추가하기")
        print("  5. 💾 데이터 저장")
        print("  0. 🚪 프로그램 종료")
        print("=" * 60)

        choice = input("원하는 메뉴를 선택하세요 (0~5): ").strip()
        if choice == "1":
            flashcard_mode(idioms)
        elif choice == "2":
            quiz_mode(idioms)
        elif choice == "3":
            search_and_list(idioms)
        elif choice == "4":
            add_custom_idiom(idioms)
        elif choice == "5":
            save_idioms(idioms)
        elif choice == "0":
            save_idioms(idioms)
            print("\n🌟 오늘도 유익한 영어 공부 되셨기를 바랍니다. 안녕히 가세요!")
            break
        else:
            print("\n올바른 번호를 선택해 주세요.")

if __name__ == "__main__":
    main()
