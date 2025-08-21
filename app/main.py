import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pygame
import database
import shutil
import os
import time
from PIL import Image, ImageTk, ImageDraw

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("800x550")

        pygame.mixer.init()

        self.current_track = None
        self.paused = False
        self.playing = False
        self.song_length = 0

        self.tracks_map = {}
        self.playlist_songs_map = {}
        self.favorites_map = {}
        self.recently_played_map = {}

        self.create_placeholder_image()
        self.create_styles()
        self.create_widgets()
        self.load_all_data()

        self.load_state()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update_progress()

    def create_placeholder_image(self):
        placeholder_path = "assets/placeholder.png"
        if not os.path.exists(placeholder_path):
            if not os.path.exists("assets"):
                os.makedirs("assets")
            img = Image.new('RGB', (100, 100), color = 'gray')
            d = ImageDraw.Draw(img)
            d.text((35,40), "No Art", fill=(255,255,255))
            img.save(placeholder_path, 'PNG')
        self.placeholder_image = self.load_album_art(placeholder_path)

    def create_styles(self):
        style = ttk.Style(self.root)
        style.configure("TButton", padding=6, relief="flat", font=('Helvetica', 10))
        style.configure("Treeview", rowheight=25, font=('Helvetica', 10))
        style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'))
        style.configure("NowPlaying.TFrame", background="lightgrey")
        style.configure("Title.TLabel", font=('Helvetica', 14, 'bold'))
        style.configure("Status.TLabel", font=('Helvetica', 10, 'italic'))

    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding="5")
        top_frame.pack(side=tk.TOP, fill=tk.X)
        library_frame = ttk.Frame(self.root, padding="5")
        library_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        bottom_frame = ttk.Frame(self.root, padding="5")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        search_frame = ttk.LabelFrame(top_frame, text="Search", padding="5")
        search_frame.pack(fill=tk.X)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        ttk.Button(search_frame, text="Search", command=self.search_library).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack(side=tk.LEFT)

        self.notebook = ttk.Notebook(library_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        # ... (Notebook setup is the same)
        gospel_frame = ttk.Frame(self.notebook); secular_frame = ttk.Frame(self.notebook)
        self.notebook.add(gospel_frame, text="Gospel"); self.notebook.add(secular_frame, text="Secular")
        self.gospel_tree = self.create_treeview(gospel_frame); self.secular_tree = self.create_treeview(secular_frame)
        favorites_frame = ttk.Frame(self.notebook); self.notebook.add(favorites_frame, text="Favorites")
        self.favorites_tree = self.create_treeview(favorites_frame)
        recently_played_frame = ttk.Frame(self.notebook); self.notebook.add(recently_played_frame, text="Recently Played")
        self.recently_played_tree = self.create_treeview(recently_played_frame)
        playlist_tab_frame = ttk.Frame(self.notebook); self.notebook.add(playlist_tab_frame, text="Playlists")
        # ... (Playlist UI setup is the same)
        playlist_left_frame = ttk.Frame(playlist_tab_frame); playlist_left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        playlist_right_frame = ttk.Frame(playlist_tab_frame); playlist_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        playlist_list_frame = ttk.LabelFrame(playlist_left_frame, text="Playlists"); playlist_list_frame.pack(fill=tk.BOTH, expand=True)
        self.playlist_listbox = tk.Listbox(playlist_list_frame, font=('Helvetica', 10)); self.playlist_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.playlist_listbox.bind('<<ListboxSelect>>', self.show_playlist_songs)
        playlist_controls_frame = ttk.Frame(playlist_left_frame); playlist_controls_frame.pack(fill=tk.X, pady=5)
        ttk.Button(playlist_controls_frame, text="New", command=self.create_new_playlist).pack(side=tk.LEFT, padx=2)
        ttk.Button(playlist_controls_frame, text="Rename", command=self.rename_selected_playlist).pack(side=tk.LEFT, padx=2)
        ttk.Button(playlist_controls_frame, text="Delete", command=self.delete_selected_playlist).pack(side=tk.LEFT, padx=2)
        playlist_songs_frame = ttk.LabelFrame(playlist_right_frame, text="Songs"); playlist_songs_frame.pack(fill=tk.BOTH, expand=True)
        self.playlist_songs_tree = self.create_treeview(playlist_songs_frame)


        now_playing_frame = ttk.LabelFrame(bottom_frame, text="Now Playing", padding="10")
        now_playing_frame.pack(fill=tk.X)

        self.album_art_label = ttk.Label(now_playing_frame, image=self.placeholder_image)
        self.album_art_label.pack(side=tk.LEFT, padx=(0, 10))

        details_frame = ttk.Frame(now_playing_frame)
        details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.song_label = ttk.Label(details_frame, text="No song selected", style="Title.TLabel")
        self.song_label.pack(anchor="w")
        self.artist_label = ttk.Label(details_frame, text="Artist", style="Status.TLabel")
        self.artist_label.pack(anchor="w")

        progress_frame = ttk.Frame(details_frame)
        progress_frame.pack(fill=tk.X, expand=True, pady=5)
        self.time_label = ttk.Label(progress_frame, text="00:00")
        self.time_label.pack(side=tk.LEFT)
        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.duration_label = ttk.Label(progress_frame, text="00:00")
        self.duration_label.pack(side=tk.RIGHT)

        controls_frame = ttk.Frame(now_playing_frame)
        controls_frame.pack(side=tk.RIGHT, padx=(10,0))
        self.prev_button = ttk.Button(controls_frame, text="⏮", command=self.prev_track, width=4); self.prev_button.pack(side=tk.LEFT, ipady=5)
        self.play_button = ttk.Button(controls_frame, text="▶", command=self.toggle_play_pause, width=6); self.play_button.pack(side=tk.LEFT, ipady=5)
        self.next_button = ttk.Button(controls_frame, text="⏭", command=self.next_track, width=4); self.next_button.pack(side=tk.LEFT, ipady=5)
        self.favorite_var = tk.StringVar(value="♡"); self.favorite_button = ttk.Button(controls_frame, textvariable=self.favorite_var, command=self.toggle_favorite, width=4); self.favorite_button.pack(side=tk.LEFT, ipady=5)

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Download Song", command=self.download_selected_song)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Add to Playlist...", command=self.add_to_playlist_dialog)
        self.context_menu.add_command(label="Toggle Favorite", command=self.toggle_favorite_from_context)

    def create_treeview(self, parent_frame):
        # ... (same as before, but with updated column widths)
        tree = ttk.Treeview(parent_frame, columns=('Title', 'Artist', 'Album', 'Status'), show='headings')
        tree.heading('Title', text='Title'); tree.column('Title', width=200)
        tree.heading('Artist', text='Artist'); tree.column('Artist', width=150)
        tree.heading('Album', text='Album'); tree.column('Album', width=150)
        tree.heading('Status', text='Status'); tree.column('Status', width=80, anchor='center')
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.bind('<Double-1>', self.play_selected_song)
        tree.bind("<Button-3>", self.show_context_menu)
        return tree

    def load_album_art(self, path):
        try:
            img = Image.open(path)
            img = img.resize((100, 100), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except:
            return self.placeholder_image

    def load_track(self):
        if self.current_track:
            # Update labels
            self.song_label.config(text=self.current_track[1])
            self.artist_label.config(text=self.current_track[2])
            self.update_favorite_button()

            # Load album art
            album_art_path = self.current_track[7]
            if album_art_path and os.path.exists(album_art_path):
                self.album_art = self.load_album_art(album_art_path)
            else:
                self.album_art = self.placeholder_image
            self.album_art_label.config(image=self.album_art)

            # Load audio and get length
            try:
                sound = pygame.mixer.Sound(self.current_track[5])
                self.song_length = sound.get_length()
                self.duration_label.config(text=time.strftime('%M:%S', time.gmtime(self.song_length)))
                self.progress_bar.config(maximum=self.song_length)
                pygame.mixer.music.load(self.current_track[5])
                self.status_label.config(text="Status: Loaded")
            except pygame.error as e:
                self.status_label.config(text=f"Status: Error - {e}")
                self.song_length = 0

    def update_progress(self):
        if self.playing and not self.paused and self.song_length > 0:
            current_time = (pygame.mixer.music.get_pos() / 1000.0)
            self.time_label.config(text=time.strftime('%M:%S', time.gmtime(current_time)))
            self.progress_bar.config(value=current_time)

        # Check if song has finished
        if self.playing and not pygame.mixer.music.get_busy() and not self.paused:
            self.next_track()

        self.root.after(1000, self.update_progress)

    def toggle_play_pause(self, force_play=False):
        # ... (logic is mostly the same, but with updated button text)
        if force_play and self.current_track: self.playing = False; pygame.mixer.music.stop()
        if not self.playing:
            if self.current_track:
                try:
                    start_pos = getattr(self, 'start_pos', 0)
                    pygame.mixer.music.play(start=start_pos)
                    if hasattr(self, 'start_pos'): delattr(self, 'start_pos')
                    self.status_label.config(text="Status: Playing"); self.play_button.config(text="⏸")
                    self.playing, self.paused = True, False
                    database.add_to_recently_played(self.current_track[0]); self.load_recently_played()
                except pygame.error: self.status_label.config(text="Status: Error playing file")
        elif self.paused:
            pygame.mixer.music.unpause(); self.status_label.config(text="Status: Playing"); self.play_button.config(text="⏸"); self.paused = False
        else:
            pygame.mixer.music.pause(); self.status_label.config(text="Status: Paused"); self.play_button.config(text="▶"); self.paused = True
        self.update_favorite_button()

    def update_favorite_button(self): self.favorite_var.set("♥" if self.current_track and self.current_track[8] == 1 else "♡")

    # ... (the rest of the methods are the same as the previous version)
    def populate_treeview(self, tree, song_list, track_map):
        tree.delete(*tree.get_children())
        track_map.clear()
        for song in song_list:
            status = "Offline" if song[9] else "Online"
            item_id = tree.insert('', 'end', values=(song[1], song[2], song[3], status))
            track_map[item_id] = song
    def load_all_data(self, query=None):
        self.load_library(query)
        self.load_playlists()
        self.load_favorites()
        self.load_recently_played()
    def get_active_tree_and_map(self):
        try:
            tab_index = self.notebook.index(self.notebook.select())
            if tab_index == 0: return self.gospel_tree, self.tracks_map
            if tab_index == 1: return self.secular_tree, self.tracks_map
            if tab_index == 2: return self.favorites_tree, self.favorites_map
            if tab_index == 3: return self.recently_played_tree, self.recently_played_map
            if tab_index == 4: return self.playlist_songs_tree, self.playlist_songs_map
        except tk.TclError: pass
        return None, None
    def show_context_menu(self, event):
        tree = event.widget
        selected_item = tree.focus()
        if selected_item: self.context_menu.post(event.x_root, event.y_root)
    def download_selected_song(self):
        tree, track_map = self.get_active_tree_and_map()
        if not tree: return
        selected_item = tree.focus()
        if not selected_item: return
        song = track_map.get(selected_item)
        if not song: return
        song_id, title, _, _, _, filepath, _, _, _, downloaded = song
        if downloaded: messagebox.showinfo("Already Downloaded", f"'{title}' is already available offline."); return
        original_path = filepath; filename = os.path.basename(original_path); offline_path = os.path.join("offline_music", filename)
        try: shutil.copy2(original_path, offline_path); database.update_song_filepath_and_status(song_id, offline_path, 1); messagebox.showinfo("Download Complete", f"'{title}' has been downloaded."); self.load_all_data(self.search_var.get() or None)
        except FileNotFoundError: messagebox.showerror("Download Error", f"Could not find file: {original_path}")
        except Exception as e: messagebox.showerror("Download Error", f"An error occurred: {e}")
    def add_to_playlist_dialog(self):
        tree, track_map = self.get_active_tree_and_map()
        if not tree: return
        selected_item = tree.focus()
        if not selected_item: return
        song_to_add = track_map.get(selected_item)
        if not song_to_add: return
        dialog = tk.Toplevel(self.root); dialog.title("Add to Playlist"); dialog.geometry("300x200")
        ttk.Label(dialog, text=f"Add '{song_to_add[1]}' to:").pack(pady=5)
        pl_listbox = tk.Listbox(dialog); pl_listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        playlists = database.get_playlists()
        for p_id, name in playlists: pl_listbox.insert(tk.END, name)
        def on_add():
            if pl_listbox.curselection():
                playlist_name = pl_listbox.get(pl_listbox.curselection()[0])
                playlist_id = next((p_id for p_id, name in playlists if name == playlist_name), None)
                if playlist_id:
                    database.add_song_to_playlist(playlist_id, song_to_add[0])
                    if self.playlist_listbox.curselection() and self.playlist_listbox.get(self.playlist_listbox.curselection()) == playlist_name: self.show_playlist_songs()
                    dialog.destroy()
            else: messagebox.showwarning("No Selection", "Please select a playlist.", parent=dialog)
        ttk.Button(dialog, text="Add", command=on_add).pack(pady=10)
        dialog.transient(self.root); dialog.grab_set(); self.root.wait_window(dialog)
    def load_library(self, query=None):
        all_songs = database.search_songs(query) if query else database.get_all_songs()
        gospel_songs = [s for s in all_songs if s[6] == 'Gospel']; secular_songs = [s for s in all_songs if s[6] == 'Secular']
        self.tracks_map.clear(); self.populate_treeview(self.gospel_tree, gospel_songs, self.tracks_map); self.populate_treeview(self.secular_tree, secular_songs, self.tracks_map)
    def search_library(self): self.load_all_data(self.search_var.get() or None)
    def clear_search(self): self.search_var.set(""); self.load_all_data()
    def load_playlists(self):
        selection = self.playlist_listbox.curselection()
        self.playlist_listbox.delete(0, tk.END); self.playlists = database.get_playlists()
        for p_id, name in self.playlists: self.playlist_listbox.insert(tk.END, name)
        if selection: self.playlist_listbox.selection_set(selection[0])
    def show_playlist_songs(self, event=None):
        if not self.playlist_listbox.curselection(): self.playlist_songs_tree.delete(*self.playlist_songs_tree.get_children()); return
        playlist_name = self.playlist_listbox.get(self.playlist_listbox.curselection()[0])
        playlist_id = next((p[0] for p in self.playlists if p[1] == playlist_name), None)
        if playlist_id: self.populate_treeview(self.playlist_songs_tree, database.get_songs_in_playlist(playlist_id), self.playlist_songs_map)
    def create_new_playlist(self):
        name = simpledialog.askstring("New Playlist", "Enter playlist name:", parent=self.root)
        if name: database.create_playlist(name); self.load_playlists()
    def rename_selected_playlist(self):
        if not self.playlist_listbox.curselection(): return
        playlist_name = self.playlist_listbox.get(self.playlist_listbox.curselection()[0])
        playlist_id = next((p[0] for p in self.playlists if p[1] == playlist_name), None)
        if playlist_id:
            new_name = simpledialog.askstring("Rename", "New name:", initialvalue=playlist_name, parent=self.root)
            if new_name and new_name != playlist_name: database.rename_playlist(playlist_id, new_name); self.load_playlists()
    def delete_selected_playlist(self):
        if not self.playlist_listbox.curselection(): return
        playlist_name = self.playlist_listbox.get(self.playlist_listbox.curselection()[0])
        if messagebox.askyesno("Delete", f"Delete '{playlist_name}'?"):
            playlist_id = next((p[0] for p in self.playlists if p[1] == playlist_name), None)
            if playlist_id: database.delete_playlist(playlist_id); self.load_playlists(); self.playlist_songs_tree.delete(*self.playlist_songs_tree.get_children())
    def load_favorites(self): self.populate_treeview(self.favorites_tree, database.get_favorite_songs(), self.favorites_map)
    def load_recently_played(self): self.populate_treeview(self.recently_played_tree, database.get_recently_played(), self.recently_played_map)
    def play_selected_song(self, event=None):
        tree, track_map = self.get_active_tree_and_map()
        if tree and track_map:
            selected_item = tree.focus()
            if selected_item:
                track = track_map.get(selected_item)
                if track: self.current_track = track; self.load_track(); self.toggle_play_pause(force_play=True)
    def on_closing(self): self.save_state(); self.root.destroy()
    def save_state(self):
        if self.current_track and pygame.mixer.music.get_busy():
            pos = (pygame.mixer.music.get_pos() / 1000.0)
            database.set_app_state('last_played_song_id', str(self.current_track[0])); database.set_app_state('last_played_position', str(pos))
        else: database.set_app_state('last_played_song_id', '')
    def load_state(self):
        song_id = database.get_app_state('last_played_song_id')
        if song_id and song_id.isdigit():
            track = database.get_song_by_id(int(song_id))
            if track: self.current_track = track; self.load_track(); self.start_pos = float(database.get_app_state('last_played_position') or 0.0); self.status_label.config(text=f"Resumed at {int(self.start_pos)}s")
    def toggle_favorite(self):
        if not self.current_track: return
        database.set_favorite_status(self.current_track[0], 1 - self.current_track[8])
        self.current_track = database.get_song_by_id(self.current_track[0])
        self.update_favorite_button(); self.load_all_data(self.search_var.get() or None)
    def toggle_favorite_from_context(self):
        tree, track_map = self.get_active_tree_and_map()
        if not tree: return
        selected_item = tree.focus()
        if selected_item:
            song = track_map.get(selected_item)
            if song:
                database.set_favorite_status(song[0], 1 - song[8]); self.load_all_data(self.search_var.get() or None)
                if self.current_track and self.current_track[0] == song[0]: self.current_track = database.get_song_by_id(song[0]); self.update_favorite_button()
    def next_track(self): self.play_adjacent_track(1)
    def prev_track(self): self.play_adjacent_track(-1)
    def play_adjacent_track(self, direction):
        tree, track_map = self.get_active_tree_and_map()
        if not tree or not self.current_track: return
        children = tree.get_children()
        if not children: return
        try:
            current_item_id = next(k for k, v in track_map.items() if v[0] == self.current_track[0] and k in children)
            current_index = children.index(current_item_id)
            next_index = (current_index + direction) % len(children)
            next_item = children[next_index]
            tree.selection_set(next_item); tree.focus(next_item)
            self.current_track = track_map.get(next_item); self.load_track(); self.toggle_play_pause(force_play=True)
        except (StopIteration, ValueError): pass

def main():
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()

if __name__ == '__main__':
    main()
