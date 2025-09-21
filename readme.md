# LLaMO: Large Language Multi-tasking Optimizer

A graph optimization framework for enhancing LLM-based robot task planning through hierarchical decomposition and shortest path optimization.

## Overview

LLaMO addresses the inefficiency problem in direct LLM outputs for robot task planning by introducing a post-optimization layer that uses graph theory to find optimal action sequences.

### Core Architecture

```
Natural Language → Task Decomposition → Action Generation → Graph Optimization → Robot Commands
                    ↑                                         ↑
              RAG Retrieval                           Dijkstra's Algorithm
```

## Key Innovations

### Mathematical Framework

**Problem Formulation:**
```
Given: Scene S, Command C, Knowledge K
Find: P* = argmin Cost(P) subject to constraints
Where: P = sequence of actions {a₁, a₂, ..., aₙ}
```

**Graph Optimization:**
```
d(v,T) = min[d(u,T') + Cost(u,v)]
```
- `d(v,T)`: shortest distance to vertex v with completed subtasks T
- `Cost(u,v)`: edge weight between action nodes u and v

### Performance Results

| Method | Success Rate | Action Efficiency |
|--------|-------------|------------------|
| **LLaMO** | **94%** | **30-40% reduction** |
| Tree of Thought | 90% | Baseline |
| Raw GPT-4 | 80% | +40% actions |
| LLM+P | 70% | Variable |

## Installation & Dependencies

### Core Dependencies
```bash
git clone https://github.com/your-repo/llamo
cd llamo
pip install -r requirements.txt
```

**Core Requirements:**
- OpenAI API (GPT-4)
- LangChain
- FAISS (vector search)
- NumPy, NetworkX

### Robot-Specific Dependencies

**For Agility Digit Humanoid:**
- Agility Robotics SDK (proprietary)
- Access to Digit robot or simulator

**For Unitree Go1 Quadruped:**
- Unitree SDK (proprietary)
- Access to Go1 robot or simulator

> **Note**: Robot-specific implementations require hardware access or licensed simulators. The core LLaMO optimization algorithms can be tested independently using the simulation scripts in `experiments/`.

## Quick Start

```python
from llamo.multitask.multi_tasks_optimization import MultiTasksManagement

# Initialize system
mtm = MultiTasksManagement()

# Define environment and task
envs = "table1 has red box, table2 has blue box"
query = "swap the boxes between tables"

# Generate optimized action sequence
actions = mtm.arrangement(envs, robot_info="", query=query)
print(actions)  # [('Goto', 'table1'), ('Pick', 'red box'), ...]
```

## Core Components

### 1. Task Decomposition (`llamo/core/task_decomposer.py`)
- GPT-4 based few-shot prompting
- Structured JSON output with dependencies
- Subtask dependency modeling

### 2. Action Generation (`llamo/core/action_chain.py`)
- Converts subtasks to robot primitives: `Goto`, `Pick`, `Place`, `Done`
- Environment-aware action planning

### 3. Graph Optimizer (`llamo/core/optimizer.py`)
- Dijkstra's algorithm for shortest path
- Action validation through `ActionLink` rules
- Permutation search for optimal task ordering

### 4. RAG Retrieval (`llamo/core/retriever.py`)
- FAISS vector database for safety rules
- OpenAI embeddings (text-embedding-ada-002)
- Context injection for workplace compliance

## Action Validation Rules

1. **Item Consistency**: Robot must carry required items for Place actions
2. **Environment Matching**: Pick/Place actions must match robot location
3. **State Transitions**: Proper hand states (empty for Pick, full for Place)
4. **Movement Optimization**: Eliminate redundant Goto commands

## Multi-Robot Support

### Agility Digit (Humanoid)
- Full manipulation capabilities
- Table-based pick-and-place tasks
- Complex multi-object scenarios

### Go1 Quadruped
- Navigation-focused tasks
- Path planning and waypoint optimization
- Dynamic task insertion during execution

## Directory Structure

```
llamo/
├── llamo/                       # Core library
│   ├── core/                    # Core LLaMO components
│   ├── analysis/                # Action analysis & frontend
│   ├── llm/                     # LLM interfaces
│   └── multitask/               # Multi-task coordination
├── robots/                      # Robot-specific implementations
│   ├── digit/                   # Agility Digit humanoid
│   └── go1/                     # Unitree Go1 quadruped
├── environments/                # Test environment configurations
├── data/                        # Knowledge base & assets
├── experiments/                 # Research experiments & demos
├── tools/                       # Utilities & preprocessing
├── docs/                        # Documentation & research
└── tests/                       # Unit tests
```

## Environments

Test environments defined in `environments/*.toml`:
- **room1.toml**: Basic two-table setup with packages
- **room2-4.toml**: Increasingly complex scenarios
- AprilTag-based object tracking
- Physics simulation parameters

## Experimental Results

### Optimization Effectiveness
- **Average Action Reduction**: 30-40% vs raw GPT-4
- **Task Success Rate**: 94% (highest among compared methods)
- **Redundancy Elimination**: Removes unnecessary intermediate steps

### Dynamic Task Handling
- Real-time task insertion during execution
- Path re-optimization without complete restart
- Maintains efficiency during runtime changes

## Configuration

Set OpenAI API key:
```bash
export OPENAI_API_KEY="your-key-here"
```

Or modify `llamo/llm/llm.py` directly (line 8).

## Research Context

This implementation is based on the paper introducing LLaMO's hierarchical optimization approach to LLM-based robotics. Key mathematical contributions include the graph-theoretic formulation of robot task planning and the integration of classical optimization with modern language models.

## Contributing

This repository serves as a research artifact. For extensions or modifications, focus on:
- Adding new robot types in `robots/`
- Extending action primitives in `llamo/core/action_chain.py`
- Improving optimization algorithms in `llamo/core/optimizer.py`