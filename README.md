# Obsidian 2 Jekyll

This is a simple python script that converts [Obsidian](https://obsidian.md/) notes to a format that is compatible with [Jekyll](https://jekyllrb.com/) themes that support wikilinks and backlinking like [Jekyll Garden](https://github.com/Jekyll-Garden/jekyll-garden.github.io) or [Digital Garden Jekyll Template](https://github.com/maximevaillancourt/digital-garden-jekyll-template). It adds the filename to the frontmatter as a title and lets you set the visibility of your notes on a folder or note-by-note basis.

## Prerequisites

* [Python3](https://www.python.org/downloads/) installation.

## Usage Instructions

### Converting

To convert your vault into theme-compatible markdown, run

```
python3 [OBSIDIAN_VAULT_DIR] [OUTPUT_DIR]
```

### Controlling the Visibility of your Notes

Notes are either **public** or **private**, where the script does not copy over notes that are defined as **private**.

* To explicitly set a note to **public** or **private**, include `public: yes` or `public: no` in the yaml frontmatter.
* If a note does not define its own visibility, it inherits the visibility of the folder it resides in. Folders can be made public or private by placing a `.public` or a `.private` file in the directory.
* If the directory does not define its own visibility, it inherits the visibility of its parent directory.
* If the parent directory also does not do not define or inherit a visibility, the visbility defaults to **private**.


## Limitations

* (TODO) & in the filename breaks links
* (TODO) obsidian aliases do not work atm
* duplicate filenames - when there are two notes with the same name, only one will be copied to the destination directory
* only works for jenkyll themes that support wikilinks - would need conversion to standard markdown links


## Duct Tape Obsidian Publish

This script is part of my selfmade Obsidian publish setup, which is roughly outlined below. It uses the [Jekyll Garden](https://github.com/Jekyll-Garden/jekyll-garden.github.io) theme and Github Pages to publish the notes.

The setup consists of 3 separate repositories:

* obsidian-to-jekyll (this one)
* jekyll-theme (the repository of the Jekyll theme connected to Github Pages)
* obsidian-vault (the Bbsidian vault connecten via [Obsidian Git](https://github.com/denolehov/obsidian-git) sync)


```
ducttape-obsidian-publish
├── obsidian-to-jekyll
├── jekyll-directory
└── obsidian-vault
```

The following Github workflow is placed in the obsidian-vault repository and opdates the Jekyll page whenever there is a change to the vault.
Add ssh credentials and adjust the filepaths if you intend to use the workflow in your own setup.

```
name: Publish Notes to Jekyll
on: 
  push:
      branches:
        - master
  workflow_dispatch:

jobs:
  deploy-application:
    runs-on: ubuntu-latest
    steps:
    - run: |
        eval $(ssh-agent -s)
        mkdir -p ~/.ssh
        chmod 700 ~/.ssh
        echo "${{ secrets.DEPLOYMENT_SERVER_KEY }}" | tr -d '\r' | ssh-add -
        echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
        ssh ${{ secrets.DEPLOYMENT_SERVER_USER }}@${{ secrets.DEPLOYMENT_SERVER_IP }} "cd /YOURPATH/ducttape-obsidian-publish/obsidian-vault && git pull"
        ssh ${{ secrets.DEPLOYMENT_SERVER_USER }}@${{ secrets.DEPLOYMENT_SERVER_IP }} "cd /YOURPATH/ducttape-obsidian-publish/obsidian-to-jekyll && python3 ./convert.py ../obsidian-vault ../jekyll-directory/NOTE_DIRECTORY"
        ssh ${{ secrets.DEPLOYMENT_SERVER_USER }}@${{ secrets.DEPLOYMENT_SERVER_IP }} 'cd /YOURPATH/ducttape-obsidian-publish/jekyll-directory && git pull && git add . && git commit -m "Update Digital Garden" && git push'
```

## Authors

- **Adrian Steffan** [adriansteffan](https://github.com/adriansteffan) [website](https://adriansteffan.com/)
