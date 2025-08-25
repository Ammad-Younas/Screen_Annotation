# Professional Screen Annotator

A professional-grade screen annotation tool with modern UI and advanced drawing features.

## ✨ New Professional Version Features

- 🎨 **Modern Professional UI** - Sleek dark theme with intuitive design
- 🖼️ **Icon-Based Tools** - Visual tool selection with professional icons
- 📐 **Multiple Drawing Tools** - Pen, Rectangle, Circle, Ellipse, Text, Eraser
- ⏪ **Undo/Redo Support** - Full history management with Ctrl+Z/Ctrl+Y
- 🎯 **Precision Drawing** - Improved shape tools with real-time preview
- 📝 **Text Annotations** - Add custom text with size control
- 🧹 **Smart Eraser** - Targeted erasing of specific elements
- 🖊️ **Enhanced Pen Tool** - Smooth drawing with adjustable brush size (1-20)
- 🎨 **Advanced Color Picker** - Professional color selection
- 💾 **Smart Screenshots** - Capture with confirmation and naming
- ⌨️ **Extended Shortcuts** - Full keyboard shortcut support

## Legacy Features

- 🖊️ **Draw on your screen** - Transparent overlay lets you draw on top of any application
- 🎨 **Color picker** - Choose any color for drawing
- 📏 **Adjustable brush size** - Change brush thickness (1-10)
- 🧹 **Clear screen** - Remove all drawings instantly
- 💾 **Save screenshots** - Capture your screen with drawings
- ⌨️ **Keyboard shortcuts** - F1 to toggle, F2 to clear, ESC to hide

## Quick Start

### 🚀 Professional Version (Recommended)

```bash
./run_professional.sh    # Linux/Mac
run_professional.bat     # Windows
# OR
python professional_overlay.py
```

### 📝 Simple Version (Legacy)

```bash
./run_overlay.sh        # Linux/Mac
run_overlay.bat         # Windows
# OR
python simple_overlay.py
```

## How to Use

### Professional Version

1. **Run the tool** - A modern control panel appears with professional design
2. **Select a tool** - Choose from Pen, Rectangle, Circle, Ellipse, Text, or Eraser using icon buttons
3. **Customize settings** - Pick color and adjust brush size (1-20)
4. **Click "Start Drawing"** - Your screen becomes drawable with selected tool
5. **Draw with precision** - Left-click and drag for shapes, click for text
6. **Use shortcuts** - F1 to toggle, F2 to clear, Ctrl+Z/Y for undo/redo
7. **Save your work** - Professional screenshot capture with confirmation

### Drawing Tools

- **🖊️ Pen Tool**: Freehand drawing with smooth lines
- **▭ Rectangle Tool**: Perfect rectangles with outline
- **● Circle Tool**: Perfect circles (maintains aspect ratio)
- **⬭ Ellipse Tool**: Oval shapes of any proportion
- **📝 Text Tool**: Add custom text annotations
- **🧹 Eraser Tool**: Remove specific drawings precisely

### Simple Version (Legacy)

1. **Run the tool** - A small control panel will appear
2. **Click "Start Drawing"** - Your screen becomes drawable
3. **Left-click and drag** - Draw on your screen
4. **Press F1** - Toggle drawing mode on/off anytime
5. **Press F2** - Clear all drawings
6. **Press ESC** - Hide the overlay

## Perfect For

- 👨‍🏫 **Presentations** - Highlight important points
- 🎥 **Screen recordings** - Add annotations while recording
- 💻 **Software demos** - Point out features and buttons
- 📚 **Tutorials** - Draw arrows and explanations
- 🎯 **Focus attention** - Circle or underline content

## Controls

### Professional Version

- **F1**: Toggle drawing mode on/off
- **F2**: Clear all drawings
- **ESC**: Hide overlay
- **Ctrl+Z**: Undo last action
- **Ctrl+Y**: Redo last undone action
- **Left-click + drag**: Draw with selected tool
- **Click (Text tool)**: Add text at cursor position
- **Tool buttons**: Switch between drawing tools
- **Color button**: Open professional color picker
- **Size slider**: Adjust brush/line thickness (1-20)

### Simple Version (Legacy)

- **F1**: Toggle drawing mode on/off
- **F2**: Clear all drawings
- **ESC**: Hide overlay
- **Left-click + drag**: Draw
- **Color button**: Change drawing color
- **Size slider**: Change brush thickness

## Requirements

- Python 3.6+
- Pillow library: `pip install Pillow`

## Installation

1. Make sure Python is installed
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the tool:
   ```bash
   ./run_overlay.sh
   ```

That's it! Happy drawing! 🎨

## Quick Start

### 🚀 For Screen Overlay (Draw on Screen)

```bash
./run_overlay.sh        # Linux/Mac
run_overlay.bat         # Windows
# OR
python screen_overlay.py
```

### 📸 For Screenshot Annotation

