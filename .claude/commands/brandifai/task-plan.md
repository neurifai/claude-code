Create detailed execution plan for an existing task file

# Task Plan Command

Analyzes an existing task file and creates a detailed execution plan with specific todos, but does NOT execute any code.

## Usage
/brandifai:task-plan task-name-slug
/brandifai:task-plan user-authentication  
/brandifai:task-plan payment-bug-fix
/brandifai:task-plan reports-api

## What it does
1. Finds the task file by name in `.claude/tasks/` directory
2. Reads the existing task content and complexity assessment
3. **Performs required codebase analysis** to understand existing patterns
4. Creates a detailed execution plan following architecture patterns defined in CLAUDE.md. If there is no CLAUDE.md, use best practices for the given technology stack
5. Updates the task file with specific todos and implementation steps using structured template
6. Uses thinking mode for medium/hard complexity tasks to work through design decisions
7. **Validates the plan** against completion checklist
8. **STOPS after planning - does not implement any code changes**

## Strict Planning-Only Constraints
During task planning, Claude is RESTRICTED to:
- **ALLOWED tools:** Read, Grep, Glob, LS (for research), TodoWrite (for task management), Edit (ONLY for updating the task file itself)
- **PROHIBITED tools:** Write (creating new files), Edit (modifying code files), Bash (implementation commands), MultiEdit
- **REQUIRED:** Must explicitly state when planning is complete and stop execution
- **FORBIDDEN:** Any code implementation, file creation, or modification of existing code files

## Architecture Patterns
The command ensures Claude follows established patterns:

### Apply Universal Best Practices
Regardless of stack, ensure the plan follows:

**Security First**
- Input validation at all entry points
- Authentication/authorization checks where needed
- Sanitization of user-provided data
  - Never trust client-side validation alone
  - Validate and sanitize on the server side as well
- Secure handling of sensitive information
- Protection against common vulnerabilities (XSS, SQL injection, CSRF)
- Prefer environment variables or SSM parameters for secrets
- Follow principle of least privilege
- Take privilege escalation into account
- IDOR prevention 
  - Always verify that the current user is authorized to access the resource 
  - Avoid predictable identifiers - use ksuids or UUIDs instead of sequential IDs 
  - Make sure users can only access what they absolutely need

