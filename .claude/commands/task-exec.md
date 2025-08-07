# Task Execution Command

Execute a previously planned task from a task file.

## Usage
/task-exec <task-file-name>         # Execute task by file pattern
/task-exec social-media-scheduler   # Execute task matching this pattern
/task-exec .claude/tasks/20250731_161601_social_media_scheduler_backend.md  # Execute specific file

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
Before executing, Claude must verify:
- Task file exists and is readable
- Task has been properly planned (contains execution plan/todos)
- No critical blockers are documented in the task
- Required dependencies/tools are available
- Task status is not already "completed"

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

### Progress Log Format
```markdown
## Progress Log

### 2025-08-01 10:30:00 - Task Execution Started
- Started executing Social Media Scheduler Backend task
- Analyzed existing codebase structure and patterns
- Validated all dependencies available
- Estimated completion time: 45 minutes

### 2025-08-01 10:35:00 - Foundation Models Created  
- Created MediaFile.java - src/main/java/com/buttrcrm/aigen/models/scheduler/MediaFile.java
- Created ScheduledEventStatus.java enum
- Created SocialMediaPlatform.java enum  
- Created ScheduledEvent.java entity
- Added SOCIALSCHEDULER constant to DataModelPSKeys.java
- All new files added to git staging
- Compilation successful - no errors

### 2025-08-01 10:40:00 - Error Encountered
- ERROR: Failed to create repository interface
- Cause: Missing JPA dependency in pom.xml
- Resolution: Added spring-boot-starter-data-jpa dependency
- Retrying repository creation...

### 2025-08-01 10:45:00 - Service Layer Implementation
- Created SchedulerService.java with core business logic
- Implemented platform-specific posting strategies
- Added comprehensive error handling
- Unit tests created: SchedulerServiceTest.java
- All tests passing (5/5)
```