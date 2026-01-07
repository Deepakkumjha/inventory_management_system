from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Item
from .serializers import ItemSerializers
import logging
from reportlab.pdfgen import canvas
from openpyxl import Workbook
logger = logging.getLogger(__name__)

@api_view(['GET','POST'])
def item(request):
        if request.method == 'GET':
            try:
                items = Item.objects.all()
                serializers = ItemSerializers(items,many=True)
                return Response(serializers.data,status=status.HTTP_200_OK)
            except Exception:
                logger.exception("error occurs in item during fetch")
                return Response({"error":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == "POST":
            try:
                data = request.data
                serializer = ItemSerializers(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response("item created",status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                logger.exception("error occurs in item during creation")
                return Response({"error":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET','PUT','PATCH','DELETE'])
def single_product(request, id):
        try:
            item = Item.objects.get(id=id)
            if request.method == "GET":
                serializer = ItemSerializers(item)
                return Response(serializer.data , status=status.HTTP_200_OK)
            if request.method == "PUT":
                serializer = ItemSerializers(item,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response("item updated", status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if request.method == "PATCH":
                serializer = ItemSerializers(item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response("item updated", status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if request.method == "DELETE":
                item.delete()
                return Response("item deleted", status=status.HTTP_404_NOT_FOUND)

        except Item.DoesNotExist:
            logger.exception("item does not exist")
            return Response("not found", status=status.HTTP_404_NOT_FOUND)
        except Item.MultipleObjectsReturned:
            logger.exception("mutliple objects returned")
            return Response("multiple objects returned", status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logger.exception("error occurs in the single_product")
        return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_pdf(request):
    try:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="items_report.pdf"'
        p = canvas.Canvas(response,pagesize=A4)
        width, height = A4
        y = height - 40
        p.setFont("Helvetica-Bold", 14)
        p.drawString(40, y, "Items Report")

        y -= 30
        p.setFont("Helvetica-Bold", 10)
        p.drawString(40, y, "ID")
        p.drawString(80, y, "Name")
        p.drawString(220, y, "Qty")
        p.drawString(260, y, "Price")
        p.drawString(320, y, "Created At")

        y -= 20
        p.setFont("Helvetica", 10)
        items = Item.objects.all()
        for item in items:
            if y < 50:
                p.showPage()
                y = height - 40

            p.drawString(40, y, str(item.id))
            p.drawString(80, y, item.name)
            p.drawString(220, y, str(item.quantity))
            p.drawString(260, y, str(item.price))
            p.drawString(320, y, item.created_at.strftime("%Y-%m-%d"))

            y -= 18
        p.showPage()
        p.save()
        return response

    except Exception:
        logger.exception("Error generating Excel report")
        return HttpResponse(
            "Internal Server Error",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_excel(request):
    try:
        items = Item.objects.all()

        wb = Workbook()
        ws = wb.active
        ws.title = "Items Report"

        headers = ["ID", "Name", "Quantity", "Price", "Created At"]
        ws.append(headers)

        for item in items:
            ws.append([
                item.id,
                item.name,
                item.quantity,
                float(item.price),
                item.created_at.strftime("%Y-%m-%d")
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="items_report.xlsx"'

        wb.save(response)

        return response

    except Exception:
        logger.exception("Error generating Excel report")
        return HttpResponse(
            "Internal Server Error",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
