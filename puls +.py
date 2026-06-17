import pygame # type: ignore
import random 
import sys
import json
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
from datetime import datetime

# ==================== 顏色定義 ====================
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,200,0)
BLUE = (0,120,255)
PINK = (255,80,180)
ORANGE = (255,165,0)
PURPLE = (128,0,128)
YELLOW = (255,255,0)
GRAY = (128,128,128)
DARK_GRAY = (64,64,64)
LIGHT_GRAY = (200,200,200)
CYAN = (0,255,255)
BROWN = (139,69,19)
GOLD = (255,215,0)
SILVER = (192,192,192)
BRONZE = (205,127,50)

# ==================== 遊戲基礎參數 ====================
CELL = 25
WIDTH, HEIGHT = 600, 650

# ==================== 速度控制全局變量 ====================
SPEED_PRESETS = {
    "Very Slow": 250,
    "Slow": 180,
    "Normal": 150,
    "Fast": 100,
    "Very Fast": 70,
    "Extreme": 50
}
DEFAULT_SPEED = 150

# 句子结束标点符号
SENTENCE_END_PUNCTUATIONS = [".", "!", "?"]
ALL_PUNCTUATIONS = [",", ".", "!", "?"]

# ==================== Easy模式变体配置 ====================
EASY_MODE_VARIANTS = {
    "standard": {
        "name": "Standard",
        "description": "Standard sentence building",
        "include_subject": True,
        "include_verb": True,
        "include_noun": True,
        "include_adjective": True,
        "include_conjunction": False,
        "include_preposition": False,
        "include_adverb": False,
        "include_helpers": True
    },
    "simple": {
        "name": "Simple",
        "description": "Subject + Verb + Object only",
        "include_subject": True,
        "include_verb": True,
        "include_noun": True,
        "include_adjective": False,
        "include_conjunction": False,
        "include_preposition": False,
        "include_adverb": False,
        "include_helpers": True
    },
    "verb_focus": {
        "name": "Verb Focus",
        "description": "Practice verb conjugation",
        "include_subject": True,
        "include_verb": True,
        "include_noun": False,
        "include_adjective": True,
        "include_conjunction": False,
        "include_preposition": False,
        "include_adverb": False,
        "include_helpers": True
    },
    "noun_focus": {
        "name": "Noun Focus",
        "description": "Practice noun genders",
        "include_subject": False,
        "include_verb": False,
        "include_noun": True,
        "include_adjective": True,
        "include_conjunction": False,
        "include_preposition": True,
        "include_adverb": False,
        "include_helpers": True
    },
    "connector": {
        "name": "Connector",
        "description": "Practice conjunctions",
        "include_subject": True,
        "include_verb": True,
        "include_noun": True,
        "include_adjective": True,
        "include_conjunction": True,
        "include_preposition": True,
        "include_adverb": True,
        "include_helpers": True
    },
    "daily_phrases": {
        "name": "Daily Phrases",
        "description": "Common everyday phrases",
        "include_subject": True,
        "include_verb": True,
        "include_noun": True,
        "include_adjective": True,
        "include_conjunction": False,
        "include_preposition": True,
        "include_adverb": True,
        "include_helpers": True
    }
}

# ==================== 词库 ====================
VERBS_DATA = {
    "sein": {"ich": "bin", "du": "bist", "er/sie/es": "ist", "wir": "sind", "ihr": "seid", "Sie": "sind"},
    "haben": {"ich": "habe", "du": "hast", "er/sie/es": "hat", "wir": "haben", "ihr": "habt", "Sie": "haben"},
    "gehen": {"ich": "gehe", "du": "gehst", "er/sie/es": "geht", "wir": "gehen", "ihr": "geht", "Sie": "gehen"},
    "kommen": {"ich": "komme", "du": "kommst", "er/sie/es": "kommt", "wir": "kommen", "ihr": "kommt", "Sie": "kommen"},
    "sehen": {"ich": "sehe", "du": "siehst", "er/sie/es": "sieht", "wir": "sehen", "ihr": "seht", "Sie": "sehen"},
    "essen": {"ich": "esse", "du": "isst", "er/sie/es": "isst", "wir": "essen", "ihr": "esst", "Sie": "essen"},
}

NOUNS_DATA = {
    "der": ["Mann", "Tisch", "Hund", "Tag", "Apfel", "Computer", "Vater"],
    "die": ["Frau", "Katze", "Blume", "Tür", "Lampe", "Schule", "Mutter"],
    "das": ["Kind", "Haus", "Auto", "Buch", "Fenster", "Handy", "Mädchen"]
}

ADJECTIVES_DATA = ["gut", "schlecht", "groß", "klein", "neu", "alt", "schön", "schnell"]
CONJUNCTIONS_DATA = ["und", "aber", "denn", "oder", "weil", "dass"]
PREPOSITIONS_DATA = ["in", "auf", "an", "zu", "mit", "nach", "vor"]
ADVERBS_DATA = ["heute", "gerne", "oft", "immer", "nie", "jetzt", "dann"]
HELPER_WORDS = {"starters": ["Heute", "Jetzt", "Dann", "Morgen"], "connectors": ["weil", "dass", "wenn"]}

GERMAN_LETTERS = list("abcdefghijklmnopqrstuvwxyzäöüß")
COMMON_WORDS = set([
    "ich", "du", "er", "sie", "es", "wir", "ihr", "Sie",
    "der", "die", "das", "den", "dem", "des", "ein", "eine",
    "bin", "bist", "ist", "sind", "seid", "habe", "hast", "hat", "haben", "habt"
])

# ==================== 渲染函数 ====================
def draw_text_with_shadow(surface, text, font, x, y, color=WHITE, shadow_color=BLACK, offset=1):
    shadow = font.render(text, True, shadow_color)
    main = font.render(text, True, color)
    surface.blit(shadow, (x + offset, y + offset))
    surface.blit(main, (x, y))

