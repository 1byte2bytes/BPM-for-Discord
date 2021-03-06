# BPM for Discord

This directory contains code for installing and running BPM inside of Discord's Mac and Windows Desktop apps (Linux support coming when a desktop app is added to Linux).

All changes to the build process are contained in the Makefile of the root of the repo.

## Development practices

All changes to Discord-specific code should be done on the `discord` branch.  All of these changes should live in the `discord` directory.  Browser code should live in `discord/addon`, `app.asar` code should live in `discord/integration` and installer code should live in `discord/installer`. 

All changes to the BPM core should be made on the `discord-core-changes`  branch.  These changes are being PR'd up to the BPM main repo.  When these changes are committed to the branch `discord` should be rebased on top of `discord-core-changes` (I am aware this will require a `git push --force origin discord`.  I am willing to accept that risk on my own repo).

Eventually once [the core repo PR](https://github.com/Rothera/bpm/pull/12) is merged in, we'll pull the upstream master branch into this fork's master and then rebase `discord` on top of it.  `discord-core-changes` will be kept for posterity.

## Build

Building BPM for Discord requires:
* Standard 'nix command-line tools (`make`, `mkdir`, `rm`, `cat`, `cd` specifically)
* Getting the BPM build chain working (Python2, Python3, Mozilla tools, see the base README.md)
* [Node.js](https://nodejs.org/en/download/) `v4.2.x`
* [`webpack`](https://www.npmjs.com/package/webpack) -- this can be acquired via `npm install -g webpack`
* [`asar`](https://www.npmjs.com/package/asar) -- this can be acquired via `npm install -g asar`

Releasing BPM for Discord requires:
* A `7z` installation on your `PATH`. 
* `git`on your `PATH`.

The following build hooks are available:
* `make discord`
* `make discord/release`

### `make discord`

1. Moves all files from `discord/installer` to `build/discord`
2. Packs all files from `discord/integration` into `integration.asar` and moves it to `build/discord/integration.asar`
3. Builds all BPM content and scripts into `build/addon`
4. Moves required addon files from `build/addon` to `build/discord/addon/core` to support building `core.js`
5. Builds `bpm.js` via Webpack and moves it to `build/discord/addon`
5. Find/Replace-s the current version numbers into compiled `build/discord/addon/bpm.js` 
6. Compiles `build/discord/addon` to `build/discord/bpm.asar`
7. `cat`s together `build/better-discord/betterDiscord-plugin.js`
9. Deletes `build/discord/addon`

The final contents of `build/discord` should now look like this:
    
    /bpm.asar
    
    /integration.asar
    
    /CONTENTS-OF-`discord/installer`

The contents of `build/better-discord` should be:

    /betterDiscord-plugin.js

### `make discord/release`

Requires an environment variable, `$DISCORD_RELEASE_GITHUB_API_TOKEN`.  This token should have `repo` permissions.

1.  Ensures `make discord` has been run/is up to date
2.  Adds, commits, and pushes `discord/RELEASE_NOTES.md`.
3.  Executes `git status` and `git log -1` and prompts the user if they're sure this is what they want to release
4.  If the user is sure, tags the current branch's `HEAD` with `DISCORD-VERSION` from the Makefile (if the tag already exists this process fails)
5.  Pushes the new tag to github
6.  Packs the contents of `build/discord` into `build/BPM for Discord DISCORD-VERSION.7z`
7.  Creates a release associated with the tag `DISCORD_VERSION`, and a base branch of `DISCORD_RELEASE_BASE_BRANCH`.  The body is identical to `discord/RELEASE_NOTES.md`

Note this intentionally does *not* place `betterDiscord-plugin.js` into the 7z file.

You will need to manually upload the release files after testing and mark the release as not a draft/pre-release.

### `make discord/upload-release-asstes`

Not yet functional.  Do not use.  Intended to upload assets for the release after they've been tested.

### `make discord/clean-tag`

Deletes the tag `DISCORD_VERSION` locally and on the remote.  Intended for use while testing new release automation code.

## Releases and Updates

BPM for Discord includes update notifications as part of its core feature set.  Updates are detected using the Github API's Releases endpoint.  If the user's current version does not match the name of the `tag` the latest non-draft, non-pre-release Release pulled from the API, they are notified in some way to update their BPM install.

What this means practically for performing releases:

**DO NOT SAVE A NON-DRAFT RELEASE AS A NON-PRE-RELEASE UNTIL YOU HAVE TESTED THE 7Z LOCALLY**

 All users (as of `discord-v0.5.0-beta`) will be notified that this has occured and will try to update accordingly.  

If you wish to perform a release that does _not_ notify users (for example if only the installers have been updated or the feature set is small enough that it's not worth bothering our end users), upload the release but **flag it as a pre-release**.

## Submodules

* <a href="https://github.com/ByzantineFailure/bpm/tree/discord/discord/installer">Installer</a>
* <a href="https://github.com/ByzantineFailure/bpm/tree/discord/discord/integration">Integration</a>
* <a href="https://github.com/ByzantineFailure/bpm/tree/discord/discord/addon">Addon</a>
* <a href="https://github.com/ByzantineFailure/bpm/tree/discord/discord/better-discord">Better Discord Plugin</a>

See each subfolder for what each submodule does.

