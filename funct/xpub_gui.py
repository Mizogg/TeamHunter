"""

@author: Team Mizogg
"""
import os
import datetime
import time
import sys
import time
import hashlib
import base58
import binascii
import json
import requests
import random
import trotter
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from mnemonic import Mnemonic
from hdwallet import HDWallet
from bloomfilter import BloomFilter
from libs import load_bloom, team_balance
from funct import (win_gui, telegram_gui, discord_gui)
from funct.console_gui import ConsoleWindow
from config import *
import locale
from game.speaker import Speaker
import itertools

addfind = load_bloom.load_bloom_filter()
TEL_ICON = "images/main/Telegram.png"
DIS_ICON = "images/main/Discord.png"
WINNER_FOUND = "found/found.txt"
CONFIG_FILE = "config/config.json"
########### Database Load and Files ###########
mylist = []
 
with open('input/mnemonics.txt', newline='', encoding='utf-8') as f:
    for line in f:
        mylist.append(line.strip())
wordlist = ["abandon","ability","able","about","above","absent","absorb","abstract","absurd","abuse","access","accident","account","accuse","achieve","acid","acoustic","acquire","across","act","action","actor","actress","actual","adapt","add","addict","address","adjust","admit","adult","advance","advice","aerobic","affair","afford","afraid","again","age","agent","agree","ahead","aim","air","airport","aisle","alarm","album","alcohol","alert","alien","all","alley","allow","almost","alone","alpha","already","also","alter","always","amateur","amazing","among","amount","amused","analyst","anchor","ancient","anger","angle","angry","animal","ankle","announce","annual","another","answer","antenna","antique","anxiety","any","apart","apology","appear","apple","approve","april","arch","arctic","area","arena","argue","arm","armed","armor","army","around","arrange","arrest","arrive","arrow","art","artefact","artist","artwork","ask","aspect","assault","asset","assist","assume","asthma","athlete","atom","attack","attend","attitude","attract","auction","audit","august","aunt","author","auto","autumn","average","avocado","avoid","awake","aware","away","awesome","awful","awkward","axis","baby","bachelor","bacon","badge","bag","balance","balcony","ball","bamboo","banana","banner","bar","barely","bargain","barrel","base","basic","basket","battle","beach","bean","beauty","because","become","beef","before","begin","behave","behind","believe","below","belt","bench","benefit","best","betray","better","between","beyond","bicycle","bid","bike","bind","biology","bird","birth","bitter","black","blade","blame","blanket","blast","bleak","bless","blind","blood","blossom","blouse","blue","blur","blush","board","boat","body","boil","bomb","bone","bonus","book","boost","border","boring","borrow","boss","bottom","bounce","box","boy","bracket","brain","brand","brass","brave","bread","breeze","brick","bridge","brief","bright","bring","brisk","broccoli","broken","bronze","broom","brother","brown","brush","bubble","buddy","budget","buffalo","build","bulb","bulk","bullet","bundle","bunker","burden","burger","burst","bus","business","busy","butter","buyer","buzz","cabbage","cabin","cable","cactus","cage","cake", "call", "calm", "camera", "camp", "can", "canal", "cancel", "candy", "cannon", "canoe", "canvas", "canyon", "capable", "capital", "captain", "car", "carbon", "card", "cargo", "carpet", "carry", "cart", "case", "cash", "casino", "castle", "casual", "cat", "catalog", "catch", "category", "cattle", "caught", "cause", "caution", "cave", "ceiling", "celery", "cement", "census", "century", "cereal", "certain", "chair", "chalk", "champion", "change", "chaos", "chapter", "charge", "chase", "chat", "cheap", "check", "cheese", "chef", "cherry", "chest", "chicken", "chief", "child", "chimney", "choice", "choose", "chronic", "chuckle", "chunk", "churn", "cigar", "cinnamon", "circle", "citizen", "city", "civil", "claim", "clap", "clarify", "claw", "clay", "clean", "clerk", "clever", "click", "client", "cliff", "climb", "clinic", "clip", "clock", "clog", "close", "cloth", "cloud", "clown", "club", "clump", "cluster", "clutch", "coach", "coast", "coconut", "code", "coffee", "coil", "coin", "collect", "color", "column", "combine", "come", "comfort", "comic", "common", "company", "concert", "conduct", "confirm", "congress", "connect", "consider", "control", "convince", "cook", "cool", "copper", "copy", "coral", "core", "corn", "correct", "cost", "cotton", "couch", "country", "couple", "course", "cousin", "cover", "coyote", "crack", "cradle", "craft", "cram", "crane", "crash", "crater", "crawl", "crazy", "cream", "credit", "creek", "crew", "cricket", "crime", "crisp", "critic", "crop", "cross", "crouch", "crowd", "crucial", "cruel", "cruise", "crumble", "crunch", "crush", "cry", "crystal", "cube", "culture", "cup", "cupboard", "curious", "current", "curtain", "curve", "cushion", "custom", "cute", "cycle", "dad", "damage", "damp", "dance", "danger", "daring", "dash", "daughter", "dawn", "day", "deal", "debate", "debris", "decade", "december", "decide", "decline", "decorate", "decrease", "deer", "defense", "define", "defy", "degree", "delay", "deliver", "demand", "demise", "denial", "dentist", "deny", "depart", "depend", "deposit", "depth", "deputy", "derive", "describe", "desert", "design", "desk", "despair", "destroy", "detail", "detect", "develop", "device", "devote", "diagram", "dial", "diamond", "diary", "dice", "diesel", "diet", "differ", "digital", "dignity", "dilemma", "dinner", "dinosaur", "direct", "dirt", "disagree", "discover", "disease", "dish", "dismiss", "disorder", "display", "distance", "divert", "divide", "divorce", "dizzy", "doctor", "document", "dog", "doll", "dolphin", "domain", "donate", "donkey", "donor", "door", "dose", "double", "dove", "draft", "dragon", "drama", "drastic", "draw", "dream", "dress", "drift", "drill", "drink", "drip", "drive", "drop", "drum", "dry", "duck", "dumb", "dune", "during", "dust", "dutch", "duty", "dwarf", "dynamic", "eager", "eagle", "early", "earn", "earth", "easily", "east", "easy", "echo", "ecology", "economy", "edge", "edit", "educate", "effort", "egg", "eight", "either", "elbow", "elder", "electric", "elegant", "element", "elephant", "elevator", "elite", "else", "embark", "embody", "embrace", "emerge", "emotion", "employ", "empower", "empty", "enable", "enact", "end", "endless", "endorse", "enemy", "energy", "enforce", "engage", "engine", "enhance", "enjoy", "enlist", "enough", "enrich", "enroll", "ensure", "enter", "entire", "entry", "envelope", "episode", "equal", "equip", "era", "erase", "erode", "erosion", "error", "erupt", "escape", "essay", "essence", "estate", "eternal", "ethics", "evidence", "evil", "evoke", "evolve", "exact", "example", "excess", "exchange", "excite", "exclude", "excuse", "execute", "exercise", "exhaust", "exhibit", "exile", "exist", "exit", "exotic", "expand", "expect", "expire", "explain", "expose", "express", "extend", "extra", "eye", "eyebrow", "fabric", "face", "faculty", "fade", "faint", "faith", "fall", "false", "fame", "family", "famous", "fan", "fancy", "fantasy", "farm", "fashion", "fat", "fatal", "father", "fatigue", "fault", "favorite", "feature", "february", "federal", "fee", "feed", "feel", "female", "fence", "festival", "fetch", "fever", "few", "fiber", "fiction", "field", "figure", "file", "film", "filter", "final", "find", "fine", "finger", "finish", "fire", "firm", "first", "fiscal", "fish", "fit", "fitness", "fix", "flag", "flame", "flash", "flat", "flavor", "flee", "flight", "flip", "float", "flock", "floor", "flower", "fluid", "flush", "fly", "foam", "focus", "fog", "foil", "fold", "follow", "food", "foot", "force", "forest", "forget", "fork", "fortune", "forum", "forward", "fossil", "foster", "found", "fox", "fragile", "frame", "frequent", "fresh", "friend", "fringe", "frog", "front", "frost", "frown", "frozen", "fruit", "fuel", "fun", "funny", "furnace", "fury", "future", "gadget", "gain", "galaxy", "gallery", "game", "gap", "garage", "garbage", "garden", "garlic", "garment", "gas", "gasp", "gate", "gather", "gauge", "gaze", "general", "genius", "genre", "gentle", "genuine", "gesture", "ghost", "giant", "gift", "giggle", "ginger", "giraffe", "girl", "give", "glad", "glance", "glare", "glass", "glide", "glimpse", "globe", "gloom", "glory", "glove", "glow", "glue", "goat", "goddess", "gold", "good", "goose", "gorilla", "gospel", "gossip", "govern", "gown", "grab", "grace", "grain", "grant", "grape", "grass", "gravity", "great", "green", "grid", "grief", "grit", "grocery", "group", "grow", "grunt", "guard", "guess", "guide", "guilt", "guitar", "gun", "gym", "habit", "hair", "half", "hammer", "hamster", "hand", "happy", "harbor", "hard", "harsh", "harvest", "hat", "have", "hawk", "hazard", "head", "health", "heart", "heavy", "hedgehog", "height", "hello", "helmet", "help", "hen", "hero", "hidden", "high", "hill", "hint", "hip", "hire", "history", "hobby", "hockey", "hold", "hole", "holiday", "hollow", "home", "honey", "hood", "hope", "horn", "horror", "horse", "hospital", "host", "hotel", "hour", "hover", "hub", "huge", "human", "humble", "humor", "hundred", "hungry", "hunt", "hurdle", "hurry", "hurt", "husband", "hybrid", "ice", "icon", "idea", "identify", "idle", "ignore", "ill", "illegal", "illness", "image", "imitate", "immense", "immune", "impact", "impose", "improve", "impulse", "inch", "include", "income", "increase", "index", "indicate", "indoor", "industry", "infant", "inflict", "inform", "inhale", "inherit", "initial", "inject", "injury", "inmate", "inner", "innocent", "input", "inquiry", "insane", "insect", "inside", "inspire", "install", "intact", "interest", "into", "invest", "invite", "involve", "iron", "island", "isolate", "issue", "item", "ivory", "jacket", "jaguar", "jar", "jazz", "jealous", "jeans", "jelly", "jewel", "job", "join", "joke", "journey", "joy", "judge", "juice", "jump", "jungle", "junior", "junk", "just", "kangaroo", "keen", "keep", "ketchup", "key", "kick", "kid", "kidney", "kind", "kingdom", "kiss", "kit", "kitchen", "kite", "kitten", "kiwi", "knee", "knife", "knock", "know", "lab", "label", "labor", "ladder", "lady", "lake", "lamp", "language", "laptop", "large", "later", "latin", "laugh", "laundry", "lava", "law", "lawn", "lawsuit", "layer", "lazy", "leader", "leaf", "learn", "leave", "lecture", "left", "leg", "legal", "legend", "leisure", "lemon", "lend", "length", "lens", "leopard", "lesson", "letter", "level", "liar", "liberty", "library", "license", "life", "lift", "light", "like", "limb", "limit", "link", "lion", "liquid", "list", "little", "live", "lizard", "load", "loan", "lobster", "local", "lock", "logic", "lonely", "long", "loop", "lottery", "loud", "lounge", "love", "loyal", "lucky", "luggage", "lumber", "lunar", "lunch", "luxury", "lyrics", "machine", "mad", "magic", "magnet", "maid", "mail", "main", "major", "make", "mammal", "man", "manage", "mandate", "mango", "mansion", "manual", "maple", "marble", "march", "margin", "marine", "market", "marriage", "mask", "mass", "master", "match", "material", "math", "matrix", "matter", "maximum", "maze", "meadow", "mean", "measure", "meat", "mechanic", "medal", "media", "melody", "melt", "member", "memory", "mention", "menu", "mercy", "merge", "merit", "merry", "mesh", "message", "metal", "method", "middle", "midnight", "milk", "million", "mimic", "mind", "minimum", "minor", "minute", "miracle", "mirror", "misery", "miss", "mistake", "mix", "mixed", "mixture", "mobile", "model", "modify", "mom", "moment", "monitor", "monkey", "monster", "month", "moon", "moral", "more", "morning", "mosquito", "mother", "motion", "motor", "mountain", "mouse", "move", "movie", "much", "muffin", "mule", "multiply", "muscle", "museum", "mushroom", "music", "must", "mutual", "myself", "mystery", "myth", "naive", "name", "napkin", "narrow", "nasty", "nation", "nature", "near", "neck", "need", "negative", "neglect", "neither", "nephew", "nerve", "nest", "net", "network", "neutral", "never", "news", "next", "nice", "night", "noble", "noise", "nominee", "noodle", "normal", "north", "nose", "notable", "note", "nothing", "notice", "novel", "now", "nuclear", "number", "nurse", "nut", "oak", "obey", "object", "oblige", "obscure", "observe", "obtain", "obvious", "occur", "ocean", "october", "odor", "off", "offer", "office", "often", "oil", "okay", "old", "olive", "olympic", "omit", "once", "one", "onion", "online", "only", "open", "opera", "opinion", "oppose", "option", "orange", "orbit", "orchard", "order", "ordinary", "organ", "orient", "original", "orphan", "ostrich", "other", "outdoor", "outer", "output", "outside", "oval", "oven", "over", "own", "owner", "oxygen", "oyster", "ozone", "pact", "paddle", "page", "pair", "palace", "palm", "panda", "panel", "panic", "panther", "paper", "parade", "parent", "park", "parrot", "party", "pass", "patch", "path", "patient", "patrol", "pattern", "pause", "pave", "payment", "peace", "peanut", "pear", "peasant", "pelican", "pen", "penalty", "pencil", "people", "pepper", "perfect", "permit", "person", "pet", "phone", "photo", "phrase", "physical", "piano", "picnic", "picture", "piece", "pig", "pigeon", "pill", "pilot", "pink", "pioneer", "pipe", "pistol", "pitch", "pizza", "place", "planet", "plastic", "plate", "play", "please", "pledge", "pluck", "plug", "plunge", "poem", "poet", "point", "polar", "pole", "police", "pond", "pony", "pool", "popular", "portion", "position", "possible", "post", "potato", "pottery", "poverty", "powder", "power", "practice", "praise", "predict", "prefer", "prepare", "present", "pretty", "prevent", "price", "pride", "primary", "print", "priority", "prison", "private", "prize", "problem", "process", "produce", "profit", "program", "project", "promote", "proof", "property", "prosper", "protect", "proud", "provide", "public", "pudding", "pull", "pulp", "pulse", "pumpkin", "punch", "pupil", "puppy", "purchase", "purity", "purpose", "purse", "push", "put", "puzzle", "pyramid", "quality", "quantum", "quarter", "question", "quick", "quit", "quiz", "quote", "rabbit", "raccoon", "race", "rack", "radar", "radio", "rail", "rain", "raise", "rally", "ramp", "ranch", "random", "range", "rapid", "rare", "rate", "rather", "raven", "raw", "razor", "ready", "real", "reason", "rebel", "rebuild", "recall", "receive", "recipe", "record", "recycle", "reduce", "reflect", "reform", "refuse", "region", "regret", "regular", "reject", "relax", "release", "relief", "rely", "remain", "remember", "remind", "remove", "render", "renew", "rent", "reopen", "repair", "repeat", "replace", "report", "require", "rescue", "resemble", "resist", "resource", "response", "result", "retire", "retreat", "return", "reunion", "reveal", "review", "reward", "rhythm", "rib", "ribbon", "rice", "rich", "ride", "ridge", "rifle", "right", "rigid", "ring", "riot", "ripple", "risk", "ritual", "rival", "river", "road", "roast", "robot", "robust", "rocket", "romance", "roof", "rookie", "room", "rose", "rotate", "rough", "round", "route", "royal", "rubber", "rude", "rug", "rule", "run", "runway", "rural", "sad", "saddle", "sadness", "safe", "sail", "salad", "salmon", "salon", "salt", "salute", "same", "sample", "sand", "satisfy", "satoshi", "sauce", "sausage", "save", "say", "scale", "scan", "scare", "scatter", "scene", "scheme", "school", "science", "scissors", "scorpion", "scout", "scrap", "screen", "script", "scrub", "sea", "search", "season", "seat", "second", "secret", "section", "security", "seed", "seek", "segment", "select", "sell", "seminar", "senior", "sense", "sentence", "series", "service", "session", "settle", "setup", "seven", "shadow", "shaft", "shallow", "share", "shed", "shell", "sheriff", "shield", "shift", "shine", "ship", "shiver", "shock", "shoe", "shoot", "shop", "short", "shoulder", "shove", "shrimp", "shrug", "shuffle", "shy", "sibling", "sick", "side", "siege", "sight", "sign", "silent", "silk", "silly", "silver", "similar", "simple", "since", "sing", "siren", "sister", "situate", "six", "size", "skate", "sketch", "ski", "skill", "skin", "skirt", "skull", "slab", "slam", "sleep", "slender", "slice", "slide", "slight", "slim", "slogan", "slot", "slow", "slush", "small", "smart", "smile", "smoke", "smooth", "snack", "snake", "snap", "sniff", "snow", "soap", "soccer", "social", "sock", "soda", "soft", "solar", "soldier", "solid", "solution", "solve", "someone", "song", "soon", "sorry", "sort", "soul", "sound", "soup", "source", "south", "space", "spare", "spatial", "spawn", "speak", "special", "speed", "spell", "spend", "sphere", "spice", "spider", "spike", "spin", "spirit", "split", "spoil", "sponsor", "spoon", "sport", "spot", "spray", "spread", "spring", "spy", "square", "squeeze", "squirrel", "stable", "stadium", "staff", "stage", "stairs", "stamp", "stand", "start", "state", "stay", "steak", "steel", "stem", "step", "stereo", "stick", "still", "sting", "stock", "stomach", "stone", "stool", "story", "stove", "strategy", "street", "strike", "strong", "struggle", "student", "stuff", "stumble", "style", "subject", "submit", "subway", "success", "such", "sudden", "suffer", "sugar", "suggest", "suit", "summer", "sun", "sunny", "sunset", "super", "supply", "supreme", "sure", "surface", "surge", "surprise", "surround", "survey", "suspect", "sustain", "swallow", "swamp", "swap", "swarm", "swear", "sweet", "swift", "swim", "swing", "switch", "sword", "symbol", "symptom", "syrup", "system", "table", "tackle", "tag", "tail", "talent", "talk", "tank", "tape", "target", "task", "taste", "tattoo", "taxi", "teach", "team", "tell", "ten", "tenant", "tennis", "tent", "term", "test", "text", "thank", "that", "theme", "then", "theory", "there", "they", "thing", "this", "thought", "three", "thrive", "throw", "thumb", "thunder", "ticket", "tide", "tiger", "tilt", "timber", "time", "tiny", "tip", "tired", "tissue", "title", "toast", "tobacco", "today", "toddler", "toe", "together", "toilet", "token", "tomato", "tomorrow", "tone", "tongue", "tonight", "tool", "tooth", "top", "topic", "topple", "torch", "tornado", "tortoise", "toss", "total", "tourist", "toward", "tower", "town", "toy", "track", "trade", "traffic", "tragic", "train", "transfer", "trap", "trash", "travel", "tray", "treat", "tree", "trend", "trial", "tribe", "trick", "trigger", "trim", "trip", "trophy", "trouble", "truck", "true", "truly", "trumpet", "trust", "truth", "try", "tube", "tuition", "tumble", "tuna", "tunnel", "turkey", "turn", "turtle", "twelve", "twenty", "twice", "twin", "twist", "two", "type", "typical", "ugly", "umbrella", "unable", "unaware", "uncle", "uncover", "under", "undo", "unfair", "unfold", "unhappy", "uniform", "unique", "unit", "universe", "unknown", "unlock", "until", "unusual", "unveil", "update", "upgrade", "uphold", "upon", "upper", "upset", "urban", "urge", "usage", "use", "used", "useful", "useless", "usual", "utility", "vacant", "vacuum", "vague", "valid", "valley", "valve", "van", "vanish", "vapor", "various", "vast", "vault", "vehicle", "velvet", "vendor", "venture", "venue", "verb", "verify", "version", "very", "vessel", "veteran", "viable", "vibrant", "vicious", "victory", "video", "view", "village", "vintage", "violin", "virtual", "virus", "visa", "visit", "visual", "vital", "vivid", "vocal", "voice", "void", "volcano", "volume", "vote", "voyage", "wage", "wagon", "wait", "walk", "wall", "walnut", "want", "warfare", "warm", "warrior", "wash", "wasp", "waste", "water", "wave", "way", "wealth", "weapon", "wear", "weasel", "weather", "web", "wedding", "weekend", "weird", "welcome", "west", "wet", "whale", "what", "wheat", "wheel", "when", "where", "whip", "whisper", "wide", "width", "wife", "wild", "will", "win", "window", "wine", "wing", "wink", "winner", "winter", "wire", "wisdom", "wise", "wish", "witness", "wolf", "woman", "wonder", "wood", "wool", "word", "work", "world", "worry", "worth", "wrap", "wreck", "wrestle", "wrist", "write", "wrong", "yard", "year", "yellow", "you", "young", "youth", "zebra", "zero", "zone", "zoo"]
        
