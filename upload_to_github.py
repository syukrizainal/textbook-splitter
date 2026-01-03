"""
Upload to GitHub Script
Helps you upload your PDF splitter to GitHub
"""

import os
import subprocess
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and show output"""
    if description:
        print(f"\n{description}")
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result

def main():
    print("=" * 60)
    print("GitHub Upload Helper")
    print("=" * 60)

    # Get GitHub credentials
    print("\nPlease enter your GitHub information:")
    github_username = input("Your GitHub username: ").strip()
    github_email = input("Your GitHub email: ").strip()
    repo_name = input("Repository name [cfa-l2-pdf-splitter]: ").strip() or "cfa-l2-pdf-splitter"

    # Configure git
    print("\n" + "=" * 60)
    print("Step 1: Configure Git")
    print("=" * 60)

    run_command(f'git config --global user.name "{github_username}"')
    run_command(f'git config --global user.email "{github_email}"')
    print("✓ Git configured")

    # Navigate to project folder
    project_dir = Path(r"C:\Users\Dell\2026 Jan Split Textbook")
    os.chdir(project_dir)

    # Initialize git
    print("\n" + "=" * 60)
    print("Step 2: Initialize Git Repository")
    print("=" * 60)

    run_command("git init")
    print("✓ Git initialized")

    # Create README
    print("\n" + "=" * 60)
    print("Step 3: Create README.md")
    print("=" * 60)

    readme_content = f"""# {repo_name}

Python scripts to split CFA Level 2 textbooks into separate readings/learning modules.

## Features

- Split PDFs by Reading (for SchweserNotes Books 1-5)
- Split PDFs by Learning Module (for CBOK Volumes 1-10)
- Automatically detects chapter boundaries from PDF bookmarks

## Requirements

```bash
pip install pypdf
```

## Usage

### Split by Reading (SchweserNotes)
```bash
python split_pdf_by_reading.py "path/to/Book 1.pdf"
```

### Split by Learning Module (CBOK)
The script automatically extracts Learning Module boundaries from PDF bookmarks.

## Files

- `split_pdf_by_reading.py` - Main PDF splitter with bookmark detection
- `split_pdf_simple.py` - Simple splitter by fixed page counts

## Output

Split PDFs are saved in `*_split` folders next to the original PDFs.

---

Created for CFA Level 2 exam preparation.
"""

    with open("README.md", "w") as f:
        f.write(readme_content)
    print("✓ README.md created")

    # Add files
    print("\n" + "=" * 60)
    print("Step 4: Add Files to Git")
    print("=" * 60)

    run_command("git add .")
    print("✓ Files added")

    # Commit
    print("\n" + "=" * 60)
    print("Step 5: Commit Files")
    print("=" * 60)

    run_command('git commit -m "Initial commit: CFA Level 2 PDF splitter"')
    print("✓ Files committed")

    # Create GitHub repo using gh CLI if available
    print("\n" + "=" * 60)
    print("Step 6: Create GitHub Repository")
    print("=" * 60)

    # Check if gh CLI is installed
    gh_check = subprocess.run("gh --version", shell=True, capture_output=True)

    if gh_check.returncode == 0:
        print("GitHub CLI found! Creating repository...")
        result = run_command(f'gh repo create {repo_name} --public --source=. --remote=origin --push')

        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("✓ SUCCESS!")
            print("=" * 60)
            print(f"\nYour repository is at: https://github.com/{github_username}/{repo_name}")
            return

    # Fallback: Manual instructions
    print("\nGitHub CLI not found. Here's how to create the repository manually:\n")
    print("1. Go to: https://github.com/new")
    print(f"2. Repository name: {repo_name}")
    print("3. Make it Public")
    print("4. Click 'Create repository'")
    print("\nThen run these commands:\n")
    print(f'   git remote add origin https://github.com/{github_username}/{repo_name}.git')
    print(f'   git branch -M main')
    print(f'   git push -u origin main')

    # Ask if they want to push now
    response = input("\nHave you created the repository? (y/n): ").strip().lower()
    if response == 'y':
        run_command(f'git remote add origin https://github.com/{github_username}/{repo_name}.git')
        run_command('git branch -M main')
        run_command('git push -u origin main')
        print("\n" + "=" * 60)
        print("✓ SUCCESS!")
        print("=" * 60)
        print(f"\nYour repository is at: https://github.com/{github_username}/{repo_name}")

if __name__ == "__main__":
    main()
