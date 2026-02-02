"""
Base de conhecimento: extração de texto do prompt_kit.pdf e ficheiros
em docs/knowledge_base para uso com análise de perfil e assistência ao utilizador.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from pypdf import PdfReader


# Caminhos relativos à raiz do projeto (imported/)
_BASE = Path(__file__).resolve().parent.parent.parent
PROMPT_KIT_PDF = _BASE / "incoming" / "caramez" / "prompt kit.pdf"
KNOWLEDGE_BASE_DIR = _BASE / "docs" / "knowledge_base" / "caramez"
KNOWLEDGE_BASE_ROOT = _BASE / "docs" / "knowledge_base"


def _extract_text_from_pdf(file_path: Path) -> str:
    """Extrai texto de um PDF com pypdf."""
    if not file_path.is_file():
        return ""
    try:
        reader = PdfReader(str(file_path))
        parts: List[str] = []
        for page in reader.pages:
            text = page.extract_text() or ""
            parts.append(text)
        return "\n".join(parts).strip()
    except Exception:
        return ""


def _load_text_files(dir_path: Path, extensions: Tuple[str, ...] = (".txt", ".md")) -> str:
    """Carrega e concatena o conteúdo de ficheiros de texto numa pasta."""
    if not dir_path.is_dir():
        return ""
    parts: List[str] = []
    for path in sorted(dir_path.iterdir()):
        if path.suffix.lower() in extensions and path.is_file():
            try:
                content = path.read_text(encoding="utf-8", errors="replace").strip()
                if content:
                    parts.append(f"--- {path.name} ---\n{content}")
            except Exception:
                continue
    return "\n\n".join(parts) if parts else ""


def get_knowledge_base_text(include_prompt_kit: bool = True) -> str:
    """
    Devolve o texto da base de conhecimento para contexto (chat, recomendações).

    - Se include_prompt_kit=True, extrai texto de «prompt kit.pdf» com pypdf.
    - Junta ficheiros .txt e .md em docs/knowledge_base/ (raiz, ex.: PROMPT_CURSOR)
    - Junta ficheiros em docs/knowledge_base/caramez/ (ABOUT, HEADLINE, etc.).

    Útil para enriquecer respostas com base na análise de perfil e nas
    informações da base de conhecimento (360Brew, PROVA, BARM, etc.).
    """
    sections: List[str] = []

    if include_prompt_kit and PROMPT_KIT_PDF.is_file():
        pdf_text = _extract_text_from_pdf(PROMPT_KIT_PDF)
        if pdf_text:
            sections.append("--- Prompt Kit ---\n" + pdf_text)

    root_kb = _load_text_files(KNOWLEDGE_BASE_ROOT)
    if root_kb:
        sections.append(root_kb)

    caramez_kb = _load_text_files(KNOWLEDGE_BASE_DIR)
    if caramez_kb:
        sections.append(caramez_kb)

    return "\n\n".join(sections).strip() if sections else ""
