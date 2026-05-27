#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enterprise Word to PDF Converter (Fixed for Windows).

Feature:
    - Converts Word (.docx, .doc) to PDF with bookmark/outline support.
    - Uses LibreOffice headless mode with isolated user environments.
    - Robust error handling, timeouts, and logging.
    - Safe for server/cloud concurrency.
    - FIX: Solves 'bootstrap.ini' corruption error on Windows by using valid URIs.

Prerequisites:
    - LibreOffice must be installed (e.g., `apt-get install libreoffice` or Windows installer).
    - Input Word documents MUST use standard 'Heading' styles to generate PDF bookmarks.

Usage:
    python word_to_pdf_v2.py --Word input.docx [-o output.pdf]

Author: Gemini
Date: 2026-02-12
"""

import argparse
import logging
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

# --- Configuration ---
LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'
DEFAULT_TIMEOUT_SEC = 300  # 5 minutes timeout for conversion

# Configure Logging
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("PDFConverter")

class ConversionError(Exception):
    """Base exception for conversion failures."""
    pass

class DependencyError(ConversionError):
    """Raised when external dependencies (LibreOffice) are missing."""
    pass

class PDFConverter:
    """
    A production-grade class to handle Document to PDF conversion.
    Encapsulates environment setup, execution, and cleanup.
    """

    def __init__(self, libreoffice_path: Optional[str] = None):
        """
        Initialize the converter.
        
        Args:
            libreoffice_path: specific path to executable, auto-detects if None.
        """
        self.libreoffice_exec = libreoffice_path or self._detect_libreoffice()
        if not self.libreoffice_exec:
            logger.error("LibreOffice not found on system.")
            logger.info("Please install LibreOffice and ensure 'soffice' is in your PATH.")
            if sys.platform == "win32":
                logger.info("On Windows, add 'C:\\Program Files\\LibreOffice\\program' to system PATH.")
            raise DependencyError("LibreOffice executable not found.")

    def _detect_libreoffice(self) -> Optional[str]:
        """Detects LibreOffice executable across platforms."""
        # Priority list for Linux/macOS/Windows
        candidates = [
            "libreoffice", "soffice", 
            "libreoffice7.6", "libreoffice7.5",
            "/usr/bin/libreoffice", 
            "/usr/bin/soffice"
        ]
        # Check Windows standard paths if on Windows
        if sys.platform == "win32":
            candidates.extend([
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
            ])

        for cmd in candidates:
            if shutil.which(cmd) or Path(cmd).exists():
                return cmd
        return None

    def convert(self, input_path: str, output_path: Optional[str] = None) -> Path:
        """
        Executes the conversion workflow.

        Args:
            input_path: Path to source file.
            output_path: Desired output path.

        Returns:
            Path object of the generated PDF.
        """
        input_file = Path(input_path).resolve()
        
        # 1. Validation
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # 2. Determine Output Path
        final_output_path = self._resolve_output_path(input_file, output_path)
        
        # 3. Create Isolated Environment (Critical for Server/Concurrency)
        # LibreOffice uses a lock file in the user profile. In a server env, 
        # using the default profile causes race conditions. We use a temp dir per run.
        with tempfile.TemporaryDirectory(prefix="lo_convert_") as temp_user_dir:
            self._run_conversion_process(input_file, final_output_path, temp_user_dir)

        return final_output_path

    def _resolve_output_path(self, input_file: Path, output_path: Optional[str]) -> Path:
        """Resolves the destination path, handling directories and defaults."""
        default_name = input_file.stem + ".pdf"
        
        if not output_path:
            return Path.cwd() / default_name
        
        dest = Path(output_path).resolve()
        
        if dest.is_dir():
            return dest / default_name
        
        # Product decision: Fail early if parent dir is missing to avoid confusion.
        if not dest.parent.exists():
            logger.warning(f"Target directory {dest.parent} does not exist. Creating it.")
            dest.parent.mkdir(parents=True, exist_ok=True)
            
        return dest

    def _run_conversion_process(self, input_file: Path, output_file: Path, user_profile_dir: str):
        """
        Constructs and runs the subprocess command.
        """
        # Output directory for LibreOffice (it converts to this dir, keeping filename)
        # We use a temp output dir first to avoid partial writes to final destination
        with tempfile.TemporaryDirectory(prefix="lo_out_") as temp_out_dir:
            
            # --- CRITICAL FIX FOR WINDOWS ---
            # Convert the user profile path to a valid file URI (file:///...)
            # This prevents LibreOffice from crashing with "bootstrap.ini" errors on Windows.
            user_profile_uri = Path(user_profile_dir).as_uri()
            # --------------------------------

            # Construct Command
            cmd = [
                self.libreoffice_exec,
                f"-env:UserInstallation={user_profile_uri}", 
                "--headless",
                "--convert-to", "pdf:writer_pdf_Export", # Explicit filter
                "--outdir", temp_out_dir,
                str(input_file)
            ]

            logger.info(f"Starting conversion: {input_file.name} -> PDF")
            logger.debug(f"Command: {cmd}")

            start_time = time.time()
            try:
                subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=DEFAULT_TIMEOUT_SEC,
                    check=True
                )
            except subprocess.TimeoutExpired:
                logger.error(f"Conversion timed out after {DEFAULT_TIMEOUT_SEC}s.")
                raise ConversionError("Process timed out.")
            except subprocess.CalledProcessError as e:
                # Decode stderr safely to avoid unicode errors on Windows consoles
                err_msg = e.stderr.decode('utf-8', errors='replace') if e.stderr else "Unknown Error"
                logger.error(f"LibreOffice Error Output: {err_msg}")
                raise ConversionError(f"Conversion failed (Exit Code {e.returncode}): {err_msg}")

            # Duration calculation
            duration = time.time() - start_time
            logger.info(f"Conversion process finished in {duration:.2f}s")

            # Locate the result in temp_out_dir
            # LibreOffice keeps the original filename stem but changes extension to .pdf
            expected_temp_file = Path(temp_out_dir) / (input_file.stem + ".pdf")

            if not expected_temp_file.exists():
                raise ConversionError("LibreOffice exited successfully, but PDF was not found. (Check file permissions or password protection)")

            # Move/Rename to final destination
            try:
                if output_file.exists():
                    logger.info(f"Overwriting existing file: {output_file}")
                
                shutil.move(str(expected_temp_file), str(output_file))
                logger.info(f"Success! Output saved to: {output_file}")
            except IOError as e:
                raise ConversionError(f"Failed to save final file: {e}")

def main():
    """CLI Entry Point."""
    parser = argparse.ArgumentParser(
        description="Convert Word to PDF (with Navigation/Bookmarks support)."
    )
    
    parser.add_argument(
        "--Word", 
        dest="input_file",
        required=True, 
        help="Path to input .docx/.doc file."
    )
    
    parser.add_argument(
        "-o", "--output",
        dest="output_file",
        required=False,
        help="Path to output .pdf file. Defaults to current directory."
    )

    args = parser.parse_args()

    try:
        converter = PDFConverter()
        converter.convert(args.input_file, args.output_file)
    except ConversionError as e:
        logger.error(f"Conversion Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()