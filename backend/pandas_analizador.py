import pandas as pd

def analisis_productivo(datos_crudos, metricas_generales):
        # Convertir a DataFrame de pandas
        df = pd.DataFrame(datos_crudos)
        df['mes'] = pd.to_datetime(df['mes'])
        
        # Obtener todos los meses únicos en formato YYYY-MM
        meses_unicos = sorted(df['mes'].dt.strftime('%Y-%m').unique())
        
        # Procesar los datos EXACTAMENTE como los necesita el frontend
        resultados = {
            'meses': meses_unicos,
            'productos': [],
            'metricas_generales': []
        }
        
        # Calcular métricas generales
        
        resultados['metricas_generales'] = [
            {'nombre': 'Total Productos', 'valor': metricas_generales['total_productos']},
            {'nombre': 'Total Producciones', 'valor': metricas_generales['total_producciones']},
            {'nombre': 'Ganancia Total', 'valor': f"${metricas_generales['ganancia_total']:,.2f}"},
            {'nombre': 'Efectividad Promedio', 'valor': f"{metricas_generales['efectividad_promedio']:.2f}%"},
            {'nombre': 'Eficiencia Promedio', 'valor': f"{metricas_generales['eficiencia_promedio']:.2f}%"},
            {'nombre': 'Producción Total', 'valor': f"{metricas_generales['produccion_total']:,.2f} kg"}
        ]
        
        # Procesar cada producto para los gráficos
        for producto_id in df['producto_id'].unique():
            producto_df = df[df['producto_id'] == producto_id]
            producto_nombre = producto_df['producto_nombre'].iloc[0]
            
            # Inicializar arrays para cada métrica (llenar con 0 para meses sin datos)
            eficacia_mensual = [0] * len(meses_unicos)
            eficiencia_mensual = [0] * len(meses_unicos)
            efectividad_mensual = [0] * len(meses_unicos)
            produccion_mensual = [0] * len(meses_unicos)
            
            # Llenar los arrays con los datos reales
            for i, mes in enumerate(meses_unicos):
                mes_df = producto_df[producto_df['mes'].dt.strftime('%Y-%m') == mes]
                if not mes_df.empty:
                    eficacia_mensual[i] = float(mes_df['eficacia'].mean())
                    eficiencia_mensual[i] = float(mes_df['eficiencia'].mean())
                    efectividad_mensual[i] = float(mes_df['efectividad'].mean())
                    produccion_mensual[i] = float(mes_df['cantidad_producida'].sum())
            
            # Calcular ganancia total del producto
            ganancia_total = float(producto_df['ganancia_bruta'].sum())
            
            resultados['productos'].append({
                'id': int(producto_id),
                'nombre': producto_nombre,
                'eficacia_mensual': eficacia_mensual,
                'eficiencia_mensual': eficiencia_mensual,
                'efectividad_mensual': efectividad_mensual,
                'produccion_mensual': produccion_mensual,
                'ganancia_total': ganancia_total
            })
        return resultados