# wikiscrape_grapherator

This project is aobut recursively extracting data from Wikipedia "infoboxes" and use that to build network graph visualizations.

### Git Setup Cheatsheet

First download the repo through CLI and use `checkout -b` to create and name a new branch.

```
cd src
gh repo clone dirediredock/wikiscrape_grapherator
cd wikiscrape_vis
git status
git checkout -b desktop_edits
git status
```

When work of the day is complete, commit all changes on VS Code and `push`, then return to `main` for a fresh start next time.

```
git push
git push --set-upstream origin desktop_edits
git fetch origin main:main
git checkout main
```
