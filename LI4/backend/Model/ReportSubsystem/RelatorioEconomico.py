from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch


def gerar_relatorio_economico(filename, ordens: int, lucro: float, crescimento: float):
    """
    Gera um relatório económico em PDF.

    Args:
        filename: caminho do ficheiro a criar (str) ou buffer (BytesIO)
        ordens: número total de ordens de serviço
        lucro: lucro total (€)
        crescimento: taxa de crescimento em percentagem
    """
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elementos = []

    style_titulo = ParagraphStyle(
        'TituloCustom',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        textColor=colors.teal
    )

    elementos.append(Paragraph("Relatório de Desempenho Económico", style_titulo))
    elementos.append(Spacer(1, 0.2 * inch))

    dados_tabela = [
        ["Métrica", "Valor Atual"],
        ["Ordens de Serviço", str(ordens)],
        ["Lucro Total", f"{lucro:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")],
        ["Taxa de Crescimento", f"{crescimento:.2f}%"]
    ]

    tabela = Table(dados_tabela, colWidths=[2.5 * inch, 2.5 * inch])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.teal),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elementos.append(tabela)
    elementos.append(Spacer(1, 0.5 * inch))

    status = "positivo" if crescimento > 0 else "negativo"
    comentario = (
        f"<b>Análise Sumária:</b> O presente relatório indica um desempenho {status} "
        f"em relação ao período anterior. Com um total de {ordens} ordens processadas, "
        f"a variação de {crescimento:.2f}% sugere uma "
        f"{'expansão' if crescimento > 0 else 'retração'} nas atividades comerciais."
    )
    elementos.append(Paragraph(comentario, styles['Normal']))

    doc.build(elementos)