import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QSlider, QStyle, QHBoxLayout, QSizePolicy, QApplication
from PyQt6.QtCore import QSize, Qt, QTimer, QRect
from PyQt6.QtGui import QColor, QPainter, QBrush
import pygame
import os
import random
import numpy as np

from game.speaker import Speaker
import pygame.event

class EqualizerBar(QWidget):
    def __init__(self, bars, steps, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        )

        if isinstance(steps, list):
            self.n_steps = len(steps)
            self.steps = steps
        elif isinstance(steps, int):
            self.n_steps = steps
            self.steps = ['red'] * steps
        else:
            raise TypeError('steps must be a list or int')

        self.n_bars = bars
        self._x_solid_percent = 0.8
        self._y_solid_percent = 2.8
        self._background_color = QColor('black')
        self._padding = 10
        self._timer = None
        self._decay = 15
        self._vmin = 0
        self._vmax = 100
        self._values = [0.0] * bars

    def paintEvent(self, e):
        painter = QPainter(self)

        brush = QBrush()
        brush.setColor(self._background_color)
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QRect(0, 0, round(painter.device().width()), round(painter.device().height()))
        painter.fillRect(rect, brush)
        d_height = painter.device().height() - (self._padding * 2)
        d_width = painter.device().width() - (self._padding * 2)
        steps = random.randint(1, 7)
        step_y = d_height / steps
        bar_height = step_y * self._y_solid_percent
        bar_height_space = step_y * (1 - self._x_solid_percent) / 2
        step_x = d_width / self.n_bars
        bar_width = step_x * self._x_solid_percent
        bar_width_space = step_x * (1 - self._y_solid_percent) / 2

        for b in range(self.n_bars):
            pc = (self._values[b] - self._vmin) / (self._vmax - self._vmin)
            bar_height_current = pc * bar_height
            brush.setColor(QColor(self.steps[b % len(self.steps)]))
            rect = QRect(
                int(self._padding + (step_x * b) + bar_width_space),
                int(self._padding + d_height - bar_height_current + bar_height_space),
                int(bar_width),
                int(bar_height_current)
            )

            painter.fillRect(rect, brush)


    def sizeHint(self):
        return QSize(66, 50)

    def _trigger_refresh(self):
        self.update()

    def setDecay(self, f):
        self._decay = float(f)

    def setDecayFrequencyMs(self, ms):
        if self._timer:
            self._timer.stop()

        if ms:
            self._timer = QTimer()
            self._timer.setInterval(ms)
            self._timer.timeout.connect(self._decay_beat)
            self._timer.start()

    def _decay_beat(self):
        self._values = [
            max(0, v - self._decay)
            for v in self._values
        ]
        self.update()

    def setValues(self, v):
        self._values = v
        self._trigger_refresh()

    def values(self):
        return self._values

    def setRange(self, vmin, vmax):
        assert float(vmin) < float(vmax)
        self._vmin, self._vmax = float(vmin), float(vmax)

    def setColor(self, color):
        self.steps = [color] * self.n_steps
        self.update()

    def setColors(self, colors):
        self.n_steps = len(colors)
        self.steps = colors
        self.update()

    def setBarPadding(self, i):
        self._padding = int(i)
        self.update()

    def setBarSolidPercent(self, f):
        self._bar_solid_percent = float(f)
        self.update()

    def setBackgroundColor(self, color):
        self._background_color = QColor(color)
        self.update()

