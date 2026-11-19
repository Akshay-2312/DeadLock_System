import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import queue
import sys
import os
import io

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.resource_manager import ResourceManager
from core.deadlock_detector import DeadlockDetector, DeadlockResult
from core.recovery_engine import RecoveryEngine
from core.simulation_engine import SimulationEngine
from gui.graph_renderer import GraphRenderer

# ================= THEME =================

BG_DARK = "#101010"
BG_PANEL = "#181818"
BG_CARD = "#202020"
BG_INPUT = "#252525"

ACCENT = "#3b82f6"
ACCENT2 = "#2563eb"

WARN = "#eab308"
DANGER = "#ef4444"
SUCCESS = "#22c55e"

TEXT_PRI = "#f5f5f5"
TEXT_SEC = "#a3a3a3"
BORDER = "#333333"

STATE_COLORS = {
    "running": "#22c55e",
    "waiting": "#eab308",
    "blocked": "#ef4444",
    "terminated": "#555555",
    "rolled_back": "#3b82f6",
}


class DeadlockSimulatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Deadlock Detection & Recovery Simulator")
        self.geometry("1400x850")
        self.minsize(1100, 650)
        self.configure(bg=BG_DARK)

        self._setup_style()

        # Backend components - DO NOT REMOVE
        self.manager = ResourceManager()
        self.detector = DeadlockDetector()
        self.recovery = RecoveryEngine()

        self._event_queue = queue.Queue()

        self.sim = SimulationEngine(
            self.manager,
            self._on_sim_event
        )

        self.renderer = None

        self._last_detection = None
        self._last_shown_detection_sig = None
        self._last_snapshot_sig = None

        self._auto_detect = tk.BooleanVar(value=True)
        self._graph_mode = tk.StringVar(value="rag")

        self._pid_counter = [1]
        self._rid_counter = [1]

        self._set_icon()

        self._build_menu()
        self._build_ui()

        self._bind_shortcuts()

        self._start_refresh_loop()
        self._start_event_queue_poll()

    
    def _setup_style(self):

        style = ttk.Style(self)
        style.theme_use("clam")

        # General styling
        style.configure(
            ".",
            background=BG_PANEL,
            foreground=TEXT_PRI,
            font=("Segoe UI", 9)
        )

        style.configure("TFrame", background=BG_PANEL)

        style.configure(
            "TLabel",
            background=BG_PANEL,
            foreground=TEXT_PRI
        )

        # Entry fields - Add Process / Add Resource
        style.configure(
            "TEntry",
            fieldbackground=BG_INPUT,
            background=BG_INPUT,
            foreground=TEXT_PRI,
            insertcolor=ACCENT,
            borderwidth=1,
            padding=5
        )

        style.map(
            "TEntry",
            fieldbackground=[("focus", BG_INPUT)],
            foreground=[("disabled", TEXT_SEC)]
        )

        # Spinboxes
        style.configure(
            "TSpinbox",
            fieldbackground=BG_INPUT,
            background=BG_CARD,
            foreground=TEXT_PRI,
            arrowcolor=ACCENT
        )

        # Comboboxes
        style.configure(
            "TCombobox",
            fieldbackground=BG_INPUT,
            background=BG_CARD,
            foreground=TEXT_PRI,
            arrowcolor=ACCENT
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", BG_INPUT)],
            foreground=[("readonly", TEXT_PRI)],
            selectbackground=[("readonly", BG_INPUT)],
            selectforeground=[("readonly", TEXT_PRI)]
        )

        # Standard buttons
        style.configure(
            "TButton",
            background=BG_CARD,
            foreground=TEXT_PRI,
            padding=7,
            borderwidth=1,
            relief="flat"
        )

        style.map(
            "TButton",
            background=[("active", ACCENT)],
            foreground=[("active", BG_DARK)]
        )

        # Accent button
        style.configure(
            "Accent.TButton",
            background=ACCENT,
            foreground=BG_DARK,
            padding=8
        )

        style.map(
            "Accent.TButton",
            background=[("active", ACCENT2)]
        )

        # Danger button
        style.configure(
            "Danger.TButton",
            background=DANGER,
            foreground=TEXT_PRI,
            padding=7
        )

        style.map(
            "Danger.TButton",
            background=[("active", "#dc2626")]
        )

        # Success button
        style.configure(
            "Success.TButton",
            background=SUCCESS,
            foreground=BG_DARK,
            padding=7
        )

        style.map(
            "Success.TButton",
            background=[("active", ACCENT2)]
        )

        # Warning button
        style.configure(
            "Warn.TButton",
            background=WARN,
            foreground=BG_DARK,
            padding=7
        )

        style.map(
            "Warn.TButton",
            background=[("active", "#ca8a04")]
        )

        # Notebook tabs
        style.configure(
            "TNotebook",
            background=BG_DARK,
            borderwidth=0,
            tabmargins=[2, 2, 2, 0]
        )

        style.configure(
            "TNotebook.Tab",
            background=BG_CARD,
            foreground=TEXT_SEC,
            padding=[10, 5]
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", BG_PANEL)],
            foreground=[("selected", ACCENT)]
        )

        # Treeview
        style.configure(
            "Treeview",
            background=BG_INPUT,
            fieldbackground=BG_INPUT,
            foreground=TEXT_PRI,
            borderwidth=0,
            rowheight=25,
            font=("Consolas", 9)
        )

        style.map(
            "Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", BG_DARK)]
        )

        style.configure(
            "Treeview.Heading",
            background=BG_CARD,
            foreground=ACCENT,
            font=("Consolas", 9, "bold"),
            relief="flat"
        )

        style.map(
            "Treeview.Heading",
            background=[("active", BG_CARD)]
        )

    def _build_menu(self):
        menubar = tk.Menu(self, bg=BG_DARK, fg=TEXT_PRI)
        file_menu = tk.Menu(menubar, tearoff=0, bg=BG_PANEL, fg=TEXT_PRI)
        file_menu.add_command(label="Export Event Log…", command=self._export_log, accelerator="")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0, bg=BG_PANEL, fg=TEXT_PRI)
        edit_menu.add_command(label="Run Detection", command=self._run_detection, accelerator="Ctrl+D")
        edit_menu.add_command(label="Run Simulation", command=self._run_simulation, accelerator="Ctrl+R")
        edit_menu.add_command(label="Load Scenario", command=self._load_scenario, accelerator="Ctrl+L")
        edit_menu.add_separator()
        edit_menu.add_command(label="Stop Simulation", command=self._stop_simulation, accelerator="Esc")
        edit_menu.add_command(label="Clear Log", command=self._clear_log, accelerator="Ctrl+Del")
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear Everything", command=self._clear_all)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = tk.Menu(menubar, tearoff=0, bg=BG_PANEL, fg=TEXT_PRI)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    # ── Window icon ──────────────────────────────────────────────────────────

    def _set_icon(self):
        """Generate a padlock icon and set it as the window icon."""
        try:
            from PIL import Image, ImageDraw
            size = 64
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            green = (74, 222, 128, 255)   # #4ade80
            dark = (10, 20, 10, 255)
            # Lock body
            draw.rounded_rectangle([12, 28, 52, 56], radius=6, fill=dark, outline=green, width=3)
            # Shackle
            draw.arc([20, 8, 44, 36], start=180, end=0, fill=green, width=3)
            draw.line([(20, 22), (20, 28)], fill=green, width=3)
            draw.line([(44, 22), (44, 28)], fill=green, width=3)
            # Keyhole
            draw.ellipse([28, 36, 36, 44], fill=green)
            draw.rectangle([30, 42, 34, 48], fill=green)
            # Convert to PhotoImage
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            photo = tk.PhotoImage(data=buf.read())
            self.iconphoto(True, photo)
            self._icon_photo = photo  # prevent GC
        except Exception:
            pass  # gracefully skip if Pillow not available

    # ── Keyboard shortcuts ───────────────────────────────────────────────────

    def _bind_shortcuts(self):
        """Global keyboard shortcuts for common actions."""
        self.bind("<Control-d>", lambda e: self._run_detection())
        self.bind("<Control-D>", lambda e: self._run_detection())
        self.bind("<Control-l>", lambda e: self._load_scenario())
        self.bind("<Control-L>", lambda e: self._load_scenario())
        self.bind("<Control-Delete>", lambda e: self._clear_log())
        self.bind("<Escape>", lambda e: self._stop_simulation())
        self.bind("<Control-r>", lambda e: self._run_simulation())
        self.bind("<Control-R>", lambda e: self._run_simulation())

    def _export_log(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt"), ("All files", "*.*")], title="Export Event Log")
        if not path:
            return
        snap = self.manager.get_snapshot()
        try:
            with open(path, "w", encoding="utf-8") as fh:
                for ev in snap["events"]:
                    fh.write(f"[{ev['timestamp']}] {ev['type']}: {ev['message']}\n")
            self._status(f"Event log exported to {path}")
        except OSError as exc:
            messagebox.showerror("Export failed", str(exc))

    def _show_about(self):
        messagebox.showinfo("About", "Deadlock Detection & Recovery Simulator\n\nImplements Resource Allocation Graph, Banker's Algorithm and Wait-For Graph detection, plus four recovery strategies (terminate, preempt, rollback, kill-all).")


    def _build_ui(self):
        self.configure(bg=BG_DARK)

        # Main banner
        hdr = tk.Frame(self, bg=BG_PANEL, height=55)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="⚙  DEADLOCK DETECTION & RECOVERY SIMULATOR",
            bg=BG_PANEL,
            fg=ACCENT,
            font=("Consolas", 15, "bold")
        ).pack(side="left", padx=20, pady=14)

        tk.Label(
            hdr,
            text="SYSTEM MONITORING  •  DEADLOCK ANALYSIS",
            bg=BG_PANEL,
            fg=TEXT_SEC,
            font=("Consolas", 8)
        ).pack(side="right", padx=20)

        # Bottom status bar
        sb = tk.Frame(self, bg=BG_DARK, height=27)
        sb.pack(fill="x", side="bottom")
        sb.pack_propagate(False)

        self._status_var = tk.StringVar(value="Ready")

        tk.Label(
            sb,
            textvariable=self._status_var,
            bg=BG_DARK,
            fg=TEXT_SEC,
            font=("Consolas", 8)
        ).pack(side="left", padx=12)

        self._deadlock_indicator = tk.Label(
            sb,
            text="● NO DEADLOCK",
            bg=BG_DARK,
            fg=SUCCESS,
            font=("Consolas", 8, "bold")
        )
        self._deadlock_indicator.pack(side="right", padx=15)

        # Main three-column layout
        main = tk.Frame(self, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=7, pady=7)

        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=0, minsize=280)
        main.grid_columnconfigure(1, weight=1, minsize=450)
        main.grid_columnconfigure(2, weight=0, minsize=360)

        # LEFT SIDEBAR
        left = tk.Frame(main, bg=BG_PANEL, width=280)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left.grid_propagate(False)

        self._build_left_panel(left)

        # CENTER GRAPH
        center = tk.Frame(main, bg=BG_DARK)
        center.grid(row=0, column=1, sticky="nsew", padx=5)

        self._build_graph_panel(center)

        # RIGHT PANEL
        right = tk.Frame(main, bg=BG_PANEL, width=360)
        right.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        right.grid_propagate(False)

        self._build_right_panel(right)
      
    
    def _build_left_panel(self, parent):

        # 1. Top Action Toolbar
        toolbar = tk.Frame(parent, bg=BG_PANEL)
        toolbar.pack(fill="x", padx=8, pady=10)

        # 2. Create Notebook
        self._left_notebook = ttk.Notebook(parent)
        self._left_notebook.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # 3. Build Original Tabs
        self._build_process_tab(self._left_notebook)
        self._build_resource_tab(self._left_notebook)
        self._build_scenario_tab(self._left_notebook)
        self._build_alloc_tab(self._left_notebook)

        # 4. Get Tab References
        tabs = self._left_notebook.tabs()

        self._process_tab = self._left_notebook.nametowidget(tabs[0])
        self._resource_tab = self._left_notebook.nametowidget(tabs[1])
        self._scenario_tab = self._left_notebook.nametowidget(tabs[2])
        self._alloc_tab = self._left_notebook.nametowidget(tabs[3])

        # 5. Toolbar Buttons
        actions = [
            ("Reset", self._clear_all),
            ("Resource", lambda: self._left_notebook.select(self._resource_tab)),
            ("Scenario", lambda: self._left_notebook.select(self._scenario_tab)),
            ("Allocat", lambda: self._left_notebook.select(self._alloc_tab))
        ]

        for text, command in actions:
            tk.Button(
                toolbar,
                text=text,
                command=command,
                bg=BG_CARD,
                fg=TEXT_PRI,
                activebackground=ACCENT,
                activeforeground=BG_DARK,
                relief="flat",
                font=("Consolas", 8, "bold"),
                padx=5,
                pady=7,
                cursor="hand2"
            ).pack(
                side="left",
                expand=True,
                fill="x",
                padx=2
            )


    def _build_process_tab(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="Processes")
        self._section(f, "Add Process")

        row = ttk.Frame(f); row.pack(fill="x", padx=8, pady=2)
        ttk.Label(row, text="Name:").pack(side="left")
        self._pname_var = tk.StringVar(value="Process-1")
        ttk.Entry(row, textvariable=self._pname_var, width=14).pack(side="right")

        row2 = ttk.Frame(f); row2.pack(fill="x", padx=8, pady=2)
        ttk.Label(row2, text="Priority (1-5):").pack(side="left")
        self._ppri_var = tk.IntVar(value=2)
        ttk.Spinbox(row2, from_=1, to=5, textvariable=self._ppri_var, width=4).pack(side="right")

        ttk.Button(f, text="+Add Process", style="Accent.TButton", command=self._add_process).pack(fill="x", padx=8, pady=4)

        self._section(f, "Active Processes")
        tree_wrap = ttk.Frame(f)
        tree_wrap.pack(fill="both", expand=True, padx=8, pady=(0, 4))
        columns = ("state", "pri", "holds", "wants")
        self._proc_tree = ttk.Treeview(tree_wrap, columns=columns, show="tree headings", height=8, selectmode="browse")
        self._proc_tree.heading("#0", text="Process")
        self._proc_tree.column("#0", width=110, anchor="w")
        self._proc_tree.heading("state", text="State")
        self._proc_tree.column("state", width=70, anchor="center")
        self._proc_tree.heading("pri", text="Pri")
        self._proc_tree.column("pri", width=30, anchor="center")
        self._proc_tree.heading("holds", text="Holds")
        self._proc_tree.column("holds", width=70, anchor="w")
        self._proc_tree.heading("wants", text="Wants")
        self._proc_tree.column("wants", width=70, anchor="w")
        
        for state, color in STATE_COLORS.items():
            self._proc_tree.tag_configure(state, foreground=color)
            
        pscroll = ttk.Scrollbar(tree_wrap, orient="vertical", command=self._proc_tree.yview)
        self._proc_tree.configure(yscrollcommand=pscroll.set)
        self._proc_tree.pack(side="left", fill="both", expand=True)
        pscroll.pack(side="right", fill="y")

        btn_row = ttk.Frame(f); btn_row.pack(fill="x", padx=8, pady=2)
        ttk.Button(btn_row, text="✗ Terminate", style="Danger.TButton", command=self._terminate_selected).pack(side="left", expand=True, fill="x", padx=(0, 2))
        ttk.Button(btn_row, text="↩ Rollback", style="Warn.TButton", command=self._rollback_selected).pack(side="right", expand=True, fill="x", padx=(2, 0))

    def _build_resource_tab_action(self):
        self._add_resource()

    def _build_scenario_tab(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="Scenarios")

        self._section(f, "Preset Scenarios")

        scenarios = [
            ("dining_philosophers", "🍝 Dining Philosophers"),
            ("bankers_classic", "🏦 Banker's Classic (safe)"),
            ("producer_consumer", "📦 Producer-Consumer"),
            ("readers_writers", "📖 Readers-Writers"),
            ("random_chaos", "🎲 Random Chaos"),
        ]

        self._scenario_var = tk.StringVar(value="dining_philosophers")

        for val, label in scenarios:
            ttk.Radiobutton(
                f,
                text=label,
                variable=self._scenario_var,
                value=val
            ).pack(anchor="w", padx=12, pady=2)

        ttk.Button(
            f,
            text="Load Scenario",
            style="Accent.TButton",
            command=self._load_scenario
        ).pack(fill="x", padx=8, pady=4)

        ttk.Button(
            f,
            text="▶ Run Simulation Steps",
            style="Success.TButton",
            command=self._run_simulation
        ).pack(fill="x", padx=8, pady=2)

        ttk.Button(
            f,
            text="⏹ Stop",
            command=self._stop_simulation
        ).pack(fill="x", padx=8, pady=2)

        self._section(f, "Simulation Speed")

        spd_row = ttk.Frame(f)
        spd_row.pack(fill="x", padx=8, pady=2)

        ttk.Label(
            spd_row,
            text="Delay (s):"
        ).pack(side="left")

        self._speed_var = tk.DoubleVar(value=0.6)

        ttk.Scale(
            spd_row,
            from_=0.1,
            to=2.0,
            variable=self._speed_var,
            orient="horizontal",
            command=lambda v: self.sim.set_speed(float(v))
        ).pack(side="right", fill="x", expand=True)

        self._section(f, "Clear")

        ttk.Button(
            f,
            text="Clear Everything",
            style="Danger.TButton",
            command=self._clear_all
        ).pack(fill="x", padx=8, pady=4)

    
    def _build_alloc_tab(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="Allocate")

        self._section(f, "Manual Allocation")

        row = ttk.Frame(f)
        row.pack(fill="x", padx=8, pady=3)

        ttk.Label(row, text="Process:").pack(side="left")

        self._alloc_pid = tk.StringVar()
        self._alloc_pid_cb = ttk.Combobox(
            row,
            textvariable=self._alloc_pid,
            width=14,
            state="readonly"
        )
        self._alloc_pid_cb.pack(side="right")

        row2 = ttk.Frame(f)
        row2.pack(fill="x", padx=8, pady=3)

        ttk.Label(row2, text="Resource:").pack(side="left")

        self._alloc_rid = tk.StringVar()
        self._alloc_rid_cb = ttk.Combobox(
            row2,
            textvariable=self._alloc_rid,
            width=14,
            state="readonly"
        )
        self._alloc_rid_cb.pack(side="right")

        row3 = ttk.Frame(f)
        row3.pack(fill="x", padx=8, pady=3)

        ttk.Label(row3, text="Count:").pack(side="left")

        self._alloc_count = tk.IntVar(value=1)

        ttk.Spinbox(
            row3,
            from_=1,
            to=10,
            textvariable=self._alloc_count,
            width=5
        ).pack(side="right")

        ttk.Button(
            f,
            text="Request Resource",
            style="Accent.TButton",
            command=self._manual_request
        ).pack(fill="x", padx=8, pady=4)

        ttk.Button(
            f,
            text="Release Resource",
            command=self._manual_release
        ).pack(fill="x", padx=8, pady=2)

    
    
    def _build_graph_panel(self, parent):

        # Graph header
        header = tk.Frame(parent, bg=BG_PANEL, height=42)
        header.pack(fill="x", pady=(0, 5))
        header.pack_propagate(False)

        tk.Label(
            header,
            text="RESOURCE ALLOCATION GRAPH",
            bg=BG_PANEL,
            fg=ACCENT,
            font=("Consolas", 10, "bold")
        ).pack(side="left", padx=12, pady=12)

        # Graph controls
        ctrl = tk.Frame(parent, bg=BG_PANEL)
        ctrl.pack(fill="x", padx=5, pady=5)

        tk.Label(
            ctrl,
            text="Graph View:",
            bg=BG_PANEL,
            fg=TEXT_SEC,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=5)

        self._graph_mode = tk.StringVar(value="rag")

        for val, label in [
            ("rag", "Resource Alloc Graph"),
            ("wfg", "Wait-For Graph")
        ]:
            tk.Radiobutton(
                ctrl,
                text=label,
                variable=self._graph_mode,
                value=val,
                bg=BG_PANEL,
                fg=TEXT_PRI,
                selectcolor=BG_CARD,
                activebackground=BG_PANEL,
                activeforeground=ACCENT,
                font=("Segoe UI", 8),
                command=self._refresh_graph
            ).pack(side="left", padx=5)

        self._auto_detect = tk.BooleanVar(value=True)

        tk.Checkbutton(
            ctrl,
            text="✓ Auto-detect on change",
            variable=self._auto_detect,
            bg=BG_PANEL,
            fg=ACCENT,
            selectcolor=BG_CARD,
            activebackground=BG_PANEL,
            font=("Segoe UI", 8)
        ).pack(side="right", padx=5)

        # Graph legend
        legend = tk.Frame(parent, bg=BG_CARD)
        legend.pack(fill="x", padx=5, pady=5)

        legend_items = [
            ("━", "Allocation (R→P)", "#22c55e"),
            ("➜", "Request (P→R)", "#ef4444"),
            ("⟶", "Wait-For (P→P)", "#38bdf8"),
            ("■", "Available", "#22c55e"),
            ("■", "Allocated", "#ef4444")
        ]

        for symbol, label, color in legend_items:
            tk.Label(
                legend,
                text=f"{symbol} {label}",
                bg=BG_CARD,
                fg=color,
                font=("Consolas", 7)
            ).pack(side="left", padx=5, pady=8)

        # Graph canvas
        self._graph_canvas = tk.Canvas(
            parent,
            bg="#050a18",
            highlightthickness=1,
            highlightbackground=BORDER
        )
        self._graph_canvas.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        self.renderer = GraphRenderer(self._graph_canvas)

        # Bottom information
        footer = tk.Frame(parent, bg=BG_CARD)
        footer.pack(fill="x", padx=5, pady=5)

        tk.Label(
            footer,
            text="● PROCESS NODES     ■ RESOURCE NODES     ↻ DEADLOCK CYCLE",
            bg=BG_CARD,
            fg=ACCENT,
            font=("Consolas", 8, "bold")
        ).pack(pady=8)

       
    def _build_right_panel(self, parent):
        nb = ttk.Notebook(parent)
        nb.pack(fill="both", expand=True, padx=4, pady=4)

        self._build_detection_tab(nb)
        self._build_resource_tab(nb)
        self._build_log_tab(nb)
   
    def _build_recovery_tab(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="Recovery")

        self._section(f, "Recovery Strategy")

        strategies = [
            ("terminate", "Kill Victim",
            "Terminate lowest-priority process", "Danger.TButton"),
            ("preempt", "Preempt Resource",
            "Take resource from a waiting process", "Warn.TButton"),
            ("rollback", "Rollback Process",
            "Reset victim and release resources", "Success.TButton"),
            ("kill_all", "Kill All",
            "Terminate all deadlocked processes", "Danger.TButton"),
        ]

        for val, label, desc, style in strategies:
            row = ttk.Frame(f)
            row.pack(fill="x", padx=8, pady=3)

            ttk.Button(
                row,
                text=label,
                style=style,
                width=15,
                command=lambda v=val: self._run_recovery(v)
            ).pack(side="left")

            ttk.Label(
                row,
                text=desc,
                foreground=TEXT_SEC,
                font=("Segoe UI", 7)
            ).pack(side="left", padx=6)

        self._section(f, "Recovery Log")

        self._rec_text = tk.Text(
            f,
            bg=BG_INPUT,
            fg=TEXT_PRI,
            font=("Consolas", 8),
            wrap="word",
            state="disabled",
            borderwidth=0
        )

        self._rec_text.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=4
        )

        self._rec_text.tag_config("step", foreground=ACCENT2)
        self._rec_text.tag_config("success", foreground=SUCCESS)
        self._rec_text.tag_config("error", foreground=DANGER)
        self._rec_text.tag_config("cost", foreground=WARN)
        self._rec_text.tag_config(
            "head",
            foreground=ACCENT,
            font=("Consolas", 9, "bold")
        )

    
    def _build_detection_tab(self, nb):

        f = ttk.Frame(nb)
        nb.add(f, text="Detection")

        self._section(f, "Choose Algorithm")

        self._algo_var = tk.StringVar(value="rag")

        algorithms = [
            ("rag", "Resource Allocation Graph"),
            ("bankers", "Banker's Algorithm"),
            ("wfg", "Wait-For Graph")
        ]

        for val, label in algorithms:
            ttk.Radiobutton(
                f,
                text=label,
                variable=self._algo_var,
                value=val
            ).pack(anchor="w", padx=15, pady=5)

        ttk.Button(
            f,
            text="▶ Run Detection",
            style="Success.TButton",
            command=self._run_detection
        ).pack(fill="x", padx=10, pady=12)

        self._section(f, "Result")

        self._det_result_frame = tk.Frame(
            f,
            bg=BG_CARD
        )
        self._det_result_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

        self._det_result_text = tk.Text(
            self._det_result_frame,
            bg=BG_INPUT,
            fg=TEXT_PRI,
            font=("Consolas", 9),
            wrap="word",
            state="disabled",
            borderwidth=0,
            padx=10,
            pady=10
        )

        scroll = ttk.Scrollbar(
            self._det_result_frame,
            command=self._det_result_text.yview
        )

        self._det_result_text.configure(
            yscrollcommand=scroll.set
        )

        self._det_result_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(side="right", fill="y")

        self._det_result_text.tag_config(
            "ok", foreground=SUCCESS
        )

        self._det_result_text.tag_config(
            "bad", foreground=DANGER
        )

        self._det_result_text.tag_config(
            "warn", foreground=WARN
        )

        self._det_result_text.tag_config(
            "head",
            foreground=ACCENT,
            font=("Consolas", 10, "bold")
        )

        self._det_result_text.tag_config(
            "cycle", foreground="#ef4444"
        )

   
    def _build_resource_tab(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="Resources")

        self._section(f, "Add Resource")

        row = ttk.Frame(f)
        row.pack(fill="x", padx=8, pady=2)

        ttk.Label(row, text="Name:").pack(side="left")

        self._rname_var = tk.StringVar(value="Mutex-1")

        ttk.Entry(
            row,
            textvariable=self._rname_var,
            width=14
        ).pack(side="right")

        row2 = ttk.Frame(f)
        row2.pack(fill="x", padx=8, pady=2)

        ttk.Label(row2, text="Instances:").pack(side="left")

        self._rinst_var = tk.IntVar(value=1)

        ttk.Spinbox(
            row2,
            from_=1,
            to=10,
            textvariable=self._rinst_var,
            width=4
        ).pack(side="right")

        row3 = ttk.Frame(f)
        row3.pack(fill="x", padx=8, pady=2)

        ttk.Label(row3, text="Type:").pack(side="left")

        self._rtype_var = tk.StringVar(value="mutex")

        ttk.Combobox(
            row3,
            textvariable=self._rtype_var,
            width=12,
            state="readonly",
            values=["mutex", "semaphore", "file", "device"]
        ).pack(side="right")

        ttk.Button(
            f,
            text="+Add Resource",
            style="Accent.TButton",
            command=self._add_resource
        ).pack(fill="x", padx=8, pady=4)

        self._section(f, "Active Resources")

        tree_wrap = ttk.Frame(f)
        tree_wrap.pack(fill="both", expand=True, padx=8, pady=(0, 4))

        columns = ("type", "free")

        self._res_tree = ttk.Treeview(
            tree_wrap,
            columns=columns,
            show="tree headings",
            height=8,
            selectmode="browse"
        )

        self._res_tree.heading("#0", text="Resource")
        self._res_tree.column("#0", width=130, anchor="w")

        self._res_tree.heading("type", text="Type")
        self._res_tree.column("type", width=80, anchor="center")

        self._res_tree.heading("free", text="Free/Total")
        self._res_tree.column("free", width=80, anchor="center")

        rscroll = ttk.Scrollbar(
            tree_wrap,
            orient="vertical",
            command=self._res_tree.yview
        )

        self._res_tree.configure(yscrollcommand=rscroll.set)

        self._res_tree.pack(side="left", fill="both", expand=True)
        rscroll.pack(side="right", fill="y")

    def _build_log_tab(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="📋 Event Log")

        self._log_text = tk.Text(f, bg=BG_INPUT, fg=TEXT_PRI, font=("Consolas", 8), wrap="word", state="disabled", borderwidth=0)
        scroll = ttk.Scrollbar(f, command=self._log_text.yview)
        self._log_text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self._log_text.pack(fill="both", expand=True, padx=4, pady=4)
        
        self._log_text.tag_config("allocate",     foreground=ACCENT2)
        self._log_text.tag_config("request",      foreground=WARN)
        self._log_text.tag_config("release",      foreground=ACCENT)
        self._log_text.tag_config("terminate",    foreground=DANGER)
        self._log_text.tag_config("rollback",     foreground="#3b82f6")
        self._log_text.tag_config("state_change", foreground="#22c55e")
        self._log_text.tag_config("scenario",     foreground="#4ade80")
        self._log_text.tag_config("error",        foreground=DANGER)
        self._log_text.tag_config("default",      foreground=TEXT_SEC)

        ttk.Button(f, text="🗑 Clear Log", command=self._clear_log).pack(fill="x", padx=4, pady=(0, 4))

    def _section(self, parent, title):
        f = tk.Frame(parent, bg=BG_PANEL)
        f.pack(fill="x", padx=8, pady=(8, 2))
        tk.Label(f, text=title.upper(), bg=BG_PANEL, fg=ACCENT, font=("Consolas", 8, "bold")).pack(anchor="w")
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=8)

    def _add_process(self):
        name = self._pname_var.get().strip() or f"Process-{self._pid_counter[0]}"
        pri  = self._ppri_var.get()
        pid  = f"P{self._pid_counter[0]}"
        self._pid_counter[0] += 1
        self.manager.add_process(pid, name, pri)
        self._pname_var.set(f"Process-{self._pid_counter[0]}")
        self._refresh(force=True)

    def _add_resource(self):
        name = self._rname_var.get().strip() or f"Resource-{self._rid_counter[0]}"
        inst = self._rinst_var.get()
        rtype = self._rtype_var.get()
        rid  = f"R{self._rid_counter[0]}"
        self._rid_counter[0] += 1
        self.manager.add_resource(rid, name, inst, rtype)
        self._rname_var.set(f"Mutex-{self._rid_counter[0]}")
        self._refresh(force=True)

    def _terminate_selected(self):
        sel = self._proc_tree.selection()
        if not sel:
            return
        pid = sel[0] 
        name = self._proc_tree.item(pid, "text")
        if not messagebox.askyesno("Confirm Termination", f"Terminate {name} ({pid})?\nThis releases its resources and cannot be undone."):
            return
        self.manager.terminate_process(pid, "manual")
        self._refresh(force=True)

    def _rollback_selected(self):
        sel = self._proc_tree.selection()
        if not sel:
            return
        pid = sel[0]
        self.manager.rollback_process(pid)
        self._refresh(force=True)

    def _load_scenario(self):
        name = self._scenario_var.get()
        self._pid_counter[0] = 1
        self._rid_counter[0] = 1
        self.sim.load_scenario(name)
        self._refresh(force=True)
        self._status(f"Scenario loaded: {name}")

    def _run_simulation(self):
        name = self._scenario_var.get()
        self.sim.set_speed(self._speed_var.get())
        self.sim.run_scenario_steps(name)

    def _stop_simulation(self):
        self.sim.stop()

    def _clear_all(self):
        if not messagebox.askyesno("Clear Everything", "Reset all processes, resources and the event log?"):
            return
        self.sim.stop()
        self.manager.clear_all()
        self._last_detection = None
        self._last_shown_detection_sig = None
        self._last_snapshot_sig = None
        self._pid_counter[0] = 1
        self._rid_counter[0] = 1
        self._refresh(force=True)
        self._status("Cleared.")

    def _manual_request(self):
        pid = self._alloc_pid.get().split()[0] if self._alloc_pid.get() else ""
        rid = self._alloc_rid.get().split()[0] if self._alloc_rid.get() else ""
        cnt = self._alloc_count.get()
        if pid and rid:
            self.manager.request_resource(pid, rid, cnt)
            self._refresh(force=True)

    def _manual_release(self):
        pid = self._alloc_pid.get().split()[0] if self._alloc_pid.get() else ""
        rid = self._alloc_rid.get().split()[0] if self._alloc_rid.get() else ""
        cnt = self._alloc_count.get()
        if pid and rid:
            self.manager.release_resource(pid, rid, cnt)
            self._refresh(force=True)

    def _run_detection(self):
        algo   = self._algo_var.get()
        snap   = self.manager.get_snapshot()
        result = self.detector.detect(snap, algo)
        self._last_detection = result
        self._show_detection_result(result)
        self._update_status_bar(result)
        self._refresh_graph()

    def _run_recovery(self, strategy: str):
        if not self._last_detection:
            snap = self.manager.get_snapshot()
            self._last_detection = self.detector.detect(snap, self._algo_var.get())
        if not self._last_detection.detected:
            messagebox.showinfo("No Deadlock", "Nothing to recover from — run detection first.")
            return
        if strategy in ("terminate", "kill_all"):
            n = len(self._last_detection.deadlocked_processes)
            verb = "every deadlocked process" if strategy == "kill_all" else "the lowest-priority deadlocked process"
            if not messagebox.askyesno("Confirm Recovery", f"This will terminate {verb} ({n} affected). Continue?"):
                return
        action = self.recovery.recover(self.manager, self._last_detection, strategy)
        self._show_recovery_result(action)
        self._last_detection = None
        self._refresh(force=True)

    def _show_detection_result(self, result: DeadlockResult):
        t = self._det_result_text
        t.configure(state="normal")
        t.delete("1.0", "end")
        t.insert("end", f"[{result.timestamp}] {result.algorithm}\n", "head")
        t.insert("end", "─" * 40 + "\n", "head")

        if result.detected:
            conclusive = getattr(result, "conclusive", True)
            if conclusive:
                t.insert("end", "⚠DEADLOCK DETECTED!\n\n", "bad")
            else:
                t.insert("end", "POSSIBLE DEADLOCK — UNCONFIRMED\n", "warn")
            t.insert("end", f"Deadlocked processes ({len(result.deadlocked_processes)}):\n", "warn")
            snap = self.manager.get_snapshot()
            for pid in result.deadlocked_processes:
                pname = snap["processes"].get(pid, {}).get("name", pid)
                t.insert("end", f"  • {pid} — {pname}\n", "bad")
            if result.deadlocked_resources:
                t.insert("end", f"\nContested resources ({len(result.deadlocked_resources)}):\n", "warn")
                for rid in result.deadlocked_resources:
                    rname = snap["resources"].get(rid, {}).get("name", rid)
                    t.insert("end", f"  • {rid} — {rname}\n", "bad")
            if result.cycle_path:
                t.insert("end", "\nCycle(s) detected:\n", "warn")
                for c in result.cycle_path:
                    t.insert("end", f"  ↻ {c}\n", "cycle")
            if result.safe_sequence:
                t.insert("end", f"\nPartial safe sequence: {' → '.join(result.safe_sequence)}\n", "warn")
        else:
            t.insert("end", "✓ No deadlock detected\n\n", "ok")
            if result.safe_sequence:
                t.insert("end", f"Safe sequence:\n  {' → '.join(result.safe_sequence)}\n", "ok")
        t.insert("end", f"\n{result.details}\n")
        t.configure(state="disabled")

    def _show_recovery_result(self, action):
        t = self._rec_text
        t.configure(state="normal")
        t.delete("1.0", "end")
        t.insert("end", f"[{action.timestamp}] {action.strategy}\n", "head")
        t.insert("end", "─" * 40 + "\n", "head")
        for step in action.steps:
            tag = "step"
            if "✗" in step or "error" in step.lower():
                tag = "error"
            elif "success" in step.lower() or "✓" in step:
                tag = "success"
            t.insert("end", step + "\n", tag)
        t.insert("end", f"Cost: {action.cost_estimate}\n", "cost")
        t.configure(state="disabled")

    def _update_status_bar(self, result: DeadlockResult):
        if result.detected and getattr(result, "conclusive", True):
            self._deadlock_indicator.configure(text=f"● DEADLOCK ({len(result.deadlocked_processes)} proc)", fg=DANGER)
        elif result.detected:
            self._deadlock_indicator.configure(text=f"● POSSIBLE DEADLOCK ({len(result.deadlocked_processes)} proc, unconfirmed)", fg=WARN)
        else:
            self._deadlock_indicator.configure(text="● NO DEADLOCK", fg=SUCCESS)

    def _start_refresh_loop(self):
        self._refresh_loop()

    def _refresh_loop(self):
        try:
            self._refresh()
        except Exception as exc:
            self._status(f"[refresh error] {exc}")
        self.after(1200, self._refresh_loop)

    def _snapshot_signature(self, snap: dict):
        procs = tuple(sorted(
            (pid, p["state"], p["priority"],
             tuple(sorted(p["allocated"].items())),
             tuple(sorted(p["requested"].items())))
            for pid, p in snap["processes"].items()
        ))
        res = tuple(sorted((rid, r["available"], r["total"]) for rid, r in snap["resources"].items()))
        return (procs, res)

    def _refresh(self, force: bool = False):
        snap = self.manager.get_snapshot()
        sig = self._snapshot_signature(snap)
        unchanged = (not force) and (sig == self._last_snapshot_sig)

        self._update_process_tree(snap["processes"])
        self._update_resource_tree(snap["resources"])

        p_choices = [f"{pid} {p['name']}" for pid, p in snap["processes"].items()]
        r_choices = [f"{rid} {r['name']}" for rid, r in snap["resources"].items()]
        self._alloc_pid_cb["values"] = p_choices
        self._alloc_rid_cb["values"] = r_choices

        self._refresh_log(snap["events"])

        if not unchanged:
            if self._auto_detect.get():
                algo = self._algo_var.get()
                result = self.detector.detect(snap, algo)
                self._last_detection = result
                shown_sig = (result.algorithm, result.detected, getattr(result, "conclusive", True), tuple(sorted(result.deadlocked_processes)))
                if shown_sig != self._last_shown_detection_sig:
                    self._show_detection_result(result)
                    self._last_shown_detection_sig = shown_sig
                self._update_status_bar(result)
            self._refresh_graph()
            self._last_snapshot_sig = sig

    def _refresh_graph(self):
        snap   = self.manager.get_snapshot()
        mode   = self._graph_mode.get()
        result = self._last_detection
        if self.renderer:
            self.renderer.render(snap, result, mode)

    def _update_process_tree(self, processes: dict):
        tree = self._proc_tree
        existing = set(tree.get_children())
        seen = set()
        for pid, p in processes.items():
            seen.add(pid)
            holds = ", ".join(f"{r}×{c}" for r, c in p["allocated"].items()) or "—"
            wants = ", ".join(f"{r}×{c}" for r, c in p["requested"].items()) or "—"
            values = (p["state"], p["priority"], holds, wants)
            if pid in existing:
                if tree.item(pid, "values") != values or tree.item(pid, "text") != p["name"]:
                    tree.item(pid, text=p["name"], values=values, tags=(p["state"],))
            else:
                tree.insert("", "end", iid=pid, text=p["name"], values=values, tags=(p["state"],))
        for pid in existing - seen:
            tree.delete(pid)

    def _update_resource_tree(self, resources: dict):
        tree = self._res_tree
        existing = set(tree.get_children())
        seen = set()
        for rid, r in resources.items():
            seen.add(rid)
            values = (r["type"], f"{r['available']}/{r['total']}")
            if rid in existing:
                if tree.item(rid, "values") != values or tree.item(rid, "text") != r["name"]:
                    tree.item(rid, text=r["name"], values=values)
            else:
                tree.insert("", "end", iid=rid, text=r["name"], values=values)
        for rid in existing - seen:
            tree.delete(rid)

    def _refresh_log(self, events):
        t = self._log_text
        t.configure(state="normal")
        t.delete("1.0", "end")
        for ev in reversed(events[-60:]):
            tag = ev.get("type", "default")
            t.insert("end", f"[{ev['timestamp']}] ", "default")
            t.insert("end", ev["message"] + "\n", tag)
        t.configure(state="disabled")

    def _clear_log(self):
        self._log_text.configure(state="normal")
        self._log_text.delete("1.0", "end")
        self._log_text.configure(state="disabled")

    def _status(self, msg: str):
        self._status_var.set(msg)

    def _on_sim_event(self, event_type: str, message: str):
        self._event_queue.put((event_type, message))

    def _start_event_queue_poll(self):
        self._drain_event_queue()

    def _drain_event_queue(self):
        try:
            while True:
                _event_type, message = self._event_queue.get_nowait()
                self._status(message)
        except queue.Empty:
            pass
        self.after(150, self._drain_event_queue)

def main():
    app = DeadlockSimulatorApp()
    app.mainloop()

if __name__ == "__main__":
    main()