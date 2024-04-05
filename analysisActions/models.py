from django.db import models
from django.utils import timezone
# Create your models here.
class CEDEAR(models.Model):
    especie = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=100, unique=True)
    cierre_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    precio_apertura = models.DecimalField(max_digits=10, decimal_places=2)
    precio_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    ultimo_precio = models.DecimalField(max_digits=10, decimal_places=2)
    variacion_diaria = models.CharField(max_length=50)
    volumen_efectivo = models.DecimalField(max_digits=15, decimal_places=2)
    volumen_nominal = models.IntegerField()
    tipo_cotizacion = models.CharField(max_length=3)  # "usd" o "ars"
    
    # Campos adicionales basados en el ejemplo JSON
    cantidad_nominal_compra = models.IntegerField(default=0)
    cantidad_nominal_venta = models.IntegerField(default=0)
    cantidad_operaciones = models.CharField(max_length=50, default=0)
    estado = models.CharField(max_length=50, blank=True, default='')
    ex = models.CharField(max_length=3, blank=True, default='')  # Ejemplo: "No"
    hora_cotizacion = models.CharField(max_length=12, default='00:00:00')
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_promedio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_promedio_ponderado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tendencia = models.IntegerField(default=None, null=True)
    vencimiento = models.CharField(max_length=50, blank=True, default='')
    ratio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    beneficio_diferencia_accion = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    accion_x_ratio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def get_queryset(self):
        # Filtrar los CEDEARs cuyos símbolos terminan en "D"
        queryset = super().get_queryset()
        queryset = queryset.filter(simbolo__endswith='D')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cedears = self.get_queryset()
        for cedear in cedears:
            accion = Accion.objects.filter(simbolo=cedear.simbolo).first()
            if accion:
                cedear.ultimo_precio_accion = accion.ultimo_precio
                cedear.diferencia_accion_x_ratio_ultimo_precio = cedear.accion_x_ratio - accion.ultimo_precio
        context['cedears'] = cedears
        return context
    def actualizar_datos(self):
        if self.ratio == 0:
            self.accion_x_ratio = -9999
        elif self.ratio > 0:
            self.accion_x_ratio = self.ultimo_precio * self.ratio
        else:
            self.accion_x_ratio = self.ultimo_precio / abs(self.ratio)
        self.save()
    class Meta:
        ordering = ['especie']
        
class Accion(models.Model):
    simbolo = models.CharField(max_length=10, unique=True)
    simbolo_cedears = models.CharField(max_length=10, null=True)
    nombre = models.CharField(max_length=100)
    mercado = models.CharField(max_length=10)  # Por ejemplo, NASDAQ o NYSE
    ultimo_precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    apertura = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    maximo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    minimo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    volumen = models.BigIntegerField(null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    recomendacion = models.CharField(max_length=16, null=True)
    def __str__(self):
        return f"{self.simbolo} - {self.nombre}"
class Operacion(models.Model):
    MONEDAS_CHOICES = [
        ('USD', 'Dólar Estadounidense'),
        ('ARS', 'Peso Argentino'),
    ]
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cantidad = models.IntegerField()
    moneda = models.CharField(max_length=3, choices=MONEDAS_CHOICES)
    fecha = models.DateTimeField(default=timezone.now)
    simbolo = models.CharField(max_length=100)
    monto_total = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.fecha} - {self.simbolo} - {self.monto_total}"

    class Meta:
        ordering = ['-fecha']