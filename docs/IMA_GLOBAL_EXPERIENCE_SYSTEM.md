# IMA Global Experience System

## Design thesis

**One global intelligence. One real relationship at a time.**

IMA must feel universal without feeling generic, personal without becoming fragmented, powerful without becoming opaque, and warm without becoming childish.

## Permanent design principles

1. **Purpose before decoration** — every surface exists to help a person accomplish or understand something.
2. **Agency** — people choose what IMA can remember, connect to, automate or share.
3. **Clarity** — the primary action and current state are obvious.
4. **Familiarity + flexibility** — use platform conventions while adapting to different people, devices, languages and abilities.
5. **Craft** — motion, typography, spacing, loading, errors and edge cases receive the same care as the hero screen.
6. **Human presence** — IMA communicates naturally and respectfully, with warmth proportional to the situation.
7. **Accessibility by default** — keyboard, screen reader, touch, voice, captions, contrast, reduced motion, reflow and assistive technology are first-class.
8. **Trust through visibility** — show sources, capability boundaries, permissions, memory state and action state when they matter.
9. **Private by default** — personal context belongs to the person; shared learning requires an explicit, governed promotion path.
10. **Global by architecture** — RTL/LTR, localization, time/date/number formats, low bandwidth and different cultural contexts are built into the system.
11. **One identity, many expressions** — interfaces and avatars may adapt, but IMA remains recognizably IMA.
12. **Evidence over claims** — planned, possible and verified capabilities must never be conflated.

## Experience layers

### 1. Welcome
The first screen answers:
- What is IMA?
- What can I do with her now?
- Why should I trust her?
- What happens to my information?
- How do I start?

### 2. Conversation
Conversation is the center of gravity. Everything else should support it rather than compete with it.

### 3. Personal context
The person can inspect and control:
- memory
- preferences
- accessibility
- connected services/devices
- language and communication style
- permissions
- personalization

### 4. Intelligence workspace
When a task needs research, tools, files, code, media or multiple models, IMA can expose the necessary workspace without making the underlying orchestration confusing.

### 5. Action
Before consequential external actions, IMA clearly communicates:
- what will happen
- where
- with which account/device
- what data will be shared
- whether money or an irreversible change is involved
- how to cancel/undo where possible

### 6. Learning
People can correct IMA and contribute knowledge. The interface distinguishes:
- personal correction
- temporary conversation context
- candidate shared learning
- verified shared learning

### 7. Recovery
Errors are part of the product. Every failure should explain:
- what failed
- what remains intact
- what the person can do next
- whether retrying is safe

## Universal-personal model

Global layer:
- identity
- verified shared knowledge
- safety and governance
- interoperability
- capabilities
- platform adapters

Personal layer:
- conversation
- private memory
- preferences
- permissions
- accessibility
- connected accounts/devices

Never merge these layers merely because data is technically available.

## Design review gate

For every meaningful UI or interaction change ask:

**Purpose:** Is the user's goal clearer?
**Agency:** Does the person remain in control?
**Clarity:** Can the next action be understood immediately?
**Accessibility:** Can people with different abilities use it?
**Globalization:** Does it work across languages, scripts and locales?
**Trust:** Are capability and data boundaries clear?
**Performance:** Is it responsive on ordinary/mobile/low-bandwidth hardware?
**Recovery:** What happens when the network, model, tool or device fails?
**Consistency:** Does it still feel like IMA across surfaces?
**Evidence:** Has the behavior actually been tested?

## Continuous improvement loop

OBSERVE → LISTEN → IDENTIFY FRICTION → PRIORITIZE → DESIGN → IMPLEMENT → TEST → ACCESSIBILITY CHECK → RUNTIME VERIFY → MEASURE → DOCUMENT → REPEAT

Use official platform guidance, standards, accessibility research, developer documentation, user feedback and observed failures as inputs. Learn from many products, but do not copy proprietary interfaces, assets or branding.

## Current external design inputs

The system should periodically review current guidance from Apple HIG/WWDC, Microsoft Fluent and accessibility guidance, Google Material/Android guidance, W3C/WCAG and other major platform/standards sources. New hardware and interaction paradigms should trigger a compatibility/design review.

## Quality bar

IMA should feel:
- calm rather than noisy
- capable rather than complicated
- personal rather than invasive
- global rather than generic
- modern rather than trend-dependent
- accessible rather than merely compliant
- trustworthy rather than overconfident

A beautiful screen that fails its interaction, accessibility, privacy or recovery behavior does not pass the IMA quality bar.
