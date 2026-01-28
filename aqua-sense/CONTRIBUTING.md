# Contributing to AquaSense

Thank you for your interest in contributing to AquaSense! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and follow our Code of Conduct.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
   ```bash
   git clone https://github.com/your-username/aqua-sense.git
   cd aqua-sense
   ```
3. **Create a branch** for your changes
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites
- Docker Desktop 24+
- Java 17+
- Node.js 18+
- Maven 3.9+

### Running Locally
```bash
# Start infrastructure
docker-compose up -d postgres redis kafka

# Start backend services
cd services
./mvnw clean install
./mvnw spring-boot:run -pl auth-service

# Start frontend
cd frontend
npm install
npm run dev
```

## Making Changes

### Code Style

#### Java
- Follow [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- Use Lombok for boilerplate code
- Write meaningful variable and method names
- Add JavaDoc comments for public APIs

#### TypeScript/React
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use functional components with hooks
- Use TypeScript for type safety
- Write meaningful component names

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): subject

body

footer
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(auth): add OAuth2 authentication

Implement OAuth2 authentication flow with support for:
- Google login
- GitHub login
- Microsoft Azure AD

Closes #123
```

### Testing

All new code should include tests:

#### Backend (Java)
```bash
# Run unit tests
mvn test

# Run integration tests
mvn verify -P integration-tests

# Check code coverage
mvn jacoco:report
```

#### Frontend (TypeScript)
```bash
# Run unit tests
npm test

# Run E2E tests
npm run test:e2e

# Check coverage
npm run test:coverage
```

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
   ```bash
   mvn clean verify
   npm test
   ```
4. **Update CHANGELOG.md** with your changes
5. **Create a Pull Request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots if UI changes
   - Test results

### Pull Request Review

- All PRs require at least one approval
- Address review comments promptly
- Keep PRs focused and reasonably sized
- Squash commits before merging

## Project Structure

```
aqua-sense/
├── services/          # Backend microservices (Java/Spring Boot)
├── frontend/          # React web application
├── infra/            # Infrastructure as Code (Terraform, K8s)
├── ci-cd/            # CI/CD pipelines
├── observability/    # Monitoring configurations
└── docs/             # Documentation
```

## Architecture Guidelines

### Microservices
- Each service should be independent and deployable
- Use REST APIs for synchronous communication
- Use Kafka for asynchronous communication
- Implement circuit breakers and retries
- Add comprehensive logging and metrics

### Database
- Use PostgreSQL for transactional data
- Use TimescaleDB for time-series data
- Use Redis for caching
- Implement database migrations with Flyway

### API Design
- Follow RESTful principles
- Use proper HTTP status codes
- Version APIs (e.g., `/api/v1/`)
- Document with OpenAPI/Swagger
- Implement pagination for lists
- Add rate limiting

### Security
- Never commit secrets or credentials
- Use environment variables for configuration
- Implement proper authentication and authorization
- Validate all inputs
- Use HTTPS in production
- Follow OWASP security guidelines

## Documentation

- Update README.md for significant changes
- Add API documentation for new endpoints
- Include architecture diagrams for new features
- Write clear code comments
- Update user guides if needed

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create a release branch
4. Tag the release
5. Deploy to staging
6. Run smoke tests
7. Deploy to production
8. Create GitHub release

## Need Help?

- Check existing issues and PRs
- Join our Slack channel: #aquasense-dev
- Email: dev@aquasense.io
- Read the [documentation](docs/)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to AquaSense! 🌊
