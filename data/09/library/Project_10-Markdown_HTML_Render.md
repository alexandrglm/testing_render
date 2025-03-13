# Project10: MarkDown Web Server

**Project10** is a web application that renders an entire library of Markdown documents into HTML, automatically generating its table of contents.

The viewer allows users to switch between a **light theme** and a **dark theme**, adjust text size (zoom), and render various Markdown elements (tables, images, formulas, etc.) in a responsive manner while consuming minimal server resources.

## Data Flow Overview

1. **Markdown Retrieval:** The system scans `data/09/library` to find Markdown files.
2. **Markdown Parsing:** Files are read and converted into HTML with enhanced features (tables, syntax highlighting, etc.).
3. **Post-Processing:** The HTML is refined, adjusting image paths for correct rendering.
4. **Final Rendering:** The formatted content is inserted and displayed into a web HTML.

---

# Markdown Demo (H1 Heading)

## H2 Heading

### H3 Heading

#### H4 Heading

##### H5 Heading

###### H6 Heading

---

## Text Formatting

- **Bold text**
- *Italic text*
- ***Bold and italic***
- ~~Strikethrough~~
- `Inline code`

---

## Lists

### Unordered List

- Item 1
- Item 2
  - Sub-item 2.1
  - Sub-item 2.2

### Ordered List

1. First item
2. Second item
3. Third item

---

## Blockquotes

> This is a blockquote example.

---

## Code Block

```python
print("Hello, World!")
```

---

## Table

| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Data A | Data B | Data C |
| Data D | Data E | Data F |

---

## Math Formulas

Inline formula: $E = mc^2$

Block formula:

$$
\int_0^1 x^2 \,dx = \frac{1}{3}
$$

---

## Emoji Support

🚀 😃 🎉 ✅

---

## Images

![Sample Image](https://picsum.photos/600/300)
![More images](https://picsum.photos/800/600)
![More images](https://picsum.photos/300/600)
![More images](https://picsum.photos/150/400)
![More images](https://picsum.photos/1024/768)

---

This document showcases the full range of Markdown features supported by Project10.
