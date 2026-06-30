import json
import hashlib
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from telemetry import tracer
TRUST_SCORE_SCHEMA = {
    "type": "object",
    "properties": {
        "reliability": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
        },
        "safety": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
        },
        "fairness": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
        },
        "privacy": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
        },
        "transparency": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
        },
        "robustness": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
        }
    },
    "required": [
        "reliability",
        "safety",
        "fairness",
        "privacy",
        "transparency",
        "robustness"
    ]
}

def validate_scores(scores):

    try:
        validate(
            instance=scores,
            schema=TRUST_SCORE_SCHEMA
        )

    except ValidationError as e:
        raise ValueError(
            f"Validation failed: {e.message}"
        )

def normalize_weights(weights):

    total_weight = sum(weights.values())

    if total_weight == 0:
        raise ValueError(
            "Total weight cannot be zero"
        )

    normalized = {
        key: value / total_weight
        for key, value in weights.items()
    }

    return normalized
def calculate_weighted_score(
        scores,
        weights
):

    weighted_score = 0

    for metric in scores:

        weighted_score += (
            scores[metric]
            * weights[metric]
        )

    return round(
        weighted_score,
        2
    )


def determine_risk_level(trust_score):

    if trust_score >= 90:
        return "Low Risk"

    elif trust_score >= 75:
        return "Moderate Risk"

    elif trust_score >= 50:
        return "High Risk"

    return "Critical Risk"

def generate_sha256(evidence_json):

    return hashlib.sha256(
        evidence_json.encode()
    ).hexdigest()

def generate_evidence(
        scores,
        weights,
        trust_score,
        risk_level
):

    evidence = {
        "scores": scores,
        "weights": weights,
        "trust_score": trust_score,
        "risk_level": risk_level
    }

    evidence_json = json.dumps(
        evidence,
        indent=4,
        sort_keys=True
    )

    evidence_hash = generate_sha256(
        evidence_json
    )

    evidence["sha256"] = evidence_hash

    return evidence

def calculate_trust_score(scores, weights):

    with tracer.start_as_current_span("calculate_trust_score"):

        with tracer.start_as_current_span("input_validation") as span:
            validate_scores(scores)
            span.set_attribute("validation.status", "passed")
            span.set_attribute("metrics.count", len(scores))

        with tracer.start_as_current_span("weight_normalization") as span:
            normalized_weights = normalize_weights(weights)
            span.set_attribute("weights.count", len(normalized_weights))
            span.set_attribute("weights.total", sum(normalized_weights.values()))

        with tracer.start_as_current_span("score_calculation") as span:
            trust_score = calculate_weighted_score(
                scores,
                normalized_weights
            )

            risk_level = determine_risk_level(trust_score)

            span.set_attribute("trust.score", trust_score)
            span.set_attribute("risk.level", risk_level)

        with tracer.start_as_current_span("evidence_generation") as span:

            evidence = generate_evidence(
                scores,
                normalized_weights,
                trust_score,
                risk_level
            )

            span.set_attribute("evidence.fields", len(evidence))

        with tracer.start_as_current_span("hash_computation") as span:

            span.set_attribute("hash.algorithm", "SHA-256")
            span.set_attribute("hash.length", len(evidence["sha256"]))

        return evidence

if __name__ == "__main__":

    scores = {
        "reliability": 90,
        "safety": 85,
        "fairness": 80,
        "privacy": 95,
        "transparency": 75,
        "robustness": 88
    }

    weights = {
        "reliability": 0.20,
        "safety": 0.20,
        "fairness": 0.15,
        "privacy": 0.15,
        "transparency": 0.15,
        "robustness": 0.15
    }

    result = calculate_trust_score(
        scores,
        weights
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )