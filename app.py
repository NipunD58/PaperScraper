import os
import logging
import requests
import tkinter as tk
from tkinter import filedialog, ttk
import threading
from pathlib import Path
from typing import Optional, List, Dict
import concurrent.futures
from url_templates import (
    SUBJECT_VARIATIONS,
    BASE_URL_PATTERNS,
    SUBJECT_SPECIFIC_PATTERNS
)

class CBSEPaperDownloader:
    def __init__(self, base_dir: str = "Paper"):
        self.base_dir = Path(base_dir)
        self.subjects = SUBJECT_VARIATIONS
        self.academic_years = [f"{year}_{str(year+1)[-2:]}" for year in range(2014, 2025)]
        self.base_url = "https://cbseacademic.nic.in/web_material/SQP"

        self.logger = self.setup_logging()
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def setup_logging(self) -> logging.Logger:

        logger = logging.getLogger('CBSEPaperDownloader')
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('paper_downloader.log')
        
        console_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.DEBUG)

        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger

    def get_paper_url(self, subject: str, academic_year: str) -> Optional[str]:

        try:
            url_patterns = []
            subject_variations = self.subjects[subject]

            if subject in SUBJECT_SPECIFIC_PATTERNS:
                url_patterns.extend([
                    f"{self.base_url}/{pattern.format(year=academic_year)}"
                    for pattern in SUBJECT_SPECIFIC_PATTERNS[subject]
                ])

            for subject_name in subject_variations:
                for pattern in BASE_URL_PATTERNS:
                    url_patterns.append(
                        f"{self.base_url}/{pattern.format(year=academic_year, subject=subject_name)}"
                    )

            for url in url_patterns:
                try:
                    response = self.session.head(url, timeout=10)
                    if response.status_code == 200:
                        self.logger.info(f"Found valid URL: {url}")
                        return url
                except requests.exceptions.RequestException as e:
                    self.logger.debug(f"Failed to access URL {url}: {str(e)}")
                    continue

            self.logger.warning(f"No valid URL found for {subject} {academic_year}")
            return None

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error checking URLs for {subject} {academic_year}: {str(e)}")
            return None

    def setup_logging(self) -> logging.Logger:
        logger = logging.getLogger('CBSEPaperDownloader')
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('paper_downloader.log')
        
        console_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.DEBUG)

        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger

    def download_file(self, url: str, save_path: Path) -> bool:
        try:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.logger.info(f"Successfully downloaded: {save_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error downloading {url}: {str(e)}")
            return False

    def download_papers_for_year(self, subject: str, academic_year: str) -> None:
        paper_url = self.get_paper_url(subject, academic_year)
        if not paper_url:
            self.logger.warning(f"No paper found for {subject} {academic_year}")
            return

        year = academic_year.split('_')[0]
        
        filename = f"sample paper_{subject}_{academic_year}.pdf"
        filename = self.sanitize_filename(filename)
        
        save_path = self.base_dir / subject / f"{year}samplepaper" / filename
        
        if save_path.exists():
            self.logger.info(f"File already exists: {save_path}")
            return

        self.download_file(paper_url, save_path)

    def download_all_papers(self) -> None:
        self.logger.info("Starting download of all papers")

        self.base_dir.mkdir(parents=True, exist_ok=True)
        

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for subject in self.subjects.keys():
                for year in self.academic_years:
                    futures.append(
                        executor.submit(
                            self.download_papers_for_year, 
                            subject, 
                            year
                        )
                    )
            
            concurrent.futures.wait(futures)
        
        self.logger.info("All downloads completed")

    def sanitize_filename(self, filename: str) -> str:
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename



class DownloaderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CBSE Sample Paper Downloader")
        self.root.geometry("600x400")

        self.dir_frame = ttk.Frame(self.root, padding="10")
        self.dir_frame.pack(fill=tk.X)
        
        self.dir_label = ttk.Label(self.dir_frame, text="Download Location:")
        self.dir_label.pack(side=tk.LEFT)
        
        self.dir_entry = ttk.Entry(self.dir_frame)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.dir_button = ttk.Button(self.dir_frame, text="Browse", command=self.choose_directory)
        self.dir_button.pack(side=tk.LEFT)

        self.progress_frame = ttk.Frame(self.root, padding="10")
        self.progress_frame.pack(fill=tk.X)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame, 
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X)
        
        self.status_label = ttk.Label(self.progress_frame, text="Ready")
        self.status_label.pack()

        self.download_button = ttk.Button(
            self.root,
            text="Start Download",
            command=self.start_download
        )
        self.download_button.pack(pady=10)

        self.status_text = tk.Text(self.root, height=10, width=50)
        self.status_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        default_dir = str(Path.home() / "Downloads" / "CBSE_Papers")
        self.dir_entry.insert(0, default_dir)

    def choose_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def update_status(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)

    def start_download(self):
        download_dir = self.dir_entry.get()
        if not download_dir:
            self.update_status("Please select a download directory first!")
            return
            
        self.download_button.config(state=tk.DISABLED)
        self.status_label.config(text="Initializing...")

        downloader = CBSEPaperDownloader(download_dir)
        
        def download_thread():
            try:
                downloader.download_all_papers()
                self.root.after(0, self.download_completed)
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error: {str(e)}"))
                self.root.after(0, self.download_completed)
        
        threading.Thread(target=download_thread, daemon=True).start()

    def download_completed(self):
        self.download_button.config(state=tk.NORMAL)
        self.status_label.config(text="Download completed")
        self.progress_var.set(0)
        self.update_status("All downloads completed!")

    def run(self):
        self.root.mainloop()

def main():
    gui = DownloaderGUI()
    gui.run()

if __name__ == "__main__":
    main()