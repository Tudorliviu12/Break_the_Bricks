import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl

class SoundManager:
    def __init__(self):
        self.muted = False
        self.bg_playlist = QMediaPlaylist()
        bg_path = os.path.abspath("assets/sounds/background.mp3")
        self.bg_playlist.addMedia(QMediaContent(QUrl.fromLocalFile(bg_path)))
        self.bg_playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.bg_player = QMediaPlayer()
        self.bg_player.setPlaylist(self.bg_playlist)
        self.bg_player.setVolume(30)
        self.fx_player = QMediaPlayer()
        #fx_path = os.path.abspath("assets/sounds/sound.mp3")
        #self.fx_content = QMediaContent(QUrl.fromLocalFile(fx_path))
        #self.fx_player.setMedia(self.fx_content)
        #self.fx_player.setVolume(70)

    def start_background_music(self):
        if not self.muted:
            self.bg_player.play()

    #def play_hit_sound(self):
        #if not self.muted:
            #if self.fx_player.state() == QMediaPlayer.PlayingState:
                #self.fx_player.stop()
            #self.fx_player.play()

    def update_volume_settings(self, sound_enabled):
        self.muted = not sound_enabled

        if self.muted:
            self.bg_player.pause()
            self.fx_player.stop()
        else:
            if self.bg_player.state() != QMediaPlayer.PlayingState:
                self.bg_player.play()