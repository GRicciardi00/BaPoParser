from BancopostaParser import BancopostaParser
# Main
# Path to the PDF statement
input_path = "./Data/your_PDF.pdf"
output_name = "./file-name"
bp = BancopostaParser(input_path)
#Preview the contour of the tables for each page
for i in range(bp.num_pages):
    bp.preview_contour(i)
# Export to Excel
bp.export_excel(output_name)
# Filter by date
start_date = "01/08/24"
end_date = "29/08/24"
filtered = bp.filter_by_date(start_date, end_date, path="./Bancoposta/",export=True)
#print(filtered)