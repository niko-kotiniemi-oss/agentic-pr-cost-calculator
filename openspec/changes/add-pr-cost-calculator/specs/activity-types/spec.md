## Purpose

Label each recorded model call with the kind of work it was part of, from a fixed list, so that the report can split a pull request's cost by activity.

Scenarios below that run the capture step follow the conventions that `usage-capture` states for its own scenarios.

## ADDED Requirements

### Requirement: Each entry carries an activity type

Each entry SHALL carry one activity type derived from the tools its call invoked: code generation for file edits and writes, file reading for reads and searches, tooling for shell commands, MCP for MCP tool calls, subagent for starting a subagent, other for a tool the classification does not know, and conversation when no tool was called. A call that invoked tools of several types SHALL carry its first tool call's type. Tool names SHALL be read only to choose the type and SHALL NOT be recorded.

#### Scenario: An edit is code generation

- **WHEN** a model call's only tool call edits a file
- **THEN** its entry's activity type is code generation

#### Scenario: An unknown tool is other

- **WHEN** a model call invokes a tool the classification does not know
- **THEN** its entry's activity type is other

#### Scenario: An MCP call does not record the server's name

- **WHEN** a model call invokes a tool of an MCP server
- **THEN** its entry's activity type is MCP, and no part of the MCP tool's or its server's name is in the ledger

#### Scenario: A file write is code generation

- **WHEN** a model call's only tool call writes a file
- **THEN** its entry's activity type is code generation

#### Scenario: A read or a search is file reading

- **WHEN** a model call's only tool call reads a file or searches files
- **THEN** its entry's activity type is file reading

#### Scenario: A shell command is tooling

- **WHEN** a model call's only tool call runs a shell command
- **THEN** its entry's activity type is tooling

#### Scenario: Starting a subagent is subagent

- **WHEN** a model call's only tool call starts a subagent
- **THEN** its entry's activity type is subagent

#### Scenario: A reply with no tool call is conversation

- **WHEN** a model call calls no tool
- **THEN** its entry's activity type is conversation

#### Scenario: A call with tools of several types takes its first tool's type

- **WHEN** a model call's first tool call runs a shell command and a later one edits a file
- **THEN** its entry's activity type is tooling
