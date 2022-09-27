# wikigraph_vis

This project is about creating a network infographic of programming languages, a visualization of how lanaguages influence each other and develop over time.

The data comes from Wikipedia, specifically from pages that have an "infobox" HTML tag, which has links that can be recursively scraped to construct an adjacency matrix, which in turn translates into a network graph - with unqiue programming languages as nodes and the relationships between them as the graph's directed links.

### Git Setup Cheatsheet

First download the repo through CLI and use `checkout -b` to create and name a new branch.

```
cd src
gh repo clone dirediredock/wikigraph_vis
cd wikigraph_infobox
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
