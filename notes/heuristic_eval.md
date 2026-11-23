# Heuristic Evaluation of SnakeRL

## Overview

**Why do a heuristic evaluation?** Before making claims like "SnakeRL did not
help participants to learn RL," the tool's usability needed to be evaluated,
so a heuristic evaluation was conducted.

**How to do a heuristic evaluation?** There is no explicit standard for
heuristic evaluations, but many projects take ideas from Jakob Nielsen's
10 Usability Heuristics for User Interface Design. His heuristics are broad
but still considered the standard, so this project will follow suit. Those
10 Heuristics inspired a spreadsheet of issues that were then used to
evaluate the  usability of SnakeRL.

<!-- Table of Heuristic Evaluation Resources -->
| Resource                      | Link                              |
| ----------------------------- | --------------------------------- |
| SnakeRL Evaluation            | [docs.google.com][snakerl_eval]   |
| Nielsen's Heuristics          | [nngroup.com][nielsen]            |
| Andy Budd's Heuristics        | [andybudd.com][andybudd]          |
| Sample Andy Budd Evaluation   | [classroom.itats.ac.id][oneview]  |
| Sample Nielsen Evaluation     | [scholar.umw.edu][gwengifts]      |
| Evaluation Template           | [myuxacademy.com][ux_academy]     |

<!-- nickname/URL mappings -->
[snakerl_eval]: https://docs.google.com/spreadsheets/d/1FxTUVJU_6q9ZqAWduvPMTkPCkN-7ChXdkKM33AlabE0/
[nielsen]: https://www.nngroup.com/articles/ten-usability-heuristics/
[gwengifts]: https://scholar.umw.edu/student_research/701/
[andybudd]: https://andybudd.com/archives/2007/01/heuristics_for_modern_web_application_de
[oneview]: https://classroom.itats.ac.id/storage/materi/412907240154/12-2024/1735521585_Heuristic_evaluation%20Andy%20Budd.pdf
[ux_academy]: https://myuxacademy.com/blog/heuristic-evaluation-template/

## Personal Notes on Nielsen's 10 Heuristics

**The Goal:** Make a product intuitive and reduce cognitve load.

**Relevance:** Some principles will be more relevant than others
depending on the interface type.

**Severity Scores:** Prioritizes what gets fixed first. Considers
frequency, impact, and persistence of issue.

| Score | Label         | Description                                                           |
| ----- | ------------- | --------------------------------------------------------------------- |
| 0     | Not a problem | Doesn't affect usability                                              |
| 1     | Cosmetic      | Minor issue, fix if time allows                                       |
| 2     | Minor         | Low priority, user can work around it                                 |
| 3     | Major         | Important to fix, will cause significant frustration or errors        |
| 4     | Catastrophe   | Must be fixed before release, blocks users or causes serious errors   |

**Nielsen's 10 Heuristic Principles:**
1. **Visibility of System Status:** ensure there is feedback. What is 
happening, navigation, and breadcrumb trails.
2. **Match between the System and the Real World:** make product intuitive.
Utilize terms, concepts, icons, and images that are familiar to your users.
3. **User Control and Freedom:** prevent unintentional actions. Add undo,
redo, and cancel menus.
4. **Consistency and Standards:** product should be consistent within itself
and consistent with other similar products.
5. **Error Prevention:** prevent invalid actions. Remove memory burdens,
support undo, and provide helpful constraints.
6. **Recgonition rather than Recall:** make elements visible. User may not
remember everything.
7. **Flexibility and Efficiency of Use:** meet needs of experienced and
inexperienced users alike. Provide shortcuts, personalization, and
customization.
8. **Aesthetic and Minimalist Design:** prioritize primary features.
Additional elements may be distracting.
9. **Help Users Recognize, Diagnose, and Recover from Errors:**
provide plain language error messages. Often use red text.
10. **Help and Documentation:** provide context to tasks.
Keep instructions concise. Help documentation should be easy to search.
Provide concrete steps.

## Personal Notes on Andy Budd's Heuristics

**What are these?** Based on Nielsen's 10 Heuristics. Adapted for modern
web design.

1. **Design for User Expectations:** provide useful features, match
common web conventions, and match functions with the real world.
2. **Clarity:** meaningful labels and icons, make for skim reading.
3. **Minimize Unnecessary Complexity and Cognitive Load:** remove
unnecessary functions and visual clutter, break up long processes
into steps.
4. **Efficiency and Task Completion:** optimize for the user, not the
system. Provide common defaults and multiple select, and quick links.
5. **Provide Users with Context:** sensible navigation with breadcrumb
trail, feedback, number steps in a process, clear site name.
6. **Consistency and Standards:** make site look and be used consistently,
use common conventions for naming and placement.
7. **Prevent Errors:** prevent irrelevant actions, provide help,
check for duplication.
8. **Help Users Notice, Understand, and Recover from Errors:** highlight
errors, provide feedback where error occurred, use plain language
9. **Promote a Pleasureable and Positive User Experience:** attractive
design with attainable goals and rewards for usage and progression
