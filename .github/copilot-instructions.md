### Quick context

This repo is a tiny Python utility used to generate many historical git commits into `contributions.txt` and commit them with fixed author/committer dates (`GIT_AUTHOR_DATE`, `GIT_COMMITTER_DATE`). The key files are:

- `generate_contributions.py` — main script that appends lines to `contributions.txt` and runs `git commit` with explicit dates; prompts for confirmation.
- `contributions.txt` — file that stores the generated commit lines and grows with each run.

### What an AI helper should know (short & actionable)

1. Script behavior: `generate_contributions.py` will create many commits with controlled timestamps using environment variables. It DOES modify git history (commits are created with custom dates) and the script suggests a force-push (`git push -f`) as a follow-up.
2. Safety first: avoid running the script on a shared or important branch. Always test in a throwaway repo or a new branch, or in a local clone with no remote. Examples below show a safe test flow.
3. Usage: run with Python 3 (python3) from the repo root. The script checks for `.git` and will refuse to run if not a git repo.

### Example safe test flow

```bash
# create a disposable repository
mkdir -p /tmp/gh-test && cd /tmp/gh-test
git init
cp /path/to/this/repo/generate_contributions.py ./
python3 generate_contributions.py   # follow the interactive confirmation
# Inspect commits with: git log --oneline --decorate --date=iso
```

### What to change when editing

- Keep changes small and obvious — this project has a single script and one large output file.
- If you add or change the hard-coded `contributions` list in `generate_contributions.py`, update the printed totals and date-range text in the script so the output remains accurate.
- Avoid adding un-tested force-push or remote-aware behavior unless you also add explicit confirmation prompts and warnings.

### Patterns and conventions

- Minimal Python tooling — no requirements file, no tests, simple structure. Keep modifications lightweight and documented in the script header.
- Commit messages are uniform: `Contribution: <date>` — add any new patterns only if you update the script’s commit creation function.

### Quick pointers for reviewers

- Validate changes locally in a disposable repository before approving them to avoid accidental mass history edits.
- Prefer explanatory comments rather than heavy refactors; this repo’s intent is explicit and narrow.

If anything here is unclear or you want the file to emphasize other conventions, tell me which area to expand and I’ll iterate.
