from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch


def gerar_relatorio_stock(filename, pecas_usadas: dict, mes_referencia: str):
    """
    Gera um relatório de consumo de stock em PDF.

    Args:
        filename: caminho do ficheiro (str) ou buffer (BytesIO)
        pecas_usadas: dict {nome_peca: quantidade} 
        mes_referencia: string descritiva, ex: "Maio/2026"
    """
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elementos = []

    style_header = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.darkblue,
        spaceAfter=12
    )

    elementos.append(Paragraph(f"Relatório de Consumo de Stock — {mes_referencia}", style_header))
    elementos.append(Spacer(1, 0.1 * inch))
    elementos.append(Paragraph("Resumo mensal de peças utilizadas na operação.", styles['Normal']))
    elementos.append(Spacer(1, 0.3 * inch))

    dados_tabela = [["Nome da Peça", "Quantidade Usada"]]
    pecas_ordenadas = dict(sorted(pecas_usadas.items(), key=lambda item: item[1], reverse=True))

    total_pecas = 0
    for peca, qtd in pecas_ordenadas.items():
        dados_tabela.append([peca, str(qtd)])
        total_pecas += qtd

    dados_tabela.append(["TOTAL", str(total_pecas)])

    tabela = Table(dados_tabela, colWidths=[3.5 * inch, 1.5 * inch])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.whitesmoke, colors.lightgrey]),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('LINEABOVE', (0, -1), (-1, -1), 1.5, colors.black),
    ]))
    elementos.append(tabela)

    elementos.append(Spacer(1, 0.5 * inch))
    elementos.append(Paragraph(
        f"<b>Nota:</b> Foram movimentados {len(pecas_usadas)} itens diferentes neste período.",
        styles['Normal']
    ))

    doc.build(elementos)