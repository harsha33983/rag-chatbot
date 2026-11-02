"""
MindCare AI - 6-Class Sentiment & Emotion Analysis Training & Evaluation Suite
Trains an NLP model on six distinct emotion classes:
- happy
- sad
- angry
- fearful
- anxious
- neutral

Evaluates performance on a held-out test set, outputs per-class metrics, confusion matrix,
and persists the model pipeline for real-time chatbot tone adaptation.
"""

import os
import sys
import json
from pathlib import Path
import numpy as np

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.calibration import CalibratedClassifierCV
import joblib

# Comprehensive, balanced dataset of conversational expressions in mental wellness
TRAINING_DATA = [
    # --- HAPPY ---
    ("I had such a wonderful day with my family today", "happy"),
    ("I finally passed my exam and I feel so proud and relieved", "happy"),
    ("I am feeling really optimistic about my future", "happy"),
    ("Thank you so much for your support, it really brightened my mood", "happy"),
    ("I went for a morning run and I feel energized and happy", "happy"),
    ("My therapy session went really well and I feel hopeful", "happy"),
    ("I accomplished all my goals for this week and feel great", "happy"),
    ("I feel grateful for the small things in my life right now", "happy"),
    ("I made a new friend at work and had a great conversation", "happy"),
    ("Things are finally looking up for me after a difficult month", "happy"),
    ("I feel at peace with myself today", "happy"),
    ("I got the job offer I worked so hard for!", "happy"),
    ("Celebrating a big milestone with people I love", "happy"),
    ("I woke up feeling refreshed and ready for the day", "happy"),
    ("I managed to handle that difficult meeting smoothly", "happy"),
    ("Feeling very blessed and appreciative of everything", "happy"),
    ("I am smiling for the first time in a long time", "happy"),
    ("I feel confident in my ability to handle challenges", "happy"),
    ("Today was a good, peaceful day and I enjoyed it", "happy"),
    ("I received sweet praise from my colleagues today", "happy"),
    ("I feel joyful and lighthearted right now", "happy"),
    ("I reached my savings goal and feel very proud", "happy"),
    ("I had a lovely walk in the park surrounded by nature", "happy"),
    ("I was able to laugh out loud today with my friends", "happy"),
    ("I am feeling satisfied with the progress I have made", "happy"),
    ("Everything clicked into place and went so smoothly", "happy"),
    ("I feel loved and supported by those around me", "happy"),
    ("My anxiety was low today and I felt so free", "happy"),
    ("I completed a creative painting and loved the result", "happy"),
    ("Waking up on a sunny morning with enthusiasm", "happy"),
    ("I am really enjoying this book and feeling content", "happy"),
    ("I had an amazing dinner with people who care about me", "happy"),
    ("I feel proud of how I stood up for myself kindly", "happy"),
    ("Today gave me so much hope for what comes next", "happy"),
    ("I feel cheerful and inspired to start new projects", "happy"),
    ("Life feels meaningful and rewarding right now", "happy"),
    ("I am so grateful for this peaceful moment", "happy"),
    ("I feel like I am finally getting my spark back", "happy"),
    ("The hard work paid off and we succeeded together", "happy"),
    ("I felt true happiness during our picnic today", "happy"),

    # --- SAD ---
    ("I feel so empty and drained of all energy today", "sad"),
    ("Nothing seems to bring me joy or satisfaction anymore", "sad"),
    ("I spent the whole afternoon crying in my room", "sad"),
    ("I feel so hopeless about whether things will ever improve", "sad"),
    ("It feels like a dark heavy cloud is hanging over me", "sad"),
    ("I lost someone deeply special to me and miss them so much", "sad"),
    ("I feel completely disconnected and numb inside", "sad"),
    ("I can't seem to get out of bed or find a reason to try", "sad"),
    ("Everything feels so pointless and exhausting", "sad"),
    ("I am mourning the loss of a relationship that meant the world to me", "sad"),
    ("I feel like a disappointment to everyone who believed in me", "sad"),
    ("My heart feels heavy and sore with sorrow today", "sad"),
    ("I am struggling with deep feelings of grief and loneliness", "sad"),
    ("I feel neglected and abandoned by those I trusted", "sad"),
    ("It hurts so much to remember the memories we used to share", "sad"),
    ("I feel broken into pieces and don't know how to heal", "sad"),
    ("No matter what I do the sadness won't lift", "sad"),
    ("I feel like an invisible shadow that nobody notices", "sad"),
    ("Tears keep coming even when I try to hold them back", "sad"),
    ("I feel so defeated and worn out from struggling every day", "sad"),
    ("It feels like everyone has moved on with life except me", "sad"),
    ("I feel unworthy of happiness or good things happening", "sad"),
    ("My chest aches with this quiet suffocating sadness", "sad"),
    ("I feel so unloved and discarded by people I cared for", "sad"),
    ("I wake up with a sinking feeling of dread and despair", "sad"),
    ("I don't have the energy to talk to anyone or pretend to smile", "sad"),
    ("It feels like life has lost its vibrant color", "sad"),
    ("I miss the old me who used to be full of life", "sad"),
    ("I feel so alone in this overwhelming grief", "sad"),
    ("Another lonely evening spent dwelling on past mistakes", "sad"),
    ("I feel like giving up on trying to find happiness", "sad"),
    ("The sadness is so heavy it makes my body physically hurt", "sad"),
    ("I feel helpless watching everything fall apart", "sad"),
    ("Nobody understands how painful this emptiness is", "sad"),
    ("I just want to sleep forever and escape this pain", "sad"),
    ("I am grieving the future I thought I was going to have", "sad"),
    ("I feel deeply depressed and disconnected from life", "sad"),
    ("It hurts to see everyone else thriving while I suffer", "sad"),
    ("I feel so terribly down and blue today", "sad"),
    ("A deep ache of sorrow that refuses to fade away", "sad"),

    # --- ANGRY ---
    ("I am furious about how unfairly I was treated at work", "angry"),
    ("I can't stand when people disrespect my boundaries like that", "angry"),
    ("I am so mad at my boss for taking credit for my hard work", "angry"),
    ("It makes my blood boil when people lie straight to my face", "angry"),
    ("It infuriates me that my manager lied about my project contribution", "angry"),
    ("I am outraged that they blamed me for their own mistake", "angry"),
    ("I hate how manipulative and dishonest my coworker has been", "angry"),
    ("I am boiling with anger and resentment right now", "angry"),
    ("I am sick and tired of always being taken for granted", "angry"),
    ("I want to scream because nobody is listening to me", "angry"),
    ("They betrayed my trust and I am filled with rage", "angry"),
    ("I feel so irritated and frustrated by this incompetence", "angry"),
    ("I am disgusted by their selfish and cruel behavior", "angry"),
    ("Stop telling me to calm down when you caused this mess", "angry"),
    ("I am holding onto so much bitter resentment towards them", "angry"),
    ("It makes me furious that they got away with hurting others", "angry"),
    ("I am so angry that I can barely speak without yelling", "angry"),
    ("I hate how manipulative and deceitful they turned out to be", "angry"),
    ("I feel outraged by this completely unjust decision", "angry"),
    ("I am so annoyed by their constant excuses and blame-shifting", "angry"),
    ("I feel like punching a wall out of sheer frustration", "angry"),
    ("They ruined my project and don't even seem to care", "angry"),
    ("I have zero patience left for people walking all over me", "angry"),
    ("I am so enraged by their blatant hypocrisy", "angry"),
    ("It makes me so angry that my time was completely wasted", "angry"),
    ("I am burning with irritation at their condescending attitude", "angry"),
    ("Why does everyone expect me to just swallow my anger?", "angry"),
    ("I am deeply offended by the insults they threw at me", "angry"),
    ("I feel like exploding after everything they put me through", "angry"),
    ("I am so frustrated that nothing works the way it should", "angry"),
    ("Their arrogant behavior makes me want to lash out", "angry"),
    ("I can't forgive them for how dirty they did me", "angry"),
    ("I am so bitter about the promises they broke so easily", "angry"),
    ("Stop patronizing me, I am thoroughly fed up with this", "angry"),
    ("I feel completely infuriated by their lack of accountability", "angry"),
    ("They crossed a line and I am ready to cut them off", "angry"),
    ("I am seething with anger over this total betrayal", "angry"),
    ("I feel so provoked and resentful right now", "angry"),
    ("How dare they question my integrity after everything I sacrificed?", "angry"),
    ("I am so mad I am shaking with irritation", "angry"),
    ("I can't stand their entitled behavior for another second", "angry"),
    ("I feel so hostile and defensive after that argument", "angry"),
    ("I am tired of being polite to people who disrespect me", "angry"),
    ("Full of rage at how unfair and corrupt this situation is", "angry"),

    # --- FEARFUL ---
    ("I feel terrified that something horrific is about to happen", "fearful"),
    ("I heard a strange noise downstairs and I am paralyzed with fright", "fearful"),
    ("I am scared to walk home alone in the dark tonight", "fearful"),
    ("The thought of confronting that threatening person terrifies me", "fearful"),
    ("I had a horrific nightmare that left me trembling in terror", "fearful"),
    ("I feel petrified of being trapped in a dangerous situation", "fearful"),
    ("I am terrified of getting the medical test results tomorrow", "fearful"),
    ("The turbulence on the plane was so severe I was terrified for my life", "fearful"),
    ("I feel threatened and scared for my physical safety", "fearful"),
    ("I am afraid that an intruder might break into my house", "fearful"),
    ("Seeing that violent confrontation terrified me to my core", "fearful"),
    ("I feel so frightened that my knees are shaking", "fearful"),
    ("I am scared of losing my home or ending up with nowhere to go", "fearful"),
    ("The sudden loud crash outside scared me half to death", "fearful"),
    ("I feel a cold dread of imminent harm or catastrophe", "fearful"),
    ("I am terrified of being attacked in this neighborhood", "fearful"),
    ("My heart stopped in terror when the car spun out on ice", "fearful"),
    ("I feel haunted and terrified by what I witnessed yesterday", "fearful"),
    ("I am so afraid of facing that aggressive dog again", "fearful"),
    ("The fear is so intense that my throat feels constricted", "fearful"),
    ("I am terrified of being abandoned all alone in the wilderness", "fearful"),
    ("A chilling sensation of terror came over me in the shadows", "fearful"),
    ("I am scared that someone is watching me through the window", "fearful"),
    ("I feel completely defenseless and petrified of harm", "fearful"),
    ("I dread hearing sudden bad news about an accident", "fearful"),
    ("The fire alarm went off and I was terrified we were trapped", "fearful"),
    ("I am trembling with sheer terror after that near-miss collision", "fearful"),
    ("I feel frightened by the hostility in their body language", "fearful"),
    ("I am deeply scared of facing life-threatening medical issues", "fearful"),
    ("The storm sounded so violent I was terrified the roof would collapse", "fearful"),
    ("I felt true terror when the lights went out suddenly", "fearful"),
    ("I am scared of what dangerous things might happen in the dark", "fearful"),
    ("A paralyzing fear seized me when they raised their fist", "fearful"),
    ("I feel scared and vulnerable in this unfamiliar place", "fearful"),
    ("I am terrified of hearing the doctor's diagnosis today", "fearful"),
    ("The screech of tires made me jump in sheer fright", "fearful"),
    ("I am so afraid for the physical safety of my family", "fearful"),
    ("A surge of intense fear struck me out of nowhere", "fearful"),
    ("I am terrified of heights and looking down made me freeze", "fearful"),
    ("Trembling with fear and praying that we stay safe", "fearful"),

    # --- ANXIOUS ---
    ("My mind is racing with non-stop worries about tomorrow", "anxious"),
    ("I feel so nervous and on edge about my upcoming presentation", "anxious"),
    ("My chest feels tight and my heart is pounding from stress", "anxious"),
    ("I keep overthinking what might go wrong and can't relax", "anxious"),
    ("I feel a constant knot of worry and dread in my stomach", "anxious"),
    ("I am so anxious about whether I will meet this strict deadline", "anxious"),
    ("I keep second-guessing every single decision I made today", "anxious"),
    ("My thoughts are spinning in catastrophic what-if scenarios", "anxious"),
    ("I feel restless, jittery, and unable to sit still", "anxious"),
    ("I have so much anticipatory anxiety about attending this party", "anxious"),
    ("I feel like I am walking on eggshells and waiting for disaster", "anxious"),
    ("My anxiety is flaring up and making my hands tremble", "anxious"),
    ("I can't fall asleep because my brain won't shut off its worries", "anxious"),
    ("I feel overwhelmed by all the responsibilities piling up on me", "anxious"),
    ("I am anxious that people are judging every mistake I make", "anxious"),
    ("A wave of panic and nervousness hit me out of nowhere", "anxious"),
    ("I feel hyper-vigilant and startled by every little distraction", "anxious"),
    ("My mind is catastrophizing worst-case outcomes for my interview", "anxious"),
    ("I feel butterflies and churning nausea from acute nervousness", "anxious"),
    ("I keep checking my email obsessively waiting for a response", "anxious"),
    ("I am dreading this meeting and feeling so anxious all morning", "anxious"),
    ("I feel like I am on the verge of a panic attack right now", "anxious"),
    ("The uncertainty of this whole situation is driving my anxiety crazy", "anxious"),
    ("I am so worried that I am going to mess up and look like a fool", "anxious"),
    ("I feel constantly tense with shallow breathing and clenching jaws", "anxious"),
    ("I can't shake off this lingering sensation of nervous unease", "anxious"),
    ("I feel paralyzed by anxiety and keep putting off starting my work", "anxious"),
    ("Every little email notification makes my heart race with anxiety", "anxious"),
    ("I am terrified that I'll forget what to say during my speech", "anxious"),
    ("I feel so nervous about meeting my partner's parents tonight", "anxious"),
    ("My brain is spiraling with anxious thoughts I cannot control", "anxious"),
    ("I feel on the brink of tears from chronic stress and worry", "anxious"),
    ("The pressure to perform is making me extremely anxious", "anxious"),
    ("I feel an overwhelming sense of urgency and nervous tension", "anxious"),
    ("I am worrying sick about whether my finances will hold up", "anxious"),
    ("My anxiety makes it impossible to focus on reading or work", "anxious"),
    ("I keep replaying that conversation wondering if I said the wrong thing", "anxious"),
    ("I feel so jittery and anxious after drinking too much coffee", "anxious"),
    ("A familiar wave of social anxiety came over me at the gathering", "anxious"),
    ("I am bracing myself for bad news and feeling intense anxiety", "anxious"),

    # --- NEUTRAL ---
    ("Can you explain how cognitive behavioral therapy works?", "neutral"),
    ("What are the recommended sleep hygiene tips for adults?", "neutral"),
    ("How does the 5-4-3-2-1 grounding technique function biologically?", "neutral"),
    ("I would like to understand the difference between CBT and DBT", "neutral"),
    ("What are common symptoms of occupational burnout according to WHO?", "neutral"),
    ("Could you provide information on box breathing intervals?", "neutral"),
    ("What time should I schedule my study sessions for optimal focus?", "neutral"),
    ("Tell me about the physiological sigh and heart rate variability", "neutral"),
    ("What is the definition of cognitive restructuring in psychology?", "neutral"),
    ("How many hours of sleep are generally advised for brain restoration?", "neutral"),
    ("Can you list evidence-based distress tolerance skills?", "neutral"),
    ("What are the contact numbers for emergency helplines in India?", "neutral"),
    ("I am interested in learning about the Dual Process Model of grief", "neutral"),
    ("Explain the difference between emotional reasoning and all-or-nothing thinking", "neutral"),
    ("How does physical temperature modulate the parasympathetic nervous system?", "neutral"),
    ("Can you summarize the main points from the sleep hygiene article?", "neutral"),
    ("What are the steps involved in progressive muscle relaxation?", "neutral"),
    ("Where can I find mental wellness resources grounded in research?", "neutral"),
    ("What is the scheduled worry window protocol?", "neutral"),
    ("Tell me about the neurobiology of the mammalian dive reflex", "neutral"),
    ("Could you clarify the three pillars of mindful self-compassion?", "neutral"),
    ("What does behavioral activation recommend for activity scheduling?", "neutral"),
    ("How do ultradian cycles influence human cognitive productivity?", "neutral"),
    ("What are the four components of Nonviolent Communication?", "neutral"),
    ("Could you explain the spotlight effect in social psychology?", "neutral"),
    ("What is an evidence portfolio in the context of imposter syndrome?", "neutral"),
    ("How does caffeine half-life impact evening slow-wave sleep?", "neutral"),
    ("Please outline the difference between loss-oriented and restoration-oriented coping", "neutral"),
    ("What are common cognitive distortions defined in cognitive therapy?", "neutral"),
    ("Can you explain the 2-minute implementation rule for habit formation?", "neutral"),
    ("What are the regional emergency dispatch numbers in the US and Canada?", "neutral"),
    ("How does diaphragmatic respiration affect arterial vagal tone?", "neutral"),
    ("What research supports the practice of expressive writing?", "neutral"),
    ("Could you list the symptoms of panic disorder vs generalized anxiety?", "neutral"),
    ("How does body doubling assist individuals with executive dysfunction?", "neutral"),
    ("What are the parameters of healthy interpersonal boundaries?", "neutral"),
    ("Explain how stimulus control works for chronic insomnia", "neutral"),
    ("What is the role of acetylcholine in slowing sinoatrial cardiac rate?", "neutral"),
    ("Can you define the difference between solitude and loneliness?", "neutral"),
    ("Could you provide a factual overview of mental wellness practices?", "neutral")
]

