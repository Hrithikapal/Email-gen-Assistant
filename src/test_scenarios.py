"""
Test Scenarios & Human Reference Emails
========================================
10 unique input scenarios (Intent, Key Facts, Tone) each paired with
a hand-written Human Reference Email (the ideal output).
"""

TEST_SCENARIOS = [
    # ------------------------------------------------------------------ #
    # Scenario 1                                                          #
    # ------------------------------------------------------------------ #
    {
        "id": 1,
        "intent": "Follow up after a job interview",
        "key_facts": [
            "Interview was on Monday at 11am for the Senior Product Manager role",
            "Discussed roadmap prioritisation and OKR alignment",
            "Interviewer's name is Sarah Chen",
            "Excited about the company's AI-driven product vision",
            "Available for next steps anytime this week",
        ],
        "tone": "Formal",
        "human_reference": """Subject: Thank You — Senior Product Manager Interview

Dear Sarah,

Thank you for taking the time to speak with me on Monday morning regarding the Senior Product Manager role. I genuinely enjoyed our conversation about roadmap prioritisation and OKR alignment, and I came away even more enthusiastic about the company's AI-driven product vision.

The discussion reinforced my belief that this role is an excellent match for both my experience and my professional goals. I am available for any next steps at your convenience this week and would welcome the opportunity to continue the conversation.

Thank you again for your time and consideration.

Best regards,
[Your Name]""",
    },
    # ------------------------------------------------------------------ #
    # Scenario 2                                                          #
    # ------------------------------------------------------------------ #
    {
        "id": 2,
        "intent": "Request a client for outstanding invoice payment",
        "key_facts": [
            "Invoice number INV-2024-089",
            "Amount due: $12,500",
            "Original due date was October 1st",
            "Payment is now 30 days overdue",
            "Please pay via bank transfer to the details on the invoice",
            "Contact billing@company.com for any queries",
        ],
        "tone": "Formal",
        "human_reference": """Subject: Reminder: Invoice INV-2024-089 — Payment Now 30 Days Overdue

Dear [Client Name],

I am writing to bring to your attention that Invoice INV-2024-089, totalling $12,500, remains outstanding. The payment was originally due on October 1st and is now 30 days overdue.

We kindly request that you arrange settlement at your earliest convenience via bank transfer using the details provided on the invoice. Should you have any questions or require clarification, please do not hesitate to contact our billing team at billing@company.com.

We value our business relationship and appreciate your prompt attention to this matter.

Yours sincerely,
[Your Name]""",
    },
    # ------------------------------------------------------------------ #
    # Scenario 3                                                          #
    # ------------------------------------------------------------------ #
    {
        "id": 3,
        "intent": "Announce a new company policy on remote work",
        "key_facts": [
            "New policy: employees must be in office Tuesdays and Thursdays",
            "Effective date: January 6th",
            "Hot-desking system will be implemented",
            "Exceptions require manager approval",
            "Full policy document available on the intranet",
        ],
        "tone": "Formal",
        "human_reference": """Subject: Updated Remote Work Policy — Effective January 6th

Dear Team,

I am writing to inform you of an important update to our remote work policy, effective January 6th.

Going forward, all employees are required to work from the office on Tuesdays and Thursdays each week. To support this, a hot-desking system will be implemented across all office floors. Employees who require an exception to this arrangement must obtain prior approval from their line manager.

The full policy document, including detailed guidance on the hot-desking system and the exceptions process, is available on the company intranet.

Thank you for your understanding and cooperation as we continue to evolve our ways of working.

Best regards,
[Your Name]""",
    },
    # ------------------------------------------------------------------ #
    # Scenario 4                                                          #
    # ------------------------------------------------------------------ #
    {
        "id": 4,
        "intent": "Invite a colleague to collaborate on a research paper",
        "key_facts": [
            "Topic: generative AI in healthcare diagnostics",
            "Target journal: Nature Digital Medicine",
            "Submission deadline: March 31st",
            "Looking for co-author to contribute the clinical trials section",
            "First draft meeting proposed for next Tuesday at 3pm",
        ],
        "tone": "Casual",
        "human_reference": """Subject: Collaboration on AI in Healthcare Paper — Interested?

Hey [Colleague's Name],

Hope you're doing well! I'm working on a research paper about generative AI in healthcare diagnostics and I'd love to have you on board as a co-author.

The plan is to submit to Nature Digital Medicine by March 31st. I'm looking for someone to take the lead on the clinical trials section — and given your background, you'd be perfect for it.

Would you be up for a first draft meeting next Tuesday at 3pm to kick things off and align on scope? Let me know what you think!

Cheers,
[Your Name]""",
    },
    # ------------------------------------------------------------------ #
    # Scenario 5                                                          #
    # ------------------------------------------------------------------ #
    {
        "id": 5,
        "intent": "Alert the operations team of a critical server outage",
        "key_facts": [
            "Production database server DB-PROD-03 is down",
            "Outage started at 14:22 UTC",
            "All read and write operations are failing",
            "On-call engineer Raj Patel has been paged",
            "Estimated recovery time: 90 minutes",
            "Use the read replica DB-READ-01 as an interim workaround",
        ],
        "tone": "Urgent",
        "human_reference": """Subject: CRITICAL: DB-PROD-03 Down — Immediate Action Required

Team,

URGENT: Production database server DB-PROD-03 has been down since 14:22 UTC. All read and write operations are currently failing, impacting live services.

On-call engineer Raj Patel has been paged and is actively investigating. Estimated recovery time is 90 minutes.

IMMEDIATE WORKAROUND: Please redirect all database traffic to the read replica DB-READ-01 until further notice.

Updates will follow every 30 minutes. Please escalate immediately if additional support is required.

[Your Name]""",
    },
    # ------------------------------------------------------------------ #
    # Scenario 6                                                          #
    # ------------------------------------------------------------------ #
    {
        "id": 6,
        "intent": "Request a software vendor for a product demo",
        "key_facts": [
            "Vendor: DataSync Pro",
            "Interested in the Enterprise Analytics Suite",
            "Team size: 25 users",
            "Want to see real-time dashboard and data integration features",
            "Preferred demo slot: any morning next week",
        ],
        "tone": "Formal",
        "human_reference": """Subject: Demo Request — Enterprise Analytics Suite

Dear DataSync Pro Team,

I am writing on behalf of our organisation to request a product demonstration of your Enterprise Analytics Suite.

We have a team of 25 users and are particularly interested in exploring the real-time dashboard capabilities and data integration features. We believe these may address several of our current operational needs.

Would it be possible to schedule a demonstration during any morning slot next week? Please let us know your availability and we will confirm a time that works for both parties.

We look forward to hearing from you.

Kind regards,
[Your Name]""",
    },
    # ------------------------------------------------------------------ #
    # Scenario 7                                                          #
    # ------------------------------------------------------------------ #
    {
        "id": 7,
        "intent": "Apologise to a customer for a delayed shipment",
        "key_facts": [
            "Order number: ORD-78432",
            "Original delivery estimate: November 10th",
            "New estimated delivery: November 18th",
            "Delay caused by severe weather disrupting logistics",
            "Offering 20% discount on next order as compensation",
            "Tracking link will be sent separately",
        ],
        "tone": "Empathetic",
        "human_reference": """Subject: Apology & Update: Your Order ORD-78432

Dear [Customer Name],

I sincerely apologise for the delay with your order ORD-78432. We completely understand how frustrating this must be, and I want to be transparent about what happened.

Severe weather conditions have disrupted our logistics network, pushing your estimated delivery from November 10th to November 18th. We know this is not the experience you expected, and we are truly sorry for the inconvenience.

As a token of our appreciation for your patience, we would like to offer you a 20% discount on your next order. You will receive a separate email with your tracking link so you can monitor the updated delivery.

Thank you for your understanding, and please do not hesitate to reach out if there is anything else we can do to help.

Warm regards,
[Your Name]""",
    },
    # ------------------------------------------------------------------ #
    # Scenario 8                                                          #
    # ------------------------------------------------------------------ #
    {
        "id": 8,
        "intent": "Pitch a partnership proposal to another company",
        "key_facts": [
            "Our company: BrightPath Analytics",
            "Their company: GreenLeaf Marketing",
            "Proposed: co-develop a customer segmentation tool",
            "Our contribution: data science expertise and platform",
            "Their contribution: marketing domain knowledge and client network",
            "Potential first client: RetailCo (500K users)",
            "Request a 30-minute exploratory call",
        ],
        "tone": "Formal",
        "human_reference": """Subject: Partnership Proposal — Customer Segmentation Tool

Dear GreenLeaf Marketing Team,

My name is [Your Name] from BrightPath Analytics, and I am reaching out to explore a potential collaboration that I believe could be mutually beneficial.

We propose co-developing a customer segmentation tool that combines BrightPath's data science expertise and platform infrastructure with GreenLeaf's deep marketing domain knowledge and established client network. Together, we see strong potential to deliver exceptional value — with RetailCo and its 500,000-strong user base already identified as a compelling first opportunity.

I would be delighted to schedule a 30-minute exploratory call at your convenience to discuss this in more detail. Please let me know a time that works for you.

I look forward to the possibility of building something great together.

Yours sincerely,
[Your Name]
BrightPath Analytics""",
    },
    # ------------------------------------------------------------------ #
    # Scenario 9                                                          #
    # ------------------------------------------------------------------ #
    {
        "id": 9,
        "intent": "Ask a manager for a performance review meeting",
        "key_facts": [
            "Has been in the role for 12 months",
            "Wants to discuss career progression to Senior Engineer",
            "Completed 3 major projects this year",
            "Interested in the upcoming ML infrastructure initiative",
            "Available any day this week after 2pm",
        ],
        "tone": "Formal",
        "human_reference": """Subject: Request for Performance Review Meeting

Dear [Manager's Name],

I hope you are well. Now that I have completed 12 months in my current role, I would like to request a performance review meeting at your earliest convenience.

Over the past year I have successfully delivered three major projects and I am keen to discuss my progress and explore the path towards a Senior Engineer position. I am also very interested in contributing to the upcoming ML infrastructure initiative and would welcome the opportunity to discuss how I can get involved.

I am available any day this week after 2pm — please let me know what suits you best.

Thank you for your time and support.

Best regards,
[Your Name]""",
    },
    # ------------------------------------------------------------------ #
    # Scenario 10                                                         #
    # ------------------------------------------------------------------ #
    {
        "id": 10,
        "intent": "Congratulate a team member on a promotion",
        "key_facts": [
            "Team member's name: Priya Sharma",
            "Promoted to Head of Design",
            "Has been with the company for 5 years",
            "Led the award-winning rebrand project last year",
            "New role starts December 1st",
        ],
        "tone": "Casual",
        "human_reference": """Subject: Huge Congratulations, Priya!

Hi Priya,

Wow — Head of Design! Congratulations! This is so well deserved.

Five years of incredible work, and what a way to top it off after leading that award-winning rebrand last year. You've made a huge impact on this team and it's fantastic to see it recognised in such a big way.

I can't wait to see everything you'll do in the new role starting December 1st. Here's to the next chapter!

Warmly,
[Your Name]""",
    },
]


if __name__ == "__main__":
    print(f"Loaded {len(TEST_SCENARIOS)} test scenarios.\n")
    for s in TEST_SCENARIOS:
        print(f"Scenario {s['id']}: [{s['tone']}] {s['intent']}")
