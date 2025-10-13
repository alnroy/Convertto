from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from docx import Document
from PIL import Image, ImageDraw, ImageFont
import pdfkit
import io
from googletrans import Translator

translator = Translator()

def workspace_page(request):
    if request.method == 'POST':
        text = request.POST.get.value('outputText', '')
    else:
        # text = request.POST.get.value('outputText', '')
        text=''
    return render(request, 'workspace.html', {'text': text})

class SaveWorkspaceAPIView(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        fmt = request.data.get('format', 'txt')
        

 
        if not text:
            return Response({'error': 'No text provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if fmt == 'txt':
                response = HttpResponse(text, content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename=workspace.txt'
                return response

            elif fmt == 'pdf':
                html = '<pre style="font-family: monospace; white-space: pre-wrap;">{}</pre>'.format(
                    text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                )
                pdf_bytes = pdfkit.from_string(html, False)
                response = HttpResponse(pdf_bytes, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=workspace.pdf'
                return response

            elif fmt == 'docx':
                doc = Document()
                for line in text.splitlines():
                    doc.add_paragraph(line)
                buf = io.BytesIO()
                doc.save(buf)
                buf.seek(0)
                response = HttpResponse(
                    buf.getvalue(),
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                response['Content-Disposition'] = 'attachment; filename=workspace.docx'
                return response

            elif fmt in ['png', 'jpg', 'jpeg']:
                lines = text.splitlines()
                max_width_chars = max((len(l) for l in lines), default=40)
                char_width = 8
                padding = 20
                img_w = max_width_chars * char_width + padding * 2
                img_h = (len(lines) + 1) * 18 + padding * 2

                img = Image.new('RGB', (img_w, img_h), color='white')
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype('DejaVuSans.ttf', 14)
                except Exception:
                    font = ImageFont.load_default()

                y = padding
                for line in lines:
                    draw.text((padding, y), line, fill='black', font=font)
                    y += 18

                buf = io.BytesIO()
                out_fmt = 'PNG' if fmt == 'png' else 'JPEG'
                img.save(buf, format=out_fmt)
                buf.seek(0)
                response = HttpResponse(buf.getvalue(), content_type=f'image/{fmt}')
                response['Content-Disposition'] = f'attachment; filename=workspace.{fmt}'
                return response

            else:
                return Response({'error': 'Unsupported format.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TranslateTextAPIView(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        target = request.data.get('target', 'ml')

        if not text:
            return Response({'error': 'No text provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            translated = translator.translate(text, dest=target)
            return Response({'translated_text': translated.text})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransliterateAPIView(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        target = request.data.get('target', 'ml')

        if not text:
            return Response({'error': 'No text provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transliterated = translator.translate(text, dest=target)
            return Response({'transliterated_text': transliterated.text})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