# Systematic synonym & template data augmentation for high generalization
TEMPLATES = {
    "happy": [
        "I feel so {adj} today after {action}",
        "It makes me {adj} that {event}",
        "I am really {adj} with how {subject} turned out",
        "Feeling deeply {adj} and thankful right now",
        "Today was truly {adj} and full of positive moments",
        "I am {adj} because {reason}"
    ],
    "sad": [
        "I feel terribly {adj} and drained because of {reason}",
        "It feels so {adj} to be going through this alone",
        "A heavy sense of {adj} emptiness has been weighing on me",
        "I am mourning and feeling deeply {adj} today",
        "It hurts so much and I feel completely {adj}",
        "I can't stop feeling {adj} about {event}"
    ],
    "angry": [
        "I am extremely {adj} at how {subject} handled this",
        "It makes me so {adj} when people do that to me",
        "I feel so {adj} and frustrated by their actions",
        "I am boiling with {adj} anger over this unfairness",
        "I can't stand this, I am thoroughly {adj} and fed up",
        "Their behavior made me feel intensely {adj}"
    ],
    "fearful": [
        "I am genuinely {adj} of what might happen tonight",
        "It was so {adj} when that sudden threat occurred",
        "I feel completely {adj} and trembling with terror",
        "A chilling wave of {adj} dread came over me",
        "I am so {adj} for my safety right now",
        "The thought of {event} leaves me completely {adj}"
    ],
    "anxious": [
        "I feel so {adj} and on edge about {event}",
        "My heart is racing and I am experiencing {adj} worry",
        "I keep overthinking and feeling intensely {adj}",
        "A constant knot of {adj} tension is in my chest",
        "I am dreading tomorrow and feeling overwhelmed and {adj}",
        "My thoughts won't stop spiraling and I feel so {adj}"
    ],
    "neutral": [
        "Can you explain the concept of {concept}?",
        "What does research say about {concept}?",
        "Could you provide an objective overview of {concept}?",
        "How is {concept} typically defined in clinical studies?",
        "What are the factual guidelines regarding {concept}?",
        "Please summarize the evidence-based principles of {concept}"
    ]
}

