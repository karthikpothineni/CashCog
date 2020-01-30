from rest_framework import viewsets
from ..serializers.expenseSerializers import *
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import View
from django.http import HttpResponse


class ExpenseViewSet(viewsets.ModelViewSet):

    def list(self, request, *args):
        try:
            expense_obj = Expense.objects.select_related('employee').all()
            expenses = []
            for each_expense in expense_obj:
                employee_obj = each_expense.employee
                each_expense = ExpenseSerializer(each_expense).data
                each_expense['employee'] = EmployeeSerializer(employee_obj).data
                expenses.append(each_expense)
            return Response(expenses,status=status.HTTP_200_OK)
        except:
            return Response("Unable to list expenses", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, pk=None):
        try:
            expense_obj = Expense.objects.select_related('employee').get(uuid=pk)
            if expense_obj is not None:
                employee_obj = expense_obj.employee
                expense_data = ExpenseSerializer(expense_obj).data
                expense_data['employee'] = EmployeeSerializer(employee_obj).data
                return Response(expense_data, status=status.HTTP_200_OK)
            else:
                return Response("Unable to get expense", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Unable to retrieve expense", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, pk=None):
        try:
            expense_obj = Expense.objects.get(uuid=pk)
            if expense_obj is not None:
                employee_obj = expense_obj.employee
                serializer = ExpenseSerializer(expense_obj, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_expense = serializer.data
                    updated_expense['employee'] = EmployeeSerializer(employee_obj).data
                    return Response(updated_expense, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Unable to get expense", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Unable to update expense", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, *args, pk=None):
        try:
            expense_obj = Expense.objects.get(uuid=pk)
            if expense_obj is not None:
                expense_obj.delete()
                return Response("Expense successfully deleted", status=status.HTTP_200_OK)
            else:
                return Response("Expense already deleted or does not exist", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Unable to delete expense", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def sort_expenses(self, request):
        try:
            sortFilter = request.query_params.get('filter', None)
            orderFilter = request.query_params.get('order', None)
            if sortFilter is not None and orderFilter is not None and orderFilter.lower() in ['asc', 'desc']:
                if orderFilter.lower() == 'desc':
                    sortFilter = '-'+sortFilter
                expense_obj = Expense.objects.select_related('employee').order_by('{0}'.format(sortFilter)).all()
                expenses = []
                for each_expense in expense_obj:
                    employee_obj = each_expense.employee
                    each_expense = ExpenseSerializer(each_expense).data
                    each_expense['employee'] = EmployeeSerializer(employee_obj).data
                    expenses.append(each_expense)
                return Response(expenses,status=status.HTTP_200_OK)
            else:
                return Response("Sort params are incorrect", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Unable to sort expenses", status=status.HTTP_500_INTERNAL_SERVER_ERROR)




######################################################################################################################################



# Healthcheck Methods
class healthcheck_view(View):
    def get(self, request):
        return HttpResponse("It's Working. Awesome!!!")
