import trafilatura
from pypdf import PdfReader
import io

def extract_from_url(url: str):
    """Scrapes a URL for article,text, autor an publication metadata."""
    downloaded = trafilatura.fetch_url(url)

    if not downloaded:
        return {"error": "Could not access the URL. It may be blocked or invalid."}
    
    article = trafilatura.extract(downloaded, output_format='json', with_metadata=True)

    if not article:
        return {"error": "Couldnt not extract text from the webpage."}
    
    import json
    data = json.loads(article)

    return {
        "text": data.get("text", ""),
        "metadata": {
            "title": data.get("title", "Unknown Title"),
            "author": data.get("author", "Unknown Author"),
            "publication_date": data.get("date", "Unknown Date"),
            "source_url": url
        }
    }

def extract_from_pdf(pdf_bytes: bytes):
    """Extracts text from a binary PDF file."""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text+= page_text + "\n"

        if not text.strip():
            return {"error": "The PDF appears to be empty or consists only of images."}
        
        return {
            "text": text,
            "metadata": {
                "title": "PDF Document",
                "author": "Unknown",
                "source": "User Upload"
            }
        }
    except Exception as e:
        return {"error": f"Failed to read PDF: {str(e)}"}