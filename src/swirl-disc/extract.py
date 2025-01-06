from io import BytesIO
from paddleocr import PaddleOCR
from PIL import Image
from pdf2image import convert_from_bytes
import requests


class Extract:
    def __init__(self):
        # Initialize PaddleOCR
        self.paddle = PaddleOCR(use_angle_cls=True, lang='en')  # 'en' for English, adjust `lang` for other languages
    
    def fetchDoc(self, doc_urls):
        results = []
        for url in doc_urls:
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    type = res.headers.get('Content-Type', '')
                    if 'application/pdf' in type:
                        pdf_content = BytesIO(res.content)  # Load PDF into memory
                        # Convert PDF to images
                        images = convert_from_bytes(pdf_content.getvalue())
                        
                        for page_number, image in enumerate(images, start=1):
                            # Convert the PIL Image object to a format compatible with PaddleOCR
                            image_path = f"page_{page_number}.jpg"
                            image.save(image_path)  # Save the image if needed (optional)
                            
                            # Extract text using PaddleOCR
                            results += self.paddle.ocr(image_path, cls=True)
                    elif 'image/' in type:
                        image_content = BytesIO(res.content)  # Load image into memory
                        image = Image.open(image_content)  # Use PIL to open the image
                        image.thumbnail((1024, 1024), Image.ANTIALIAS)
                        
                        # Convert to OCR-compatible format (Pillow image to file path or directly)
                        results += self.paddle.ocr(image_content, cls=True)
                    else:
                        print("Unknown file type.", type)
            except:
                pass
            
        return results
        
# Example usage
if __name__ == "__main__":
    ex = Extract()
    
    # res = ex.fetchDoc(["https://cdn.filestackcontent.com/ZXCwYtkDQn23FlL9R2bM", "https://cdn.filestackcontent.com/xoJSES9TyicMsmHq4EAQ"])
    res = ex.fetchDoc(["https://cdn.filestackcontent.com/Puy4AJZRRyuNnEubmRJ2", "https://cdn.filestackcontent.com/7l8erVmdTAjVjuGyeCl6"])
    
    for line in res[0]:
            print(f"Detected text: {line[1][0]}, Confidence: {line[1][1]}")