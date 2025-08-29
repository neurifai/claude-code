# Task Execution Command

Execute a previously planned task from a task file.

## Usage
/brandifai:task-exec <task-file-name>         # Execute task by file pattern
/brandifai:task-exec social-media-scheduler   # Execute task matching this pattern
/brandifai:task-exec .claude/tasks/20250731_161601_social_media_scheduler_backend.md  # Execute specific file

## What it does
1. Finds the task file matching the given pattern or name
2. Validates the task has been properly planned before execution
3. Instructs Claude to execute the plan and todos in that file
4. Follows the execution plan step by step
5. **Continuously updates the task file** with progress and results throughout execution
6. **Updates todo checkboxes** in the task file as tasks are completed ([ ] to [x])
7. **Maintains detailed progress log** with timestamps, actions taken, files created/modified, and results
8. **Handles errors gracefully** and documents them in the progress log

## File Matching
- Searches for task files in `.claude/tasks/` directory
- Matches partial names (e.g., "scheduler" matches "social-media-scheduler")
- Uses the most recent file if multiple matches found
- Accepts full file paths for exact matching
- **Error handling**: If no match found, lists available task files

## Pre-Execution Validation
The handler automatically validates:
- **Task Status**: Checks if task is already completed, failed, or blocked
  - COMPLETED tasks are rejected (user must update Final Status to re-execute)
  - FAILED tasks show warning but allow retry
  - BLOCKED tasks are rejected until issues resolved
- **Plan Completeness**: Validates presence of:
  - Implementation Plan or Execution Plan section
  - File Modifications table with structured format
  - Uncompleted todos (- [ ] format)
  - Implementation Steps section
  - No unfilled "[To be filled by Claude]" sections
- **File Structure**: Ensures task file exists and is readable

## Execution Strategy Selection
The handler determines execution approach based on assessed complexity:

### EASY Complexity
- **Strategy**: Sequential execution
- **Agent Usage**: No sub-agents
- **Validation**: Basic checks only
- **Commits**: Single commit at end

### MEDIUM Complexity (Default)
- **Strategy**: Sequential with milestones
- **Agent Usage**: No sub-agents typically
- **Validation**: Standard testing and validation
- **Commits**: At logical milestones

### HARD Complexity
- **Strategy**: Phased execution
- **Agent Usage**: Spawn sub-agents for complex subtasks
- **Validation**: Comprehensive testing and validation
- **Commits**: After each major phase

## Task Execution Requirements

When executing a task file, Claude must:

### Progress Tracking
1. **Read the task file** to understand the full execution plan and todo items
2. **Update todo checkboxes** in real-time as tasks are completed:
   - Change `- [ ] Task description` to `- [x] Task description` when completed
   - **Update todos immediately** when work is done, even if implementing multiple items in parallel
   - Mark partial completion appropriately (e.g., if implementing features across multiple phases simultaneously)
3. **Maintain detailed progress log** in the task file under "## Progress Log" section:
   - Add timestamped entries for each significant action
   - Document files created, modified, or deleted
   - Note any issues encountered and their resolutions
   - Include git operations performed
   - Track execution time for major phases

### Execution Guidelines

#### Plan Verification
- Review the entire execution plan before starting
- Identify dependencies between TODOs
- Where appropriate, spawn sub-agents for complex tasks
- Follow the plan as closely as possible
- If deviations are necessary, document them in the progress log

#### Code Quality Checks
- Run linters/formatters after creating new files (if configured)
- Ensure new code follows existing patterns identified during planning
- Verify imports and dependencies are properly added
- Check for compilation/syntax errors immediately after file creation

#### Testing During Execution
- After implementing each major component, verify it compiles/runs
- Create basic test files as specified in the plan
- Document any test failures in the progress log
- Note areas that need additional testing

#### Git Operations
- Stage new files after creation (`git add`)
- Make logical commits at phase boundaries if specified
- Use descriptive commit messages referencing the task
- Document commit hashes in progress log

### Error Handling

#### Recoverable Errors
- Document the error in progress log
- Attempt alternative approach if available
- Mark todo as partially complete with notes
- Continue with next independent task

#### Critical Errors
- Stop execution immediately
- Document full error details in progress log
- Update task status to "blocked" or "failed"
- Provide clear next steps for resolution

## Structured Execution Process

The handler provides detailed execution instructions including:

### Execution Phases
1. **Phase 1: Setup** - Create new files, add dependencies
2. **Phase 2: Implementation** - Modify existing files per plan
3. **Phase 3: Testing** - Run tests, fix issues
4. **Phase 4: Validation** - Run lint/build, verify all changes

### Progress Log Format
Use this template for each progress entry:
```markdown
### {timestamp} - {Phase Name}
- Action: {what was done}
- Files: {files created/modified with full paths}
- Result: {success/failure/partial}
- Notes: {any issues or deviations from plan}
- Time taken: {duration}
```

### Error Handling Protocol
1. **Compilation/Syntax errors**: Fix immediately, document fix in log
2. **Missing dependencies**: Add to package.json/pom.xml/requirements.txt, re-run install
3. **Test failures**: Fix if simple, otherwise document and continue
4. **File not found**: Verify path, create parent directories if needed
5. **Permission denied**: Document issue, suggest chmod/sudo fix

### Completion Checklist
Before marking task complete, verify:
- □ All todos marked as done [x]
- □ All files in plan created/modified
- □ Tests written and passing
- □ Lint/build commands successful
- □ Progress log fully updated with timestamps
- □ No unresolved errors documented
- □ Code follows existing patterns from codebase
- □ Documentation updated if specified in plan

### Critical Requirements
- Use EXACT file paths and line numbers from the plan
- Use code snippets provided in the plan
- Update progress log with timestamps after each phase
- Handle errors gracefully and document them
- Run lint/build/test commands after changes
- For HARD complexity: Use Task tool for complex subtasks