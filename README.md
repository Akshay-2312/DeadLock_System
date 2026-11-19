# ⚙️ Deadlock-Simulator — Real-Time OS Deadlock Engine

### Never freeze your system. Interactive **deadlock detection, cycle visualization & automated recovery** in real time.

_Your desktop Operating Systems concurrency lab — 3 detection algorithms, 4 recovery strategies, 5 preset scenarios, thread-safe state engine & native dark-mode graph canvas._

**Resource Allocation Graph (RAG) • Banker's Algorithm • Wait-For Graph (WFG) • Victim Termination • Resource Preemption • Process Rollback • Kill-All Recovery • 100% Python**

---

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/UI-Tkinter%20Dark%20Mode-3b82f6?logo=python&logoColor=white)](#%EF%B8%8F-key-features)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20Mandatory-22c55e)](#%E2%9A%A1-quick-start)
[![Unit Tests](https://img.shields.io/badge/Unit%20Tests-18%20Cases-22c55e?logo=pytest&logoColor=white)](#%E2%9A%A1-quick-start)

[![stars](https://custom-icon-badges.demolab.com/github/stars/Akshay-2312/DeadLock_System?logo=star&style=flat)](https://github.com/Akshay-2312/DeadLock_System/stargazers)
[![open issues](https://custom-icon-badges.demolab.com/github/issues-raw/Akshay-2312/DeadLock_System?logo=issue)](https://github.com/Akshay-2312/DeadLock_System/issues)
[![license](https://custom-icon-badges.demolab.com/github/license/Akshay-2312/DeadLock_System?logo=law)](https://github.com/Akshay-2312/DeadLock_System)
[![last commit](https://custom-icon-badges.demolab.com/github/last-commit/Akshay-2312/DeadLock_System?logo=history&logoColor=white)](https://github.com/Akshay-2312/DeadLock_System/commits/main)
[![code size](https://custom-icon-badges.demolab.com/github/languages/code-size/Akshay-2312/DeadLock_System?logo=file-code&logoColor=white)](https://github.com/Akshay-2312/DeadLock_System)
[![pr closed](https://custom-icon-badges.demolab.com/github/issues-pr-closed/Akshay-2312/DeadLock_System?color=purple&logo=git-pull-request&logoColor=white)](https://github.com/Akshay-2312/DeadLock_System/pulls?q=is%3Apr+is%3Aclosed)
[![tag](https://custom-icon-badges.demolab.com/github/v/tag/Akshay-2312/DeadLock_System?logo=tag&logoColor=white)](https://github.com/Akshay-2312/DeadLock_System/tags)
[![fork](https://custom-icon-badges.demolab.com/github/forks/Akshay-2312/DeadLock_System?logo=fork)](https://github.com/Akshay-2312/DeadLock_System/network/members)
[![watch](https://custom-icon-badges.demolab.com/github/watchers/Akshay-2312/DeadLock_System?logo=eye)](https://github.com/Akshay-2312/DeadLock_System/watchers)

[⚡ Quick Start](#-quick-start) • [💡 Key Features](#-key-features) • [🔄 How It Works](#-how-it-works) • [🎯 What It Solves](#-what-deadlock-simulator-solves--core-os-pain-points--use-cases) • [📊 Algorithms at a Glance](#-algorithms--recovery-at-a-glance) • [📖 Architecture](#-architecture--module-reference)

</div>

---

## 🖼️ Main Dashboard

<div align="center">
  <img src="./Screenshots/Dining Philosophers - Detection.png" alt="Deadlock Simulator Dashboard" width="800"/>
</div>

---

### 🧩 Complete Concurrency & Deadlock Toolkit

_Simulate resource contention, inspect live cycle topology, verify safety sequences, and resolve deadlocks with zero external runtime overhead._

<table>
  <tr>
    <td align="center" width="130">
      🔍<br/>
      <b>RAG Cycle DFS</b><br/>
      <sub><code>O(V + E)</code></sub>
    </td>
    <td align="center" width="130">
      🏦<br/>
      <b>Banker's Safety</b><br/>
      <sub><code>O(n² · m)</code></sub>
    </td>
    <td align="center" width="130">
      🕸️<br/>
      <b>Wait-For Graph</b><br/>
      <sub><code>O(P²)</code></sub>
    </td>
    <td align="center" width="130">
      🎯<br/>
      <b>Kill Victim</b><br/>
      <sub>Priority-Based</sub>
    </td>
    <td align="center" width="130">
      ⚡<br/>
      <b>Preempt Resource</b><br/>
      <sub>Low Disruption</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="130">
      ↩️<br/>
      <b>Process Rollback</b><br/>
      <sub>Checkpoint Reset</sub>
    </td>
    <td align="center" width="130">
      💥<br/>
      <b>Kill All</b><br/>
      <sub>Nuclear Option</sub>
    </td>
    <td align="center" width="130">
      🍝<br/>
      <b>5 OS Scenarios</b><br/>
      <sub>Preset & Chaos</sub>
    </td>
    <td align="center" width="130">
      🎨<br/>
      <b>Live Canvas</b><br/>
      <sub>RAG ↔ WFG View</sub>
    </td>
    <td align="center" width="130">
      🔒<br/>
      <b>Thread-Safe Core</b><br/>
      <sub>Lock + Snapshot</sub>
    </td>
  </tr>
</table>

<sub>⚡ All algorithms operate on immutable point-in-time snapshots via <code>ResourceManager.get_snapshot()</code> — zero race conditions, instant visual feedback</sub>

---

## 🤔 Why Deadlock-Simulator?

**Stop guessing how resource contention locks up your system:**

- <img src="https://img.shields.io/badge/✗-e74c3c?style=flat-square" height="16"/> Static textbook graphs that don't react to live allocations or releases
- <img src="https://img.shields.io/badge/✗-e74c3c?style=flat-square" height="16"/> False-positive cycle warnings on multi-instance resources without safety verification
- <img src="https://img.shields.io/badge/✗-e74c3c?style=flat-square" height="16"/> Opaque recovery trade-offs between killing processes, rolling back, or preempting mutexes
- <img src="https://img.shields.io/badge/✗-e74c3c?style=flat-square" height="16"/> Tedious manual matrix math for `Allocation`, `MaxNeed`, `Need`, and `Available` vectors

**Deadlock-Simulator solves this:**

- ✅ **Live Bipartite & Wait-For Rendering** — Dual-ring `tk.Canvas` graph updates dynamically with solid green allocation edges, dashed red request edges, and red deadlock halos
- ✅ **Conclusive vs. Unconfirmed Cycle Classification** — RAG automatically flags single-instance cycles as confirmed deadlocks and marks multi-instance cycles as `conclusive=False` until Banker's confirms
- ✅ **4 One-Click Recovery Engines** — Execute Victim Termination, Resource Preemption, Process Rollback, or Kill All with step-by-step audit logs and OS disruption cost estimates
- ✅ **Built-In Concurrency Scenarios** — Step through Dining Philosophers, Banker's Classic, Producer-Consumer, Readers-Writers, or Random Chaos at `0.1s`–`2.0s` speed

---

## 🔄 How It Works

```text
┌────────────────────────────────────────────────────────────────────┐
│  User Controls (GUI / Shortcuts)  │  SimulationEngine (Daemon)     │
│  Add Process / Resource / Request │  5 Preset & Chaos Scenarios    │
└──────────────────┬────────────────┴───────────────┬────────────────┘
                   │                                │
                   └───────────────┬────────────────┘
                                   ▼
                 ┌───────────────────────────────────┐
                 │  ResourceManager (threading.Lock) │
                 │  • Processes & Resource Pools     │
                 │  • Allocation & Request Tables    │
                 │  • Rolling Event Log (500 cap)    │
                 └─────────────────┬─────────────────┘
                                   │ get_snapshot() (immutable copy)
        ┌──────────────────────────┼──────────────────────────┐
        ▼                          ▼                          ▼
┌────────────────┐       ┌───────────────────┐      ┌─────────────────┐
│ [Engine 1: RAG]│       │ [Engine 2: WFG]   │      │ [Engine 3:      │
│  Bipartite DFS │       │  Process-Only DFS │      │  Banker's]      │
│  Single vs     │       │  Collapsed Wait   │      │  Work/Finish    │
│  Multi-Instance│       │  Edges (P_i → P_j)│      │  Safe Sequence  │
└───────┬────────┘       └─────────┬─────────┘      └────────┬────────┘
        └──────────────────────────┼─────────────────────────┘
                                   ▼
                 ┌───────────────────────────────────┐
                 │      DeadlockDetector Result      │
                 │  detected, conclusive, cycle_path │
                 └─────────────────┬─────────────────┘
                                   │
             ┌─────────────────────┴─────────────────────┐
             ▼                                           ▼
┌─────────────────────────┐                 ┌─────────────────────────┐
│     GraphRenderer       │                 │     RecoveryEngine      │
│  • Dual-Ring tk.Canvas  │                 │  • terminate (victim)   │
│  • RAG ↔ WFG View Mode  │                 │  • preempt (steal + rb) │
│  • Instance Dots & Halo │                 │  • rollback (keep alive)│
└─────────────────────────┘                 │  • kill_all (nuclear)   │
                                            └─────────────────────────┘
```

---

## 🎯 What Deadlock-Simulator Solves — Core OS Pain Points & Use Cases

> **Understanding OS deadlocks requires seeing state transitions, graph cycles, and recovery side effects together.** Deadlock-Simulator unifies state management, multi-algorithm verification, and live graph visualization in one lightweight desktop workspace.

<details>
<summary><b>🔍 1. "A cycle in a Resource Allocation Graph doesn't always mean a deadlock"</b></summary>

In OS theory, a cycle in a Resource Allocation Graph is a **necessary and sufficient** condition for deadlock only when every resource in the cycle has a single instance (`total == 1`). When multi-instance semaphores or device pools are involved, a cycle is only a warning sign.

**How Deadlock-Simulator solves it:**

- **Single-Instance Confirmation** — `DeadlockDetector._rag_detection()` checks `all(resources[r]["total"] == 1 for r in cycle_rids)` across every detected cycle
- **Honest Conclusiveness Flag** — Sets `conclusive=True` when a single-instance cycle is found, and `conclusive=False` when multi-instance resources participate
- **Actionable Guidance** — Prompts the operator to run **Banker's Algorithm** (`_bankers_detection`) to prove whether a safe completion sequence still exists before triggering recovery
- **Safety Caution Injection** — `RecoveryEngine.recover()` prepends a `CAUTION: triggered by an UNCONFIRMED cycle` warning if invoked on a non-conclusive detection result

</details>

<details>
<summary><b>⚖️ 2. "Breaking a deadlock has hidden OS disruption costs"</b></summary>

Terminating a process frees all of its held resources immediately, but destroys unsaved work. Preempting a single resource minimizes work loss, yet may only break one edge of a multi-process cycle.

**How Deadlock-Simulator solves it:**

- **4 Dedicated Strategies** — Compare `terminate`, `preempt`, `rollback`, and `kill_all` directly against the same deadlocked snapshot
- **Priority-Aware Victim Selection** — `_terminate_victim()` and `_rollback()` select the lowest-priority deadlocked process (`priority` 1–5, tie-broken alphabetically for termination)
- **Non-Destructive Survival** — `rollback_process()` returns all held allocations and clears requests while preserving the process in `rolled_back` state
- **Structured `RecoveryAction` Output** — Displays affected PIDs, freed RIDs, step-by-step execution trace, and a clear OS disruption `cost_estimate`

</details>

<details>
<summary><b>🍝 3. "Classic OS concurrency bugs happen too fast to observe in real code"</b></summary>

In production code, race conditions and circular waits trigger in microseconds, leaving developers with frozen threads and no visibility into the exact sequence of resource requests that caused the deadlock.

**How Deadlock-Simulator solves it:**

- **Step-Timed Daemon Simulation** — `SimulationEngine` replays deterministic and randomized allocation sequences on a background thread
- **Adjustable Execution Speed** — Slide delay dynamically between `0.1s` and `2.0s` per step while watching edges form in real time
- **5 Built-In Classic Scenarios** — Load `dining_philosophers`, `bankers_classic`, `producer_consumer`, `readers_writers`, or `random_chaos` in one click
- **Reverse-Chronological Event Log** — Inspect every `allocate`, `request`, `release`, `terminate`, `rollback`, and `scenario` timestamped event or export to `.txt`

</details>

<details>
<summary><b>🕸️ 4. "Bipartite graphs get visually noisy in process-heavy workloads"</b></summary>

When dozens of allocation and request arrows cross between processes and resources, tracing which process is actually blocking which becomes hard to read at a glance.

**How Deadlock-Simulator solves it:**

- **Instant View Switching** — Toggle live between `Resource Alloc Graph` (bipartite `P ↔ R`) and `Wait-For Graph` (process-only `P → P`)
- **Automated Edge Abstraction** — `GraphRenderer._draw_wfg_edges()` collapses `P_i → R_k → P_j` dependencies into clean yellow `P_i → P_j` wait-for arrows
- **Dual-Ring Radial Geometry** — Automatically positions processes on an inner ring (`0.38 × radius`) and resources on an outer ring (`0.70 × radius`)
- **Per-Instance Availability Dots** — Resource rectangles render individual instance dots (bright green for available, dark green for allocated)

</details>

<details>
<summary><b>🔒 5. "Multi-threaded simulations crash or flicker GUI widgets"</b></summary>

Calling Tkinter widget updates from a background simulation thread causes race conditions or crashes, while re-rendering the entire canvas every timer tick creates visual flicker.

**How Deadlock-Simulator solves it:**

- **Lock-Protected State Table** — Every mutation in `ResourceManager` acquires `self._lock` (`threading.Lock`)
- **Thread-Safe Event Queue** — `SimulationEngine` pushes status events via callback into `queue.Queue`, drained safely on the main UI thread every `150ms`
- **Snapshot Signature Diffing** — `DeadlockSimulatorApp._refresh()` computes `_snapshot_signature()` every `1200ms` and only redraws the canvas or re-runs auto-detection when state actually changes

</details>

<details>
<summary><b>🧪 6. "Testing detection & recovery algorithms programmatically without launching a GUI"</b></summary>

Academic and automated test harnesses need to instantiate `ResourceManager`, `DeadlockDetector`, and `RecoveryEngine` headlessly without requiring a display server.

**How Deadlock-Simulator solves it:**

- **Decoupled `core/` Package** — Zero Tkinter imports anywhere inside `core/`; every method accepts and returns plain Python dataclasses and dicts
- **Serializable Results** — `Resource.to_dict()`, `Process.to_dict()`, `DeadlockResult.to_dict()`, and `RecoveryAction.to_dict()` export clean JSON-ready payloads
- **Matrix Export Support** — `ResourceManager.get_allocation_matrix()` outputs `pids`, `rids`, `allocation`, `request`, and `available` structures directly
- **18-Case Unit Test Suite** — Run `tests/test_core.py` via `unittest` or `pytest` in milliseconds

</details>

### Example Playbooks (Integrated Use Cases)

**Playbook A: Classic 2-Process Mutex Deadlock (Manual Setup)**

```txt
1. Add Resources: Mutex-A (1 instance), Mutex-B (1 instance)
2. Add Processes: Worker-1 (pri=2), Worker-2 (pri=2)
3. Allocate / Request:
   • Worker-1 requests Mutex-A  → ✓ Granted (running)
   • Worker-2 requests Mutex-B  → ✓ Granted (running)
   • Worker-1 requests Mutex-B  → ✗ Blocked (waiting)
   • Worker-2 requests Mutex-A  → ✗ Blocked (waiting)
4. Run Detection (RAG / WFG / Banker's):
   Cycle: Worker-1 → [Mutex-B] → Worker-2 → [Mutex-A] → Worker-1
   Outcome: CONFIRMED deadlock (conclusive=True)
```

**Playbook B: Multi-Instance Cycle → Banker's Algorithm Verification**

```txt
1. Scenario: multi-instance semaphore pool (total >= 2)
2. Run RAG Detection:
   • Cycle found involving multi-instance resource
   • Output: POSSIBLE DEADLOCK — UNCONFIRMED (conclusive=False)
3. Switch Detection Algorithm → Banker's Algorithm:
   • Evaluates Need[P][R] = MaxNeed[P][R] - Allocation[P][R]
   • Returns exact safe completion sequence or proves UNSAFE state
```

**Playbook C: Dining Philosophers → Non-Destructive Rollback**

```txt
1. Select Scenario: 🍝 Dining Philosophers → Load Scenario
2. Press Ctrl+R (Run Simulation Steps):
   • P1..P5 each acquire left chopstick (R1..R5)
   • P1..P5 request right chopstick → all enter waiting state
3. Auto-detect triggers:
   • 5 processes CONFIRMED deadlocked on 5 resources
4. Run Rollback Strategy:
   • Victim selected by lowest priority, resources released, state → rolled_back
```

**Playbook D: Headless Python API & Unit Test Verification**

```bash
python tests/test_core.py
# Verifies 7 ResourceManager tests, 6 DeadlockDetector tests, 5 RecoveryEngine tests
```

---

## 📊 Algorithms & Recovery at a Glance

### Detection Engines (`core/deadlock_detector.py`)

| Algorithm                           | Time Complexity | Graph / Data Model                                    | Multi-Instance Safe?                              | Output Highlights                                                          |
| ----------------------------------- | --------------- | ----------------------------------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------- |
| **Resource Allocation Graph (RAG)** | `O(V + E)`      | Directed bipartite graph (`P ↔ R`) via recursive DFS  | Flags as `conclusive=False` & recommends Banker's | `cycle_path`, `deadlocked_processes`, `deadlocked_resources`, `conclusive` |
| **Banker's Algorithm**              | `O(n² · m)`     | `Allocation`, `MaxNeed`, `Need`, `Available` matrices | **Yes** — exact safety check across instances     | `safe_sequence`, unfinished `deadlocked_processes`, `details`              |
| **Wait-For Graph (WFG)**            | `O(P²)`         | Process-only directed graph (`P_i → P_j`) via DFS     | Best for single-instance wait chains              | `cycle_path` (`P1 ⇒ P2`), `deadlocked_processes`                           |

### Recovery Strategies (`core/recovery_engine.py`)

| Strategy                | Key         | Disruption | Victim Selection                                        | Side Effects                                                                                                  |
| ----------------------- | ----------- | ---------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Process Termination** | `terminate` | Medium     | Lowest `priority` (tie-break: `name`)                   | Releases all held resources, clears requests, marks `terminated`                                              |
| **Resource Preemption** | `preempt`   | Low–Medium | Holder of resource wanted by another deadlocked process | Steals 1 resource, grants to waiter, marks victim `rolled_back` (falls back to `_rollback` if no direct edge) |
| **Process Rollback**    | `rollback`  | Low        | Lowest `priority` deadlocked process                    | Releases all held resources, clears requests, keeps process alive (`rolled_back`)                             |
| **Kill All**            | `kill_all`  | High       | Every process in `deadlocked_processes`                 | Terminates all deadlocked processes immediately; frees entire contested pool                                  |

```txt
Decision Matrix:
  Single-instance cycle? ──▶ RAG / WFG gives instant conclusive proof
  Multi-instance pool?   ──▶ Banker's Algorithm verifies SAFE vs UNSAFE sequence
  Need minimal data loss?──▶ Rollback or Preempt preserves victim state
  System stability first?──▶ Terminate lowest-priority victim or Kill All
```

---

## ⚡ Quick Start

### 1) Clone the repository

```bash
git clone https://github.com/Akshay-2312/DeadLock_System.git
cd DeadLock_System
```

### 2) Optional dependencies

Core simulation, detection, recovery, and the Tkinter UI run purely on the **Python standard library** (`tkinter`, `threading`, `dataclasses`, `queue`, `unittest`). Install optional packages only for the generated window icon or running tests via `pytest`:

```bash
pip install Pillow pytest
```

### 3) Launch the Desktop Simulator

```bash
python gui/main_window.py
```

### 4) Run the Unit Test Suite

```bash
# Using Python's built-in unittest runner
python tests/test_core.py

# Or using pytest
python -m pytest tests/ -v
```

### Command & Shortcut Reference

| Shortcut / Action           | Description                                                  |
| --------------------------- | ------------------------------------------------------------ |
| `python gui/main_window.py` | Launch the dark-mode Desktop Deadlock Simulator (`1400×850`) |
| `python tests/test_core.py` | Run all 18 core engine unit tests with verbose output        |
| `Ctrl+D`                    | Run selected deadlock detection algorithm immediately        |
| `Ctrl+R`                    | Execute simulation steps for the currently selected scenario |
| `Ctrl+L`                    | Load the selected preset scenario into `ResourceManager`     |
| `Ctrl+Del`                  | Clear the Event Log panel                                    |
| `Esc`                       | Stop the running background simulation thread                |
| `File → Export Event Log…`  | Save the last 50 recorded events to a `.txt` file            |

---

## 💡 Key Features

### 🧠 Detection & Graph Analysis

| Feature                      | What It Does                                                                                                                       |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 🔍 **RAG Cycle Detection**   | Builds directed request (`P → R`) and allocation (`R → P`) adjacency lists and detects wait cycles via DFS                         |
| 🏦 **Banker's Safety Check** | Computes `Need = MaxNeed - Allocation` (defaulting undeclared `max_need` to full resource pool) and finds safe execution orderings |
| 🕸️ **Wait-For Graph View**   | Abstracts resource nodes into direct `P_i → P_j` wait edges for fast process-level cycle inspection                                |
| ⚠️ **Conclusiveness Guard**  | Distinguishes proven single-instance deadlocks from unconfirmed multi-instance cycles                                              |
| 🔄 **Auto-Detect on Change** | Automatically re-runs detection when `_snapshot_signature()` detects state mutations                                               |

### 🛡️ Recovery & Fault Tolerance

| Feature                            | What It Does                                                                         |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| 🎯 **Lowest-Priority Victim**      | Selects minimum-priority deadlocked process for termination or rollback              |
| ⚡ **Targeted Preemption**         | Transfers an overlapping held/requested resource directly from victim to beneficiary |
| ↩️ **Non-Destructive Rollback**    | Frees held resources while keeping the victim process alive in `rolled_back` state   |
| 💥 **Nuclear Kill-All**            | Terminates all deadlocked processes in one pass with confirmation dialog in UI       |
| 📜 **Step-by-Step Recovery Trace** | Outputs timestamped actions, freed resources, and cost commentary per run            |

### 🖥️ Interactive Dark-Mode GUI & Canvas

| Feature                               | What It Does                                                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 🎨 **Dual-Ring `tk.Canvas` Renderer** | Plots processes on an inner ring and resources on an outer ring with arrow markers                                              |
| 🔴 **Deadlock Halos**                 | Highlights deadlocked processes and contested resources with stippled red outlines                                              |
| 🟢 **Instance Dots**                  | Renders individual capacity dots inside each resource node (`available` vs `allocated`)                                         |
| 📋 **3-Column Workspace**             | Left controls (`Processes`, `Resources`, `Scenarios`, `Allocate`), center live graph, right analysis (`Detection`, `Event Log`) |
| 🔒 **Generated Padlock Icon**         | Dynamically draws a 64×64 PNG padlock window icon at startup via `Pillow` (falls back gracefully if absent)                     |

### ⚙️ Simulation & Architecture

| Feature                              | What It Does                                                                                         |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| 🧵 **Thread-Safe `ResourceManager`** | Guards all reads/writes with `threading.Lock` and returns safe copies via `get_snapshot()`           |
| 🍝 **5 Preset OS Scenarios**         | Includes Dining Philosophers, Banker's Classic, Producer-Consumer, Readers-Writers, and Random Chaos |
| ⏱️ **Variable Step Delay**           | Real-time slider controls background simulation delay between `0.1s` and `2.0s`                      |
| 📨 **Decoupled Event Queue**         | Bridges background simulation threads to Tkinter via `queue.Queue` polled at `150ms`                 |

---

## 📖 Setup & Usage Guide

<details>
<summary><b>🍝 Preset Scenarios Reference</b></summary>

| Scenario ID           | Label                      | Processes                     | Resources                                                             | Typical Behavior                          |
| --------------------- | -------------------------- | ----------------------------- | --------------------------------------------------------------------- | ----------------------------------------- |
| `dining_philosophers` | 🍝 Dining Philosophers     | 5 (`P1`–`P5`, priority 2)     | 5 single-instance chopsticks (`R1`–`R5`, `mutex`)                     | Classic 5-node circular wait deadlock     |
| `bankers_classic`     | 🏦 Banker's Classic (safe) | 4 (`P0`–`P3`, priorities 1–4) | `Tape-Drive` (10), `Disk-Drive` (5), `Printer` (7)                    | Multi-instance safe allocation sequence   |
| `producer_consumer`   | 📦 Producer-Consumer       | 4 (2 Producers, 2 Consumers)  | `Buffer-Mutex` (1), `Full`/`Empty` Semaphores (5), `Printer-Lock` (1) | Contention on single-instance mutex locks |
| `readers_writers`     | 📖 Readers-Writers         | 5 (2 Writers, 3 Readers)      | `DB-Write-Lock` (1), `DB-Read-Lock` (3), `Log-File` (1)               | Write-starvation and lock contention      |
| `random_chaos`        | 🎲 Random Chaos            | 3–6 random processes          | 2–5 random resources (1–3 instances)                                  | 20 randomized requests for stress testing |

</details>

<details>
<summary><b>🐍 Headless Python API Integration</b></summary>

You can drive the simulation, detection, and recovery engines directly from any Python script without starting Tkinter:

```python
from core.resource_manager import ResourceManager
from core.deadlock_detector import DeadlockDetector
from core.recovery_engine import RecoveryEngine

mgr = ResourceManager()
det = DeadlockDetector()
rec = RecoveryEngine()

# Build a 2-process deadlock
mgr.add_process("P1", "Worker-1", priority=4)
mgr.add_process("P2", "Worker-2", priority=1)
mgr.add_resource("R1", "Mutex-A", instances=1, rtype="mutex")
mgr.add_resource("R2", "Mutex-B", instances=1, rtype="mutex")

mgr.request_resource("P1", "R1")  # Granted
mgr.request_resource("P2", "R2")  # Granted
mgr.request_resource("P1", "R2")  # Blocked -> waiting
mgr.request_resource("P2", "R1")  # Blocked -> deadlock!

# Inspect snapshot with RAG
snap = mgr.get_snapshot()
result = det.detect(snap, algorithm="rag")
print(result.detected, result.conclusive, result.cycle_path)

# Recover by terminating lowest-priority victim (P2)
action = rec.recover(mgr, result, strategy="terminate")
print(action.strategy, action.affected_processes, action.cost_estimate)
```

</details>

<details>
<summary><b>🎨 Graph Visual Legend & State Color Palette</b></summary>

#### Canvas Edges & Indicators (`gui/graph_renderer.py`)

| Element                   | Visual Style                     | Meaning                                                        |
| ------------------------- | -------------------------------- | -------------------------------------------------------------- |
| **Allocation Edge**       | Solid Green (`#4ade80`) `R → P`  | Resource currently held by process                             |
| **Request Edge**          | Dashed Red (`#ef4444`) `P → R`   | Process blocked waiting for resource                           |
| **Wait-For Edge**         | Solid Yellow (`#eab308`) `P → P` | Process waiting on resource held by another process (WFG mode) |
| **Resource Dot (Bright)** | `#4ade80` filled circle          | Available resource instance                                    |
| **Resource Dot (Dark)**   | `#166534` filled circle          | Allocated resource instance                                    |
| **Deadlock Halo**         | Stippled Red (`#ef4444`) outline | Process or resource participating in detected deadlock         |

#### Process Lifecycle States (`gui/main_window.py`)

| State         | Color Hex | Trigger                                             |
| ------------- | --------- | --------------------------------------------------- |
| `running`     | `#22c55e` | Process created or resource request granted         |
| `waiting`     | `#eab308` | Resource request exceeded `available_instances`     |
| `blocked`     | `#ef4444` | Explicitly marked blocked via `set_process_state()` |
| `terminated`  | `#555555` | Process terminated manually or by recovery engine   |
| `rolled_back` | `#3b82f6` | Victim rolled back or preempted during recovery     |

</details>

---

## 🐛 Troubleshooting

<details>
<summary><b>Click to expand troubleshooting guide</b></summary>

**`ModuleNotFoundError: No module named 'tkinter'` (Linux)**

- Install your distribution's Tk bindings package (e.g., `sudo apt install python3-tk` on Debian/Ubuntu or `sudo dnf install python3-tkinter` on Fedora).

**Window icon does not appear**

- `DeadlockSimulatorApp._set_icon()` uses `Pillow` (`PIL.Image`, `PIL.ImageDraw`) to render the padlock icon dynamically. If `Pillow` is not installed, the app intentionally skips icon generation and runs normally. Install via `pip install Pillow` if desired.

**Banker's Algorithm reports `UNSAFE` even when no cycle exists in RAG**

- Processes added through the GUI or `SimulationEngine` do not explicitly populate `max_need`. When `max_need` is omitted for a resource, `DeadlockDetector._bankers_detection()` conservatively assumes worst-case demand (`max_need[pid][rid] = resources[rid]["total"]`). Pass explicit `max_need` dictionaries via `ResourceManager.add_process(pid, name, priority, max_need={...})` for exact Banker's claims.

**UI appears without a Recovery tab in the right panel**

- Check `gui/main_window.py` `_build_right_panel()`: ensure `self._build_recovery_tab(nb)` is called instead of duplicating `self._build_resource_tab(nb)`. (Note: `DeadlockSimulatorApp._build_recovery_tab` and `RecoveryEngine` remain implemented in the codebase.)

**Released resources don't immediately satisfy a waiting process**

- `ResourceManager.release_resource()`, `terminate_process()`, and `rollback_process()` return instances to `available_instances`, while waiting processes retain their pending `requested` edges until re-requested or cleared, letting you inspect post-recovery state before resuming execution.

</details>

---

## 🛠️ Tech Stack

<details>
<summary><b>Click to expand tech stack details</b></summary>

- **Language**: Python 3.8+ (`dataclasses`, `typing`, `threading`, `queue`, `time`, `math`, `io`)
- **Desktop GUI**: Standard Library `tkinter` + `ttk` (`clam` theme, custom dark palette `#101010` / `#181818` / `#3b82f6`)
- **Graph Visualization**: Custom native `tk.Canvas` renderer (`GraphRenderer`) with dual-ring radial layout
- **Concurrency**: `threading.Lock` state synchronization + daemon `threading.Thread` scenario runner + `queue.Queue` UI bridge
- **Testing**: Python `unittest` (`tests/test_core.py`, 18 unit tests covering state management, detection, and recovery)
- **Optional**: `Pillow` (dynamic 64×64 PNG padlock icon generation), `pytest` (alternative test runner)

</details>

---

## 📖 Architecture & Module Reference

```text
Deadlock-Simulator/
├── core/
│   ├── __init__.py
│   ├── resource_manager.py      # Resource & Process dataclasses, lock-guarded state table, snapshot/matrix export
│   ├── deadlock_detector.py     # DeadlockResult + RAG (DFS), Banker's Algorithm, and WFG detection engines
│   ├── recovery_engine.py       # RecoveryAction + 4 strategies: terminate, preempt, rollback, kill_all
│   └── simulation_engine.py     # Background daemon runner with 5 preset/random concurrency scenarios
├── gui/
│   ├── __init__.py
│   ├── main_window.py           # DeadlockSimulatorApp (Tkinter dark-mode UI, polling loops, shortcuts)
│   └── graph_renderer.py        # GraphRenderer (dual-ring RAG & WFG tk.Canvas rendering)
├── tests/
│   ├── __init__.py
│   └── test_core.py             # 18 unit tests for ResourceManager, DeadlockDetector, and RecoveryEngine
├── .gitignore
└── README.md
```

| Module                                                   | Primary Class / Symbols                                             | Responsibility                                                                                                             |
| -------------------------------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| [`core/resource_manager.py`](core/resource_manager.py)   | `Resource`, `Process`, `ResourceManager`                            | Thread-safe allocation/request state, rollback/termination cleanup, event log                                              |
| [`core/deadlock_detector.py`](core/deadlock_detector.py) | `DeadlockResult`, `DeadlockDetector`                                | Snapshot-based RAG, Banker's, and WFG deadlock analysis                                                                    |
| [`core/recovery_engine.py`](core/recovery_engine.py)     | `RecoveryAction`, `RecoveryEngine`                                  | Victim selection, resource preemption, rollback, kill-all resolution                                                       |
| [`core/simulation_engine.py`](core/simulation_engine.py) | `SimulationEngine`                                                  | Timed scenario playback (`dining_philosophers`, `bankers_classic`, `producer_consumer`, `readers_writers`, `random_chaos`) |
| [`gui/graph_renderer.py`](gui/graph_renderer.py)         | `GraphRenderer`                                                     | Dual-ring `tk.Canvas` layout, edge routing, instance dots, deadlock halos                                                  |
| [`gui/main_window.py`](gui/main_window.py)               | `DeadlockSimulatorApp`                                              | 3-column dark UI, menu/shortcuts, snapshot diffing, event queue polling                                                    |
| [`tests/test_core.py`](tests/test_core.py)               | `TestResourceManager`, `TestDeadlockDetector`, `TestRecoveryEngine` | Core engine verification suite (18 test cases)                                                                             |

---

## 🗺️ Roadmap

| Area                   | Planned Improvements                         | Highlights                                                                                                  |
| ---------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| 🖥️ **GUI & Controls**  | Recovery Tab Restoration & `max_need` Inputs | Re-wire `_build_recovery_tab` in right panel and add per-process `max_need` editor for Banker's Algorithm   |
| ⚙️ **Core Engine**     | Auto-Grant Queue & Multi-Cycle DFS           | Automatically evaluate waiting `requested` edges when instances are freed; enumerate all overlapping cycles |
| 🧪 **CLI & Packaging** | Headless CLI Entrypoint                      | Add `cli.py` and `main.py` wrappers for terminal-only classroom demos and automated grading                 |
| 🕸️ **WFG Accuracy**    | Multi-Instance WFG Warnings                  | Mark WFG cycles involving multi-instance resources with `conclusive=False` matching RAG behavior            |

---

## How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

---

## 🙏 Acknowledgments

Built to make classic Operating Systems concurrency, resource allocation theory, and deadlock recovery mechanics immediately visual and interactive.

- **Author**: **Akshay Yadav , Vanshika Krishan, Jagriti Upadhayay**

---

## 📄 License

Open-source educational project — see repository for license details.

---
