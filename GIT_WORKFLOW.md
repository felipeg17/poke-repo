# Git Workflow Summary: Fork to Pull Request

## Initial Setup

### 1. Add Upstream Remote
```bash
git remote add upstream https://github.com/felipeg17/poke-repo
```

### 2. Verify Remotes
```bash
git remote -v
```

Should show:
- `origin` - your forked repository
- `upstream` - the original repository

## Sync with Upstream

### 3. Fetch Latest Changes from Upstream
```bash
git fetch upstream
```

### 4. Switch to Your Local dev Branch
```bash
git checkout dev
```

### 5. Merge Upstream Changes into Local dev
```bash
git merge upstream/dev
```

### 6. Push Updated dev to Your Fork
```bash
git push origin dev
```

## Create Feature Branch

### 7. Create and Switch to New Feature Branch
```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### 8. Make Your Changes
- Edit files
- Add new features
- Fix bugs

### 9. Stage Changes
```bash
git add .
```
or for specific files:
```bash
git add filename.py
```

### 10. Commit Changes
```bash
git commit -m "Add descriptive commit message"
```

### 11. Push Feature Branch to Your Fork
```bash
git push origin feature/your-feature-name
```

## Create Pull Request

### 12. Navigate to GitHub UI
1. Go to your forked repository on GitHub
2. Click **"Compare & pull request"** button
3. Set:
   - **Base repository:** `felipeg17/poke-repo`
   - **Base branch:** `dev`
   - **Head repository:** `your-username/poke-repo`
   - **Compare branch:** `feature/your-feature-name`
4. Add title and description
5. Click **"Create pull request"**

## Additional Commands (As Needed)

### Check Status
```bash
git status
```

### View Commit History
```bash
git log --oneline
```

### Switch Between Branches
```bash
git checkout branch-name
```

### Update Feature Branch with Latest dev
```bash
git checkout feature/your-feature-name
git rebase dev
```

## Example Complete Workflow

```bash
# Initial setup (do once)
git remote add upstream https://github.com/felipeg17/poke-repo
git remote -v

# Start new feature
git fetch upstream
git checkout dev
git merge upstream/dev
git push origin dev
git checkout -b feature/add-pokemon-stats

# Development cycle
# ... make changes ...
git add .
git commit -m "Add Pokemon stats calculation"
git push origin feature/add-pokemon-stats

# Create PR via GitHub UI
# ... follow steps 12 above ...
```

## Notes

- Always sync with upstream before starting new work
- Write clear, descriptive commit messages
- Keep commits focused and atomic
- Test your changes before pushing

This workflow ensures your fork stays synchronized with the upstream repository and follows best practices for collaborative development.