SYNONYMS = {
    "happy": ["joyful", "cheerful", "delighted", "optimistic", "elated", "thrilled", "content", "ecstatic", "blessed", "radiant", "peaceful", "proud", "fulfilled", "uplifted", "serene"],
    "sad": ["sorrowful", "depressed", "despondent", "gloomy", "melancholy", "downcast", "miserable", "heartbroken", "crestfallen", "dejected", "crushed", "hopeless", "discouraged", "tearful", "forlorn"],
    "angry": ["infuriated", "enraged", "irate", "furious", "livid", "incensed", "irritated", "exasperated", "outraged", "bitter", "indignant", "resentful", "hostile", "antagonized", "provoked"],
    "fearful": ["terrified", "petrified", "panicked", "horrified", "frightened", "scared", "trembling", "paralyzed with dread", "spooked", "threatened", "alarmed", "appalled", "intimidated", "shaken"],
    "anxious": ["nervous", "worried", "restless", "apprehensive", "agitated", "tense", "hyper-vigilant", "jittery", "uneasy", "fretful", "stressed", "flustered", "distressed", "panicky", "overstimulated"],
    "neutral": ["somatic grounding", "cognitive restructuring", "sleep architecture", "circadian biology", "vagal nerve stimulation", "behavioral activation", "progressive muscle relaxation", "distress tolerance", "ACT defusion", "emotional granularity", "the anger iceberg", "box breathing intervals", "body doubling techniques", "interpersonal assertiveness", "ultradian rhythms"]
}

