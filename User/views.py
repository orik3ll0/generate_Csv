from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date
from time import sleep
from User.forms import *
from User.tasks import *

import json



@login_required
def DashboardView(request):
    schema = Schema.objects.filter(user_id=request.user.id).order_by('-id')     #getting schemas data

    context = {'schemas':schema}
    return render(request, 'dashboard.html', context)


@login_required
def NewSchemaView(request):

    if request.method == 'POST':
        form = SchemaForm(request.POST)                     #form for name,separator, string character
        formColumns = SchemaColumnsForm(request.POST)       #form for columns

        if form.is_valid() and formColumns.is_valid():      #forms validations check

            schema = form.save(commit=False)
            schema.user_id = request.user.id
            schema.save()                                   #here we save main form ( name, separator, strin character )

            columnName=request.POST.getlist('columnName')   #getting column name
            type=request.POST.getlist('type')               #getting type of column
            from_int=request.POST.getlist('from_int')       #getting value if type is integer
            to_int=request.POST.getlist('to_int')           #getting value if type is integer
            sentence=request.POST.getlist('sentence')       #getting value if type is text
            order=request.POST.getlist('order')             #getting order of column

            for i in range(len(columnName)):                #checking length of list and create for loop
                form = SchemaColumnsForm(                   #collecting data to form
                    {
                        'columnName': columnName[i],
                        'type': type[i],
                        'from_int': None if from_int[i] == '' else int(from_int[i]),
                        'to_int': None if to_int[i] == '' else int(to_int[i]),
                        'sentence': None if sentence[i] == '' else int(sentence[i]),
                        'order': None if order[i] == '' else int(order[i]),
                    }
                )
                columns = form.save()                       #saving data to our Columns Table
                schema.schemaColumns.add(columns)           #Many To Many id. Connecting tables

            return redirect('User:dashboard')               #redirecting on complate
        else:
            print(form.errors)  # To see the form errors in console.
            print(formColumns.errors)  # To see the form errors in console.

            context = {'form_error': form.errors, 'form_column_error':formColumns.errors}

            return redirect('User:MySchemas', context)  # redirecting on complate
    else:
        form = SchemaForm()
        formColumns = SchemaColumnsForm()

    context = {'form':form, 'formColumns':formColumns}
    return render(request, 'newSchema.html', context)

@login_required
def EditSchemaView(request, pk):
    schema = Schema.objects.get(id=pk)
    input_types = InputType.objects.filter(status=1)
    form = SchemaForm(instance=schema)

    if request.method == 'POST':
        form = SchemaForm(request.POST, instance=schema)
        if form.is_valid():
            schema = form.save(commit=False)
            schema.user_id = request.user.id
            schema.save()                               #updating selectet row

        schema.schemaColumns.all().delete()             #deletes schema columns to create new update
        schema.schemaColumns.clear()                    #clearing pivot table

        columnName = request.POST.getlist('columnName')  # getting column name
        type = request.POST.getlist('type')  # getting type of column
        from_int = request.POST.getlist('from_int')  # getting value if type is integer
        to_int = request.POST.getlist('to_int')  # getting value if type is integer
        sentence = request.POST.getlist('sentence')  # getting value if type is text
        order = request.POST.getlist('order')  # getting order of column

        for i in range(len(columnName)):  # checking length of list and create for loop
            form = SchemaColumnsForm(  # collecting data to form
                {
                    'columnName': columnName[i],
                    'type': type[i],
                    'from_int': None if from_int[i] == '' else int(from_int[i]),
                    'to_int': None if to_int[i] == '' else int(to_int[i]),
                    'sentence': None if sentence[i] == '' else int(sentence[i]),
                    'order': None if order[i] == '' else int(order[i]),
                }
            )
            columns = form.save()  # saving data to our Columns Table
            schema.schemaColumns.add(columns)  # Many To Many id. Connecting tables

        return redirect('User:dashboard')  # redirecting on the end
    else:
        formColumns = SchemaColumnsForm()



        form = SchemaForm(instance=schema)  # form for name,separator, string character

    context = {'form':form, 'formColumns':formColumns, 'schema':schema, 'input_types':input_types}
    return render(request, 'editSchema.html', context)

@login_required
def DeleteSchemaView(request,pk):
    schema = Schema.objects.get(id=pk)              #getting record by id

    if request.method == 'POST':
        for row in schema.schemaColumns.all():      #deleting row related to record
            row.delete()

        schema.schemaColumns.clear()                #deleting relationgs record between tables
        schema.delete()                             #deleting schema
        return redirect('User:dashboard')
    else:
        return redirect('User:dashboard')

@login_required
def MySchemaView(request, pk):
    generated_csv_rows = Generated_csv.objects.filter(schema_id=pk)

    context = {'pk':pk, 'generated_csv_rows': generated_csv_rows}
    return render(request, 'mySchemas.html', context)


@login_required
def GenerateView(request, pk):
    if request.POST:                                    #checking if request is POST
        row = request.POST.get("row")                   #getting inserted row count
        row_id = request.POST.get("row_id")             #getting inserted row count

        schema = Schema.objects.get(id=pk)              #retrieving Schema table

        data_to_send_dict = {}                          #Dictionary to collect columns data

        for column in schema.schemaColumns.order_by('order'):   #for loop to collect data
            data_to_send_dict[column.id] = (
                {
                'columnName': str(column),
                'type': column.type.id,
                'from_int': column.from_int,
                'to_int': column.to_int,
                'sentence': column.sentence,
                'order': column.order
                }
            )

        #task for celery. Sending dictionary, separator, string Character and row count
        task = create_task.delay(data_to_send_dict, str(schema.separator.prefix), str(schema.stringCharacter.prefix), row, row_id)

        #Checking for status every 5 seconds
        result = sleep_to_check_status(task, row)

        generated_csv_rows = Generated_csv.objects.filter(schema_id=pk)

        context = {'generated_csv_rows': generated_csv_rows}
        return render(request, 'generated_data.html', context)


def sleep_to_check_status(task, row):
    """checking status if pending, on success sends json with state"""
    if task.state == "PENDING":
        sleep(5)
        return sleep_to_check_status(task, row)
    else:
        if task.get() == False:
            data = {'task_status': 'FAILURE', 'row': row}
        else:
            data = {'task_status': task.state, 'row': row}

        return data


def CreateRow(request, pk):
    """Creates row which shows status and to be able download on ready"""
    if request.method == 'POST':

        form = Generated_csvForm(request.POST)  # form for name,separator, string character

        if form.is_valid():  # forms validations check

            schema = form.save(commit=False)
            schema.save()
        else:
            print(form.errors)

        myhtml = """<tr><th scope="row">{0}</th> <td>{1}</td> <td><span class="badge badge-secondary">Processing</span></td> <td></td></tr>""".format(schema.id, datetime.date(schema.date_created))
        return JsonResponse({"created_row_id": schema.id, "myhtml":myhtml})
