import pygame
import random
import sys
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple
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
GOLD = (255,215,0)
SILVER = (192,192,192)

# ==================== 遊戲基礎參數 ====================
CELL = 25
WIDTH, HEIGHT = 600, 650
TOTAL_FOOD_COUNT = 60  # 增加到60个食物

# ==================== 速度選項 ====================
SPEED_OPTIONS = [
    ("Very Slow", 250),
    ("Slow", 180),
    ("Normal", 150),
    ("Fast", 100),
    ("Very Fast", 70),
    ("Extreme", 50)
]
DEFAULT_SPEED = 150

# 标点符号
END_PUNCTUATIONS = [".", "!", "?"]
ALL_PUNCTUATIONS = [",", ".", "!", "?"]

# ==================== 词库 ====================
VERBS = {
    "sein": {"ich": "bin", "du": "bist", "er/sie/es": "ist", "wir": "sind", "ihr": "seid", "Sie": "sind"},
    "haben": {"ich": "habe", "du": "hast", "er/sie/es": "hat", "wir": "haben", "ihr": "habt", "Sie": "haben"},
    "gehen": {"ich": "gehe", "du": "gehst", "er/sie/es": "geht", "wir": "gehen", "ihr": "geht", "Sie": "gehen"},
    "kommen": {"ich": "komme", "du": "kommst", "er/sie/es": "kommt", "wir": "kommen", "ihr": "kommt", "Sie": "kommen"},
    "machen": {"ich": "mache", "du": "machst", "er/sie/es": "macht", "wir": "machen", "ihr": "macht", "Sie": "machen"},
    "sagen": {"ich": "sage", "du": "sagst", "er/sie/es": "sagt", "wir": "sagen", "ihr": "sagt", "Sie": "sagen"},
    "schlafen": {"ich": "schlafe", "du": "schläfst", "er/sie/es": "schläft", "wir": "schlafen", "ihr": "schlaft", "Sie": "schlafen"},
    "sehen": {"ich": "sehe", "du": "siehst", "er/sie/es": "sieht", "wir": "sehen", "ihr": "seht", "Sie": "sehen"},
}

NOUNS = {
    "der": ["Mann", "Tisch", "Hund", "Tag", "Baum", "Computer", "Himmel"],
    "die": ["Frau", "Katze", "Blume", "Tür", "Straße", "Lampe", "Sonne"],
    "das": ["Kind", "Haus", "Auto", "Buch", "Fenster", "Bier", "Brot"]
}

ADJECTIVES = ["gut", "schlecht", "groß", "klein", "neu", "alt", "schön", "schnell", "langsam"]
CONJUNCTIONS = ["und", "aber", "denn", "oder", "weil", "dass"]
PREPOSITIONS = ["in", "auf", "an", "zu", "mit", "nach", "aus", "bei", "unter", "über", "neben"]
ADVERBS = ["heute", "gerne", "oft", "immer", "nie", "dort", "hier", "morgen", "jetzt"]
HELPERS = ["Heute", "Jetzt", "Dann", "Morgen", "Vielleicht", "Gestern"]

SUBJECTS = ["ich", "du", "er", "sie", "es", "wir", "ihr", "Sie"]

LETTERS = list("abcdefghijklmnopqrstuvwxyzäöüß")

# ==================== A1-B1 级别德语词汇库（用于单词拼写检查） ====================
A1_B1_WORD_LIST = {
    # 常用动词
    "sein", "haben", "werden", "können", "müssen", "wollen", "dürfen", "sollen",
    "gehen", "kommen", "sehen", "essen", "trinken", "schlafen", "arbeiten", "lernen",
    "sprechen", "schreiben", "lesen", "hören", "spielen", "machen", "sagen", "helfen",
    "finden", "geben", "nehmen", "verstehen", "kaufen", "verkaufen", "wohnen", "reisen",
    
    # 变位形式
    "bin", "bist", "ist", "sind", "seid", "habe", "hast", "hat", "haben", "habt",
    "gehe", "gehst", "geht", "gehen", "komme", "kommst", "kommt", "kommen",
    "sehe", "siehst", "sieht", "sehen", "seht", "schlafe", "schläfst", "schläft",
    "mache", "machst", "macht", "machen", "sage", "sagst", "sagt", "sagen",
    
    # 名词（常见）
    "mann", "frau", "kind", "haus", "auto", "hund", "katze", "tisch", "stuhl", "tür",
    "fenster", "brot", "wasser", "kaffee", "bier", "apfel", "arbeit", "schule", "universität",
    "stadt", "land", "straße", "platz", "park", "garten", "baum", "blume", "himmel", "sonne",
    "mond", "stern", "tag", "nacht", "woche", "monat", "jahr", "uhr", "zeit",
    
    # 形容词
    "gut", "schlecht", "groß", "klein", "neu", "alt", "jung", "schnell", "langsam",
    "schön", "hässlich", "teuer", "billig", "reich", "arm", "glücklich", "traurig",
    "müde", "wach", "krank", "gesund", "heiß", "kalt", "warm", "kühl",
    
    # 副词
    "heute", "morgen", "gestern", "jetzt", "später", "früh", "oft", "immer", "nie",
    "manchmal", "gern", "sehr", "zu", "auch", "nur", "schon", "noch",
    
    # 代词
    "ich", "du", "er", "sie", "es", "wir", "ihr", "Sie", "mir", "dir", "ihm", "ihr",
    
    # 冠词/限定词
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem", "einer", "eines",
    
    # 介词
    "in", "auf", "an", "zu", "mit", "nach", "aus", "bei", "von", "für", "durch", "um", "gegen",
    
    # 连词
    "und", "aber", "denn", "oder", "weil", "dass", "wenn", "dann", "als", "wie",
    
    # 数字
    "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn",
    "elf", "zwölf", "zwanzig", "dreißig", "vierzig", "fünfzig", "hundert", "tausend",
    
    # 疑问词
    "wer", "was", "wo", "woher", "wohin", "wann", "warum", "wie", "welcher",
    
    # 其他常用词
    "bitte", "danke", "ja", "nein", "vielleicht", "natürlich", "leider", "gern", "bald"
}

# ==================== 单词检查器 ====================
class GermanWordChecker:
    """A1-B1级别德语单词拼写检查器"""
    
    def __init__(self):
        self.word_list = A1_B1_WORD_LIST
        self.valid_words = self.word_list
        self.stats = {"checked": 0, "valid": 0, "invalid": 0}
    
    def check_word(self, word: str) -> Tuple[bool, str]:
        word_lower = word.lower().strip()
        self.stats["checked"] += 1
        
        if word_lower in self.valid_words:
            self.stats["valid"] += 1
            return True, word_lower
        else:
            suggestion = self._find_suggestion(word_lower)
            self.stats["invalid"] += 1
            return False, suggestion
    
    def _find_suggestion(self, word: str) -> str:
        best_match = None
        best_score = 0
        
        for valid_word in self.valid_words:
            score = self._similarity_score(word, valid_word)
            if score > best_score and score > 0.6:
                best_score = score
                best_match = valid_word
        
        return best_match if best_match else ""
    
    def _similarity_score(self, word1: str, word2: str) -> float:
        if len(word1) == 0 or len(word2) == 0:
            return 0
        
        common_prefix = 0
        for i in range(min(len(word1), len(word2))):
            if word1[i] == word2[i]:
                common_prefix += 1
            else:
                break
        
        length_diff = abs(len(word1) - len(word2))
        score = (common_prefix / max(len(word1), len(word2))) * (1 - length_diff / max(len(word1), len(word2)))
        
        return score
    
    def get_stats(self):
        return self.stats
    
    def is_valid_word(self, word: str) -> bool:
        return word.lower() in self.valid_words


# 创建全局单词检查器
word_checker = GermanWordChecker()

# ==================== 德語句子語法檢查器 ====================
class GermanSentenceChecker:
    """German sentence grammar checker - validates collected sentence fragments"""
    
    def __init__(self):
        self.valid_patterns = [
            ["subject", "verb"],
            ["subject", "verb", "noun"],
            ["subject", "verb", "preposition"],
            ["subject", "verb", "adjective"],
            ["subject", "verb", "adverb"],
            ["subject", "verb", "determiner", "noun"],
            ["noun", "verb"],
            ["noun", "verb", "noun"],
            ["noun", "verb", "preposition"],
            ["pronoun", "verb"],
            ["pronoun", "verb", "noun"],
        ]
        self.requires_v2 = True
        self.debug_mode = False
        
        # 词类词典
        self.subjects = {"ich", "du", "er", "sie", "es", "wir", "ihr", "Sie"}
        self.pronouns = {"ich", "du", "er", "sie", "es", "wir", "ihr", "Sie", "mir", "dir", "ihm", "ihr"}
        
        # 动词及其变位形式
        self.verbs = set()
        for verb_conj in VERBS.values():
            for form in verb_conj.values():
                self.verbs.add(form.lower())
        
        self.prepositions = set(PREPOSITIONS)
        self.adjectives = set(ADJECTIVES)
        self.adverbs = set(ADVERBS)
        self.determiners = {"der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem", "einer"}
        
        # 主语-动词匹配规则
        self.subject_verb_map = {
            "ich": ["e", "bin", "habe"],
            "du": ["st", "bist", "hast"],
            "er": ["t", "ist", "hat"],
            "sie": ["t", "ist", "hat"],
            "es": ["t", "ist", "hat"],
            "wir": ["en", "sind", "haben"],
            "ihr": ["t", "seid", "habt"],
            "Sie": ["en", "sind", "haben"],
        }
    
    def enable_debug(self):
        self.debug_mode = True
    
    def _get_word_type(self, word: str) -> str:
        word_lower = word.lower()
        
        if word_lower in self.subjects:
            return "subject"
        elif word_lower in self.pronouns:
            return "pronoun"
        elif word_lower in self.verbs:
            return "verb"
        elif word_lower in self.prepositions:
            return "preposition"
        elif word_lower in self.adjectives:
            return "adjective"
        elif word_lower in self.adverbs:
            return "adverb"
        elif word_lower in self.determiners:
            return "determiner"
        else:
            if word and word[0].isupper() and len(word) > 1:
                return "noun"
            return "unknown"
    
    def check_sentence(self, fragments: List[str], subject_hint: str = None) -> Tuple[bool, str, List[str]]:
        issues = []
        
        if not fragments:
            return False, "No words collected yet", ["句子为空，请至少收集2-3个单词"]
        
        if self.debug_mode:
            print(f"[CHECKER] Checking: {' → '.join(fragments)}")
        
        # 1. 检查句末标点
        if fragments[-1] not in END_PUNCTUATIONS:
            issues.append("❌ 句子应以句号(.)、感叹号(!)或问号(?)结尾")
        
        # 2. 识别每个单词的词性
        tagged = [(word, self._get_word_type(word)) for word in fragments]
        
        # 3. 检查最小长度
        if len(tagged) < 2:
            issues.append("❌ 德语句子至少需要主语和动词")
            return False, "句子太短", issues
        
        # 4. 检查是否有动词
        has_verb = any(tag == "verb" for _, tag in tagged)
        if not has_verb:
            issues.append("❌ 每个德语句子都需要一个动词！")
        
        # 5. 检查是否有主语或名词
        has_subject = any(tag in ["subject", "pronoun", "noun"] for _, tag in tagged)
        if not has_subject:
            issues.append("❌ 缺少主语（谁或什么在执行动作？）")
        
        # 6. 检查动词位置
        if self.requires_v2:
            verb_positions = [i for i, (_, tag) in enumerate(tagged) if tag == "verb"]
            if verb_positions:
                first_verb_pos = verb_positions[0]
                if first_verb_pos != 1:
                    issues.append(f"❌ 动词应在第二位（当前在第{first_verb_pos + 1}位）")
            else:
                issues.append("❌ 未找到动词")
        
        # 7. 检查句子开头
        first_word, first_tag = tagged[0]
        if first_tag not in ["subject", "pronoun", "noun", "determiner"]:
            issues.append(f"❌ 句子应以主语或名词开头（'{first_word}' 不是合适的主语）")
        
        # 8. 检查主语-动词一致性
        if has_verb and has_subject:
            subject_word = None
            verb_word = None
            
            for word, tag in tagged:
                if tag in ["subject", "pronoun"] and not subject_word:
                    subject_word = word.lower()
                if tag == "verb" and not verb_word:
                    verb_word = word.lower()
            
            if subject_word and verb_word:
                agreement_ok = self._check_subject_verb_agreement(subject_word, verb_word)
                if not agreement_ok:
                    issues.append(f"❌ 主语 '{subject_word}' 与动词 '{verb_word}' 不匹配")
        
        # 9. 检查句首大写
        first_char = fragments[0][0] if fragments[0] else ''
        if first_char.islower() and fragments[0].lower() not in self.subjects:
            issues.append(f"❌ 句子首单词 '{fragments[0]}' 的首字母应大写")
        
        # 10. 生成总结消息
        if issues:
            critical_issues = [i for i in issues if not i.startswith("💡")]
            if critical_issues:
                main_msg = critical_issues[0]
            else:
                main_msg = "句子有改进空间"
            return False, main_msg, issues
        else:
            return True, "✅ 句子结构正确！", []
    
    def _check_subject_verb_agreement(self, subject: str, verb: str) -> bool:
        if subject not in self.subject_verb_map:
            return True
        
        expected_endings = self.subject_verb_map[subject]
        
        for ending in expected_endings:
            if verb.endswith(ending) or verb == ending:
                return True
        
        return False
    
    def get_grammar_tips(self) -> List[str]:
        return [
            "📖 德语主句结构：主语 + 动词 + 其他成分",
            "📖 动词必须在第二位！",
            "📖 名词首字母永远大写",
            "📖 句子以句号/感叹号/问号结尾",
            "📖 'ich' 需要动词以 -e 结尾",
            "📖 'du' 需要动词以 -st 结尾",
            "📖 'er/sie/es' 需要动词以 -t 结尾",
            "📖 'wir/Sie' 需要动词以 -en 结尾",
            "📖 'ihr' 需要动词以 -t 结尾",
        ]


# 创建全局语法检查器
grammar_checker = GermanSentenceChecker()

# ==================== A1-B1 级别字母权重随机发生器 ====================
class A1B1LetterGenerator:
    """A1-B1级别德语字母权重随机发生器（区分大小写）"""
    
    def __init__(self):
        self.letter_weights = {
            'e': 16.2, 'n': 9.3, 'i': 7.2, 's': 5.4, 'r': 6.3,
            'a': 5.7, 't': 5.8, 'd': 4.3, 'h': 4.5, 'u': 4.0,
            'l': 3.1, 'c': 2.4, 'g': 2.5, 'm': 2.1, 'o': 2.2,
            'f': 1.5, 'w': 1.5, 'b': 1.4, 'k': 1.0, 'z': 0.9,
            'p': 0.6, 'v': 0.5, 'ü': 0.55, 'ä': 0.50, 'ö': 0.40,
            'j': 0.25, 'ß': 0.25, 'x': 0.03, 'y': 0.03, 'q': 0.02,
            'S': 2.1, 'E': 1.1, 'A': 1.0, 'D': 0.8, 'N': 0.7,
            'R': 0.5, 'T': 0.5, 'I': 0.4, 'C': 0.4, 'M': 0.4,
            'H': 0.3, 'G': 0.3, 'B': 0.3, 'U': 0.2, 'L': 0.2,
            'O': 0.2, 'F': 0.2, 'W': 0.2, 'V': 0.2, 'K': 0.1,
            'Z': 0.1, 'P': 0.1, 'J': 0.05, 'Ü': 0.05, 'Ä': 0.05,
            'Ö': 0.05, 'X': 0.02, 'Y': 0.02, 'Q': 0.01,
        }
        
        self.letters = list(self.letter_weights.keys())
        self.weights = list(self.letter_weights.values())
        self.stats = {letter: 0 for letter in self.letters}
        self.total_generated = 0
    
    def sample_letter(self) -> str:
        letter = random.choices(self.letters, weights=self.weights)[0]
        self.stats[letter] += 1
        self.total_generated += 1
        return letter


class WeightedLetterPool:
    def __init__(self):
        self.generator = A1B1LetterGenerator()
        self.buffer = []
        self.buffer_size = 200
        self._refill_buffer()
    
    def _refill_buffer(self):
        while len(self.buffer) < self.buffer_size:
            self.buffer.append(self.generator.sample_letter())
    
    def get_letter(self) -> str:
        if not self.buffer:
            self._refill_buffer()
        letter = self.buffer.pop()
        self._refill_buffer()
        return letter
    
    def get_letters(self, count: int) -> list:
        return [self.get_letter() for _ in range(count)]


# ==================== 权重随机发生器（词类） ====================
class WeightedPOSGenerator:
    def __init__(self):
        self.pos_weights = {
            'verb': 19, 'noun': 19, 'adj_adv': 11, 'prep': 9,
            'conj': 8, 'det': 8, 'pronoun': 9, 'num': 4.5, 'punct': 13.5,
        }
        self.punct_weights = {'.': 50, ',': 35, '?': 9, '!': 4}
        
        self.pos_list = list(self.pos_weights.keys())
        self.pos_weight_values = list(self.pos_weights.values())
        self.punct_list = list(self.punct_weights.keys())
        self.punct_weight_values = list(self.punct_weights.values())
    
    def sample_pos(self):
        return random.choices(self.pos_list, weights=self.pos_weight_values)[0]
    
    def sample_punctuation(self):
        return random.choices(self.punct_list, weights=self.punct_weight_values)[0]
    
    def generate_word(self, pos_type, subject=None):
        if pos_type == 'verb':
            verbs = list(VERBS.keys())
            return {"word": random.choice(verbs), "type": "verb", "needs_conjugation": True, "display_type": "动词"}
        elif pos_type == 'noun':
            art = random.choice(list(NOUNS.keys()))
            noun = random.choice(NOUNS[art])
            return {"word": f"{art} {noun}", "type": "noun", "needs_conjugation": False, "display_type": "名词"}
        elif pos_type == 'adj_adv':
            word = random.choice(ADJECTIVES + ADVERBS)
            return {"word": word, "type": "adj_adv", "needs_conjugation": False, "display_type": "形容词/副词"}
        elif pos_type == 'prep':
            word = random.choice(PREPOSITIONS)
            return {"word": word, "type": "prep", "needs_conjugation": False, "display_type": "介词"}
        elif pos_type == 'conj':
            word = random.choice(CONJUNCTIONS)
            return {"word": word, "type": "conj", "needs_conjugation": False, "display_type": "连词"}
        elif pos_type == 'det':
            art = random.choice(list(NOUNS.keys()))
            return {"word": art, "type": "det", "needs_conjugation": False, "display_type": "冠词"}
        elif pos_type == 'pronoun':
            word = random.choice(SUBJECTS)
            return {"word": word, "type": "pronoun", "needs_conjugation": False, "display_type": "代词"}
        elif pos_type == 'num':
            numbers = ["eins", "zwei", "drei", "vier", "fünf", "zehn", "hundert", "tausend"]
            return {"word": random.choice(numbers), "type": "num", "needs_conjugation": False, "display_type": "数词"}
        elif pos_type == 'punct':
            punct = self.sample_punctuation()
            return {"word": punct, "type": "punct", "needs_conjugation": False, "display_type": "标点"}
        else:
            return {"word": random.choice(list(A1_B1_WORD_LIST)), "type": "default", "needs_conjugation": False, "display_type": "其他"}
    
    def get_weighted_fragment(self, subject=None):
        pos_type = self.sample_pos()
        fragment = self.generate_word(pos_type, subject)
        if fragment["needs_conjugation"] and subject and fragment["type"] == "verb":
            verb_base = fragment["word"]
            if verb_base in VERBS and subject in VERBS[verb_base]:
                fragment["word"] = VERBS[verb_base][subject]
        return fragment


# ==================== 渲染函数 ====================
def draw_shadow_text(surface, text, font, x, y, color=WHITE, shadow=BLACK):
    shadow_surf = font.render(text, True, shadow)
    text_surf = font.render(text, True, color)
    surface.blit(shadow_surf, (x+1, y+1))
    surface.blit(text_surf, (x, y))


# ==================== 按钮类 ====================
class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, text_color=WHITE, size=20):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("arial", size)
        self.hovered = False
    
    def draw(self, surf):
        col = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surf, col, self.rect)
        pygame.draw.rect(surf, WHITE, self.rect, 2)
        tw = self.font.size(self.text)[0]
        th = self.font.get_height()
        draw_shadow_text(surf, self.text, self.font, 
                        self.rect.x + (self.rect.w - tw)//2,
                        self.rect.y + (self.rect.h - th)//2,
                        self.text_color)
    
    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)
    
    def clicked(self, pos):
        return self.rect.collidepoint(pos)


# ==================== 难度配置 ====================
@dataclass
class Config:
    name: str
    speed: int
    allow_wrap: bool
    fatal_self: bool
    word_source: str
    score_per_word: int
    color: Tuple
    subject: str = None


# ==================== 句子池 ====================
class SentencePool:
    def __init__(self, variant="standard"):
        self.generator = WeightedPOSGenerator()
    
    def get(self, subject=None):
        return self.generator.get_weighted_fragment(subject)


