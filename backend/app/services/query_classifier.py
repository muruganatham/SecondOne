"""
Query Intent Classifier
-----------------------
Classifies incoming natural language questions into intent buckets
using local regex/keyword rules (zero API calls, ~0ms latency).

Intent buckets:
  general_knowledge  — no DB needed, answer from LLM knowledge
  simple_count       — COUNT(*) style query, no need for schema analysis
  top_performer      — leaderboard / best-student queries, use course_wise_segregations
  comparison         — SREC vs SKCET style, UNION pattern
  trend              — over-time / monthly queries
  assessment         — assessment count / question analysis
  complex            — everything else, full pipeline
"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ClassifiedIntent:
    intent: str                          # one of the buckets above
    confidence: float                    # how confident the rule engine is (0–1)
    table_hint: Optional[str] = None    # table to use (skips schema analysis)
    sql_template: Optional[str] = None  # pre-built SQL template (skips SQL gen)
    metadata: dict = field(default_factory=dict)


class QueryIntentClassifier:
    """
    Rule-based query intent classifier.
    Zero AI calls. Runs in <1ms.
    """

    # ── Signals that always mean DB is needed (override general_knowledge) ──
    DB_CONTEXT_SIGNALS = {
        "skcet", "srec", "kcet", "kongu", "psg", "student", "students",
        "batch", "department", "dept", "college", "section", "enrollment",
        "cgpa", "marks", "score", "rank", "eligible", "placement",
        "performer", "assessment", "attendance", "leaderboard", "my",
        "how many", "list", "show", "find", "top", "who",
    }

    # ── General knowledge patterns ──────────────────────────────────────────
    GENERAL_KNOWLEDGE_PATTERNS = [
        r"\bwhat (is|are|does)\b.*(python|java|c\+\+|sql|array|loop|function|algorithm|data structure|oop|recursion|sorting|linked list|stack|queue|tree|graph)\b",
        r"\bexplain\b.*(concept|algorithm|pattern|principle)",
        r"\bhow (do|does|to)\b.*(work|function|implement|write|code)",
        r"\bdefine\b",
        r"\bdifference between\b.*\band\b",
        r"\bwhat is the (meaning|definition|purpose) of\b",
    ]

    # ── Simple count patterns ────────────────────────────────────────────────
    SIMPLE_COUNT_PATTERNS = [
        r"\bhow many (students?|users?|colleges?|departments?|batches?|sections?)\b",
        r"\btotal (number of|count of)?\s*(students?|users?|colleges?)\b",
        r"\bcount of\b",
    ]

    # ── Top performer patterns ───────────────────────────────────────────────
    TOP_PERFORMER_PATTERNS = [
        r"\b(top|best|highest|leading|rank)\b.*(performer|student|scorer|achiever)",
        r"\bwho (is|are) (the )?(top|best|highest|leading)\b",
        r"\b(top|best)\s+\d*\s*(performer|student|scorer)\b",
        r"\bwho (scored|performed|achieved) (the )?(highest|most|best)\b",
        r"\bleaderboard\b",
        r"\branking\b",
    ]

    # ── Assessment patterns ──────────────────────────────────────────────────
    ASSESSMENT_PATTERNS = [
        r"\bhow many (assessments?|tests?|exams?)\b",
        r"\bassessments?\s+(conducted|done|completed|taken)\b",
        r"\b(assessment|test|exam)\s+count\b",
        r"\bnumber of (assessments?|tests?)\b",
    ]

    # ── Comparison patterns ──────────────────────────────────────────────────
    COMPARISON_PATTERNS = [
        r"\bvs\.?\b",
        r"\bversus\b",
        r"\bcompare\b",
        r"\bbetween\b.*\band\b.*college",
        r"\b(srec|skcet|kcet|kongu|psg)\b.*(vs|versus|compared|against)\b",
    ]

    # ── Trend patterns ───────────────────────────────────────────────────────
    TREND_PATTERNS = [
        r"\b(monthly|weekly|daily|yearly|over time|trend)\b",
        r"\bby (month|week|day|year)\b",
        r"\bprogress (over|across|through)\b",
        r"\bgrowth\b",
    ]

    def classify(self, question: str) -> ClassifiedIntent:
        q = question.lower().strip()

        # Safety guard: if question has DB context signals, never skip the DB
        has_db_context = any(signal in q for signal in self.DB_CONTEXT_SIGNALS)

        # 1. General knowledge (skip DB entirely) — only if NO db context
        if not has_db_context:
            for pattern in self.GENERAL_KNOWLEDGE_PATTERNS:
                if re.search(pattern, q):
                    return ClassifiedIntent(
                        intent="general_knowledge",
                        confidence=0.85,
                        metadata={"reason": f"matched general knowledge pattern: {pattern}"},
                    )

        # 2. Top performer (high confidence — use course_wise_segregations)
        for pattern in self.TOP_PERFORMER_PATTERNS:
            if re.search(pattern, q):
                lang = self._extract_language(q)
                return ClassifiedIntent(
                    intent="top_performer",
                    confidence=0.90,
                    table_hint="course_wise_segregations",
                    metadata={"language": lang, "reason": f"matched top performer pattern"},
                )

        # 3. Assessment count
        for pattern in self.ASSESSMENT_PATTERNS:
            if re.search(pattern, q):
                return ClassifiedIntent(
                    intent="assessment",
                    confidence=0.88,
                    table_hint="_test_data",     # suffix — ai will append college prefix
                    metadata={"reason": "matched assessment pattern"},
                )

        # 4. Simple count
        for pattern in self.SIMPLE_COUNT_PATTERNS:
            if re.search(pattern, q):
                entity = self._extract_count_entity(q)
                return ClassifiedIntent(
                    intent="simple_count",
                    confidence=0.85,
                    metadata={"entity": entity, "reason": "matched simple count pattern"},
                )

        # 5. Comparison
        for pattern in self.COMPARISON_PATTERNS:
            if re.search(pattern, q):
                return ClassifiedIntent(
                    intent="comparison",
                    confidence=0.80,
                    metadata={"reason": "matched comparison pattern"},
                )

        # 6. Trend
        for pattern in self.TREND_PATTERNS:
            if re.search(pattern, q):
                return ClassifiedIntent(
                    intent="trend",
                    confidence=0.80,
                    metadata={"reason": "matched trend pattern"},
                )

        # 7. Default — full pipeline
        return ClassifiedIntent(
            intent="complex",
            confidence=1.0,
            metadata={"reason": "no pattern matched — using full pipeline"},
        )

    def _extract_language(self, q: str) -> Optional[str]:
        lang_map = {
            "java": "java",
            "c\\+\\+": "c++",
            "cpp": "c++",
            "python": "python",
            "c ": "c",
            " c$": "c",
            "html": "html",
            "react": "react",
        }
        for pattern, lang in lang_map.items():
            if re.search(pattern, q):
                return lang
        return None

    def _extract_count_entity(self, q: str) -> str:
        entities = ["students", "users", "colleges", "departments", "batches", "sections"]
        for e in entities:
            if e in q or e.rstrip("s") in q:
                return e
        return "records"

    def should_skip_schema_analysis(self, intent: ClassifiedIntent) -> bool:
        """
        Returns True when we can skip the schema analysis API call.
        Only general_knowledge is safe to skip — for all DB intents we
        still need schema analysis so the SQL gen has full join context.
        The intent hint is injected into the prompt regardless.
        """
        return intent.intent == "general_knowledge"

    def should_skip_db(self, intent: ClassifiedIntent) -> bool:
        """Returns True when we can skip DB entirely."""
        return intent.intent == "general_knowledge"

    def get_intent_hint_for_prompt(self, intent: ClassifiedIntent) -> str:
        """Returns a short hint to inject into the SQL generation prompt."""
        hints = {
            "top_performer":  "HINT: Use `course_wise_segregations` table (pre-computed ranks/scores). Join with `users` for name.",
            "assessment":     "HINT: Query `<college>_<year>_test_data` table. COUNT DISTINCT question_id for assessment count.",
            "simple_count":   "HINT: Use COUNT(*) or COUNT(DISTINCT id). Keep query simple.",
            "comparison":     "HINT: Use UNION ALL to compare across colleges. Alias all columns consistently.",
            "trend":          "HINT: GROUP BY MONTH(created_at) or YEAR(created_at). Use submission_tracks tables.",
            "complex":        "",
        }
        return hints.get(intent.intent, "")


# Singleton
query_classifier = QueryIntentClassifier()
