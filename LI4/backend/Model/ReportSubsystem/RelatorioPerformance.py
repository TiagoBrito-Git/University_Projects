from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch


def gerar_relatorio_performance(
    filename,
    tempo_medio: float,
    diff_tempo: float,
    pct_nao_avancadas: float,
    diff_nao_avancadas: float,
    num_ordens: int,
    diff_ordens: float,
):
    """
    Gera um relatório de performance operacional em PDF.

    Args:
        filename: caminho do ficheiro (str) ou buffer (BytesIO)
        tempo_medio: tempo médio de execução em horas
        diff_tempo: variação percentual do tempo médio vs. período anterior
        pct_nao_avancadas: % de ordens paradas/não avançadas
        diff_nao_avancadas: variação percentual de ordens paradas
        num_ordens: total de ordens de serviço
        diff_ordens: variação percentual do total de ordens
    """
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elementos = []

    titulo_style = ParagraphStyle(
        'Titulo', parent=styles['Heading1'],
        fontSize=20, textColor=colors.navy, spaceAfter=20
    )
    elementos.append(Paragraph("Dashboard de Performance Operacional", titulo_style))

    def _fmt(valor):
        prefixo = "+" if valor > 0 else ""
        return f"{prefixo}{valor:.1f}%"

    # Cor invertida para "não avançadas": subir é mau
    cor_tempo = colors.green if diff_tempo < 0 else colors.red
    cor_nao_avanc = colors.red if diff_nao_avancadas > 0 else colors.green
    cor_ordens = colors.green if diff_ordens > 0 else colors.red

    dados_kpi = [
        ["Métrica de Performance", "Valor Atual", "vs. Período Anterior"],
        ["Tempo Médio de Execução", f"{tempo_medio:.1f}h", _fmt(diff_tempo)],
        ["Ordens Não Avançadas", f"{pct_nao_avancadas:.1f}%", _fmt(diff_nao_avancadas)],
        ["Total de Ordens de Serviço", str(num_ordens), _fmt(diff_ordens)],
    ]

    tabela = Table(dados_kpi, colWidths=[2.5 * inch, 1.5 * inch, 1.5 * inch])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (2, 1), (2, 1), cor_tempo),
        ('TEXTCOLOR', (2, 2), (2, 2), cor_nao_avanc),
        ('TEXTCOLOR', (2, 3), (2, 3), cor_ordens),
    ]))
    elementos.append(tabela)

    elementos.append(Spacer(1, 0.4 * inch))
    elementos.append(Paragraph("<b>Análise de Eficiência:</b>", styles['Heading3']))

    tendencia = "melhoria" if diff_tempo < 0 and diff_nao_avancadas < 0 else "necessidade de revisão"
    obs = f"A análise dos dados indica uma <b>{tendencia}</b> nos processos operacionais."
    elementos.append(Paragraph(obs, styles['Normal']))

    doc.build(elementos)