# Agent notes for bp-test

KiCad work in this repo goes through the **kicadmium** Agent Portal plugin
(https://github.com/meawoppl/agent-portal-plugins, under `kicadmium/`; issues carry the `kicadmium` label). It provides the `kicadmium` CLI, the
native `kct` tool port, the browser workbench, and the `kicadmium:*` skills.
Projects are declared in `.kicad-pcb.json` at the repo root.

## kicadmium setup (run once per machine; every step is idempotent)

Check first. If all three pass, skip to "Using kicadmium".

```sh
which kicadmium                      # expect ~/.local/bin/kicadmium
kicadmium doctor --json --cwd . | head -c 300   # expect "ok": true
agent-portal plugin list | grep kicadmium       # expect enabled
```

If anything is missing:

```sh
# 1. Install and build the plugin (Rust; builds target/release/kicadmium).
#    Needs cargo, trunk and the wasm32-unknown-unknown target. Agent shells
#    often lack ~/.cargo/bin on PATH; the install fails with "cargo: not
#    found" and leaves the plugin unregistered if so.
export PATH="$HOME/.cargo/bin:$PATH"
agent-portal plugin install github:meawoppl/agent-portal-plugins//kicadmium   # runs setup (the build) itself
# To update an installed plugin: `agent-portal plugin remove kicadmium`, then
# install again. Install refuses to overwrite an existing plugin directory.

# 2. Put the binary on PATH. The plugin does not do this itself, and the
#    kicadmium skills assume `kicadmium ...` resolves from the shell.
mkdir -p ~/.local/bin
ln -sfn ~/agent-portal-plugins/kicadmium/target/release/kicadmium ~/.local/bin/kicadmium
case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) echo 'add ~/.local/bin to PATH in your shell profile';; esac

# 3. Verify.
kicadmium doctor --json --cwd .            # ok:true, tools.kicad-cli and tools.kct true
agent-portal plugin doctor kicadmium       # same report, via the plugin runner
kicadmium kct -- lint --help
```

KiCad itself (`kicad-cli`, 10.x) must already be installed; kicadmium never
downloads it. It is discovered via `KICADMIUM_KICAD_CLI`, `KICAD_CLI`, or PATH.

## Using kicadmium

- **Skills.** Load `kicadmium:pcb-workflow` before any board work and
  `kicadmium:kct-lint` before changing geometry. These two, plus
  `kicadmium:kicad-tools-automation`, may be missing from the session's
  advertised skill list even though they load fine when invoked by name.
  `agent-portal plugin skills` lists everything the plugin ships.
- **Workbench.** `agent-portal plugin open kicadmium` starts the surface and
  forwards it. Open a specific board with `?project=<id>` on the URL
  (`agent-portal plugin status kicadmium` shows the port). Stop it with
  `agent-portal plugin stop kicadmium` when done.
- **Lint, read-only.**
  `kicadmium kct -- lint run boards/<board>/<board>.kicad_pcb --format json`
  does not write anything. Redirect to a file instead of piping into `head`;
  `kct` panics with a broken-pipe backtrace when the reader closes early.
- **Mutating `kct` commands are design edits.** Clean tree or an explicit
  branch only, and commit `<board>.lint.json` together with the board.
- Layout preferences and the DRC-gap checklist live in `docs/pcb-playbook/`.
