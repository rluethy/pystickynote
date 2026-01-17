import customtkinter as ctk
import sys
import json


def set_cursor_recursive(widget, cursor):
    """Set cursor on widget and all its tkinter children."""
    try:
        widget.configure(cursor=cursor)
    except:
        print(f"Warning: Could not set cursor {cursor} on {widget}")
    # Recursively set on all tkinter children
    try:
        for child in widget.winfo_children():
            set_cursor_recursive(child, cursor)
    except:
        print(f"Warning: Could not set cursor {cursor} on {widget}")


class ConfirmDialog(ctk.CTkToplevel):
    """Confirmation dialog for delete operations."""

    def __init__(self, parent, note_name, config):
        super().__init__(parent)
        self.result = False
        self.config = config

        self.title("Confirm Delete")
        self.attributes('-topmost', True)
        self.resizable(False, False)

        # Center on parent
        self.transient(parent)
        self.grab_set()

        # Use default CTk theme (matches title bar)

        # Message (use default theme text color)
        label = ctk.CTkLabel(
            self,
            text=f"Are you sure you want to delete '{note_name}'?",
            font=("Arial", int(config.font_size) + 2),
        )
        label.pack(padx=20, pady=(20, 10))

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(10, 20))

        self.no_btn = ctk.CTkButton(
            btn_frame,
            text="No",
            width=85,
            height=30,
            corner_radius=8,
            command=self._on_no,
            fg_color=("#d0d0d0", "#404040"),
            hover_color=("#b0b0b0", "#505050"),
            text_color=("#1a1a1a", "#f0f0f0")
        )
        self.no_btn.pack(side="left", padx=5)

        self.yes_btn = ctk.CTkButton(
            btn_frame,
            text="Yes",
            width=85,
            height=30,
            corner_radius=8,
            command=self._on_yes,
            fg_color=("#ffcccc", "#662222"),
            hover_color=("#ff9999", "#883333"),
            text_color=("#660000", "#ffcccc")
        )
        self.yes_btn.pack(side="left", padx=5)

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_no)

        # Wait for window to be ready before centering
        self.update_idletasks()
        self._center_on_parent(parent)

        # Set cursors after window is fully rendered
        self.after(100, self._set_button_cursors)

    def _set_button_cursors(self):
        """Set hand cursor on buttons after they're fully rendered."""
        set_cursor_recursive(self.no_btn, "hand2")
        set_cursor_recursive(self.yes_btn, "hand2")

    def _center_on_parent(self, parent):
        """Center this dialog on the parent window."""
        self.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_x()
        py = parent.winfo_y()
        w = self.winfo_width()
        h = self.winfo_height()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"+{x}+{y}")

    def _darken_color(self, hex_color):
        """Darken a hex color for hover effect."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = max(0, int(r * 0.8))
        g = max(0, int(g * 0.8))
        b = max(0, int(b * 0.8))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _on_yes(self):
        self.result = True
        self.destroy()

    def _on_no(self):
        self.result = False
        self.destroy()


class StickyNoteWindow(ctk.CTkToplevel):
    """A sticky note window that can be dragged and stays on top."""

    def __init__(self, parent, name, content, config, note_obj, is_new=False):
        super().__init__(parent)
        self.name = name
        self.config = config
        self.note_obj = note_obj
        self.is_new = is_new
        self._drag_x = 0
        self._drag_y = 0

        # Window properties
        self.title(name)
        self.attributes('-topmost', True)

        # Handle no_titlebar setting (not on macOS)
        self.no_titlebar = config.no_titlebar if 'darwin' not in sys.platform else False
        if self.no_titlebar:
            self.overrideredirect(True)

        # Use default CTk theme (matches title bar)

        # Build UI
        self._build_ui(content)

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Set minimum size
        self.minsize(300, 200)

        # Apply transparency after window is ready (Linux compatibility)
        self.update_idletasks()
        self.wm_attributes('-alpha', float(config.alpha))

        # Set cursors after window is fully rendered
        self.after(100, self._set_all_cursors)

    def _build_ui(self, content):
        """Build the note UI components."""
        # Store widgets for cursor setting later
        self.cursor_widgets = []

        # Title label (only if no titlebar)
        if self.no_titlebar:
            title_frame = ctk.CTkFrame(self, fg_color="transparent")
            title_frame.pack(fill="x", padx=10, pady=(10, 0))

            title = ctk.CTkLabel(
                title_frame,
                text=self.name,
                font=("Arial", int(self.config.title_size) + 4, "bold"),
                anchor="center"
            )
            title.pack(fill="x")

            # Enable dragging via title area
            title_frame.bind('<Button-1>', self._start_drag)
            title_frame.bind('<B1-Motion>', self._do_drag)
            title.bind('<Button-1>', self._start_drag)
            title.bind('<B1-Motion>', self._do_drag)

            # Store for cursor setting
            self.cursor_widgets.append((title_frame, "fleur"))
            self.cursor_widgets.append((title, "fleur"))

        # Calculate font size (scale up for better readability)
        font_size = int(self.config.font_size) + 4

        # Text area
        self.textbox = ctk.CTkTextbox(
            self,
            width=int(self.config.width) * 10,
            height=int(self.config.height) * 30,
            font=("Arial", font_size),
            fg_color=self.config.background_color,
            text_color=self.config.text_color,
            border_width=int(self.config.border_width),
            border_color=self.config.text_color
        )
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)
        self.textbox.insert("1.0", content)

        # Store for cursor setting (pencil indicates writing)
        self.cursor_widgets.append((self.textbox, "pencil"))

        # Prevent textbox from interfering with text selection
        # (drag-anywhere only works on the window frame/buttons, not inside textbox)

        # Buttons frame - use default CTk background for contrast
        # Fill X so left/right "grip" areas can stretch to the window edges.
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=0, pady=(0, 12))

        # Center the buttons by surrounding them with expandable spacers.
        # When there's no OS titlebar, those spacers also act as drag "grip" areas.
        grip_height = 30

        left_grip = ctk.CTkFrame(btn_frame, fg_color="transparent", height=grip_height)
        left_grip.pack(side="left", fill="both", expand=True)
        left_grip.pack_propagate(False)

        buttons_parent = ctk.CTkFrame(btn_frame, fg_color="transparent")
        buttons_parent.pack(side="left")

        right_grip = ctk.CTkFrame(btn_frame, fg_color="transparent", height=grip_height)
        right_grip.pack(side="left", fill="both", expand=True)
        right_grip.pack_propagate(False)

        if self.no_titlebar:
            left_grip.bind('<Button-1>', self._start_drag)
            left_grip.bind('<B1-Motion>', self._do_drag)
            right_grip.bind('<Button-1>', self._start_drag)
            right_grip.bind('<B1-Motion>', self._do_drag)
            self.cursor_widgets.append((left_grip, "fleur"))
            self.cursor_widgets.append((right_grip, "fleur"))

        # Nice rounded buttons with subtle styling
        close_btn = ctk.CTkButton(
            buttons_parent,
            text="Close",
            width=85,
            height=30,
            corner_radius=8,
            command=self._on_close,
            fg_color=("#d0d0d0", "#404040"),
            hover_color=("#b0b0b0", "#505050"),
            text_color=("#1a1a1a", "#f0f0f0"),
            font=("Arial", font_size - 2)
        )
        close_btn.pack(side="left", padx=4)
        self.cursor_widgets.append((close_btn, "hand2"))

        delete_btn = ctk.CTkButton(
            buttons_parent,
            text="Delete",
            width=85,
            height=30,
            corner_radius=8,
            command=self._on_delete,
            fg_color=("#ffcccc", "#662222"),
            hover_color=("#ff9999", "#883333"),
            text_color=("#660000", "#ffcccc"),
            font=("Arial", font_size - 2)
        )
        delete_btn.pack(side="left", padx=4)
        self.cursor_widgets.append((delete_btn, "hand2"))

        save_btn = ctk.CTkButton(
            buttons_parent,
            text="Save",
            width=85,
            height=30,
            corner_radius=8,
            command=self._on_save,
            fg_color=("#4a9eff", "#1a5fb4"),
            hover_color=("#3a8eef", "#2a6fc4"),
            text_color="white",
            font=("Arial", font_size - 2)
        )
        save_btn.pack(side="left", padx=4)
        self.cursor_widgets.append((save_btn, "hand2"))

    def _set_all_cursors(self):
        """Set cursors on all widgets after they're fully rendered."""
        for widget, cursor in self.cursor_widgets:
            set_cursor_recursive(widget, cursor)

    def _darken_color(self, hex_color):
        """Darken a hex color for hover effect."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = max(0, int(r * 0.8))
        g = max(0, int(g * 0.8))
        b = max(0, int(b * 0.8))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _start_drag(self, event):
        """Start dragging the window."""
        self._drag_x = event.x
        self._drag_y = event.y

    def _do_drag(self, event):
        """Handle window dragging."""
        x = self.winfo_x() + event.x - self._drag_x
        y = self.winfo_y() + event.y - self._drag_y
        self.geometry(f"+{x}+{y}")

    def _on_close(self):
        """Close the window without saving."""
        self.destroy()
        self.master.destroy()

    def _on_save(self):
        """Save the note content."""
        content = self.textbox.get("1.0", "end-1c")
        self.note_obj[self.name] = content
        with open(self.config.notes_path, 'w') as f:
            json.dump(self.note_obj, f, indent=4)

    def _on_delete(self):
        """Delete the note after confirmation."""
        dialog = ConfirmDialog(self, self.name, self.config)
        self.wait_window(dialog)

        if dialog.result:
            self.note_obj.pop(self.name, None)
            with open(self.config.notes_path, 'w') as f:
                json.dump(self.note_obj, f, indent=4)
            self._on_close()


def _create_hidden_root():
    """Create a hidden root window for the application."""
    root = ctk.CTk()
    root.withdraw()
    return root


def open_note(name, config):
    """Open an existing note for editing."""
    with open(config.notes_path, 'r') as notes:
        note_obj = json.load(notes)

    if name not in note_obj:
        print('No Note Found With That Name')
        exit(1)

    content = note_obj[name]

    root = _create_hidden_root()
    StickyNoteWindow(root, name, content, config, note_obj, is_new=False)
    root.mainloop()


def create_note(name, config):
    """Create a new note."""
    with open(config.notes_path, 'r') as notes:
        note_obj = json.load(notes)

    root = _create_hidden_root()
    StickyNoteWindow(root, name, "", config, note_obj, is_new=True)
    root.mainloop()


def list_notes(config):
    """List all available notes."""
    with open(config.notes_path, 'r') as json_file:
        obj = json.load(json_file)
        print('Available Notes:\n')
        for k in obj.keys():
            print(k)


def delete_note(name, config):
    """Delete a note by name."""
    with open(config.notes_path, "r") as json_file:
        obj = json.load(json_file)

    try:
        del obj[name]
        print(f'Deleted note "{name}".')
    except KeyError:
        print(f'No note found with name "{name}"')
        return

    with open(config.notes_path, "w") as json_file:
        json.dump(obj, json_file, indent=4)
