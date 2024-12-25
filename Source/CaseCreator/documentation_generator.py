import os
import inspect
import pydoc
from pathlib import Path
from sphinx.application import Sphinx
from weasyprint import HTML
import importlib.util


class DocumentationGenerator:
    """
    Generates documentation for the project, including HTML and PDF outputs.
    """

    @staticmethod
    def generate_pydoc_html(source_file, output_dir="docs"):
        """
        Generates a raw HTML manual using `pydoc` for the specified source file.
        :param source_file: Path to the Python file for which to generate documentation.
        :param output_dir: Directory where the HTML file will be saved.
        """
        module_name = Path(source_file).stem
        output_path = Path(output_dir) / f"{module_name}.html"
        os.makedirs(output_dir, exist_ok=True)

        # Dynamically import the module from the file path
        try:
            spec = importlib.util.spec_from_file_location(module_name, source_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"Error loading module: {e}")
            return

        # Generate HTML documentation
        with open(output_path, "w") as f:
            f.write(pydoc.HTMLDoc().docmodule(module))

        print(f"HTML documentation generated at: {output_path}")

    @staticmethod
    def generate_sphinx_docs(source_dir, build_dir="docs/_build", format="html"):
        """
        Generates styled documentation using Sphinx.
        :param source_dir: Directory where Sphinx source files are located.
        :param build_dir: Directory where the Sphinx output will be built.
        :param format: Output format (e.g., "html" or "pdf").
        """
        os.makedirs(build_dir, exist_ok=True)

        # Initialize Sphinx app and build docs
        app = Sphinx(
            srcdir=source_dir,
            confdir=source_dir,
            outdir=build_dir,
            doctreedir=os.path.join(build_dir, "doctrees"),
            buildername=format,
        )
        app.build()

        print(f"Sphinx documentation generated in {format} format at: {build_dir}")

    @staticmethod
    def convert_html_to_pdf(html_path, pdf_path):
        """
        Converts an HTML file to a PDF using WeasyPrint.
        :param html_path: Path to the HTML file.
        :param pdf_path: Path to save the output PDF file.
        """
        HTML(html_path).write_pdf(pdf_path)
        print(f"PDF generated at: {pdf_path}")

    @staticmethod
    def generate_manual(source_file, output_dir="docs"):
        """
        Combines all the functionalities to generate an HTML and PDF manual.
        :param source_file: Path to the main Python file for documentation.
        :param output_dir: Directory to save the documentation.
        """
        module_name = Path(source_file).stem
        html_output = Path(output_dir) / f"{module_name}.html"
        pdf_output = Path(output_dir) / f"{module_name}.pdf"
        os.makedirs(output_dir, exist_ok=True)

        # Generate HTML using `pydoc`
        DocumentationGenerator.generate_pydoc_html(source_file, output_dir)

        # Check if HTML was successfully generated
        if not html_output.exists():
            print(f"Error: HTML file {html_output} not found.")
            return

        # Convert HTML to PDF
        DocumentationGenerator.convert_html_to_pdf(html_output, pdf_output)

        print(f"Documentation completed! HTML at {html_output}, PDF at {pdf_output}")

