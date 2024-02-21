from kivymd.uix.screen import MDScreen

import json

from libs.components.circular_avatar_image import CircularAvatarImage

from libs.components.post_card import PostCard

class HomePage(MDScreen):
    profile_picture = "resources/img/pic2.png"

    # Ajout contenu story
    # evenement declenche au lancement de l'application
    def on_enter(self):
        self.list_stories()
        self.list_posts()

    def list_stories(self):
        # ouverture du fic json contenant les noms user et lien image
        with open("resources/data/stories.json") as f_obj:
            data = json.load(f_obj)
            for name in data:
                # element possedant un id `stories` -> ajout des widget
                self.ids.stories.add_widget(CircularAvatarImage(
                    avatar = data[name]['avatar'],
                    name = name

                ))

    def list_posts(self):
        with open("resources/data/posts.json") as f_obj:
            data = json.load(f_obj)
            for name in data:
                self.ids.timeline.add_widget(PostCard(
                    username = name,
                    avatar = data[name]['avatar'],
                    profile_picture = self.profile_picture,
                    post = data[name]['post'],
                    caption = data[name]['caption'],
                    likes = data[name]['likes'],
                    posted_ago = data[name]['posted_ago'],
                    comments = data[name]['comments']

                ))
