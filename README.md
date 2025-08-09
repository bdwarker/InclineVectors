# InclineVectors 

---

This Python program is an **interactive physics visualization** that shows how a force applied to an object on an inclined plane can be broken down into its **parallel** and **normal** components.  
It also simulates **gravity**, **friction**, and **object motion** along the slope, letting you explore the effects of applied forces in real time.

---

## 🎯 Features

- **Interactive Force Application**  
  Click and drag on the object to apply a force. The program will:
  - Draw the **applied force vector**.
  - Decompose it into **parallel** and **normal** components relative to the slope.
  - Remove the vectors when the mouse is released.

- **Gravity & Friction Simulation**  
  The object naturally slides down the incline due to gravity, with friction opposing motion.

- **Adjustable Incline Angle**  
  Change the slope from flat to steep using keyboard controls.

- **Change Object Shape**  
  Switch between a **rectangle** and a **circle** while keeping it aligned with the slope.

- **Physics Accuracy**  
  Forces and accelerations are computed according to the slope angle, gravity, and friction.

---

## 🖥️ Controls

| Action                          | Key / Mouse                |
|---------------------------------|----------------------------|
| Apply force                     | **Click & drag** on object |
| Increase slope angle            | **↑** (Up Arrow)           |
| Decrease slope angle            | **↓** (Down Arrow)         |
| Switch object shape             | **S**                      |
| Move object left (up slope)     | **←** (Left Arrow)         |
| Move object right (down slope)  | **→** (Right Arrow)        |
| Increase friction               | **F**                      |
| Decrease friction               | **D**                      |
| Quit                            | **Close window**           |

---

## 📦 Requirements

- Python 3.8+
- [Pygame](https://www.pygame.org/) library

Install Pygame with:

```bash
pip install pygame
```

---

## 📷 Example

When you drag the mouse from the object:
- **Red vector**: Applied Force
- **Green vector**: Parallel Component (along the slope)
- **Blue vector**: Normal Component (into the slope)
- **Yellow vector**: Gravity

---

**Author:** Mohammed Shaan