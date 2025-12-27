# Research: Phase I CLI Todo Application

**Feature**: 001-phase1-cli-todo
**Date**: 2025-12-27
**Phase**: Phase 0 (Research)

## Research Summary

Phase I scope is fully specified and requires minimal research. All technical decisions are constrained by Phase I boundaries (no external dependencies, in-memory only, console interface).

## Technical Decisions

### Decision 1: Python Version

**Question**: Which Python version to target?

**Research**:
- Python 3.11 released October 2022, widely adopted as of 2025
- Python 3.11+ provides improved error messages, helpful for console application debugging
- Python 3.12+ available but 3.11 is more universally installed
- No async/await needed for Phase I (single-threaded console app)

**Decision**: Python 3.11 or higher

**Rationale**:
- Balances modern features with broad compatibility
- No external dependencies means version choice has minimal impact
- Standard library features (input, print, list, dict) unchanged across 3.11-3.13
- Clear error messages benefit development and debugging

**Alternatives Considered**:
- Python 3.8/3.9: Too old, less clear error messages
- Python 3.13: Too new, not universally installed yet

### Decision 2: Data Storage Structure

**Question**: How to store tasks in memory?

**Research**:
- Options: List of dictionaries, list of tuples, list of custom objects, dictionary of dictionaries
- List of dictionaries: Pythonic, easy to iterate, simple to understand
- Custom classes: More structure but overkill for Phase I
- Dictionary of dictionaries: O(1) lookup but requires key management

**Decision**: List of dictionaries with linear search

**Rationale**:
- Simple and Pythonic
- No external dependencies or complex data structures
- O(n) search acceptable for Phase I scale (dozens to hundreds of tasks)
- Easy to serialize to JSON in Phase II when adding API
- No premature optimization

**Alternatives Considered**:
- Custom Task class: Deferred to Phase II when API needs serialization
- Dict of dicts (keyed by ID): Adds complexity without meaningful benefit at Phase I scale

### Decision 3: Input Validation Strategy

**Question**: How to handle invalid user input?

**Research**:
- Options: Try-except on every input, pre-validation with regex, type hints with validation library
- Python's input() returns strings, need conversion for integers
- ValueError raised when int() fails on non-numeric strings
- KeyboardInterrupt (Ctrl+C) should be handled gracefully

**Decision**: Try-except blocks for numeric conversion, strip/length checks for strings

**Rationale**:
- Standard Python error handling, no external dependencies
- Clear error messages aligned with spec requirements
- Graceful handling of Ctrl+C for user-friendly exit

**Alternatives Considered**:
- Regex validation: Overkill for simple integer/non-empty-string checks
- Validation library (pydantic): Violates "no external dependencies" constraint

### Decision 4: Display Formatting

**Question**: How to format task list for console display?

**Research**:
- Options: Plain text lines, ASCII table, rich library (colored tables)
- Spec requires "readable format with clear separation between fields"
- No external dependencies allowed (rules out rich, tabulate, prettytable)
- Manual string formatting with padding sufficient for console display

**Decision**: Manual ASCII table with fixed-width columns

**Rationale**:
- No external dependencies
- Clear separation between fields (ID, title, description, status)
- Works on all terminals/consoles
- Simple to implement with f-strings

**Alternatives Considered**:
- Rich library: Violates "no external dependencies" constraint
- JSON output: Not user-friendly for console interaction
- CSV format: Less readable than ASCII table

### Decision 5: Function vs Class-Based Design

**Question**: Should we use functions or classes for business logic?

**Research**:
- Functions: Simple, stateless, easy to test
- Classes: Encapsulation, state management, OOP patterns
- Phase I is single-user, no concurrency, no complex state management
- Phase II will need classes for API models (Pydantic/SQLModel)

**Decision**: Function-based design for Phase I

**Rationale**:
- Simpler for single-file script
- No state management needed (global tasks list is sufficient)
- Easier to understand for console application
- Phase II refactor will introduce classes for API layer

**Alternatives Considered**:
- Class-based (TodoManager, Task classes): Premature for Phase I, defer to Phase II

## Performance Considerations

**Expected Scale**: 10-1000 tasks per session

**Performance Analysis**:
- Task creation: O(1) - append to list
- Task viewing: O(n) - iterate and print
- Task lookup: O(n) - linear search by ID
- Task update: O(n) - find then modify
- Task deletion: O(n) - find then remove

**Verdict**: All operations acceptable for Phase I scale. No optimization needed.

**Future Optimization** (Phase II+):
- If task count exceeds 10,000: Use dictionary keyed by ID for O(1) lookup
- If viewing becomes slow: Implement pagination
- For now: Keep it simple

## Testing Strategy

**Phase I Testing**: Manual acceptance testing per specification scenarios

**Rationale**:
- Spec provides clear Given/When/Then scenarios for each user story
- Console application difficult to automate without external test framework
- pytest would be external dependency (violates Phase I constraints)
- Phase II will introduce automated testing when API layer added

**Manual Test Checklist**: Will be derived from acceptance scenarios in spec.md

## Dependencies Assessment

**External Dependencies**: None (Python standard library only)

**Standard Library Modules Used**:
- `sys` - For exit handling
- No other imports needed (input, print, list, dict are built-ins)

**Phase II Preparation**:
- Structure code for easy refactor when introducing FastAPI, Pydantic
- Keep functions modular and single-responsibility
- Avoid tight coupling between display and business logic

## Risk Assessment

**Risk 1: User enters extremely long input (millions of characters)**
- **Mitigation**: Python handles large strings in memory; crash unlikely but possible
- **Phase I Acceptance**: Spec explicitly allows "arbitrary lengths" - out of scope for Phase I validation
- **Phase II Resolution**: Add max length validation when API layer introduced

**Risk 2: User expects data persistence**
- **Mitigation**: Clear messaging on startup and exit: "All data will be lost on exit"
- **Spec Requirement**: Explicitly states no persistence for Phase I

**Risk 3: Ctrl+C crashes application ungracefully**
- **Mitigation**: Wrap main loop in try-except KeyboardInterrupt, display "Exiting..." message

## Open Questions

*None* - All Phase I technical decisions resolved. Spec is clear and complete.

## Research Artifacts

- Python 3.11 documentation: https://docs.python.org/3.11/
- Python f-string formatting: https://docs.python.org/3/reference/lexical_analysis.html#f-strings
- Python exception handling: https://docs.python.org/3/tutorial/errors.html

## Sign-off

**Research Status**: ✅ Complete
**Next Phase**: Phase 1 (Design - data-model.md, quickstart.md)
