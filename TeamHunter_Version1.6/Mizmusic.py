import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QSlider, QStyle, QHBoxLayout, QSizePolicy, QApplication, QListWidget, QListWidgetItem
from PyQt6.QtCore import QSize, Qt, QTimer, QRect
from PyQt6.QtGui import QColor, QPainter, QBrush, QLinearGradient
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

        self.n_bars = bars
        self.n_steps = len(steps) if isinstance(steps, list) else steps
        self.steps = steps if isinstance(steps, list) else ['red'] * steps

        self._values = [0.0] * bars
        self._target_values = [0.0] * bars
        self._peak_values = [0.0] * bars
        self._is_playing = False
        
        # Animation timer
        self._timer = QTimer()
        self._timer.setInterval(50)  # 20fps
        self._timer.timeout.connect(self._update_animation)
        self._timer.start()
        
        # Constants
        self._decay_speed = 3.0
        self._peak_decay = 0.8  # Slower peak decay
        self._rise_speed = 0.5
        #self._background = QColor('#1E1E1E')
        self._bar_padding = 2
        self._min_height = 5  # Reduced minimum height
        self._update_counter = 0
        self._stopping = False  # New flag to track stopping state

    def _update_animation(self):
        """Update animation values"""
        if not self._is_playing:
            # Gradually decay all values to 0 when not playing
            all_zero = True
            for i in range(self.n_bars):
                if self._values[i] > 0:
                    self._values[i] = max(0, self._values[i] - self._decay_speed)
                    all_zero = False
                if self._peak_values[i] > 0:
                    # Continue peak decay even when stopped
                    self._peak_values[i] = max(0, self._peak_values[i] - (self._peak_decay * 0.5))
                    all_zero = False
            
            if not all_zero:
                self.update()
            return

        self._update_counter += 1
        
        # Update target values every 5 frames
        if self._update_counter % 5 == 0:
            for i in range(self.n_bars):
                if random.random() < 0.3:  # 30% chance to change each bar
                    self._target_values[i] = random.uniform(self._min_height, 100)
        
        # Smooth transitions
        for i in range(self.n_bars):
            # Move current value towards target
            diff = self._target_values[i] - self._values[i]
            if abs(diff) < 0.1:
                self._values[i] = self._target_values[i]
            else:
                self._values[i] += diff * self._rise_speed
            
            # Update peaks
            if not self._stopping:
                self._peak_values[i] = max(self._peak_values[i], self._values[i])
            self._peak_values[i] = max(0, self._peak_values[i] - self._peak_decay)
        
        self.update()

    def set_playing(self, is_playing):
        """Set whether music is currently playing"""
        self._is_playing = is_playing
        if not is_playing:
            self._target_values = [0.0] * self.n_bars
            self._stopping = True  # Set stopping flag when playback stops
        else:
            self._stopping = False  # Reset stopping flag when playback starts

    def reset(self):
        """Reset all values to 0"""
        self._values = [0.0] * self.n_bars
        self._target_values = [0.0] * self.n_bars
        # Don't immediately reset peak values - let them decay naturally
        self._is_playing = False
        self._stopping = True
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        
        # Calculate dimensions
        width = self.width() - 2
        height = self.height() - 2
        bar_width = (width - (self.n_bars - 1) * self._bar_padding) / self.n_bars
        
        # Draw bars
        x = 1
        for i in range(self.n_bars):
            # Get bar height
            value = self._values[i]
            bar_height = value * height / 100
            
            # Get color
            color_idx = min(int(value * (len(self.steps) - 1) / 100), len(self.steps) - 1)
            color = QColor(self.steps[color_idx])
            
            # Create gradient
            gradient = QLinearGradient(0, height - bar_height, 0, height)
            gradient.setColorAt(0, color.lighter(150))
            gradient.setColorAt(1, color.darker(150))
            
            # Draw bar
            bar_rect = QRect(
                int(x),
                int(height - bar_height + 1),
                int(bar_width),
                int(bar_height)
            )
            painter.fillRect(bar_rect, gradient)
            
            # Draw peak
            peak_height = self._peak_values[i] * height / 100
            peak_rect = QRect(
                int(x),
                int(height - peak_height),
                int(bar_width),
                2
            )
            painter.fillRect(peak_rect, QColor(255, 20, 147))  # Bright pink color
            
            x += bar_width + self._bar_padding

    def sizeHint(self):
        return QSize(200, 100)

