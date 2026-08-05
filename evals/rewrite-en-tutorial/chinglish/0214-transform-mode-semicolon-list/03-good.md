The Publish skill has two modes.

**Transform mode** walks through the entire conversion in one pass:

- Asks for your new repo name and your own name (intake).
- Removes every trace of the cardinal teaching setup: `docs/learn-this-project/`, `README-cn.md`, and the five generated sibling skills. It keeps `learn-this-project-meta/`, since that's a portfolio bonus.
- Asks you, file by file, whether each borderline file stays or goes.
- Generates a dependency ordered commit list at `tmp/publish-commit-plan.md`.
- Co-writes your English README with you in D-mode, section by section (it asks, you answer, it writes, you edit).

**Audit mode** is a hostile scanner. It assumes an interviewer is hunting for proof this started as a tutorial, and it digs out every trace in file names, README wording, commit messages, and git tags or branches.