class Music_Player:
    pygame.mixer.init()

    def __init__(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.sounds_dir = os.path.join(current_dir, "music")
        self.current_song = ""
        self.playlist = []
        self.repeat = False
        self.update_timer = QTimer()
        self.update_timer.start(100)

    def play_my_music(self, seek_slider, equalizer_bar, current_song_label):
        if not self.playlist:
            self.shuffle_playlist()

        if self.playlist:
            my_song = os.path.join(self.sounds_dir, self.playlist.pop(0))
            pygame.mixer.music.load(my_song)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()

            # Set end event to trigger next song
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            pygame.event.set_allowed(pygame.USEREVENT)

            self.current_song = os.path.basename(my_song)
            current_song_label.setText(f'Current Song: {self.current_song}')  # Update current song label
            duration = pygame.mixer.Sound(my_song).get_length() * 1000
            seek_slider.setRange(0, int(duration))
            
            self.update_timer.timeout.connect(lambda: self.update_equalizer(equalizer_bar))

            # When the song ends, advance to the next song
            pygame.mixer.music.queue(os.path.join(self.sounds_dir, self.playlist[0]))


    def update_equalizer(self, equalizer_bar):
        current_position = pygame.mixer.music.get_pos()
        values = [int(np.sin(0.1 * (current_position + i)) * 50 + 50) for i in range(equalizer_bar.n_bars)]
        equalizer_bar.setValues(values)
        
    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_song = ""

    def get_song_list(self):
        return [file for file in os.listdir(self.sounds_dir) if file.endswith(".mp3")]

    def get_current_song(self):
        return self.current_song

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def get_volume(self):
        return pygame.mixer.music.get_volume()

    def shuffle_playlist(self):
        self.playlist = self.get_song_list()
        random.shuffle(self.playlist)

    def seekPosition(self, position):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_pos(position / 1000)


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.speaker = Music_Player()
        self.current_index = 0
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_seek_slider)
        self.update_timer.start(100)
        self.seek_position = 0
        self.init_ui()

        initial_volume = 50
        self.volume_slider.setValue(initial_volume)
        self.set_volume(initial_volume / 100.0)

        self.equalizer_bar = EqualizerBar(66, ['#0C0786', '#40039C', '#6A00A7', '#8F0DA3', '#B02A8F', '#CA4678', '#E06461',
                                          '#F1824C', '#FCA635', '#FCCC25', '#EFF821'])
        self.layout().addWidget(self.equalizer_bar)

        # Initialize the Pygame video system
        pygame.init()

        # Connect the Pygame music end event to the next_song function
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def play_music(self):
        self.speaker.play_my_music(self.seek_slider, self.equalizer_bar, self.current_song_label)
        self.update_current_song_label()

        self.equalizer_bar.setValues([
            min(100, v+random.randint(0, 100) if random.randint(0, 10) > 2 else v)
            for v in self.equalizer_bar.values()
            ])

    def stop_music(self):
        self.speaker.stop_music()
        self.update_current_song_label()

    def init_ui(self):
        common_style = (
            "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
            "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
        )

        self.play_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay), '')
        self.stop_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop), '')
        self.next_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward), '')

        self.play_button.setStyleSheet(common_style)
        self.stop_button.setStyleSheet(common_style)
        self.next_button.setStyleSheet(common_style)
        
        self.play_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_accept))
        self.stop_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        
        self.current_song_label = QLabel('Current Song: ')
        self.volume_label = QLabel(f'Volume: {self.speaker.get_volume() * 100} dB')

        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.setSpacing(10) 
        layout1.addWidget(self.current_song_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(self.volume_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(self.volume_slider)
        layout1.addWidget(self.play_button)
        layout1.addWidget(self.stop_button)
        layout1.addWidget(self.next_button)

        self.seek_slider = QSlider(Qt.Orientation.Horizontal)
        self.seek_timer_label = QLabel("0:00")

        layout1.addWidget(self.seek_timer_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(self.seek_slider)

        self.seek_slider.sliderMoved.connect(self.seek_slider_moved)
        self.seek_slider.sliderReleased.connect(self.seek_music)

        layout.addLayout(layout1)
        self.setLayout(layout)

        decibel_value = round(self.speaker.get_volume() * 100, 2)
        self.volume_label.setText(f'Volume: {decibel_value} dB')

        self.play_button.clicked.connect(self.play_music)
        self.stop_button.clicked.connect(self.stop_music)
        self.next_button.clicked.connect(self.next_song)
        self.volume_slider.valueChanged.connect(self.set_volume)

    def update_seek_slider(self):
            if not self.seek_slider.isSliderDown():
                position = pygame.mixer.music.get_pos()
                self.seek_slider.setValue(position)
                self.seek_timer_label.setText('%d:%02d' % (int(position / 60000), int((position / 1000) % 60)))

    def seek_slider_moved(self, position):
        self.seek_timer_label.setText('%d:%02d' % (int(position / 60000), int((position / 1000) % 60)))

    def seek_music(self):
        position = self.seek_slider.value()
        self.speaker.seekPosition(position)
        self.seek_timer_label.setText('%d:%02d' % (int(position / 60000), int((position / 1000) % 60)))

    def next_song(self):
        self.speaker.play_my_music(self.seek_slider, self.equalizer_bar, self.current_song_label)
        self.update_current_song_label()

    def update_current_song_label(self):
        current_song = self.speaker.get_current_song()
        self.current_song_label.setText(f'Current Song: {current_song}')

    def set_volume(self, value):
        volume = value / 100.0
        self.speaker.set_volume(volume)

        decibel_value = round(self.speaker.get_volume() * 100, 2)
        self.volume_label.setText(f'Volume: {decibel_value} dB')

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            self.next_song()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())