**Code Organization**
- Single Responsibility Principle (one function/class, one purpose)
- DRY (Don't Repeat Yourself) - identify reusable components
- Separation of concerns (business logic, data access, presentation)
- Dependency injection over hard dependencies
- Prefer composition to inheritance
- Keep methods/ functions small and focused
  - consider breaking down functions longer than ~30 lines
  - aim for functions that do one thing well
- Consistent naming conventions
  - use descriptive names for functions
  - follow language specific conventions (camelCase, PascalCase, snake_case)
- Modular structure (feature-based or domain-driven design)
  - prefer interfaces and abstractions
- Keep classes and files focused on a single responsibility
- Comprehensive unit tests for new functionality
- Integration tests for critical paths
- End-to-end tests for user flows if applicable

**Performance Considerations**
- Identify potential bottlenecks (N+1 queries, unnecessary loops)
- Plan for caching strategies where appropriate
- Consider lazy loading for heavy resources
- Optimize database queries and API calls
- Plan for pagination of large datasets

**Error Handling Strategy**
- Comprehensive error handling at all levels
- User-friendly error messages
- Proper logging for debugging
- Graceful degradation where possible
- Consistent error response formats

### Documentation Requirements
Plan for:
- Inline comments for complex logic
- Function/method documentation
- API endpoint documentation
- README updates if adding new features
- Configuration documentation for new settings
- CLAUDE.md updates if architecture patterns change

### Primary Source: CLAUDE.md
First check for architecture patterns defined in CLAUDE.md. If present, these take precedence as they represent project-specific conventions.

### Fallback Architecture Guidelines (when no CLAUDE.md exists)
If CLAUDE.md is not found, analyze the existing codebase to identify patterns and follow these principles:

#### 1. Detect Technology Stack
- Examine package.json, requirements.txt, go.mod, Gemfile, etc.
- Identify framework-specific files (next.config.js, django settings.py, etc.)
- Check for configuration files that indicate tech choices (.eslintrc, tsconfig.json, etc.)

#### 2. Analyze Existing Patterns (REQUIRED)
Before planning, you MUST execute these analysis steps:

**Pattern Detection Commands:**
```bash
# Find class inheritance patterns
grep -r "class.*extends" --include="*.ts" --include="*.js" --include="*.java"

# Find constructor dependencies
grep -r "constructor(" --include="*.ts" --include="*.java"

# Identify test patterns
find . -name "*.test.*" -o -name "*.spec.*" | head -10

# Find build/lint commands
grep -E "build|compile|lint|test" package.json pom.xml build.gradle
```

**Document These Patterns:**
- **Directory structure**: Identify if using MVC, feature-based, or domain-driven organization
- **Naming conventions**: File naming (kebab-case, PascalCase), variable naming patterns
- **Import patterns**: How are dependencies imported (relative vs absolute paths)
- **Code style**: Indentation, bracket placement, import organization
- **Common patterns**: How are similar features currently implemented?
- **Test structure**: Location and naming of test files, testing frameworks used
- **Error handling**: How are errors typically handled (try-catch, error boundaries, etc.)

#### 3. Stack-Specific Conventions

**For React/Next.js projects:**
- Prefer functional components with hooks
- Use proper data fetching patterns (SSR, SSG, CSR as appropriate)
- Plan for proper state management (Context, Redux, Zustand based on existing usage)
- Follow React best practices for performance (memoization, code splitting)

**For Angular projects:**
- Follow Angular style guide (feature modules, barrel exports)
- Use proper dependency injection patterns
- Plan for RxJS usage (Observables, Subjects, proper unsubscription)
- Organize by feature with shared modules for common functionality
- Use Angular CLI conventions for file naming (component.ts, service.ts, module.ts)
- Implement proper change detection strategies (OnPush where appropriate)
- Plan for lazy loading of feature modules
- Use reactive forms for complex form handling
- Follow Angular's TypeScript conventions (interfaces, enums, types)
- Proper use of Angular lifecycle hooks
- Plan for proper error handling with interceptors

**For Node.js/Express projects:**
- Middleware organization and order
- Proper async/await error handling
- RESTful API conventions or GraphQL patterns
- Database connection pooling

**For Java/Spring Boot projects:**
- Follow package naming conventions (com.company.project.feature)
- Use proper layering (Controller, Service, Repository, Entity)
- Implement DTOs for API contracts, separate from entities
- Use dependency injection via constructor injection (not field injection)
- Follow Spring Boot conventions (@RestController, @Service, @Repository)
- Plan for proper transaction management (@Transactional)
- Use Spring's exception handling (@ControllerAdvice, @ExceptionHandler)
- Implement proper validation (@Valid, custom validators)
- Follow Java naming conventions (camelCase methods, PascalCase classes)
- Use Lombok annotations consistently if already in project
- Plan for proper logging with SLF4J
- Consider Spring Security integration for auth endpoints
- Use Spring Profiles for environment-specific configuration

**For Java (non-Spring) projects:**
- Follow standard Java project structure (src/main/java, src/test/java)
- Use appropriate design patterns (Builder, Factory, Singleton as needed)
- Implement interfaces for abstraction
- Follow SOLID principles rigorously
- Use Java 8+ features appropriately (Streams, Optional, lambdas)
- Plan for proper exception hierarchy
- Consider thread safety for concurrent operations
- Use appropriate collections (List vs Set vs Map)
- Follow Java coding conventions (Oracle/Google style guide)
- Plan for proper resource management (try-with-resources)

**For Python/Django/FastAPI projects:**
- Follow PEP 8 style guidelines
- Use type hints where the project already does
- Proper use of Django's ORM or SQLAlchemy patterns
- Appropriate use of decorators and middleware

**For Go projects:**
- Follow effective Go guidelines
- Proper error handling (return errors, don't panic)
- Interface-driven design
- Concurrent programming patterns where appropriate

**For Full-Stack Java/Angular projects:**
- Ensure consistent data models between backend DTOs and frontend interfaces
- Plan for proper API contract adherence
- Use consistent naming between Java REST endpoints and Angular services
- Plan for proper CORS configuration
- Consider code generation tools if already in use (OpenAPI, Swagger)
- Implement consistent error handling across stack
- Plan for consistent validation (backend + frontend)
- Use consistent date/time handling (Java LocalDateTime ↔ TypeScript Date)
- Plan for proper authentication flow (JWT tokens, session management)
- Consider build pipeline integration (Maven/Gradle with Angular CLI)

### Required Planning Output Structure
Your plan MUST include ALL of these sections:

#### 1. Prerequisites Check
- [ ] List all dependencies with exact versions
- [ ] Document all files to be modified with line numbers
- [ ] List new files to be created with full paths

#### 2. Implementation Steps
Provide numbered steps with specific details:
```
1. Create authentication handler at /src/handlers/authHandler.ts
   - Extends: BaseHandler (from /src/handlers/base.ts:15)
   - Imports: jwt from 'jsonwebtoken', User from '../types/user'
   - Methods: validateToken(), refreshToken(), logout()

2. Modify user service at /src/services/userService.ts:45-67
   - Add: authentication methods
   - Update: constructor to include AuthConfig dependency
```

#### 3. File Modifications Table
| File Path | Change Type | Line Numbers | Description |
|-----------|-------------|--------------|-------------|
| /src/handlers/authHandler.ts | Create | N/A | New authentication handler |
| /src/services/userService.ts | Edit | 45-67 | Add auth methods |
| /src/types/auth.d.ts | Create | N/A | Type definitions |
| package.json | Edit | 15 | Add jsonwebtoken dependency |

#### 4. Code Snippets
Include actual code for complex parts:
```typescript
// Example implementation pattern
async validateJWT(token: string): Promise<User> {
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    return await this.userService.findById(decoded.userId);
  } catch (error) {
    throw new UnauthorizedError('Invalid token');
  }
}
```

#### 5. Testing Checklist
- [ ] Unit tests for: validateJWT, refreshToken, logout
- [ ] Integration tests for: auth flow, token expiry
- [ ] Edge cases: expired tokens, malformed tokens, missing tokens
- [ ] Test file locations: /src/handlers/__tests__/authHandler.test.ts

#### 6. Rollback Plan
Step-by-step to undo if needed:
1. Remove /src/handlers/authHandler.ts
2. Revert /src/services/userService.ts to previous version
3. Remove auth types from /src/types/auth.d.ts
4. Remove jsonwebtoken from package.json and run npm install

## Workflow
1. First use `/brandifai:task` to create the task file
2. Optionally edit the task file to add more context
3. Use `/brandifai:task-plan` to generate the execution plan (PLANNING ONLY)
4. Finally use `/brandifai:task-exec` to execute the planned implementation

## Plan Completion Checklist
A plan is ready for execution when it includes:
- [ ] Exact file paths with line numbers for modifications
- [ ] Complete code snippets for complex logic
- [ ] Specific test cases to implement with file locations
- [ ] All required imports and dependencies with versions
- [ ] Database migration scripts (if applicable)
- [ ] Configuration changes needed (env vars, settings)
- [ ] Rollback instructions for each change
- [ ] Error handling strategy documented
- [ ] Performance considerations addressed
- [ ] Security implications reviewed

## Completion Criteria
The command is complete when:
- All items in the Plan Completion Checklist are addressed
- Detailed execution plan is documented in the task file using the structured template
- All implementation steps are broken down with specific file:line references
- Architecture decisions are documented with reasoning
- Task file is updated with comprehensive plan
- Claude explicitly states "Task planning complete - ready for execution phase"

## Complexity-Based Requirements

### Easy Tasks
- Focus on: File locations, method signatures, basic error handling
- Minimum plan sections: Prerequisites, Implementation Steps, File Modifications
- Test requirements: Basic unit tests

### Medium Tasks  
- Include: Dependency analysis, integration points, data flow, state management
- All plan sections required
- Test requirements: Unit tests + integration tests
- Use thinking mode for design decisions

### Hard Tasks
- Required: Architecture diagrams (ASCII or descriptions), sequence flows, security analysis
- Performance considerations mandatory
- Database schema changes must include migrations
- Test requirements: Unit + integration + performance tests
- Use thinking mode for thorough architectural analysis
- Consider scalability, maintainability, and technical debt