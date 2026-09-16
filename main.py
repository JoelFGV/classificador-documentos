import pymupdf

REGRAS = {
    "Comprovante": ["comprovante"],
    "Cobranca": ["vencimento", "pague com", "pix"],
    "Nota_Fiscal": ["danfe", "nf-e", "nota fiscal", "nfs-e", "NFe"],
    "Recibo": ["recibo", "recebi", "recebemos"],
}

def extrair_pagina(pdf, page_num, dpi=300):
    pagina = pdf.load_page(page_num - 1)
    textpage = pagina.get_textpage_ocr(language="por", dpi=dpi)
    texto = pagina.get_text(textpage=textpage)
    return texto

def classificar_pagina(texto):
    texto_lower = texto.lower()
    categorias = {}
    
    for categoria, palavras in REGRAS.items():
        score = sum(1 for p in palavras if p in texto_lower)
        if score > 0:
            categorias[categoria] = score
    
    if categorias:
        return max(categorias, key=categorias.get)
    return "Outros"

pdf = pymupdf.open("Documentos_Mesclados.pdf")
for pag_num in range(1, 80):
    texto = extrair_pagina(pdf, pag_num) 
    categoria = classificar_pagina(texto)

    print(f"{pag_num} --> {categoria}")
    
