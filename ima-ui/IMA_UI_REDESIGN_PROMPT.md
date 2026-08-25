# IMA UI — FULL AUDIT + REDESIGN

You are the lead frontend architect and product designer for IMA.

Do NOT blindly rewrite the application.

First understand the existing system completely:
- inspect every source file
- inspect package.json
- inspect Vite configuration
- inspect all React components
- inspect CSS
- inspect API clients
- inspect state
- inspect avatar/persona systems
- inspect experience/world systems
- inspect assets
- inspect existing routes/pages
- inspect every backend/API integration
- identify what is real and what is placeholder

PROJECT:
~/ima_kernel/ima-ui

KNOWN API:
POST http://127.0.0.1:8080/ask

## ABSOLUTE PRESERVATION RULE

Do NOT modify:
- ~/ima_kernel/.ima
- backend/kernel
- learning systems
- MEDA
- existing API contracts
- working authentication
- existing backend logic

unless a minimal UI-required API adaptation is genuinely necessary.

Never replace a real capability with mock functionality.

Never expose a capability in the UI merely because it sounds good.
Only expose capabilities that actually exist.

## PHASE 1 — COMPLETE AUDIT

Map the existing application:

1. Entry points
2. App shell
3. Components
4. Pages/routes
5. API calls
6. State management
7. Persona/identity
8. Avatar
9. 3D/world systems
10. Conversation system
11. Memory
12. Dashboard
13. CSS/design tokens
14. Assets
15. Dependencies

For every important component determine:

REAL / PARTIAL / PLACEHOLDER / DEAD

Find:
- duplicated functionality
- dead code
- unused components
- mock data
- fake capabilities
- broken imports
- inconsistent styling
- duplicated avatar systems
- duplicated conversation systems
- architectural conflicts

Do not delete anything before understanding its role.

## PHASE 2 — PRODUCT ARCHITECTURE

The target product is NOT a generic admin dashboard.

IMA should feel like:

ONE INTELLIGENCE
ONE PRESENCE
ONE CONTINUOUS CONTEXT

The interface should communicate:
- intelligence
- presence
- memory
- context
- action
- learning
- system state

without visual clutter.

## PHASE 3 — DESIGN SYSTEM

Create one coherent IMA visual language:

- premium
- futuristic
- minimal
- calm
- deep
- precise
- highly readable

Define consistently:
- typography
- spacing
- surfaces
- borders
- radius
- shadows
- hierarchy
- interaction states
- focus states
- transitions
- motion
- empty states
- loading states
- error states

Avoid generic SaaS-dashboard aesthetics.

## PHASE 4 — MAIN EXPERIENCE

The primary screen should revolve around IMA itself.

Core structure:

IMA PRESENCE
        ↓
MAIN INTELLIGENCE SURFACE
        ↓
CONTEXT / CAPABILITIES
        ↓
COMMAND INPUT

The conversation must remain the primary interaction.

Chat must support, where actually possible:
- rich messages
- markdown
- code
- copy
- retry
- loading
- error
- conversation history
- RTL/LTR mixed content
- keyboard navigation
- multiline input
- send
- stop/cancel if API supports it

## PHASE 5 — IMA PRESENCE

Use the existing avatar/persona systems if they are functional.

Do not create a second competing avatar architecture.

IMA should have clear states such as:

idle
thinking
working
responding
error
offline

These states should be represented visually without becoming distracting.

## PHASE 6 — CAPABILITIES

Expose only verified existing capabilities.

Potential categories:

Memory
Learning
Reasoning
Actions
System
Engines
Integrations

If a capability is not actually implemented:
DO NOT present it as active.

It may be represented as unavailable/planned only if that is useful.

## PHASE 7 — CONTEXT PANEL

Create a context/intelligence surface capable of showing actual information such as:

- current task
- active context
- active engine
- relevant memory
- current system state
- actions
- results

Do not fabricate data.

## PHASE 8 — NAVIGATION

Keep navigation minimal.

Possible structure:

IMA
Memory
Learning
Actions
System
Settings

But only create screens that have real functionality.

If functionality does not exist, do not build fake screens.

## PHASE 9 — RTL

Hebrew is first-class.

RTL must be architectural.

Correctly handle:
- Hebrew
- English
- mixed Hebrew/English
- code
- numbers
- technical identifiers
- punctuation
- chat messages

Do not solve RTL through scattered hacks.

Use logical CSS properties wherever possible.

## PHASE 10 — RESPONSIVE

Design mobile-first.

Explicitly handle:

mobile
tablet
desktop
ultrawide

Do not simply compress the desktop layout onto mobile.

## PHASE 11 — ACCESSIBILITY

Implement:
- keyboard navigation
- semantic structure
- visible focus
- aria labels where necessary
- sufficient contrast
- reduced motion
- usable touch targets

## PHASE 12 — MOTION

Motion should communicate state.

Use restrained motion for:
- appearance
- transitions
- thinking
- working
- system state
- panel transitions

No gratuitous animation.

Respect prefers-reduced-motion.

## PHASE 13 — CLEANUP

After understanding the architecture:

- remove genuinely dead code
- consolidate duplicate systems
- consolidate duplicate styling
- remove unused demo assets
- preserve functional systems
- preserve useful experimental systems unless clearly obsolete

Do not perform destructive cleanup blindly.

## PHASE 14 — VERIFICATION

Run:

npm run build

npm run lint

If tests exist, run them.

Fix all errors introduced by the redesign.

## FINAL DELIVERABLE

Produce:

1. complete audit
2. existing architecture map
3. capability map
4. design system
5. new application shell
6. redesigned intelligence/chat experience
7. IMA presence integration
8. context surface
9. responsive implementation
10. RTL implementation
11. accessibility
12. motion system
13. cleanup
14. build verification

Final principle:

EXISTING IMA CAPABILITIES
        ↓
ONE COHERENT INTELLIGENCE EXPERIENCE
        ↓
PREMIUM IMA INTERFACE

Do not build a beautiful dashboard that hides the intelligence.

Understand the existing code first.
Then redesign it.
