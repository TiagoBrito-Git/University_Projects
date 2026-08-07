from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from Model.PaymentsSubsystem.Fatura import Fatura

# ── Gerador de PDF ──────────────────────────────────────────────────────────
ESTADO_CORES = {
    "paga":      colors.HexColor("#27ae60"),
    "pendente":  colors.HexColor("#e67e22"),
    "cancelada": colors.HexColor("#e74c3c"),
}

ESTADO_LABELS = {
    "paga":      "PAGA",
    "pendente":  "PENDENTE",
    "cancelada": "CANCELADA",
}

PAGAMENTO_ICONS = {
    "dinheiro":      "💵 Dinheiro",
    "cartão":        "💳 Cartão",
    "transferência": "🏦 Transferência",
}


def gerar_pdf_fatura(fatura: Fatura, caminho_saida = "fatura.pdf"):
    """Gera o PDF da fatura.
    
    `caminho_saida` pode ser:
      - str  → escreve o PDF no caminho indicado
      - io.BytesIO → escreve o PDF no buffer (para servir via HTTP sem tocar em disco)
    """
    doc = SimpleDocTemplate(
        caminho_saida,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()
    cor_primaria = colors.HexColor("#2c3e50")
    cor_secundaria = colors.HexColor("#ecf0f1")
    cor_estado = ESTADO_CORES.get(fatura.estado, colors.grey)

    style_titulo = ParagraphStyle("titulo", fontSize=26, textColor=colors.white,
                                  alignment=TA_LEFT, fontName="Helvetica-Bold", leading=30)
    style_subtitulo = ParagraphStyle("subtitulo", fontSize=10, textColor=colors.HexColor("#bdc3c7"),
                                     alignment=TA_LEFT, fontName="Helvetica")
    style_label = ParagraphStyle("label", fontSize=8, textColor=colors.HexColor("#7f8c8d"),
                                 fontName="Helvetica-Bold", spaceAfter=2)
    style_valor = ParagraphStyle("valor", fontSize=10, textColor=cor_primaria,
                                 fontName="Helvetica")
    style_total_label = ParagraphStyle("total_label", fontSize=12, textColor=colors.white,
                                       fontName="Helvetica-Bold", alignment=TA_LEFT)
    style_total_valor = ParagraphStyle("total_valor", fontSize=16, textColor=colors.white,
                                       fontName="Helvetica-Bold", alignment=TA_RIGHT)
    style_rodape = ParagraphStyle("rodape", fontSize=8, textColor=colors.grey,
                                  alignment=TA_CENTER, fontName="Helvetica")

    story = []

    # ── Cabeçalho colorido ──────────────────────────────────────────────────
    header_data = [[
        Paragraph("FATURA", style_titulo),
        Paragraph(f"N.º {fatura.numero}", ParagraphStyle(
            "num", fontSize=14, textColor=colors.HexColor("#bdc3c7"),
            fontName="Helvetica-Bold", alignment=TA_RIGHT)),
    ]]
    header_table = Table(header_data, colWidths=[10*cm, 7*cm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), cor_primaria),
        ("TOPPADDING",    (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING",   (0, 0), (-1, -1), 16),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 16),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.4*cm))

    # ── Sub-cabeçalho: data + estado + OS ──────────────────────────────────
    estado_label = ESTADO_LABELS.get(fatura.estado, fatura.estado)
    data_str = fatura.data.strftime("%d/%m/%Y")

    info_data = [[
        Paragraph(f"<b>Data:</b> {data_str}", style_valor),
        Paragraph(f"<b>Ordem de Serviço:</b> #{fatura.id_os}", style_valor),
        Paragraph(f'<font color="{cor_estado.hexval()}" size="11"><b>{estado_label}</b></font>',
                  ParagraphStyle("estado", fontSize=11, alignment=TA_RIGHT,
                                 fontName="Helvetica-Bold")),
    ]]
    info_table = Table(info_data, colWidths=[6*cm, 6*cm, 5*cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), cor_secundaria),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [4, 4, 4, 4]),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.8*cm))

    # ── Tabela de valores ───────────────────────────────────────────────────
    story.append(Paragraph("RESUMO DE VALORES", ParagraphStyle(
        "sec", fontSize=9, textColor=colors.HexColor("#7f8c8d"),
        fontName="Helvetica-Bold", spaceAfter=6)))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dfe6e9")))
    story.append(Spacer(1, 0.3*cm))

    # ── Tabela de peças (detalhe) ───────────────────────────────────────────
    tem_pecas = bool(getattr(fatura, "pecas", {}))

    if tem_pecas:
        pecas_data = [["Peça / Material", "Qtd", "Preço Unit.", "Subtotal"]]
        for id_peca, dados in fatura.pecas.items():
            nome = dados.get("nome", f"Peça #{id_peca}")
            qty = dados["quantidade"]
            preco = dados["preco_unitario"]
            subtotal = qty * preco
            pecas_data.append([nome, str(qty), f"{preco:.2f} €", f"{subtotal:.2f} €"])
        pecas_data.append(["Subtotal — Peças", "", "", f"{fatura.sub_total_pecas:.2f} €"])

        idx_subtotal = len(pecas_data) - 1

        pecas_table = Table(pecas_data, colWidths=[8*cm, 1.5*cm, 3*cm, 4.5*cm])
        pecas_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), cor_primaria),
            ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",   (0, 0), (-1, 0), 9),
            ("ALIGN",  (1, 0), (-1, -1), "RIGHT"),
            ("FONTNAME",   (0, 1), (-1, idx_subtotal - 1), "Helvetica"),
            ("FONTSIZE",   (0, 1), (-1, idx_subtotal - 1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, idx_subtotal - 1), [colors.white, cor_secundaria]),
            ("BACKGROUND", (0, idx_subtotal), (-1, idx_subtotal), colors.HexColor("#dfe6e9")),
            ("FONTNAME",   (0, idx_subtotal), (-1, idx_subtotal), "Helvetica-Bold"),
            ("FONTSIZE",   (0, idx_subtotal), (-1, idx_subtotal), 9),
            ("LINEABOVE",  (0, idx_subtotal), (-1, idx_subtotal), 0.8, colors.HexColor("#bdc3c7")),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 12),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
            ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.HexColor("#2c3e50")),
        ]))
        story.append(pecas_table)
        story.append(Spacer(1, 0.3*cm))
    else:
        linha = Table([["Subtotal — Peças", f"{fatura.sub_total_pecas:.2f} €"]], colWidths=[13*cm, 4*cm])
        linha.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), cor_secundaria),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN",  (1, 0), (-1, -1), "RIGHT"),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 12),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ]))
        story.append(linha)
        story.append(Spacer(1, 0.3*cm))

    # ── Mão de obra ─────────────────────────────────────────────────────────
    mao_obra_table = Table([["Mão de Obra", f"{fatura.sub_total_mao_obra:.2f} €"]], colWidths=[13*cm, 4*cm])
    mao_obra_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN",  (1, 0), (-1, -1), "RIGHT"),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#dfe6e9")),
    ]))
    story.append(mao_obra_table)
    story.append(Spacer(1, 0.4*cm))

    # ── Linha de total ──────────────────────────────────────────────────────
    total_data = [[
        Paragraph("TOTAL", style_total_label),
        Paragraph(f"{fatura.total:.2f} €", style_total_valor),
    ]]
    total_table = Table(total_data, colWidths=[13*cm, 4*cm])
    total_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), cor_primaria),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(total_table)
    story.append(Spacer(1, 0.8*cm))

    # ── Método de pagamento ─────────────────────────────────────────────────
    pagamento_label = PAGAMENTO_ICONS.get(fatura.tipo_pagamento, fatura.tipo_pagamento.capitalize())
    pag_data = [[
        Paragraph("MÉTODO DE PAGAMENTO", ParagraphStyle(
            "pg_label", fontSize=8, textColor=colors.HexColor("#7f8c8d"),
            fontName="Helvetica-Bold")),
        Paragraph(pagamento_label, ParagraphStyle(
            "pg_valor", fontSize=10, textColor=cor_primaria,
            fontName="Helvetica", alignment=TA_RIGHT)),
    ]]
    pag_table = Table(pag_data, colWidths=[10*cm, 7*cm])
    pag_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), cor_secundaria),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(pag_table)

    # ── Rodapé ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.5*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dfe6e9")))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        f"Documento gerado automaticamente · Fatura ID {fatura.id} · OS #{fatura.id_os}",
        style_rodape))

    doc.build(story)
    if isinstance(caminho_saida, str):
        print(f"PDF gerado com sucesso: {caminho_saida}")