# ==================== 分数系统 ====================
class ScoreBoard:
    def __init__(self):
        self.records = []
        self.load()
    
    def load(self):
        try:
            with open("scores.txt", "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        self.records.append((int(parts[0]), parts[1], parts[2], int(parts[3])))
        except:
            pass
        self.records.sort(key=lambda x: x[0], reverse=True)
    
    def save(self):
        with open("scores.txt", "w") as f:
            for r in self.records[:10]:
                f.write(f"{r[0]}|{r[1]}|{r[2]}|{r[3]}\n")
    
    def add(self, score, mode, length):
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.records.append((score, mode, date, length))
        self.records.sort(key=lambda x: x[0], reverse=True)
        self.records = self.records[:10]
        self.save()
    
    def get_top(self):
        return self.records


score_board = ScoreBoard()
screen = None


# ==================== A1-B1 字母系统 ====================
class A1B1LetterSystem:
    def __init__(self, config):
        self.config = config
        self.letter_pool = WeightedLetterPool()
        self.items = []
        self.target = TOTAL_FOOD_COUNT
        self.spawn()
    
    def _random_pos(self):
        return (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT-150, CELL))
    
    def _get_available_positions(self, snake_body):
        occupied = set(snake_body)
        available = []
        for x in range(0, WIDTH, CELL):
            for y in range(0, HEIGHT-150, CELL):
                if (x, y) not in occupied:
                    available.append((x, y))
        return available
    
    def spawn(self):
        self.items = []
        used = set()
        for _ in range(self.target):
            pos = self._random_pos()
            while pos in used:
                pos = self._random_pos()
            used.add(pos)
            letter = self.letter_pool.get_letter()
            self.items.append({"pos": pos, "char": letter, "type": "letter", "display_type": "字母"})
    
    def add_one_food(self, snake_body):
        occupied = set(snake_body)
        for item in self.items:
            occupied.add(item["pos"])
        available = self._get_available_positions(snake_body)
        available = [pos for pos in available if pos not in occupied]
        if not available:
            return False
        new_pos = random.choice(available)
        letter = self.letter_pool.get_letter()
        self.items.append({"pos": new_pos, "char": letter, "type": "letter", "display_type": "字母"})
        return True
    
    def eat(self, head, snake_body):
        for i, item in enumerate(self.items):
            if item["pos"] == head:
                eaten = self.items.pop(i)
                self.add_one_food(snake_body)
                return eaten
        return None
    
    def draw(self):
        for item in self.items:
            x, y = item["pos"]
            char = item["char"]
            if char.isupper():
                color = GOLD
            elif char in ['ä', 'ö', 'ü', 'ß']:
                color = CYAN
            else:
                color = BLUE
            pygame.draw.circle(screen, color, (x+CELL//2, y+CELL//2), CELL//2)
            font = pygame.font.SysFont("arial", 18)
            draw_shadow_text(screen, char, font, x+7, y+5)
    
    def get_food_count(self):
        return len(self.items)


# ==================== 单词系统 ====================
class WordSystem:
    def __init__(self, config):
        self.config = config
        self.target = TOTAL_FOOD_COUNT
        
        if config.word_source == "sentence":
            self.pool = SentencePool()
            self.use_a1b1 = False
            self.items = []
            self.spawn()
        else:
            self.use_a1b1 = True
            self.a1b1_system = A1B1LetterSystem(config)
            self.items = self.a1b1_system.items
    
    def _random_pos(self):
        return (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT-150, CELL))
    
    def _get_available_positions(self, snake_body):
        occupied = set(snake_body)
        available = []
        for x in range(0, WIDTH, CELL):
            for y in range(0, HEIGHT-150, CELL):
                if (x, y) not in occupied:
                    available.append((x, y))
        return available
    
    def spawn(self):
        self.items = []
        used = set()
        for _ in range(self.target):
            pos = self._random_pos()
            while pos in used:
                pos = self._random_pos()
            used.add(pos)
            f = self.pool.get(self.config.subject)
            self.items.append({
                "pos": pos, "char": f["word"], "type": f["type"], 
                "display_type": f.get("display_type", f["type"])
            })
    
    def add_one_food_sentence(self, snake_body):
        occupied = set(snake_body)
        for item in self.items:
            occupied.add(item["pos"])
        available = self._get_available_positions(snake_body)
        available = [pos for pos in available if pos not in occupied]
        if not available:
            return False
        new_pos = random.choice(available)
        f = self.pool.get(self.config.subject)
        self.items.append({
            "pos": new_pos, "char": f["word"], "type": f["type"],
            "display_type": f.get("display_type", f["type"])
        })
        return True
    
    def eat(self, head, snake_body):
        if self.use_a1b1:
            return self.a1b1_system.eat(head, snake_body)
        else:
            for i, item in enumerate(self.items):
                if item["pos"] == head:
                    eaten = self.items.pop(i)
                    self.add_one_food_sentence(snake_body)
                    return eaten
            return None
    
    def draw(self):
        if self.use_a1b1:
            self.a1b1_system.draw()
        else:
            for item in self.items:
                x, y = item["pos"]
                t = item["type"]
                if t == "pronoun":
                    pygame.draw.rect(screen, CYAN, (x, y, CELL-1, CELL-1))
                elif t == "verb":
                    pygame.draw.rect(screen, YELLOW, (x, y, CELL-1, CELL-1))
                elif t == "noun":
                    pygame.draw.rect(screen, ORANGE, (x, y, CELL-1, CELL-1))
                elif t == "punct":
                    pygame.draw.rect(screen, PURPLE, (x, y, CELL-1, CELL-1))
                elif t == "adj_adv":
                    pygame.draw.rect(screen, PINK, (x, y, CELL-1, CELL-1))
                elif t == "prep":
                    pygame.draw.rect(screen, GOLD, (x, y, CELL-1, CELL-1))
                elif t == "conj":
                    pygame.draw.rect(screen, SILVER, (x, y, CELL-1, CELL-1))
                elif t == "det":
                    pygame.draw.rect(screen, (100, 200, 100), (x, y, CELL-1, CELL-1))
                elif t == "num":
                    pygame.draw.rect(screen, (200, 100, 200), (x, y, CELL-1, CELL-1))
                else:
                    pygame.draw.rect(screen, GREEN, (x, y, CELL-1, CELL-1))
                font = pygame.font.SysFont("arial", 14)
                display_char = item["char"][:8] if len(item["char"]) > 8 else item["char"]
                draw_shadow_text(screen, display_char, font, x+3, y+5)
    
    def get_food_count(self):
        return len(self.items)
    
    def check_word(self, collected_letters: List[str]) -> Tuple[bool, int, str]:
        word = "".join(collected_letters).lower()
        
        if len(word) < 2:
            return False, 0, ""
        
        is_valid, suggestion = word_checker.check_word(word)
        
        if is_valid:
            score = len(word) * self.config.score_per_word
            return True, score, word
        else:
            return False, 0, suggestion


# ==================== 蛇类 ====================
class Snake:
    def __init__(self, config):
        self.config = config
        self.body = [(WIDTH//2, HEIGHT//2 - 50)]
        self.dir = (CELL, 0)
        self.next_dir = (CELL, 0)
        self.collected = []
        self.pool_words = []
        self.score = 0
        self.alive = True
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
            if self.config.fatal_self:
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
        if (d[0]*-1, d[1]*-1) != self.dir:
            self.next_dir = d
    
    def draw(self):
        for i, pos in enumerate(self.body):
            x, y = pos
            if i == 0:
                pygame.draw.rect(screen, self.config.color, (x, y, CELL-1, CELL-1))
                eye_offset = CELL // 4
                eye_radius = 3
                if self.dir == (CELL, 0):
                    pygame.draw.circle(screen, WHITE, (x + CELL - 6, y + eye_offset), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + CELL - 6, y + CELL - eye_offset), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + CELL - 5, y + eye_offset), 1)
                    pygame.draw.circle(screen, BLACK, (x + CELL - 5, y + CELL - eye_offset), 1)
                elif self.dir == (-CELL, 0):
                    pygame.draw.circle(screen, WHITE, (x + 6, y + eye_offset), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + 6, y + CELL - eye_offset), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + 5, y + eye_offset), 1)
                    pygame.draw.circle(screen, BLACK, (x + 5, y + CELL - eye_offset), 1)
                elif self.dir == (0, CELL):
                    pygame.draw.circle(screen, WHITE, (x + eye_offset, y + CELL - 6), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + CELL - eye_offset, y + CELL - 6), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + eye_offset, y + CELL - 5), 1)
                    pygame.draw.circle(screen, BLACK, (x + CELL - eye_offset, y + CELL - 5), 1)
                elif self.dir == (0, -CELL):
                    pygame.draw.circle(screen, WHITE, (x + eye_offset, y + 6), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + CELL - eye_offset, y + 6), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + eye_offset, y + 5), 1)
                    pygame.draw.circle(screen, BLACK, (x + CELL - eye_offset, y + 5), 1)
                else:
                    pygame.draw.circle(screen, WHITE, (x + CELL - 6, y + eye_offset), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + CELL - 6, y + CELL - eye_offset), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + CELL - 5, y + eye_offset), 1)
                    pygame.draw.circle(screen, BLACK, (x + CELL - 5, y + CELL - eye_offset), 1)
            else:
                pygame.draw.rect(screen, GREEN, (x, y, CELL-1, CELL-1))