def winner_save(words, account_extended_private_key, account_extended_public_key, balance_initial, totalReceived_initial, totalSent_initial, txs_initial):
    with open('WINNER_found.txt', 'a') as file:
        file.write(f"Initial Balance Check BTC\n")
        file.write(f"Words: {words}\n")
        file.write(f"Account Extended Private Key: BTC {account_extended_private_key}\n")
        file.write(f"Account Extended Public Key: BTC {account_extended_public_key}\n")
        file.write(f"Balance: {balance_initial}  TotalReceived: {totalReceived_initial} TotalSent: {totalSent_initial} Txs: {txs_initial}\n\n")
        
def found_save_bal(path, caddr, balance_derivationc, totalReceived_derivationc, totalSent_derivationc, txs_derivationc, uaddr, balance_derivationu, totalReceived_derivationu, totalSent_derivationu, txs_derivationu, words, private_key, root_public_key, extended_private_key, root_extended_private_key, compressed_public_key, uncompressed_public_key, wif_private_key, wif_compressed_private_key):
    with open('found_info.txt', 'a') as file:
        file.write(f"\nDerivation Path: {path}\n")
        file.write(f"Compressed Address: {caddr}\n")
        file.write(f"Compressed Balance: {balance_derivationc}  TotalReceived: {totalReceived_derivationc} TotalSent: {totalSent_derivationc} Txs: {txs_derivationc}\n")
        file.write(f"Uncompressed Address: {uaddr}\n")
        file.write(f"Uncompressed Balance: {balance_derivationu}  TotalReceived: {totalReceived_derivationu} TotalSent: {totalSent_derivationu} Txs: {txs_derivationu}\n")
        file.write(f"Mnemonic Words: {words}\n")
        file.write(f"Private Key: {private_key}\n")
        file.write(f"Root Public Key: {root_public_key}\n")
        file.write(f"Extended Private Key: {extended_private_key}\n")
        file.write(f"Root Extended Private Key: {root_extended_private_key}\n")
        file.write(f"Compressed Public Key: {compressed_public_key}\n")
        file.write(f"Uncompressed Public Key: {uncompressed_public_key}\n")
        file.write(f"WIF Private Key: {wif_private_key}\n")
        file.write(f"WIF Compressed Private Key: {wif_compressed_private_key}\n")
        file.write("\n")
        
