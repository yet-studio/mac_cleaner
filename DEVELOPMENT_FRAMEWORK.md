# Development Framework

This document serves as the authoritative guide for all development decisions, ensuring consistency and maintaining focus throughout the development process.

## 1. Development Phases
Each feature MUST go through these phases in order:

### Phase 1: Planning
- [ ] Define feature scope in `PROJECT_TODO.md`
- [ ] Write acceptance criteria
- [ ] Create test scenarios
- [ ] Update architecture documentation if needed

### Phase 2: Test Creation
- [ ] Write unit tests (TDD)
- [ ] Write integration tests
- [ ] Write property-based tests
- [ ] Ensure test coverage requirements

### Phase 3: Implementation
- [ ] Implement feature following TDD
- [ ] Add type hints
- [ ] Add docstrings
- [ ] Implement error handling

### Phase 4: Quality Assurance
- [ ] Run all tests
- [ ] Run type checker
- [ ] Run linters
- [ ] Run security checks
- [ ] Update documentation

## 2. Code Quality Gates
All code MUST pass these gates before being considered complete:

### Testing Gates
- [ ] 100% test coverage
- [ ] All tests passing
- [ ] Property-based tests passing
- [ ] Integration tests passing

### Static Analysis Gates
- [ ] MyPy with strict mode passing
- [ ] Pylint score ≥ 9.5
- [ ] Black formatting passing
- [ ] isort passing
- [ ] Bandit security checks passing

### Documentation Gates
- [ ] Docstrings complete
- [ ] README updated
- [ ] Architecture docs updated
- [ ] API documentation complete

## 3. Feature Implementation Rules

### Rule 1: Single Responsibility
- Each module has ONE clear purpose
- Each class has ONE responsibility
- Each function does ONE thing
- Max function length: 20 lines
- Max class length: 200 lines

### Rule 2: Error Handling
- All errors MUST be caught and handled
- Custom exceptions for domain errors
- No silent failures
- Proper error messages
- Error logging

### Rule 3: Type Safety
- All code MUST be type-hinted
- No `Any` types unless absolutely necessary
- No implicit optional parameters
- No dynamic attribute access
- Generic types where appropriate

### Rule 4: Testing
- Test FIRST, code SECOND
- One assertion per test
- Use fixtures for setup
- Mock external dependencies
- Test edge cases with property-based tests

### Rule 5: Documentation
- Every public API must be documented
- Examples in docstrings
- Architecture decisions documented
- Update docs before marking complete

## 4. Development Workflow

### Step 1: Feature Branch
```bash
git checkout -b feat/feature-name
```

### Step 2: Development Cycle
1. Write failing test
2. Write minimum code to pass
3. Refactor
4. Repeat

### Step 3: Quality Check
```bash
# Run all checks
pytest
mypy .
black .
isort .
pylint src tests
bandit -r src
```

### Step 4: Documentation
- Update relevant documentation
- Add code examples
- Update architecture docs if needed

### Step 5: Review
- Self-review against this framework
- Update PROJECT_TODO.md
- Create pull request

## 5. AI Assistant Guidelines

### Rule 1: Consistency
- Always follow this framework
- No shortcuts or exceptions
- Reference this document when making decisions

### Rule 2: Communication
- Explain decisions based on framework
- Reference specific rules when making choices
- Keep track of progress in PROJECT_TODO.md

### Rule 3: Focus
- Work on one feature at a time
- Complete all phases before moving on
- Don't mix concerns across features

### Rule 4: Quality First
- Never skip quality gates
- No temporary solutions
- No "we'll fix it later"

## 6. Progress Tracking

### Feature Status Template
```markdown
## Feature: [Name]
Status: [Planning/Testing/Implementation/QA/Complete]
- [ ] Phase 1 Complete
- [ ] Phase 2 Complete
- [ ] Phase 3 Complete
- [ ] Phase 4 Complete
```

### Quality Gates Status
```markdown
## Quality Gates
- [ ] Testing Gates
- [ ] Static Analysis Gates
- [ ] Documentation Gates
```

## 7. Version Control Guidelines

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- test: Adding tests
- refactor: Code refactoring
- style: Formatting
- chore: Maintenance

## 8. Definition of Done
A feature is only considered DONE when:
1. All phases are complete
2. All quality gates are passed
3. Documentation is updated
4. PROJECT_TODO.md is updated
5. All tests are passing
6. Code review is complete
