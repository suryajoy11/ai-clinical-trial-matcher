from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_text_similarity(patient, trial):
    patient_text = " ".join([
        patient.condition,
        " ".join(patient.diagnoses),
        " ".join(patient.medications),
        " ".join(patient.biomarkers)
    ])

    trial_text = " ".join([
        trial.get("title") or "",
        trial.get("eligibility_criteria") or ""
    ])

    documents = [
        patient_text,
        trial_text
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0]

    return round(
        similarity * 100,
        2
    )