# ==================== 难度配置 ====================
@dataclass
class DifficultyConfig:
    name: str
    speed: int
    allow_wrap: bool
    self_collision_fatal: bool
    word_source: str
    base_score_per_word: int
    color: Tuple[int,int,int]
    subject: str = None

# ==================== 句子碎片池 ====================
class SentencePool:
    def __init__(self, variant_config: dict = None):
        self.all_fragments = []
        self.variant = variant_config if variant_config else EASY_MODE_VARIANTS["standard"]
        self._build()
    
    def _build(self):
        cfg = self.variant
        
        if cfg.get("include_subject", True):
            for s in ["ich", "du", "er", "sie", "es", "wir", "ihr", "Sie"]:
                self.all_fragments.append({"word": s, "type": "subject", "base_form": s})
                self.all_fragments.append({"word": s, "type": "subject", "base_form": s})
        
        if cfg.get("include_verb", True):
            for vb, conj in VERBS_DATA.items():
                for form in conj.values():
                    if isinstance(form, str):
                        self.all_fragments.append({"word": form, "type": "verb", "base_form": vb})
                        if vb in ["sein", "haben"]:
                            self.all_fragments.append({"word": form, "type": "verb", "base_form": vb})
        
        if cfg.get("include_noun", True):
            for art, nouns in NOUNS_DATA.items():
                for n in nouns:
                    self.all_fragments.append({"word": f"{art} {n}", "type": "noun", "base_form": n})
        
        if cfg.get("include_adjective", True):
            for adj in ADJECTIVES_DATA:
                self.all_fragments.append({"word": adj, "type": "adjective", "base_form": adj})
        
        if cfg.get("include_conjunction", False):
            for c in CONJUNCTIONS_DATA:
                self.all_fragments.append({"word": c, "type": "conjunction", "base_form": c})
        
        if cfg.get("include_preposition", False):
            for p in PREPOSITIONS_DATA:
                self.all_fragments.append({"word": p, "type": "preposition", "base_form": p})
        
        if cfg.get("include_adverb", False):
            for a in ADVERBS_DATA:
                self.all_fragments.append({"word": a, "type": "adverb", "base_form": a})
        
        for p in ALL_PUNCTUATIONS:
            self.all_fragments.append({"word": p, "type": "punctuation", "base_form": p})
            if p in [".", "!", "?"]:
                self.all_fragments.append({"word": p, "type": "punctuation", "base_form": p})
        
        if cfg.get("include_helpers", True):
            for w in HELPER_WORDS["starters"]:
                self.all_fragments.append({"word": w, "type": "helper", "base_form": w})
        
        random.shuffle(self.all_fragments)
        print(f"碎片池: {len(self.all_fragments)} 个碎片")
    
    def get_conjugated_verb(self, verb_base: str, subject: str) -> str:
        if verb_base in VERBS_DATA:
            return VERBS_DATA[verb_base].get(subject, verb_base)
        return verb_base
    
    def get_random(self, subject: str = None) -> dict:
        if not self.all_fragments:
            return {"word": "Hallo", "type": "default"}
        f = random.choice(self.all_fragments).copy()
        if subject and f["type"] == "verb":
            f["word"] = self.get_conjugated_verb(f["base_form"], subject)
        return f

# ==================== 分数记录 ====================
@dataclass
class ScoreRecord:
    score: int; mode: str; date: str; length: int

class ScoreBoard:
    def __init__(self):
        self.records = []
        self.load()
    
    def load(self):
        try:
            with open("snake_scores.txt", "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        self.records.append(ScoreRecord(
                            score=int(parts[0]), mode=parts[1], date=parts[2], length=int(parts[3])
                        ))
        except: pass
        self.records.sort(key=lambda x: x.score, reverse=True)
    
    def save(self):
        with open("snake_scores.txt", "w") as f:
            for r in self.records[:10]:
                f.write(f"{r.score}|{r.mode}|{r.date}|{r.length}\n")
    
    def add(self, score: int, mode: str, length: int):
        self.records.append(ScoreRecord(score, mode, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), length))
        self.records.sort(key=lambda x: x.score, reverse=True)
        self.records = self.records[:10]
        self.save()
    
    def get_top(self, n=10):
        return self.records[:n]

score_board = ScoreBoard()
screen = None
sentence_pool = SentencePool()

# ==================== 按钮类 ====================
class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, text_color=WHITE, font_size=20):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("arial", font_size)
        self.hovered = False
    
    def draw(self, surf):
        col = self.hover if self.hovered else self.color
        pygame.draw.rect(surf, col, self.rect)
        pygame.draw.rect(surf, WHITE, self.rect, 2)
        tw = self.font.size(self.text)[0]
        th = self.font.get_height()
        draw_text_with_shadow(surf, self.text, self.font, 
                              self.rect.x + (self.rect.w - tw)//2, 
                              self.rect.y + (self.rect.h - th)//2, 
                              self.text_color, BLACK, 1)
    
    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                return True
        return False

# ==================== 语法助手 ====================
class GrammarHelper:
    def __init__(self):
        self.completed = []
    
    def add(self, sentence: str, score: int):
        self.completed.append({"sentence": sentence, "score": score, "time": datetime.now().strftime("%H:%M:%S")})
        if len(self.completed) > 10:
            self.completed.pop(0)
    
    def clear(self):
        self.completed.clear()
    
    def check(self, words):
        if not words:
            return False, "句子为空"
        
        clean = [w for w in words if w not in SENTENCE_END_PUNCTUATIONS]
        if not clean:
            return False, "只有标点"
        
        has_verb = False
        for w in clean:
            if w in ["bin","bist","ist","sind","seid","habe","hast","hat","haben","habt"] or w.endswith(('e','t','st','en')):
                if w not in ["ich","du","er","sie","es","wir","ihr","Sie","der","die","das"]:
                    has_verb = True
                    break
        
        issues = []
        if not has_verb and len(clean) > 1:
            issues.append("缺少动词")
        
        if clean[0] and clean[0][0].islower() and clean[0] not in ["ich","du","er","sie","es","wir","ihr","Sie"]:
            issues.append("首字母应大写")
        
        if words[-1] not in SENTENCE_END_PUNCTUATIONS:
            issues.append("应以 . ! ? 结尾")
        
        if issues:
            return False, "； ".join(issues[:2])
        return True, "语法正确"

