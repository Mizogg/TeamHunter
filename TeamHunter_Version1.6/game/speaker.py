import pygame
import random
import os

class Speaker():
    muted = False
    pygame.mixer.init()
    current_dir = os.path.dirname (os.path.realpath(__file__))
    block_fallen                = "block_fallen.wav"
    death1                      = "death_1.wav"
    death2                      = "death_2.wav"
    generic_scroll_01           = "generic_scroll_01.wav"
    lvl1                        = "lvl1.wav"
    lvl2                        = "lvl2.wav"
    lvl3                        = "lvl3.wav"
    lvl4                        = "lvl4.wav"
    lvl5                        = "lvl5.wav"
    menu_accept                 = "menu_accept.wav"
    menu_back                   = "menu_back.wav"
    menu_focus                  = "menu_focus.wav"
    null                        = "null.wav"
    row_deleted                 = "row_deleted.wav"
    ui_menu_flip_single_01      = "ui_menu_flip_single_01.wav"
    ui_menu_flip_single_02      = "ui_menu_flip_single_02.wav"

    def toggle_mute():
        Speaker.muted = not Speaker.muted

    def scroll():
        sound = random.randint(1,2)
        if sound == 1:
            Speaker.playsound(Speaker.obj(Speaker.ui_menu_flip_single_01))
        if sound == 2:
            Speaker.playsound(Speaker.obj(Speaker.ui_menu_flip_single_02))

    def play_background_music():
        if not Speaker.muted:
            main_theme = "background_music.mp3"
            music_path = os.path.join(Speaker.current_dir, "sounds", main_theme)
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

    def stop_background_music():
        pygame.mixer.music.stop()

    def obj(name):
        return pygame.mixer.Sound(os.path.join(Speaker.current_dir, "sounds\\"+name))

    def playsound(wave_obj, volume = 1.0):
        if not Speaker.muted:
            wave_obj.play()
            wave_obj.set_volume(volume)
        
    def play_death():
        if not Speaker.muted:
            sound = random.randint(1,2)
            if sound == 1:
                Speaker.playsound(Speaker.obj(Speaker.death1), 0.5)
            if sound == 2:
                Speaker.playsound(Speaker.obj(Speaker.death2), 0.5)
