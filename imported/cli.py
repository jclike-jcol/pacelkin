#!/usr/bin/env python3
"""
LinkedIn Optimizer Assistant - Interface CLI
Comandos para análise e otimização de perfis LinkedIn.

Autor: JC | CloserPace
Versão: 1.0
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import logging

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent))

from core.pdf_parser import parse_linkedin_pdf
from core.analyzer import PerfilAnalyzer

# Setup
console = Console()
logger = logging.getLogger(__name__)


# ==============================================================
# CLI GROUP
# ==============================================================

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    🚀 LinkedIn Optimizer Assistant
    
    Sistema modular para análise e otimização de perfis LinkedIn
    baseado no algoritmo 360Brew.
    
    Exemplos:
    
      $ python cli.py analyze-perfil perfil.pdf
      
      $ python cli.py analyze-perfil perfil.pdf --output relatorio.json
    """
    pass


# ==============================================================
# COMANDO: ANALYZE-PERFIL
# ==============================================================

@cli.command('analyze-perfil')
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option(
    '--output', '-o',
    type=click.Path(),
    help='Caminho para ficheiro de output (JSON ou MD)'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Modo verbose com detalhes de debug'
)
def analyze_perfil(pdf_path: str, output: str, verbose: bool):
    """
    Analisa perfil LinkedIn a partir de PDF exportado.
    
    Extrai dados do PDF, aplica checklist 360Brew e gera score
    com recomendações detalhadas.
    
    Exemplo:
    
        $ python cli.py analyze-perfil perfil.pdf -o relatorio.json
    """
    # Setup logging
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console.print("\n[bold cyan]🚀 LinkedIn Optimizer Assistant[/bold cyan]")
    console.print("[dim]Análise de Perfil 360Brew[/dim]\n")
    
    try:
        # Parsing do PDF
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("📄 A parsear PDF...", total=None)
            perfil = parse_linkedin_pdf(pdf_path)
            progress.update(task, description="✓ PDF parseado")
        
        console.print(f"\n[green]✓[/green] Perfil extraído: [bold]{perfil.nome}[/bold]")
        console.print(f"  📍 {perfil.localizacao}")
        console.print(f"  💼 {len(perfil.experiencias)} experiências")
        console.print(f"  🎯 {len(perfil.competencias)} competências\n")
        
        # Análise
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("🔍 A analisar perfil...", total=None)
            
            # Carrega checklist
            checklist_path = Path(__file__).parent.parent / "config" / "checklists" / "360brew_checklist.yaml"
            analyzer = PerfilAnalyzer(str(checklist_path))
            
            # Analisa
            resultado = analyzer.analyze(perfil)
            progress.update(task, description="✓ Análise completa")
        
        # Display resultados
        _display_resultados(resultado)
        
        # Guarda output se especificado
        if output:
            _save_output(resultado, output)
            console.print(f"\n[green]✓[/green] Resultados guardados em: [cyan]{output}[/cyan]")
        
        # Retorna código baseado no score
        if resultado.percentagem >= 85:
            sys.exit(0)  # Excelente
        elif resultado.percentagem >= 70:
            sys.exit(1)  # Bom
        elif resultado.percentagem >= 50:
            sys.exit(2)  # Regular
        else:
            sys.exit(3)  # Crítico
            
    except FileNotFoundError as e:
        console.print(f"\n[red]✗ Erro:[/red] {e}")
        sys.exit(1)
        
    except Exception as e:
        console.print(f"\n[red]✗ Erro inesperado:[/red] {e}")
        if verbose:
            console.print_exception()
        sys.exit(1)


# ==============================================================
# HELPERS DE DISPLAY
# ==============================================================

def _display_resultados(resultado):
    """Exibe resultados da análise no terminal."""
    
    # Header com score
    score_color = _get_score_color(resultado.percentagem)
    emoji = _get_score_emoji(resultado.categoria_score)
    
    panel = Panel(
        f"[bold {score_color}]{resultado.score_total}/{resultado.score_maximo}[/bold {score_color}] "
        f"([{score_color}]{resultado.percentagem:.1f}%[/{score_color}])\n\n"
        f"{emoji} [bold]{resultado.categoria_score.upper()}[/bold]",
        title="📊 Score Geral",
        border_style=score_color
    )
    console.print(panel)
    
    # Tabela de critérios
    console.print("\n[bold]📋 Análise por Critério:[/bold]\n")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Critério", style="white", width=40)
    table.add_column("Score", justify="right", width=12)
    table.add_column("Status", justify="center", width=8)
    
    for crit in resultado.criterios:
        status = "✓" if crit.passou else "✗"
        status_color = "green" if crit.passou else "red"
        
        table.add_row(
            crit.nome,
            f"{crit.score}/{crit.peso} ({crit.percentagem:.0f}%)",
            f"[{status_color}]{status}[/{status_color}]"
        )
    
    console.print(table)
    
    # Red Flags
    if resultado.red_flags:
        console.print("\n[bold red]⚠️  Red Flags Identificados:[/bold red]\n")
        for rf in resultado.red_flags:
            console.print(f"  [red]•[/red] {rf.nome} (penalização: {rf.penalizacao} pts)")
            for evidencia in rf.evidencias:
                console.print(f"    [dim]→ {evidencia}[/dim]")
    
    # Pontos Fortes
    if resultado.pontos_fortes:
        console.print("\n[bold green]✨ Pontos Fortes:[/bold green]\n")
        for pf in resultado.pontos_fortes:
            console.print(f"  [green]✓[/green] {pf}")
    
    # Oportunidades (top 5)
    if resultado.oportunidades:
        console.print("\n[bold yellow]🎯 Top Oportunidades de Melhoria:[/bold yellow]\n")
        for oport in resultado.oportunidades[:5]:
            prioridade_color = "red" if oport['prioridade'] == 'Alta' else "yellow"
            console.print(f"  [{prioridade_color}]•[/{prioridade_color}] {oport['criterio']} ({oport['score_atual']:.0f}%)")
            for sugestao in oport['sugestoes'][:2]:  # Max 2 sugestões
                console.print(f"    [dim]→ {sugestao}[/dim]")
    
    # Recomendações gerais
    console.print("\n[bold]💡 Próximos Passos:[/bold]\n")
    recomendacoes = _get_recomendacoes(resultado.categoria_score)
    for rec in recomendacoes.get('acoes', [])[:3]:
        console.print(f"  [cyan]1.[/cyan] {rec}")


