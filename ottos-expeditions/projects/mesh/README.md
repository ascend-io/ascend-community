# Otto's Expeditions on {{ .DataPlane }}

This directory contains an example project for Otto's Expeditions on {{ .DataPlane }}.

You can find [the quickstart document here](https://docs.ascend.io/getting-started/quickstart-{{ .DataPlaneLower }}).

## Internal

TODO: work in progress.

### Instance setup

- [`ottos-expeditions.app-dev`](https://ottos-expeditions.app-dev.ascend.io): no setup needed!
- [`ascend` CLI](https://instance.app.local.ascend.dev): no setup needed!
- [local Instance](https://instance.app.local.ascend.dev): setup the Repo and Project

For any other instance, you need to give access to the Environments GCP identities to the corresponding `ottos-expeditions-*` GCP project's google secret manager (GSM). Use the infra repo. Instructions coming soon.

You setup the Repo, use `git@github.com:ascend-io/ascend-community-internal`...for the Git SSH key, instructions coming soon.

For the Project, use `ottos-expeditions/projects/mesh`.

### Developing

Run these `just` commands from the `ottos-expeditions/oeutils` directory.

Format/lint:

```bash
just fmt
```

Build:

```bash
just build
```

Test:

```bash
just test
```

### Releasing

Run these `just` commands from the `ottos-expeditions/` directory.

Unmesh:

```bash
just unmesh
```

Commit the changes (after reviewing):

```bash
git add .
git commit -m "just unmesh"
git push
```

Release:

```
just release
```

