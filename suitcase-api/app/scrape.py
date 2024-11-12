import requests
import time
import os
from multiprocessing import Pool, Manager, Lock
from datetime import datetime
import logging
from pathlib import Path

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(processName)s - %(message)s',
        handlers=[
            logging.FileHandler('scraper.log'),
            logging.StreamHandler()
        ]
    )

def download_doc(args):
    """Download a single document with rate limiting using shared counter"""
    doc_id, shared_dict, lock = args
    
    # Ensure we don't exceed 10 requests per second across all processes
    with lock:
        current_time = time.time()
        if 'last_request' in shared_dict:
            time_diff = current_time - shared_dict['last_request']
            if time_diff < 0.1:  # Maintain 10 reqs/sec across all processes
                time.sleep(0.1 - time_diff)
        shared_dict['last_request'] = time.time()

    url = f"https://indiankanoon.org/doc/{doc_id}/"
    out_dir = Path('docs') / f"{doc_id // 1000:05d}"
    out_file = out_dir / f"doc_{doc_id}.txt"
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(out_dir, exist_ok=True)
        
        while True:
            # Download with timeout
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                with open(out_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                logging.info(f"Downloaded {doc_id}")
                return True
            elif response.status_code == 429:
                logging.warning(f"Rate limit hit for {doc_id}. Retrying after 1 seconds.")
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                logging.error(f"Error {response.status_code} on {doc_id}")
                return False
            
    except Exception as e:
        logging.error(f"Failed {doc_id}: {str(e)}")
        return False

def main():
    # Create output directory
    os.makedirs('docs', exist_ok=True)
    
    # Setup logging
    setup_logging()
    
    # Number of processes - using 8 workers
    num_processes = 8
    
    # Setup shared state for rate limiting
    manager = Manager()
    shared_dict = manager.dict()
    lock = manager.Lock()
    
    # Create process pool
    with Pool(processes=num_processes) as pool:
        # Create args with shared state
        args = [(i, shared_dict, lock) for i in range(2450, 30_000_001)]
        
        # Start processing with progress monitoring
        for i, success in enumerate(pool.imap_unordered(download_doc, args)):
            if i % 100 == 0:
                logging.info(f"Processed {i} documents")

if __name__ == '__main__':
    main()