def _get_score_color(percentagem: float) -> str:
    """Retorna cor baseada no score."""
    if percentagem >= 85:
        return "green"
    elif percentagem >= 70:
        return "yellow"
    elif percentagem >= 50:
        return "orange"
    else:
        return "red"


def _get_score_emoji(categoria: str) -> str:
    """Retorna emoji baseado na categoria."""
    emojis = {
        'excelente': '🟢',
        'bom': '🟡',
        'regular': '🟠',
        'critico': '🔴'
    }
    return emojis.get(categoria, '⚪')


def _get_recomendacoes(categoria: str) -> dict:
    """Carrega recomendações da checklist."""
    # Simplified - em produção carregaria do YAML
    recs = {
        'excelente': {
            'acoes': [
                'Mantém consistência temática nos próximos posts',
                'Analisa quais posts geram mais saves',
                'Experimenta novos formatos mantendo pilares'
            ]
        },
        'bom': {
            'acoes': [
                'Revê headline para incluir pilares mais específicos',
                'Aumenta consistência temática nos posts',
                'Melhora taxa de resposta a comentários'
            ]
        },
        'regular': {
            'acoes': [
                'PRIORIDADE: Define 2-3 pilares temáticos claros',
                'Reescreve secção Sobre alinhada com pilares',
                'Cria calendário editorial focado'
            ]
        },
        'critico': {
            'acoes': [
                'URGENTE: Clarificação de identidade profissional',
                'Reescrever headline e sobre do zero',
                'Estudar perfis benchmark no teu setor'
            ]
        }
    }
    return recs.get(categoria, recs['regular'])


def _save_output(resultado, output_path: str):
    """Guarda resultados em ficheiro."""
    path = Path(output_path)
    
    if path.suffix == '.json':
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(resultado.to_dict(), f, indent=2, ensure_ascii=False)
    
    elif path.suffix in ['.md', '.txt']:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(_generate_markdown_report(resultado))
    
    else:
        # Default: JSON
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(resultado.to_dict(), f, indent=2, ensure_ascii=False)


def _generate_markdown_report(resultado) -> str:
    """Gera relatório em Markdown."""
    emoji = _get_score_emoji(resultado.categoria_score)
    
    md = f"""# Análise de Perfil LinkedIn - 360Brew

**Perfil:** {resultado.perfil.nome}  
**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📊 Score Geral: {resultado.score_total}/{resultado.score_maximo} ({resultado.percentagem:.1f}%)

{emoji} **{resultado.categoria_score.upper()}**

---

## ✅ Pontos Fortes

"""
    
    for pf in resultado.pontos_fortes:
        md += f"- {pf}\n"
    
    md += "\n## 🎯 Oportunidades de Melhoria\n\n"
    
    for oport in resultado.oportunidades[:5]:
        md += f"### {oport['criterio']} ({oport['score_atual']:.0f}%)\n\n"
        md += f"**Prioridade:** {oport['prioridade']}\n\n"
        for sug in oport['sugestoes']:
            md += f"- {sug}\n"
        md += "\n"
    
    if resultado.red_flags:
        md += "## ⚠️ Red Flags\n\n"
        for rf in resultado.red_flags:
            md += f"- **{rf.nome}** (penalização: {rf.penalizacao} pts)\n"
    
    md += "\n---\n\n"
    md += "*Relatório gerado por: LinkedIn Optimizer Assistant v1.0*  \n"
    md += "*Metodologia: 360Brew Algorithm Framework*\n"
    
    return md


# ==============================================================
# COMANDO: INFO
# ==============================================================

@cli.command('info')
def info():
    """Exibe informação sobre o sistema."""
    console.print("\n[bold cyan]LinkedIn Optimizer Assistant[/bold cyan]")
    console.print("[dim]Versão 1.0.0[/dim]\n")
    console.print("📦 [bold]Módulos disponíveis:[/bold]")
    console.print("  ✓ Análise de Perfil (PDF → Score + Recomendações)")
    console.print("  ⏳ Geração de Sobre (PROVA) [em desenvolvimento]")
    console.print("  ⏳ Estratégia Recomendações [em desenvolvimento]")
    console.print("  ⏳ Plano de Ação 90 dias [em desenvolvimento]")
    console.print("  ⏳ Análise de Conteúdo [em desenvolvimento]")
    console.print("\n📚 [bold]Documentação:[/bold]")
    console.print("  README: docs/README.md")
    console.print("  Metodologia: docs/METODOLOGIA_360BREW.md")
    console.print("\n💡 [bold]Para começar:[/bold]")
    console.print("  $ python cli.py analyze-perfil <seu_perfil.pdf>\n")


# ==============================================================
# MAIN
# ==============================================================

if __name__ == '__main__':
    cli()
