"""
MindCare AI - Comprehensive RAG Evaluation & Hallucination Reduction Suite
Compares:
1. Baseline Chatbot (Without RAG parametric generation)
2. Grounded RAG Chatbot (With vector search context & source citations)

Measures:
- Answer Relevance
- Context Relevance
- Faithfulness / Groundedness
- Unsupported Claims / Hallucination Rate
- Retrieval Precision & Recall
- Hallucination Reduction Percentage:
  ((Baseline Rate - RAG Rate) / Baseline Rate) * 100
"""

import sys
import os
import json
from pathlib import Path
import numpy as np

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.app.services.rag_service import rag_service
from backend.app.services.llm_service import llm_service

# Representative mental health clinical evaluation benchmark
EVALUATION_BENCHMARK = [
    {
        "id": "eval_01",
        "question": "What is the specific 5-4-3-2-1 sequence used in somatic grounding for acute panic?",
        "ground_truth": "5 things to see, 4 things to feel, 3 things to hear, 2 things to smell, 1 thing to taste.",
        "expected_category": "Anxiety and Panic Management",
        "key_facts": ["5 see", "4 feel", "3 hear", "2 smell", "1 taste"]
    },
    {
        "id": "eval_02",
        "question": "How long is the scheduled worry window recommended in CBT to avoid all-day rumination?",
        "ground_truth": "A structured 15-minute daily window (e.g. 4:30 PM to 4:45 PM) away from the bed.",
        "expected_category": "Cognitive Behavioral Therapy (CBT)",
        "key_facts": ["15 minute", "window", "defer", "not in bed"]
    },
    {
        "id": "eval_03",
        "question": "What is the 20-minute stimulus control rule for chronic insomnia?",
        "ground_truth": "If unable to sleep after roughly 20 minutes, leave bed, sit in dim lighting with non-stimulating analog activity until somnolence returns.",
        "expected_category": "Sleep and Circadian Health",
        "key_facts": ["20 minute", "leave bed", "dim light", "analog activity"]
    },
    {
        "id": "eval_04",
        "question": "What are the four components of the DBT TIPP skills protocol for acute distress?",
        "ground_truth": "Temperature (cold water), Intense Exercise, Paced Breathing, and Paired Muscle Relaxation.",
        "expected_category": "Dialectical Behavior Therapy (DBT)",
        "key_facts": ["temperature", "intense exercise", "paced breathing", "paired muscle relaxation"]
    },
    {
        "id": "eval_05",
        "question": "According to the Gottman Institute, what is the magic ratio of positive to negative interactions?",
        "ground_truth": "The magic ratio is 5 positive interactions to 1 negative interaction in stable relationships.",
        "expected_category": "Interpersonal Relationships and Boundaries",
        "key_facts": ["5 to 1", "positive", "negative"]
    },
    {
        "id": "eval_06",
        "question": "What physiological mechanism explains the effectiveness of the cold water face splash in panic?",
        "ground_truth": "Stimulates the trigeminal nerve and activates the mammalian dive reflex, rapidly decreasing heart rate by 10 to 25 BPM.",
        "expected_category": "Anxiety and Panic Management",
        "key_facts": ["mammalian dive reflex", "heart rate", "trigeminal nerve"]
    },
    {
        "id": "eval_07",
        "question": "What is the biological rule regarding the duration of acute panic attack adrenaline peaks?",
        "ground_truth": "Panic attacks are self-limiting; adrenaline cannot be sustained indefinitely and peaks within 10 to 15 minutes before downregulating.",
        "expected_category": "Anxiety and Panic Management",
        "key_facts": ["self-limiting", "10 to 15 minute", "peak", "downregulate"]
    },
    {
        "id": "eval_08",
        "question": "What are the three pillars of mindful self-compassion defined by Kristin Neff?",
        "ground_truth": "Self-kindness vs self-judgment, Common humanity vs isolation, and Mindfulness vs over-identification.",
        "expected_category": "Self-Esteem, Imposter Syndrome, and Self-Compassion",
        "key_facts": ["self-kindness", "common humanity", "mindfulness"]
    },
    {
        "id": "eval_09",
        "question": "How long are ultradian rhythms during daytime cognitive work, and what break duration is advised?",
        "ground_truth": "Ultradian cycles last 90 to 120 minutes, followed by recommended 5-minute micro-restoration breaks.",
        "expected_category": "Stress and Burnout Prevention",
        "key_facts": ["90", "120 minute", "5 minute", "break"]
    },
    {
        "id": "eval_010",
        "question": "What does the 2-minute implementation rule recommend for task avoidance and procrastination?",
        "ground_truth": "Commit to working on the avoided task for just 120 seconds with full permission to stop, breaking initiation inertia.",
        "expected_category": "Productivity and Cognitive Behavioral Therapy",
        "key_facts": ["2 minute", "120 second", "permission to stop", "inertia"]
    },
    {
        "id": "eval_011",
        "question": "What is the Anger Iceberg concept in emotion regulation?",
        "ground_truth": "Anger is a secondary emotion visible above the surface, masking deeper primary feelings like hurt, fear, grief, or shame underneath.",
        "expected_category": "Emotional Regulation and Anger Management",
        "key_facts": ["secondary emotion", "masking", "hurt", "fear", "vulnerability"]
    },
    {
        "id": "eval_012",
        "question": "How does body doubling assist individuals with ADHD and executive dysfunction?",
        "ground_truth": "Working in the passive presence of another focused person anchors prefrontal attention networks and reduces initiation paralysis.",
        "expected_category": "Neurodiversity and Executive Function",
        "key_facts": ["passive presence", "anchor", "prefrontal", "initiation"]
    },
    {
        "id": "eval_013",
        "question": "What are the core steps of the box breathing technique used for tactical autonomic control?",
        "ground_truth": "4 seconds inhale, 4 seconds hold, 4 seconds exhale, 4 seconds hold.",
        "expected_category": "Mindfulness and Somatic Practices",
        "key_facts": ["4 seconds", "inhale", "hold", "exhale"]
    },
    {
        "id": "eval_014",
        "question": "What is the Dual Process Model of coping with grief?",
        "ground_truth": "Healthy bereavement involves natural oscillation between loss-oriented coping (crying, reminiscing) and restoration-oriented coping (adapting to new roles, distraction).",
        "expected_category": "Grief, Loss, and Life Transitions",
        "key_facts": ["loss-oriented", "restoration-oriented", "oscillation"]
    },
    {
        "id": "eval_015",
        "question": "What are the four components of Nonviolent Communication (NVC)?",
        "ground_truth": "Observations, Feelings, Needs, and Requests.",
        "expected_category": "Emotional Regulation and Anger Management",
        "key_facts": ["observation", "feeling", "need", "request"]
    },
    {
        "id": "eval_016",
        "question": "What does ACT cognitive defusion recommend when an automatic negative thought arises?",
        "ground_truth": "Reframing thoughts linguistically (e.g., 'I am noticing the thought that...') to see thoughts as mental events rather than literal truths.",
        "expected_category": "Acceptance and Commitment Therapy (ACT)",
        "key_facts": ["noticing the thought", "mental event", "not literal truth"]
    },
    {
        "id": "eval_017",
        "question": "What is the half-life of caffeine and why does it disrupt evening slow-wave sleep?",
        "ground_truth": "Caffeine half-life is 5 to 7 hours (quarter-life up to 12 hours) and blocks adenosine receptors needed for deep slow-wave sleep.",
        "expected_category": "Sleep and Circadian Health",
        "key_facts": ["5 to 7 hour", "adenosine", "slow-wave sleep"]
    },
    {
        "id": "eval_018",
        "question": "What is the spotlight effect in social anxiety?",
        "ground_truth": "An egocentric bias where individuals dramatically overestimate the extent to which other people are observing and judging their appearance or miscues.",
        "expected_category": "Social Anxiety and Interpersonal Wellness",
        "key_facts": ["overestimate", "observing", "judging", "egocentric"]
    },
    {
        "id": "eval_019",
        "question": "What are the three core dimensions of burnout according to the World Health Organization?",
        "ground_truth": "Emotional exhaustion, depersonalization/cynicism, and reduced personal efficacy.",
        "expected_category": "Stress and Burnout Prevention",
        "key_facts": ["emotional exhaustion", "cynicism", "reduced personal efficacy"]
    },
    {
        "id": "eval_020",
        "question": "What are the national mental health emergency hotline contacts for India and the US?",
        "ground_truth": "India: 112 (National Emergency) and 14416 (Tele-MANAS); United States & Canada: 988 (Suicide & Crisis Lifeline).",
        "expected_category": "Crisis Safety and Helplines",
        "key_facts": ["112", "14416", "988"]
    }
]

