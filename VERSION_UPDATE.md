# Version Update Guide

This website displays the build version in the footer automatically based on Git commit count.

## How it works

The version information is stored in `_data/version.yml` and is automatically updated by the `update_version.sh` script.

## Updating the version

### Method 1: Manual update (recommended)

Before committing and pushing changes, run:

```bash
./update_version.sh
git add _data/version.yml
git commit -m "Update version"
git push
```

### Method 2: Automatic update with Git hook

You can set up a pre-push hook to automatically update the version:

```bash
# Create pre-push hook
cat > .git/hooks/pre-push <<'EOF'
#!/bin/bash
./update_version.sh
git add _data/version.yml
git commit --amend --no-edit
EOF

chmod +x .git/hooks/pre-push
```

## What gets displayed

The footer will show:
- **Version**: v{build_number} (e.g., v451)
- **Build Number**: Total Git commit count
- **Commit Hash**: Short Git commit hash (in version.yml, not displayed on site)
- **Last Updated**: Date of last version update (in version.yml, not displayed on site)

Example: `Version v451 (Build #451)`

## Files involved

- `_data/version.yml` - Stores version information
- `update_version.sh` - Script to update version from Git
- `_includes/footer.html` - Displays version in footer
- `_plugins/git_version.rb` - Legacy plugin (not used, kept for reference)
