# -*- coding: utf-8 -*-
"""Stamp when each member joined, and use it when they move to alumni.

Alumni carry a `period` like "24.~26.2", but nothing recorded when a current
member had arrived, so every retirement needed the date looked up by hand -- and
when it could not be, `period` was simply left blank.

This records it up front instead. A member's join date is the day they were
registered on the homepage, which git already knows exactly: the first commit
that put their name into _data/members.yml. New members have no such commit yet,
so they are stamped with today.

    python scripts/members_joined.py            # stamp anyone missing `joined`
    python scripts/members_joined.py --check    # report only, change nothing
    python scripts/members_joined.py --retire "Subin Kang"

--retire moves a member into the matching alumni group and fills `period` in as
`<joined>~<today>`, so the start date needs no lookup.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMBERS = os.path.join(ROOT, "_data", "members.yml")

# which alumni group a retiring member lands in
RETIRE_TO = {
    "ms_students": "former_ms_students",
    "phd_students": "former_ms_students",
    "interns": "former_interns",
}
GROUPS = list(RETIRE_TO)


def ym(date):
    """The "26.9" form the period strings already use (no zero padding)."""
    return "%s.%d" % (date.strftime("%y"), date.month)


def git_joined(*names):
    """Earliest commit introducing any spelling of this name to members.yml.

    Both spellings are tried because names get revised in place -- 'Kho' was
    renamed to 'Koh' long after those members had joined, and searching only the
    current spelling would date them to the rename.
    """
    best = None
    for n in names:
        if not n:
            continue
        out = subprocess.run(
            ["git", "log", "--reverse", "--format=%cI", "-S", n, "--", "_data/members.yml"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout.strip()
        if out:
            iso = out.split("\n")[0]
            if best is None or iso < best:
                best = iso
    if not best:
        return None
    return "%s.%d" % (best[2:4], int(best[5:7]))


def load():
    with open(MEMBERS, encoding="utf-8") as f:
        text = f.read()
    return text, yaml.safe_load(text)


def save(text):
    """Write back, but only if it still parses and nothing else moved."""
    with open(MEMBERS, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def member_blocks(text):
    """(name, start, end) for every list entry, by line index.

    An entry is located by its leading `-`, not by `name:` coming first:
    entries written through the admin CMS come back with their keys sorted, so
    `email:` can legitimately be the first line of a member.
    """
    lines = text.split("\n")
    out = []
    for i, l in enumerate(lines):
        if not re.match(r"^  - \w+:", l):
            continue
        j = i + 1
        while j < len(lines) and (lines[j].startswith("    ") or not lines[j].strip()):
            j += 1
        name = None
        for k in range(i, j):
            m = re.match(r'^(?:  - |    )name:\s*"?([^"\n]+?)"?\s*$', lines[k])
            if m:
                name = m.group(1)
                break
        if name:
            out.append((name, i, j))
    return lines, out

def group_of(data, name):
    for g in GROUPS:
        for m in data["students"].get(g) or []:
            if m["name"] == name:
                return g, m
    return None, None


def stamp(check_only=False):
    text, data = load()
    lines, blocks = member_blocks(text)
    today = ym(datetime.date.today())

    wanted = {}
    for g in GROUPS:
        for m in data["students"].get(g) or []:
            if "joined" in m:
                continue
            wanted[m["name"]] = git_joined(m["name"], m.get("name_ko")) or today

    if not wanted:
        print("모든 멤버에 joined 기록됨 - 변경 없음")
        return 0

    # insert back to front so earlier line numbers stay valid
    added = []
    for name, start, end in reversed(blocks):
        if name not in wanted:
            continue
        anchor = start
        for k in range(start, end):
            if re.match(r"^    name_ko:", lines[k]):
                anchor = k
                break
        lines.insert(anchor + 1, '    joined: "%s"' % wanted[name])
        added.append((name, wanted[name], wanted[name] == today))

    for name, val, is_new in reversed(added):
        print("  + %-18s joined %-7s %s" % (name, val, "(신규 - 오늘)" if is_new else "(git 등록일)"))

    if check_only:
        print("\n--check: 파일은 변경하지 않음")
        return 0

    new_text = "\n".join(lines)
    after = yaml.safe_load(new_text)
    for g in GROUPS:
        before_g = data["students"].get(g) or []
        after_g = after["students"].get(g) or []
        assert len(before_g) == len(after_g), "%s 인원 수가 바뀜" % g
        for b, a in zip(before_g, after_g):
            assert {k: v for k, v in a.items() if k != "joined"} == b, "%s 항목이 변형됨" % b["name"]
    save(new_text)
    print("\n%d명 기록 완료" % len(added))
    return 0


def retire(name):
    text, data = load()
    g, member = group_of(data, name)
    if not member:
        print("현재 멤버에 없음: %s" % name)
        return 1

    joined = member.get("joined")
    if not joined:
        joined = git_joined(member["name"], member.get("name_ko")) or ""
    period = "%s~%s" % (joined, ym(datetime.date.today()))

    lines, blocks = member_blocks(text)
    block = next(((s, e) for n, s, e in blocks if n == name), None)
    start, end = block
    chunk = [l for l in lines[start:end]
             if l.strip() and not re.match(r"^    joined:", l)]
    chunk.append('    period: "%s"' % period)

    del lines[start:end]
    dest = RETIRE_TO[g]
    text = "\n".join(lines)
    anchor = "\n  %s:\n" % dest
    assert text.count(anchor) == 1, "알룸나이 그룹을 찾지 못함: %s" % dest
    i = text.index(anchor) + len(anchor)
    text = text[:i] + "\n".join(chunk) + "\n\n" + text[i:]

    after = yaml.safe_load(text)
    assert all(m["name"] != name for m in after["students"].get(g) or []), "원래 그룹에 남아있음"
    moved = [m for m in after["alumni"][dest] if m["name"] == name]
    assert len(moved) == 1 and moved[0]["period"] == period, "알룸나이 기록 실패"
    save(text)
    print("%s: %s -> alumni.%s   period \"%s\"" % (name, g, dest, period))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="보고만 하고 파일은 그대로 둠")
    ap.add_argument("--retire", metavar="NAME", help="알룸나이로 이동 (period 자동 계산)")
    a = ap.parse_args()
    return retire(a.retire) if a.retire else stamp(a.check)


if __name__ == "__main__":
    sys.exit(main())
