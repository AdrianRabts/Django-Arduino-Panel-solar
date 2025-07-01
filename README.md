Django-Arduino-Panel-solar
Panel de control web para monitorear y analizar datos de sensores conectados a un panel solar, usando Django como backend y Arduino como fuente de datos.

Descripción
Este proyecto permite visualizar y analizar los datos recolectados por sensores LDR (fotoresistencias) y de salida solar conectados a un Arduino, que luego son almacenados y gestionados desde un backend en Django. Incluye un dashboard web moderno (HTML + Bootstrap + Chart.js) para seguimiento en tiempo real y visualización histórica.

Características
Visualización de los últimos datos registrados por sensores en un panel solar.
Dashboard responsive con métricas, tablas y gráficos.
Backend en Django, con modelos listos para almacenar y consultar datos.
Uso de filtros personalizados en plantillas para cálculos estadísticos rápidos (máximo, mínimo, promedio).
Preparado para recibir y mostrar datos de Arduino.

Estructura del Proyecto
Django-Arduino-Panel-solar/
├── datos_arduino/
│   ├── migrations/
│   ├── templates/datos_arduino/lista_datos.html
│   ├── templatetags/stats_filters.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
├── panel_solar/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
├── manage.py

Modelo de Datos
El modelo principal es SensorData, que almacena:

timestamp: Fecha y hora de la medición.
ldr_left_top, ldr_right_top, ldr_left_bottom, ldr_right_bottom: Lecturas de sensores LDR.
solar_value: Valor de salida solar.

Interfaz Web
La plantilla principal (lista_datos.html) ofrece:

Dashboard moderno y responsivo.
Visualización de métricas y tabla de últimas lecturas.
Gráficos preparados para integrar datos históricos.

Comunicación con Arduino
Deberás implementar una rutina (por ejemplo, usando pySerial) para recibir datos del Arduino y guardarlos en la base de datos. El backend y frontend ya están listos para mostrar los datos almacenados.
--------------------------------------------------------------------------------------------------------

#include <Servo.h>  

Servo horizontal; // Servo horizontal
int servohori = 180;  
int servohoriLimitHigh = 175;
int servohoriLimitLow = 5;

Servo vertical; // Servo vertical
int servovert = 45;  
int servovertLimitHigh = 100;
int servovertLimitLow = 1;

// Pines de los LDR
int ldrlt = A0; // Izquierda arriba
int ldrrt = A3; // Derecha arriba
int ldrld = A1; // Izquierda abajo
int ldrrd = A2; // Derecha abajo

int solarPin = A4; // Pin para el panel solar

// Variables para suavizar las lecturas
int lt_prev = 0;
int rt_prev = 0;
int ld_prev = 0;
int rd_prev = 0;
int solarPrev = 0;

void setup() {
  horizontal.attach(2);
  vertical.attach(13);
  horizontal.write(180);
  vertical.write(45);
  delay(2500);
  
  Serial.begin(9600);  // Iniciar comunicación serial
}

void loop() {
  // Leer valores de los LDRs y panel solar
  int lt = analogRead(ldrlt); // Arriba izquierda
  int rt = analogRead(ldrrt); // Arriba derecha
  int ld = analogRead(ldrld); // Abajo izquierda
  int rd = analogRead(ldrrd); // Derecha abajo
  int solarValue = analogRead(solarPin); // Valor del panel solar

  // Promediar los valores de los LDRs para evitar lecturas erráticas
  lt = (lt + lt_prev) / 2;
  rt = (rt + rt_prev) / 2;
  ld = (ld + ld_prev) / 2;
  rd = (rd + rd_prev) / 2;
  solarValue = (solarValue + solarPrev) / 2;

  // Guardar las lecturas previas para el próximo ciclo
  lt_prev = lt;
  rt_prev = rt;
  ld_prev = ld;
  rd_prev = rd;
  solarPrev = solarValue;

  // Imprimir los valores de los LDRs y el panel solar en formato CSV
  Serial.print("LDR_Left_Top: ");
  Serial.print(lt);
  Serial.print(", LDR_Right_Top: ");
  Serial.print(rt);
  Serial.print(", LDR_Left_Bottom: ");
  Serial.print(ld);
  Serial.print(", LDR_Right_Bottom: ");
  Serial.print(rd);
  Serial.print(", Solar_Value: ");
  Serial.println(solarValue);  // Termina la línea para facilitar la lectura en Python

  // Configurar tolerancia y el tiempo de retraso
  int dtime = 10;  
  int tol = 90; // Tolerancia

  int avt = (lt + rt) / 2; // Promedio superior
  int avd = (ld + rd) / 2; // Promedio inferior
  int avl = (lt + ld) / 2; // Promedio izquierdo
  int avr = (rt + rd) / 2; // Promedio derecho

  int dvert = avt - avd; // Diferencia vertical
  int dhoriz = avl - avr; // Diferencia horizontal

  // EJE VERTICAL (invertido)
  if (abs(dvert) > tol) {  
    if (avt > avd) {
      servovert = --servovert;  // Movimiento invertido
      if (servovert < servovertLimitLow) servovert = servovertLimitLow;
    } else {
      servovert = ++servovert;  // Movimiento invertido
      if (servovert > servovertLimitHigh) servovert = servovertLimitHigh;
    }
    vertical.write(servovert);
  }

  // EJE HORIZONTAL (normal)
  if (abs(dhoriz) > tol) {  
    if (avl > avr) {
      servohori = --servohori;
      if (servohori < servohoriLimitLow) servohori = servohoriLimitLow;
    } else {
      servohori = ++servohori;
      if (servohori > servohoriLimitHigh) servohori = servohoriLimitHigh;
    }
    horizontal.write(servohori);
  }

  delay(dtime);
}
