# MindCare AI - Comprehensive Mental Wellness Knowledge Base Library
# Curated resources across Cognitive Behavioral Therapy, Anxiety Management, 
# Depression Support, Mindfulness, Sleep Hygiene, Burnout Prevention, and Grounding.

import json
import os

KNOWLEDGE_DOCUMENTS = [
    {
        "id": "kb_cbt_001",
        "title": "Cognitive Restructuring and Identifying Cognitive Distortions",
        "category": "Cognitive Behavioral Therapy",
        "author": "MindCare Clinical Education Team",
        "organization": "MindCare Mental Wellness Research",
        "publication_date": "2024-01-15",
        "source_url": "https://mindcare.ai/resources/cbt-cognitive-restructuring",
        "licensing": "Educational Open Access",
        "content": """Cognitive restructuring is a core therapeutic technique in Cognitive Behavioral Therapy (CBT) that helps individuals recognize, challenge, and modify maladaptive or irrational thoughts known as cognitive distortions.

Key Common Cognitive Distortions:
1. All-or-Nothing Thinking (Black-and-White Thinking): Viewing situations in extreme terms with no middle ground. For example, 'If I am not perfect, I have completely failed.'
2. Catastrophizing: Assuming the absolute worst-case scenario will occur, magnifying negative outcomes while minimizing positive coping capacity.
3. Mind Reading: Believing you know what others are thinking about you without sufficient evidence, usually assuming negative judgment.
4. Emotional Reasoning: Believing that because you feel something strongly, it must be an objective truth (e.g., 'I feel anxious, therefore something terrible is bound to happen').
5. Should and Must Statements: Imposing rigid behavioral rules upon oneself or others, which leads to chronic guilt, frustration, and resentment.
6. Overgeneralization: Viewing a single negative event as an ongoing, never-ending pattern of defeat (e.g., 'I stumbled on this presentation; I will always fail in public speaking').
7. Mental Filtering: Focusing exclusively on a single negative detail while completely disregarding positive or neutral evidence.

Step-by-Step Cognitive Restructuring Exercise:
Step 1: Identify the Triggering Event: Note the exact situation or event that precipitated feelings of emotional distress.
Step 2: Catch the Automatic Negative Thought (ANT): Record the immediate thought that flashed through your mind. Rate your belief in this thought from 0% to 100%.
Step 3: Identify the Distortions: Match the thought against known distortion categories.
Step 4: Examine the Evidence: Create two columns: 'Evidence Supporting the Thought' and 'Evidence Contradicting the Thought'. Stick strictly to verifiable facts, not emotional impressions.
Step 5: Generate a Balanced Alternative Thought: Formulate a rational, nuanced perspective that integrates both perspectives.
Step 6: Re-rate Emotional Intensity: Measure emotional distress before and after balanced thought generation to track subjective relief."""
    },
    {
        "id": "kb_anx_002",
        "title": "Somatic Grounding and the 5-4-3-2-1 Coping Technique for Acute Anxiety",
        "category": "Anxiety and Panic Management",
        "author": "Dr. Elena Vance, PsyD",
        "organization": "National Anxiety & Stress Institute",
        "publication_date": "2023-11-20",
        "source_url": "https://mindcare.ai/resources/54321-grounding-anxiety",
        "licensing": "Creative Commons Attribution 4.0",
        "content": """Somatic grounding techniques assist individuals during periods of severe anxiety, panic attacks, dissociation, and hyperarousal by redirecting neural focus from internal autonomic alarm pathways to external sensory reality.

The 5-4-3-2-1 Sensory Grounding Method:
This sensory orientation sequence engages five sensory modalities sequentially to activate the parasympathetic nervous system and downregulate the amygdala's fight-flight-freeze response:

1. Look for 5 Things You Can See:
Scan the room and name five distinct items (e.g., the pattern on a wooden desk, sunlight hitting the curtain, a blue pen, books on a shelf, a reflection in glass). Pay attention to colors, shapes, and textures.

2. Acknowledge 4 Things You Can Physically Feel:
Notice tactile sensation: the contact of your feet against the floor, the texture of fabric against your skin, the cool surface of a tabletop, or the weight of a watch on your wrist.

3. Listen for 3 Things You Can Hear:
Tune into ambient background audio: distant traffic, the hum of an air conditioner or fan, bird calls outside, or the rhythmic sound of your own inhalation and exhalation.

4. Identify 2 Things You Can Smell:
Notice environmental scents: coffee, fresh air, hand lotion, paper, or clothing detergent. If no scent is noticeable, visualize an enjoyable soothing aroma like lavender or pine.

5. Notice 1 Thing You Can Taste:
Acknowledge the taste inside your mouth, take a mindful sip of cool water, or chew a mint or piece of gum. Focus on the physical temperature and tongue sensations.

Physiological Mechanism:
Engaging the prefrontal cortex in deliberate sensory cataloging inhibits autonomic sympathetic nervous system hyperarousal, lowering heart rate and normalizing respiratory rate."""
    },
    {
        "id": "kb_brn_003",
        "title": "Burnout Prevention, Chronic Stress Physiology, and Work-Life Boundary Architecture",
        "category": "Stress and Burnout",
        "author": "Marcus Sterling, MSc",
        "organization": "Occupational Health & Wellness Collaborative",
        "publication_date": "2024-02-10",
        "source_url": "https://mindcare.ai/resources/burnout-boundary-architecture",
        "licensing": "Educational Open Access",
        "content": """Burnout is defined by the World Health Organization (WHO) as an occupational phenomenon resulting from chronic workplace stress that has not been successfully managed. It is characterized by three core dimensions: emotional exhaustion, depersonalization/cynicism, and a reduced sense of personal accomplishment.

Pathophysiology of Chronic Workplace Stress:
Prolonged elevation of cortisol and catecholamines dysregulates the hypothalamic-pituitary-adrenal (HPA) axis, resulting in executive function impairments, chronic fatigue, sleep fragmentation, impaired immune function, and irritability.

Three-Tiered Burnout Intervention Strategy:
1. Micro-Restoration Breaks (Ultradian Rhythm Care):
The human brain functions in 90- to 120-minute ultradian cycles. Continuous screen work beyond this window causes cognitive fatigue. Introduce 5-minute cognitive detours every 90 minutes: stand up, gaze at a distant horizon (allowing ocular relaxation), drink water, and practice paced diaphragmatic breathing.

2. Cognitive Boundary Management:
- Implement a defined 'Digital Sunset': cease checking professional email and work communications at least 60-90 minutes before bedtime.
- Segment physical workspace from relaxation space when working remotely.
- Practice polite assertiveness: replace unconditional acquiescence with capacity-based commitments ('I can take this project on by Tuesday if we reprioritize the secondary report').

3. Meaning and Values Realignment:
Distinguish between instrumental tasks and value-aligned endeavors. Dedicate time each week to activities with intrinsic reward, completely detached from productivity metrics (creative pursuits, physical movement, connection with nature)."""
    },
    {
        "id": "kb_slp_004",
        "title": "Evidence-Based Sleep Hygiene and Circadian Rhythm Optimization",
        "category": "Sleep and Circadian Health",
        "author": "Dr. Sarah Jenkins, MD, Sleep Specialist",
        "organization": "Sleep Medicine and Circadian Biology Center",
        "publication_date": "2023-09-12",
        "source_url": "https://mindcare.ai/resources/sleep-hygiene-circadian-health",
        "licensing": "Public Health Domain",
        "content": """Sleep is the foundational pillar of emotional resilience, neurochemical balance, and cognitive synthesis. Insomnia and irregular sleep architecture disproportionately exacerbate depressive and anxiety symptoms.

Foundational Sleep Hygiene Rules:
1. Circadian Anchoring via Consistent Wake Times:
Wake up at the identical time seven days a week, regardless of duration of sleep the night before. This anchors the central circadian pacemaker in the suprachiasmatic nucleus (SCN).

2. Morning Light Exposure:
Expose eyes to bright natural sunlight within 30-60 minutes of waking for 10-20 minutes. Sunlight triggers cortisol pulse for daytime alertness and starts a 14-to-16 hour countdown for evening melatonin release.

3. Temperature and Sleep Environment:
The human core body temperature must decrease by approximately 1 to 2 degrees Fahrenheit to initiate and sustain deep non-REM slow-wave sleep. Maintain bedroom temperature between 65°F to 68°F (18°C to 20°C). Keep room completely dark using blackout curtains.

4. The 20-Minute Bed-Association Rule (Stimulus Control):
If unable to fall asleep after roughly 20 minutes, get out of bed. Sit in a dimly lit room and engage in non-stimulating analog activity (reading a physical book or listening to relaxing music). Return to bed only when somnolence returns. This preserves the brain's conditioned association between the bed and sleep rather than wakeful anxiety.

5. Caffeine and Alcohol Cutoffs:
Caffeine has an average half-life of 5-7 hours and a quarter-life of up to 12 hours. Cease caffeine intake at least 10 hours before target sleep time. Avoid alcohol as a sleep aid; while sedative, alcohol fragments REM sleep and triggers rebound sympathetic awakening in the second half of the night."""
    },
    {
        "id": "kb_dep_005",
        "title": "Behavioral Activation for Low Mood and Depressive Inertia",
        "category": "Depression and Mood Regulation",
        "author": "Clinical Depression Support Group",
        "organization": "Mood and Affective Disorders Alliance",
        "publication_date": "2023-12-05",
        "source_url": "https://mindcare.ai/resources/behavioral-activation-depression",
        "licensing": "Educational Open Access",
        "content": """Behavioral Activation (BA) is an empirically validated behavioral intervention for depression that addresses the vicious cycle of low energy, social withdrawal, loss of interest, and subsequent deepening of depression.

The Depressive Inactivity Spiral:
When individuals feel depressed or fatigued, the natural urge is to withdraw and rest. However, prolonged inactivity reduces exposure to positive environmental reinforcement and mastery experiences, which deepens fatigue and feelings of guilt.

Principles of Behavioral Activation:
1. Action Precedes Motivation:
Do not wait to 'feel like doing something' before acting. In depression, dopamine signaling is blunted; motivation arrives after initiating the behavior, not beforehand ('Outside-in approach').

2. The 5-Minute Rule / Micro-Stepping:
Deconstruct overwhelming tasks into micro-steps so small that resistance is minimized. For example, if showering feels impossible, commit only to stepping into the bathroom and turning on the water. Once begun, momentum often carries the person forward.

3. Categorizing Activities into Mastery and Pleasure:
- Mastery Activities: Tasks that instill a sense of accomplishment or self-efficacy (e.g., paying a single bill, taking out the garbage, making the bed, organizing a workspace).
- Pleasure Activities: Behaviors that provide sensory or emotional enjoyment (e.g., listening to favorite music, taking a warm bath, tasting a warm beverage, spending time with a pet).

4. Daily Activity Scheduling with Subjective Ratings:
Record completed activities and assign two scores from 0-10:
M = Sense of Mastery (accomplishment)
P = Sense of Pleasure (enjoyment)
Even small scores of 2 or 3 provide vital counter-evidence against the depressive belief that 'nothing matters or helps'."""
    },
    {
        "id": "kb_mnd_006",
        "title": "Mindful Breathing, Heart Rate Variability (HRV), and the Box Breathing Protocol",
        "category": "Mindfulness and Somatic Practices",
        "author": "Dr. Aris Thorne, Neurobiology Researcher",
        "organization": "Integrative Mind-Body Institute",
        "publication_date": "2024-01-28",
        "source_url": "https://mindcare.ai/resources/box-breathing-hrv",
        "licensing": "Creative Commons Attribution 4.0",
        "content": """Controlled respiration is one of the few autonomic bodily functions subject to conscious voluntary control. By modulating respiration depth and cadence, individuals can directly alter vagal nerve tone and increase Heart Rate Variability (HRV).

The Physiological Sigh:
Two quick inhalations through the nose followed by an extended, slow exhalation through the mouth. Repeating this pattern 2-3 times rapidly re-inflates collapsed pulmonary alveoli and expels excess carbon dioxide, providing immediate somatic calming within 30 seconds.

The 4x4 Box Breathing Protocol:
Used widely by high-stress professionals and clinical practitioners to regain emotional composure:
1. Inhale smoothly through the nose for 4 counts, expanding the diaphragm.
2. Hold the breath at full lung capacity for 4 counts without straining.
3. Exhale steadily through parted lips for 4 counts.
4. Hold the lungs empty for 4 counts before initiating the next inhale.
Repeat for 4 to 6 cycles (approximately 3 to 4 minutes).

Vagus Nerve Stimulation and HRV:
When exhalation is intentionally prolonged relative to inhalation (such as 4 seconds in, 6-7 seconds out), the cardiac branch of the vagus nerve releases acetylcholine onto the sinoatrial node, slowing the heart rate and signaling biological safety to the limbic system."""
    },
    {
        "id": "kb_saf_007",
        "title": "Crisis Intervention Standards, Immediate Helplines, and Safety Protocol Guidance",
        "category": "Crisis Safety and Helplines",
        "author": "Global Emergency Mental Health Taskforce",
        "organization": "Crisis Safety International",
        "publication_date": "2024-03-01",
        "source_url": "https://mindcare.ai/resources/crisis-intervention-standards",
        "licensing": "Public Domain / Universal Welfare",
        "content": """Emergency and crisis interventions are critical safety protocols when an individual experiences acute suicidal ideation, urges for self-harm, severe distress, or perceived immediate danger.

Crucial Emergency Resources by Region:
1. India:
- National Emergency Number: Dial 112 (Police, Ambulance, Fire, General Emergency)
- Tele-MANAS (Ministry of Health and Family Welfare): Dial 14416 or 1800-891-4416 (24/7 free mental health counseling in multiple regional languages)
- Vandrevala Foundation Helpline: Dial 9999 666 555 (24/7 free mental health crisis support)
- KIRAN Helpline: Dial 1800-599-0019

2. United States & Canada:
- National Suicide and Crisis Lifeline: Dial 988 (Available 24/7, free, confidential text or call)
- Crisis Text Line: Text 'HOME' to 741741
- Emergency Services: Dial 911

3. United Kingdom:
- Emergency Services: Dial 999
- Samaritans: Dial 116 123 (24/7 free support)
- NHS Mental Health Services: Dial 111

4. International / Worldwide:
- Befrienders Worldwide: https://www.befrienders.org
- IASP (International Association for Suicide Prevention): https://www.iasp.info/resources/Crisis_Centres/

Safety Plan Core Elements:
A personal crisis safety plan includes:
1. Warning signs indicating a crisis is developing (restlessness, withdrawal, acute hopelessness).
2. Internal coping strategies (breathing, walks, grounding).
3. Safe people and social settings that provide healthy distraction.
4. Trusted friends or family members to ask for direct help.
5. Professionals and agencies to contact.
6. Ensuring the immediate environment is physically safe."""
    },
    {
        "id": "kb_emo_008",
        "title": "Distress Tolerance and the TIPP Skills from Dialectical Behavior Therapy (DBT)",
        "category": "Dialectical Behavior Therapy",
        "author": "Dr. Maya Lin, DBT Certified Clinician",
        "organization": "DBT Center for Emotional Regulation",
        "publication_date": "2023-10-18",
        "source_url": "https://mindcare.ai/resources/dbt-tipp-skills",
        "licensing": "Educational Open Access",
        "content": """When emotional distress reaches an overwhelming 8, 9, or 10 on a 10-point scale, higher-level cognitive problem-solving becomes biologically inaccessible due to amygdala hijacking. Distress tolerance skills from Dialectical Behavior Therapy (DBT) aim not to solve the crisis, but to survive the acute moment without making it worse.

The TIPP Skills Protocol:
1. T - Temperature:
Change your body temperature rapidly by placing an ice pack on your eyes and cheeks, or immersing your face in a bowl of cold water (above 50°F / 10°C) for 15-30 seconds while holding your breath. This activates the mammalian dive reflex, which instantly lowers your heart rate and stimulates the parasympathetic nervous system.

2. I - Intense Exercise:
Engage in short, vigorous bursts of physical exertion for 10-15 minutes (jumping jacks, rapid pacing, brisk walking up stairs, sprinting). This burns off excess adrenaline and cortisol accumulated from acute stress.

3. P - Paced Breathing:
Slow your respiration to approximately 5-7 breaths per minute. Inhale deeply through the belly for 4 counts, and exhale slowly for 6 to 8 counts. Keeping exhalations longer than inhalations downregulates arousal.

4. P - Paired Muscle Relaxation:
Progressively tense muscle groups (such as shoulders, fists, calves) for 5 seconds, then consciously release the tension completely while saying the word 'Relax' to yourself. Contrast the physical feeling of tension with releasing, softening muscles."""
    },
    {
        "id": "kb_slf_009",
        "title": "Self-Compassion Practices for Combating Toxic Self-Criticism and Shame",
        "category": "Positive Psychology and Self-Compassion",
        "author": "Dr. Kristin Neff Research Review",
        "organization": "Center for Mindful Self-Compassion",
        "publication_date": "2024-01-08",
        "source_url": "https://mindcare.ai/resources/self-compassion-practices",
        "licensing": "Educational Open Access",
        "content": """Self-criticism is frequently adopted as a misguided motivational strategy; however, neuroimaging demonstrates that self-criticism activates the mammalian threat defense system (fight-or-flight), elevating cortisol and triggering withdrawal. In contrast, self-compassion activates the mammalian caregiving and mammalian soothe system, releasing oxytocin and endorphins.

The Three Pillars of Self-Compassion:
1. Self-Kindness vs. Self-Judgment:
Treating oneself with warmth, understanding, and forgiveness when encountering personal shortcomings or failure, rather than harsh verbal chastisement.

2. Common Humanity vs. Isolation:
Recognizing that suffering, vulnerability, and making mistakes are universal elements of the shared human experience, rather than feeling alienated ('Why does this only happen to me?').

3. Mindfulness vs. Over-Identification:
Holding painful thoughts and emotions in balanced, non-judgmental awareness without suppressing them or becoming swept away in catastrophic rumination.

The Self-Compassion Break (3-Minute Exercise):
When encountering emotional pain or failure, pause and speak these phrases silently to yourself:
1. 'This is a moment of suffering.' (Acknowledging mindfulness).
2. 'Suffering and imperfection are a normal part of life.' (Common humanity).
3. Place a hand gently over your heart or on your arm.
4. 'May I be kind to myself in this moment. May I give myself the patience I need.' (Self-kindness)."""
    },
    {
        "id": "kb_grf_010",
        "title": "Navigating Grief, Bereavement, and The Dual Process Model of Coping",
        "category": "Grief and Loss Support",
        "author": "Margaret Stroebe & Henk Schut Synthesis",
        "organization": "Grief Support & Bereavement Network",
        "publication_date": "2023-08-14",
        "source_url": "https://mindcare.ai/resources/dual-process-model-grief",
        "licensing": "Educational Open Access",
        "content": """Grief is an organic, non-linear human response to the loss of a significant person, relationship, health state, or life dream. Unlike outdated linear models suggesting individuals progress neatly through discrete stages, modern bereavement science recognizes the Dual Process Model.

The Dual Process Model of Grief:
Healthy grieving involves an ongoing, natural oscillation between two orientations:

1. Loss-Oriented Coping:
- Focusing on the emotional reality of the loss.
- Processing grief work, yearning, crying, and reminiscing.
- Looking through photographs or expressing deep sadness.
- Necessary for integrating the emotional reality into one's life story.

2. Restoration-Oriented Coping:
- Focusing on secondary stressors and adapting to the changed world.
- Learning new skills or routines previously handled by the lost person.
- Attending to practical obligations, career tasks, and new social relationships.
- Taking time off from grieving to experience moments of humor, distraction, and recreation.

Key Coping Affirmations:
- It is completely normal to laugh or feel joy even when grieving; taking a break from grief does not dishonor who or what was lost.
- There is no arbitrary deadline for grief.
- Rather than 'getting over' a profound loss, individuals learn to build their lives around the grief, creating expanded capacity for meaning and memory."""
    }
]

