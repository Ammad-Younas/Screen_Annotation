![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

# Screen Annotation

## Description
Screen Annotation is a Python-based desktop application built with PyQt6, designed for real-time screen annotation. It provides a user-friendly interface with multiple drawing tools, including pen, rectangle, circle, ellipse, text, and eraser, allowing users to annotate directly on their screen. The application features a modern, dark-themed UI, undo/redo functionality, customizable brush sizes and colors, and keyboard shortcuts for efficient workflow. Ideal for presentations, tutorials, or collaborative work, this tool is both intuitive and powerful.

## Features
- **Multiple Drawing Tools**: Pen, rectangle, circle, ellipse, text, and eraser.
- **Professional UI**: Dark-themed, modern interface with icon-based tool selection.
- **Undo/Redo**: Easily revert or reapply changes with Ctrl+Z and Ctrl+Y.
- **Customizable Options**: Adjustable brush size and color picker for precise annotations.
- **Keyboard Shortcuts**:
  - F1: Toggle overlay
  - F2: Clear all drawings
  - Esc: Hide overlay
  - Ctrl+Z: Undo
  - Ctrl+Y: Redo
- **Cross-Platform**: Built with PyQt6, compatible with Windows, macOS, and Linux.
- **Transparent Overlay**: Draw directly on the screen with a transparent background.

## Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt` (primarily PyQt6)
- Optional: Icon files for tools (pen.png, rectangle.png, circle.png, ellipse.png, text.png, eraser.png, undo.png, redo.png, delete.png) in an `icons` folder in the same directory as the script.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Screen_Annotation.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Screen_Annotation
   ```
3. Install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Add icon files to an `icons` folder in the project directory.
5. Run the application:
   ```bash
   python screen_annotation.py
   ```

## Usage
1. Launch the application using `python screen_annotation.py`.
2. The control window appears, centered on your screen.
3. Click **Start Drawing** or press **F1** to activate the transparent overlay.
4. Select a tool (pen, rectangle, circle, ellipse, text, or eraser) from the control window.
5. Adjust brush size and color as needed.
6. Draw directly on the screen overlay.
7. Use **Undo** (Ctrl+Z) or **Redo** (Ctrl+Y) to manage annotations.
8. Press **F2** to clear all drawings or **Esc** to hide the overlay.
9. Close the control window to exit the application.

## GitHub Description
**Screen Annotation**  
A Python-based screen annotation tool built with PyQt6, featuring a sleek, dark-themed UI and versatile drawing tools (pen, rectangle, circle, ellipse, text, eraser). Supports undo/redo, customizable brush sizes/colors, and keyboard shortcuts for seamless annotation during presentations or tutorials. Cross-platform and easy to use.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for bug reports or feature requests.

## Acknowledgments
- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Inspired by professional annotation tools for presentations and tutorials
