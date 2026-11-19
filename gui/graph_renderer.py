import math
import tkinter as tk
from typing import Dict, List, Optional, Tuple

class GraphRenderer:
    NODE_RADIUS = 28
    RESOURCE_HALF = 24
    FONT_LABEL = ("Consolas", 8, "bold")
    FONT_NAME = ("Segoe UI", 7)

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self._positions: Dict[str, Tuple[float, float]] = {}
        self._node_items: Dict[str, List[int]] = {}

    def render(self, snapshot: dict, detection_result=None, mode: str = "rag"):
        self.canvas.delete("all")
        processes = snapshot.get("processes", {})
        resources = snapshot.get("resources", {})
        
        if not processes and not resources:
            self._draw_empty()
            return
            
        deadlocked_pids = set()
        deadlocked_rids = set()
        
        if detection_result and detection_result.detected:
            deadlocked_pids = set(detection_result.deadlocked_processes)
            deadlocked_rids = set(detection_result.deadlocked_resources)
            
        positions = self._compute_layout(processes, resources)
        self._positions = positions
        
        if mode == "wfg":
            self._draw_wfg_edges(processes, positions)
        else:
            self._draw_rag_edges(processes, resources, positions)
            
        for pid, p in processes.items():
            x, y = positions.get(pid, (0, 0))
            self._draw_process_node(pid, p, x, y, pid in deadlocked_pids)
            
        for rid, r in resources.items():
            x, y = positions.get(rid, (0, 0))
            self._draw_resource_node(rid, r, x, y, rid in deadlocked_rids)
            
        self._draw_legend(mode)

    def _compute_layout(self, processes: dict, resources: dict) -> Dict[str, Tuple[float, float]]:
        w = int(self.canvas.winfo_width() or 700)
        h = int(self.canvas.winfo_height() or 500)
        cx, cy = w / 2, h / 2
        positions = {}
        pids = list(processes.keys())
        rids = list(resources.keys())
        r_inner = min(cx, cy) * 0.38
        r_outer = min(cx, cy) * 0.70
        
        for i, pid in enumerate(pids):
            angle = 2 * math.pi * i / max(len(pids), 1) - math.pi / 2
            positions[pid] = (cx + r_inner * math.cos(angle), cy + r_inner * math.sin(angle))

        for i, rid in enumerate(rids):
            angle = 2 * math.pi * i / max(len(rids), 1) - math.pi / 2 + math.pi / max(len(rids), 1)
            positions[rid] = (cx + r_outer * math.cos(angle), cy + r_outer * math.sin(angle))
            
        return positions

    def _draw_rag_edges(self, processes: dict, resources: dict, pos: dict):
        for pid, p in processes.items():
            px, py = pos.get(pid, (0, 0))
            for rid in p.get("requested", {}):
                if rid in pos:
                    rx, ry = pos[rid]
                    self._arrow(px, py, rx, ry, "#ef4444", dash=(5, 3), label="wants")
            for rid in p.get("allocated", {}):
                if rid in pos:
                    rx, ry = pos[rid]
                    self._arrow(rx, ry, px, py, "#4ade80", label="holds")

    def _draw_wfg_edges(self, processes: dict, pos: dict):
        holder: Dict[str, List[str]] = {}
        for pid, p in processes.items():
            for rid in p.get("allocated", {}):
                holder.setdefault(rid, []).append(pid)
                
        for pid, p in processes.items():
            px, py = pos.get(pid, (0, 0))
            for rid in p.get("requested", {}):
                for hpid in holder.get(rid, []):
                    if hpid != pid and hpid in pos:
                        hx, hy = pos[hpid]
                        self._arrow(px, py, hx, hy, "#eab308", label="waits-for")

    def _arrow(self, x1, y1, x2, y2, color, dash=None, label=""):
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy) or 1
        ux, uy = dx / length, dy / length
        margin = self.NODE_RADIUS + 4
        sx, sy = x1 + ux * margin, y1 + uy * margin
        ex, ey = x2 - ux * (margin - 4), y2 - uy * (margin - 4)
        kw = {"fill": color, "width": 2, "arrow": tk.LAST, "arrowshape": (10, 12, 4)}
        if dash:
            kw["dash"] = dash
        self.canvas.create_line(sx, sy, ex, ey, **kw)

    def _draw_process_node(self, pid, p, x, y, deadlocked):
        r = self.NODE_RADIUS
        color = p.get("color", "#4ade80")
        state = p.get("state", "running")
        state_colors = {
            "running": color,
            "waiting": "#eab308",
            "blocked": "#ef4444",
            "terminated": "#166534",
            "rolled_back": "#3b82f6",
        }
        fill = state_colors.get(state, color)
        
        if deadlocked:
            self.canvas.create_oval(x-r-6, y-r-6, x+r+6, y+r+6, fill="#ef4444", outline="", stipple="gray50")
            
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline="#f0fdf4", width=2)
        self.canvas.create_text(x, y-6, text=pid, fill="#000000", font=self.FONT_LABEL)
        self.canvas.create_text(x, y+8, text=p.get("name",""), fill="#000000", font=self.FONT_NAME)
        
        sdot_colors = {"running":"#16a34a", "waiting":"#eab308", "blocked":"#ef4444", "terminated":"#166534", "rolled_back":"#3b82f6"}
        sdot = sdot_colors.get(state, "#166534")
        self.canvas.create_oval(x+r-8, y-r, x+r+2, y-r+10, fill=sdot, outline="#f0fdf4", width=1)

    def _draw_resource_node(self, rid, r, x, y, deadlocked):
        h = self.RESOURCE_HALF
        rtype_colors = {
            "mutex": "#1a3a1a", "semaphore": "#1a2e1a",
            "file": "#1e3a1e", "device": "#1a3520",
        }
        fill = rtype_colors.get(r.get("type", "mutex"), "#0f170f")

        if deadlocked:
            self.canvas.create_rectangle(x-h-6, y-h-6, x+h+6, y+h+6, fill="#ef4444", outline="", stipple="gray50")

        self.canvas.create_rectangle(x-h, y-h, x+h, y+h, fill=fill, outline="#4ade80", width=2)
        self.canvas.create_text(x, y-8, text=rid, fill="#f0fdf4", font=self.FONT_LABEL)
        self.canvas.create_text(x, y+4, text=r.get("name",""), fill="#86efac", font=self.FONT_NAME)
        
        total = r.get("total", 1)
        avail = r.get("available", 0)
        dot_r = 4
        spacing = 10
        start_x = x - (total - 1) * spacing / 2
        for i in range(total):
            dot_x = start_x + i * spacing
            dot_color = "#4ade80" if i < avail else "#166534"
            self.canvas.create_oval(dot_x-dot_r, y+12-dot_r, dot_x+dot_r, y+12+dot_r, fill=dot_color, outline="#000000")

    def _draw_legend(self, mode: str):
        items = [
            ("#4ade80", "─────", "Allocation (R→P)"),
            ("#ef4444", "- - -", "Request (P→R)"),
            ("#eab308", "─────", "Wait-For (P→P)"),
            ("#4ade80", "●", "Instance available"),
            ("#166534", "●", "Instance allocated"),
        ] if mode == "rag" else [
            ("#eab308", "─────", "Wait-For (P→P)"),
        ]
        x, y = 12, 12
        for color, sym, label in items:
            self.canvas.create_text(x, y, text=sym, fill=color, font=("Consolas", 9), anchor="w")
            self.canvas.create_text(x+30, y, text=label, fill="#86efac", font=("Segoe UI", 8), anchor="w")
            y += 16

    def _draw_empty(self):
        w = int(self.canvas.winfo_width() or 700)
        h = int(self.canvas.winfo_height() or 500)
        self.canvas.create_text(w//2, h//2, text="No processes or resources.\nAdd some or load a scenario.", fill="#166534", font=("Segoe UI", 13), justify="center")