import os
import asyncio
import http.server
import threading
from highrise import BaseBot, User, Position
from highrise.models import SessionMetadata, CurrencyItem

# ==========================
# SIMULATION DE PORT POUR RENDER GRATUIT
# ==========================

def run_fake_server():
    # Render donne un port dans les variables (souvent 10000), sinon on prend 10000
    port = int(os.environ.get("PORT", 10000))
    server_address = ('0.0.0.0', port)
    try:
        httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
        print(f"🌍 Faux serveur Web activé sur le port {port} pour tromper Render.")
        httpd.serve_forever()
    except OSError:
        print(f"⚠️ Le port {port} est déjà utilisé. En attente de la fermeture de l'ancien bot...")

# On lance le faux serveur web dans un fil secondaire (thread) pour ne pas bloquer le bot
threading.Thread(target=run_fake_server, daemon=True).start()

# ==========================
# CONFIGURATION DU BOT
# ==========================
BOT_USERNAME = "leviae"

OWNERS = ["65592020383c55ed5c45aabd"]
MODERATORS = ["65592020383c55ed5c45aabd"]

EMOTES = {
    "swagbounce": "dance-swagbounce", "duckwalk": "dance-duckwalk", "pennywise": "dance-pennywise",
    "floorsleeping": "idle-floorsleeping", "sexy": "dance-sexy", "laidback": "sit-idle-laidBack",
    "ghostidle": "emote-ghost-idle", "annoyed": "idle-loop-annoyed", "touch": "dance-touch",
    "jinglebell": "dance-jinglebell", "space": "idle-space", "metal": "dance-metal",
    "flex": "emoji-flex", "orangejustice": "dance-orangejustice", "shy2": "emote-shy2",
    "blowkisses": "emote-blowkisses", "stargazer": "emote-stargazer", "knocscreen": "emote-knocking-screen",
    "curtsy": "emote-curtsy", "slap": "emote-slap", "twerk": "dance-twerk", "singing": "idle_singing",
    "swinging": "idle-dance-swinging", "kawai": "dance-kawai", "pose9": "emote-pose9",
    "tiktok9": "dance-tiktok9", "floss": "dance-floss", "breakdance": "dance-breakdance",
    "wild": "dance-wild", "hipshake": "dance-hipshake", "griddy": "dance-griddy",
    "shrink": "emote-shrink", "lust": "emote-lust", "spiritual": "dance-spiritual",
    "martialartist": "dance-martial-artist", "hero": "emote-hero", "tiktok2": "dance-tiktok2",
    "popularvibe": "dance-popularvibe", "headball": "emote-headball", "trueheart": "dance-true-heart",
    "cursing": "emoji-cursing", "mine": "dance-mine", "robotic": "dance-robotic",
    "graceful": "emote-graceful", "meditate": "emote-meditate-idle", "frollicking": "emote-frollicking",
    "ballet": "dance-ballet", "woah": "dance-woah", "shuffle": "dance-shuffle", "frog": "emote-frog",
    "lying": "emoji-lying", "laughing2": "emote-laughing2", "boxer": "emote-boxer",
    "tiktok10": "dance-tiktok10", "attention": "emote-attention", "dab": "emote-dab",
    "timejump": "emote-timejump", "puppet": "emote-puppet", "gagging": "emoji-gagging",
    "aerobics": "dance-aerobics", "guitar": "idle-guitar", "tiktok7": "idle-dance-tiktok7",
    "tiktok11": "dance-tiktok11", "tapdance": "idle-loop-tapdance", "pose10": "emote-pose10",
    "scared": "emoji-scared", "arrogance": "emoji-arrogance", "wrong": "dance-wrong",
    "halo": "emoji-halo", "anime": "dance-anime", "hyped": "emote-hyped", "boo": "emote-boo",
    "trampoline": "emote-trampoline", "ghost": "emoji-ghost", "float": "emote-float",
    "sleigh": "emote-sleigh", "cheerleader": "dance-cheerleader", "ninjarun": "emote-ninjarun",
    "gangnam": "emote-gangnam", "snake": "emote-snake", "pinguin": "dance-pinguin",
    "loopaerobics": "idle-loop-aerobics", "howl": "emote-howl", "launch": "emote-launch",
    "creepypuppet": "dance-creepypuppet", "gravity": "emote-gravity", "confused": "emote-confused",
    "creepycute": "emote-creepycute", "smoothwalk": "dance-smoothwalk", "nervous": "idle-nervous",
    "gordonshuffle": "emote-gordonshuffle", "rofl": "emote-rofl", "icecream": "dance-icecream",
    "celebrate": "emote-celebrate", "panic": "emote-panic", "punkguitar": "emote-punkguitar",
    "singleladies": "dance-singleladies", "punch": "emoji-punch", "shoppingcart": "dance-shoppingcart",
    "poop": "emoji-poop", "tiktok4": "idle-dance-tiktok4", "nightfever": "emote-nightfever",
    "snowangel": "emote-snowangel", "headblowup": "emote-headblowup", "roll": "emote-roll",
    "sitopen": "sit-open", "floorsleeping2": "idle-floorsleeping2", "teleporting": "emote-teleporting",
    "hearteyes": "emote-hearteyes", "tiktok8": "dance-tiktok8", "angry": "idle-angry",
    "astronaut": "emote-astronaut", "sitrelaxed": "sit-relaxed", "fashionista": "emote-fashionista",
    "kissing": "emote-kissing", "rainbow": "emote-rainbow", "toilet": "idle-toilet",
    "snowball": "emote-snowball", "peekaboo": "emote-peekaboo", "frustrated": "emote-frustrated",
    "jetpack": "emote-jetpack", "looping": "emote-looping", "idlehowl": "idle-howl",
    "emotetapdance": "emote-tapdance", "death": "emote-death", "secrethandshake": "emote-secrethandshake",
    "fruity": "dance-fruity", "zombie": "dance-zombie", "robot": "emote-robot",
    "zombierun": "emote-zombierun", "charging": "emote-charging", "fighter": "idle-fighter",
    "kicking": "emote-kicking", "layingdown": "idle_layingdown", "uwu": "idle-uwu",
    "harlemshake": "emote-harlemshake", "blackpink": "dance-blackpink", "employee": "dance-employee",
    "cute": "emote-cute", "tiktok14": "dance-tiktok14", "russian": "dance-russian",
    "handstand": "emote-handstand", "elbowbump": "emote-elbowbump", "floating": "idle-floating",
    "mindblown": "emoji-mind-blown", "idlezombie": "idle_zombie", "disco": "emote-disco",
    "jumpb": "emote-jumpb", "heartshape": "emote-heartshape", "judochop": "emote-judochop",
    "levelup": "emote-levelup", "peace": "emote-peace", "suckthumb": "emote-suckthumb",
    "think": "emote-think", "headbobbing": "idle-dance-headbobbing", "tired": "idle-loop-tired",
    "crying": "emoji-crying", "dizzy": "emoji-dizzy", "pray": "emoji-pray",
    "exasperated": "emote-exasperated", "sad": "idle-sad", "deathdrop": "emote-deathdrop",
    "hot": "emote-hot", "hug": "emote-hug", "loopsad": "idle-loop-sad", "lookup": "idle-lookup",
    "posh": "idle-posh", "wings": "emote-wings", "there": "emoji-there", "superpunch": "emote-superpunch",
    "sleep": "idle-sleep", "weird": "dance-weird", "fainting": "emote-fainting",
    "monsterfail": "emote-monster_fail", "idlehero": "idle-hero", "handsup": "dance-handsup",
    "fail2": "emote-fail2", "ropepull": "emote-ropepull", "bow": "emote-bow", "model": "emote-model",
    "splitsdrop": "emote-splitsdrop", "sick": "emoji-sick", "embarrassed": "emote-embarrassed",
    "proposing": "emote-proposing", "enthusiastic": "idle-enthusiastic", "cold": "emote-cold",
    "telekinesis": "emote-telekinesis", "hadoken": "emoji-hadoken", "sneeze": "emoji-sneeze",
    "fail1": "emote-fail1", "naughty": "emoji-naughty", "hugyourself": "emote-hugyourself",
    "theatrical": "emote-theatrical", "greedy": "emote-greedy", "baseball": "emote-baseball",
    "sumo": "emote-sumo", "death2": "emote-death2", "smirking": "emoji-smirking",
    "voguehands": "dance-voguehands", "eyeroll": "emoji-eyeroll", "giveup": "emoji-give-up",
    "bunnyhop": "emote-bunnyhop", "exasperatedb": "emote-exasperatedb", "loophappy": "idle-loop-happy",
    "heartfingers": "emote-heartfingers", "collabphoto": "emote-collab-photo-left"
}

