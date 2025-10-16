#!/usr/bin/env bash
# scripts/git_push.sh
# Usage: git bash -c "./scripts/git_push.sh [remote-url] [commit-message]"
# Example: ./scripts/git_push.sh https://github.com/NHGiang2004/DoAn4.git "Initial commit"

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

REMOTE_URL="${1:-https://github.com/NHGiang2004/DoAn4.git}"
COMMIT_MSG="${2:-Auto commit from script}" 

# Ensure git repo
if [ ! -d .git ]; then
  echo "No .git directory found — initializing repository"
  git init
else
  echo ".git found — repository already initialized"
fi

# Add remote if not present or different
REMOTE_NAME="origin"
EXISTING_URL=""
if git remote get-url "$REMOTE_NAME" >/dev/null 2>&1; then
  EXISTING_URL=$(git remote get-url "$REMOTE_NAME")
fi

if [ -z "$EXISTING_URL" ]; then
  echo "Adding remote $REMOTE_NAME -> $REMOTE_URL"
  git remote add "$REMOTE_NAME" "$REMOTE_URL"
elif [ "$EXISTING_URL" != "$REMOTE_URL" ]; then
  echo "Remote $REMOTE_NAME exists with different URL ($EXISTING_URL). Updating to $REMOTE_URL"
  git remote set-url "$REMOTE_NAME" "$REMOTE_URL"
else
  echo "Remote $REMOTE_NAME already set to $REMOTE_URL"
fi

# Stage all changes
git add -A

# Commit if there are staged changes
if git diff --cached --quiet; then
  echo "No changes to commit"
else
  echo "Committing changes: $COMMIT_MSG"
  git commit -m "$COMMIT_MSG"
fi

# Determine current branch (default to main if not set)
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
if [ -z "$CURRENT_BRANCH" ] || [ "$CURRENT_BRANCH" = "HEAD" ]; then
  CURRENT_BRANCH="main"
  echo "No current branch detected, creating/updating branch '$CURRENT_BRANCH'"
  git branch -M "$CURRENT_BRANCH"
fi

# Push to remote
echo "Pushing to $REMOTE_NAME/$CURRENT_BRANCH"
git push -u "$REMOTE_NAME" "$CURRENT_BRANCH"

echo "Done."
