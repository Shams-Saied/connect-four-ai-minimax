# Connect 4 AI Agent 

An AI-powered Connect 4 game implemented in Python featuring a graphical interface and an intelligent agent using adversarial search algorithms (Minimax with Alpha-Beta pruning). The project demonstrates core Artificial Intelligence concepts applied to game playing.

---

## Features

- AI opponent using **Minimax algorithm**
- Performance optimization using **Alpha-Beta pruning**
- Heuristic evaluation function for board state scoring
- Interactive **GUI-based gameplay**
- Modular design separating game logic, AI, and interface
- Jupyter Notebook for experimentation and algorithm testing

---

## AI Approach

The AI agent uses:

- **Minimax Algorithm** → explores possible game states to determine optimal moves  
- **Alpha-Beta Pruning** → reduces search space and improves performance  
- **Heuristic Evaluation Function** → scores board positions to guide decision-making  

This allows the AI to simulate intelligent gameplay while maintaining efficiency.

---

## Project Structure
connect4-ai-agent/
│
├── connect4.py # Core game logic (board, rules, win detection)
├── algorithms.py # AI algorithms (Minimax, Alpha-Beta pruning, heuristics)
├── gui.py # Graphical user interface for gameplay
├── notebook.ipynb # Experiments and testing of AI logic

---

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- Artificial Intelligence (Minimax, Alpha-Beta Pruning)
- Data Structures & Algorithms
- GUI development (Tkinter / similar)

---

## How to Run

### 1. Install dependencies
```bash
pip install numpy
### 2. Run the game
python gui.py
