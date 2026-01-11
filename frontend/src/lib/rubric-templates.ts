export const RUBRIC_TEMPLATES = {
  standard: {
    name: "Standard Interview Assessment",
    content: `## Strategic Thinking
- Demonstrates long-term vision beyond immediate roadmap
- Makes decisions considering broader organizational impact
- Anticipates future challenges and opportunities
- Shows ability to connect current work to company strategy

## Leadership & Influence
- Influences without authority across teams and stakeholders
- Builds consensus among people with competing priorities
- Mentors and develops team members effectively
- Takes initiative and drives outcomes proactively

## Execution Excellence
- Delivers complex projects on time with high quality
- Manages dependencies and risks proactively
- Shows adaptability when priorities shift
- Demonstrates strong problem-solving and troubleshooting skills

## Communication & Collaboration
- Communicates clearly and concisely to various audiences
- Active listener who seeks to understand different perspectives
- Gives and receives constructive feedback well
- Builds strong working relationships across teams

## Technical/Domain Expertise
- Demonstrates deep knowledge in their area of focus
- Stays current with industry trends and best practices
- Makes sound technical/domain decisions with proper tradeoffs
- Can explain complex concepts to non-experts`,
  },

  technical: {
    name: "Technical Leadership",
    content: `## Technical Excellence
- Deep expertise in relevant technologies and systems
- Makes sound architectural decisions with proper tradeoffs
- Stays current with industry trends and emerging technologies
- Demonstrates strong debugging and problem-solving skills

## System Design & Architecture
- Designs scalable, maintainable, and reliable systems
- Considers performance, security, and operational implications
- Documents technical decisions and reasoning clearly
- Balances technical debt with feature development

## Code Quality & Best Practices
- Writes clean, well-tested, and maintainable code
- Follows established patterns and conventions
- Reviews code thoroughly and provides constructive feedback
- Champions engineering excellence and quality standards

## Technical Leadership
- Mentors engineers and raises the technical bar
- Influences technical direction and strategy
- Drives technical initiatives and improvements
- Collaborates effectively with cross-functional teams

## Project Execution
- Breaks down complex problems into manageable pieces
- Estimates accurately and delivers on commitments
- Manages technical risks and dependencies proactively
- Communicates progress and blockers effectively`,
  },

  product: {
    name: "Product Management",
    content: `## Product Strategy & Vision
- Develops compelling product vision aligned with business goals
- Identifies and prioritizes opportunities based on data and insights
- Makes strategic decisions about product direction and roadmap
- Balances short-term execution with long-term strategy

## User Understanding & Customer Focus
- Deeply understands user needs, pain points, and behaviors
- Uses data, research, and feedback to inform decisions
- Advocates for user experience and value delivery
- Validates assumptions through experimentation and testing

## Execution & Delivery
- Ships high-quality products on schedule
- Manages scope, resources, and tradeoffs effectively
- Drives alignment across engineering, design, and stakeholders
- Handles ambiguity and adapts to changing circumstances

## Cross-functional Leadership
- Builds strong relationships across teams and functions
- Influences without authority to drive outcomes
- Communicates product strategy and decisions clearly
- Facilitates productive discussions and resolves conflicts

## Business & Impact
- Understands business model and key metrics
- Defines success criteria and measures impact
- Makes data-driven decisions with proper context
- Demonstrates strong analytical and problem-solving skills`,
  },

  leadership: {
    name: "Management & Leadership",
    content: `## People Leadership
- Builds and develops high-performing teams
- Provides clear direction, feedback, and coaching
- Creates inclusive environment where team members thrive
- Handles performance issues constructively and promptly

## Strategic Thinking
- Sets clear team vision and goals aligned with company strategy
- Makes sound decisions considering long-term implications
- Identifies opportunities and risks proactively
- Balances competing priorities effectively

## Execution & Results
- Drives team to consistently deliver high-quality results
- Manages resources and timelines effectively
- Removes blockers and enables team success
- Holds self and team accountable to commitments

## Communication & Influence
- Communicates vision and strategy clearly to all levels
- Influences across the organization without direct authority
- Builds strong relationships with stakeholders and partners
- Represents team's work and accomplishments effectively

## Culture & Development
- Models company values and expected behaviors
- Invests in team growth and career development
- Fosters collaboration and knowledge sharing
- Builds organizational capability and bench strength`,
  },
};

export const DEFAULT_RUBRIC = RUBRIC_TEMPLATES.standard.content;

export type RubricTemplateKey = keyof typeof RUBRIC_TEMPLATES;
