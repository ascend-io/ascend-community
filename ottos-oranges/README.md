# Otto's Oranges

Data generation for Otto's Oranges.

## Setup

Clone the repo:

```bash
git clone git@github.com:ascend-io/ascend-community.git
```

or:

```bash
gh repo clone ascend-io/ascend-community
```

Change into the directory:

```bash
cd ascend-community/ottos-oranges
```

Install `just` and `uv`:

```
brew install just uv
```

`just setup`:

```bash
just setup
```

Source the Python vritual environment:

```bash
source .venv/bin/activate
```

Run the data generation:

```bash
ottos-oranges datagen --days 1
```

