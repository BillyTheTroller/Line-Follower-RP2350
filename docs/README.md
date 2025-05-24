# 📚 docs/ - Project Documentation

This directory contains technical documentation, diagrams, and resources for the line follower project.

## 🖼️ Diagram Types
1. **System Architecture**  
   - Mermaid.js flowcharts (`.mmd`)
   - Exported PNG/SVG files

2. **Hardware Wiring**  
   - Fritzing/Circuit diagrams
   - Pin mapping tables

## 🛠️ How to Update
```bash
# Generate new Mermaid diagrams (requires Node.js)
npx mmdc -i diagrams/system_flow.mmd -o diagrams/system_flow.png

# Update API docs when endpoints change:
python3 -m http.server  # Live preview