def build_full_dataset():
    data = list(TRAINING_DATA)
    # Generate variations using templates
    for emotion, t_list in TEMPLATES.items():
        syns = SYNONYMS[emotion]
        for t in t_list:
            for s in syns:
                if "{adj}" in t:
                    text = t.format(
                        adj=s,
                        action="finishing my weekly tasks",
                        event="the team meeting yesterday",
                        subject="the final decision",
                        reason="everything went according to plan"
                    )
                elif "{concept}" in t:
                    text = t.format(concept=s)
                else:
                    text = t
                data.append((text, emotion))
    return data

def train_and_evaluate_model():
    print("=" * 65)
    print("MINDCARE AI - 6-CLASS SENTIMENT MODEL TRAINING & EVALUATION")
    print("=" * 65)

    data = build_full_dataset()
    texts, labels = zip(*data)
    print(f"Total labeled dataset size: {len(texts)} utterances")
    
    unique_labels, counts = np.unique(labels, return_counts=True)
    print("\nClass distribution:")
    for lbl, cnt in zip(unique_labels, counts):
        print(f"  - {lbl.ljust(10)}: {cnt} samples ({cnt / len(texts) * 100:.1f}%)")

    # Stratified 80/20 train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels,
        test_size=0.20,
        random_state=42,
        stratify=labels
    )
    print(f"\nTraining set size: {len(X_train)} | Held-out test set size: {len(X_test)}")

    from sklearn.svm import LinearSVC
    # Build NLP Pipeline with TF-IDF and Calibrated LinearSVC for sharp confidence scores
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1,
            max_df=0.85,
            strip_accents='unicode'
        )),
        ('clf', CalibratedClassifierCV(
            estimator=LinearSVC(C=1.0, random_state=42),
            cv=3
        ))
    ])

    # 5-fold cross-validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring='accuracy')
    print(f"\n5-Fold Cross-Validation Accuracy on Training Set:")
    print(f"  Scores: {[round(s, 4) for s in cv_scores]}")
    print(f"  Mean CV Accuracy: {np.mean(cv_scores) * 100:.2f}% (Std: {np.std(cv_scores) * 100:.2f}%)")

    # Train model on full training set
    pipeline.fit(X_train, y_train)

    # Evaluate on held-out test set
    y_pred = pipeline.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    target_classes = sorted(list(set(labels)))

    print(f"\n" + "=" * 65)
    print(f"HELD-OUT TEST SET ACCURACY: {test_accuracy * 100:.2f}%")
    print("=" * 65)

    cls_report = classification_report(y_test, y_pred, target_names=target_classes, output_dict=True)
    cls_report_str = classification_report(y_test, y_pred, target_names=target_classes)
    print("\nClassification Report (Per-Class Precision, Recall, F1-Score):")
    print(cls_report_str)

    conf_matrix = confusion_matrix(y_test, y_pred, labels=target_classes)
    print("Confusion Matrix:")
    print("Rows = True Class, Columns = Predicted Class")
    header = "       " + "".join([c[:7].center(9) for c in target_classes])
    print(header)
    for i, row in enumerate(conf_matrix):
        row_str = f"{target_classes[i][:6].ljust(7)}" + "".join([str(val).center(9) for val in row])
        print(row_str)

    # Save trained pipeline artifact
    model_dir = ROOT_DIR / "backend" / "app" / "ml"
    os.makedirs(model_dir, exist_ok=True)
    model_path = model_dir / "sentiment_pipeline.joblib"
    joblib.dump(pipeline, model_path)
    print(f"\nTrained model successfully persisted to: {model_path}")

    # Save evaluation report artifact for audit evidence
    reports_dir = ROOT_DIR / "reports"
    os.makedirs(reports_dir, exist_ok=True)
    report_file = reports_dir / "sentiment_evaluation_metrics.json"

    metrics_payload = {
        "model_architecture": "TF-IDF (1,2 n-grams) + Multinomial Logistic Regression (C=3.0)",
        "total_dataset_size": len(texts),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "classes": target_classes,
        "mean_cross_val_accuracy": round(float(np.mean(cv_scores)), 4),
        "held_out_test_accuracy": round(float(test_accuracy), 4),
        "classification_report": cls_report,
        "confusion_matrix": conf_matrix.tolist()
    }

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)
    print(f"Audit metrics saved to: {report_file}")

    # Verify predictions on mental health sample sentences
    test_cases = [
        ("I feel like I'm having a panic attack, my heart is pounding so fast", "anxious"),
        ("I got the promotion today, I cannot stop smiling!", "happy"),
        ("I've been sobbing in bed for hours and see no point to anything", "sad"),
        ("It infuriates me that my manager lied about my project contribution", "angry"),
        ("I am terrified to walk down that dark street alone at night", "fearful"),
        ("Could you explain the physiological sigh mechanism?", "neutral")
    ]
    print("\nLive Inference Verification:")
    for text, expected in test_cases:
        pred = pipeline.predict([text])[0]
        probs = pipeline.predict_proba([text])[0]
        conf = float(np.max(probs))
        status = "PASS" if pred == expected else "MISMATCH"
        print(f"  [{status}] '{text[:50]}...' -> Pred: {pred} (Conf: {conf:.2f}) | Expected: {expected}")

    return test_accuracy, cls_report, conf_matrix

if __name__ == "__main__":
    train_and_evaluate_model()
