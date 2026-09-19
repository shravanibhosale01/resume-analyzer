"""
Core analysis logic - fully local, no API calls, no paid services.

Uses spaCy instead of raw regex/TF-IDF:
1. PhraseMatcher for skill extraction. Because spaCy tokenizes text
   properly, a short alias like "ts" only matches the standalone token
   "ts" - not a substring buried inside "results" or "tests" the way a
   naive regex search would.
2. Word-vector similarity (nlp(text).similarity()) for the overall
   relevance score. This captures MEANING, not just literal word overlap
   - e.g. "delinquency trends" and "credit risk analytics" will register
   as related even with zero shared words, which TF-IDF cannot do.
3. A confidence-weighted overall score blending #1 and #2, so a JD with
   very few dictionary skills detected doesn't produce a misleading
   100/100 just because "1 out of 1" skills matched.
4. Simple rule-based suggestions generated from the missing-skills list.
"""

import spacy
from spacy.matcher import PhraseMatcher

from skills_data import SKILL_ALIASES

# Below this many detected JD skills, the keyword score is considered
# low-confidence (too small a sample to mean much) and gets blended more
# heavily with semantic similarity instead of being trusted on its own.
FULL_CONFIDENCE_SKILL_COUNT = 5

_nlp = None
_matcher = None


def _load_nlp():
    """
    Lazily load the spaCy model + PhraseMatcher once per process.
    Requires: python -m spacy download en_core_web_md
    (en_core_web_md ships real word vectors, needed for meaningful
    .similarity() scores - the small model does not have these.)
    """
    global _nlp, _matcher
    if _nlp is not None:
        return _nlp, _matcher

    try:
        _nlp = spacy.load("en_core_web_md")
    except OSError as e:
        raise RuntimeError(
            "spaCy model 'en_core_web_md' isn't installed. Run this once in "
            "your activated virtual environment:\n\n"
            "    python -m spacy download en_core_web_md\n"
        ) from e

    _matcher = PhraseMatcher(_nlp.vocab, attr="LOWER")
    for canonical_skill, aliases in SKILL_ALIASES.items():
        patterns = [_nlp.make_doc(alias) for alias in aliases]
        _matcher.add(canonical_skill, patterns)

    return _nlp, _matcher


def find_skills_in_text(nlp, matcher, text: str) -> set:
    """Return the set of canonical skill names found in the given text."""
    doc = nlp(text)
    matches = matcher(doc)
    found = set()
    for match_id, start, end in matches:
        canonical_skill = nlp.vocab.strings[match_id]
        found.add(canonical_skill)
    return found


def compute_semantic_similarity(nlp, resume_text: str, jd_text: str) -> int:
    """
    Word-vector-based semantic similarity between resume and JD, scaled
    to 0-100. Unlike keyword overlap, this can recognize that related
    but differently-worded content (e.g. "risk profiling" vs "delinquency
    analytics") is topically close.
    """
    # Cap length for speed; a few thousand characters is plenty of signal.
    doc1 = nlp(resume_text[:20000])
    doc2 = nlp(jd_text[:20000])
    if not doc1.vector_norm or not doc2.vector_norm:
        return 0
    similarity = doc1.similarity(doc2)
    similarity = max(0.0, min(1.0, similarity))
    return round(similarity * 100)


def generate_suggestions(missing_skills: list, overall_score: int, low_confidence: bool) -> list:
    """Simple rule-based suggestions from missing skills + overall score."""
    suggestions = []

    if missing_skills:
        top_missing = missing_skills[:5]
        suggestions.append(
            f"Add specific, concrete experience with: {', '.join(top_missing)} "
            f"\u2014 mention actual projects or tasks, not just the keyword."
        )

    if low_confidence:
        suggestions.append(
            "This job description only contained a couple of recognizable "
            "skill keywords, so the keyword score alone isn't very reliable "
            "here \u2014 lean more on the semantic similarity score and your "
            "own read of the posting."
        )

    if overall_score < 40:
        suggestions.append(
            "Your resume's overall content is quite different in substance "
            "from this job description \u2014 consider reframing your "
            "experience around the responsibilities this role actually "
            "emphasizes, where that's genuinely accurate."
        )
    elif overall_score < 70:
        suggestions.append(
            "You have decent topical overlap with this role, but tightening "
            "your bullet points to reflect the JD's specific responsibilities "
            "could improve your match further."
        )

    if len(missing_skills) > 8:
        suggestions.append(
            "There's a large skills gap for this specific role \u2014 double-check "
            "this posting matches your target level, or treat missing skills "
            "as a learning roadmap rather than something to fake."
        )

    if not suggestions:
        suggestions.append(
            "Strong match! Focus your remaining edits on quantifying your "
            "achievements (numbers, scale, impact) rather than adding keywords."
        )

    return suggestions


def analyze_resume(resume_text: str, jd_text: str) -> dict:
    """
    Compare resume_text against jd_text using spaCy-based skill matching
    and semantic similarity. Returns a dict the UI can render directly.
    """
    nlp, matcher = _load_nlp()

    resume_skills = find_skills_in_text(nlp, matcher, resume_text)
    jd_skills = find_skills_in_text(nlp, matcher, jd_text)
    jd_skill_count = len(jd_skills)

    matched_skills = sorted(resume_skills & jd_skills)
    missing_skills = sorted(jd_skills - resume_skills)

    keyword_match_score = (
        round(100 * len(matched_skills) / jd_skill_count) if jd_skill_count else 0
    )
    semantic_score = compute_semantic_similarity(nlp, resume_text, jd_text)

    # Confidence scales from 0 (no JD skills detected) to 1 (>= FULL_CONFIDENCE_SKILL_COUNT
    # detected). Low confidence means we lean more on semantic similarity instead of a
    # potentially misleading small-sample keyword ratio (e.g. "1/1 matched" = 100).
    confidence = min(jd_skill_count, FULL_CONFIDENCE_SKILL_COUNT) / FULL_CONFIDENCE_SKILL_COUNT
    low_confidence = jd_skill_count < 3

    overall_score = round(confidence * keyword_match_score + (1 - confidence) * semantic_score)

    if overall_score >= 70:
        relevance = "High"
    elif overall_score >= 40:
        relevance = "Medium"
    else:
        relevance = "Low"

    experience_notes = (
        f"Based on keyword overlap ({len(matched_skills)}/{jd_skill_count or 'N/A'} "
        f"detected skills matched) and semantic similarity ({semantic_score}/100) "
        f"between the full texts, weighted by how many recognizable skills the "
        f"job description contained."
    )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "keyword_match_score": keyword_match_score,
        "semantic_similarity_score": semantic_score,
        "overall_score": overall_score,
        "low_confidence": low_confidence,
        "experience_relevance": relevance,
        "experience_notes": experience_notes,
        "suggestions": generate_suggestions(missing_skills, overall_score, low_confidence),
    }
