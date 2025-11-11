"""
Generador de datos de ejemplo para el proyecto de Finanzas
Crea gastos.csv y presupuesto.csv con datos realistas
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generar_datos_ejemplo():
    """
    Genera archivos CSV de ejemplo para gastos y presupuesto
    """
    # Crear carpeta data si no existe
    os.makedirs('project/data', exist_ok=True)
    
    # ========== GASTOS.CSV ==========
    print("📊 Generando gastos.csv...")
    
    # Áreas de la empresa
    areas = ['Ventas', 'Marketing', 'TI', 'RRHH', 'Operaciones', 'ventas', 'ti']  # Con variaciones
    
    # Partidas presupuestarias
    partidas = [
        'Salarios', 'Material Oficina', 'Software', 'Hardware',
        'Publicidad', 'Formación', 'Viajes', 'Servicios Externos',
        'salarios', 'PUBLICIDAD'  # Variaciones para validar limpieza
    ]
    
    # Generar 500 registros de gastos
    np.random.seed(42)
    num_registros = 500
    
    fecha_inicio = datetime(2024, 1, 1)
    
    gastos_data = []
    for i in range(num_registros):
        # Fecha aleatoria en 2024
        dias_aleatorios = np.random.randint(0, 300)
        fecha = fecha_inicio + timedelta(days=dias_aleatorios)
        
        area = np.random.choice(areas)
        partida = np.random.choice(partidas)
        
        # Importes realistas (algunos negativos para validar)
        if np.random.random() < 0.02:  # 2% de errores
            importe = np.random.uniform(-1000, -100)  # Negativos (inválidos)
        else:
            importe = round(np.random.uniform(100, 15000), 2)
        
        gastos_data.append({
            'fecha': fecha.strftime('%Y-%m-%d'),
            'area': area,
            'partida': partida,
            'importe': importe
        })
    
    # Añadir algunos registros duplicados para probar deduplicación
    gastos_data.append(gastos_data[0].copy())
    gastos_data.append(gastos_data[0].copy())
    
    # Añadir registros con datos faltantes (para cuarentena)
    gastos_data.append({
        'fecha': '2024-05-15',
        'area': None,
        'partida': 'Salarios',
        'importe': 5000
    })
    gastos_data.append({
        'fecha': '2024-06-20',
        'area': 'Ventas',
        'partida': None,
        'importe': 3000
    })
    
    df_gastos = pd.DataFrame(gastos_data)
    df_gastos.to_csv('project/data/gastos.csv', index=False)
    print(f"✅ gastos.csv creado: {len(df_gastos)} registros")
    
    # ========== PRESUPUESTO.CSV ==========
    print("\n📊 Generando presupuesto.csv...")
    
    # Presupuestos por área (normalizados)
    areas_normalizadas = ['Ventas', 'Marketing', 'TI', 'RRHH', 'Operaciones']
    
    presupuesto_data = []
    for area in areas_normalizadas:
        # Presupuesto anual por área
        presupuesto_anual = np.random.uniform(200000, 800000)
        
        presupuesto_data.append({
            'area': area,
            'presupuesto_anual': round(presupuesto_anual, 2),
            'año': 2024
        })
    
    df_presupuesto = pd.DataFrame(presupuesto_data)
    df_presupuesto.to_csv('project/data/presupuesto.csv', index=False)
    print(f"✅ presupuesto.csv creado: {len(df_presupuesto)} registros")
    
    print("\n🎉 Datos de ejemplo generados correctamente en project/data/")
    print("\nPróximos pasos:")
    print("  1. Ejecuta: python project/ingest/run.py")
    print("  2. Revisa el reporte en: project/output/reporte.md")

if __name__ == '__main__':
    generar_datos_ejemplo()