```bash
./launch.sh             # Linux/Mac
launch.bat              # Windows
# OR
python main.py
```

## Usage

### Screen Overlay Tool (Draw on Screen)

**Perfect for:** Live presentations, tutorials, highlighting content on screen

1. **Start the tool**: Run `screen_overlay.py`
2. **Control panel opens**: Small window with tools and options
3. **Click "Start Overlay"**: Transparent overlay covers your screen
4. **Draw away!**: Use any tool to draw on your screen
5. **Toggle anytime**: Press F1 to show/hide overlay

**Key Controls:**

- `F1`: Toggle overlay on/off
- `F2`: Clear all annotations
- `ESC`: Hide overlay
- `Right-click`: Context menu with options
- `Ctrl+S`: Save screenshot with annotations

### Screenshot Annotation Tool (Traditional)

**Perfect for:** Detailed image editing, documentation, tutorials

1. **Take Screenshot**: Click "Screenshot" to capture your screen
2. **Select Tool**: Choose from Pen, Rectangle, Circle, Ellipse, Text, or Eraser
3. **Customize**: Set color, brush size, and other properties
4. **Annotate**: Draw on the canvas
5. **Save**: Export your annotated image

### Keyboard Shortcuts

- `Ctrl+Z`: Undo
- `Ctrl+Y`: Redo
- `Ctrl+S`: Save annotation
- `Ctrl+O`: Open image
- `Delete`: Delete selected items
- `Escape`: Cancel current operation

### Screenshot Capture

1. Click "Screenshot" button
2. Main window will hide temporarily
3. Drag to select the area you want to capture
4. Release to capture the selected area
5. Press `Escape` to cancel

### Layer Management

- **Add Layer**: Create new annotation layers
- **Delete Layer**: Remove current layer (minimum 1 layer required)
- **Visibility**: Toggle layer visibility with checkbox
- **Lock**: Lock layers to prevent editing
- **Selection**: Click on layer name to switch active layer

### Drawing Tools

#### Pen Tool

- Click and drag to draw freehand lines
- Adjustable brush size (1-20 pixels)
- Smooth line rendering

#### Shape Tools

- Click and drag to create shapes
- Rectangle: Creates rectangular outlines
- Circle: Creates perfect circles (equal width/height)
- Ellipse: Creates oval shapes

#### Text Tool

- Click where you want to add text
- Enter text in the popup dialog
- Customizable font family and size
- Text anchored at click position

#### Eraser Tool

- Click and drag to erase annotations
- Erases any overlapping annotations
- Adjustable eraser size

### Color and Styling

- **Color Button**: Click to open color picker
- **Size Slider**: Adjust brush/line thickness
- **Font Controls**: Choose font family and size for text

### File Operations

- **Open Image**: Load existing image as background
- **Save**: Export final annotation as PNG/JPEG
- **Load Project**: Load previously saved annotation project
- **Clear All**: Remove all annotations (with confirmation)

## File Formats

### Supported Import Formats

- PNG, JPEG, JPG, GIF, BMP, TIFF

### Export Formats

- PNG (recommended for annotations)
- JPEG
- Project files (JSON format for reopening)

## Technical Details

### Architecture

- **GUI Framework**: Tkinter with ttk widgets
- **Image Processing**: PIL (Pillow) for image manipulation
- **Canvas System**: Tkinter Canvas with custom drawing logic
- **State Management**: History-based undo/redo system

### Performance

- Optimized for smooth drawing performance
- Efficient memory usage with state compression
- Responsive UI with proper event handling

### Compatibility

- **OS**: Cross-platform (Windows, macOS, Linux)
- **Python**: Python 3.6+
- **Dependencies**: Minimal (only Pillow required)

## Troubleshooting

### Common Issues

**Screenshot not working:**

- Ensure you have screen capture permissions
- Try running with administrator/sudo privileges if needed

**Fonts not appearing:**

- Check if the selected font is installed on your system
- Default fonts (Arial, Times, Courier) should always work

**Performance issues:**

- Large images may cause slower performance
- Consider reducing image size or brush complexity
- Clear history if memory usage becomes high

**Save/Load errors:**

- Ensure you have write permissions to the target directory
- Check file path validity and disk space

## Development

### Project Structure

```
Screen_Annotation/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── icons/              # Icon resources
    ├── circle.png
    ├── close.png
    ├── delete.png
    ├── ellipse.png
    ├── eraser.png
    ├── pen.png
    ├── rectangle.png
    ├── redo.png
    ├── text.png
    └── undo.png
```

### Key Classes

- `ScreenAnnotationApp`: Main application class
- `AnnotationLayer`: Layer management system
- Custom drawing handlers for each tool type

### Extending the Application

- Add new tools by implementing draw handlers
- Extend layer system for advanced features
- Add new export formats in save methods
- Implement additional keyboard shortcuts

## License

This project is provided as-is for educational and practical use.

## Credits

Created by GitHub Copilot
Date: August 25, 2025
