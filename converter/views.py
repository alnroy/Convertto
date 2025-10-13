import os
import traceback
from io import BytesIO
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from google.cloud import vision
import fitz  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from googletrans import Translator
import pypandoc
from weasyprint import HTML, CSS
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

translator = Translator()

@csrf_exempt
def translate_text(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')
        src = data.get('src', 'en')
        dest = data.get('dest', 'ml')
        try:
            result = translator.translate(text, src=src, dest=dest)
            return JsonResponse({'translated': result.text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def transliterate_text(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')
        try:
            mal = transliterate(text, sanscript.ITRANS, sanscript.MALAYALAM)
            return JsonResponse({'transliterated': mal})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
def save_document(request):
    data = json.loads(request.body)
    html_content = data.get('html', '')

    full_html = f"""
    <html>
      <head>
        <style>
          body {{
            font-family: 'Calibri', sans-serif;
          }}
          .ql-editor {{
            width: 21cm;
            min-height: 29.7cm;
            padding: 2cm;
          }}
        </style>
      </head>
      <body>{html_content}</body>
    </html>
    """

    pdf = HTML(string=full_html).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin: 1in; }')])
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="workspace.pdf"'
    return response



class ConvertHandwritingAPIView(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            
            # Save uploaded file temporarily
            safe_name = uploaded_file.name.replace(" ", "_").replace(":", "_")
            path = default_storage.save('tmp/' + safe_name, ContentFile(uploaded_file.read()))
            full_path = default_storage.path(path)

            text = ""
            languages = []

            try:
                if uploaded_file.name.lower().endswith('.pdf'):
                    pages_bytes = pdf_to_images(full_path)
                    for img_bytes in pages_bytes:
                        page_text, page_langs = extract_text_from_image_bytes(img_bytes)
                        text += page_text + "\n\n"
                        languages.extend(page_langs)
                else:
                    with open(full_path, 'rb') as img_file:
                        content = img_file.read()
                    text, languages = extract_text_from_image_bytes(content)

                languages = list(set(languages))
            except Exception as e:
                return Response({"error": f"OCR error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                # Delete temporary file
                default_storage.delete(path)

            return Response({"text": text, "languages": languages}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


client = vision.ImageAnnotatorClient()

@csrf_exempt
def extract_text_from_image_bytes(image_bytes):
    image = vision.Image(content=image_bytes)
    response = client.document_text_detection(image=image)
    annotations = response.full_text_annotation

    text = annotations.text if annotations.text else ""
    langs = []

    for page in annotations.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    if word.property.detected_languages:
                        for lang in word.property.detected_languages:
                            langs.append(lang.language_code)

    return text, list(set(langs))

@csrf_exempt
def pdf_to_images(pdf_path):
    """Convert PDF pages to JPEG bytes using PyMuPDF"""
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("jpeg")
        images.append(img_bytes)
    return images

@csrf_exempt
def upload_and_convert(request):
    text = ""
    languages = []

    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']

        # Save uploaded file
        safe_name = uploaded_file.name.replace(" ", "_").replace(":", "_")
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(safe_name, uploaded_file)
        full_path = os.path.join(settings.MEDIA_ROOT, filename)

        try:
            if uploaded_file.name.lower().endswith('.pdf'):
                # --- Handle PDF using PyMuPDF 
                pages_bytes = pdf_to_images(full_path)
                for img_bytes in pages_bytes:
                    page_text, page_langs = extract_text_from_image_bytes(img_bytes)
                    text += page_text + "\n\n"
                    languages.extend(page_langs)
            else:
                # --- Handle Images ---
                with open(full_path, 'rb') as img_file:
                    content = img_file.read()
                text, languages = extract_text_from_image_bytes(content)

            languages = list(set(languages))

        except Exception as e:
            print("----- OCR ERROR TRACEBACK -----")
            traceback.print_exc()
            print("----- END TRACEBACK -----")
            text = f"⚠️ Error during OCR: {str(e)}" 

    return render(request, 'upload.html', {'text': text, 'languages': languages})


@csrf_exempt
def home(request):
    return render(request, 'index.html')
