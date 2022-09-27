# wikigraph_vis

A project about a network infographic of programming languages (PLs) - an all-at-once visualization of how PLs influence each other and develop over time.

The data comes from Wikipedia, specifically from PL pages that have an "infobox" HTML tag, which has links that can be recursively scraped to construct an adjacency matrix, which in turn translates into a network graph. Each unqiue PL is a node, and relationships between nodes is determined by how PLs relate to one another. Supplementary data can include year of introduction, programming paradigm, and typing discipline.

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