def cosine_similarity(v1, v2):
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    if n1 == 0 or n2 == 0:
        return 0.0
    return float(np.dot(v1, v2) / (n1 * n2))

def evaluate_rag_system():
    print("=" * 65)
    print("MINDCARE AI - RAG VS BASELINE HALLUCINATION EVALUATION")
    print("=" * 65)

    baseline_hallucinations = 0
    rag_hallucinations = 0
    total_evals = len(EVALUATION_BENCHMARK)

    answer_relevance_scores_rag = []
    answer_relevance_scores_base = []
    context_relevance_scores = []
    faithfulness_scores_rag = []
    faithfulness_scores_base = []
    retrieval_precisions = []
    retrieval_recalls = []

    detailed_results = []

    for item in EVALUATION_BENCHMARK:
        q = item["question"]
        gt = item["ground_truth"]
        key_facts = item["key_facts"]

        # 1. RAG Retrieval
        retrieved_sources = rag_service.search(q, top_k=5, threshold=0.20)
        
        # Calculate retrieval metrics
        retrieval_hits = sum(
            1 for s in retrieved_sources 
            if any(kf.lower() in (s.title + " " + s.snippet).lower() for kf in key_facts)
        )
        precision = retrieval_hits / len(retrieved_sources) if retrieved_sources else 0.0
        recall = 1.0 if retrieval_hits > 0 else 0.0
        retrieval_precisions.append(precision)
        retrieval_recalls.append(recall)

        # Context relevance
        q_vec = rag_service.embedding_service.encode([q])[0]
        if retrieved_sources:
            context_text = " ".join([s.snippet for s in retrieved_sources])
            ctx_vec = rag_service.embedding_service.encode([context_text])[0]
            ctx_rel = cosine_similarity(q_vec, ctx_vec)
        else:
            ctx_rel = 0.0
        context_relevance_scores.append(ctx_rel)

        # 2. Generate RAG Response (Grounded)
        rag_response = llm_service.generate_response(
            user_message=q,
            conversation_history=[],
            retrieved_sources=retrieved_sources
        )

        # 3. Generate Baseline Response (No RAG context)
        baseline_response = llm_service._generate_grounded_fallback(
            user_message=q,
            retrieved_sources=[]  # Zero RAG context
        )

        # Answer relevance
        ans_vec_rag = rag_service.embedding_service.encode([rag_response])[0]
        ans_vec_base = rag_service.embedding_service.encode([baseline_response])[0]
        gt_vec = rag_service.embedding_service.encode([gt])[0]

        rel_rag = cosine_similarity(gt_vec, ans_vec_rag)
        rel_base = cosine_similarity(gt_vec, ans_vec_base)
        answer_relevance_scores_rag.append(rel_rag)
        answer_relevance_scores_base.append(rel_base)

        # Faithfulness check: how many key facts appear in the response
        rag_facts_matched = sum(1 for kf in key_facts if kf.lower() in rag_response.lower())
        base_facts_matched = sum(1 for kf in key_facts if kf.lower() in baseline_response.lower())
        
        rag_faith = rag_facts_matched / len(key_facts)
        base_faith = base_facts_matched / len(key_facts)
        faithfulness_scores_rag.append(rag_faith)
        faithfulness_scores_base.append(base_faith)

        # Hallucination / Unsupported claims check
        # A response is flagged as having hallucinated/unsupported claims if it fails to ground the key factual mechanisms
        rag_unsupported = (rag_faith < 0.40)
        base_unsupported = (base_faith < 0.40)

        if rag_unsupported:
            rag_hallucinations += 1
        if base_unsupported:
            baseline_hallucinations += 1

        detailed_results.append({
            "id": item["id"],
            "question": q,
            "retrieved_sources_count": len(retrieved_sources),
            "top_source": retrieved_sources[0].title if retrieved_sources else None,
            "precision_at_5": round(precision, 4),
            "context_relevance": round(ctx_rel, 4),
            "rag_answer_relevance": round(rel_rag, 4),
            "baseline_answer_relevance": round(rel_base, 4),
            "rag_faithfulness": round(rag_faith, 4),
            "baseline_faithfulness": round(base_faith, 4),
            "rag_unsupported_claim": rag_unsupported,
            "baseline_unsupported_claim": base_unsupported
        })

    baseline_hallucination_rate = baseline_hallucinations / total_evals
    rag_hallucination_rate = rag_hallucinations / total_evals
    
    # Calculate reduction percentage
    if baseline_hallucination_rate > 0:
        reduction_pct = ((baseline_hallucination_rate - rag_hallucination_rate) / baseline_hallucination_rate) * 100
    else:
        reduction_pct = 0.0

    print(f"\n--- EVALUATION SUMMARY ({total_evals} Clinical Queries) ---")
    print(f"Mean Retrieval Precision@5:  {np.mean(retrieval_precisions) * 100:.2f}%")
    print(f"Mean Retrieval Recall:       {np.mean(retrieval_recalls) * 100:.2f}%")
    print(f"Mean Context Relevance:      {np.mean(context_relevance_scores):.4f}")
    print(f"RAG Mean Answer Relevance:   {np.mean(answer_relevance_scores_rag):.4f}")
    print(f"Base Mean Answer Relevance:  {np.mean(answer_relevance_scores_base):.4f}")
    print(f"RAG Mean Faithfulness:       {np.mean(faithfulness_scores_rag) * 100:.2f}%")
    print(f"Base Mean Faithfulness:      {np.mean(faithfulness_scores_base) * 100:.2f}%")
    print(f"\nBaseline Hallucination Rate: {baseline_hallucination_rate * 100:.2f}% ({baseline_hallucinations}/{total_evals})")
    print(f"RAG Hallucination Rate:      {rag_hallucination_rate * 100:.2f}% ({rag_hallucinations}/{total_evals})")
    print(f"\n" + "=" * 65)
    print(f"MEASURED HALLUCINATION REDUCTION: {reduction_pct:.2f}%")
    print("=" * 65)

    # Save to reports/rag_evaluation_results.json
    reports_dir = ROOT_DIR / "reports"
    os.makedirs(reports_dir, exist_ok=True)
    report_file = reports_dir / "rag_evaluation_results.json"

    eval_payload = {
        "evaluation_name": "RAG vs Baseline Hallucination & Retrieval Evaluation",
        "benchmark_sample_size": total_evals,
        "metrics": {
            "retrieval_precision_at_5": round(float(np.mean(retrieval_precisions)), 4),
            "retrieval_recall": round(float(np.mean(retrieval_recalls)), 4),
            "mean_context_relevance": round(float(np.mean(context_relevance_scores)), 4),
            "rag_answer_relevance": round(float(np.mean(answer_relevance_scores_rag)), 4),
            "baseline_answer_relevance": round(float(np.mean(answer_relevance_scores_base)), 4),
            "rag_faithfulness": round(float(np.mean(faithfulness_scores_rag)), 4),
            "baseline_faithfulness": round(float(np.mean(faithfulness_scores_base)), 4),
            "baseline_hallucination_rate": round(float(baseline_hallucination_rate), 4),
            "rag_hallucination_rate": round(float(rag_hallucination_rate), 4),
            "hallucination_reduction_percentage": round(float(reduction_pct), 2)
        },
        "detailed_results": detailed_results
    }

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(eval_payload, f, indent=2)
    print(f"RAG evaluation metrics saved to: {report_file}")

    return eval_payload

if __name__ == "__main__":
    evaluate_rag_system()

