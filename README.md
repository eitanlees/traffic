# Traffic

A traffic tracker.

I want to know how long it will take me to drive to work. 

## DEV LOG

### 2024-09-23 (Inital setup):

Aaahhh that fresh repository smell. Let's see how long it takes to muck things up.

I have never used [Poetry](https://python-poetry.org/) before, so lets give that a shot!
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

As this is not a package, I need to set `package-mode = false` in the `pyproject.toml` file.
```bash
[tool.poetry]
package-mode = false
```

To install the dependencies only, such as when deploying this application, run the install command with the --no-root flag:
```bash
poetry install --no-root
```

I have installed the cursor editor and I experimenting with an AI centric workflow. We will see how this goes. 

I have the basic structure of the program outlined. Next time, I am now going to try to set up the database. 