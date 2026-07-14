import json
import os
import random
from highrise import User, Position
from highrise.models import CurrencyItem

class Game:
    def __init__(self):
        self.players = {}
        self.points = {}
        self.load_data()

    def load_data(self):
        # Encodage sécurisé en utf-8 pour éviter les crashs sur les serveurs de Render
        if os.path.exists("players.json"):
            try:
                with open("players.json", "r", encoding="utf-8") as f:
                    self.points = json.load(f)
            except Exception:
                self.points = {}

    def save_data(self):
        try:
            with open("players.json", "w", encoding="utf-8") as f:
                json.dump(self.points, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erreur de sauvegarde JSON : {e}")

    def add_player(self, user: User):
        self.players[user.id] = user.username
        if user.username not in self.points:
            self.points[user.username] = 0
            self.save_data()

    def remove_player(self, user: User):
        if user.id in self.players:
            del self.players[user.id]

    async def gameloop(self, highrise_api):
        # Boucle automatique en arrière-plan pour animer le salon toutes les 60 secondes
        while True:
            await asyncio.sleep(60)
            if self.players:
                # Choisit un joueur au hasard présent dans la pièce pour lui offrir un bonus
                random_user_id = random.choice(list(self.players.keys()))
                username = self.players[random_user_id]
                self.points[username] = self.points.get(username, 0) + 10
                self.save_data()
                try:
                    await highrise_api.chat(f"Félicitations @{username} ! Tu gagnes 10 points bonus d'activité ! 🎉")
                    # SYNTAXE CORRIGÉE : l'ID de l'utilisateur passe toujours en premier
                    await highrise_api.send_emote(random_user_id, "emote-celebrate")
                except Exception:
                    pass

    async def handle_command(self, highrise_api, user: User, message: str) -> None:
        msg = message.lower().strip()

        # Commande pour voir ses points accumulés
        if msg == "/points":
            pts = self.points.get(user.username, 0)
            await highrise_api.chat(f"@{user.username}, tu possèdes actuellement {pts} points ! 🏆")
            return

        # Commande de danse / emote générique
        if msg.startswith("/dance") or msg.startswith("/emote"):
            # Liste d'emotes populaires utilisables par défaut
            emotes_disponibles = ["dance-macarena", "dance-blackpink", "emote-wave", "emote-laughing", "emote-shy"]
            dance_choisie = random.choice(emotes_disponibles)
            try:
                # SYNTAXE CORRIGÉE : Correction de l'ancienne version défectueuse d'ilorez
                await highrise_api.send_emote(user.id, dance_choisie)
            except Exception:
                await highrise_api.send_whisper(user.id, "Zut ! Je ne peux pas exécuter cette danse pour le moment.")
            return

        # Guide d'aide pour afficher les commandes aux utilisateurs
        if msg == "/help":
            aide = "Commandes disponibles : /points (voir votre score), /dance (lancer une danse aléatoire), /joke (écouter une blague)."
            await highrise_api.chat(aide)
            return

    async def handle_whisper_command(self, highrise_api, user: User, message: str) -> None:
        # Gestion optionnelle des messages reçus en chuchotement privé
        msg = message.lower().strip()
        if msg == "/secret":
            await highrise_api.send_whisper(user.id, "Chut... C'est un message top secret entre toi et moi ! 🤫")

    async def process_tip(self, highrise_api, sender: User, amount: int) -> None:
        # Traitement spécial quand un joueur donne de l'or au bot
        username = sender.username
        # On récompense le donateur en lui offrant 100 points par pièce d'or offerte
        points_gagnes = amount * 100
        self.points[username] = self.points.get(username, 0) + points_gagnes
        self.save_data()
        print(f"[Économie] {username} a reçu {points_gagnes} points grâce à son don.")