def found_save_off(path, caddr, uaddr, words, private_key, root_public_key, extended_private_key, root_extended_private_key, compressed_public_key, uncompressed_public_key, wif_private_key, wif_compressed_private_key):
    with open('found_info.txt', 'a') as file:
        file.write(f"\nDerivation Path: {path}\n")
        file.write(f"Compressed Address: {caddr}\n")
        file.write(f"Uncompressed Address: {uaddr}\n")
        file.write(f"Mnemonic Words: {words}\n")
        file.write(f"Private Key: {private_key}\n")
        file.write(f"Root Public Key: {root_public_key}\n")
        file.write(f"Extended Private Key: {extended_private_key}\n")
        file.write(f"Root Extended Private Key: {root_extended_private_key}\n")
        file.write(f"Compressed Public Key: {compressed_public_key}\n")
        file.write(f"Uncompressed Public Key: {uncompressed_public_key}\n")
        file.write(f"WIF Private Key: {wif_private_key}\n")
        file.write(f"WIF Compressed Private Key: {wif_compressed_private_key}\n")
        file.write("\n")
        
class RecoveryThread(QThread):
    recoveryFinished = pyqtSignal(str)

    def __init__(self, div_input, rec_IN, mode, wordlist, update_keys_per_sec, ONLINE_button1):
        super().__init__()
        self.rec_IN = rec_IN
        self.mode = mode
        self.wordlist = wordlist
        self.update_keys_per_sec = update_keys_per_sec
        self.batch_size = 1
        self.ONLINE_button1 = ONLINE_button1
        self.div_input = div_input
        
    def run(self):
        self.timer = QTimer()
        missing_length = self.rec_IN.count('*')
        key_length = len(self.rec_IN)
        allowed_characters = self.wordlist
        missing_letters_master_list = trotter.Amalgams(missing_length, allowed_characters)
        try:
            max_loop_length = len(missing_letters_master_list)
        except OverflowError:
            max_loop_length = sys.maxsize
            if self.mode == 'sequential':
                self.recoveryFinished.emit(f"Warning: Some letters will not be processed in sequential mode because "
                      f"the possible space is too large. Try random mode.")
        start_time = time.time()
        counter = 0
        batch_counter = 0

        with ThreadPoolExecutor() as executor:
            for i in range(max_loop_length):
                if self.mode == 'sequential':
                    potential_key = self.complete_key(self.rec_IN, missing_letters_master_list[i])
                elif self.mode == 'random':
                    potential_key = self.complete_key(self.rec_IN, missing_letters_master_list.random())
                counter += 1
                batch_counter += 1
                self.timer.timeout.connect(self.update_keys_per_sec)
                self.timer.start()
                self.mnemonic_main(potential_key)
                if batch_counter >= self.batch_size:
                    self.recoveryFinished.emit(potential_key)
                    batch_counter = 0
            self.recoveryFinished.emit('Recovery Finished')

    def complete_key(self, rec_IN_string, missing_letters):
        for letter in missing_letters:
            rec_IN_string = rec_IN_string.replace('*', letter, 1)
        return rec_IN_string
            
    def mnemonic_main(self, words):
        if self.ONLINE_button1.isChecked():
            try:
                hdwallet = HDWallet().from_mnemonic(words)
                hdwallet.from_path("m/44'/0'/0'")
                account_extended_private_key = hdwallet.xprivate_key()
                account_extended_public_key = hdwallet.xpublic_key()
                balance_initial, totalReceived_initial, totalSent_initial, txs_initial = team_balance.check_xpub(account_extended_public_key)
                infobtc =f'''                        BITCOIN Mnemonic Words: 
                
        {words}
     
                                        Account Extended Private Key: 
                
        {account_extended_private_key}
     
                                        Account Extended Public Key: 
                
        {account_extended_public_key}
     
                Balance: {balance_initial}  TotalReceived: {totalReceived_initial} TotalSent: {totalSent_initial} Txs: {txs_initial}
            
                '''
                self.recoveryFinished.emit(infobtc)
                if balance_initial > 0 or totalReceived_initial > 0 or totalSent_initial > 0 or txs_initial > 0:
                    self.recoveryFinished.emit("Balance or other important values found in initial Account Extended Public Key.")
                    winner_save(words, account_extended_private_key, account_extended_public_key, balance_initial, totalReceived_initial, totalSent_initial, txs_initial)
                    #derivations = ["m/44'/0'/0'/0", "m/0", "m/0'/0'", "m/0'/0", "m/44'/0'/0'"]
                    derivations = ["m/44'/0'/0'/0"]
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        futures = []
                        for derivation in derivations:
                            for p in range(0, self.div_input):
                                future = executor.submit(process_derivation_on, words, derivation, p)
                                futures.append(future)

                        for future in concurrent.futures.as_completed(futures):
                            derived_info = future.result()
                            if derived_info:
                                path = derived_info["derivation_path"]
                                caddr = derived_info["compressed_address"]
                                uaddr = derived_info["uncompressed_address"]
                                balance_derivationc = derived_info["balance_derivationc"]
                                totalReceived_derivationc = derived_info["totalReceived_derivationc"]
                                totalSent_derivationc = derived_info["totalSent_derivationc"]
                                txs_derivationc = derived_info["txs_derivationc"]
                                balance_derivationu = derived_info["balance_derivationu"]
                                totalReceived_derivationu = derived_info["totalReceived_derivationu"]
                                totalSent_derivationu = derived_info["totalSent_derivationu"]
                                txs_derivationu = derived_info["txs_derivationu"]
                                private_key = derived_info["private_key"]
                                root_public_key = derived_info["root_public_key"]
                                extended_private_key = derived_info["extended_private_key"]
                                root_extended_private_key = derived_info["root_extended_private_key"]
                                compressed_public_key = derived_info["compressed_public_key"]
                                uncompressed_public_key = derived_info["uncompressed_public_key"]
                                wif_private_key = derived_info["wif_private_key"]
                                wif_compressed_private_key = derived_info["wif_compressed_private_key"]
                                scaninfo = f'''

    Derivation Path: {path}
    Compressed Address: {caddr}
    Compressed Balance: {balance_derivationc}  TotalReceived: {totalReceived_derivationc} TotalSent: {totalSent_derivationc} Txs: {txs_derivationc}

    Uncompressed Address: {uaddr}
    Uncompressed Balance: {balance_derivationu}  TotalReceived: {totalReceived_derivationu} TotalSent: {totalSent_derivationu} Txs: {txs_derivationu}

    Mnemonic words: {words}
    Private Key: {private_key}
    Root Public Key: {root_public_key}
    Extended Private Key: {extended_private_key}
    Root Extended Private Key: {root_extended_private_key}
    Compressed Public Key: {compressed_public_key}
    Uncompressed Public Key: {uncompressed_public_key}
    WIF Private Key: {wif_private_key}
    WIF Compressed Private Key: {wif_compressed_private_key}
    '''
                                self.recoveryFinished.emit(scaninfo)

            except Exception as e:
                self.recoveryFinished.emit(f"Error occurred in mnemonic_main: {str(e)}")
                pass

        else:
            try:
                hdwallet = HDWallet().from_mnemonic(words)
                #derivations = ["m/44'/0'/0'/0", "m/0", "m/0'/0'", "m/0'/0", "m/44'/0'/0'"]
                derivations = ["m/44'/0'/0'/0"]
                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = []
                    for derivation in derivations:
                        for p in range(0, self.div_input):
                            future = executor.submit(process_derivation_off, words, derivation, p)
                            futures.append(future)

                    for future in concurrent.futures.as_completed(futures):
                        derived_info = future.result()
                        if derived_info:
                            path = derived_info["derivation_path"]
                            caddr = derived_info["compressed_address"]
                            uaddr = derived_info["uncompressed_address"]
                            private_key = derived_info["private_key"]
                            root_public_key = derived_info["root_public_key"]
                            extended_private_key = derived_info["extended_private_key"]
                            root_extended_private_key = derived_info["root_extended_private_key"]
                            compressed_public_key = derived_info["compressed_public_key"]
                            uncompressed_public_key = derived_info["uncompressed_public_key"]
                            wif_private_key = derived_info["wif_private_key"]
                            wif_compressed_private_key = derived_info["wif_compressed_private_key"]
                            scaninfo = f'''

    Derivation Path: {path}
    Compressed Address: {caddr}
    Uncompressed Address: {uaddr}
    Mnemonic words: {words}
    Private Key: {private_key}
    Root Public Key: {root_public_key}
    Extended Private Key: {extended_private_key}
    Root Extended Private Key: {root_extended_private_key}
    Compressed Public Key: {compressed_public_key}
    Uncompressed Public Key: {uncompressed_public_key}
    WIF Private Key: {wif_private_key}
    WIF Compressed Private Key: {wif_compressed_private_key}
'''
                            self.recoveryFinished.emit(scaninfo)

            except Exception as e:
                self.recoveryFinished.emit(f"Error occurred in mnemonic_main: {str(e)}")
                pass

