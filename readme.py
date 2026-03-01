#!/usr/bin/env python3
"""
README Generator - Auto-generates README.md for repos
"""
import sys

TEMPLATES = {
    "python": """# {name}

{description}

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python {main}
```

## Features

- Feature 1
- Feature 2

## License

MIT
""",
    
    "typescript": """# {name}

{description}

## Setup

```bash
npm install
```

## Usagenpm start
```



```bash
## License

MIT
""",
    
    "simple": """# {name}

{description}

## Quick Start

```bash
{command}
```

## What's Inside

- Simple and focused
- Easy to understand

## License

MIT
"""
}

def generate(name, lang="python", description="", main="main.py"):
    template = TEMPLATES.get(lang, TEMPLATES["simple"])
    
    content = template.format(
        name=name,
        description=description or f"A {name} project.",
        main=main,
        command=f"python {main}" if lang == "python" else "npm start"
    )
    
    print(content)


def main():
    args = sys.argv[1:]
    
    if not args:
        print("Usage: readme.py <name> [python|typescript|simple] [description]")
        print("\nTemplates: python, typescript, simple")
        return
    
    name = args[0]
    lang = args[1] if len(args) > 1 else "python"
    desc = args[2] if len(args) > 2 else ""
    
    generate(name, lang, desc)


if __name__ == "__main__":
    main()
