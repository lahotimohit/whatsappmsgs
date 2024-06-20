import openpyxl
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm
from .models import UserData
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.xlsx'):
                messages.error(request, 'This is not a Excel file')
                return redirect('upload_csv')

            wb = openpyxl.load_workbook(csv_file)
            sheet = wb.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                full_name, email, mobile_number = row
                if full_name and email and mobile_number:
                    UserData.objects.create(full_name=full_name, email=email, mobile_number=mobile_number)

            messages.success(request, 'Excel file has been uploaded and data saved.')
            return redirect('upload_csv')
    else:
        form = CSVUploadForm()
    return render(request, 'index.html', {'form': form})

@csrf_exempt
def receive_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            original_message_body = data.get('original_message_body')
            print(f"Received message from Flask server:{original_message_body}")
            return JsonResponse({'status': 'success', 'msg': original_message_body})
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)