# ==========================
# LOGIQUE DU BOT
# ==========================
class Bot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata):
        print("🤖 Bot connecté !")
        await self.highrise.chat("✅ Leviae est en ligne ! Tape !help")

    async def on_user_join(self, user: User, position: Position):
        await self.highrise.chat(f"👋 Bienvenue {user.username} !")

    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem):
        if receiver.username.lower() == BOT_USERNAME.lower():
            amount = tip.amount if hasattr(tip, 'amount') else tip
            await self.highrise.chat(f"💎 Merci {sender.username} pour le tip de {amount} gold !")
            try:
                await self.highrise.send_emote(sender.id, "dance-shoppingcart")
            except Exception:
                pass

    async def on_chat(self, user: User, message: str):
        text = message.lower().strip()
        if text in EMOTES:
            try: await self.highrise.send_emote(user.id, EMOTES[text])
            except Exception: pass
            return

        if text == "!help":
            await self.highrise.chat("📜 Tapez le nom d'une danse (ex: voguehands, griddy, heartfingers) ou !dance / !wave")
        elif text == "!id":
            await self.highrise.chat(f"👤 Ton ID Highrise : {user.id}")
        elif text == "!dance":
            try: await self.highrise.send_emote(user.id, "idle-dance-casual")
            except Exception: pass
        elif text == "!wave":
            try: await self.highrise.send_emote(user.id, "idle-wave")
            except Exception: pass
        elif text.startswith("!emote"):
            if user.id not in OWNERS:
                await self.highrise.chat("❌ Propriétaire requis.")
                return
            emote = message[6:].strip()
            try: await self.highrise.send_emote(user.id, emote)
            except Exception: await self.highrise.chat("❌ Emote inconnue.")
        elif text.startswith("!kick"):
            if user.id not in OWNERS and user.id not in MODERATORS:
                await self.highrise.chat("❌ Permission refusée.")
                return
            target = message[5:].strip().replace("@", "")
            try:
                room_users = await self.highrise.get_room_users()
                for u, pos in room_users.users:
                    if u.username.lower() == target.lower():
                        await self.highrise.kick_user(u.id)
                        await self.highrise.chat(f"🚪 {u.username} a été expulsé.")
                        break
            except Exception as e:
                print(f"Erreur kick : {e}")
        elif "bonjour" in text:
            await self.highrise.chat(f"👋 Bonjour {user.username} !")
        elif "bot" in text:
            await self.highrise.chat("🤖 Oui, je suis là.")

if __name__ == "__main__":
    room = os.environ.get("room_id", "65e361f8aef42a7b0ed22029")
    token = os.environ.get("api_token", "f1f9d1cae9063a6a0a50ccfc95d0864005990c820d5f7dcf3463a6a11ecd3cfa")
    os.system(f"highrise main:Bot {room} {token}")
