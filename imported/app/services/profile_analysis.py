from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import re

from pypdf import PdfReader


SECTION_TITLES = [
    "Resumo",
    "Experiência",
    "Experiencia",
    "Formação",
    "Education",
    "Certifications",
    "Languages",
    "Principais competências",
]


@dataclass
class ProfileAnalysis:
    score: float
    summary: str
    sections: Dict[str, str]
    recommendations: List[str]
    red_flags: List[str]
    report: List[Dict[str, str | int | float | bool]]


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    parts: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        parts.append(text)
    return "\n".join(parts)


def _find_section_blocks(text: str) -> Dict[str, str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    sections: Dict[str, List[str]] = {}
    current_title = "Geral"
    sections[current_title] = []
    for line in lines:
        if line in SECTION_TITLES:
            current_title = line
            sections[current_title] = []
            continue
        sections[current_title].append(line)
    return {title: "\n".join(content).strip() for title, content in sections.items()}


def _extract_header(lines: List[str]) -> Tuple[str, str, str]:
    name = ""
    headline = ""
    location = ""
    for idx, line in enumerate(lines[:30]):
        if not name and line and len(line.split()) >= 2:
            name = line
            if idx + 1 < len(lines):
                headline = lines[idx + 1]
            if idx + 2 < len(lines):
                location = lines[idx + 2]
            break
    return name, headline, location


def _count_experiences(text: str) -> int:
    return text.count(" - Present") + text.count(" - Atual") + text.count(" - Presente")


def _get_language_pack(lang: str) -> dict:
    packs = {
        "pt-PT": {
            "labels": {
                "name": "Nome detetado",
                "headline": "Headline",
                "location": "Localização",
                "summary": "Resumo",
                "experience": "Experiência",
                "skills": "Competências",
                "languages": "Idiomas",
                "certifications": "Certificações",
            },
            "bool": {"yes": "sim", "no": "não"},
            "recommendations": {
                "headline": "Refinar headline entre 50-120 caracteres com pilares claros.",
                "summary": "Expandir secção Sobre para pelo menos 600 caracteres.",
                "experience": "Adicionar mais experiências com datas claras.",
                "skills": "Adicionar pelo menos 5 competências relevantes.",
                "languages": "Indicar 2+ idiomas e nível.",
                "certifications": "Adicionar certificações relevantes.",
                "links": "Incluir links de contacto ou website.",
                "structure": "Adicionar estrutura com separadores (//) ou bullets.",
                "location": "Confirmar localização no perfil.",
                "metrics": "Incluir resultados quantitativos (%, €, anos, etc.).",
                "emoji": "Evitar emojis na headline para perfil B2B.",
                "consistency": "Garantir consistência entre headline e secção Sobre.",
                "comments": "Promover comentários significativos, não genéricos.",
                "saves": "Criar conteúdo guardável (checklists, frameworks).",
                "dwell": "Aumentar tempo de leitura com narrativa clara.",
            },
            "red_flags": {
                "engagement_bait": "Possível engagement bait (ex.: 'Concordas?', 'Comenta se...').",
                "inconsistent_theme": "Inconsistência temática entre headline e resumo.",
                "generic_ai": "Texto potencialmente genérico ou pouco específico.",
            },
            "criteria": {
                "headline_length": "Headline com 50-120 caracteres",
                "about_length": "Secção Sobre com 600+ caracteres",
                "pillars": "2-4 pilares claros na headline",
                "alignment": "Alinhamento entre headline e Sobre",
                "experience": "3+ experiências com datas",
                "skills": "5+ competências relevantes",
                "languages": "2+ idiomas com nível",
                "certifications": "Certificações relevantes",
                "links": "Links de contacto/website",
                "structure": "Estrutura clara (//, bullets, setas)",
                "metrics": "Resultados quantificados (%, €, anos, etc.)",
                "location": "Localização definida no perfil",
                "emoji": "Headline sem emojis (B2B)",
            },
            "evidence": {
                "headline_length": "Comprimento detetado: {value} caracteres.",
                "about_length": "Comprimento detetado: {value} caracteres.",
                "pillars": "Pilares detetados: {value}.",
                "alignment": "Palavras em comum: {value}.",
                "experience": "Experiências detetadas: {value}.",
                "skills": "Competências detetadas: {value}.",
                "languages": "Idiomas detetados: {value}.",
                "certifications": "Certificações detetadas: {value}.",
                "links": "Links detetados: {value}.",
                "structure": "Estrutura detectada: {value}.",
                "metrics": "Resultados numéricos: {value}.",
                "location": "Localização detetada: {value}.",
                "emoji": "Emojis na headline: {value}.",
            },
        },
        "en": {
            "labels": {
                "name": "Detected name",
                "headline": "Headline",
                "location": "Location",
                "summary": "About",
                "experience": "Experience",
                "skills": "Skills",
                "languages": "Languages",
                "certifications": "Certifications",
            },
            "bool": {"yes": "yes", "no": "no"},
            "recommendations": {
                "headline": "Refine headline to 50-120 chars with clear pillars.",
                "summary": "Expand About section to at least 600 characters.",
                "experience": "Add more experiences with clear dates.",
                "skills": "Add at least 5 relevant skills.",
                "languages": "List 2+ languages with level.",
                "certifications": "Add relevant certifications.",
                "links": "Include contact or website links.",
                "structure": "Add structure with separators (//) or bullets.",
                "location": "Confirm location is set.",
                "metrics": "Include measurable results (%, €, years, etc.).",
                "emoji": "Avoid emojis in headline for B2B profiles.",
                "consistency": "Ensure headline and About are aligned.",
                "comments": "Encourage meaningful comments, not generic.",
                "saves": "Create save-worthy content (checklists, frameworks).",
                "dwell": "Increase dwell time with clear narrative.",
            },
            "red_flags": {
                "engagement_bait": "Possible engagement bait (e.g. 'Agree?', 'Comment if...').",
                "inconsistent_theme": "Theme inconsistency between headline and About.",
                "generic_ai": "Content looks generic or low specificity.",
            },
            "criteria": {
                "headline_length": "Headline length 50-120 characters",
                "about_length": "About section 600+ characters",
                "pillars": "2-4 clear pillars in headline",
                "alignment": "Headline/About alignment",
                "experience": "3+ experiences with dates",
                "skills": "5+ relevant skills",
                "languages": "2+ languages with level",
                "certifications": "Relevant certifications",
                "links": "Contact/website links",
                "structure": "Clear structure (//, bullets, arrows)",
                "metrics": "Quantified results (%, €, years, etc.)",
                "location": "Profile location set",
                "emoji": "Headline without emojis (B2B)",
            },
            "evidence": {
                "headline_length": "Detected length: {value} characters.",
                "about_length": "Detected length: {value} characters.",
                "pillars": "Detected pillars: {value}.",
                "alignment": "Shared keywords: {value}.",
                "experience": "Detected experiences: {value}.",
                "skills": "Detected skills: {value}.",
                "languages": "Detected languages: {value}.",
                "certifications": "Detected certifications: {value}.",
                "links": "Detected links: {value}.",
                "structure": "Structure detected: {value}.",
                "metrics": "Numeric results: {value}.",
                "location": "Location detected: {value}.",
                "emoji": "Emojis in headline: {value}.",
            },
        },
        "es": {
            "labels": {
                "name": "Nombre detectado",
                "headline": "Headline",
                "location": "Ubicación",
                "summary": "Sobre",
                "experience": "Experiencia",
                "skills": "Competencias",
                "languages": "Idiomas",
                "certifications": "Certificaciones",
            },
            "bool": {"yes": "sí", "no": "no"},
            "recommendations": {
                "headline": "Refinar headline entre 50-120 caracteres con pilares claros.",
                "summary": "Ampliar la sección Sobre a 600+ caracteres.",
                "experience": "Añadir más experiencias con fechas claras.",
                "skills": "Añadir al menos 5 competencias relevantes.",
                "languages": "Indicar 2+ idiomas con nivel.",
                "certifications": "Añadir certificaciones relevantes.",
                "links": "Incluir links de contacto o web.",
                "structure": "Añadir estructura con separadores (//) o bullets.",
                "location": "Confirmar ubicación en el perfil.",
                "metrics": "Incluir resultados cuantificables (%, €, años, etc.).",
                "emoji": "Evitar emojis en headline para perfiles B2B.",
                "consistency": "Garantizar coherencia entre headline y Sobre.",
                "comments": "Fomentar comentarios significativos, no genéricos.",
                "saves": "Crear contenido guardable (checklists, frameworks).",
                "dwell": "Aumentar tiempo de lectura con narrativa clara.",
            },
            "red_flags": {
                "engagement_bait": "Posible engagement bait (ej.: '¿Estás de acuerdo?', 'Comenta si...').",
                "inconsistent_theme": "Inconsistencia temática entre headline y Sobre.",
                "generic_ai": "Texto potencialmente genérico o poco específico.",
            },
            "criteria": {
                "headline_length": "Headline con 50-120 caracteres",
                "about_length": "Sección Sobre con 600+ caracteres",
                "pillars": "2-4 pilares claros en headline",
                "alignment": "Alineación headline/Sobre",
                "experience": "3+ experiencias con fechas",
                "skills": "5+ competencias relevantes",
                "languages": "2+ idiomas con nivel",
                "certifications": "Certificaciones relevantes",
                "links": "Links de contacto/web",
                "structure": "Estructura clara (//, bullets, flechas)",
                "metrics": "Resultados cuantificados (%, €, años, etc.)",
                "location": "Ubicación definida en el perfil",
                "emoji": "Headline sin emojis (B2B)",
            },
            "evidence": {
                "headline_length": "Longitud detectada: {value} caracteres.",
                "about_length": "Longitud detectada: {value} caracteres.",
                "pillars": "Pilares detectados: {value}.",
                "alignment": "Palabras en común: {value}.",
                "experience": "Experiencias detectadas: {value}.",
                "skills": "Competencias detectadas: {value}.",
                "languages": "Idiomas detectados: {value}.",
                "certifications": "Certificaciones detectadas: {value}.",
                "links": "Links detectados: {value}.",
                "structure": "Estructura detectada: {value}.",
                "metrics": "Resultados numéricos: {value}.",
                "location": "Ubicación detectada: {value}.",
                "emoji": "Emojis en headline: {value}.",
            },
        },
        "fr": {
            "labels": {
                "name": "Nom détecté",
                "headline": "Headline",
                "location": "Localisation",
                "summary": "À propos",
                "experience": "Expérience",
                "skills": "Compétences",
                "languages": "Langues",
                "certifications": "Certifications",
            },
            "bool": {"yes": "oui", "no": "non"},
            "recommendations": {
                "headline": "Affiner la headline (50-120 caractères) avec des piliers clairs.",
                "summary": "Allonger la section À propos à 600+ caractères.",
                "experience": "Ajouter plus d'expériences avec dates claires.",
                "skills": "Ajouter au moins 5 compétences pertinentes.",
                "languages": "Indiquer 2+ langues avec niveau.",
                "certifications": "Ajouter des certifications pertinentes.",
                "links": "Inclure des liens de contact ou site.",
                "structure": "Ajouter une structure avec séparateurs (//) ou bullets.",
                "location": "Confirmer la localisation du profil.",
                "metrics": "Inclure des résultats quantifiables (%, €, années, etc.).",
                "emoji": "Éviter les emojis dans la headline pour le B2B.",
                "consistency": "Assurer la cohérence entre headline et À propos.",
                "comments": "Favoriser des commentaires significatifs.",
                "saves": "Créer du contenu gardable (checklists, frameworks).",
                "dwell": "Augmenter le temps de lecture avec un récit clair.",
            },
            "red_flags": {
                "engagement_bait": "Engagement bait possible (ex. 'Tu es d'accord ?', 'Commente si...').",
                "inconsistent_theme": "Incohérence thématique entre headline et À propos.",
                "generic_ai": "Texte trop générique ou peu spécifique.",
            },
            "criteria": {
                "headline_length": "Headline de 50-120 caractères",
                "about_length": "Section À propos 600+ caractères",
                "pillars": "2-4 piliers clairs dans la headline",
                "alignment": "Alignement headline/À propos",
                "experience": "3+ expériences avec dates",
                "skills": "5+ compétences pertinentes",
                "languages": "2+ langues avec niveau",
                "certifications": "Certifications pertinentes",
                "links": "Liens de contact/site",
                "structure": "Structure claire (//, bullets, flèches)",
                "metrics": "Résultats quantifiés (%, €, années, etc.)",
                "location": "Localisation du profil définie",
                "emoji": "Headline sans emojis (B2B)",
            },
            "evidence": {
                "headline_length": "Longueur détectée : {value} caractères.",
                "about_length": "Longueur détectée : {value} caractères.",
                "pillars": "Piliers détectés : {value}.",
                "alignment": "Mots communs : {value}.",
                "experience": "Expériences détectées : {value}.",
                "skills": "Compétences détectées : {value}.",
                "languages": "Langues détectées : {value}.",
                "certifications": "Certifications détectées : {value}.",
                "links": "Liens détectés : {value}.",
                "structure": "Structure détectée : {value}.",
                "metrics": "Résultats numériques : {value}.",
                "location": "Localisation détectée : {value}.",
                "emoji": "Emojis dans la headline : {value}.",
            },
        },
        "de": {
            "labels": {
                "name": "Erkannter Name",
                "headline": "Headline",
                "location": "Ort",
                "summary": "Über mich",
                "experience": "Erfahrung",
                "skills": "Skills",
                "languages": "Sprachen",
                "certifications": "Zertifizierungen",
            },
            "bool": {"yes": "ja", "no": "nein"},
            "recommendations": {
                "headline": "Headline auf 50-120 Zeichen mit klaren Säulen optimieren.",
                "summary": "Über mich auf mindestens 600 Zeichen erweitern.",
                "experience": "Mehr Erfahrungen mit klaren Daten hinzufügen.",
                "skills": "Mindestens 5 relevante Skills hinzufügen.",
                "languages": "2+ Sprachen mit Level angeben.",
                "certifications": "Relevante Zertifizierungen hinzufügen.",
                "links": "Kontakt- oder Website-Links hinzufügen.",
                "structure": "Struktur mit Trennern (//) oder Bullets hinzufügen.",
                "location": "Profil-Standort bestätigen.",
                "metrics": "Messbare Ergebnisse einfügen (%, €, Jahre, etc.).",
                "emoji": "Emojis in der Headline für B2B vermeiden.",
                "consistency": "Headline und Über mich konsistent halten.",
                "comments": "Sinnvolle Kommentare fördern.",
                "saves": "Speicherwürdige Inhalte erstellen (Checklists, Frameworks).",
                "dwell": "Lesezeit durch klare Struktur erhöhen.",
            },
            "red_flags": {
                "engagement_bait": "Mögliches Engagement-Baiting (z.B. 'Stimmst du zu?', 'Kommentiere wenn...').",
                "inconsistent_theme": "Thematische Inkonsistenz zwischen Headline und Über mich.",
                "generic_ai": "Text wirkt zu generisch oder unspezifisch.",
            },
            "criteria": {
                "headline_length": "Headline 50-120 Zeichen",
                "about_length": "Über mich 600+ Zeichen",
                "pillars": "2-4 klare Säulen in der Headline",
                "alignment": "Headline/Über mich konsistent",
                "experience": "3+ Erfahrungen mit Daten",
                "skills": "5+ relevante Skills",
                "languages": "2+ Sprachen mit Level",
                "certifications": "Relevante Zertifizierungen",
                "links": "Kontakt-/Website-Links",
                "structure": "Klare Struktur (//, Bullets, Pfeile)",
                "metrics": "Messbare Ergebnisse (%, €, Jahre, etc.)",
                "location": "Profil-Standort gesetzt",
                "emoji": "Headline ohne Emojis (B2B)",
            },
            "evidence": {
                "headline_length": "Ermittelte Länge: {value} Zeichen.",
                "about_length": "Ermittelte Länge: {value} Zeichen.",
                "pillars": "Ermittelte Säulen: {value}.",
                "alignment": "Gemeinsame Keywords: {value}.",
                "experience": "Ermittelte Erfahrungen: {value}.",
                "skills": "Ermittelte Skills: {value}.",
                "languages": "Ermittelte Sprachen: {value}.",
                "certifications": "Ermittelte Zertifizierungen: {value}.",
                "links": "Ermittelte Links: {value}.",
                "structure": "Struktur erkannt: {value}.",
                "metrics": "Numerische Ergebnisse: {value}.",
                "location": "Standort erkannt: {value}.",
                "emoji": "Emojis in der Headline: {value}.",
            },
        },
    }
    return packs.get(lang, packs["pt-PT"])


def _has_emoji(text: str) -> bool:
    return bool(re.search(r"[\U00010000-\U0010ffff]", text))


def _count_non_empty_lines(text: str) -> int:
    return len([line for line in text.splitlines() if line.strip()])


def _tokenize_keywords(text: str) -> List[str]:
    words = re.findall(r"[A-Za-zÀ-ÿ0-9]{4,}", text.lower())
    blacklist = {"linkedin", "sobre", "resumo", "experiencia", "experiência", "formacao", "formação"}
    return [w for w in words if w not in blacklist]


def _is_generic(text: str) -> bool:
    return len(set(_tokenize_keywords(text))) < 8


def _count_pillars(headline: str) -> int:
    if not headline:
        return 0
    separators = ["|", "•", "·", "-", "—", "–"]
    for sep in separators:
        if sep in headline:
            parts = [p.strip() for p in headline.split(sep) if p.strip()]
            return len(parts)
    return 1


def analyze_profile(file_path: str, lang: str = "pt-PT") -> ProfileAnalysis:
    text = extract_text_from_pdf(file_path)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    name, headline, location = _extract_header(lines)
    sections = _find_section_blocks(text)

    summary_section = sections.get("Resumo", "") or sections.get("Summary", "")
    experiences_section = sections.get("Experiência", "") or sections.get("Experiencia", "")
    skills_section = sections.get("Principais competências", "")
    languages_section = sections.get("Languages", "")
    certifications_section = sections.get("Certifications", "")

    pack = _get_language_pack(lang)
    labels = pack["labels"]
    recs_text = pack["recommendations"]
    red_flags_text = pack["red_flags"]

    score = 0.0
    recommendations: List[str] = []
    red_flags: List[str] = []
    report: List[Dict[str, str | int | float | bool]] = []

    headline_len = len(headline)
    headline_pass = 50 <= headline_len <= 120
    report.append(
        {
            "id": "headline_length",
            "label": pack["criteria"]["headline_length"],
            "weight": 15,
            "passed": headline_pass,
            "score": 15 if headline_pass else 0,
            "evidence": pack["evidence"]["headline_length"].format(value=headline_len),
        }
    )
    if headline_pass:
        score += 15
    else:
        recommendations.append(recs_text["headline"])

    summary_len = len(summary_section)
    summary_pass = summary_len >= 600
    report.append(
        {
            "id": "about_length",
            "label": pack["criteria"]["about_length"],
            "weight": 20,
            "passed": summary_pass,
            "score": 20 if summary_pass else 0,
            "evidence": pack["evidence"]["about_length"].format(value=summary_len),
        }
    )
    if summary_pass:
        score += 20
    else:
        recommendations.append(recs_text["summary"])

    experiences_count = _count_experiences(experiences_section)
    experience_pass = experiences_count >= 3
    report.append(
        {
            "id": "experience",
            "label": pack["criteria"]["experience"],
            "weight": 10,
            "passed": experience_pass,
            "score": 10 if experience_pass else 0,
            "evidence": pack["evidence"]["experience"].format(value=experiences_count),
        }
    )
    if experience_pass:
        score += 10
    else:
        recommendations.append(recs_text["experience"])

    skills_count = _count_non_empty_lines(skills_section)
    skills_pass = skills_count >= 5
    report.append(
        {
            "id": "skills",
            "label": pack["criteria"]["skills"],
            "weight": 5,
            "passed": skills_pass,
            "score": 5 if skills_pass else 0,
            "evidence": pack["evidence"]["skills"].format(value=skills_count),
        }
    )
    if skills_pass:
        score += 5
    else:
        recommendations.append(recs_text["skills"])

    languages_count = _count_non_empty_lines(languages_section)
    languages_pass = languages_count >= 2
    report.append(
        {
            "id": "languages",
            "label": pack["criteria"]["languages"],
            "weight": 5,
            "passed": languages_pass,
            "score": 5 if languages_pass else 0,
            "evidence": pack["evidence"]["languages"].format(value=languages_count),
        }
    )
    if languages_pass:
        score += 5
    else:
        recommendations.append(recs_text["languages"])

    certifications_count = _count_non_empty_lines(certifications_section)
    certifications_pass = certifications_count >= 1
    report.append(
        {
            "id": "certifications",
            "label": pack["criteria"]["certifications"],
            "weight": 5,
            "passed": certifications_pass,
            "score": 5 if certifications_pass else 0,
            "evidence": pack["evidence"]["certifications"].format(value=certifications_count),
        }
    )
    if certifications_pass:
        score += 5
    else:
        recommendations.append(recs_text["certifications"])

    links_found = "www.linkedin.com" in text or "http" in text
    report.append(
        {
            "id": "links",
            "label": pack["criteria"]["links"],
            "weight": 5,
            "passed": links_found,
            "score": 5 if links_found else 0,
            "evidence": pack["evidence"]["links"].format(
                value=pack["bool"]["yes"] if links_found else pack["bool"]["no"]
            ),
        }
    )
    if links_found:
        score += 5
    else:
        recommendations.append(recs_text["links"])

    structure_found = "//" in summary_section or "→" in summary_section or "•" in summary_section
    report.append(
        {
            "id": "structure",
            "label": pack["criteria"]["structure"],
            "weight": 5,
            "passed": structure_found,
            "score": 5 if structure_found else 0,
            "evidence": pack["evidence"]["structure"].format(
                value=pack["bool"]["yes"] if structure_found else pack["bool"]["no"]
            ),
        }
    )
    if structure_found:
        score += 5
    else:
        recommendations.append(recs_text["structure"])

    location_pass = bool(location)
    report.append(
        {
            "id": "location",
            "label": pack["criteria"]["location"],
            "weight": 0,
            "passed": location_pass,
            "score": 0,
            "evidence": pack["evidence"]["location"].format(
                value=location if location_pass else "N/D"
            ),
        }
    )
    if not location_pass:
        recommendations.append(recs_text["location"])

    metrics_found = bool(re.search(r"\d", summary_section))
    report.append(
        {
            "id": "metrics",
            "label": pack["criteria"]["metrics"],
            "weight": 10,
            "passed": metrics_found,
            "score": 10 if metrics_found else 0,
            "evidence": pack["evidence"]["metrics"].format(
                value=pack["bool"]["yes"] if metrics_found else pack["bool"]["no"]
            ),
        }
    )
    if metrics_found:
        score += 10
    else:
        recommendations.append(recs_text["metrics"])

    emoji_found = _has_emoji(headline) if headline else False
    report.append(
        {
            "id": "emoji",
            "label": pack["criteria"]["emoji"],
            "weight": 0,
            "passed": not emoji_found,
            "score": 0,
            "evidence": pack["evidence"]["emoji"].format(
                value=pack["bool"]["yes"] if emoji_found else pack["bool"]["no"]
            ),
        }
    )
    if not headline or emoji_found:
        recommendations.append(recs_text["emoji"])

    pillar_count = _count_pillars(headline)
    pillars_pass = 2 <= pillar_count <= 4
    report.append(
        {
            "id": "pillars",
            "label": pack["criteria"]["pillars"],
            "weight": 10,
            "passed": pillars_pass,
            "score": 10 if pillars_pass else 0,
            "evidence": pack["evidence"]["pillars"].format(value=pillar_count),
        }
    )
    if pillars_pass:
        score += 10
    else:
        recommendations.append(recs_text["consistency"])

    headline_keywords = set(_tokenize_keywords(headline))
    summary_keywords = set(_tokenize_keywords(summary_section))
    overlap = headline_keywords.intersection(summary_keywords)
    alignment_pass = len(overlap) >= 2
    report.append(
        {
            "id": "alignment",
            "label": pack["criteria"]["alignment"],
            "weight": 10,
            "passed": alignment_pass,
            "score": 10 if alignment_pass else 0,
            "evidence": pack["evidence"]["alignment"].format(value=len(overlap)),
        }
    )
    if alignment_pass:
        score += 10
    else:
        red_flags.append(red_flags_text["inconsistent_theme"])
        recommendations.append(recs_text["consistency"])

    engagement_bait_patterns = [
        r"concordas\??",
        r"comenta se",
        r"tag",
        r"marca alguém",
        r"opina",
        r"agree\??",
        r"comment if",
    ]
    bait_found = any(re.search(pat, summary_section.lower()) for pat in engagement_bait_patterns)
    if bait_found:
        red_flags.append(red_flags_text["engagement_bait"])
        recommendations.append(recs_text["comments"])

    if _is_generic(summary_section):
        red_flags.append(red_flags_text["generic_ai"])
        recommendations.append(recs_text["dwell"])
        recommendations.append(recs_text["saves"])

    score = min(100.0, round(score, 1))

    summary_lines = [
        f"{labels['name']}: {name or 'N/D'}",
        f"{labels['headline']}: {headline or 'N/D'}",
        f"{labels['location']}: {location or 'N/D'}",
        f"{labels['summary']}: {summary_len} chars",
        f"{labels['experience']}: {experiences_count}",
        f"{labels['skills']}: {skills_count}",
        f"{labels['languages']}: {languages_count}",
        f"{labels['certifications']}: {certifications_count}",
    ]
    return ProfileAnalysis(
        score=score,
        summary=" | ".join(summary_lines),
        sections=sections,
        recommendations=list(dict.fromkeys(recommendations))[:6],
        red_flags=red_flags,
        report=report,
    )
