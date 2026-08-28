# gtosh4's Claude Code skills

A [Claude Code](https://claude.com/claude-code) plugin marketplace. Add it once, install
whichever skills you want.

## Install

```
/plugin marketplace add gtosh4/claude-skills
/plugin install listo-build@gtosh4-skills
/plugin install artifact-publisher@gtosh4-skills
```

Restart Claude Code (or run `/plugin`) and the skill is live — Claude picks it up
automatically when it's relevant, or you can invoke it directly with `/listo-build`.

## Updating

```
/plugin marketplace update gtosh4-skills
```

## Skills

### `listo-build`

Plans Baldur's Gate 3 character builds for the **Listonomicon** modlist, assuming a
two-player Lone Wolf run, and publishes the result as a character-sheet artifact.

Listo changes enough of BG3 that vanilla build knowledge is actively misleading, and the
published docs lag the shipped list (the docs site stops at v10.0; the Wabbajack gallery
ships 10.2). The skill checks everything load-bearing against a bundled copy of the actual
10.2 manifest instead of the docs.

Ask for a build — "plan me a Listo gloomstalker", "what feats are worth taking on a Lone
Wolf paladin" — and it'll work from what the modlist actually contains.

### `artifact-publisher`

Adds MCP tools for listing, reading, and updating existing `claude.ai/code/artifact` pages.
Updates require reading the live source first and carry its version as an optimistic-concurrency
precondition, so a concurrent publish is refused instead of overwritten. It uses an existing OMP
or Claude Code OAuth login and never returns credentials through MCP.

## Adding more skills

Drop a new plugin under `plugins/<name>/` with a `.claude-plugin/plugin.json` and a
`skills/<name>/SKILL.md`, then add an entry to the `plugins` array in
`.claude-plugin/marketplace.json`.