# ==================== Grammar Helper 面板 ====================
def show_grammar_panel(sentence: List[str], subject: str):
    """显示语法检查面板"""
    w, h = 550, 480
    x, y = (WIDTH - w) // 2, (HEIGHT - h) // 2
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    pygame.draw.rect(screen, DARK_GRAY, (x, y, w, h))
    pygame.draw.rect(screen, GOLD, (x, y, w, h), 3)
    
    font_title = pygame.font.SysFont("arial", 24)
    draw_shadow_text(screen, "Grammar Helper", font_title, x + w//2 - 70, y + 15, YELLOW)
    
    font = pygame.font.SysFont("arial", 16)
    current_text = subject + " → " + " → ".join(sentence) if sentence else "(empty)"
    if len(current_text) > 50:
        current_text = current_text[:47] + "..."
    draw_shadow_text(screen, "Current Sentence:", font, x + 15, y + 55, CYAN)
    draw_shadow_text(screen, current_text, pygame.font.SysFont("arial", 14), x + 15, y + 80, WHITE)
    
    is_valid, main_msg, issues = grammar_checker.check_sentence(sentence, subject)
    
    result_color = GREEN if is_valid else RED
    draw_shadow_text(screen, "Grammar Check Result:", font, x + 15, y + 120, result_color)
    draw_shadow_text(screen, main_msg, pygame.font.SysFont("arial", 14), x + 15, y + 145, result_color)
    
    if issues:
        draw_shadow_text(screen, "Details:", font, x + 15, y + 175, ORANGE)
        for i, issue in enumerate(issues[:6]):
            draw_shadow_text(screen, issue, pygame.font.SysFont("arial", 12), 
                           x + 20, y + 200 + i * 22, LIGHT_GRAY)
    
    tips_y = y + 350
    draw_shadow_text(screen, "💡 Grammar Tips:", font, x + 15, tips_y, CYAN)
    tips = grammar_checker.get_grammar_tips()[:5]
    for i, tip in enumerate(tips):
        draw_shadow_text(screen, tip, pygame.font.SysFont("arial", 11), 
                       x + 20, tips_y + 25 + i * 18, LIGHT_GRAY)
    
    close_btn = Button(x + w - 80, y + h - 45, 65, 30, "Close", RED, DARK_GRAY, WHITE, 16)
    close_btn.draw(screen)
    
    pygame.display.update()
    
    while True:
        mx, my = pygame.mouse.get_pos()
        close_btn.update((mx, my))
        close_btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if close_btn.clicked((mx, my)):
                    return


# ==================== 单词检查面板 ====================
def show_word_check_panel(word: str, suggestion: str):
    """显示单词检查结果面板（Medium/Hard模式）"""
    w, h = 400, 250
    x, y = (WIDTH - w) // 2, (HEIGHT - h) // 2
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    pygame.draw.rect(screen, DARK_GRAY, (x, y, w, h))
    pygame.draw.rect(screen, GOLD, (x, y, w, h), 3)
    
    font_title = pygame.font.SysFont("arial", 24)
    draw_shadow_text(screen, "Word Check", font_title, x + w//2 - 55, y + 15, YELLOW)
    
    font = pygame.font.SysFont("arial", 18)
    draw_shadow_text(screen, f"Your word: '{word}'", font, x + 20, y + 65, CYAN)
    
    if suggestion:
        draw_shadow_text(screen, f"Did you mean: '{suggestion}'?", 
                       pygame.font.SysFont("arial", 16), x + 20, y + 105, ORANGE)
        draw_shadow_text(screen, "Tip: Try to spell valid A1-B1 German words!", 
                       pygame.font.SysFont("arial", 12), x + 20, y + 145, LIGHT_GRAY)
    else:
        draw_shadow_text(screen, "Not a valid A1-B1 German word!", 
                       pygame.font.SysFont("arial", 16), x + 20, y + 105, RED)
        draw_shadow_text(screen, "Try shorter or more common words", 
                       pygame.font.SysFont("arial", 12), x + 20, y + 145, LIGHT_GRAY)
    
    close_btn = Button(x + w - 80, y + h - 45, 65, 30, "Close", RED, DARK_GRAY, WHITE, 16)
    close_btn.draw(screen)
    
    pygame.display.update()
    
    while True:
        mx, my = pygame.mouse.get_pos()
        close_btn.update((mx, my))
        close_btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if close_btn.clicked((mx, my)):
                    return
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                return


# ==================== UI函数 ====================
def draw_game_ui(snake, config, food_count, words_system):
    font = pygame.font.SysFont("arial", 18)
    draw_shadow_text(screen, f"Mode: {config.name}", font, 10, 5, config.color)
    draw_shadow_text(screen, f"Score: {snake.score}", font, 10, 30)
    draw_shadow_text(screen, f"Length: {len(snake.body)}", font, 10, 55)
    draw_shadow_text(screen, f"Food: {food_count}/{TOTAL_FOOD_COUNT}", font, 10, 80, CYAN)
    draw_shadow_text(screen, f"Speed: {config.speed}ms", font, WIDTH-110, 5, LIGHT_GRAY)
    
    collected = "".join(snake.collected)
    
    if config.word_source == "sentence":
        draw_shadow_text(screen, f"Current: {collected[:25]}", font, 10, 105)
        draw_shadow_text(screen, f"({len(snake.collected)} words - need . ! ?)", 
                        pygame.font.SysFont("arial", 12), 10, 128, LIGHT_GRAY)
        
        if len(snake.collected) >= 2:
            is_valid, msg, _ = grammar_checker.check_sentence(snake.collected, snake.subject)
            if not is_valid:
                draw_shadow_text(screen, msg[:35], pygame.font.SysFont("arial", 11), 10, 148, RED)
        
        y = HEIGHT - 120
        pygame.draw.rect(screen, DARK_GRAY, (0, y, WIDTH, 120))
        pygame.draw.rect(screen, WHITE, (0, y, WIDTH, 120), 2)
        draw_shadow_text(screen, f"Subject: {snake.subject.upper()}", pygame.font.SysFont("arial", 16), 10, y+5, YELLOW)
        if snake.pool_words:
            text = snake.subject + " → " + " → ".join(snake.pool_words[-8:])
            if len(text) > 45:
                text = text[:42] + "..."
            draw_shadow_text(screen, text, pygame.font.SysFont("arial", 14), 10, y+35)
    else:
        draw_shadow_text(screen, f"Letters: {collected} ({len(snake.collected)})", font, 10, 105)
        draw_shadow_text(screen, "A1-B1 Letter Distribution", pygame.font.SysFont("arial", 10), 10, 128, LIGHT_GRAY)
        
        if len(snake.collected) >= 2:
            word = "".join(snake.collected).lower()
            if word_checker.is_valid_word(word):
                draw_shadow_text(screen, f"✓ '{word}' is a valid German word! (Press SPACE to confirm)", 
                               pygame.font.SysFont("arial", 11), 10, 148, GREEN)
            elif len(word) >= 3:
                draw_shadow_text(screen, f"Current: '{word}'", 
                               pygame.font.SysFont("arial", 11), 10, 148, LIGHT_GRAY)
                suggestion = word_checker._find_suggestion(word)
                if suggestion:
                    draw_shadow_text(screen, f"Did you mean: '{suggestion}'?", 
                                   pygame.font.SysFont("arial", 10), 10, 168, ORANGE)
        else:
            draw_shadow_text(screen, "Collect 2+ letters to form German words!", 
                           pygame.font.SysFont("arial", 10), 10, 148, LIGHT_GRAY)
        
        draw_shadow_text(screen, "Press SPACE to check/confirm word", 
                       pygame.font.SysFont("arial", 10), 10, 190, CYAN)


def show_pause_menu(score, mode, length, sentence, subject):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    btns = [
        Button(WIDTH//2-100, 120, 200, 45, "Resume", GREEN, DARK_GRAY),
        Button(WIDTH//2-100, 190, 200, 45, "Grammar Helper", PURPLE, DARK_GRAY),
        Button(WIDTH//2-100, 260, 200, 45, "Save & Exit", BLUE, DARK_GRAY),
        Button(WIDTH//2-100, 330, 200, 45, "Exit (No Save)", ORANGE, DARK_GRAY),
        Button(WIDTH//2-100, 400, 200, 45, "Scoreboard", GOLD, DARK_GRAY),
        Button(WIDTH//2-100, 470, 200, 45, "Quit", RED, DARK_GRAY),
    ]
    
    font = pygame.font.SysFont("arial", 48)
    draw_shadow_text(screen, "PAUSED", font, WIDTH//2-70, 40, YELLOW)
    font = pygame.font.SysFont("arial", 20)
    draw_shadow_text(screen, f"Score: {score}", font, WIDTH//2-50, 90)
    
    while True:
        mx, my = pygame.mouse.get_pos()
        for btn in btns:
            btn.update((mx, my))
            btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return "resume"
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btns[0].clicked((mx, my)):
                    return "resume"
                elif btns[1].clicked((mx, my)):
                    show_grammar_panel(sentence, subject)
                    screen.blit(overlay, (0, 0))
                    for b in btns:
                        b.draw(screen)
                elif btns[2].clicked((mx, my)):
                    score_board.add(score, mode, length)
                    return "menu"
                elif btns[3].clicked((mx, my)):
                    return "menu"
                elif btns[4].clicked((mx, my)):
                    show_scoreboard()
                    screen.blit(overlay, (0, 0))
                    for b in btns:
                        b.draw(screen)
                elif btns[5].clicked((mx, my)):
                    pygame.quit()
                    sys.exit()


def show_scoreboard():
    records = score_board.get_top()
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 36)
        draw_shadow_text(screen, "HIGH SCORES", font, WIDTH//2-100, 30, YELLOW)
        
        font = pygame.font.SysFont("arial", 18)
        headers = ["Rank", "Score", "Mode", "Length", "Date"]
        xs = [40, 130, 220, 300, 400]
        for i, h in enumerate(headers):
            draw_shadow_text(screen, h, font, xs[i], 100)
        pygame.draw.line(screen, GRAY, (30, 125), (WIDTH-30, 125), 2)
        
        for i, r in enumerate(records[:8]):
            y = 140 + i * 35
            color = YELLOW if i < 3 else WHITE
            draw_shadow_text(screen, f"#{i+1}", font, 55, y, color)
            draw_shadow_text(screen, str(r[0]), font, 140, y, color)
            draw_shadow_text(screen, r[1], font, 230, y, color)
            draw_shadow_text(screen, str(r[3]), font, 310, y, color)
            draw_shadow_text(screen, r[2][:10], font, 400, y, LIGHT_GRAY)
        
        back = Button(WIDTH//2-80, HEIGHT-60, 160, 40, "Back", GRAY, DARK_GRAY, WHITE, 20)
        back.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back.clicked((mx, my)):
                    return


def game_over_screen(score, mode, length):
    score_board.add(score, mode, length)
    btns = [
        Button(WIDTH//2-200, HEIGHT-90, 170, 45, "Play Again", GREEN, DARK_GRAY),
        Button(WIDTH//2-90, HEIGHT-90, 170, 45, "Scores", BLUE, DARK_GRAY),
        Button(WIDTH//2+20, HEIGHT-90, 170, 45, "Menu", ORANGE, DARK_GRAY),
        Button(WIDTH//2+130, HEIGHT-90, 130, 45, "Quit", RED, DARK_GRAY),
    ]
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 48)
        draw_shadow_text(screen, "GAME OVER", font, WIDTH//2-120, 40, RED)
        font = pygame.font.SysFont("arial", 28)
        draw_shadow_text(screen, f"Score: {score}", font, WIDTH//2-70, 110, YELLOW)
        draw_shadow_text(screen, f"Mode: {mode}", font, WIDTH//2-60, 160)
        draw_shadow_text(screen, f"Length: {length}", font, WIDTH//2-70, 210)
        
        mx, my = pygame.mouse.get_pos()
        for btn in btns:
            btn.update((mx, my))
            btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btns[0].clicked((mx, my)):
                    return "play"
                elif btns[1].clicked((mx, my)):
                    show_scoreboard()
                elif btns[2].clicked((mx, my)):
                    return "menu"
                elif btns[3].clicked((mx, my)):
                    pygame.quit()
                    sys.exit()


# ==================== 游戏主循环 ====================
def game_loop(config):
    snake = Snake(config)
    words = WordSystem(config)
    clock = pygame.time.Clock()
    paused = False
    msg_timer = 0
    msg_text = ""
    msg_color = ORANGE
    last_move = 0
    last_word_check_time = 0
    
    while True:
        now = pygame.time.get_ticks()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE and not paused:
                    res = show_pause_menu(snake.score, config.name, len(snake.body), snake.pool_words, snake.subject)
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
                    # 空格键手动触发单词检查
                    elif ev.key == pygame.K_SPACE and config.word_source != "sentence":
                        if len(snake.collected) >= 2:
                            word = "".join(snake.collected).lower()
                            is_valid, suggestion = word_checker.check_word(word)
                            if is_valid:
                                score_gain = len(word) * config.score_per_word
                                snake.score += score_gain
                                snake.grow()
                                msg_text = f"✓ '{word}' +{score_gain}!"
                                msg_color = GREEN
                                msg_timer = 80
                                snake.collected.clear()
                            else:
                                show_word_check_panel(word, suggestion)
                                msg_text = f"Invalid: '{word}'"
                                msg_color = RED
                                msg_timer = 60
                                snake.collected.clear()
        
        if not paused:
            screen.fill(BLACK)
            
            if now - last_move >= config.speed:
                last_move = now
                eaten = words.eat(snake.body[0], snake.body)
                if eaten:
                    snake.collected.append(eaten["char"])
                    if config.word_source == "sentence":
                        snake.pool_words.append(eaten["char"])
                    
                    # 句子模式：检查句子完成
                    if config.word_source == "sentence":
                        if len(snake.collected) >= 8 and snake.collected[-1] not in END_PUNCTUATIONS:
                            msg_text = "No punctuation! Sentence cleared (8 words)"
                            msg_color = RED
                            msg_timer = 60
                            snake.collected.clear()
                            snake.pool_words.clear()
                        
                        if snake.collected and snake.collected[-1] in END_PUNCTUATIONS:
                            is_valid, check_msg, issues = grammar_checker.check_sentence(snake.collected, snake.subject)
                            
                            if is_valid:
                                score_gain = len(snake.collected) * config.score_per_word
                                snake.score += score_gain
                                snake.grow()
                                bonus = len(snake.pool_words) * 5
                                snake.score += bonus
                                msg_text = f"✅ Correct! +{score_gain} +{bonus} bonus!"
                                msg_color = GREEN
                                msg_timer = 80
                            else:
                                msg_text = f"❌ {check_msg[:35]}"
                                msg_color = RED
                                msg_timer = 60
                            
                            snake.collected.clear()
                            snake.pool_words.clear()
                    
                    # 字母模式：实时检查单词拼写
                    else:
                        # 每次添加字母后立即检查当前组合
                        if len(snake.collected) >= 2:
                            current_word = "".join(snake.collected).lower()
                            is_valid, suggestion = word_checker.check_word(current_word)
                            
                            if is_valid:
                                score_gain = len(current_word) * config.score_per_word
                                snake.score += score_gain
                                snake.grow()
                                msg_text = f"✓ '{current_word}' +{score_gain}!"
                                msg_color = GREEN
                                msg_timer = 80
                                snake.collected.clear()
                            elif len(snake.collected) >= 12:
                                show_word_check_panel(current_word, suggestion)
                                msg_text = f"Too long: '{current_word}'"
                                msg_color = RED
                                msg_timer = 60
                                snake.collected.clear()
                
                if not snake.move():
                    res = game_over_screen(snake.score, config.name, len(snake.body))
                    if res == "play":
                        game_loop(config)
                        return
                    elif res == "menu":
                        return
            
            snake.draw()
            words.draw()
            draw_game_ui(snake, config, words.get_food_count(), words)
            
            if msg_timer > 0:
                font = pygame.font.SysFont("arial", 16)
                draw_shadow_text(screen, msg_text, font, WIDTH//2 - font.size(msg_text)[0]//2, HEIGHT//2-60, msg_color)
                msg_timer -= 1
            
            pygame.display.update()
            clock.tick(60)


# ==================== 速度选择菜单 ====================
def speed_menu(mode_name, mode_color):
    selected = 2
    back = Button(20, HEIGHT-60, 100, 40, "Back", GRAY, DARK_GRAY)
    confirm = Button(WIDTH//2-80, HEIGHT-60, 160, 45, "Confirm", GREEN, DARK_GRAY, BLACK, 20)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 32)
        title = font.render(f"{mode_name} Mode - Speed", True, mode_color)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        w, h = 200, 45
        start_x = (WIDTH - w) // 2
        y = 130
        for i, (name, val) in enumerate(SPEED_OPTIONS):
            rect = pygame.Rect(start_x, y + i*55, w, h)
            if i == selected:
                pygame.draw.rect(screen, mode_color, rect)
                pygame.draw.rect(screen, YELLOW, rect, 3)
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect)
                pygame.draw.rect(screen, GRAY, rect, 2)
            fn = pygame.font.SysFont("arial", 18)
            screen.blit(fn.render(name, True, WHITE), (start_x+15, y+i*55+12))
            screen.blit(fn.render(f"{val}ms", True, LIGHT_GRAY), (start_x+w-65, y+i*55+12))
        
        back.draw(screen)
        confirm.draw(screen)
        hint = pygame.font.SysFont("arial", 12).render("UP/DOWN: Select | ENTER: Confirm", True, GRAY)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT-35))
        pygame.display.update()
        
        mx, my = pygame.mouse.get_pos()
        back.update((mx, my))
        confirm.update((mx, my))
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    selected = max(0, selected-1)
                elif ev.key == pygame.K_DOWN:
                    selected = min(len(SPEED_OPTIONS)-1, selected+1)
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    return SPEED_OPTIONS[selected][1]
                elif ev.key == pygame.K_ESCAPE:
                    return None
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if confirm.clicked((mx, my)):
                    return SPEED_OPTIONS[selected][1]
                if back.clicked((mx, my)):
                    return None
                for i, (name, val) in enumerate(SPEED_OPTIONS):
                    rect = pygame.Rect(start_x, y + i*55, w, h)
                    if rect.collidepoint((mx, my)):
                        selected = i


# ==================== Easy模式菜单 ====================
def easy_style_menu():
    variants = [
        ("standard", "Standard", "All word types"),
        ("simple", "Simple", "Subject + Verb + Object"),
        ("verb_focus", "Verb Focus", "Practice verbs"),
        ("noun_focus", "Noun Focus", "Practice nouns"),
    ]
    selected = 0
    back = Button(20, HEIGHT-60, 100, 40, "Back", GRAY, DARK_GRAY)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 28)
        title = font.render("Easy Mode - Style", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        w, h = 250, 50
        start_x = (WIDTH - w) // 2
        y = 100
        for i, (key, name, desc) in enumerate(variants):
            rect = pygame.Rect(start_x, y + i*60, w, h)
            if i == selected:
                pygame.draw.rect(screen, PURPLE, rect)
                pygame.draw.rect(screen, YELLOW, rect, 3)
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect)
                pygame.draw.rect(screen, GRAY, rect, 2)
            fn = pygame.font.SysFont("arial", 18)
            screen.blit(fn.render(name, True, WHITE), (rect.x+10, rect.y+8))
            fn = pygame.font.SysFont("arial", 12)
            screen.blit(fn.render(desc, True, LIGHT_GRAY), (rect.x+10, rect.y+30))
        
        back.draw(screen)
        control = pygame.font.SysFont("arial", 12).render("UP/DOWN: Select | ENTER: Confirm", True, GRAY)
        screen.blit(control, (WIDTH//2 - control.get_width()//2, HEIGHT-35))
        pygame.display.update()
        
        mx, my = pygame.mouse.get_pos()
        back.update((mx, my))
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    selected = max(0, selected-1)
                elif ev.key == pygame.K_DOWN:
                    selected = min(len(variants)-1, selected+1)
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    return variants[selected][0]
                elif ev.key == pygame.K_ESCAPE:
                    return None
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if back.clicked((mx, my)):
                    return None
                for i, (key, name, desc) in enumerate(variants):
                    rect = pygame.Rect(start_x, y + i*60, w, h)
                    if rect.collidepoint((mx, my)):
                        selected = i


def easy_subject_menu():
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
    back = Button(20, HEIGHT-60, 100, 40, "Back", GRAY, DARK_GRAY)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 32)
        title = font.render("Easy Mode - Subject", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        w, h = 170, 45
        cols = 2
        spacing = 15
        start_x = (WIDTH - cols*w - (cols-1)*spacing)//2
        y = 100
        for i, (key, display, subj) in enumerate(subjects):
            row, col = i//cols, i%cols
            x = start_x + col*(w+spacing)
            rect = pygame.Rect(x, y + row*(h+10), w, h)
            color = PURPLE if key == "mixed" else (GOLD if i == selected else SILVER)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, YELLOW if i == selected else WHITE, rect, 2)
            fn = pygame.font.SysFont("arial", 18)
            screen.blit(fn.render(display, True, WHITE), (x + w//2 - fn.size(display)[0]//2, y + row*(h+10) + h//2 - 9))
        
        back.draw(screen)
        control = pygame.font.SysFont("arial", 12).render("ARROWS: Select | ENTER: Confirm", True, GRAY)
        screen.blit(control, (WIDTH//2 - control.get_width()//2, HEIGHT-35))
        pygame.display.update()
        
        mx, my = pygame.mouse.get_pos()
        back.update((mx, my))
        
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
                    return subjects[selected]
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if back.clicked((mx, my)):
                    return None
                for i, (key, display, subj) in enumerate(subjects):
                    row, col = i//cols, i%cols
                    x = start_x + col*(w+spacing)
                    rect = pygame.Rect(x, y + row*(h+10), w, h)
                    if rect.collidepoint((mx, my)):
                        return (key, display, subj)


# ==================== Medium/Hard菜单 ====================
def medium_hard_menu(difficulty, color):
    current_speed = DEFAULT_SPEED
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 42)
        title = font.render(f"{difficulty} Mode", True, color)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        
        font = pygame.font.SysFont("arial", 18)
        if difficulty == "Medium":
            desc = "A1-B1 letters | Spell German words | Wrap around"
        else:
            desc = "A1-B1 letters | Spell German words | No wrap | Instant death"
        screen.blit(font.render(desc, True, WHITE), (WIDTH//2 - font.size(desc)[0]//2, 160))
        screen.blit(font.render("Collect letters to form valid A1-B1 German words!", True, YELLOW), 
                   (WIDTH//2 - font.size("Collect letters to form valid A1-B1 German words!")[0]//2, 200))
        
        font = pygame.font.SysFont("arial", 18)
        draw_shadow_text(screen, f"Current Speed: {current_speed}ms", font, WIDTH//2 - 90, 250, CYAN)
        
        speed_btn = Button(WIDTH//2-130, 300, 260, 50, "CUSTOMIZE SPEED", PURPLE, DARK_GRAY, WHITE, 20)
        start_btn = Button(WIDTH//2-130, 370, 120, 50, "START", GREEN, DARK_GRAY, BLACK, 24)
        back_btn = Button(WIDTH//2+10, 370, 120, 50, "BACK", GRAY, DARK_GRAY, WHITE, 24)
        
        mx, my = pygame.mouse.get_pos()
        speed_btn.update((mx, my))
        start_btn.update((mx, my))
        back_btn.update((mx, my))
        
        speed_btn.draw(screen)
        start_btn.draw(screen)
        back_btn.draw(screen)
        
        hint = pygame.font.SysFont("arial", 12).render("Click buttons or press ENTER to start", True, GRAY)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT-40))
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return "back", None
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    return "start", current_speed
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if speed_btn.clicked((mx, my)):
                    new_speed = speed_menu(difficulty, color)
                    if new_speed:
                        current_speed = new_speed
                elif start_btn.clicked((mx, my)):
                    return "start", current_speed
                elif back_btn.clicked((mx, my)):
                    return "back", None


# ==================== 主菜单 ====================
def main_menu():
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 36)
        draw_shadow_text(screen, "SNAKE GERMAN WORD GAME", font, WIDTH//2-180, 40, YELLOW)
        draw_shadow_text(screen, "Learn German with Grammar & Word Checker!", 
                       pygame.font.SysFont("arial", 14), WIDTH//2-190, 85, LIGHT_GRAY)
        
        w, h = 160, 55
        spacing = 30
        total = 3*w + 2*spacing
        start_x = (WIDTH - total)//2
        y = 180
        options = [("Easy", GREEN), ("Medium", BLUE), ("Hard", RED)]
        selected = 0
        
        rects = []
        mx, my = pygame.mouse.get_pos()
        
        for i, (name, color) in enumerate(options):
            x = start_x + i*(w+spacing)
            rect = pygame.Rect(x, y, w, h)
            rects.append(rect)
            if rect.collidepoint((mx, my)):
                selected = i
            col = color if i == selected else DARK_GRAY
            pygame.draw.rect(screen, col, rect)
            pygame.draw.rect(screen, YELLOW if i == selected else color, rect, 3)
            fn = pygame.font.SysFont("arial", 26)
            screen.blit(fn.render(name, True, WHITE), (x + w//2 - fn.size(name)[0]//2, y + h//2 - 13))
        
        font = pygame.font.SysFont("arial", 14)
        descs = [
            "Easy: Sentence building | Verb conjugation | Grammar Checker",
            "Medium: A1-B1 letters | Spell valid German words",
            "Hard: A1-B1 letters | No wrap | Instant death"
        ]
        for i, desc in enumerate(descs):
            color = YELLOW if i == selected else GRAY
            draw_shadow_text(screen, desc, font, WIDTH//2-280, 270 + i*24, color)
        
        select_btn = Button(WIDTH//2-100, 360, 200, 45, "SELECT", GREEN, DARK_GRAY, BLACK, 22)
        score_btn = Button(WIDTH//2-100, 420, 200, 40, "VIEW SCORES", BLUE, DARK_GRAY, WHITE, 18)
        
        select_btn.update((mx, my))
        score_btn.update((mx, my))
        
        select_btn.draw(screen)
        score_btn.draw(screen)
        
        draw_shadow_text(screen, "CLICK or use ARROWS + ENTER", pygame.font.SysFont("arial", 12), WIDTH//2-150, HEIGHT-35, GRAY)
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
                            subj_res = easy_subject_menu()
                            if subj_res:
                                key, display, subject = subj_res
                                speed = speed_menu("Easy", GREEN)
                                if speed:
                                    if key == "mixed":
                                        subj = random.choice(["ich", "du", "er", "wir", "ihr", "Sie"])
                                        config = Config(f"Easy (Mixed - {subj})", speed, True, False, "sentence", 10, GREEN, subj)
                                    else:
                                        config = Config(f"Easy ({display})", speed, True, False, "sentence", 10, GREEN, subject)
                                    game_loop(config)
                    elif selected == 1:
                        action, speed = medium_hard_menu("Medium", BLUE)
                        if action == "start" and speed:
                            config = Config("Medium (A1-B1 Letters)", speed, True, False, "alphabet", 15, BLUE)
                            game_loop(config)
                    elif selected == 2:
                        action, speed = medium_hard_menu("Hard", RED)
                        if action == "start" and speed:
                            config = Config("Hard (A1-B1 Letters)", speed, False, True, "alphabet", 15, RED)
                            game_loop(config)
                elif ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if select_btn.clicked((mx, my)):
                    if selected == 0:
                        style = easy_style_menu()
                        if style:
                            subj_res = easy_subject_menu()
                            if subj_res:
                                key, display, subject = subj_res
                                speed = speed_menu("Easy", GREEN)
                                if speed:
                                    if key == "mixed":
                                        subj = random.choice(["ich", "du", "er", "wir", "ihr", "Sie"])
                                        config = Config(f"Easy (Mixed - {subj})", speed, True, False, "sentence", 10, GREEN, subj)
                                    else:
                                        config = Config(f"Easy ({display})", speed, True, False, "sentence", 10, GREEN, subject)
                                    game_loop(config)
                    elif selected == 1:
                        action, speed = medium_hard_menu("Medium", BLUE)
                        if action == "start" and speed:
                            config = Config("Medium (A1-B1 Letters)", speed, True, False, "alphabet", 15, BLUE)
                            game_loop(config)
                    elif selected == 2:
                        action, speed = medium_hard_menu("Hard", RED)
                        if action == "start" and speed:
                            config = Config("Hard (A1-B1 Letters)", speed, False, True, "alphabet", 15, RED)
                            game_loop(config)
                if score_btn.clicked((mx, my)):
                    show_scoreboard()


# ==================== 入口 ====================
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake German Word Game - Learn German!")
    main_menu()
    import pygame
import random
import sys
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple
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
GOLD = (255,215,0)
SILVER = (192,192,192)

# ==================== 遊戲基礎參數 ====================
CELL = 25
WIDTH, HEIGHT = 600, 650
TOTAL_FOOD_COUNT = 60  # 增加到60个食物

# ==================== 速度選項 ====================
SPEED_OPTIONS = [
    ("Very Slow", 250),
    ("Slow", 180),
    ("Normal", 150),
    ("Fast", 100),
    ("Very Fast", 70),
    ("Extreme", 50)
]
DEFAULT_SPEED = 150

# 标点符号
END_PUNCTUATIONS = [".", "!", "?"]
ALL_PUNCTUATIONS = [",", ".", "!", "?"]

# ==================== 词库 ====================
VERBS = {
    "sein": {"ich": "bin", "du": "bist", "er/sie/es": "ist", "wir": "sind", "ihr": "seid", "Sie": "sind"},
    "haben": {"ich": "habe", "du": "hast", "er/sie/es": "hat", "wir": "haben", "ihr": "habt", "Sie": "haben"},
    "gehen": {"ich": "gehe", "du": "gehst", "er/sie/es": "geht", "wir": "gehen", "ihr": "geht", "Sie": "gehen"},
    "kommen": {"ich": "komme", "du": "kommst", "er/sie/es": "kommt", "wir": "kommen", "ihr": "kommt", "Sie": "kommen"},
    "machen": {"ich": "mache", "du": "machst", "er/sie/es": "macht", "wir": "machen", "ihr": "macht", "Sie": "machen"},
    "sagen": {"ich": "sage", "du": "sagst", "er/sie/es": "sagt", "wir": "sagen", "ihr": "sagt", "Sie": "sagen"},
    "schlafen": {"ich": "schlafe", "du": "schläfst", "er/sie/es": "schläft", "wir": "schlafen", "ihr": "schlaft", "Sie": "schlafen"},
    "sehen": {"ich": "sehe", "du": "siehst", "er/sie/es": "sieht", "wir": "sehen", "ihr": "seht", "Sie": "sehen"},
}

NOUNS = {
    "der": ["Mann", "Tisch", "Hund", "Tag", "Baum", "Computer", "Himmel"],
    "die": ["Frau", "Katze", "Blume", "Tür", "Straße", "Lampe", "Sonne"],
    "das": ["Kind", "Haus", "Auto", "Buch", "Fenster", "Bier", "Brot"]
}

ADJECTIVES = ["gut", "schlecht", "groß", "klein", "neu", "alt", "schön", "schnell", "langsam"]
CONJUNCTIONS = ["und", "aber", "denn", "oder", "weil", "dass"]
PREPOSITIONS = ["in", "auf", "an", "zu", "mit", "nach", "aus", "bei", "unter", "über", "neben"]
ADVERBS = ["heute", "gerne", "oft", "immer", "nie", "dort", "hier", "morgen", "jetzt"]
HELPERS = ["Heute", "Jetzt", "Dann", "Morgen", "Vielleicht", "Gestern"]

SUBJECTS = ["ich", "du", "er", "sie", "es", "wir", "ihr", "Sie"]

LETTERS = list("abcdefghijklmnopqrstuvwxyzäöüß")

# ==================== A1-B1 级别德语词汇库（用于单词拼写检查） ====================
A1_B1_WORD_LIST = {
    # 常用动词
    "sein", "haben", "werden", "können", "müssen", "wollen", "dürfen", "sollen",
    "gehen", "kommen", "sehen", "essen", "trinken", "schlafen", "arbeiten", "lernen",
    "sprechen", "schreiben", "lesen", "hören", "spielen", "machen", "sagen", "helfen",
    "finden", "geben", "nehmen", "verstehen", "kaufen", "verkaufen", "wohnen", "reisen",
    
    # 变位形式
    "bin", "bist", "ist", "sind", "seid", "habe", "hast", "hat", "haben", "habt",
    "gehe", "gehst", "geht", "gehen", "komme", "kommst", "kommt", "kommen",
    "sehe", "siehst", "sieht", "sehen", "seht", "schlafe", "schläfst", "schläft",
    "mache", "machst", "macht", "machen", "sage", "sagst", "sagt", "sagen",
    
    # 名词（常见）
    "mann", "frau", "kind", "haus", "auto", "hund", "katze", "tisch", "stuhl", "tür",
    "fenster", "brot", "wasser", "kaffee", "bier", "apfel", "arbeit", "schule", "universität",
    "stadt", "land", "straße", "platz", "park", "garten", "baum", "blume", "himmel", "sonne",
    "mond", "stern", "tag", "nacht", "woche", "monat", "jahr", "uhr", "zeit",
    
    # 形容词
    "gut", "schlecht", "groß", "klein", "neu", "alt", "jung", "schnell", "langsam",
    "schön", "hässlich", "teuer", "billig", "reich", "arm", "glücklich", "traurig",
    "müde", "wach", "krank", "gesund", "heiß", "kalt", "warm", "kühl",
    
    # 副词
    "heute", "morgen", "gestern", "jetzt", "später", "früh", "oft", "immer", "nie",
    "manchmal", "gern", "sehr", "zu", "auch", "nur", "schon", "noch",
    
    # 代词
    "ich", "du", "er", "sie", "es", "wir", "ihr", "Sie", "mir", "dir", "ihm", "ihr",
    
    # 冠词/限定词
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem", "einer", "eines",
    
    # 介词
    "in", "auf", "an", "zu", "mit", "nach", "aus", "bei", "von", "für", "durch", "um", "gegen",
    
    # 连词
    "und", "aber", "denn", "oder", "weil", "dass", "wenn", "dann", "als", "wie",
    
    # 数字
    "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn",
    "elf", "zwölf", "zwanzig", "dreißig", "vierzig", "fünfzig", "hundert", "tausend",
    
    # 疑问词
    "wer", "was", "wo", "woher", "wohin", "wann", "warum", "wie", "welcher",
    
    # 其他常用词
    "bitte", "danke", "ja", "nein", "vielleicht", "natürlich", "leider", "gern", "bald"
}

# ==================== 单词检查器 ====================
class GermanWordChecker:
    """A1-B1级别德语单词拼写检查器"""
    
    def __init__(self):
        self.word_list = A1_B1_WORD_LIST
        self.valid_words = self.word_list
        self.stats = {"checked": 0, "valid": 0, "invalid": 0}
    
    def check_word(self, word: str) -> Tuple[bool, str]:
        word_lower = word.lower().strip()
        self.stats["checked"] += 1
        
        if word_lower in self.valid_words:
            self.stats["valid"] += 1
            return True, word_lower
        else:
            suggestion = self._find_suggestion(word_lower)
            self.stats["invalid"] += 1
            return False, suggestion
    
    def _find_suggestion(self, word: str) -> str:
        best_match = None
        best_score = 0
        
        for valid_word in self.valid_words:
            score = self._similarity_score(word, valid_word)
            if score > best_score and score > 0.6:
                best_score = score
                best_match = valid_word
        
        return best_match if best_match else ""
    
    def _similarity_score(self, word1: str, word2: str) -> float:
        if len(word1) == 0 or len(word2) == 0:
            return 0
        
        common_prefix = 0
        for i in range(min(len(word1), len(word2))):
            if word1[i] == word2[i]:
                common_prefix += 1
            else:
                break
        
        length_diff = abs(len(word1) - len(word2))
        score = (common_prefix / max(len(word1), len(word2))) * (1 - length_diff / max(len(word1), len(word2)))
        
        return score
    
    def get_stats(self):
        return self.stats
    
    def is_valid_word(self, word: str) -> bool:
        return word.lower() in self.valid_words


# 创建全局单词检查器
word_checker = GermanWordChecker()

# ==================== 德語句子語法檢查器 ====================
class GermanSentenceChecker:
    """German sentence grammar checker - validates collected sentence fragments"""
    
    def __init__(self):
        self.valid_patterns = [
            ["subject", "verb"],
            ["subject", "verb", "noun"],
            ["subject", "verb", "preposition"],
            ["subject", "verb", "adjective"],
            ["subject", "verb", "adverb"],
            ["subject", "verb", "determiner", "noun"],
            ["noun", "verb"],
            ["noun", "verb", "noun"],
            ["noun", "verb", "preposition"],
            ["pronoun", "verb"],
            ["pronoun", "verb", "noun"],
        ]
        self.requires_v2 = True
        self.debug_mode = False
        
        # 词类词典
        self.subjects = {"ich", "du", "er", "sie", "es", "wir", "ihr", "Sie"}
        self.pronouns = {"ich", "du", "er", "sie", "es", "wir", "ihr", "Sie", "mir", "dir", "ihm", "ihr"}
        
        # 动词及其变位形式
        self.verbs = set()
        for verb_conj in VERBS.values():
            for form in verb_conj.values():
                self.verbs.add(form.lower())
        
        self.prepositions = set(PREPOSITIONS)
        self.adjectives = set(ADJECTIVES)
        self.adverbs = set(ADVERBS)
        self.determiners = {"der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem", "einer"}
        
        # 主语-动词匹配规则
        self.subject_verb_map = {
            "ich": ["e", "bin", "habe"],
            "du": ["st", "bist", "hast"],
            "er": ["t", "ist", "hat"],
            "sie": ["t", "ist", "hat"],
            "es": ["t", "ist", "hat"],
            "wir": ["en", "sind", "haben"],
            "ihr": ["t", "seid", "habt"],
            "Sie": ["en", "sind", "haben"],
        }
    
    def enable_debug(self):
        self.debug_mode = True
    
    def _get_word_type(self, word: str) -> str:
        word_lower = word.lower()
        
        if word_lower in self.subjects:
            return "subject"
        elif word_lower in self.pronouns:
            return "pronoun"
        elif word_lower in self.verbs:
            return "verb"
        elif word_lower in self.prepositions:
            return "preposition"
        elif word_lower in self.adjectives:
            return "adjective"
        elif word_lower in self.adverbs:
            return "adverb"
        elif word_lower in self.determiners:
            return "determiner"
        else:
            if word and word[0].isupper() and len(word) > 1:
                return "noun"
            return "unknown"
    
    def check_sentence(self, fragments: List[str], subject_hint: str = None) -> Tuple[bool, str, List[str]]:
        issues = []
        
        if not fragments:
            return False, "No words collected yet", ["句子为空，请至少收集2-3个单词"]
        
        if self.debug_mode:
            print(f"[CHECKER] Checking: {' → '.join(fragments)}")
        
        # 1. 检查句末标点
        if fragments[-1] not in END_PUNCTUATIONS:
            issues.append("❌ 句子应以句号(.)、感叹号(!)或问号(?)结尾")
        
        # 2. 识别每个单词的词性
        tagged = [(word, self._get_word_type(word)) for word in fragments]
        
        # 3. 检查最小长度
        if len(tagged) < 2:
            issues.append("❌ 德语句子至少需要主语和动词")
            return False, "句子太短", issues
        
        # 4. 检查是否有动词
        has_verb = any(tag == "verb" for _, tag in tagged)
        if not has_verb:
            issues.append("❌ 每个德语句子都需要一个动词！")
        
        # 5. 检查是否有主语或名词
        has_subject = any(tag in ["subject", "pronoun", "noun"] for _, tag in tagged)
        if not has_subject:
            issues.append("❌ 缺少主语（谁或什么在执行动作？）")
        
        # 6. 检查动词位置
        if self.requires_v2:
            verb_positions = [i for i, (_, tag) in enumerate(tagged) if tag == "verb"]
            if verb_positions:
                first_verb_pos = verb_positions[0]
                if first_verb_pos != 1:
                    issues.append(f"❌ 动词应在第二位（当前在第{first_verb_pos + 1}位）")
            else:
                issues.append("❌ 未找到动词")
        
        # 7. 检查句子开头
        first_word, first_tag = tagged[0]
        if first_tag not in ["subject", "pronoun", "noun", "determiner"]:
            issues.append(f"❌ 句子应以主语或名词开头（'{first_word}' 不是合适的主语）")
        
        # 8. 检查主语-动词一致性
        if has_verb and has_subject:
            subject_word = None
            verb_word = None
            
            for word, tag in tagged:
                if tag in ["subject", "pronoun"] and not subject_word:
                    subject_word = word.lower()
                if tag == "verb" and not verb_word:
                    verb_word = word.lower()
            
            if subject_word and verb_word:
                agreement_ok = self._check_subject_verb_agreement(subject_word, verb_word)
                if not agreement_ok:
                    issues.append(f"❌ 主语 '{subject_word}' 与动词 '{verb_word}' 不匹配")
        
        # 9. 检查句首大写
        first_char = fragments[0][0] if fragments[0] else ''
        if first_char.islower() and fragments[0].lower() not in self.subjects:
            issues.append(f"❌ 句子首单词 '{fragments[0]}' 的首字母应大写")
        
        # 10. 生成总结消息
        if issues:
            critical_issues = [i for i in issues if not i.startswith("💡")]
            if critical_issues:
                main_msg = critical_issues[0]
            else:
                main_msg = "句子有改进空间"
            return False, main_msg, issues
        else:
            return True, "✅ 句子结构正确！", []
    
    def _check_subject_verb_agreement(self, subject: str, verb: str) -> bool:
        if subject not in self.subject_verb_map:
            return True
        
        expected_endings = self.subject_verb_map[subject]
        
        for ending in expected_endings:
            if verb.endswith(ending) or verb == ending:
                return True
        
        return False
    
    def get_grammar_tips(self) -> List[str]:
        return [
            "📖 德语主句结构：主语 + 动词 + 其他成分",
            "📖 动词必须在第二位！",
            "📖 名词首字母永远大写",
            "📖 句子以句号/感叹号/问号结尾",
            "📖 'ich' 需要动词以 -e 结尾",
            "📖 'du' 需要动词以 -st 结尾",
            "📖 'er/sie/es' 需要动词以 -t 结尾",
            "📖 'wir/Sie' 需要动词以 -en 结尾",
            "📖 'ihr' 需要动词以 -t 结尾",
        ]


# 创建全局语法检查器
grammar_checker = GermanSentenceChecker()

# ==================== A1-B1 级别字母权重随机发生器 ====================
class A1B1LetterGenerator:
    """A1-B1级别德语字母权重随机发生器（区分大小写）"""
    
    def __init__(self):
        self.letter_weights = {
            'e': 16.2, 'n': 9.3, 'i': 7.2, 's': 5.4, 'r': 6.3,
            'a': 5.7, 't': 5.8, 'd': 4.3, 'h': 4.5, 'u': 4.0,
            'l': 3.1, 'c': 2.4, 'g': 2.5, 'm': 2.1, 'o': 2.2,
            'f': 1.5, 'w': 1.5, 'b': 1.4, 'k': 1.0, 'z': 0.9,
            'p': 0.6, 'v': 0.5, 'ü': 0.55, 'ä': 0.50, 'ö': 0.40,
            'j': 0.25, 'ß': 0.25, 'x': 0.03, 'y': 0.03, 'q': 0.02,
            'S': 2.1, 'E': 1.1, 'A': 1.0, 'D': 0.8, 'N': 0.7,
            'R': 0.5, 'T': 0.5, 'I': 0.4, 'C': 0.4, 'M': 0.4,
            'H': 0.3, 'G': 0.3, 'B': 0.3, 'U': 0.2, 'L': 0.2,
            'O': 0.2, 'F': 0.2, 'W': 0.2, 'V': 0.2, 'K': 0.1,
            'Z': 0.1, 'P': 0.1, 'J': 0.05, 'Ü': 0.05, 'Ä': 0.05,
            'Ö': 0.05, 'X': 0.02, 'Y': 0.02, 'Q': 0.01,
        }
        
        self.letters = list(self.letter_weights.keys())
        self.weights = list(self.letter_weights.values())
        self.stats = {letter: 0 for letter in self.letters}
        self.total_generated = 0
    
    def sample_letter(self) -> str:
        letter = random.choices(self.letters, weights=self.weights)[0]
        self.stats[letter] += 1
        self.total_generated += 1
        return letter


class WeightedLetterPool:
    def __init__(self):
        self.generator = A1B1LetterGenerator()
        self.buffer = []
        self.buffer_size = 200
        self._refill_buffer()
    
    def _refill_buffer(self):
        while len(self.buffer) < self.buffer_size:
            self.buffer.append(self.generator.sample_letter())
    
    def get_letter(self) -> str:
        if not self.buffer:
            self._refill_buffer()
        letter = self.buffer.pop()
        self._refill_buffer()
        return letter
    
    def get_letters(self, count: int) -> list:
        return [self.get_letter() for _ in range(count)]


# ==================== 权重随机发生器（词类） ====================
class WeightedPOSGenerator:
    def __init__(self):
        self.pos_weights = {
            'verb': 19, 'noun': 19, 'adj_adv': 11, 'prep': 9,
            'conj': 8, 'det': 8, 'pronoun': 9, 'num': 4.5, 'punct': 13.5,
        }
        self.punct_weights = {'.': 50, ',': 35, '?': 9, '!': 4}
        
        self.pos_list = list(self.pos_weights.keys())
        self.pos_weight_values = list(self.pos_weights.values())
        self.punct_list = list(self.punct_weights.keys())
        self.punct_weight_values = list(self.punct_weights.values())
    
    def sample_pos(self):
        return random.choices(self.pos_list, weights=self.pos_weight_values)[0]
    
    def sample_punctuation(self):
        return random.choices(self.punct_list, weights=self.punct_weight_values)[0]
    
    def generate_word(self, pos_type, subject=None):
        if pos_type == 'verb':
            verbs = list(VERBS.keys())
            return {"word": random.choice(verbs), "type": "verb", "needs_conjugation": True, "display_type": "动词"}
        elif pos_type == 'noun':
            art = random.choice(list(NOUNS.keys()))
            noun = random.choice(NOUNS[art])
            return {"word": f"{art} {noun}", "type": "noun", "needs_conjugation": False, "display_type": "名词"}
        elif pos_type == 'adj_adv':
            word = random.choice(ADJECTIVES + ADVERBS)
            return {"word": word, "type": "adj_adv", "needs_conjugation": False, "display_type": "形容词/副词"}
        elif pos_type == 'prep':
            word = random.choice(PREPOSITIONS)
            return {"word": word, "type": "prep", "needs_conjugation": False, "display_type": "介词"}
        elif pos_type == 'conj':
            word = random.choice(CONJUNCTIONS)
            return {"word": word, "type": "conj", "needs_conjugation": False, "display_type": "连词"}
        elif pos_type == 'det':
            art = random.choice(list(NOUNS.keys()))
            return {"word": art, "type": "det", "needs_conjugation": False, "display_type": "冠词"}
        elif pos_type == 'pronoun':
            word = random.choice(SUBJECTS)
            return {"word": word, "type": "pronoun", "needs_conjugation": False, "display_type": "代词"}
        elif pos_type == 'num':
            numbers = ["eins", "zwei", "drei", "vier", "fünf", "zehn", "hundert", "tausend"]
            return {"word": random.choice(numbers), "type": "num", "needs_conjugation": False, "display_type": "数词"}
        elif pos_type == 'punct':
            punct = self.sample_punctuation()
            return {"word": punct, "type": "punct", "needs_conjugation": False, "display_type": "标点"}
        else:
            return {"word": random.choice(list(A1_B1_WORD_LIST)), "type": "default", "needs_conjugation": False, "display_type": "其他"}
    
    def get_weighted_fragment(self, subject=None):
        pos_type = self.sample_pos()
        fragment = self.generate_word(pos_type, subject)
        if fragment["needs_conjugation"] and subject and fragment["type"] == "verb":
            verb_base = fragment["word"]
            if verb_base in VERBS and subject in VERBS[verb_base]:
                fragment["word"] = VERBS[verb_base][subject]
        return fragment


# ==================== 渲染函数 ====================
def draw_shadow_text(surface, text, font, x, y, color=WHITE, shadow=BLACK):
    shadow_surf = font.render(text, True, shadow)
    text_surf = font.render(text, True, color)
    surface.blit(shadow_surf, (x+1, y+1))
    surface.blit(text_surf, (x, y))


# ==================== 按钮类 ====================
class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, text_color=WHITE, size=20):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("arial", size)
        self.hovered = False
    
    def draw(self, surf):
        col = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surf, col, self.rect)
        pygame.draw.rect(surf, WHITE, self.rect, 2)
        tw = self.font.size(self.text)[0]
        th = self.font.get_height()
        draw_shadow_text(surf, self.text, self.font, 
                        self.rect.x + (self.rect.w - tw)//2,
                        self.rect.y + (self.rect.h - th)//2,
                        self.text_color)
    
    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)
    
    def clicked(self, pos):
        return self.rect.collidepoint(pos)


# ==================== 难度配置 ====================
@dataclass
class Config:
    name: str
    speed: int
    allow_wrap: bool
    fatal_self: bool
    word_source: str
    score_per_word: int
    color: Tuple
    subject: str = None


# ==================== 句子池 ====================
class SentencePool:
    def __init__(self, variant="standard"):
        self.generator = WeightedPOSGenerator()
    
    def get(self, subject=None):
        return self.generator.get_weighted_fragment(subject)


# ==================== 分数系统 ====================
class ScoreBoard:
    def __init__(self):
        self.records = []
        self.load()
    
    def load(self):
        try:
            with open("scores.txt", "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        self.records.append((int(parts[0]), parts[1], parts[2], int(parts[3])))
        except:
            pass
        self.records.sort(key=lambda x: x[0], reverse=True)
    
    def save(self):
        with open("scores.txt", "w") as f:
            for r in self.records[:10]:
                f.write(f"{r[0]}|{r[1]}|{r[2]}|{r[3]}\n")
    
    def add(self, score, mode, length):
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.records.append((score, mode, date, length))
        self.records.sort(key=lambda x: x[0], reverse=True)
        self.records = self.records[:10]
        self.save()
    
    def get_top(self):
        return self.records


score_board = ScoreBoard()
screen = None


# ==================== A1-B1 字母系统 ====================
class A1B1LetterSystem:
    def __init__(self, config):
        self.config = config
        self.letter_pool = WeightedLetterPool()
        self.items = []
        self.target = TOTAL_FOOD_COUNT
        self.spawn()
    
    def _random_pos(self):
        return (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT-150, CELL))
    
    def _get_available_positions(self, snake_body):
        occupied = set(snake_body)
        available = []
        for x in range(0, WIDTH, CELL):
            for y in range(0, HEIGHT-150, CELL):
                if (x, y) not in occupied:
                    available.append((x, y))
        return available
    
    def spawn(self):
        self.items = []
        used = set()
        for _ in range(self.target):
            pos = self._random_pos()
            while pos in used:
                pos = self._random_pos()
            used.add(pos)
            letter = self.letter_pool.get_letter()
            self.items.append({"pos": pos, "char": letter, "type": "letter", "display_type": "字母"})
    
    def add_one_food(self, snake_body):
        occupied = set(snake_body)
        for item in self.items:
            occupied.add(item["pos"])
        available = self._get_available_positions(snake_body)
        available = [pos for pos in available if pos not in occupied]
        if not available:
            return False
        new_pos = random.choice(available)
        letter = self.letter_pool.get_letter()
        self.items.append({"pos": new_pos, "char": letter, "type": "letter", "display_type": "字母"})
        return True
    
    def eat(self, head, snake_body):
        for i, item in enumerate(self.items):
            if item["pos"] == head:
                eaten = self.items.pop(i)
                self.add_one_food(snake_body)
                return eaten
        return None
    
    def draw(self):
        for item in self.items:
            x, y = item["pos"]
            char = item["char"]
            if char.isupper():
                color = GOLD
            elif char in ['ä', 'ö', 'ü', 'ß']:
                color = CYAN
            else:
                color = BLUE
            pygame.draw.circle(screen, color, (x+CELL//2, y+CELL//2), CELL//2)
            font = pygame.font.SysFont("arial", 18)
            draw_shadow_text(screen, char, font, x+7, y+5)
    
    def get_food_count(self):
        return len(self.items)


# ==================== 单词系统 ====================
class WordSystem:
    def __init__(self, config):
        self.config = config
        self.target = TOTAL_FOOD_COUNT
        
        if config.word_source == "sentence":
            self.pool = SentencePool()
            self.use_a1b1 = False
            self.items = []
            self.spawn()
        else:
            self.use_a1b1 = True
            self.a1b1_system = A1B1LetterSystem(config)
            self.items = self.a1b1_system.items
    
    def _random_pos(self):
        return (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT-150, CELL))
    
    def _get_available_positions(self, snake_body):
        occupied = set(snake_body)
        available = []
        for x in range(0, WIDTH, CELL):
            for y in range(0, HEIGHT-150, CELL):
                if (x, y) not in occupied:
                    available.append((x, y))
        return available
    
    def spawn(self):
        self.items = []
        used = set()
        for _ in range(self.target):
            pos = self._random_pos()
            while pos in used:
                pos = self._random_pos()
            used.add(pos)
            f = self.pool.get(self.config.subject)
            self.items.append({
                "pos": pos, "char": f["word"], "type": f["type"], 
                "display_type": f.get("display_type", f["type"])
            })
    
    def add_one_food_sentence(self, snake_body):
        occupied = set(snake_body)
        for item in self.items:
            occupied.add(item["pos"])
        available = self._get_available_positions(snake_body)
        available = [pos for pos in available if pos not in occupied]
        if not available:
            return False
        new_pos = random.choice(available)
        f = self.pool.get(self.config.subject)
        self.items.append({
            "pos": new_pos, "char": f["word"], "type": f["type"],
            "display_type": f.get("display_type", f["type"])
        })
        return True
    
    def eat(self, head, snake_body):
        if self.use_a1b1:
            return self.a1b1_system.eat(head, snake_body)
        else:
            for i, item in enumerate(self.items):
                if item["pos"] == head:
                    eaten = self.items.pop(i)
                    self.add_one_food_sentence(snake_body)
                    return eaten
            return None
    
    def draw(self):
        if self.use_a1b1:
            self.a1b1_system.draw()
        else:
            for item in self.items:
                x, y = item["pos"]
                t = item["type"]
                if t == "pronoun":
                    pygame.draw.rect(screen, CYAN, (x, y, CELL-1, CELL-1))
                elif t == "verb":
                    pygame.draw.rect(screen, YELLOW, (x, y, CELL-1, CELL-1))
                elif t == "noun":
                    pygame.draw.rect(screen, ORANGE, (x, y, CELL-1, CELL-1))
                elif t == "punct":
                    pygame.draw.rect(screen, PURPLE, (x, y, CELL-1, CELL-1))
                elif t == "adj_adv":
                    pygame.draw.rect(screen, PINK, (x, y, CELL-1, CELL-1))
                elif t == "prep":
                    pygame.draw.rect(screen, GOLD, (x, y, CELL-1, CELL-1))
                elif t == "conj":
                    pygame.draw.rect(screen, SILVER, (x, y, CELL-1, CELL-1))
                elif t == "det":
                    pygame.draw.rect(screen, (100, 200, 100), (x, y, CELL-1, CELL-1))
                elif t == "num":
                    pygame.draw.rect(screen, (200, 100, 200), (x, y, CELL-1, CELL-1))
                else:
                    pygame.draw.rect(screen, GREEN, (x, y, CELL-1, CELL-1))
                font = pygame.font.SysFont("arial", 14)
                display_char = item["char"][:8] if len(item["char"]) > 8 else item["char"]
                draw_shadow_text(screen, display_char, font, x+3, y+5)
    
    def get_food_count(self):
        return len(self.items)
    
    def check_word(self, collected_letters: List[str]) -> Tuple[bool, int, str]:
        word = "".join(collected_letters).lower()
        
        if len(word) < 2:
            return False, 0, ""
        
        is_valid, suggestion = word_checker.check_word(word)
        
        if is_valid:
            score = len(word) * self.config.score_per_word
            return True, score, word
        else:
            return False, 0, suggestion


# ==================== 蛇类 ====================
class Snake:
    def __init__(self, config):
        self.config = config
        self.body = [(WIDTH//2, HEIGHT//2 - 50)]
        self.dir = (CELL, 0)
        self.next_dir = (CELL, 0)
        self.collected = []
        self.pool_words = []
        self.score = 0
        self.alive = True
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
            if self.config.fatal_self:
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
        if (d[0]*-1, d[1]*-1) != self.dir:
            self.next_dir = d
    
    def draw(self):
        for i, pos in enumerate(self.body):
            x, y = pos
            if i == 0:
                pygame.draw.rect(screen, self.config.color, (x, y, CELL-1, CELL-1))
                eye_offset = CELL // 4
                eye_radius = 3
                if self.dir == (CELL, 0):
                    pygame.draw.circle(screen, WHITE, (x + CELL - 6, y + eye_offset), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + CELL - 6, y + CELL - eye_offset), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + CELL - 5, y + eye_offset), 1)
                    pygame.draw.circle(screen, BLACK, (x + CELL - 5, y + CELL - eye_offset), 1)
                elif self.dir == (-CELL, 0):
                    pygame.draw.circle(screen, WHITE, (x + 6, y + eye_offset), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + 6, y + CELL - eye_offset), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + 5, y + eye_offset), 1)
                    pygame.draw.circle(screen, BLACK, (x + 5, y + CELL - eye_offset), 1)
                elif self.dir == (0, CELL):
                    pygame.draw.circle(screen, WHITE, (x + eye_offset, y + CELL - 6), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + CELL - eye_offset, y + CELL - 6), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + eye_offset, y + CELL - 5), 1)
                    pygame.draw.circle(screen, BLACK, (x + CELL - eye_offset, y + CELL - 5), 1)
                elif self.dir == (0, -CELL):
                    pygame.draw.circle(screen, WHITE, (x + eye_offset, y + 6), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + CELL - eye_offset, y + 6), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + eye_offset, y + 5), 1)
                    pygame.draw.circle(screen, BLACK, (x + CELL - eye_offset, y + 5), 1)
                else:
                    pygame.draw.circle(screen, WHITE, (x + CELL - 6, y + eye_offset), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + CELL - 6, y + CELL - eye_offset), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + CELL - 5, y + eye_offset), 1)
                    pygame.draw.circle(screen, BLACK, (x + CELL - 5, y + CELL - eye_offset), 1)
            else:
                pygame.draw.rect(screen, GREEN, (x, y, CELL-1, CELL-1))


# ==================== Grammar Helper 面板 ====================
def show_grammar_panel(sentence: List[str], subject: str):
    """显示语法检查面板"""
    w, h = 550, 480
    x, y = (WIDTH - w) // 2, (HEIGHT - h) // 2
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    pygame.draw.rect(screen, DARK_GRAY, (x, y, w, h))
    pygame.draw.rect(screen, GOLD, (x, y, w, h), 3)
    
    font_title = pygame.font.SysFont("arial", 24)
    draw_shadow_text(screen, "Grammar Helper", font_title, x + w//2 - 70, y + 15, YELLOW)
    
    font = pygame.font.SysFont("arial", 16)
    current_text = subject + " → " + " → ".join(sentence) if sentence else "(empty)"
    if len(current_text) > 50:
        current_text = current_text[:47] + "..."
    draw_shadow_text(screen, "Current Sentence:", font, x + 15, y + 55, CYAN)
    draw_shadow_text(screen, current_text, pygame.font.SysFont("arial", 14), x + 15, y + 80, WHITE)
    
    is_valid, main_msg, issues = grammar_checker.check_sentence(sentence, subject)
    
    result_color = GREEN if is_valid else RED
    draw_shadow_text(screen, "Grammar Check Result:", font, x + 15, y + 120, result_color)
    draw_shadow_text(screen, main_msg, pygame.font.SysFont("arial", 14), x + 15, y + 145, result_color)
    
    if issues:
        draw_shadow_text(screen, "Details:", font, x + 15, y + 175, ORANGE)
        for i, issue in enumerate(issues[:6]):
            draw_shadow_text(screen, issue, pygame.font.SysFont("arial", 12), 
                           x + 20, y + 200 + i * 22, LIGHT_GRAY)
    
    tips_y = y + 350
    draw_shadow_text(screen, "💡 Grammar Tips:", font, x + 15, tips_y, CYAN)
    tips = grammar_checker.get_grammar_tips()[:5]
    for i, tip in enumerate(tips):
        draw_shadow_text(screen, tip, pygame.font.SysFont("arial", 11), 
                       x + 20, tips_y + 25 + i * 18, LIGHT_GRAY)
    
    close_btn = Button(x + w - 80, y + h - 45, 65, 30, "Close", RED, DARK_GRAY, WHITE, 16)
    close_btn.draw(screen)
    
    pygame.display.update()
    
    while True:
        mx, my = pygame.mouse.get_pos()
        close_btn.update((mx, my))
        close_btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if close_btn.clicked((mx, my)):
                    return


# ==================== 单词检查面板 ====================
def show_word_check_panel(word: str, suggestion: str):
    """显示单词检查结果面板（Medium/Hard模式）"""
    w, h = 400, 250
    x, y = (WIDTH - w) // 2, (HEIGHT - h) // 2
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    pygame.draw.rect(screen, DARK_GRAY, (x, y, w, h))
    pygame.draw.rect(screen, GOLD, (x, y, w, h), 3)
    
    font_title = pygame.font.SysFont("arial", 24)
    draw_shadow_text(screen, "Word Check", font_title, x + w//2 - 55, y + 15, YELLOW)
    
    font = pygame.font.SysFont("arial", 18)
    draw_shadow_text(screen, f"Your word: '{word}'", font, x + 20, y + 65, CYAN)
    
    if suggestion:
        draw_shadow_text(screen, f"Did you mean: '{suggestion}'?", 
                       pygame.font.SysFont("arial", 16), x + 20, y + 105, ORANGE)
        draw_shadow_text(screen, "Tip: Try to spell valid A1-B1 German words!", 
                       pygame.font.SysFont("arial", 12), x + 20, y + 145, LIGHT_GRAY)
    else:
        draw_shadow_text(screen, "Not a valid A1-B1 German word!", 
                       pygame.font.SysFont("arial", 16), x + 20, y + 105, RED)
        draw_shadow_text(screen, "Try shorter or more common words", 
                       pygame.font.SysFont("arial", 12), x + 20, y + 145, LIGHT_GRAY)
    
    close_btn = Button(x + w - 80, y + h - 45, 65, 30, "Close", RED, DARK_GRAY, WHITE, 16)
    close_btn.draw(screen)
    
    pygame.display.update()
    
    while True:
        mx, my = pygame.mouse.get_pos()
        close_btn.update((mx, my))
        close_btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if close_btn.clicked((mx, my)):
                    return
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                return


# ==================== UI函数 ====================
def draw_game_ui(snake, config, food_count, words_system):
    font = pygame.font.SysFont("arial", 18)
    draw_shadow_text(screen, f"Mode: {config.name}", font, 10, 5, config.color)
    draw_shadow_text(screen, f"Score: {snake.score}", font, 10, 30)
    draw_shadow_text(screen, f"Length: {len(snake.body)}", font, 10, 55)
    draw_shadow_text(screen, f"Food: {food_count}/{TOTAL_FOOD_COUNT}", font, 10, 80, CYAN)
    draw_shadow_text(screen, f"Speed: {config.speed}ms", font, WIDTH-110, 5, LIGHT_GRAY)
    
    collected = "".join(snake.collected)
    
    if config.word_source == "sentence":
        draw_shadow_text(screen, f"Current: {collected[:25]}", font, 10, 105)
        draw_shadow_text(screen, f"({len(snake.collected)} words - need . ! ?)", 
                        pygame.font.SysFont("arial", 12), 10, 128, LIGHT_GRAY)
        
        if len(snake.collected) >= 2:
            is_valid, msg, _ = grammar_checker.check_sentence(snake.collected, snake.subject)
            if not is_valid:
                draw_shadow_text(screen, msg[:35], pygame.font.SysFont("arial", 11), 10, 148, RED)
        
        y = HEIGHT - 120
        pygame.draw.rect(screen, DARK_GRAY, (0, y, WIDTH, 120))
        pygame.draw.rect(screen, WHITE, (0, y, WIDTH, 120), 2)
        draw_shadow_text(screen, f"Subject: {snake.subject.upper()}", pygame.font.SysFont("arial", 16), 10, y+5, YELLOW)
        if snake.pool_words:
            text = snake.subject + " → " + " → ".join(snake.pool_words[-8:])
            if len(text) > 45:
                text = text[:42] + "..."
            draw_shadow_text(screen, text, pygame.font.SysFont("arial", 14), 10, y+35)
    else:
        draw_shadow_text(screen, f"Letters: {collected} ({len(snake.collected)})", font, 10, 105)
        draw_shadow_text(screen, "A1-B1 Letter Distribution", pygame.font.SysFont("arial", 10), 10, 128, LIGHT_GRAY)
        
        if len(snake.collected) >= 2:
            word = "".join(snake.collected).lower()
            if word_checker.is_valid_word(word):
                draw_shadow_text(screen, f"✓ '{word}' is a valid German word! (Press SPACE to confirm)", 
                               pygame.font.SysFont("arial", 11), 10, 148, GREEN)
            elif len(word) >= 3:
                draw_shadow_text(screen, f"Current: '{word}'", 
                               pygame.font.SysFont("arial", 11), 10, 148, LIGHT_GRAY)
                suggestion = word_checker._find_suggestion(word)
                if suggestion:
                    draw_shadow_text(screen, f"Did you mean: '{suggestion}'?", 
                                   pygame.font.SysFont("arial", 10), 10, 168, ORANGE)
        else:
            draw_shadow_text(screen, "Collect 2+ letters to form German words!", 
                           pygame.font.SysFont("arial", 10), 10, 148, LIGHT_GRAY)
        
        draw_shadow_text(screen, "Press SPACE to check/confirm word", 
                       pygame.font.SysFont("arial", 10), 10, 190, CYAN)


def show_pause_menu(score, mode, length, sentence, subject):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    btns = [
        Button(WIDTH//2-100, 120, 200, 45, "Resume", GREEN, DARK_GRAY),
        Button(WIDTH//2-100, 190, 200, 45, "Grammar Helper", PURPLE, DARK_GRAY),
        Button(WIDTH//2-100, 260, 200, 45, "Save & Exit", BLUE, DARK_GRAY),
        Button(WIDTH//2-100, 330, 200, 45, "Exit (No Save)", ORANGE, DARK_GRAY),
        Button(WIDTH//2-100, 400, 200, 45, "Scoreboard", GOLD, DARK_GRAY),
        Button(WIDTH//2-100, 470, 200, 45, "Quit", RED, DARK_GRAY),
    ]
    
    font = pygame.font.SysFont("arial", 48)
    draw_shadow_text(screen, "PAUSED", font, WIDTH//2-70, 40, YELLOW)
    font = pygame.font.SysFont("arial", 20)
    draw_shadow_text(screen, f"Score: {score}", font, WIDTH//2-50, 90)
    
    while True:
        mx, my = pygame.mouse.get_pos()
        for btn in btns:
            btn.update((mx, my))
            btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return "resume"
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btns[0].clicked((mx, my)):
                    return "resume"
                elif btns[1].clicked((mx, my)):
                    show_grammar_panel(sentence, subject)
                    screen.blit(overlay, (0, 0))
                    for b in btns:
                        b.draw(screen)
                elif btns[2].clicked((mx, my)):
                    score_board.add(score, mode, length)
                    return "menu"
                elif btns[3].clicked((mx, my)):
                    return "menu"
                elif btns[4].clicked((mx, my)):
                    show_scoreboard()
                    screen.blit(overlay, (0, 0))
                    for b in btns:
                        b.draw(screen)
                elif btns[5].clicked((mx, my)):
                    pygame.quit()
                    sys.exit()


def show_scoreboard():
    records = score_board.get_top()
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 36)
        draw_shadow_text(screen, "HIGH SCORES", font, WIDTH//2-100, 30, YELLOW)
        
        font = pygame.font.SysFont("arial", 18)
        headers = ["Rank", "Score", "Mode", "Length", "Date"]
        xs = [40, 130, 220, 300, 400]
        for i, h in enumerate(headers):
            draw_shadow_text(screen, h, font, xs[i], 100)
        pygame.draw.line(screen, GRAY, (30, 125), (WIDTH-30, 125), 2)
        
        for i, r in enumerate(records[:8]):
            y = 140 + i * 35
            color = YELLOW if i < 3 else WHITE
            draw_shadow_text(screen, f"#{i+1}", font, 55, y, color)
            draw_shadow_text(screen, str(r[0]), font, 140, y, color)
            draw_shadow_text(screen, r[1], font, 230, y, color)
            draw_shadow_text(screen, str(r[3]), font, 310, y, color)
            draw_shadow_text(screen, r[2][:10], font, 400, y, LIGHT_GRAY)
        
        back = Button(WIDTH//2-80, HEIGHT-60, 160, 40, "Back", GRAY, DARK_GRAY, WHITE, 20)
        back.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back.clicked((mx, my)):
                    return


def game_over_screen(score, mode, length):
    score_board.add(score, mode, length)
    btns = [
        Button(WIDTH//2-200, HEIGHT-90, 170, 45, "Play Again", GREEN, DARK_GRAY),
        Button(WIDTH//2-90, HEIGHT-90, 170, 45, "Scores", BLUE, DARK_GRAY),
        Button(WIDTH//2+20, HEIGHT-90, 170, 45, "Menu", ORANGE, DARK_GRAY),
        Button(WIDTH//2+130, HEIGHT-90, 130, 45, "Quit", RED, DARK_GRAY),
    ]
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 48)
        draw_shadow_text(screen, "GAME OVER", font, WIDTH//2-120, 40, RED)
        font = pygame.font.SysFont("arial", 28)
        draw_shadow_text(screen, f"Score: {score}", font, WIDTH//2-70, 110, YELLOW)
        draw_shadow_text(screen, f"Mode: {mode}", font, WIDTH//2-60, 160)
        draw_shadow_text(screen, f"Length: {length}", font, WIDTH//2-70, 210)
        
        mx, my = pygame.mouse.get_pos()
        for btn in btns:
            btn.update((mx, my))
            btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btns[0].clicked((mx, my)):
                    return "play"
                elif btns[1].clicked((mx, my)):
                    show_scoreboard()
                elif btns[2].clicked((mx, my)):
                    return "menu"
                elif btns[3].clicked((mx, my)):
                    pygame.quit()
                    sys.exit()


# ==================== 游戏主循环 ====================
def game_loop(config):
    snake = Snake(config)
    words = WordSystem(config)
    clock = pygame.time.Clock()
    paused = False
    msg_timer = 0
    msg_text = ""
    msg_color = ORANGE
    last_move = 0
    last_word_check_time = 0
    
    while True:
        now = pygame.time.get_ticks()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE and not paused:
                    res = show_pause_menu(snake.score, config.name, len(snake.body), snake.pool_words, snake.subject)
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
                    # 空格键手动触发单词检查
                    elif ev.key == pygame.K_SPACE and config.word_source != "sentence":
                        if len(snake.collected) >= 2:
                            word = "".join(snake.collected).lower()
                            is_valid, suggestion = word_checker.check_word(word)
                            if is_valid:
                                score_gain = len(word) * config.score_per_word
                                snake.score += score_gain
                                snake.grow()
                                msg_text = f"✓ '{word}' +{score_gain}!"
                                msg_color = GREEN
                                msg_timer = 80
                                snake.collected.clear()
                            else:
                                show_word_check_panel(word, suggestion)
                                msg_text = f"Invalid: '{word}'"
                                msg_color = RED
                                msg_timer = 60
                                snake.collected.clear()
        
        if not paused:
            screen.fill(BLACK)
            
            if now - last_move >= config.speed:
                last_move = now
                eaten = words.eat(snake.body[0], snake.body)
                if eaten:
                    snake.collected.append(eaten["char"])
                    if config.word_source == "sentence":
                        snake.pool_words.append(eaten["char"])
                    
                    # 句子模式：检查句子完成
                    if config.word_source == "sentence":
                        if len(snake.collected) >= 8 and snake.collected[-1] not in END_PUNCTUATIONS:
                            msg_text = "No punctuation! Sentence cleared (8 words)"
                            msg_color = RED
                            msg_timer = 60
                            snake.collected.clear()
                            snake.pool_words.clear()
                        
                        if snake.collected and snake.collected[-1] in END_PUNCTUATIONS:
                            is_valid, check_msg, issues = grammar_checker.check_sentence(snake.collected, snake.subject)
                            
                            if is_valid:
                                score_gain = len(snake.collected) * config.score_per_word
                                snake.score += score_gain
                                snake.grow()
                                bonus = len(snake.pool_words) * 5
                                snake.score += bonus
                                msg_text = f"✅ Correct! +{score_gain} +{bonus} bonus!"
                                msg_color = GREEN
                                msg_timer = 80
                            else:
                                msg_text = f"❌ {check_msg[:35]}"
                                msg_color = RED
                                msg_timer = 60
                            
                            snake.collected.clear()
                            snake.pool_words.clear()
                    
                    # 字母模式：实时检查单词拼写
                    else:
                        # 每次添加字母后立即检查当前组合
                        if len(snake.collected) >= 2:
                            current_word = "".join(snake.collected).lower()
                            is_valid, suggestion = word_checker.check_word(current_word)
                            
                            if is_valid:
                                score_gain = len(current_word) * config.score_per_word
                                snake.score += score_gain
                                snake.grow()
                                msg_text = f"✓ '{current_word}' +{score_gain}!"
                                msg_color = GREEN
                                msg_timer = 80
                                snake.collected.clear()
                            elif len(snake.collected) >= 12:
                                show_word_check_panel(current_word, suggestion)
                                msg_text = f"Too long: '{current_word}'"
                                msg_color = RED
                                msg_timer = 60
                                snake.collected.clear()
                
                if not snake.move():
                    res = game_over_screen(snake.score, config.name, len(snake.body))
                    if res == "play":
                        game_loop(config)
                        return
                    elif res == "menu":
                        return
            
            snake.draw()
            words.draw()
            draw_game_ui(snake, config, words.get_food_count(), words)
            
            if msg_timer > 0:
                font = pygame.font.SysFont("arial", 16)
                draw_shadow_text(screen, msg_text, font, WIDTH//2 - font.size(msg_text)[0]//2, HEIGHT//2-60, msg_color)
                msg_timer -= 1
            
            pygame.display.update()
            clock.tick(60)


# ==================== 速度选择菜单 ====================
def speed_menu(mode_name, mode_color):
    selected = 2
    back = Button(20, HEIGHT-60, 100, 40, "Back", GRAY, DARK_GRAY)
    confirm = Button(WIDTH//2-80, HEIGHT-60, 160, 45, "Confirm", GREEN, DARK_GRAY, BLACK, 20)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 32)
        title = font.render(f"{mode_name} Mode - Speed", True, mode_color)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        w, h = 200, 45
        start_x = (WIDTH - w) // 2
        y = 130
        for i, (name, val) in enumerate(SPEED_OPTIONS):
            rect = pygame.Rect(start_x, y + i*55, w, h)
            if i == selected:
                pygame.draw.rect(screen, mode_color, rect)
                pygame.draw.rect(screen, YELLOW, rect, 3)
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect)
                pygame.draw.rect(screen, GRAY, rect, 2)
            fn = pygame.font.SysFont("arial", 18)
            screen.blit(fn.render(name, True, WHITE), (start_x+15, y+i*55+12))
            screen.blit(fn.render(f"{val}ms", True, LIGHT_GRAY), (start_x+w-65, y+i*55+12))
        
        back.draw(screen)
        confirm.draw(screen)
        hint = pygame.font.SysFont("arial", 12).render("UP/DOWN: Select | ENTER: Confirm", True, GRAY)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT-35))
        pygame.display.update()
        
        mx, my = pygame.mouse.get_pos()
        back.update((mx, my))
        confirm.update((mx, my))
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    selected = max(0, selected-1)
                elif ev.key == pygame.K_DOWN:
                    selected = min(len(SPEED_OPTIONS)-1, selected+1)
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    return SPEED_OPTIONS[selected][1]
                elif ev.key == pygame.K_ESCAPE:
                    return None
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if confirm.clicked((mx, my)):
                    return SPEED_OPTIONS[selected][1]
                if back.clicked((mx, my)):
                    return None
                for i, (name, val) in enumerate(SPEED_OPTIONS):
                    rect = pygame.Rect(start_x, y + i*55, w, h)
                    if rect.collidepoint((mx, my)):
                        selected = i


# ==================== Easy模式菜单 ====================
def easy_style_menu():
    variants = [
        ("standard", "Standard", "All word types"),
        ("simple", "Simple", "Subject + Verb + Object"),
        ("verb_focus", "Verb Focus", "Practice verbs"),
        ("noun_focus", "Noun Focus", "Practice nouns"),
    ]
    selected = 0
    back = Button(20, HEIGHT-60, 100, 40, "Back", GRAY, DARK_GRAY)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 28)
        title = font.render("Easy Mode - Style", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        w, h = 250, 50
        start_x = (WIDTH - w) // 2
        y = 100
        for i, (key, name, desc) in enumerate(variants):
            rect = pygame.Rect(start_x, y + i*60, w, h)
            if i == selected:
                pygame.draw.rect(screen, PURPLE, rect)
                pygame.draw.rect(screen, YELLOW, rect, 3)
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect)
                pygame.draw.rect(screen, GRAY, rect, 2)
            fn = pygame.font.SysFont("arial", 18)
            screen.blit(fn.render(name, True, WHITE), (rect.x+10, rect.y+8))
            fn = pygame.font.SysFont("arial", 12)
            screen.blit(fn.render(desc, True, LIGHT_GRAY), (rect.x+10, rect.y+30))
        
        back.draw(screen)
        control = pygame.font.SysFont("arial", 12).render("UP/DOWN: Select | ENTER: Confirm", True, GRAY)
        screen.blit(control, (WIDTH//2 - control.get_width()//2, HEIGHT-35))
        pygame.display.update()
        
        mx, my = pygame.mouse.get_pos()
        back.update((mx, my))
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    selected = max(0, selected-1)
                elif ev.key == pygame.K_DOWN:
                    selected = min(len(variants)-1, selected+1)
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    return variants[selected][0]
                elif ev.key == pygame.K_ESCAPE:
                    return None
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if back.clicked((mx, my)):
                    return None
                for i, (key, name, desc) in enumerate(variants):
                    rect = pygame.Rect(start_x, y + i*60, w, h)
                    if rect.collidepoint((mx, my)):
                        selected = i


def easy_subject_menu():
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
    back = Button(20, HEIGHT-60, 100, 40, "Back", GRAY, DARK_GRAY)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 32)
        title = font.render("Easy Mode - Subject", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        w, h = 170, 45
        cols = 2
        spacing = 15
        start_x = (WIDTH - cols*w - (cols-1)*spacing)//2
        y = 100
        for i, (key, display, subj) in enumerate(subjects):
            row, col = i//cols, i%cols
            x = start_x + col*(w+spacing)
            rect = pygame.Rect(x, y + row*(h+10), w, h)
            color = PURPLE if key == "mixed" else (GOLD if i == selected else SILVER)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, YELLOW if i == selected else WHITE, rect, 2)
            fn = pygame.font.SysFont("arial", 18)
            screen.blit(fn.render(display, True, WHITE), (x + w//2 - fn.size(display)[0]//2, y + row*(h+10) + h//2 - 9))
        
        back.draw(screen)
        control = pygame.font.SysFont("arial", 12).render("ARROWS: Select | ENTER: Confirm", True, GRAY)
        screen.blit(control, (WIDTH//2 - control.get_width()//2, HEIGHT-35))
        pygame.display.update()
        
        mx, my = pygame.mouse.get_pos()
        back.update((mx, my))
        
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
                    return subjects[selected]
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if back.clicked((mx, my)):
                    return None
                for i, (key, display, subj) in enumerate(subjects):
                    row, col = i//cols, i%cols
                    x = start_x + col*(w+spacing)
                    rect = pygame.Rect(x, y + row*(h+10), w, h)
                    if rect.collidepoint((mx, my)):
                        return (key, display, subj)


# ==================== Medium/Hard菜单 ====================
def medium_hard_menu(difficulty, color):
    current_speed = DEFAULT_SPEED
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 42)
        title = font.render(f"{difficulty} Mode", True, color)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        
        font = pygame.font.SysFont("arial", 18)
        if difficulty == "Medium":
            desc = "A1-B1 letters | Spell German words | Wrap around"
        else:
            desc = "A1-B1 letters | Spell German words | No wrap | Instant death"
        screen.blit(font.render(desc, True, WHITE), (WIDTH//2 - font.size(desc)[0]//2, 160))
        screen.blit(font.render("Collect letters to form valid A1-B1 German words!", True, YELLOW), 
                   (WIDTH//2 - font.size("Collect letters to form valid A1-B1 German words!")[0]//2, 200))
        
        font = pygame.font.SysFont("arial", 18)
        draw_shadow_text(screen, f"Current Speed: {current_speed}ms", font, WIDTH//2 - 90, 250, CYAN)
        
        speed_btn = Button(WIDTH//2-130, 300, 260, 50, "CUSTOMIZE SPEED", PURPLE, DARK_GRAY, WHITE, 20)
        start_btn = Button(WIDTH//2-130, 370, 120, 50, "START", GREEN, DARK_GRAY, BLACK, 24)
        back_btn = Button(WIDTH//2+10, 370, 120, 50, "BACK", GRAY, DARK_GRAY, WHITE, 24)
        
        mx, my = pygame.mouse.get_pos()
        speed_btn.update((mx, my))
        start_btn.update((mx, my))
        back_btn.update((mx, my))
        
        speed_btn.draw(screen)
        start_btn.draw(screen)
        back_btn.draw(screen)
        
        hint = pygame.font.SysFont("arial", 12).render("Click buttons or press ENTER to start", True, GRAY)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT-40))
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return "back", None
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    return "start", current_speed
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if speed_btn.clicked((mx, my)):
                    new_speed = speed_menu(difficulty, color)
                    if new_speed:
                        current_speed = new_speed
                elif start_btn.clicked((mx, my)):
                    return "start", current_speed
                elif back_btn.clicked((mx, my)):
                    return "back", None


# ==================== 主菜单 ====================
def main_menu():
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 36)
        draw_shadow_text(screen, "SNAKE GERMAN WORD GAME", font, WIDTH//2-180, 40, YELLOW)
        draw_shadow_text(screen, "Learn German with Grammar & Word Checker!", 
                       pygame.font.SysFont("arial", 14), WIDTH//2-190, 85, LIGHT_GRAY)
        
        w, h = 160, 55
        spacing = 30
        total = 3*w + 2*spacing
        start_x = (WIDTH - total)//2
        y = 180
        options = [("Easy", GREEN), ("Medium", BLUE), ("Hard", RED)]
        selected = 0
        
        rects = []
        mx, my = pygame.mouse.get_pos()
        
        for i, (name, color) in enumerate(options):
            x = start_x + i*(w+spacing)
            rect = pygame.Rect(x, y, w, h)
            rects.append(rect)
            if rect.collidepoint((mx, my)):
                selected = i
            col = color if i == selected else DARK_GRAY
            pygame.draw.rect(screen, col, rect)
            pygame.draw.rect(screen, YELLOW if i == selected else color, rect, 3)
            fn = pygame.font.SysFont("arial", 26)
            screen.blit(fn.render(name, True, WHITE), (x + w//2 - fn.size(name)[0]//2, y + h//2 - 13))
        
        font = pygame.font.SysFont("arial", 14)
        descs = [
            "Easy: Sentence building | Verb conjugation | Grammar Checker",
            "Medium: A1-B1 letters | Spell valid German words",
            "Hard: A1-B1 letters | No wrap | Instant death"
        ]
        for i, desc in enumerate(descs):
            color = YELLOW if i == selected else GRAY
            draw_shadow_text(screen, desc, font, WIDTH//2-280, 270 + i*24, color)
        
        select_btn = Button(WIDTH//2-100, 360, 200, 45, "SELECT", GREEN, DARK_GRAY, BLACK, 22)
        score_btn = Button(WIDTH//2-100, 420, 200, 40, "VIEW SCORES", BLUE, DARK_GRAY, WHITE, 18)
        
        select_btn.update((mx, my))
        score_btn.update((mx, my))
        
        select_btn.draw(screen)
        score_btn.draw(screen)
        
        draw_shadow_text(screen, "CLICK or use ARROWS + ENTER", pygame.font.SysFont("arial", 12), WIDTH//2-150, HEIGHT-35, GRAY)
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
                            subj_res = easy_subject_menu()
                            if subj_res:
                                key, display, subject = subj_res
                                speed = speed_menu("Easy", GREEN)
                                if speed:
                                    if key == "mixed":
                                        subj = random.choice(["ich", "du", "er", "wir", "ihr", "Sie"])
                                        config = Config(f"Easy (Mixed - {subj})", speed, True, False, "sentence", 10, GREEN, subj)
                                    else:
                                        config = Config(f"Easy ({display})", speed, True, False, "sentence", 10, GREEN, subject)
                                    game_loop(config)
                    elif selected == 1:
                        action, speed = medium_hard_menu("Medium", BLUE)
                        if action == "start" and speed:
                            config = Config("Medium (A1-B1 Letters)", speed, True, False, "alphabet", 15, BLUE)
                            game_loop(config)
                    elif selected == 2:
                        action, speed = medium_hard_menu("Hard", RED)
                        if action == "start" and speed:
                            config = Config("Hard (A1-B1 Letters)", speed, False, True, "alphabet", 15, RED)
                            game_loop(config)
                elif ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if select_btn.clicked((mx, my)):
                    if selected == 0:
                        style = easy_style_menu()
                        if style:
                            subj_res = easy_subject_menu()
                            if subj_res:
                                key, display, subject = subj_res
                                speed = speed_menu("Easy", GREEN)
                                if speed:
                                    if key == "mixed":
                                        subj = random.choice(["ich", "du", "er", "wir", "ihr", "Sie"])
                                        config = Config(f"Easy (Mixed - {subj})", speed, True, False, "sentence", 10, GREEN, subj)
                                    else:
                                        config = Config(f"Easy ({display})", speed, True, False, "sentence", 10, GREEN, subject)
                                    game_loop(config)
                    elif selected == 1:
                        action, speed = medium_hard_menu("Medium", BLUE)
                        if action == "start" and speed:
                            config = Config("Medium (A1-B1 Letters)", speed, True, False, "alphabet", 15, BLUE)
                            game_loop(config)
                    elif selected == 2:
                        action, speed = medium_hard_menu("Hard", RED)
                        if action == "start" and speed:
                            config = Config("Hard (A1-B1 Letters)", speed, False, True, "alphabet", 15, RED)
                            game_loop(config)
                if score_btn.clicked((mx, my)):
                    show_scoreboard()


# ==================== 入口 ====================
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake German Word Game - Learn German!")
    main_menu()
    import pygame
import random
import sys
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple
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
GOLD = (255,215,0)
SILVER = (192,192,192)

# ==================== 遊戲基礎參數 ====================
CELL = 25
WIDTH, HEIGHT = 600, 650
TOTAL_FOOD_COUNT = 60  # 增加到60个食物
TOP_SAFE_ZONE = 100    # 顶部安全区域，用于显示UI信息，食物不会出现在这个区域

# ==================== 速度選項 ====================
SPEED_OPTIONS = [
    ("Very Slow", 250),
    ("Slow", 180),
    ("Normal", 150),
    ("Fast", 100),
    ("Very Fast", 70),
    ("Extreme", 50)
]
DEFAULT_SPEED = 150

# 标点符号
END_PUNCTUATIONS = [".", "!", "?"]
ALL_PUNCTUATIONS = [",", ".", "!", "?"]

# ==================== 词库 ====================
VERBS = {
    "sein": {"ich": "bin", "du": "bist", "er/sie/es": "ist", "wir": "sind", "ihr": "seid", "Sie": "sind"},
    "haben": {"ich": "habe", "du": "hast", "er/sie/es": "hat", "wir": "haben", "ihr": "habt", "Sie": "haben"},
    "gehen": {"ich": "gehe", "du": "gehst", "er/sie/es": "geht", "wir": "gehen", "ihr": "geht", "Sie": "gehen"},
    "kommen": {"ich": "komme", "du": "kommst", "er/sie/es": "kommt", "wir": "kommen", "ihr": "kommt", "Sie": "kommen"},
    "machen": {"ich": "mache", "du": "machst", "er/sie/es": "macht", "wir": "machen", "ihr": "macht", "Sie": "machen"},
    "sagen": {"ich": "sage", "du": "sagst", "er/sie/es": "sagt", "wir": "sagen", "ihr": "sagt", "Sie": "sagen"},
    "schlafen": {"ich": "schlafe", "du": "schläfst", "er/sie/es": "schläft", "wir": "schlafen", "ihr": "schlaft", "Sie": "schlafen"},
    "sehen": {"ich": "sehe", "du": "siehst", "er/sie/es": "sieht", "wir": "sehen", "ihr": "seht", "Sie": "sehen"},
}

NOUNS = {
    "der": ["Mann", "Tisch", "Hund", "Tag", "Baum", "Computer", "Himmel"],
    "die": ["Frau", "Katze", "Blume", "Tür", "Straße", "Lampe", "Sonne"],
    "das": ["Kind", "Haus", "Auto", "Buch", "Fenster", "Bier", "Brot"]
}

ADJECTIVES = ["gut", "schlecht", "groß", "klein", "neu", "alt", "schön", "schnell", "langsam"]
CONJUNCTIONS = ["und", "aber", "denn", "oder", "weil", "dass"]
PREPOSITIONS = ["in", "auf", "an", "zu", "mit", "nach", "aus", "bei", "unter", "über", "neben"]
ADVERBS = ["heute", "gerne", "oft", "immer", "nie", "dort", "hier", "morgen", "jetzt"]
HELPERS = ["Heute", "Jetzt", "Dann", "Morgen", "Vielleicht", "Gestern"]

SUBJECTS = ["ich", "du", "er", "sie", "es", "wir", "ihr", "Sie"]

LETTERS = list("abcdefghijklmnopqrstuvwxyzäöüß")

# ==================== A1-B1 级别德语词汇库（用于单词拼写检查） ====================
A1_B1_WORD_LIST = {
    # 常用动词
    "sein", "haben", "werden", "können", "müssen", "wollen", "dürfen", "sollen",
    "gehen", "kommen", "sehen", "essen", "trinken", "schlafen", "arbeiten", "lernen",
    "sprechen", "schreiben", "lesen", "hören", "spielen", "machen", "sagen", "helfen",
    "finden", "geben", "nehmen", "verstehen", "kaufen", "verkaufen", "wohnen", "reisen",
    
    # 变位形式
    "bin", "bist", "ist", "sind", "seid", "habe", "hast", "hat", "haben", "habt",
    "gehe", "gehst", "geht", "gehen", "komme", "kommst", "kommt", "kommen",
    "sehe", "siehst", "sieht", "sehen", "seht", "schlafe", "schläfst", "schläft",
    "mache", "machst", "macht", "machen", "sage", "sagst", "sagt", "sagen",
    
    # 名词（常见）
    "mann", "frau", "kind", "haus", "auto", "hund", "katze", "tisch", "stuhl", "tür",
    "fenster", "brot", "wasser", "kaffee", "bier", "apfel", "arbeit", "schule", "universität",
    "stadt", "land", "straße", "platz", "park", "garten", "baum", "blume", "himmel", "sonne",
    "mond", "stern", "tag", "nacht", "woche", "monat", "jahr", "uhr", "zeit",
    
    # 形容词
    "gut", "schlecht", "groß", "klein", "neu", "alt", "jung", "schnell", "langsam",
    "schön", "hässlich", "teuer", "billig", "reich", "arm", "glücklich", "traurig",
    "müde", "wach", "krank", "gesund", "heiß", "kalt", "warm", "kühl",
    
    # 副词
    "heute", "morgen", "gestern", "jetzt", "später", "früh", "oft", "immer", "nie",
    "manchmal", "gern", "sehr", "zu", "auch", "nur", "schon", "noch",
    
    # 代词
    "ich", "du", "er", "sie", "es", "wir", "ihr", "Sie", "mir", "dir", "ihm", "ihr",
    
    # 冠词/限定词
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem", "einer", "eines",
    
    # 介词
    "in", "auf", "an", "zu", "mit", "nach", "aus", "bei", "von", "für", "durch", "um", "gegen",
    
    # 连词
    "und", "aber", "denn", "oder", "weil", "dass", "wenn", "dann", "als", "wie",
    
    # 数字
    "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn",
    "elf", "zwölf", "zwanzig", "dreißig", "vierzig", "fünfzig", "hundert", "tausend",
    
    # 疑问词
    "wer", "was", "wo", "woher", "wohin", "wann", "warum", "wie", "welcher",
    
    # 其他常用词
    "bitte", "danke", "ja", "nein", "vielleicht", "natürlich", "leider", "gern", "bald"
}

# ==================== 单词检查器 ====================
class GermanWordChecker:
    """A1-B1级别德语单词拼写检查器"""
    
    def __init__(self):
        self.word_list = A1_B1_WORD_LIST
        self.valid_words = self.word_list
        self.stats = {"checked": 0, "valid": 0, "invalid": 0}
    
    def check_word(self, word: str) -> Tuple[bool, str]:
        word_lower = word.lower().strip()
        self.stats["checked"] += 1
        
        if word_lower in self.valid_words:
            self.stats["valid"] += 1
            return True, word_lower
        else:
            suggestion = self._find_suggestion(word_lower)
            self.stats["invalid"] += 1
            return False, suggestion
    
    def _find_suggestion(self, word: str) -> str:
        best_match = None
        best_score = 0
        
        for valid_word in self.valid_words:
            score = self._similarity_score(word, valid_word)
            if score > best_score and score > 0.6:
                best_score = score
                best_match = valid_word
        
        return best_match if best_match else ""
    
    def _similarity_score(self, word1: str, word2: str) -> float:
        if len(word1) == 0 or len(word2) == 0:
            return 0
        
        common_prefix = 0
        for i in range(min(len(word1), len(word2))):
            if word1[i] == word2[i]:
                common_prefix += 1
            else:
                break
        
        length_diff = abs(len(word1) - len(word2))
        score = (common_prefix / max(len(word1), len(word2))) * (1 - length_diff / max(len(word1), len(word2)))
        
        return score
    
    def get_stats(self):
        return self.stats
    
    def is_valid_word(self, word: str) -> bool:
        return word.lower() in self.valid_words


# 创建全局单词检查器
word_checker = GermanWordChecker()

# ==================== 德語句子語法檢查器 ====================
class GermanSentenceChecker:
    """German sentence grammar checker - validates collected sentence fragments"""
    
    def __init__(self):
        self.valid_patterns = [
            ["subject", "verb"],
            ["subject", "verb", "noun"],
            ["subject", "verb", "preposition"],
            ["subject", "verb", "adjective"],
            ["subject", "verb", "adverb"],
            ["subject", "verb", "determiner", "noun"],
            ["noun", "verb"],
            ["noun", "verb", "noun"],
            ["noun", "verb", "preposition"],
            ["pronoun", "verb"],
            ["pronoun", "verb", "noun"],
        ]
        self.requires_v2 = True
        self.debug_mode = False
        
        # 词类词典
        self.subjects = {"ich", "du", "er", "sie", "es", "wir", "ihr", "Sie"}
        self.pronouns = {"ich", "du", "er", "sie", "es", "wir", "ihr", "Sie", "mir", "dir", "ihm", "ihr"}
        
        # 动词及其变位形式
        self.verbs = set()
        for verb_conj in VERBS.values():
            for form in verb_conj.values():
                self.verbs.add(form.lower())
        
        self.prepositions = set(PREPOSITIONS)
        self.adjectives = set(ADJECTIVES)
        self.adverbs = set(ADVERBS)
        self.determiners = {"der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem", "einer"}
        
        # 主语-动词匹配规则
        self.subject_verb_map = {
            "ich": ["e", "bin", "habe"],
            "du": ["st", "bist", "hast"],
            "er": ["t", "ist", "hat"],
            "sie": ["t", "ist", "hat"],
            "es": ["t", "ist", "hat"],
            "wir": ["en", "sind", "haben"],
            "ihr": ["t", "seid", "habt"],
            "Sie": ["en", "sind", "haben"],
        }
    
    def enable_debug(self):
        self.debug_mode = True
    
    def _get_word_type(self, word: str) -> str:
        word_lower = word.lower()
        
        if word_lower in self.subjects:
            return "subject"
        elif word_lower in self.pronouns:
            return "pronoun"
        elif word_lower in self.verbs:
            return "verb"
        elif word_lower in self.prepositions:
            return "preposition"
        elif word_lower in self.adjectives:
            return "adjective"
        elif word_lower in self.adverbs:
            return "adverb"
        elif word_lower in self.determiners:
            return "determiner"
        else:
            if word and word[0].isupper() and len(word) > 1:
                return "noun"
            return "unknown"
    
    def check_sentence(self, fragments: List[str], subject_hint: str = None) -> Tuple[bool, str, List[str]]:
        issues = []
        
        if not fragments:
            return False, "No words collected yet", ["句子为空，请至少收集2-3个单词"]
        
        if self.debug_mode:
            print(f"[CHECKER] Checking: {' → '.join(fragments)}")
        
        # 1. 检查句末标点
        if fragments[-1] not in END_PUNCTUATIONS:
            issues.append("❌ 句子应以句号(.)、感叹号(!)或问号(?)结尾")
        
        # 2. 识别每个单词的词性
        tagged = [(word, self._get_word_type(word)) for word in fragments]
        
        # 3. 检查最小长度
        if len(tagged) < 2:
            issues.append("❌ 德语句子至少需要主语和动词")
            return False, "句子太短", issues
        
        # 4. 检查是否有动词
        has_verb = any(tag == "verb" for _, tag in tagged)
        if not has_verb:
            issues.append("❌ 每个德语句子都需要一个动词！")
        
        # 5. 检查是否有主语或名词
        has_subject = any(tag in ["subject", "pronoun", "noun"] for _, tag in tagged)
        if not has_subject:
            issues.append("❌ 缺少主语（谁或什么在执行动作？）")
        
        # 6. 检查动词位置
        if self.requires_v2:
            verb_positions = [i for i, (_, tag) in enumerate(tagged) if tag == "verb"]
            if verb_positions:
                first_verb_pos = verb_positions[0]
                if first_verb_pos != 1:
                    issues.append(f"❌ 动词应在第二位（当前在第{first_verb_pos + 1}位）")
            else:
                issues.append("❌ 未找到动词")
        
        # 7. 检查句子开头
        first_word, first_tag = tagged[0]
        if first_tag not in ["subject", "pronoun", "noun", "determiner"]:
            issues.append(f"❌ 句子应以主语或名词开头（'{first_word}' 不是合适的主语）")
        
        # 8. 检查主语-动词一致性
        if has_verb and has_subject:
            subject_word = None
            verb_word = None
            
            for word, tag in tagged:
                if tag in ["subject", "pronoun"] and not subject_word:
                    subject_word = word.lower()
                if tag == "verb" and not verb_word:
                    verb_word = word.lower()
            
            if subject_word and verb_word:
                agreement_ok = self._check_subject_verb_agreement(subject_word, verb_word)
                if not agreement_ok:
                    issues.append(f"❌ 主语 '{subject_word}' 与动词 '{verb_word}' 不匹配")
        
        # 9. 检查句首大写
        first_char = fragments[0][0] if fragments[0] else ''
        if first_char.islower() and fragments[0].lower() not in self.subjects:
            issues.append(f"❌ 句子首单词 '{fragments[0]}' 的首字母应大写")
        
        # 10. 生成总结消息
        if issues:
            critical_issues = [i for i in issues if not i.startswith("💡")]
            if critical_issues:
                main_msg = critical_issues[0]
            else:
                main_msg = "句子有改进空间"
            return False, main_msg, issues
        else:
            return True, "✅ 句子结构正确！", []
    
    def _check_subject_verb_agreement(self, subject: str, verb: str) -> bool:
        if subject not in self.subject_verb_map:
            return True
        
        expected_endings = self.subject_verb_map[subject]
        
        for ending in expected_endings:
            if verb.endswith(ending) or verb == ending:
                return True
        
        return False
    
    def get_grammar_tips(self) -> List[str]:
        return [
            "📖 德语主句结构：主语 + 动词 + 其他成分",
            "📖 动词必须在第二位！",
            "📖 名词首字母永远大写",
            "📖 句子以句号/感叹号/问号结尾",
            "📖 'ich' 需要动词以 -e 结尾",
            "📖 'du' 需要动词以 -st 结尾",
            "📖 'er/sie/es' 需要动词以 -t 结尾",
            "📖 'wir/Sie' 需要动词以 -en 结尾",
            "📖 'ihr' 需要动词以 -t 结尾",
        ]


# 创建全局语法检查器
grammar_checker = GermanSentenceChecker()

# ==================== A1-B1 级别字母权重随机发生器 ====================
class A1B1LetterGenerator:
    """A1-B1级别德语字母权重随机发生器（区分大小写）"""
    
    def __init__(self):
        self.letter_weights = {
            'e': 16.2, 'n': 9.3, 'i': 7.2, 's': 5.4, 'r': 6.3,
            'a': 5.7, 't': 5.8, 'd': 4.3, 'h': 4.5, 'u': 4.0,
            'l': 3.1, 'c': 2.4, 'g': 2.5, 'm': 2.1, 'o': 2.2,
            'f': 1.5, 'w': 1.5, 'b': 1.4, 'k': 1.0, 'z': 0.9,
            'p': 0.6, 'v': 0.5, 'ü': 0.55, 'ä': 0.50, 'ö': 0.40,
            'j': 0.25, 'ß': 0.25, 'x': 0.03, 'y': 0.03, 'q': 0.02,
            'S': 2.1, 'E': 1.1, 'A': 1.0, 'D': 0.8, 'N': 0.7,
            'R': 0.5, 'T': 0.5, 'I': 0.4, 'C': 0.4, 'M': 0.4,
            'H': 0.3, 'G': 0.3, 'B': 0.3, 'U': 0.2, 'L': 0.2,
            'O': 0.2, 'F': 0.2, 'W': 0.2, 'V': 0.2, 'K': 0.1,
            'Z': 0.1, 'P': 0.1, 'J': 0.05, 'Ü': 0.05, 'Ä': 0.05,
            'Ö': 0.05, 'X': 0.02, 'Y': 0.02, 'Q': 0.01,
        }
        
        self.letters = list(self.letter_weights.keys())
        self.weights = list(self.letter_weights.values())
        self.stats = {letter: 0 for letter in self.letters}
        self.total_generated = 0
    
    def sample_letter(self) -> str:
        letter = random.choices(self.letters, weights=self.weights)[0]
        self.stats[letter] += 1
        self.total_generated += 1
        return letter


class WeightedLetterPool:
    def __init__(self):
        self.generator = A1B1LetterGenerator()
        self.buffer = []
        self.buffer_size = 200
        self._refill_buffer()
    
    def _refill_buffer(self):
        while len(self.buffer) < self.buffer_size:
            self.buffer.append(self.generator.sample_letter())
    
    def get_letter(self) -> str:
        if not self.buffer:
            self._refill_buffer()
        letter = self.buffer.pop()
        self._refill_buffer()
        return letter
    
    def get_letters(self, count: int) -> list:
        return [self.get_letter() for _ in range(count)]


# ==================== 权重随机发生器（词类） ====================
class WeightedPOSGenerator:
    def __init__(self):
        self.pos_weights = {
            'verb': 19, 'noun': 19, 'adj_adv': 11, 'prep': 9,
            'conj': 8, 'det': 8, 'pronoun': 9, 'num': 4.5, 'punct': 13.5,
        }
        self.punct_weights = {'.': 50, ',': 35, '?': 9, '!': 4}
        
        self.pos_list = list(self.pos_weights.keys())
        self.pos_weight_values = list(self.pos_weights.values())
        self.punct_list = list(self.punct_weights.keys())
        self.punct_weight_values = list(self.punct_weights.values())
    
    def sample_pos(self):
        return random.choices(self.pos_list, weights=self.pos_weight_values)[0]
    
    def sample_punctuation(self):
        return random.choices(self.punct_list, weights=self.punct_weight_values)[0]
    
    def generate_word(self, pos_type, subject=None):
        if pos_type == 'verb':
            verbs = list(VERBS.keys())
            return {"word": random.choice(verbs), "type": "verb", "needs_conjugation": True, "display_type": "动词"}
        elif pos_type == 'noun':
            art = random.choice(list(NOUNS.keys()))
            noun = random.choice(NOUNS[art])
            return {"word": f"{art} {noun}", "type": "noun", "needs_conjugation": False, "display_type": "名词"}
        elif pos_type == 'adj_adv':
            word = random.choice(ADJECTIVES + ADVERBS)
            return {"word": word, "type": "adj_adv", "needs_conjugation": False, "display_type": "形容词/副词"}
        elif pos_type == 'prep':
            word = random.choice(PREPOSITIONS)
            return {"word": word, "type": "prep", "needs_conjugation": False, "display_type": "介词"}
        elif pos_type == 'conj':
            word = random.choice(CONJUNCTIONS)
            return {"word": word, "type": "conj", "needs_conjugation": False, "display_type": "连词"}
        elif pos_type == 'det':
            art = random.choice(list(NOUNS.keys()))
            return {"word": art, "type": "det", "needs_conjugation": False, "display_type": "冠词"}
        elif pos_type == 'pronoun':
            word = random.choice(SUBJECTS)
            return {"word": word, "type": "pronoun", "needs_conjugation": False, "display_type": "代词"}
        elif pos_type == 'num':
            numbers = ["eins", "zwei", "drei", "vier", "fünf", "zehn", "hundert", "tausend"]
            return {"word": random.choice(numbers), "type": "num", "needs_conjugation": False, "display_type": "数词"}
        elif pos_type == 'punct':
            punct = self.sample_punctuation()
            return {"word": punct, "type": "punct", "needs_conjugation": False, "display_type": "标点"}
        else:
            return {"word": random.choice(list(A1_B1_WORD_LIST)), "type": "default", "needs_conjugation": False, "display_type": "其他"}
    
    def get_weighted_fragment(self, subject=None):
        pos_type = self.sample_pos()
        fragment = self.generate_word(pos_type, subject)
        if fragment["needs_conjugation"] and subject and fragment["type"] == "verb":
            verb_base = fragment["word"]
            if verb_base in VERBS and subject in VERBS[verb_base]:
                fragment["word"] = VERBS[verb_base][subject]
        return fragment


# ==================== 渲染函数 ====================
def draw_shadow_text(surface, text, font, x, y, color=WHITE, shadow=BLACK):
    shadow_surf = font.render(text, True, shadow)
    text_surf = font.render(text, True, color)
    surface.blit(shadow_surf, (x+1, y+1))
    surface.blit(text_surf, (x, y))


# ==================== 按钮类 ====================
class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, text_color=WHITE, size=20):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("arial", size)
        self.hovered = False
    
    def draw(self, surf):
        col = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surf, col, self.rect)
        pygame.draw.rect(surf, WHITE, self.rect, 2)
        tw = self.font.size(self.text)[0]
        th = self.font.get_height()
        draw_shadow_text(surf, self.text, self.font, 
                        self.rect.x + (self.rect.w - tw)//2,
                        self.rect.y + (self.rect.h - th)//2,
                        self.text_color)
    
    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)
    
    def clicked(self, pos):
        return self.rect.collidepoint(pos)


# ==================== 难度配置 ====================
@dataclass
class Config:
    name: str
    speed: int
    allow_wrap: bool
    fatal_self: bool
    word_source: str
    score_per_word: int
    color: Tuple
    subject: str = None


# ==================== 句子池 ====================
class SentencePool:
    def __init__(self, variant="standard"):
        self.generator = WeightedPOSGenerator()
    
    def get(self, subject=None):
        return self.generator.get_weighted_fragment(subject)


# ==================== 分数系统 ====================
class ScoreBoard:
    def __init__(self):
        self.records = []
        self.load()
    
    def load(self):
        try:
            with open("scores.txt", "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        self.records.append((int(parts[0]), parts[1], parts[2], int(parts[3])))
        except:
            pass
        self.records.sort(key=lambda x: x[0], reverse=True)
    
    def save(self):
        with open("scores.txt", "w") as f:
            for r in self.records[:10]:
                f.write(f"{r[0]}|{r[1]}|{r[2]}|{r[3]}\n")
    
    def add(self, score, mode, length):
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.records.append((score, mode, date, length))
        self.records.sort(key=lambda x: x[0], reverse=True)
        self.records = self.records[:10]
        self.save()
    
    def get_top(self):
        return self.records


score_board = ScoreBoard()
screen = None


# ==================== A1-B1 字母系统 ====================
class A1B1LetterSystem:
    def __init__(self, config):
        self.config = config
        self.letter_pool = WeightedLetterPool()
        self.items = []
        self.target = TOTAL_FOOD_COUNT
        self.spawn()
    
    def _random_pos(self):
        return (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT-150, CELL))
    
    def _get_available_positions(self, snake_body):
        occupied = set(snake_body)
        available = []
        for x in range(0, WIDTH, CELL):
            for y in range(0, HEIGHT-150, CELL):
                if (x, y) not in occupied:
                    available.append((x, y))
        return available
    
    def spawn(self):
        self.items = []
        used = set()
        for _ in range(self.target):
            pos = self._random_pos()
            while pos in used:
                pos = self._random_pos()
            used.add(pos)
            letter = self.letter_pool.get_letter()
            self.items.append({"pos": pos, "char": letter, "type": "letter", "display_type": "字母"})
    
    def add_one_food(self, snake_body):
        occupied = set(snake_body)
        for item in self.items:
            occupied.add(item["pos"])
        available = self._get_available_positions(snake_body)
        available = [pos for pos in available if pos not in occupied]
        if not available:
            return False
        new_pos = random.choice(available)
        letter = self.letter_pool.get_letter()
        self.items.append({"pos": new_pos, "char": letter, "type": "letter", "display_type": "字母"})
        return True
    
    def eat(self, head, snake_body):
        for i, item in enumerate(self.items):
            if item["pos"] == head:
                eaten = self.items.pop(i)
                self.add_one_food(snake_body)
                return eaten
        return None
    
    def draw(self):
        for item in self.items:
            x, y = item["pos"]
            char = item["char"]
            if char.isupper():
                color = GOLD
            elif char in ['ä', 'ö', 'ü', 'ß']:
                color = CYAN
            else:
                color = BLUE
            pygame.draw.circle(screen, color, (x+CELL//2, y+CELL//2), CELL//2)
            font = pygame.font.SysFont("arial", 18)
            draw_shadow_text(screen, char, font, x+7, y+5)
    
    def get_food_count(self):
        return len(self.items)


# ==================== 单词系统 ====================
class WordSystem:
    def __init__(self, config):
        self.config = config
        self.target = TOTAL_FOOD_COUNT
        
        if config.word_source == "sentence":
            self.pool = SentencePool()
            self.use_a1b1 = False
            self.items = []
            self.spawn()
        else:
            self.use_a1b1 = True
            self.a1b1_system = A1B1LetterSystem(config)
            self.items = self.a1b1_system.items
    
    def _random_pos(self):
        return (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT-150, CELL))
    
    def _get_available_positions(self, snake_body):
        occupied = set(snake_body)
        available = []
        for x in range(0, WIDTH, CELL):
            for y in range(0, HEIGHT-150, CELL):
                if (x, y) not in occupied:
                    available.append((x, y))
        return available
    
    def spawn(self):
        self.items = []
        used = set()
        for _ in range(self.target):
            pos = self._random_pos()
            while pos in used:
                pos = self._random_pos()
            used.add(pos)
            f = self.pool.get(self.config.subject)
            self.items.append({
                "pos": pos, "char": f["word"], "type": f["type"], 
                "display_type": f.get("display_type", f["type"])
            })
    
    def add_one_food_sentence(self, snake_body):
        occupied = set(snake_body)
        for item in self.items:
            occupied.add(item["pos"])
        available = self._get_available_positions(snake_body)
        available = [pos for pos in available if pos not in occupied]
        if not available:
            return False
        new_pos = random.choice(available)
        f = self.pool.get(self.config.subject)
        self.items.append({
            "pos": new_pos, "char": f["word"], "type": f["type"],
            "display_type": f.get("display_type", f["type"])
        })
        return True
    
    def eat(self, head, snake_body):
        if self.use_a1b1:
            return self.a1b1_system.eat(head, snake_body)
        else:
            for i, item in enumerate(self.items):
                if item["pos"] == head:
                    eaten = self.items.pop(i)
                    self.add_one_food_sentence(snake_body)
                    return eaten
            return None
    
    def draw(self):
        if self.use_a1b1:
            self.a1b1_system.draw()
        else:
            for item in self.items:
                x, y = item["pos"]
                t = item["type"]
                if t == "pronoun":
                    pygame.draw.rect(screen, CYAN, (x, y, CELL-1, CELL-1))
                elif t == "verb":
                    pygame.draw.rect(screen, YELLOW, (x, y, CELL-1, CELL-1))
                elif t == "noun":
                    pygame.draw.rect(screen, ORANGE, (x, y, CELL-1, CELL-1))
                elif t == "punct":
                    pygame.draw.rect(screen, PURPLE, (x, y, CELL-1, CELL-1))
                elif t == "adj_adv":
                    pygame.draw.rect(screen, PINK, (x, y, CELL-1, CELL-1))
                elif t == "prep":
                    pygame.draw.rect(screen, GOLD, (x, y, CELL-1, CELL-1))
                elif t == "conj":
                    pygame.draw.rect(screen, SILVER, (x, y, CELL-1, CELL-1))
                elif t == "det":
                    pygame.draw.rect(screen, (100, 200, 100), (x, y, CELL-1, CELL-1))
                elif t == "num":
                    pygame.draw.rect(screen, (200, 100, 200), (x, y, CELL-1, CELL-1))
                else:
                    pygame.draw.rect(screen, GREEN, (x, y, CELL-1, CELL-1))
                font = pygame.font.SysFont("arial", 14)
                display_char = item["char"][:8] if len(item["char"]) > 8 else item["char"]
                draw_shadow_text(screen, display_char, font, x+3, y+5)
    
    def get_food_count(self):
        return len(self.items)
    
    def check_word(self, collected_letters: List[str]) -> Tuple[bool, int, str]:
        word = "".join(collected_letters).lower()
        
        if len(word) < 2:
            return False, 0, ""
        
        is_valid, suggestion = word_checker.check_word(word)
        
        if is_valid:
            score = len(word) * self.config.score_per_word
            return True, score, word
        else:
            return False, 0, suggestion


# ==================== 蛇类 ====================
class Snake:
    def __init__(self, config):
        self.config = config
        self.body = [(WIDTH//2, HEIGHT//2 - 50)]
        self.dir = (CELL, 0)
        self.next_dir = (CELL, 0)
        self.collected = []
        self.pool_words = []
        self.score = 0
        self.alive = True
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
            if self.config.fatal_self:
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
        if (d[0]*-1, d[1]*-1) != self.dir:
            self.next_dir = d
    
    def draw(self):
        for i, pos in enumerate(self.body):
            x, y = pos
            if i == 0:
                pygame.draw.rect(screen, self.config.color, (x, y, CELL-1, CELL-1))
                eye_offset = CELL // 4
                eye_radius = 3
                if self.dir == (CELL, 0):
                    pygame.draw.circle(screen, WHITE, (x + CELL - 6, y + eye_offset), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + CELL - 6, y + CELL - eye_offset), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + CELL - 5, y + eye_offset), 1)
                    pygame.draw.circle(screen, BLACK, (x + CELL - 5, y + CELL - eye_offset), 1)
                elif self.dir == (-CELL, 0):
                    pygame.draw.circle(screen, WHITE, (x + 6, y + eye_offset), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + 6, y + CELL - eye_offset), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + 5, y + eye_offset), 1)
                    pygame.draw.circle(screen, BLACK, (x + 5, y + CELL - eye_offset), 1)
                elif self.dir == (0, CELL):
                    pygame.draw.circle(screen, WHITE, (x + eye_offset, y + CELL - 6), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + CELL - eye_offset, y + CELL - 6), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + eye_offset, y + CELL - 5), 1)
                    pygame.draw.circle(screen, BLACK, (x + CELL - eye_offset, y + CELL - 5), 1)
                elif self.dir == (0, -CELL):
                    pygame.draw.circle(screen, WHITE, (x + eye_offset, y + 6), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + CELL - eye_offset, y + 6), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + eye_offset, y + 5), 1)
                    pygame.draw.circle(screen, BLACK, (x + CELL - eye_offset, y + 5), 1)
                else:
                    pygame.draw.circle(screen, WHITE, (x + CELL - 6, y + eye_offset), eye_radius)
                    pygame.draw.circle(screen, WHITE, (x + CELL - 6, y + CELL - eye_offset), eye_radius)
                    pygame.draw.circle(screen, BLACK, (x + CELL - 5, y + eye_offset), 1)
                    pygame.draw.circle(screen, BLACK, (x + CELL - 5, y + CELL - eye_offset), 1)
            else:
                pygame.draw.rect(screen, GREEN, (x, y, CELL-1, CELL-1))


# ==================== Grammar Helper 面板 ====================
def show_grammar_panel(sentence: List[str], subject: str):
    """显示语法检查面板"""
    w, h = 550, 480
    x, y = (WIDTH - w) // 2, (HEIGHT - h) // 2
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    pygame.draw.rect(screen, DARK_GRAY, (x, y, w, h))
    pygame.draw.rect(screen, GOLD, (x, y, w, h), 3)
    
    font_title = pygame.font.SysFont("arial", 24)
    draw_shadow_text(screen, "Grammar Helper", font_title, x + w//2 - 70, y + 15, YELLOW)
    
    font = pygame.font.SysFont("arial", 16)
    current_text = subject + " → " + " → ".join(sentence) if sentence else "(empty)"
    if len(current_text) > 50:
        current_text = current_text[:47] + "..."
    draw_shadow_text(screen, "Current Sentence:", font, x + 15, y + 55, CYAN)
    draw_shadow_text(screen, current_text, pygame.font.SysFont("arial", 14), x + 15, y + 80, WHITE)
    
    is_valid, main_msg, issues = grammar_checker.check_sentence(sentence, subject)
    
    result_color = GREEN if is_valid else RED
    draw_shadow_text(screen, "Grammar Check Result:", font, x + 15, y + 120, result_color)
    draw_shadow_text(screen, main_msg, pygame.font.SysFont("arial", 14), x + 15, y + 145, result_color)
    
    if issues:
        draw_shadow_text(screen, "Details:", font, x + 15, y + 175, ORANGE)
        for i, issue in enumerate(issues[:6]):
            draw_shadow_text(screen, issue, pygame.font.SysFont("arial", 12), 
                           x + 20, y + 200 + i * 22, LIGHT_GRAY)
    
    tips_y = y + 350
    draw_shadow_text(screen, "💡 Grammar Tips:", font, x + 15, tips_y, CYAN)
    tips = grammar_checker.get_grammar_tips()[:5]
    for i, tip in enumerate(tips):
        draw_shadow_text(screen, tip, pygame.font.SysFont("arial", 11), 
                       x + 20, tips_y + 25 + i * 18, LIGHT_GRAY)
    
    close_btn = Button(x + w - 80, y + h - 45, 65, 30, "Close", RED, DARK_GRAY, WHITE, 16)
    close_btn.draw(screen)
    
    pygame.display.update()
    
    while True:
        mx, my = pygame.mouse.get_pos()
        close_btn.update((mx, my))
        close_btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if close_btn.clicked((mx, my)):
                    return


# ==================== 单词检查面板 ====================
def show_word_check_panel(word: str, suggestion: str):
    """显示单词检查结果面板（Medium/Hard模式）"""
    w, h = 400, 250
    x, y = (WIDTH - w) // 2, (HEIGHT - h) // 2
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    pygame.draw.rect(screen, DARK_GRAY, (x, y, w, h))
    pygame.draw.rect(screen, GOLD, (x, y, w, h), 3)
    
    font_title = pygame.font.SysFont("arial", 24)
    draw_shadow_text(screen, "Word Check", font_title, x + w//2 - 55, y + 15, YELLOW)
    
    font = pygame.font.SysFont("arial", 18)
    draw_shadow_text(screen, f"Your word: '{word}'", font, x + 20, y + 65, CYAN)
    
    if suggestion:
        draw_shadow_text(screen, f"Did you mean: '{suggestion}'?", 
                       pygame.font.SysFont("arial", 16), x + 20, y + 105, ORANGE)
        draw_shadow_text(screen, "Tip: Try to spell valid A1-B1 German words!", 
                       pygame.font.SysFont("arial", 12), x + 20, y + 145, LIGHT_GRAY)
    else:
        draw_shadow_text(screen, "Not a valid A1-B1 German word!", 
                       pygame.font.SysFont("arial", 16), x + 20, y + 105, RED)
        draw_shadow_text(screen, "Try shorter or more common words", 
                       pygame.font.SysFont("arial", 12), x + 20, y + 145, LIGHT_GRAY)
    
    close_btn = Button(x + w - 80, y + h - 45, 65, 30, "Close", RED, DARK_GRAY, WHITE, 16)
    close_btn.draw(screen)
    
    pygame.display.update()
    
    while True:
        mx, my = pygame.mouse.get_pos()
        close_btn.update((mx, my))
        close_btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if close_btn.clicked((mx, my)):
                    return
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                return


# ==================== UI函数 ====================
def draw_game_ui(snake, config, food_count, words_system):
    font = pygame.font.SysFont("arial", 18)
    
    # 绘制半透明背景条，让文字更清晰
    info_bg = pygame.Surface((WIDTH, 95))
    info_bg.set_alpha(180)
    info_bg.fill(BLACK)
    screen.blit(info_bg, (0, 0))
    
    # 第一行：模式名称和速度
    draw_shadow_text(screen, f"Mode: {config.name}", font, 10, 5, config.color)
    draw_shadow_text(screen, f"Speed: {config.speed}ms", font, WIDTH-130, 5, LIGHT_GRAY)
    
    # 第二行：分数和长度
    draw_shadow_text(screen, f"Score: {snake.score}", font, 10, 28)
    draw_shadow_text(screen, f"Length: {len(snake.body)}", font, 10, 51)
    
    # 第三行：食物数量
    draw_shadow_text(screen, f"Food: {food_count}/{TOTAL_FOOD_COUNT}", font, 10, 74, CYAN)
    
    collected = "".join(snake.collected)
    
    if config.word_source == "sentence":
        # 句子模式 - 在游戏区域上方显示当前收集的单词
        draw_shadow_text(screen, f"Current: {collected[:25]}", font, 10, 100)
        draw_shadow_text(screen, f"({len(snake.collected)} words - need . ! ?)", 
                        pygame.font.SysFont("arial", 12), 10, 122, LIGHT_GRAY)
        
        if len(snake.collected) >= 2:
            is_valid, msg, _ = grammar_checker.check_sentence(snake.collected, snake.subject)
            if not is_valid:
                draw_shadow_text(screen, msg[:35], pygame.font.SysFont("arial", 11), 10, 142, RED)
        
        # 句子池显示在底部
        y = HEIGHT - 120
        pool_bg = pygame.Surface((WIDTH, 120))
        pool_bg.set_alpha(200)
        pool_bg.fill(DARK_GRAY)
        screen.blit(pool_bg, (0, y))
        pygame.draw.rect(screen, WHITE, (0, y, WIDTH, 120), 2)
        draw_shadow_text(screen, f"Subject: {snake.subject.upper()}", pygame.font.SysFont("arial", 16), 10, y+5, YELLOW)
        if snake.pool_words:
            text = snake.subject + " → " + " → ".join(snake.pool_words[-8:])
            if len(text) > 45:
                text = text[:42] + "..."
            draw_shadow_text(screen, text, pygame.font.SysFont("arial", 14), 10, y+35)
    else:
        # 字母模式
        draw_shadow_text(screen, f"Letters: {collected} ({len(snake.collected)})", font, 10, 100)
        draw_shadow_text(screen, "A1-B1 Letter Distribution", pygame.font.SysFont("arial", 10), 10, 122, LIGHT_GRAY)
        
        if len(snake.collected) >= 2:
            word = "".join(snake.collected).lower()
            if word_checker.is_valid_word(word):
                draw_shadow_text(screen, f"✓ '{word}' is a valid German word! (Press SPACE to confirm)", 
                               pygame.font.SysFont("arial", 11), 10, 142, GREEN)
            elif len(word) >= 3:
                draw_shadow_text(screen, f"Current: '{word}'", 
                               pygame.font.SysFont("arial", 11), 10, 142, LIGHT_GRAY)
                suggestion = word_checker._find_suggestion(word)
                if suggestion:
                    draw_shadow_text(screen, f"Did you mean: '{suggestion}'?", 
                                   pygame.font.SysFont("arial", 10), 10, 162, ORANGE)
        else:
            draw_shadow_text(screen, "Collect 2+ letters to form German words!", 
                           pygame.font.SysFont("arial", 10), 10, 142, LIGHT_GRAY)
        
        draw_shadow_text(screen, "Press SPACE to check/confirm word", 
                       pygame.font.SysFont("arial", 10), 10, 185, CYAN)
    draw_shadow_text(screen, f"Mode: {config.name}", font, 10, 5, config.color)
    draw_shadow_text(screen, f"Score: {snake.score}", font, 10, 30)
    draw_shadow_text(screen, f"Length: {len(snake.body)}", font, 10, 55)
    draw_shadow_text(screen, f"Food: {food_count}/{TOTAL_FOOD_COUNT}", font, 10, 80, CYAN)
    draw_shadow_text(screen, f"Speed: {config.speed}ms", font, WIDTH-110, 5, LIGHT_GRAY)
    
    collected = "".join(snake.collected)
    
    if config.word_source == "sentence":
        draw_shadow_text(screen, f"Current: {collected[:25]}", font, 10, 105)
        draw_shadow_text(screen, f"({len(snake.collected)} words - need . ! ?)", 
                        pygame.font.SysFont("arial", 12), 10, 128, LIGHT_GRAY)
        
        if len(snake.collected) >= 2:
            is_valid, msg, _ = grammar_checker.check_sentence(snake.collected, snake.subject)
            if not is_valid:
                draw_shadow_text(screen, msg[:35], pygame.font.SysFont("arial", 11), 10, 148, RED)
        
        y = HEIGHT - 120
        pygame.draw.rect(screen, DARK_GRAY, (0, y, WIDTH, 120))
        pygame.draw.rect(screen, WHITE, (0, y, WIDTH, 120), 2)
        draw_shadow_text(screen, f"Subject: {snake.subject.upper()}", pygame.font.SysFont("arial", 16), 10, y+5, YELLOW)
        if snake.pool_words:
            text = snake.subject + " → " + " → ".join(snake.pool_words[-8:])
            if len(text) > 45:
                text = text[:42] + "..."
            draw_shadow_text(screen, text, pygame.font.SysFont("arial", 14), 10, y+35)
    else:
        draw_shadow_text(screen, f"Letters: {collected} ({len(snake.collected)})", font, 10, 105)
        draw_shadow_text(screen, "A1-B1 Letter Distribution", pygame.font.SysFont("arial", 10), 10, 128, LIGHT_GRAY)
        
        if len(snake.collected) >= 2:
            word = "".join(snake.collected).lower()
            if word_checker.is_valid_word(word):
                draw_shadow_text(screen, f"✓ '{word}' is a valid German word! (Press SPACE to confirm)", 
                               pygame.font.SysFont("arial", 11), 10, 148, GREEN)
            elif len(word) >= 3:
                draw_shadow_text(screen, f"Current: '{word}'", 
                               pygame.font.SysFont("arial", 11), 10, 148, LIGHT_GRAY)
                suggestion = word_checker._find_suggestion(word)
                if suggestion:
                    draw_shadow_text(screen, f"Did you mean: '{suggestion}'?", 
                                   pygame.font.SysFont("arial", 10), 10, 168, ORANGE)
        else:
            draw_shadow_text(screen, "Collect 2+ letters to form German words!", 
                           pygame.font.SysFont("arial", 10), 10, 148, LIGHT_GRAY)
        
        draw_shadow_text(screen, "Press SPACE to check/confirm word", 
                       pygame.font.SysFont("arial", 10), 10, 190, CYAN)


def show_pause_menu(score, mode, length, sentence, subject):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    btns = [
        Button(WIDTH//2-100, 120, 200, 45, "Resume", GREEN, DARK_GRAY),
        Button(WIDTH//2-100, 190, 200, 45, "Grammar Helper", PURPLE, DARK_GRAY),
        Button(WIDTH//2-100, 260, 200, 45, "Save & Exit", BLUE, DARK_GRAY),
        Button(WIDTH//2-100, 330, 200, 45, "Exit (No Save)", ORANGE, DARK_GRAY),
        Button(WIDTH//2-100, 400, 200, 45, "Scoreboard", GOLD, DARK_GRAY),
        Button(WIDTH//2-100, 470, 200, 45, "Quit", RED, DARK_GRAY),
    ]
    
    font = pygame.font.SysFont("arial", 48)
    draw_shadow_text(screen, "PAUSED", font, WIDTH//2-70, 40, YELLOW)
    font = pygame.font.SysFont("arial", 20)
    draw_shadow_text(screen, f"Score: {score}", font, WIDTH//2-50, 90)
    
    while True:
        mx, my = pygame.mouse.get_pos()
        for btn in btns:
            btn.update((mx, my))
            btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return "resume"
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btns[0].clicked((mx, my)):
                    return "resume"
                elif btns[1].clicked((mx, my)):
                    show_grammar_panel(sentence, subject)
                    screen.blit(overlay, (0, 0))
                    for b in btns:
                        b.draw(screen)
                elif btns[2].clicked((mx, my)):
                    score_board.add(score, mode, length)
                    return "menu"
                elif btns[3].clicked((mx, my)):
                    return "menu"
                elif btns[4].clicked((mx, my)):
                    show_scoreboard()
                    screen.blit(overlay, (0, 0))
                    for b in btns:
                        b.draw(screen)
                elif btns[5].clicked((mx, my)):
                    pygame.quit()
                    sys.exit()


def show_scoreboard():
    records = score_board.get_top()
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 36)
        draw_shadow_text(screen, "HIGH SCORES", font, WIDTH//2-100, 30, YELLOW)
        
        font = pygame.font.SysFont("arial", 18)
        headers = ["Rank", "Score", "Mode", "Length", "Date"]
        xs = [40, 130, 220, 300, 400]
        for i, h in enumerate(headers):
            draw_shadow_text(screen, h, font, xs[i], 100)
        pygame.draw.line(screen, GRAY, (30, 125), (WIDTH-30, 125), 2)
        
        for i, r in enumerate(records[:8]):
            y = 140 + i * 35
            color = YELLOW if i < 3 else WHITE
            draw_shadow_text(screen, f"#{i+1}", font, 55, y, color)
            draw_shadow_text(screen, str(r[0]), font, 140, y, color)
            draw_shadow_text(screen, r[1], font, 230, y, color)
            draw_shadow_text(screen, str(r[3]), font, 310, y, color)
            draw_shadow_text(screen, r[2][:10], font, 400, y, LIGHT_GRAY)
        
        back = Button(WIDTH//2-80, HEIGHT-60, 160, 40, "Back", GRAY, DARK_GRAY, WHITE, 20)
        back.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back.clicked((mx, my)):
                    return


def game_over_screen(score, mode, length):
    score_board.add(score, mode, length)
    btns = [
        Button(WIDTH//2-200, HEIGHT-90, 170, 45, "Play Again", GREEN, DARK_GRAY),
        Button(WIDTH//2-90, HEIGHT-90, 170, 45, "Scores", BLUE, DARK_GRAY),
        Button(WIDTH//2+20, HEIGHT-90, 170, 45, "Menu", ORANGE, DARK_GRAY),
        Button(WIDTH//2+130, HEIGHT-90, 130, 45, "Quit", RED, DARK_GRAY),
    ]
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 48)
        draw_shadow_text(screen, "GAME OVER", font, WIDTH//2-120, 40, RED)
        font = pygame.font.SysFont("arial", 28)
        draw_shadow_text(screen, f"Score: {score}", font, WIDTH//2-70, 110, YELLOW)
        draw_shadow_text(screen, f"Mode: {mode}", font, WIDTH//2-60, 160)
        draw_shadow_text(screen, f"Length: {length}", font, WIDTH//2-70, 210)
        
        mx, my = pygame.mouse.get_pos()
        for btn in btns:
            btn.update((mx, my))
            btn.draw(screen)
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btns[0].clicked((mx, my)):
                    return "play"
                elif btns[1].clicked((mx, my)):
                    show_scoreboard()
                elif btns[2].clicked((mx, my)):
                    return "menu"
                elif btns[3].clicked((mx, my)):
                    pygame.quit()
                    sys.exit()


# ==================== 游戏主循环 ====================
def game_loop(config):
    snake = Snake(config)
    words = WordSystem(config)
    clock = pygame.time.Clock()
    paused = False
    msg_timer = 0
    msg_text = ""
    msg_color = ORANGE
    last_move = 0
    last_word_check_time = 0
    
    while True:
        now = pygame.time.get_ticks()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE and not paused:
                    res = show_pause_menu(snake.score, config.name, len(snake.body), snake.pool_words, snake.subject)
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
                    # 空格键手动触发单词检查
                    elif ev.key == pygame.K_SPACE and config.word_source != "sentence":
                        if len(snake.collected) >= 2:
                            word = "".join(snake.collected).lower()
                            is_valid, suggestion = word_checker.check_word(word)
                            if is_valid:
                                score_gain = len(word) * config.score_per_word
                                snake.score += score_gain
                                snake.grow()
                                msg_text = f"✓ '{word}' +{score_gain}!"
                                msg_color = GREEN
                                msg_timer = 80
                                snake.collected.clear()
                            else:
                                show_word_check_panel(word, suggestion)
                                msg_text = f"Invalid: '{word}'"
                                msg_color = RED
                                msg_timer = 60
                                snake.collected.clear()
        
        if not paused:
            screen.fill(BLACK)
            
            if now - last_move >= config.speed:
                last_move = now
                eaten = words.eat(snake.body[0], snake.body)
                if eaten:
                    snake.collected.append(eaten["char"])
                    if config.word_source == "sentence":
                        snake.pool_words.append(eaten["char"])
                    
                    # 句子模式：检查句子完成
                    if config.word_source == "sentence":
                        if len(snake.collected) >= 8 and snake.collected[-1] not in END_PUNCTUATIONS:
                            msg_text = "No punctuation! Sentence cleared (8 words)"
                            msg_color = RED
                            msg_timer = 60
                            snake.collected.clear()
                            snake.pool_words.clear()
                        
                        if snake.collected and snake.collected[-1] in END_PUNCTUATIONS:
                            is_valid, check_msg, issues = grammar_checker.check_sentence(snake.collected, snake.subject)
                            
                            if is_valid:
                                score_gain = len(snake.collected) * config.score_per_word
                                snake.score += score_gain
                                snake.grow()
                                bonus = len(snake.pool_words) * 5
                                snake.score += bonus
                                msg_text = f"✅ Correct! +{score_gain} +{bonus} bonus!"
                                msg_color = GREEN
                                msg_timer = 80
                            else:
                                msg_text = f"❌ {check_msg[:35]}"
                                msg_color = RED
                                msg_timer = 60
                            
                            snake.collected.clear()
                            snake.pool_words.clear()
                    
                    # 字母模式：实时检查单词拼写
                    else:
                        # 每次添加字母后立即检查当前组合
                        if len(snake.collected) >= 2:
                            current_word = "".join(snake.collected).lower()
                            is_valid, suggestion = word_checker.check_word(current_word)
                            
                            if is_valid:
                                score_gain = len(current_word) * config.score_per_word
                                snake.score += score_gain
                                snake.grow()
                                msg_text = f"✓ '{current_word}' +{score_gain}!"
                                msg_color = GREEN
                                msg_timer = 80
                                snake.collected.clear()
                            elif len(snake.collected) >= 12:
                                show_word_check_panel(current_word, suggestion)
                                msg_text = f"Too long: '{current_word}'"
                                msg_color = RED
                                msg_timer = 60
                                snake.collected.clear()
                
                if not snake.move():
                    res = game_over_screen(snake.score, config.name, len(snake.body))
                    if res == "play":
                        game_loop(config)
                        return
                    elif res == "menu":
                        return
            
            snake.draw()
            words.draw()
            draw_game_ui(snake, config, words.get_food_count(), words)
            
            if msg_timer > 0:
                font = pygame.font.SysFont("arial", 16)
                draw_shadow_text(screen, msg_text, font, WIDTH//2 - font.size(msg_text)[0]//2, HEIGHT//2-60, msg_color)
                msg_timer -= 1
            
            pygame.display.update()
            clock.tick(60)


# ==================== 速度选择菜单 ====================
def speed_menu(mode_name, mode_color):
    selected = 2
    back = Button(20, HEIGHT-60, 100, 40, "Back", GRAY, DARK_GRAY)
    confirm = Button(WIDTH//2-80, HEIGHT-60, 160, 45, "Confirm", GREEN, DARK_GRAY, BLACK, 20)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 32)
        title = font.render(f"{mode_name} Mode - Speed", True, mode_color)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        w, h = 200, 45
        start_x = (WIDTH - w) // 2
        y = 130
        for i, (name, val) in enumerate(SPEED_OPTIONS):
            rect = pygame.Rect(start_x, y + i*55, w, h)
            if i == selected:
                pygame.draw.rect(screen, mode_color, rect)
                pygame.draw.rect(screen, YELLOW, rect, 3)
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect)
                pygame.draw.rect(screen, GRAY, rect, 2)
            fn = pygame.font.SysFont("arial", 18)
            screen.blit(fn.render(name, True, WHITE), (start_x+15, y+i*55+12))
            screen.blit(fn.render(f"{val}ms", True, LIGHT_GRAY), (start_x+w-65, y+i*55+12))
        
        back.draw(screen)
        confirm.draw(screen)
        hint = pygame.font.SysFont("arial", 12).render("UP/DOWN: Select | ENTER: Confirm", True, GRAY)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT-35))
        pygame.display.update()
        
        mx, my = pygame.mouse.get_pos()
        back.update((mx, my))
        confirm.update((mx, my))
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    selected = max(0, selected-1)
                elif ev.key == pygame.K_DOWN:
                    selected = min(len(SPEED_OPTIONS)-1, selected+1)
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    return SPEED_OPTIONS[selected][1]
                elif ev.key == pygame.K_ESCAPE:
                    return None
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if confirm.clicked((mx, my)):
                    return SPEED_OPTIONS[selected][1]
                if back.clicked((mx, my)):
                    return None
                for i, (name, val) in enumerate(SPEED_OPTIONS):
                    rect = pygame.Rect(start_x, y + i*55, w, h)
                    if rect.collidepoint((mx, my)):
                        selected = i


# ==================== Easy模式菜单 ====================
def easy_style_menu():
    variants = [
        ("standard", "Standard", "All word types"),
        ("simple", "Simple", "Subject + Verb + Object"),
        ("verb_focus", "Verb Focus", "Practice verbs"),
        ("noun_focus", "Noun Focus", "Practice nouns"),
    ]
    selected = 0
    back = Button(20, HEIGHT-60, 100, 40, "Back", GRAY, DARK_GRAY)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 28)
        title = font.render("Easy Mode - Style", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        w, h = 250, 50
        start_x = (WIDTH - w) // 2
        y = 100
        for i, (key, name, desc) in enumerate(variants):
            rect = pygame.Rect(start_x, y + i*60, w, h)
            if i == selected:
                pygame.draw.rect(screen, PURPLE, rect)
                pygame.draw.rect(screen, YELLOW, rect, 3)
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect)
                pygame.draw.rect(screen, GRAY, rect, 2)
            fn = pygame.font.SysFont("arial", 18)
            screen.blit(fn.render(name, True, WHITE), (rect.x+10, rect.y+8))
            fn = pygame.font.SysFont("arial", 12)
            screen.blit(fn.render(desc, True, LIGHT_GRAY), (rect.x+10, rect.y+30))
        
        back.draw(screen)
        control = pygame.font.SysFont("arial", 12).render("UP/DOWN: Select | ENTER: Confirm", True, GRAY)
        screen.blit(control, (WIDTH//2 - control.get_width()//2, HEIGHT-35))
        pygame.display.update()
        
        mx, my = pygame.mouse.get_pos()
        back.update((mx, my))
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    selected = max(0, selected-1)
                elif ev.key == pygame.K_DOWN:
                    selected = min(len(variants)-1, selected+1)
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    return variants[selected][0]
                elif ev.key == pygame.K_ESCAPE:
                    return None
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if back.clicked((mx, my)):
                    return None
                for i, (key, name, desc) in enumerate(variants):
                    rect = pygame.Rect(start_x, y + i*60, w, h)
                    if rect.collidepoint((mx, my)):
                        selected = i


def easy_subject_menu():
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
    back = Button(20, HEIGHT-60, 100, 40, "Back", GRAY, DARK_GRAY)
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 32)
        title = font.render("Easy Mode - Subject", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        w, h = 170, 45
        cols = 2
        spacing = 15
        start_x = (WIDTH - cols*w - (cols-1)*spacing)//2
        y = 100
        for i, (key, display, subj) in enumerate(subjects):
            row, col = i//cols, i%cols
            x = start_x + col*(w+spacing)
            rect = pygame.Rect(x, y + row*(h+10), w, h)
            color = PURPLE if key == "mixed" else (GOLD if i == selected else SILVER)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, YELLOW if i == selected else WHITE, rect, 2)
            fn = pygame.font.SysFont("arial", 18)
            screen.blit(fn.render(display, True, WHITE), (x + w//2 - fn.size(display)[0]//2, y + row*(h+10) + h//2 - 9))
        
        back.draw(screen)
        control = pygame.font.SysFont("arial", 12).render("ARROWS: Select | ENTER: Confirm", True, GRAY)
        screen.blit(control, (WIDTH//2 - control.get_width()//2, HEIGHT-35))
        pygame.display.update()
        
        mx, my = pygame.mouse.get_pos()
        back.update((mx, my))
        
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
                    return subjects[selected]
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if back.clicked((mx, my)):
                    return None
                for i, (key, display, subj) in enumerate(subjects):
                    row, col = i//cols, i%cols
                    x = start_x + col*(w+spacing)
                    rect = pygame.Rect(x, y + row*(h+10), w, h)
                    if rect.collidepoint((mx, my)):
                        return (key, display, subj)


# ==================== Medium/Hard菜单 ====================
def medium_hard_menu(difficulty, color):
    current_speed = DEFAULT_SPEED
    
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 42)
        title = font.render(f"{difficulty} Mode", True, color)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        
        font = pygame.font.SysFont("arial", 18)
        if difficulty == "Medium":
            desc = "A1-B1 letters | Spell German words | Wrap around"
        else:
            desc = "A1-B1 letters | Spell German words | No wrap | Instant death"
        screen.blit(font.render(desc, True, WHITE), (WIDTH//2 - font.size(desc)[0]//2, 160))
        screen.blit(font.render("Collect letters to form valid A1-B1 German words!", True, YELLOW), 
                   (WIDTH//2 - font.size("Collect letters to form valid A1-B1 German words!")[0]//2, 200))
        
        font = pygame.font.SysFont("arial", 18)
        draw_shadow_text(screen, f"Current Speed: {current_speed}ms", font, WIDTH//2 - 90, 250, CYAN)
        
        speed_btn = Button(WIDTH//2-130, 300, 260, 50, "CUSTOMIZE SPEED", PURPLE, DARK_GRAY, WHITE, 20)
        start_btn = Button(WIDTH//2-130, 370, 120, 50, "START", GREEN, DARK_GRAY, BLACK, 24)
        back_btn = Button(WIDTH//2+10, 370, 120, 50, "BACK", GRAY, DARK_GRAY, WHITE, 24)
        
        mx, my = pygame.mouse.get_pos()
        speed_btn.update((mx, my))
        start_btn.update((mx, my))
        back_btn.update((mx, my))
        
        speed_btn.draw(screen)
        start_btn.draw(screen)
        back_btn.draw(screen)
        
        hint = pygame.font.SysFont("arial", 12).render("Click buttons or press ENTER to start", True, GRAY)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT-40))
        pygame.display.update()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return "back", None
                elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                    return "start", current_speed
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if speed_btn.clicked((mx, my)):
                    new_speed = speed_menu(difficulty, color)
                    if new_speed:
                        current_speed = new_speed
                elif start_btn.clicked((mx, my)):
                    return "start", current_speed
                elif back_btn.clicked((mx, my)):
                    return "back", None


# ==================== 主菜单 ====================
def main_menu():
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 36)
        draw_shadow_text(screen, "SNAKE GERMAN WORD GAME", font, WIDTH//2-180, 40, YELLOW)
        draw_shadow_text(screen, "Learn German with Grammar & Word Checker!", 
                       pygame.font.SysFont("arial", 14), WIDTH//2-190, 85, LIGHT_GRAY)
        
        w, h = 160, 55
        spacing = 30
        total = 3*w + 2*spacing
        start_x = (WIDTH - total)//2
        y = 180
        options = [("Easy", GREEN), ("Medium", BLUE), ("Hard", RED)]
        selected = 0
        
        rects = []
        mx, my = pygame.mouse.get_pos()
        
        for i, (name, color) in enumerate(options):
            x = start_x + i*(w+spacing)
            rect = pygame.Rect(x, y, w, h)
            rects.append(rect)
            if rect.collidepoint((mx, my)):
                selected = i
            col = color if i == selected else DARK_GRAY
            pygame.draw.rect(screen, col, rect)
            pygame.draw.rect(screen, YELLOW if i == selected else color, rect, 3)
            fn = pygame.font.SysFont("arial", 26)
            screen.blit(fn.render(name, True, WHITE), (x + w//2 - fn.size(name)[0]//2, y + h//2 - 13))
        
        font = pygame.font.SysFont("arial", 14)
        descs = [
            "Easy: Sentence building | Verb conjugation | Grammar Checker",
            "Medium: A1-B1 letters | Spell valid German words",
            "Hard: A1-B1 letters | No wrap | Instant death"
        ]
        for i, desc in enumerate(descs):
            color = YELLOW if i == selected else GRAY
            draw_shadow_text(screen, desc, font, WIDTH//2-280, 270 + i*24, color)
        
        select_btn = Button(WIDTH//2-100, 360, 200, 45, "SELECT", GREEN, DARK_GRAY, BLACK, 22)
        score_btn = Button(WIDTH//2-100, 420, 200, 40, "VIEW SCORES", BLUE, DARK_GRAY, WHITE, 18)
        
        select_btn.update((mx, my))
        score_btn.update((mx, my))
        
        select_btn.draw(screen)
        score_btn.draw(screen)
        
        draw_shadow_text(screen, "CLICK or use ARROWS + ENTER", pygame.font.SysFont("arial", 12), WIDTH//2-150, HEIGHT-35, GRAY)
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
                            subj_res = easy_subject_menu()
                            if subj_res:
                                key, display, subject = subj_res
                                speed = speed_menu("Easy", GREEN)
                                if speed:
                                    if key == "mixed":
                                        subj = random.choice(["ich", "du", "er", "wir", "ihr", "Sie"])
                                        config = Config(f"Easy (Mixed - {subj})", speed, True, False, "sentence", 10, GREEN, subj)
                                    else:
                                        config = Config(f"Easy ({display})", speed, True, False, "sentence", 10, GREEN, subject)
                                    game_loop(config)
                    elif selected == 1:
                        action, speed = medium_hard_menu("Medium", BLUE)
                        if action == "start" and speed:
                            config = Config("Medium (A1-B1 Letters)", speed, True, False, "alphabet", 15, BLUE)
                            game_loop(config)
                    elif selected == 2:
                        action, speed = medium_hard_menu("Hard", RED)
                        if action == "start" and speed:
                            config = Config("Hard (A1-B1 Letters)", speed, False, True, "alphabet", 15, RED)
                            game_loop(config)
                elif ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if select_btn.clicked((mx, my)):
                    if selected == 0:
                        style = easy_style_menu()
                        if style:
                            subj_res = easy_subject_menu()
                            if subj_res:
                                key, display, subject = subj_res
                                speed = speed_menu("Easy", GREEN)
                                if speed:
                                    if key == "mixed":
                                        subj = random.choice(["ich", "du", "er", "wir", "ihr", "Sie"])
                                        config = Config(f"Easy (Mixed - {subj})", speed, True, False, "sentence", 10, GREEN, subj)
                                    else:
                                        config = Config(f"Easy ({display})", speed, True, False, "sentence", 10, GREEN, subject)
                                    game_loop(config)
                    elif selected == 1:
                        action, speed = medium_hard_menu("Medium", BLUE)
                        if action == "start" and speed:
                            config = Config("Medium (A1-B1 Letters)", speed, True, False, "alphabet", 15, BLUE)
                            game_loop(config)
                    elif selected == 2:
                        action, speed = medium_hard_menu("Hard", RED)
                        if action == "start" and speed:
                            config = Config("Hard (A1-B1 Letters)", speed, False, True, "alphabet", 15, RED)
                            game_loop(config)
                if score_btn.clicked((mx, my)):
                    show_scoreboard()


# ==================== 入口 ====================
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake German Word Game - Learn German!")
    main_menu()