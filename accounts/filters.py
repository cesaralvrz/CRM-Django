import django_filters
# Importamos el filtro de fecha
from django_filters import DateFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    # La variable se importa de 'DateDilter', en el field
    # asignamos la variable del modelo que queremos usar
    # y la visualización usamos "Greaten than equal to"
    #start_date = DateFilter(field_name="date_created", lookup_expr='gt')
    # Visualización usamos "Less than equal to"
    #end_date = DateFilter(field_name="date_created", lookup_expr='lt')

    class Meta:
        model = Order
        fields = '__all__'
        # Excluimos la variables 'customer' (porque no la queremos)
        # y 'date_created' porque vamos a usar otro formato
        exclude = ['customer', 'date_created']
