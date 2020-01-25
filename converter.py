# include requirements
import pandas as pd
from pdflatex import PDFLaTeX
import os


class Converter:
    def __init__(self, filename):
        # Columns:
        # No, Name, Street Address 1, Street Address 2, City, State, Country, Pincode, Phone
        self.clear()
        self.content = pd.read_csv(filename)
        self.create_latex_labels()

    def create_latex_labels(self):
        print("Creating latex labels...")
        begin = "\documentclass[a4paper]{article}\n\\usepackage{fullpage,tikz}\n\\usepackage{framed,multicol}\n\\begin{document}\\begin{multicols}{2}\n"
        end = "\end{multicols}\n\end{document}"
        addresses = ""
        for i in range(len(self.content)):
            address = ( "\\begin{framed}\n"
            + str(self.content.iloc[i][0]) + "\par\n"
            + str(self.content.iloc[i][1]) + "\par\n"
            + str(self.content.iloc[i][2]) + "\par\n"
            + str(self.content.iloc[i][3]) + ", "
            + str(self.content.iloc[i][4]) + ", "
            + str(self.content.iloc[i][6]) + "\par\n"
            + str(self.content.iloc[i][7]) + "\n"
            + "\end{framed}\n" )
            addresses += address
        tex_content = begin + addresses + end

        with open('addresses.tex', 'w+') as f:
            f.write(tex_content)

        print("Latex file written")
        self.convert_to_pdf()

    def convert_to_pdf(self):
        print('Converting to PDF...')
        pdfl = PDFLaTeX.from_texfile('addresses.tex')
        pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)

    def clear(self):
        # delete latex and pdf file before creating again
        print("Clearing previous versions")
        os.remove("addresses.tex")
        os.remove("addresses.pdf")


if __name__ == '__main__':
    # Take parameters like filename using argparse
    filename = 'addresses.csv'
    if os.path.isfile(filename):
        converter = Converter(filename)
    else:
        print("file does not exist")