class GUIInstance(QMainWindow):
    def __init__(self):
        super().__init__()
        self.num = 0
        self.counter = 0
        self.start_time = 0
        self.wordlist = wordlist
        self.addfind = addfind
        self.recovery_thread = None
        self.executor = ThreadPoolExecutor()
        self.scanning = False
        self.initUI()

    def process_derivation_on(self, words, derivation, p):
	    try:
	        hdwallet = HDWallet().from_mnemonic(words)
	        wallet = hdwallet.from_mnemonic(words)
	        path = f"{derivation}/{p}"
	        hdwallet.from_path(path=path)
	        path_read = hdwallet.path()
	        private_key = hdwallet.private_key()
	        root_public_key = hdwallet.xpublic_key()
	        extended_private_key = hdwallet.xprivate_key()
	        root_extended_private_key = hdwallet.root_xprivate_key()
	        compressed_public_key = hdwallet.public_key(compressed=True)
	        uncompressed_public_key = '04' + hdwallet.public_key(compressed=False)
	        compressed_address_bytes = hashlib.new('ripemd160', hashlib.sha256(bytes.fromhex(compressed_public_key)).digest()).digest()
	        compressed_address = base58.b58encode_check(b'\x00' + compressed_address_bytes)
	        uncompressed_address_bytes = hashlib.new('ripemd160', hashlib.sha256(bytes.fromhex(uncompressed_public_key)).digest()).digest()
	        uncompressed_address = base58.b58encode_check(b'\x00' + uncompressed_address_bytes)
	        wif_private_key = base58.b58encode_check(b'\x80' + binascii.unhexlify(private_key)).decode()
	        wif_compressed_private_key = base58.b58encode_check(b'\x80' + binascii.unhexlify(private_key) + b'\x01').decode()
	        caddr = compressed_address.decode('utf-8')
	        uaddr = uncompressed_address.decode('utf-8')
	        balance_derivationc, totalReceived_derivationc, totalSent_derivationc, txs_derivationc = team_balance.check_balance(caddr)
	        balance_derivationu, totalReceived_derivationu, totalSent_derivationu, txs_derivationu = team_balance.check_balance(uaddr)
	        derived_info = {
	            "derivation_path": path,
	            "compressed_address": caddr,
	            "uncompressed_address": uaddr,
	            "balance_derivationc": balance_derivationc,
	            "totalReceived_derivationc": totalReceived_derivationc,
	            "totalSent_derivationc": totalSent_derivationc,
	            "txs_derivationc": txs_derivationc,
	            "balance_derivationu": balance_derivationu,
	            "totalReceived_derivationu": totalReceived_derivationu,
	            "totalSent_derivationu": totalSent_derivationu,
	            "txs_derivationu": txs_derivationu,
	            "mnemonic_words": words,
	            "private_key": private_key,
	            "root_public_key": root_public_key,
	            "extended_private_key": extended_private_key,
	            "root_extended_private_key": root_extended_private_key,
	            "compressed_public_key": compressed_public_key,
	            "uncompressed_public_key": uncompressed_public_key,
	            "wif_private_key": wif_private_key,
	            "wif_compressed_private_key": wif_compressed_private_key
	        }
	        if int(balance_derivationc) > 0 or int(txs_derivationc) > 0 or int(balance_derivationu) > 0 or int(txs_derivationu) > 0:
	            found_save_bal(path, caddr, balance_derivationc, totalReceived_derivationc, totalSent_derivationc, txs_derivationc, uaddr, balance_derivationu, totalReceived_derivationu, totalSent_derivationu, txs_derivationu, words, private_key, root_public_key, extended_private_key, root_extended_private_key, compressed_public_key, uncompressed_public_key, wif_private_key, wif_compressed_private_key)
	        if self.use_telegram_credentials_checkbox.isChecked():
	            self.send_to_telegram(derived_info)
	        elif self.use_discord_credentials_checkbox.isChecked():
	            self.send_to_discord(derived_info)

	        return derived_info


	    except Exception as e:
	        self.recoveryFinished.emit(f'Error occurred in derivation {derivation}/{p}: {str(e)}')
	        return None
    def process_derivation_off(self, words, derivation, p):
	    try:
	        hdwallet = HDWallet().from_mnemonic(words)
	        path = f"{derivation}/{p}"
	        hdwallet.from_path(path=path)
	        path_read = hdwallet.path()
	        private_key = hdwallet.private_key()
	        root_public_key = hdwallet.xpublic_key()
	        extended_private_key = hdwallet.xprivate_key()
	        root_extended_private_key = hdwallet.root_xprivate_key()
	        compressed_public_key = hdwallet.public_key(compressed=True)
	        uncompressed_public_key = '04' + hdwallet.public_key(compressed=False)
	        compressed_address_bytes = hashlib.new('ripemd160', hashlib.sha256(bytes.fromhex(compressed_public_key)).digest()).digest()
	        compressed_address = base58.b58encode_check(b'\x00' + compressed_address_bytes)
	        uncompressed_address_bytes = hashlib.new('ripemd160', hashlib.sha256(bytes.fromhex(uncompressed_public_key)).digest()).digest()
	        uncompressed_address = base58.b58encode_check(b'\x00' + uncompressed_address_bytes)
	        wif_private_key = base58.b58encode_check(b'\x80' + binascii.unhexlify(private_key)).decode()
	        wif_compressed_private_key = base58.b58encode_check(b'\x80' + binascii.unhexlify(private_key) + b'\x01').decode()
	        caddr = compressed_address.decode('utf-8')
	        uaddr = uncompressed_address.decode('utf-8')
	        derived_info = {
	            "derivation_path": path,
	            "compressed_address": caddr,
	            "uncompressed_address": uaddr,
	            "mnemonic_words": words,
	            "private_key": private_key,
	            "root_public_key": root_public_key,
	            "extended_private_key": extended_private_key,
	            "root_extended_private_key": root_extended_private_key,
	            "compressed_public_key": compressed_public_key,
	            "uncompressed_public_key": uncompressed_public_key,
	            "wif_private_key": wif_private_key,
	            "wif_compressed_private_key": wif_compressed_private_key
	        }
	        if caddr in addfind or uaddr in addfind:
	            found_save_off(path, caddr, uaddr, words, private_key, root_public_key, extended_private_key, root_extended_private_key, compressed_public_key, uncompressed_public_key, wif_private_key, wif_compressed_private_key)
	        elif self.use_telegram_credentials_checkbox.isChecked():
	            self.send_to_telegram(derived_info)
	        elif self.use_discord_credentials_checkbox.isChecked():
	            self.send_to_discord(derived_info)
	        elif self.win_checkbox.isChecked():
	            winner_dialog = win_gui.WinnerDialog(words, self)
	            winner_dialog.exec()
	        return derived_info
	        
	    except Exception as e:
	        self.recoveryFinished.emit(f'Error occurred in derivation {derivation}/{p}: {str(e)}')
	        return None
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.add_count_label = QLabel(self.count_addresses(), objectName="count_addlabel", alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(self.add_count_label)
        line1_label = QLabel('For every 1 xpub roughly 2,147,483,647 Address are checked Online mode Only')
        line1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line1_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #E7481F;")
        main_layout.addWidget(line1_label)
        line2_label = QLabel('Pick Ammount of words to Check Online or OffLine. Many different Languages to choose from. Amount Derivations does not do much for Online Checking as the XPub is used,  works better for Offline scanning for checking against your Database file.')
        line2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line2_label.setStyleSheet("font-size: 14px; color: #E7481F;")
        main_layout.addWidget(line2_label)
        radio_button_layout = QHBoxLayout()
        ammount_words_label = QLabel('Amount of words:')
        ammount_words_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #E7481F;")
        ammount_words_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        radio_button_layout.addWidget(ammount_words_label)
        self.ammount_words = QComboBox()
        self.ammount_words.addItems(['random', '12', '15', '18', '21', '24'])
        self.ammount_words.setCurrentIndex(1)
        radio_button_layout.addWidget(self.ammount_words)
        lang_words_label = QLabel('Chose Language:')
        lang_words_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #E7481F;")
        lang_words_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        radio_button_layout.addWidget(lang_words_label)
        self.lang_words = QComboBox()
        self.lang_words.addItems(['random', 'english', 'french', 'italian', 'spanish', 'chinese_simplified', 'chinese_traditional', 'japanese', 'korean'])
        self.lang_words.setCurrentIndex(1)
        radio_button_layout.addWidget(self.lang_words)
        div_label = QLabel('Choose Amount Derivations:')
        div_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #E7481F;")
        div_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        radio_button_layout.addWidget(div_label)
        self.derivation_choice = QComboBox()
        self.derivation_choice.addItems(['1', '2', '5', '10', '20', '50', '100'])
        self.derivation_choice.setCurrentIndex(0)
        radio_button_layout.addWidget(self.derivation_choice)

        self.win_checkbox = QCheckBox("Stop if found")
        self.win_checkbox.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Ticks can be removed to search for single type or mutiple types of Bitcoin Address. Removing some will increase speed. Address not selected we not be searched </span>')
        self.win_checkbox.setChecked(True)
        radio_button_layout.addWidget(self.win_checkbox)
        start_button = QPushButton("Start", self)
        start_button.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        start_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start scanning </span>')
        start_button.clicked.connect(self.start)
        start_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        start_button.setFixedWidth(300)
        radio_button_layout.addWidget(start_button)
        stop_button = QPushButton("Stop", self)
        stop_button.setStyleSheet(
            "QPushButton { font-size: 12pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 12pt; background-color: #5D6062; color: white; }"
        )
        stop_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Stop scanning </span>')
        stop_button.clicked.connect(self.stop)
        stop_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back))
        stop_button.setFixedWidth(300)
        radio_button_layout.addWidget(stop_button)
        custom_phrase_layout = QHBoxLayout()
        custom_phrase_label = QLabel('Custom Phrase:')
        custom_phrase_layout.addWidget(custom_phrase_label)
        self.custom_phrase_edit = QLineEdit()
        self.custom_phrase_edit.setPlaceholderText('Type here your Mnemonic to Check')
        custom_phrase_layout.addWidget(self.custom_phrase_edit)
        enter_button = QPushButton('Enter')
        enter_button.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        enter_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Mnemonic to Check </span>')
        enter_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        enter_button.setFixedWidth(300)
        enter_button.clicked.connect(self.enter)
        custom_phrase_layout.addWidget(enter_button)

        start_button_read = QPushButton("Read File of Menmonic Words", self)
        start_button_read.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        start_button_read.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start scanning </span>')
        start_button_read.clicked.connect(self.read_mnms)
        start_button_read.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        start_button_read.setFixedWidth(400)
        custom_phrase_layout.addWidget(start_button_read)

        main_layout1 = QVBoxLayout()
        welcome_label1 = QLabel('Recovery Mnemonic Scanner Type Mnemonic HERE  (**** MAX 5 MISSING ****) press Forward to start and stop or Random to start and stop Recovery')
        welcome_label1.setStyleSheet("font-size: 18px; font-weight: bold; color: #E7481F;")
        welcome_label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout1.addWidget(welcome_label1)

        custom_phrase_layout1 = QHBoxLayout()
        self.ONLINE_button1 = QRadioButton('ONLINE')
        self.ONLINE_button1.setChecked(True)
        self.OFFLINE_button1 = QRadioButton('OFFLINE')
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.ONLINE_button1)
        self.button_group.addButton(self.OFFLINE_button1)
        custom_phrase_layout1.addWidget(self.ONLINE_button1)
        custom_phrase_layout1.addWidget(self.OFFLINE_button1)
        self.txt_input_word = QLineEdit("abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon *")
        custom_phrase_layout1.addWidget(self.txt_input_word)
        div_label1 = QLabel('Choose Amount Derivations:')
        div_label1.setStyleSheet("font-size: 12pt; font-weight: bold; color: #E7481F;")
        div_label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        custom_phrase_layout1.addWidget(div_label1)

        self.derivation_choice1 = QComboBox()
        self.derivation_choice1.addItems(['1', '2', '5', '10', '20', '50', '100'])
        self.derivation_choice1.setCurrentIndex(0)
        custom_phrase_layout1.addWidget(self.derivation_choice1)
        forward_button = QPushButton('Forward (Start/Stop)')
        forward_button.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        forward_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start scanning Forward </span>')
        forward_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        forward_button.setFixedWidth(300)
        forward_button.clicked.connect(lambda: self.start_recovery_MNEMO_S())
        custom_phrase_layout1.addWidget(forward_button)
        random_button = QPushButton('Random (Start/Stop)')
        random_button.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        random_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start Random scanning </span>')
        random_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        random_button.setFixedWidth(300)
        random_button.clicked.connect(lambda: self.start_recovery_MNEMO_R())
        custom_phrase_layout1.addWidget(random_button)
        keys_layout = QHBoxLayout()
        self.ONLINE_button = QRadioButton('ONLINE')
        self.ONLINE_button.setChecked(True)
        self.OFFLINE_button = QRadioButton('OFFLINE')
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.ONLINE_button)
        self.button_group.addButton(self.OFFLINE_button)
        keys_layout.addWidget(self.ONLINE_button)
        keys_layout.addWidget(self.OFFLINE_button)
        found_keys_scanned_label = QLabel('Found')
        self.found_keys_scanned_edit = QLineEdit('0')
        self.found_keys_scanned_edit.setReadOnly(True)
        keys_layout.addWidget(found_keys_scanned_label)
        keys_layout.addWidget(self.found_keys_scanned_edit)
        total_keys_scanned_label = QLabel('Total keys scanned:')
        self.total_keys_scanned_edit = QLineEdit('0')
        self.total_keys_scanned_edit.setReadOnly(True)
        keys_layout.addWidget(total_keys_scanned_label)
        keys_layout.addWidget(self.total_keys_scanned_edit)
        keys_per_sec_label = QLabel('Keys per second:')
        self.keys_per_sec_edit = QLineEdit()
        self.keys_per_sec_edit.setReadOnly(True)
        keys_layout.addWidget(keys_per_sec_label)
        keys_layout.addWidget(self.keys_per_sec_edit)
        
        main_layout.addLayout(radio_button_layout)
        main_layout.addLayout(keys_layout)
        main_layout.addLayout(custom_phrase_layout)
        main_layout.addLayout(main_layout1)
        main_layout.addLayout(custom_phrase_layout1)
        
        self.consoleWindow = ConsoleWindow(self)
        main_layout.addWidget(self.consoleWindow)

        icon_size = QSize(32, 32)
        icontel = QIcon(QPixmap(TEL_ICON))
        icondis = QIcon(QPixmap(DIS_ICON))

        self.telegram_mode_button = QPushButton(self)
        self.telegram_mode_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Enter Custom Telegram Credentials Settings .</span>')
        self.telegram_mode_button.setStyleSheet("font-size: 12pt;")
        self.telegram_mode_button.setIconSize(icon_size)
        self.telegram_mode_button.setIcon(icontel)
        self.telegram_mode_button.clicked.connect(self.open_telegram_settings)
        self.telegram_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back))
        self.use_telegram_credentials_checkbox = QCheckBox("Use Custom Telegram Credentials")
        self.use_telegram_credentials_checkbox.setChecked(False)

        self.discord_mode_button = QPushButton(self)
        self.discord_mode_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Enter Custom Discord Credentials Settings .</span>')
        self.discord_mode_button.setStyleSheet("font-size: 12pt;")
        self.discord_mode_button.setIconSize(icon_size)
        self.discord_mode_button.setIcon(icondis)
        self.discord_mode_button.clicked.connect(self.open_discord_settings)
        self.discord_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back))
        self.use_discord_credentials_checkbox = QCheckBox("Use Custom Discord Credentials")
        self.use_discord_credentials_checkbox.setChecked(False)

        self.load_mode_button = QPushButton("Load New Database from File",self)
        self.load_mode_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Load New Database from File.</span>')
        self.load_mode_button.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        self.load_mode_button.clicked.connect(self.onOpen)
        
        custom_credentials_layout = QHBoxLayout()
        custom_credentials_layout.addWidget(self.telegram_mode_button)
        custom_credentials_layout.addWidget(self.use_telegram_credentials_checkbox)
        custom_credentials_layout.addWidget(self.discord_mode_button)
        custom_credentials_layout.addWidget(self.use_discord_credentials_checkbox)
        custom_credentials_layout.addWidget(self.load_mode_button)
        main_layout.addLayout(custom_credentials_layout)

    def start_recovery_MNEMO_S(self):
        if self.recovery_thread and self.recovery_thread.isRunning():
            self.recovery_thread.terminate()
            self.scanning = False
        else:
            div_input = int(self.derivation_choice1.currentText())
            rec_IN = self.txt_input_word.text()
            mode = 'sequential'
            self.recovery_thread = RecoveryThread(div_input, rec_IN, mode, self.wordlist, self.update_keys_per_sec, self.ONLINE_button1)
            self.recovery_thread.recoveryFinished.connect(self.handle_recovery_result)
            self.recovery_thread.start()
            self.scanning = True

    def start_recovery_MNEMO_R(self):
        if self.recovery_thread and self.recovery_thread.isRunning():
            self.recovery_thread.terminate()
            self.scanning = False
        else:
            div_input = int(self.derivation_choice1.currentText())
            rec_IN = self.txt_input_word.text()
            mode = 'random'
            self.recovery_thread = RecoveryThread(div_input, rec_IN, mode, self.wordlist, self.update_keys_per_sec, self.ONLINE_button1)
            self.recovery_thread.recoveryFinished.connect(self.handle_recovery_result)
            self.recovery_thread.start()
            self.scanning = True

    def handle_recovery_result(self, result):
        if result == 'Recovery Finished':
            QMessageBox.information(self, 'Recovery Finished', 'Key recovery process finished.')
        else:
            self.consoleWindow.append_output(result)

    def read_mnms(self):
        self.word_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_next_mnm)
        self.timer.start(0)
        self.start_time = time.time()
        self.timer.timeout.connect(self.update_keys_per_sec)

    def process_next_mnm(self):
        if self.word_index < len(mylist):
            words = mylist[self.word_index]
            self.mnemonic_btc(words)
            self.word_index += 1
        else:
            self.timer.stop()
            
    def update_keys_per_sec(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time == 0:
            keys_per_sec = 0
        else:
            keys_per_sec = self.counter / elapsed_time
        keys_per_sec = round(keys_per_sec, 2)
        self.keys_per_sec_edit.setText(str(keys_per_sec))
        self.start_time = time.time()
        total_keys_scanned = int(self.total_keys_scanned_edit.text()) + self.counter
        self.total_keys_scanned_edit.setText(str(total_keys_scanned))
        self.counter = 0

    def closeEvent(self, event):
        if self.recovery_thread and self.recovery_thread.isRunning():
            self.recovery_thread.terminate()
        event.accept()
        
    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_keys_per_sec)
        self.timer.timeout.connect(self.generate_mnemonic)
        self.scanning = True
        self.timer.start()
        
    def stop(self):
        if self.timer.isActive():
            self.scanning = False
            self.timer.stop()
    
    def enter(self):
        words = self.custom_phrase_edit.text()
        self.mnemonic_btc(words)
        self.counter += 1
        
    def error_Result(self, message_error):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setText(message_error)
        ok_button = QPushButton("OK")
        msg_box.addButton(ok_button, QMessageBox.ButtonRole.AcceptRole)
        msg_box.exec()

    def onOpen(self):
        global addfind, BTC_BF_FILE
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "BF Files (*.bf);;Text Files (*.txt)"
        )

        if not filePath:
            return

        try:
            if filePath.endswith(".bf"):
                with open(filePath, "rb") as fp:
                    addfind = BloomFilter.load(fp)
            elif filePath.endswith(".txt"):
                with open(filePath, "r") as file:
                    addfind = file.read().split()
            else:
                raise ValueError("Unsupported file type")
            
            BTC_BF_FILE = filePath
            
        except Exception as e:
            error_message = f"Error loading file: {str(e)}"
            QMessageBox.critical(self, "Error", error_message)
            return

        success_message = f"File loaded: {filePath}"
        QMessageBox.information(self, "File Loaded", success_message)

        self.add_count_label.setText(self.count_addresses(BTC_BF_FILE))

    def exit_app(self):
        QApplication.quit()

    def open_telegram_settings(self):
        settings_dialog = telegram_gui.Settings_telegram_Dialog(self)
        settings_dialog.exec()
    
    def open_discord_settings(self):
        settings_dialog = discord_gui.Settings_discord_Dialog(self)
        settings_dialog.exec()

    def count_addresses(self, btc_bf_file=None):
        if btc_bf_file is None:
            btc_bf_file = BTC_BF_FILE       
        try:
            last_updated = os.path.getmtime(BTC_BF_FILE)
            last_updated_datetime = datetime.datetime.fromtimestamp(last_updated)
            now = datetime.datetime.now()
            delta = now - last_updated_datetime

            if delta < datetime.timedelta(days=1):
                hours, remainder = divmod(delta.seconds, 3600)
                minutes = remainder // 60

                time_units = []

                if hours > 0:
                    time_units.append(f"{hours} {'hour' if hours == 1 else 'hours'}")

                if minutes > 0:
                    time_units.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")

                time_str = ', '.join(time_units)

                if time_units:
                    message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses. The database is <b>{time_str}</b> old.'
                else:
                    message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses. The database is <b>less than a minute</b> old.'
            elif delta < datetime.timedelta(days=2):
                hours, remainder = divmod(delta.seconds, 3600)
                minutes = remainder // 60

                time_str = f'1 day'

                if hours > 0:
                    time_str += f', {hours} {"hour" if hours == 1 else "hours"}'

                if minutes > 0:
                    time_str += f', {minutes} {"minute" if minutes == 1 else "minutes"}'

                message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses. The database is <b>{time_str}</b> old.'
            else:
                message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses. The database is <b>{delta.days} days</b> old.'
        except FileNotFoundError:
            message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses.'

        return message

    def send_to_discord(self, text):
        settings = self.load_config()  # Load settings from config.json
        webhook_url = settings.get("Discord", {}).get("webhook_url", "").strip()
        headers = {'Content-Type': 'application/json'}

        payload = {
            'content': text
        }

        try:
            response = requests.post(webhook_url, json=payload, headers=headers)

            if response.status_code == 204:
                print('Message sent to Discord successfully!')
            else:
                print(f'Failed to send message to Discord. Status Code: {response.status_code}')
        except Exception as e:
            print(f'Error sending message to Discord: {str(e)}')

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def send_to_telegram(self, text):
        settings = self.load_config()  # Load settings from config.json
        apiToken = settings.get("Telegram", {}).get("token", "").strip()
        chatID = settings.get("Telegram", {}).get("chatid", "").strip()

        if not apiToken or not chatID:
            token_message = "No token or ChatID found in CONFIG_FILE"
            QMessageBox.information(self, "No token or ChatID", token_message)
            return

        apiURL = f"https://api.telegram.org/bot{apiToken}/sendMessage"

        try:
            response = requests.post(apiURL, json={"chat_id": chatID, "text": text})
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            error_message = f"HTTP Error: {errh}"
            QMessageBox.critical(self, "Error", error_message)
        except Exception as e:
            error_message = f"Telegram error: {str(e)}"
            QMessageBox.critical(self, "Error", error_message)
    
    def generate_mnemonic(self):
        if self.timer.isActive():
            if self.lang_words.currentText() == 'random':
                lang = random.choice(['english', 'french', 'italian', 'spanish', 'chinese_simplified', 'chinese_traditional', 'japanese', 'korean'])
            else:
                lang = self.lang_words.currentText()
            
            if self.ammount_words.currentText() == 'random':
                word_length = random.choice([12, 15, 18, 21, 24])
            else:
                word_length = int(self.ammount_words.currentText())
            
            strengths = {
                12: 128,
                15: 160,
                18: 192,
                21: 224,
                24: 256
            }
            strength = strengths[word_length]
            mnemonic = Mnemonic(lang)
            words = mnemonic.generate(strength=strength)
            self.mnemonic_btc(words)
            self.counter += 1

    def mnemonic_btc(self, words):
	    found = int(self.found_keys_scanned_edit.text())
	    if self.ONLINE_button.isChecked():
	        try:
	            hdwallet = HDWallet().from_mnemonic(words)
	            hdwallet.from_path("m/44'/0'/0'")
	            account_extended_private_key = hdwallet.xprivate_key()
	            account_extended_public_key = hdwallet.xpublic_key()
	            balance_initial, totalReceived_initial, totalSent_initial, txs_initial = team_balance.check_xpub(account_extended_public_key)
	            infobtc = f'''BITCOIN Mnemonic Words: 
	{words}
	Account Extended Private Key: 
	{account_extended_private_key}
	Account Extended Public Key: 
	{account_extended_public_key}

	Balance: {balance_initial}  TotalReceived: {totalReceived_initial} TotalSent: {totalSent_initial} Txs: {txs_initial}
	'''
	            self.consoleWindow.append_output(infobtc)
	            if balance_initial > 0 or totalReceived_initial > 0 or totalSent_initial > 0 or txs_initial > 0:
	                found += 1
	                self.found_keys_scanned_edit.setText(str(found))
	                winner_save(words, account_extended_private_key, account_extended_public_key, balance_initial, totalReceived_initial, totalSent_initial, txs_initial)
	                derivations = ["m/44'/0'/0'/0"]
	                div_input = int(self.derivation_choice.currentText())
	                with ThreadPoolExecutor(max_workers=10) as executor:
	                    futures = []
	                    for derivation in derivations:
	                        for p in range(0, div_input):
	                            future = executor.submit(self.process_derivation_on, words, derivation, p)
	                            futures.append(future)

	                    for future in concurrent.futures.as_completed(futures):
	                        derived_info = future.result()
	                        if derived_info:
	                            path = derived_info["derivation_path"]
	                            caddr = derived_info["compressed_address"]
	                            uaddr = derived_info["uncompressed_address"]
	                            balance_derivationc = derived_info["balance_derivationc"]
	                            totalReceived_derivationc = derived_info["totalReceived_derivationc"]
	                            totalSent_derivationc = derived_info["totalSent_derivationc"]
	                            txs_derivationc = derived_info["txs_derivationc"]
	                            balance_derivationu = derived_info["balance_derivationu"]
	                            totalReceived_derivationu = derived_info["totalReceived_derivationu"]
	                            totalSent_derivationu = derived_info["totalSent_derivationu"]
	                            txs_derivationu = derived_info["txs_derivationu"]
	                            private_key = derived_info["private_key"]
	                            root_public_key = derived_info["root_public_key"]
	                            extended_private_key = derived_info["extended_private_key"]
	                            root_extended_private_key = derived_info["root_extended_private_key"]
	                            compressed_public_key = derived_info["compressed_public_key"]
	                            uncompressed_public_key = derived_info["uncompressed_public_key"]
	                            wif_private_key = derived_info["wif_private_key"]
	                            wif_compressed_private_key = derived_info["wif_compressed_private_key"]

	                            if int(balance_derivationc) > 0 or int(txs_derivationc) > 0 or int(balance_derivationu) > 0 or int(txs_derivationu) > 0:
	                                found += 1
	                                self.found_keys_scanned_edit.setText(str(found))
	                                found_save_bal(path, caddr, balance_derivationc, totalReceived_derivationc, totalSent_derivationc, txs_derivationc, uaddr, balance_derivationu, totalReceived_derivationu, totalSent_derivationu, txs_derivationu, words, private_key, root_public_key, extended_private_key, root_extended_private_key, compressed_public_key, uncompressed_public_key, wif_private_key, wif_compressed_private_key)
	                            if self.use_telegram_credentials_checkbox.isChecked():
	                                self.send_to_telegram(derived_info)
	                            if self.use_discord_credentials_checkbox.isChecked():
	                                self.send_to_discord(derived_info)
	                            if self.win_checkbox.isChecked():
	                                winner_dialog = win_gui.WinnerDialog(words, self)
	                                winner_dialog.exec()
	        except Exception as e:
	            message_error = f'Error occurred in mnemonic_btc: {str(e)}'
	            self.error_Result(message_error)
	            pass
	    else:
	        try:
	            hdwallet = HDWallet().from_mnemonic(words)
	            derivations = ["m/44'/0'/0'/0"]
	            div_input = int(self.derivation_choice.currentText())
	            with ThreadPoolExecutor(max_workers=10) as executor:
	                futures = []
	                for derivation in derivations:
	                    for p in range(0, div_input):
	                        future = executor.submit(self.process_derivation_off, words, derivation, p)
	                        futures.append(future)

	                for future in concurrent.futures.as_completed(futures):
	                    derived_info = future.result()
	                    if derived_info:
	                        path = derived_info["derivation_path"]
	                        caddr = derived_info["compressed_address"]
	                        uaddr = derived_info["uncompressed_address"]
	                        private_key = derived_info["private_key"]
	                        root_public_key = derived_info["root_public_key"]
	                        extended_private_key = derived_info["extended_private_key"]
	                        root_extended_private_key = derived_info["root_extended_private_key"]
	                        compressed_public_key = derived_info["compressed_public_key"]
	                        uncompressed_public_key = derived_info["uncompressed_public_key"]
	                        wif_private_key = derived_info["wif_private_key"]
	                        wif_compressed_private_key = derived_info["wif_compressed_private_key"]
	                        scaninfo = f'''Derivation Path: {path}
	Compressed Address: {caddr}
	Uncompressed Address: {uaddr}
	Mnemonic words: {words}
	Private Key: {private_key}
	Root Public Key: {root_public_key}
	Extended Private Key: {extended_private_key}
	Root Extended Private Key: {root_extended_private_key}
	Compressed Public Key: {compressed_public_key}
	Uncompressed Public Key: {uncompressed_public_key}
	WIF Private Key: {wif_private_key}
	WIF Compressed Private Key: {wif_compressed_private_key}
	'''
	                        self.consoleWindow.append_output(scaninfo)

	                        if caddr in addfind or uaddr in addfind:
	                            found += 1
	                            self.found_keys_scanned_edit.setText(str(found))
	                            found_save_off(path, caddr, uaddr, words, private_key, root_public_key, extended_private_key, root_extended_private_key, compressed_public_key, uncompressed_public_key, wif_private_key, wif_compressed_private_key)
	                        if self.use_telegram_credentials_checkbox.isChecked():
	                            self.send_to_telegram(scaninfo)
	                        if self.use_discord_credentials_checkbox.isChecked():
	                            self.send_to_discord(scaninfo)
	                        if self.win_checkbox.isChecked():
	                            winner_dialog = win_gui.WinnerDialog(words, self)
	                            winner_dialog.exec()

	        except Exception as e:
	            self.recoveryFinished.emit(f"Error occurred in mnemonic_main: {str(e)}")
	            pass