# UML Diagrams

This directory contains UML diagrams for Parallel Text Analyzer.

The diagrams are written in PlantUML.

## Directory Structure

    docs/uml/
    ├── README.md
    ├── source/
    │   ├── activity-diagram.puml
    │   ├── class-diagram.puml
    │   ├── component-diagram.puml
    │   ├── deployment-diagram.puml
    │   └── sequence-diagram.puml
    └── images/
        ├── activity-diagram.png
        ├── class-diagram.png
        ├── component-diagram.png
        ├── deployment-diagram.png
        └── sequence-diagram.png

## Diagram List

| Diagram | Source | Image | Purpose |
|---|---|---|---|
| Class Diagram | source/class-diagram.puml | images/class-diagram.png | Shows main classes and relationships |
| Component Diagram | source/component-diagram.puml | images/component-diagram.png | Shows application components and layers |
| Sequence Diagram | source/sequence-diagram.puml | images/sequence-diagram.png | Shows safe GUI and worker thread interaction |
| Activity Diagram | source/activity-diagram.puml | images/activity-diagram.png | Shows the main analysis workflow |
| Deployment Diagram | source/deployment-diagram.puml | images/deployment-diagram.png | Shows local development and repository environment |

## Notes

Both PlantUML source files and generated PNG images should be included in the repository.

Source files make diagrams editable.

PNG images make diagrams easy to view directly on GitHub.
