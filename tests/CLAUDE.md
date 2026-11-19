# CLAUDE.md: Agentic PR cost calculator, the tests
These rules add to this repository's root `CLAUDE.md` for work on files under `tests/`, or make its
rules stricter there. They never loosen it: where one would, the root wins, so tell the owner.
Unless the root's text is in front of you, read it first. The guide, `docs/patterns.md`, steers
below the root and this file, and its concern Testing gives the principles that these rules rest on;
records DR-084 to DR-093 and DR-109 are their long form.
- Test everything that can be tested.
- Positive and negative tests reach every boundary.
- Invariants get property-based tests. The tool's code keeps 100% branch coverage and survives
  mutation testing.
- Tests never use the network: recorded responses stand in for APIs.
- A check of the documentation compares it with a source that a machine reads, such as a spec, a
  workflow, a record or a file, and is added only where its kind of defect has reached the default
  branch or a review, or a threat with a risk of 4 or more rests on it. A rule about prose, such as
  whether a citation covers what it replaces, is held by review (DR-251).
