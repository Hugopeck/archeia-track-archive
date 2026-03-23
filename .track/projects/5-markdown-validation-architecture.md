# Markdown Validation Architecture

## Goal

Design a future markdown validation stack that strengthens contracts without
creating a second canonical spec surface.

## Why Now

The repo now has stronger governance boundaries. This is the right time to
design validation around protocol extraction rather than start with hand-written
schema files that would drift.

## In Scope

- validation level definitions
- extraction-path design from protocols and templates
- canonicality rules for any future machine-readable mirrors

## Out Of Scope

- implementing a generic markdown validator in this phase
- adding new canonical schema files by hand
- repo-wide formatting enforcement before ownership is clear

## Shared Context

`docs/designs/markdown-validation.md` owns the architecture direction here.
Track and Archeia should remain free to keep their current executable contracts
until a future extraction-based implementation is ready.

## Dependency Notes

This project depends on the governance foundation defining where rules live.
Future implementation work should not start until that boundary remains stable.

## Success Definition

- validation levels are well-defined
- canonicality rules prevent shadow specs
- future implementation work can be decomposed without redefining ownership

## Candidate Task Seeds

- decide which document families merit deterministic validation first
- design an extraction format from protocols/templates if needed
- prototype formatting and semantic checks only after canonicality is locked