# ==================== 单词系统 ====================
class WordSystem:
    def __init__(self, config):
        self.config = config
        self.items = []
        self.target = 30
        self.spawn()
    
    def _random_pos(self):
        return (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT - 150, CELL))
    
    def _gen_sentence(self):
        self.target = random.randint(28, 40)
        items = []
        used = set()
        subj = self.config.subject if self.config.word_source == "sentence" else None
        for _ in range(self.target):
            pos = self._random_pos()
            while pos in used:
                pos = self._random_pos()
            used.add(pos)
            f = sentence_pool.get_random(subj)
            items.append({"pos": pos, "char": f["word"], "type": f["type"], "base": f.get("base_form", f["word"])})
        return items
    
    def _gen_letters(self):
        self.target = random.randint(35, 50)
        items = []
        used = set()
        for _ in range(self.target):
            pos = self._random_pos()
            while pos in used:
                pos = self._random_pos()
            used.add(pos)
            items.append({"pos": pos, "char": random.choice(GERMAN_LETTERS), "type": "letter"})
        return items
    
    def spawn(self):
        if self.config.word_source == "sentence":
            self.items = self._gen_sentence()
        else:
            self.items = self._gen_letters()
    
    def draw(self):
        for item in self.items:
            x, y = item["pos"]
            t = item["type"]
            if t == "subject":
                pygame.draw.rect(screen, CYAN, (x, y, CELL-1, CELL-1))
            elif t == "verb":
                pygame.draw.rect(screen, YELLOW, (x, y, CELL-1, CELL-1))
            elif t == "noun":
                pygame.draw.rect(screen, ORANGE, (x, y, CELL-1, CELL-1))
            elif t == "punctuation":
                pygame.draw.rect(screen, PURPLE, (x, y, CELL-1, CELL-1))
            elif t == "letter":
                pygame.draw.circle(screen, BLUE, (x + CELL//2, y + CELL//2), CELL//2)
            else:
                pygame.draw.rect(screen, GREEN, (x, y, CELL-1, CELL-1))
            font = pygame.font.SysFont("arial", 16)
            draw_text_with_shadow(screen, item["char"], font, x + 3, y + 5, WHITE, BLACK, 1)
    
    def eat(self, head):
        for i, item in enumerate(self.items):
            if item["pos"] == head:
                return self.items.pop(i)
        return None
    
    def refill(self):
        while len(self.items) < self.target:
            pos = self._random_pos()
            if pos not in [i["pos"] for i in self.items]:
                if self.config.word_source == "sentence":
                    f = sentence_pool.get_random(self.config.subject)
                    self.items.append({"pos": pos, "char": f["word"], "type": f["type"], "base": f.get("base_form", f["word"])})
                else:
                    self.items.append({"pos": pos, "char": random.choice(GERMAN_LETTERS), "type": "letter"})
    
    def check_completion(self, collected):
        if self.config.word_source == "sentence":
            if collected and collected[-1] in SENTENCE_END_PUNCTUATIONS:
                formed = " ".join(collected)
                score = len(collected) * self.config.base_score_per_word
                return True, score, formed, "sentence"
            return False, 0, "", ""
        else:
            word = "".join(collected).lower()
            if len(word) >= 2 and word in COMMON_WORDS:
                score = len(word) * self.config.base_score_per_word
                return True, score, word, "word"
            return False, 0, "", ""

# ==================== 蛇类 ====================
class Snake:
    def __init__(self, config):
        self.config = config
        self.body = [(WIDTH//2, HEIGHT//2 - 50)]
        self.dir = (CELL, 0)
        self.next_dir = (CELL, 0)
        self.collected = []
        self.score = 0
        self.alive = True
        self.pool = []
        self.subject = config.subject if config.subject else "?"
    
    def move(self):
        self.dir = self.next_dir
        hx, hy = self.body[0]
        nx, ny = hx + self.dir[0], hy + self.dir[1]
        
        if self.config.allow_wrap:
            if nx < 0: nx = WIDTH - CELL
            elif nx >= WIDTH: nx = 0
            if ny < 0: ny = HEIGHT - 150 - CELL
            elif ny >= HEIGHT - 150: ny = 0
        else:
            if nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT - 150:
                self.alive = False
                return False
        
        new_head = (nx, ny)
        
        if new_head in self.body:
            if self.config.self_collision_fatal:
                self.alive = False
                return False
            else:
                self.score = max(0, self.score - 5)
                self.body.insert(0, new_head)
                self.body.pop()
                return True
        
        self.body.insert(0, new_head)
        self.body.pop()
        return True
    
    def grow(self):
        self.body.append(self.body[-1])
    
    def change_dir(self, d):
        if (d[0] * -1, d[1] * -1) != self.dir:
            self.next_dir = d
    
    def draw(self):
        for i, pos in enumerate(self.body):
            x, y = pos
            if i == 0:
                pygame.draw.rect(screen, self.config.color, (x, y, CELL-1, CELL-1))
                pygame.draw.circle(screen, WHITE, (x + CELL-6, y + CELL//3), 3)
                pygame.draw.circle(screen, WHITE, (x + CELL-6, y + 2*CELL//3), 3)
            else:
                pygame.draw.rect(screen, GREEN, (x, y, CELL-1, CELL-1))

# ==================== UI函数 ====================
def draw_pool(pool_list, config, subject):
    if config.word_source != "sentence":
        return
    y = HEIGHT - 140
    pygame.draw.rect(screen, DARK_GRAY, (0, y, WIDTH, 130))
    pygame.draw.rect(screen, WHITE, (0, y, WIDTH, 130), 2)
    font = pygame.font.SysFont("arial", 16)
    draw_text_with_shadow(screen, f"Subject: {subject.upper()}", font, 10, y + 5, YELLOW, BLACK, 1)
    if pool_list:
        text = subject + " -> " + " -> ".join(pool_list)
        if len(text) > 45:
            text = text[:42] + "..."
        draw_text_with_shadow(screen, text, font, 10, y + 35, WHITE, BLACK, 1)

def show_grammar_panel(sentence, subject, helper):
    w, h = 500, 400
    px, py = (WIDTH - w)//2, (HEIGHT - h)//2
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, DARK_GRAY, (px, py, w, h))
    pygame.draw.rect(screen, GOLD, (px, py, w, h), 3)
    
    y = py + 15
    font = pygame.font.SysFont("arial", 20)
    draw_text_with_shadow(screen, "Grammar Helper", font, px + w//2 - 60, y, YELLOW, BLACK, 1)
    y += 35
    
    font = pygame.font.SysFont("arial", 16)
    draw_text_with_shadow(screen, "Current:", font, px + 15, y, CYAN, BLACK, 1)
    y += 25
    
    text = subject + " -> " + " -> ".join(sentence) if sentence else "(empty)"
    if len(text) > 50:
        text = text[:47] + "..."
    draw_text_with_shadow(screen, text, pygame.font.SysFont("arial", 14), px + 15, y, WHITE, BLACK, 1)
    y += 40
    
    ok, msg = helper.check(sentence)
    color = GREEN if ok else ORANGE
    draw_text_with_shadow(screen, "Check:", font, px + 15, y, color, BLACK, 1)
    y += 25
    for i, line in enumerate(msg.split("；")[:2]):
        draw_text_with_shadow(screen, f"  {line}", pygame.font.SysFont("arial", 13), px + 15, y + i*20, WHITE, BLACK, 1)
    y += 60
    
    draw_text_with_shadow(screen, "Completed:", font, px + 15, y, GOLD, BLACK, 1)
    y += 25
    for i, item in enumerate(helper.completed[-5:]):
        s = item["sentence"][:30] + "..." if len(item["sentence"]) > 30 else item["sentence"]
        draw_text_with_shadow(screen, f"{i+1}. {s} (+{item['score']})", pygame.font.SysFont("arial", 12), px + 20, y + i*18, LIGHT_GRAY, BLACK, 1)
    
    close = Button(px + w - 70, py + h - 40, 60, 30, "Close", RED, DARK_GRAY, WHITE, 16)
    close.draw(screen)
    pygame.display.update()
    
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return
            if close.handle(ev):
                return

def pause_menu(score, mode, length, sentence, subject, helper):
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.set_alpha(180)
    bg.fill(BLACK)
    
    btns = [
        Button(WIDTH//2 - 125, 100, 250, 45, "Resume", GREEN, DARK_GRAY),
        Button(WIDTH//2 - 125, 160, 250, 45, "Grammar Helper", PURPLE, DARK_GRAY),
        Button(WIDTH//2 - 125, 220, 250, 45, "Save & Exit", BLUE, DARK_GRAY),
        Button(WIDTH//2 - 125, 280, 250, 45, "Exit (No Save)", ORANGE, DARK_GRAY),
        Button(WIDTH//2 - 125, 340, 250, 45, "Scoreboard", GOLD, DARK_GRAY),
        Button(WIDTH//2 - 125, 400, 250, 45, "Quit Game", RED, DARK_GRAY),
    ]
    
    while True:
        screen.blit(bg, (0, 0))
        font = pygame.font.SysFont("arial", 48)
        draw_text_with_shadow(screen, "PAUSED", font, WIDTH//2 - 80, 30, YELLOW, BLACK, 2)
        font = pygame.font.SysFont("arial", 20)
        draw_text_with_shadow(screen, f"Score: {score}", font, WIDTH//2 - 50, 70, WHITE, BLACK, 1)
        for btn in btns:
            btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return "resume"
            for i, btn in enumerate(btns):
                if btn.handle(ev):
                    if i == 0:
                        return "resume"
                    elif i == 1:
                        show_grammar_panel(sentence, subject, helper)
                        screen.blit(bg, (0, 0))
                        for b in btns:
                            b.draw(screen)
                        pygame.display.update()
                    elif i == 2:
                        score_board.add(score, mode, length)
                        return "menu"
                    elif i == 3:
                        helper.clear()
                        return "menu"
                    elif i == 4:
                        show_scoreboard_screen()
                        screen.blit(bg, (0, 0))
                        for b in btns:
                            b.draw(screen)
                        pygame.display.update()
                    elif i == 5:
                        pygame.quit()
                        sys.exit()

def show_scoreboard_screen():
    scroll = 0
    records = score_board.get_top()
    max_scroll = max(0, len(records) - 8)
    back = Button(WIDTH//2 - 80, HEIGHT - 60, 160, 40, "Back", GRAY, DARK_GRAY, WHITE, 20)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 36)
        draw_text_with_shadow(screen, "HIGH SCORES", font, WIDTH//2 - 100, 30, YELLOW, BLACK, 2)
        font = pygame.font.SysFont("arial", 18)
        headers = ["Rank", "Score", "Mode", "Length"]
        xs = [50, 150, 250, 350]
        for i, h in enumerate(headers):
            draw_text_with_shadow(screen, h, font, xs[i], 100, WHITE, BLACK, 1)
        pygame.draw.line(screen, GRAY, (30, 125), (WIDTH-30, 125), 2)
        
        for idx, r in enumerate(records[scroll:scroll+8]):
            y = 140 + idx * 35
            color = YELLOW if idx + scroll < 3 else WHITE
            draw_text_with_shadow(screen, f"#{idx+scroll+1}", font, 55, y, color, BLACK, 1)
            draw_text_with_shadow(screen, str(r.score), font, 155, y, color, BLACK, 1)
            draw_text_with_shadow(screen, r.mode, font, 255, y, color, BLACK, 1)
            draw_text_with_shadow(screen, str(r.length), font, 360, y, color, BLACK, 1)
        
        back.draw(screen)
        control = pygame.font.SysFont("arial", 12)
        draw_text_with_shadow(screen, "UP/DOWN: Scroll | ESC: Back", control, WIDTH-180, HEIGHT-30, GRAY, BLACK, 1)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return
                elif ev.key == pygame.K_UP:
                    scroll = max(0, scroll - 1)
                elif ev.key == pygame.K_DOWN:
                    scroll = min(max_scroll, scroll + 1)
            if back.handle(ev):
                return

def game_over(score, mode, length):
    score_board.add(score, mode, length)
    btns = [
        Button(WIDTH//2 - 200, HEIGHT - 90, 170, 45, "Play Again", GREEN, DARK_GRAY, WHITE, 18),
        Button(WIDTH//2 - 90, HEIGHT - 90, 170, 45, "Scores", BLUE, DARK_GRAY, WHITE, 18),
        Button(WIDTH//2 + 20, HEIGHT - 90, 170, 45, "Menu", ORANGE, DARK_GRAY, WHITE, 18),
        Button(WIDTH//2 + 130, HEIGHT - 90, 130, 45, "Quit", RED, DARK_GRAY, WHITE, 18),
    ]
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 48)
        draw_text_with_shadow(screen, "GAME OVER", font, WIDTH//2 - 120, 40, RED, BLACK, 2)
        font = pygame.font.SysFont("arial", 28)
        draw_text_with_shadow(screen, f"Score: {score}", font, WIDTH//2 - 70, 110, YELLOW, BLACK, 2)
        draw_text_with_shadow(screen, f"Mode: {mode}", font, WIDTH//2 - 60, 160, WHITE, BLACK, 2)
        draw_text_with_shadow(screen, f"Length: {length}", font, WIDTH//2 - 70, 210, WHITE, BLACK, 2)
        
        for btn in btns:
            btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for i, btn in enumerate(btns):
                if btn.handle(ev):
                    if i == 0:
                        return "play"
                    elif i == 1:
                        show_scoreboard_screen()
                    elif i == 2:
                        return "menu"
                    elif i == 3:
                        pygame.quit()
                        sys.exit()

# ==================== 速度选择菜单 ====================
def speed_select_menu(mode_name, mode_color):
    selected = 2
    opts = list(SPEED_PRESETS.items())
    w, h = 200, 45
    spacing = 12
    start_x = (WIDTH - w) // 2
    start_y = 150
    back = Button(20, HEIGHT - 60, 100, 40, "Back", GRAY, DARK_GRAY, WHITE, 18)
    confirm = Button(WIDTH//2 - 80, HEIGHT - 60, 160, 45, "Confirm", GREEN, DARK_GRAY, BLACK, 20)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 32)
        title = font.render(f"{mode_name} Mode - Speed", True, mode_color)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        for i, (name, val) in enumerate(opts):
            y = start_y + i * (h + spacing)
            rect = pygame.Rect(start_x, y, w, h)
            if i == selected:
                pygame.draw.rect(screen, mode_color, rect)
                pygame.draw.rect(screen, YELLOW, rect, 3)
                check = pygame.font.SysFont("arial", 20).render("✓", True, YELLOW)
                screen.blit(check, (start_x + w - 25, y + 10))
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect)
                pygame.draw.rect(screen, GRAY, rect, 2)
            fn = pygame.font.SysFont("arial", 18)
            screen.blit(fn.render(name, True, WHITE), (start_x + 15, y + 12))
            screen.blit(fn.render(f"{val}ms", True, LIGHT_GRAY), (start_x + w - 65, y + 12))
        
        back.draw(screen)
        confirm.draw(screen)
        hint = pygame.font.SysFont("arial", 12).render("UP/DOWN: Select | ENTER: Confirm | ESC: Back", True, GRAY)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 35))
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    selected = max(0, selected - 1)
                elif ev.key == pygame.K_DOWN:
                    selected = min(len(opts)-1, selected + 1)
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    return opts[selected][1]
                elif ev.key == pygame.K_ESCAPE:
                    return None
            if confirm.handle(ev):
                return opts[selected][1]
            if back.handle(ev):
                return None

# ==================== Easy模式菜单 ====================
def easy_style_menu():
    selected = 0
    variants = list(EASY_MODE_VARIANTS.items())
    back = Button(20, HEIGHT - 60, 100, 40, "Back", GRAY, DARK_GRAY, WHITE, 18)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 28)
        title = font.render("Easy Mode - Choose Style", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        font = pygame.font.SysFont("arial", 14)
        sub = font.render("Select a style that matches your learning goal", True, YELLOW)
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 60))
        
        w, h = 260, 55
        spacing = 10
        start_x = (WIDTH - w) // 2
        start_y = 100
        visible = 5
        scroll = max(0, min(selected - 2, len(variants) - visible)) if selected > 2 else 0
        
        btns = []
        for i, (key, var) in enumerate(variants[scroll:scroll+visible]):
            y = start_y + i * (h + spacing)
            rect = pygame.Rect(start_x, y, w, h)
            btns.append((rect, key))
            is_sel = (scroll + i) == selected
            color = PURPLE if is_sel else DARK_GRAY
            border = GOLD if is_sel else GRAY
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, border, rect, 2)
            fn = pygame.font.SysFont("arial", 18)
            screen.blit(fn.render(var["name"], True, WHITE), (rect.x + 10, rect.y + 8))
            fn = pygame.font.SysFont("arial", 12)
            screen.blit(fn.render(var["description"][:30], True, LIGHT_GRAY), (rect.x + 10, rect.y + 32))
        
        cur = variants[selected][1]
        detail = pygame.font.SysFont("arial", 13).render(f"Info: {cur['description']}", True, CYAN)
        screen.blit(detail, (WIDTH//2 - detail.get_width()//2, HEIGHT - 90))
        back.draw(screen)
        control = pygame.font.SysFont("arial", 12).render("UP/DOWN: Select | ENTER: Confirm | ESC: Back", True, GRAY)
        screen.blit(control, (WIDTH//2 - control.get_width()//2, HEIGHT - 35))
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return None
                elif ev.key == pygame.K_UP:
                    selected = max(0, selected - 1)
                elif ev.key == pygame.K_DOWN:
                    selected = min(len(variants)-1, selected + 1)
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    return variants[selected][0]
            for rect, key in btns:
                if rect.collidepoint(pygame.mouse.get_pos()) and ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    return key
            if back.handle(ev):
                return None

def easy_subject_menu(variant_key):
    subjects = [
        ("mixed", "Mixed (Random)", None),
        ("ich", "ich", "ich"),
        ("du", "du", "du"),
        ("er", "er/sie/es", "er"),
        ("wir", "wir", "wir"),
        ("ihr", "ihr", "ihr"),
        ("Sie", "Sie", "Sie")
    ]
    selected = 0
    back = Button(20, HEIGHT - 60, 100, 40, "Back", GRAY, DARK_GRAY, WHITE, 18)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 32)
        title = font.render("Easy Mode - Choose Subject", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        w, h = 170, 45
        spacing = 15
        cols = 2
        start_x = (WIDTH - cols * w - (cols-1)*spacing) // 2
        start_y = 120
        
        btns = []
        for i, (key, display, subj) in enumerate(subjects):
            row, col = i // cols, i % cols
            x = start_x + col * (w + spacing)
            y = start_y + row * (h + 10)
            rect = pygame.Rect(x, y, w, h)
            btns.append((rect, key, display, subj))
            color = PURPLE if key == "mixed" else (GOLD if i == selected else SILVER)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, YELLOW if i == selected else WHITE, rect, 2)
            fn = pygame.font.SysFont("arial", 18)
            screen.blit(fn.render(display, True, WHITE), (x + w//2 - fn.size(display)[0]//2, y + h//2 - 9))
        
        var_info = f"Style: {EASY_MODE_VARIANTS[variant_key]['name']}"
        fn = pygame.font.SysFont("arial", 14)
        screen.blit(fn.render(var_info, True, CYAN), (10, HEIGHT - 50))
        
        back.draw(screen)
        control = pygame.font.SysFont("arial", 12).render("ARROWS: Select | ENTER: Confirm | ESC: Back", True, GRAY)
        screen.blit(control, (WIDTH//2 - control.get_width()//2, HEIGHT - 35))
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return None
                elif ev.key == pygame.K_UP:
                    selected = (selected - cols) % len(subjects)
                elif ev.key == pygame.K_DOWN:
                    selected = (selected + cols) % len(subjects)
                elif ev.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(subjects)
                elif ev.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(subjects)
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    key, display, subj = subjects[selected]
                    return (key, display, subj)
            for rect, key, display, subj in btns:
                if rect.collidepoint(pygame.mouse.get_pos()) and ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    return (key, display, subj)
            if back.handle(ev):
                return None

# ==================== Medium/Hard菜单 ====================
def medium_hard_menu(difficulty, color):
    speed = DEFAULT_SPEED
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 42)
        title = font.render(f"{difficulty} Mode", True, color)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        
        font = pygame.font.SysFont("arial", 18)
        if difficulty == "Medium":
            desc = "Single letters | Spell German words | Wrap around"
        else:
            desc = "Single letters | Spell German words | No wrap | Instant death"
        screen.blit(font.render(desc, True, WHITE), (WIDTH//2 - font.size(desc)[0]//2, 160))
        screen.blit(font.render("Speed can be customized!", True, YELLOW), (WIDTH//2 - font.size("Speed can be customized!")[0]//2, 200))
        
        # 显示当前速度
        speed_font = pygame.font.SysFont("arial", 18)
        speed_text = f"Current Speed: {speed}ms"
        draw_text_with_shadow(screen, speed_text, speed_font, WIDTH//2 - speed_font.size(speed_text)[0]//2, 250, CYAN, BLACK, 1)
        
        speed_btn = Button(WIDTH//2 - 130, 300, 260, 50, "CUSTOMIZE SPEED", PURPLE, DARK_GRAY, WHITE, 20)
        start_btn = Button(WIDTH//2 - 130, 370, 120, 50, "START", GREEN, DARK_GRAY, BLACK, 24)
        back_btn = Button(WIDTH//2 + 10, 370, 120, 50, "BACK", GRAY, DARK_GRAY, WHITE, 24)
        
        speed_btn.draw(screen)
        start_btn.draw(screen)
        back_btn.draw(screen)
        
        hint = pygame.font.SysFont("arial", 12).render("Click buttons or press ENTER to start", True, GRAY)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 40))
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return "back", None
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    return "start", speed
            if speed_btn.handle(ev):
                new_speed = speed_select_menu(difficulty, color)
                if new_speed:
                    speed = new_speed
                    # 继续循环，不返回，让界面更新显示新速度
                    continue
            if start_btn.handle(ev):
                return "start", speed
            if back_btn.handle(ev):
                return "back", None

# ==================== 游戏主循环 ====================
def game_loop(config):
    helper = GrammarHelper()
    snake = Snake(config)
    words = WordSystem(config)
    clock = pygame.time.Clock()
    paused = False
    msg_timer = 0
    msg_text = ""
    msg_color = ORANGE
    pause_btn = Button(WIDTH - 55, 10, 45, 35, "||", GRAY, DARK_GRAY, WHITE, 20)
    last_move = 0
    
    while True:
        now = pygame.time.get_ticks()
        if not paused:
            screen.fill(BLACK)
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and pause_btn.rect.collidepoint(ev.pos) and not paused:
                res = pause_menu(snake.score, config.name, len(snake.body), snake.pool, snake.subject, helper)
                if res == "resume":
                    paused = False
                elif res == "menu":
                    return
                continue
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE and not paused:
                    res = pause_menu(snake.score, config.name, len(snake.body), snake.pool, snake.subject, helper)
                    if res == "resume":
                        paused = False
                    elif res == "menu":
                        return
                    continue
                if not paused:
                    if ev.key == pygame.K_UP:
                        snake.change_dir((0, -CELL))
                    elif ev.key == pygame.K_DOWN:
                        snake.change_dir((0, CELL))
                    elif ev.key == pygame.K_LEFT:
                        snake.change_dir((-CELL, 0))
                    elif ev.key == pygame.K_RIGHT:
                        snake.change_dir((CELL, 0))
        
        pause_btn.hovered = pause_btn.rect.collidepoint(pygame.mouse.get_pos())
        
        if not paused:
            if now - last_move >= config.speed:
                last_move = now
                eaten = words.eat(snake.body[0])
                if eaten:
                    snake.collected.append(eaten["char"])
                    if config.word_source == "sentence":
                        snake.pool.append(eaten["char"])
                    words.refill()
                    
                    # 简单模式：8词无标点警告
                    if config.word_source == "sentence" and len(snake.collected) >= 8:
                        if snake.collected[-1] not in SENTENCE_END_PUNCTUATIONS:
                            msg_text = "No punctuation! Sentence cleared (8 words)"
                            msg_color = RED
                            msg_timer = 60
                            snake.collected.clear()
                            snake.pool.clear()
                    
                    completed, add, formed, ftype = words.check_completion(snake.collected)
                    if completed:
                        if ftype == "sentence":
                            ok, fb = helper.check(snake.collected)
                            if ok:
                                snake.score += add
                                snake.grow()
                                helper.add(formed, add)
                                bonus = len(snake.pool) * 5
                                snake.score += bonus
                                msg_text = f"Correct! +{add} +{bonus} bonus!"
                                msg_color = GREEN
                                msg_timer = 80
                            else:
                                msg_text = f"Error: {fb}"
                                msg_color = RED
                                msg_timer = 80
                            snake.collected.clear()
                            snake.pool.clear()
                        else:
                            snake.score += add
                            snake.grow()
                            msg_text = f"Word: {formed} +{add}"
                            msg_color = ORANGE
                            msg_timer = 60
                            snake.collected.clear()
                
                if not snake.move():
                    res = game_over(snake.score, config.name, len(snake.body))
                    if res == "play":
                        game_loop(config)
                        return
                    elif res == "menu":
                        return
            
            snake.draw()
            words.draw()
            draw_pool(snake.pool, config, snake.subject)
            
            font = pygame.font.SysFont("arial", 18)
            draw_text_with_shadow(screen, f"Mode: {config.name}", font, 10, 5, config.color, BLACK, 1)
            draw_text_with_shadow(screen, f"Score: {snake.score}", font, 10, 30, WHITE, BLACK, 1)
            collected_str = "".join(snake.collected)
            if config.word_source == "sentence":
                draw_text_with_shadow(screen, f"Current: {collected_str}", font, 10, 55, WHITE, BLACK, 1)
                draw_text_with_shadow(screen, f"({len(snake.collected)}/8 words - need . ! ?)", pygame.font.SysFont("arial", 12), 10, 78, LIGHT_GRAY, BLACK, 1)
            else:
                draw_text_with_shadow(screen, f"Letters: {collected_str} ({len(snake.collected)})", font, 10, 55, WHITE, BLACK, 1)
            draw_text_with_shadow(screen, f"Length: {len(snake.body)}", font, 10, 95, WHITE, BLACK, 1)
            draw_text_with_shadow(screen, f"Speed: {config.speed}ms", font, WIDTH-110, 5, LIGHT_GRAY, BLACK, 1)
            pause_btn.draw(screen)
            
            if msg_timer > 0:
                mf = pygame.font.SysFont("arial", 16)
                draw_text_with_shadow(screen, msg_text, mf, WIDTH//2 - mf.size(msg_text)[0]//2, HEIGHT//2 - 60, msg_color, BLACK, 1)
                msg_timer -= 1
            
            pygame.display.update()
            clock.tick(60)

# ==================== 主菜单 ====================
def main_menu():
    global sentence_pool
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 36)
        draw_text_with_shadow(screen, "SNAKE GERMAN WORD GAME", font, WIDTH//2 - 180, 40, YELLOW, BLACK, 2)
        font = pygame.font.SysFont("arial", 16)
        draw_text_with_shadow(screen, "Learn German verb conjugation!", font, WIDTH//2 - 120, 85, WHITE, BLACK, 1)
        
        w, h = 160, 55
        spacing = 30
        total = 3 * w + 2 * spacing
        start_x = (WIDTH - total) // 2
        y = 180
        options = [("Easy", GREEN), ("Medium", BLUE), ("Hard", RED)]
        selected = 0
        
        rects = []
        for i, (name, color) in enumerate(options):
            x = start_x + i * (w + spacing)
            rect = pygame.Rect(x, y, w, h)
            rects.append(rect)
            pygame.draw.rect(screen, color if i == selected else DARK_GRAY, rect)
            pygame.draw.rect(screen, YELLOW if i == selected else color, rect, 3)
            fn = pygame.font.SysFont("arial", 26)
            screen.blit(fn.render(name, True, WHITE), (x + w//2 - fn.size(name)[0]//2, y + h//2 - 13))
        
        font = pygame.font.SysFont("arial", 14)
        descs = [
            "Easy: Sentence building | Verb conjugation | Custom speed",
            "Medium: Single letters | Spell words | Custom speed",
            "Hard: Single letters | No wrap | Instant death | Custom speed"
        ]
        for i, desc in enumerate(descs):
            color = YELLOW if i == selected else GRAY
            draw_text_with_shadow(screen, desc, font, WIDTH//2 - 280, 270 + i * 24, color, BLACK, 1)
        
        select_btn = Button(WIDTH//2 - 100, 360, 200, 45, "SELECT", GREEN, DARK_GRAY, BLACK, 22)
        score_btn = Button(WIDTH//2 - 100, 420, 200, 40, "VIEW SCORES", BLUE, DARK_GRAY, WHITE, 18)
        select_btn.draw(screen)
        score_btn.draw(screen)
        draw_text_with_shadow(screen, "LEFT/RIGHT: Select | ENTER: Choose | ESC: Quit", pygame.font.SysFont("arial", 12), WIDTH//2 - 200, HEIGHT - 35, GRAY, BLACK, 1)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT:
                    selected = (selected - 1) % 3
                elif ev.key == pygame.K_RIGHT:
                    selected = (selected + 1) % 3
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    if selected == 0:
                        style = easy_style_menu()
                        if style:
                            subj_res = easy_subject_menu(style)
                            if subj_res:
                                key, display, subject = subj_res
                                speed = speed_select_menu("Easy", GREEN)
                                if speed:
                                    sentence_pool = SentencePool(EASY_MODE_VARIANTS[style])
                                    if key == "mixed":
                                        subj = random.choice(["ich", "du", "er", "wir", "ihr", "Sie"])
                                        config = DifficultyConfig(
                                            name=f"Easy (Mixed - {subj})", speed=speed,
                                            allow_wrap=True, self_collision_fatal=False,
                                            word_source="sentence", base_score_per_word=10,
                                            color=GREEN, subject=subj
                                        )
                                    else:
                                        config = DifficultyConfig(
                                            name=f"Easy ({display})", speed=speed,
                                            allow_wrap=True, self_collision_fatal=False,
                                            word_source="sentence", base_score_per_word=10,
                                            color=GREEN, subject=subject
                                        )
                                    game_loop(config)
                    elif selected == 1:
                        action, speed = medium_hard_menu("Medium", BLUE)
                        if action == "start" and speed:
                            config = DifficultyConfig(
                                name="Medium", speed=speed,
                                allow_wrap=True, self_collision_fatal=False,
                                word_source="alphabet", base_score_per_word=15,
                                color=BLUE, subject=None
                            )
                            game_loop(config)
                    elif selected == 2:
                        action, speed = medium_hard_menu("Hard", RED)
                        if action == "start" and speed:
                            config = DifficultyConfig(
                                name="Hard", speed=speed,
                                allow_wrap=False, self_collision_fatal=True,
                                word_source="alphabet", base_score_per_word=15,
                                color=RED, subject=None
                            )
                            game_loop(config)
                elif ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(ev.pos):
                        selected = i
                if select_btn.handle(ev):
                    if selected == 0:
                        style = easy_style_menu()
                        if style:
                            subj_res = easy_subject_menu(style)
                            if subj_res:
                                key, display, subject = subj_res
                                speed = speed_select_menu("Easy", GREEN)
                                if speed:
                                    sentence_pool = SentencePool(EASY_MODE_VARIANTS[style])
                                    if key == "mixed":
                                        subj = random.choice(["ich", "du", "er", "wir", "ihr", "Sie"])
                                        config = DifficultyConfig(
                                            name=f"Easy (Mixed - {subj})", speed=speed,
                                            allow_wrap=True, self_collision_fatal=False,
                                            word_source="sentence", base_score_per_word=10,
                                            color=GREEN, subject=subj
                                        )
                                    else:
                                        config = DifficultyConfig(
                                            name=f"Easy ({display})", speed=speed,
                                            allow_wrap=True, self_collision_fatal=False,
                                            word_source="sentence", base_score_per_word=10,
                                            color=GREEN, subject=subject
                                        )
                                    game_loop(config)
                    elif selected == 1:
                        action, speed = medium_hard_menu("Medium", BLUE)
                        if action == "start" and speed:
                            config = DifficultyConfig(
                                name="Medium", speed=speed,
                                allow_wrap=True, self_collision_fatal=False,
                                word_source="alphabet", base_score_per_word=15,
                                color=BLUE, subject=None
                            )
                            game_loop(config)
                    elif selected == 2:
                        action, speed = medium_hard_menu("Hard", RED)
                        if action == "start" and speed:
                            config = DifficultyConfig(
                                name="Hard", speed=speed,
                                allow_wrap=False, self_collision_fatal=True,
                                word_source="alphabet", base_score_per_word=15,
                                color=RED, subject=None
                            )
                            game_loop(config)
                if score_btn.handle(ev):
                    show_scoreboard_screen()

# ==================== 入口 ====================
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake German Word Game")
    print("=" * 50)
    print("Snake German Word Game")
    print("Easy: Build sentences with verb conjugation")
    print("Medium/Hard: Spell German words from letters")
    print("All modes have customizable speed")
    print("=" * 50)
    main_menu()