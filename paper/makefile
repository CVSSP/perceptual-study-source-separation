DOC = paper
OUTPUT = build

FLAGS = --filter=pandoc-crossref \
		--template=icassp_template.latex \
		-s \
		--biblatex \
		-f markdown

all: pdf

pdf: tex
	@pdflatex -halt-on-error -output-directory $(OUTPUT) $(OUTPUT)/$(DOC).tex
	@biber $(OUTPUT)/$(DOC)
	@pdflatex -halt-on-error -output-directory $(OUTPUT) $(OUTPUT)/$(DOC).tex
	@pdflatex -halt-on-error -output-directory $(OUTPUT) $(OUTPUT)/$(DOC).tex
	@biber --output_format=bibtex --output_resolve $(OUTPUT)/$(DOC).bcf

tex:
	@mkdir -p $(OUTPUT)
	@pandoc -o $(OUTPUT)/$(DOC).tex $(FLAGS) $(DOC).md metadata.yaml

clean:
	@rm -rf $(OUTPUT)

read:
	@evince $(OUTPUT)/$(DOC).pdf &
