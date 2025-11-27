#!/usr/bin/env python3
"""
GitHub Contributions Generator
Generated on: 2025-11-27
Total commits: 275
"""

import os
import subprocess
from datetime import datetime

def run_command(cmd):
    """Execute shell command"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.returncode == 0

def create_commit(date, commit_num):
    """Create a commit with specific date"""
    # Create or modify a file
    filename = "contributions.txt"
    with open(filename, "a") as f:
        f.write(f"Contribution on {date} - Commit #{commit_num}\n")
    
    # Set environment variables for commit date
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date
    env['GIT_COMMITTER_DATE'] = date
    
    # Git add and commit
    subprocess.run(['git', 'add', filename], env=env)
    subprocess.run([
        'git', 'commit', '-m', f'Contribution: {date}'
    ], env=env)

def main():
    print("🚀 GitHub Contributions Generator")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not a git repository!")
        print("Please run: git init")
        return
    
    contributions = [
        {"date": "2025-01-02", "commits": 12},  # Kamis
        {"date": "2025-01-03", "commits": 7},  # Jumat
        {"date": "2025-01-06", "commits": 19},  # Senin
        {"date": "2025-01-07", "commits": 11},  # Selasa
        {"date": "2025-01-08", "commits": 3},  # Rabu
        {"date": "2025-01-09", "commits": 9},  # Kamis
        {"date": "2025-01-10", "commits": 6},  # Jumat
        {"date": "2025-01-13", "commits": 25},  # Senin
        {"date": "2025-01-14", "commits": 14},  # Selasa
        {"date": "2025-01-15", "commits": 2},  # Rabu
        {"date": "2025-01-16", "commits": 1},  # Kamis
        {"date": "2025-01-17", "commits": 25},  # Jumat
        {"date": "2025-01-20", "commits": 12},  # Senin
        {"date": "2025-01-21", "commits": 19},  # Selasa
        {"date": "2025-01-22", "commits": 24},  # Rabu
        {"date": "2025-01-23", "commits": 13},  # Kamis
        {"date": "2025-01-24", "commits": 2},  # Jumat
        {"date": "2025-01-27", "commits": 10},  # Senin
        {"date": "2025-01-28", "commits": 19},  # Selasa
        {"date": "2025-01-29", "commits": 7},  # Rabu
        {"date": "2025-01-30", "commits": 14},  # Kamis
        {"date": "2025-01-31", "commits": 21},  # Jumat
    ]
    
    total_commits = sum(c['commits'] for c in contributions)
    print(f"📊 Total contributions to generate: {total_commits}")
    print(f"📅 Date range: {contributions[0]['date']} to {contributions[-1]['date']}")
    print()
    
    confirm = input("Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        return
    
    print("\n⏳ Generating contributions...")
    
    commit_count = 0
    for contrib in contributions:
        date = contrib['date']
        commits = contrib['commits']
        
        for i in range(commits):
            # Format date for git (ISO 8601)
            git_date = f"{date}T{12 + (i % 12):02d}:00:00"
            create_commit(git_date, commit_count + 1)
            commit_count += 1
            
            if commit_count % 10 == 0:
                print(f"  ✓ Generated {commit_count}/{total_commits} commits...")
    
    print(f"\n✅ Successfully generated {commit_count} commits!")
    print("\n📤 Next steps:")
    print("1. Push to GitHub: git push -f origin main")
    print("2. Check your GitHub profile contributions graph")
    print("\n⚠️  Note: It may take a few minutes for GitHub to update the graph")

if __name__ == "__main__":
    main()
