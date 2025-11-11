"""
Copia el reporte generado a la carpeta de Quartz para publicacion web
"""
import shutil
import os
from datetime import datetime

# Rutas
REPORTE_ORIGEN = 'project/output/reporte.md'
REPORTE_DESTINO = 'site/content/reportes/reporte-UT1.md'

def copiar_reporte():
    """Copia el reporte a la carpeta de Quartz"""
    
    print("Copiando reporte a Quartz...")
    
    if not os.path.exists(REPORTE_ORIGEN):
        print(f"ERROR: No se encuentra {REPORTE_ORIGEN}")
        print("   Ejecuta primero: python project/ingest/run.py")
        return
    
    # Crear carpeta destino si no existe
    os.makedirs(os.path.dirname(REPORTE_DESTINO), exist_ok=True)
    
    # Copiar archivo
    shutil.copy2(REPORTE_ORIGEN, REPORTE_DESTINO)
    
    print(f"Reporte copiado a: {REPORTE_DESTINO}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nProximos pasos para publicar en GitHub Pages:")
    print("   1. cd site")
    print("   2. npx quartz build --serve  (para previsualizar)")
    print("   3. git add . && git commit -m 'Actualizar reporte'")
    print("   4. git push origin main")
    print("\n   El workflow de GitHub Actions desplegara automaticamente.")

if __name__ == '__main__':
    copiar_reporte()