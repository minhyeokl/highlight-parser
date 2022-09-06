from PyPDF2 import PdfReader

reader = PdfReader("1.pdf")

for page in reader.pages:
    if "/Annots" in page:
        for annot in page["/Annots"]:
            subtype = annot.get_object()["/Subtype"]
            if subtype == "/Highlight":
                coords = annot.get_object()["/QuadPoints"]
                lines = len(coords) // 8
                for line in range(lines) :
                    x1, y1, x2, y2, x3, y3, x4, y4 = coords[line*8:(line+1)*8]
                    print(x1, y1, x2, y2, x3, y3, x4, y4)