class Music_Player:
    pygame.mixer.init()

    def __init__(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.sounds_dir = os.path.join(current_dir, "music")
        self.current_song = ""
        self.playlist = []
        self.repeat = False
        
        # Reduced update frequency for equalizer
        self.update_timer = QTimer()
        self.update_timer.setInterval(100)  # 10fps
        self.update_timer.start()
        
        self.current_sound = None
        self.current_duration = 0
        self._fft_buffer = None
        self._last_update = 0
        self.load_playlist()

    def load_playlist(self):
        """Load all available songs into the playlist"""
        self.playlist = self.get_song_list()
        random.shuffle(self.playlist)

    def play_my_music(self, seek_slider, equalizer_bar, current_song_label, specific_song=None):
        if specific_song:
            self.current_song = specific_song
            my_song = os.path.join(self.sounds_dir, specific_song)
        else:
            if not self.playlist:
                self.shuffle_playlist()
            if self.playlist:
                my_song = os.path.join(self.sounds_dir, self.playlist[0])
                self.current_song = os.path.basename(my_song)
            else:
                current_song_label.setText('Playlist is empty.')
                return

        try:
            # Load and cache the sound object
            self.current_sound = pygame.mixer.Sound(my_song)
            self.current_duration = self.current_sound.get_length() * 1000
            
            pygame.mixer.music.load(my_song)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()

            # Set end event to trigger next song
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            pygame.event.set_allowed(pygame.USEREVENT)

            current_song_label.setText(f'Current Song: {self.current_song}')
            seek_slider.setRange(0, int(self.current_duration))

        except pygame.error as e:
            print(f"Error playing {my_song}: {str(e)}")
            if not specific_song and self.playlist:
                self.playlist.pop(0)
                self.play_my_music(seek_slider, equalizer_bar, current_song_label)

    def update_equalizer(self, equalizer_bar):
        # This method is now empty since the equalizer animates itself
        pass

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_song = ""

    def get_song_list(self):
        return [file for file in os.listdir(self.sounds_dir) if file.lower().endswith(('.mp3', '.wav', '.ogg'))]

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
            try:
                pygame.mixer.music.set_pos(position / 1000)
            except:
                print(f"Cannot seek to position {position}")


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        
        self.speaker = Music_Player()
        self.current_index = 0
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_seek_slider)
        self.update_timer.start(50)  # Increased update frequency for smoother UI
        self.seek_position = 0
        self.manual_stop = False  # Add flag for manual stop
        
        # Add event processing timer
        self.event_timer = QTimer()
        self.event_timer.timeout.connect(self.process_pygame_events)
        self.event_timer.start(100)  # Check for events every 100ms
        
        self.init_ui()

        initial_volume = 50
        self.volume_slider.setValue(initial_volume)
        self.set_volume(initial_volume / 100.0)

        self.equalizer_bar = EqualizerBar(33, ['#0C0786', '#40039C', '#6A00A7', '#8F0DA3', '#B02A8F', '#CA4678', '#E06461',
                                          '#F1824C', '#FCA635', '#FCCC25', '#EFF821'])
        self.layout().addWidget(self.equalizer_bar)

        pygame.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Create a single row for all controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)  # Reduce spacing between elements
        
        # Previous button
        self.prev_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward), '')
        self.prev_button.clicked.connect(self.previous_song)
        self.prev_button.setStyleSheet( "QPushButton { font-size: 16pt; padding: 4px; }")
        
        # Play button
        self.play_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay), '')
        self.play_button.clicked.connect(self.play_music)
        self.play_button.setStyleSheet( "QPushButton { font-size: 16pt; padding: 4px; }")
        
        # Stop button
        self.stop_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop), '')
        self.stop_button.clicked.connect(self.stop_music)
        self.stop_button.setStyleSheet( "QPushButton { font-size: 16pt; padding: 4px; }")
        
        # Next button
        self.next_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward), '')
        self.next_button.clicked.connect(self.next_song)
        self.next_button.setStyleSheet( "QPushButton { font-size: 16pt; padding: 4px; }")
        
        # Current time labels
        self.current_time_label = QLabel('0:00')
        self.current_time_label.setStyleSheet("QLabel { min-width: 45px; }")
        self.total_time_label = QLabel('/ 0:00')
        self.total_time_label.setStyleSheet("QLabel { min-width: 45px; }")
        
        # Seek slider
        self.seek_slider = QSlider(Qt.Orientation.Horizontal)
        self.seek_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #666666;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #E7481F;
                width: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QSlider::sub-page:horizontal {
                background: #E7481F;
            }
        """)
        self.seek_slider.sliderMoved.connect(self.seek_slider_moved)
        self.seek_slider.sliderReleased.connect(self.seek_music)
        
        # Volume control
        volume_label = QLabel('🔊')
        volume_label.setStyleSheet("QLabel { font-size: 16pt; }")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMaximumWidth(100)  # Limit volume slider width
        self.volume_slider.setMaximum(100)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #666666;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #E7481F;
                width: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QSlider::sub-page:horizontal {
                background: #E7481F;
            }
        """)
        self.volume_slider.valueChanged.connect(self.set_volume)

        # Current song label
        self.current_song_label = QLabel('Current Song: ')
        
        # Add all controls to the layout
        controls_layout.addWidget(self.current_song_label)
        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(self.next_button)
        controls_layout.addWidget(self.current_time_label)
        controls_layout.addWidget(self.seek_slider)
        controls_layout.addWidget(self.total_time_label)
        controls_layout.addWidget(volume_label)
        controls_layout.addWidget(self.volume_slider)
        
        # Set stretch factors
        controls_layout.setStretchFactor(self.current_song_label, 2)
        controls_layout.setStretchFactor(self.seek_slider, 3)
        controls_layout.setStretchFactor(self.volume_slider, 1)
        
        main_layout.addLayout(controls_layout)
        self.setLayout(main_layout)

    def update_seek_slider(self):
        if not self.seek_slider.isSliderDown() and pygame.mixer.music.get_busy():
            position = pygame.mixer.music.get_pos()
            if position > -1:  # Only update if position is valid
                self.seek_slider.setValue(position)
                
                # Efficient time calculations
                current_time = position / 1000
                total_time = self.speaker.current_duration / 1000 if self.speaker.current_duration else 0
                
                # Format times efficiently
                self.current_time_label.setText(f'{int(current_time // 60)}:{int(current_time % 60):02d}')
                self.total_time_label.setText(f'/ {int(total_time // 60)}:{int(total_time % 60):02d}')

    def seek_slider_moved(self, position):
        """Update time label when seek slider is moved"""
        minutes = int(position / 60000)
        seconds = int((position / 1000) % 60)
        self.current_time_label.setText(f'{minutes}:{seconds:02d}')

    def seek_music(self):
        """Seek to position in current song"""
        position = self.seek_slider.value()
        self.speaker.seekPosition(position)
        minutes = int(position / 60000)
        seconds = int((position / 1000) % 60)
        self.current_time_label.setText(f'{minutes}:{seconds:02d}')

    def next_song(self):
        """Play the next song in the playlist"""
        if self.speaker.playlist:
            # Get all songs and current index
            all_songs = self.speaker.get_song_list()
            try:
                current_index = all_songs.index(self.speaker.current_song)
                next_index = (current_index + 1) % len(all_songs)
                next_song = all_songs[next_index]
                
                # Update playlist to start from next song
                self.speaker.playlist = all_songs[next_index:] + all_songs[:next_index]
                
                # Play the next song
                self.speaker.play_my_music(self.seek_slider, self.equalizer_bar, self.current_song_label, next_song)
                self.update_current_song_label()
            except ValueError:
                # If current song not found, start fresh
                self.speaker.shuffle_playlist()
                self.play_music()
        else:
            self.speaker.shuffle_playlist()
            self.play_music()

    def update_current_song_label(self):
        """Update the current song label"""
        current_song = self.speaker.get_current_song()
        self.current_song_label.setText(f'Current Song: {current_song if current_song else "No song playing"}')

    def set_volume(self, value):
        """Set the volume level"""
        volume = value / 100.0
        self.speaker.set_volume(volume)
        self.volume_slider.setToolTip(f'Volume: {int(value)}%')

    def handle_event(self, event):
        """Handle end of song event"""
        if event.type == pygame.USEREVENT:
            if not self.manual_stop:  # Only play next song if not manually stopped
                self.next_song()
            self.manual_stop = False  # Reset the flag

    def play_music(self):
        """Play the current song"""
        if not pygame.mixer.music.get_busy():
            self.speaker.play_my_music(self.seek_slider, self.equalizer_bar, self.current_song_label)
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
            self.equalizer_bar.set_playing(True)
        else:
            pygame.mixer.music.pause() if pygame.mixer.music.get_busy() else pygame.mixer.music.unpause()
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
                if pygame.mixer.music.get_busy()
                else self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
            )
            self.equalizer_bar.set_playing(pygame.mixer.music.get_busy())
        self.update_current_song_label()

    def stop_music(self):
        """Stop the current song"""
        self.manual_stop = True  # Set flag before stopping
        self.speaker.stop_music()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.current_time_label.setText('0:00')
        self.total_time_label.setText('/ 0:00')
        self.seek_slider.setValue(0)
        self.equalizer_bar.reset()  # Use new reset method instead of setValues
        self.update_current_song_label()

    def process_pygame_events(self):
        """Process pygame events to catch end of song"""
        for event in pygame.event.get():
            self.handle_event(event)

    def previous_song(self):
        """Play the previous song in the playlist"""
        if self.speaker.playlist:
            all_songs = self.speaker.get_song_list()
            try:
                current_index = all_songs.index(self.speaker.current_song)
                prev_index = (current_index - 1) % len(all_songs)
                prev_song = all_songs[prev_index]
                
                # Update playlist to start from previous song
                self.speaker.playlist = all_songs[prev_index:] + all_songs[:prev_index]
                
                # Play the previous song
                self.speaker.play_my_music(self.seek_slider, self.equalizer_bar, self.current_song_label, prev_song)
                self.update_current_song_label()
            except ValueError:
                self.speaker.shuffle_playlist()
                self.play_music()
        else:
            self.speaker.shuffle_playlist()
            self.play_music()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())