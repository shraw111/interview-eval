"""
Hardcoded evaluation rubric for case study presentations.
This rubric is used for all evaluations and is not user-configurable.
"""

import json

# Hardcoded rubric as JSON string
EVALUATION_RUBRIC_JSON = json.dumps({
    "evaluation_rubric": {
        "name": "Case Study Presentation Evaluation",
        "description": "Evaluation rubric for case study presentations based on presentation quality, structure, storytelling, case study depth, and prototype creation",
        "scoring_scale": {
            "min": 1,
            "max": 5,
            "description": "5-point scale where 1-2 = Poor/Below standard, 3 = Adequate/Current level, 4 = Target level/Strong, 5 = Exceptional/Mastery"
        },
        "categories": [
            {
                "id": "presentation",
                "name": "Overall Presentation Quality",
                "weight": 10,
                "criteria": [
                    {
                        "id": "attr_1",
                        "name": "Overall Presentation Quality",
                        "description": "Evaluates verbal delivery, pacing, command, and stakeholder engagement",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "Verbal delivery is disorganized or hesitant. Frequent filler words or poor pacing make it difficult to grasp the core logic or intent."},
                            {"score": 2, "description": "Verbal delivery is disorganized or hesitant. Frequent filler words or poor pacing make it difficult to grasp the core logic or intent."},
                            {"score": 3, "description": "Professional and clear articulation. The delivery is adequate for a standard report but lacks the persuasive energy or 'ownership' needed to drive a business decision at the Target Level."},
                            {"score": 4, "description": "Demonstrates Command and Pacing. The delivery is engaging and reflects a strong mental grasp of the subject. The candidate handles questions smoothly and uses emphasis to highlight strategic intent, showing they are ready for client-facing or senior stakeholder discussions."},
                            {"score": 5, "description": "Exceptional presence. Sets a new standard for clarity and persuasion, using rhetorical skill to create deep alignment and stakeholder buy-in."}
                        ]
                    }
                ]
            },
            {
                "id": "structure",
                "name": "Presentation Structure",
                "weight": 10,
                "criteria": [
                    {
                        "id": "attr_2",
                        "name": "Presentation Structure",
                        "description": "Evaluates logical flow, strategic continuity, and framework usage",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "Verbal explanation feels fragmented or disconnected. There is no clear logical sequence, making it difficult for the listener to follow the core argument."},
                            {"score": 2, "description": "Verbal explanation feels fragmented or disconnected. There is no clear logical sequence, making it difficult for the listener to follow the core argument."},
                            {"score": 3, "description": "Follows a predictable, standard sequence (Introduction → Analysis → Conclusion). Frameworks are mentioned but serve more as labels than as the logical engine driving the argument."},
                            {"score": 4, "description": "Demonstrates Strategic Continuity. The candidate maintains a clear 'verbal thread' that logically connects the problem to the solution. They use structured thinking to explain why their data leads to their specific conclusions, ensuring the listener understands the strategic 'bridge' between sections."},
                            {"score": 5, "description": "Masterful structure where complex ideas are synthesized flawlessly. The candidate adapts logic to the situation, providing deep clarity that sets an internal standard for strategic communication."}
                        ]
                    }
                ]
            },
            {
                "id": "storytelling",
                "name": "Storytelling Skills",
                "weight": 20,
                "criteria": [
                    {
                        "id": "attr_3",
                        "name": "Storytelling Skills",
                        "description": "Evaluates narrative flow, business context, and persuasive impact",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "The narrative is fragmented or purely reactive. The candidate fails to explain the 'why' behind the project, making the transition from problem to solution feel abrupt or illogical."},
                            {"score": 2, "description": "The narrative is fragmented or purely reactive. The candidate fails to explain the 'why' behind the project, making the transition from problem to solution feel abrupt or illogical."},
                            {"score": 3, "description": "Provides a clear sequence with a beginning, middle, and end. The delivery is factual and accurate but lacks the engagement or persuasive 'hook' required to inspire confidence at the Target Level."},
                            {"score": 4, "description": "Demonstrates Purposeful Narrative. The candidate connects the problem to the solution in a way that makes the business impact clear. They move beyond 'reporting activities' to build a persuasive case for the proposed solution."},
                            {"score": 5, "description": "Masterful storytelling that uses business context to create a deep sense of urgency. The narrative drives total stakeholder buy-in by making the solution feel both inevitable and essential."}
                        ]
                    }
                ]
            },
            {
                "id": "case_study",
                "name": "Case Study",
                "weight": 60,
                "description": "10 sub-attributes with equal weight (6% each)",
                "criteria": [
                    {
                        "id": "attr_4a",
                        "name": "Problem Statement",
                        "description": "Evaluates clarity of problem definition and root cause identification",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "Explanation is vague or circular. It remains unclear what specific user pain point or business friction is being solved."},
                            {"score": 2, "description": "Explanation is vague or circular. It remains unclear what specific user pain point or business friction is being solved."},
                            {"score": 3, "description": "Identifies the core issue logically but focuses on the symptoms rather than the root cause. It is a competent summary but lacks strategic precision."},
                            {"score": 4, "description": "Clearly defines Root Cause and Impact. The candidate explains not just what the problem is, but why it matters to the business, making the solution feel necessary."},
                            {"score": 5, "description": "Articulates a non-obvious or multifaceted problem that others might overlook, providing unique strategic clarity."}
                        ]
                    },
                    {
                        "id": "attr_4b",
                        "name": "Opportunity Sizing",
                        "description": "Evaluates quantification of market opportunity and business value",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "Purely qualitative claims (e.g., 'this is a big market') without any mention of scale, data, or impact."},
                            {"score": 2, "description": "Purely qualitative claims (e.g., 'this is a big market') without any mention of scale, data, or impact."},
                            {"score": 3, "description": "Mentions broad industry stats or general market size but fails to narrow it down to the specific opportunity for their solution."},
                            {"score": 4, "description": "Explains Logical Scale. Instead of a rigid dollar amount, the candidate walks the listener through the logic of the value (e.g., volume of users impacted, time saved, or cost avoided)."},
                            {"score": 5, "description": "Describes a sophisticated business case with clear assumptions and impact drivers, demonstrating mastery of business value."}
                        ]
                    },
                    {
                        "id": "attr_4c",
                        "name": "Depth of Research",
                        "description": "Evaluates thoroughness of user, market, and technical research",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "Findings are superficial or based on general assumptions without specific data points or insights."},
                            {"score": 2, "description": "Findings are superficial or based on general assumptions without specific data points or insights."},
                            {"score": 3, "description": "Research covers some perspectives but lacks a balanced view across the user, market, and technical feasibility."},
                            {"score": 4, "description": "Demonstrates Holistic Discovery. Verbally shows they looked at the problem from three sides: what the user needs, what the business goals are, and what the technical capabilities allow."},
                            {"score": 5, "description": "Exceptional evidence of primary research or deep competitive intelligence that provides a distinct strategic advantage."}
                        ]
                    },
                    {
                        "id": "attr_4d",
                        "name": "Current Business Model Definition",
                        "description": "Evaluates understanding of existing operational model and inefficiencies",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "Vague or confusing description of how things work today; the starting point is unclear."},
                            {"score": 2, "description": "Vague or confusing description of how things work today; the starting point is unclear."},
                            {"score": 3, "description": "Articulates the existing model accurately but misses the nuances of where the inefficiencies truly lie."},
                            {"score": 4, "description": "Provides a Clear Operational Map. The candidate demonstrates a thorough understanding of the current workflow and can pinpoint exactly where the system is breaking down."},
                            {"score": 5, "description": "Identifies hidden complexities or legacy constraints that others would miss, showing mastery of business architecture."}
                        ]
                    },
                    {
                        "id": "attr_4e",
                        "name": "Business Analysis",
                        "description": "Evaluates depth of analysis on business challenges and gaps",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "Weak analysis; identifies symptoms but fails to articulate actual business challenges or gaps."},
                            {"score": 2, "description": "Weak analysis; identifies symptoms but fails to articulate actual business challenges or gaps."},
                            {"score": 3, "description": "Identifies standard challenges. Logic is sound for their current role but stays on the surface of the problem."},
                            {"score": 4, "description": "Performs a Deep-Dive Analysis. Clearly identifies structural gaps and multifaceted challenges that the proposed solution must resolve."},
                            {"score": 5, "description": "Identifies non-obvious strategic gaps or market shifts, providing a compelling case for transformation."}
                        ]
                    },
                    {
                        "id": "attr_4f",
                        "name": "Target Business Model Alternatives",
                        "description": "Evaluates exploration of alternative solutions and strategic options",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "Proposes only one path, showing a lack of creative exploration or 'Plan B' thinking."},
                            {"score": 2, "description": "Proposes only one path, showing a lack of creative exploration or 'Plan B' thinking."},
                            {"score": 3, "description": "Mentions other ideas, but doesn't develop them into viable options or explain why they were discarded."},
                            {"score": 4, "description": "Demonstrates Strategic Options. Verbally articulates at least two distinct and viable ways the problem could have been solved, showing business acumen in the selection process."},
                            {"score": 5, "description": "Proposes radically innovative alternatives that challenge industry norms."}
                        ]
                    },
                    {
                        "id": "attr_4g",
                        "name": "Criteria for Selection",
                        "description": "Evaluates decision-making framework and trade-off analysis",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "Choice of solution feels arbitrary; fails to explain why one path was chosen over others."},
                            {"score": 2, "description": "Choice of solution feels arbitrary; fails to explain why one path was chosen over others."},
                            {"score": 3, "description": "Mentions reasons for the choice, but the decision-making feels informal rather than structured."},
                            {"score": 4, "description": "Uses a Logical Trade-off Framework. Justifies the chosen solution using objective criteria (e.g., cost vs. impact, speed to market vs. scalability)."},
                            {"score": 5, "description": "Sophisticated multi-criteria decision-making that accounts for long-term risks and global scalability."}
                        ]
                    },
                    {
                        "id": "attr_4h",
                        "name": "GTM Approach",
                        "description": "Evaluates go-to-market strategy and launch planning",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "Generic list of channels with no clear strategy or target audience."},
                            {"score": 2, "description": "Generic list of channels with no clear strategy or target audience."},
                            {"score": 3, "description": "Standard rollout plan. Clear, but lacks a tailored value proposition for the specific target business."},
                            {"score": 4, "description": "Practical Launch Strategy. Defines who the first users are, why they will care, and how the product will reach them in a logical, phased manner."},
                            {"score": 5, "description": "Detailed strategy including growth loops, partnership models, or innovative acquisition tactics."}
                        ]
                    },
                    {
                        "id": "attr_4i",
                        "name": "Vision & Roadmap",
                        "description": "Evaluates product vision and phased execution plan",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "Simple list of features with no overarching vision or user-centric logic."},
                            {"score": 2, "description": "Simple list of features with no overarching vision or user-centric logic."},
                            {"score": 3, "description": "Breaks the model into an MVP and features, but lacks a deep connection to user needs or long-term sustainability."},
                            {"score": 4, "description": "Articulates Phased Value. Shows a clear product vision and explains how the roadmap balances user desirability with business feasibility."},
                            {"score": 5, "description": "Visionary yet practical roadmap that balances immediate execution with long-term innovation."}
                        ]
                    },
                    {
                        "id": "attr_4j",
                        "name": "Implementation Plan",
                        "description": "Evaluates execution planning, timelines, and team structure",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "Vague plan; missing timelines or a clear sense of how the work gets done."},
                            {"score": 2, "description": "Vague plan; missing timelines or a clear sense of how the work gets done."},
                            {"score": 3, "description": "Basic timeline provided. Clear, but lacks detail on team roles or specific delivery methods."},
                            {"score": 4, "description": "Shows Execution Readiness. Details clear timelines and the necessary team structure (e.g., 'I need 2 devs and 1 designer') to bring the solution to life."},
                            {"score": 5, "description": "Comprehensive plan referencing Agile or SAFe methodologies to manage complex dependencies."}
                        ]
                    }
                ]
            },
            {
                "id": "prototype",
                "name": "Prototype Creation",
                "weight": 0,
                "description": "Prototype quality evaluation (0% weight)",
                "criteria": [
                    {
                        "id": "attr_5",
                        "name": "Prototype Creation",
                        "description": "Evaluates prototype structure, user flow, and functional connectivity",
                        "is_critical": False,
                        "scoring_levels": [
                            {"score": 1, "description": "No detail on structure or tools; fails to mention specific pages or features."},
                            {"score": 2, "description": "No detail on structure or tools; fails to mention specific pages or features."},
                            {"score": 3, "description": "Confirms a working prototype exists. Focuses on the 'front-end' visuals (screens/buttons) using generic language."},
                            {"score": 4, "description": "Articulates Functional Connectivity. Explains the user flow (how they move through the app) and the data logic (how the app gets its information). Instead of requiring 'REST API,' they explain how systems talk to each other to make the feature work."},
                            {"score": 5, "description": "Describes a sophisticated prototype accounting for complex journeys and third-party integrations, showing 'operational readiness.'"}
                        ]
                    }
                ]
            }
        ],
        "decision_rules": {
            "weighted_calculation": True,
            "weights_definition": "Category weights: Presentation 10%, Structure 10%, Storytelling 20%, Case Study 60% (10 sub-attributes at 6% each), Prototype 0%",
            "critical_criteria": [],
            "scoring_note": "Score 3 represents current level competence, Score 4 represents target level readiness"
        }
    }
}, indent=2)
