PDF Address Replacer
Replace a specific three-line address in a PDF statement with a new address while preserving font consistency.

Make sure to update the address strings in fix_statement.py

python fix_statement.py input.pdf output.pdf font.otf

Requirements

Python 3.6+
PyMuPDF 1.25.5: pip install PyMuPDF==1.25.5

Ensure the font file is a valid OTF/TTF

Issues:
- Name/address seem to fall back to helvetica. You can confirm this with pdftool. 

name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
AAAAAB+ABCMonumentGrotesk-Bold       CID TrueType      Identity-H       yes yes yes      5  0
AAAAAC+ABCMonumentGrotesk-Regular    CID TrueType      Identity-H       yes yes yes      6  0
Helvetica                            Type 1            WinAnsi          no  no  no      39  0


- Need to fudge creation date to match statement date and remove modification date
