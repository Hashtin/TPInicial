class DashboardProductivo {
    constructor() {
        this.datos = null;
    }

    async cargarDatos() {
        try {
            const response = await fetch(`${API_URL}/analisis/productividad`);
            this.datos = await response.json();
            this.renderizarDashboard();
        } catch (error) {
            console.error('Error cargando datos:', error);
        }
    }

    renderizarDashboard() {
        this.crearGraficoEfectividadTiempo();
        this.crearGraficoEficienciaTiempo();
        this.crearGraficoEficaciaTiempo();
        this.crearGraficoProduccionTiempo();
        this.crearGraficoGananciaProducto();
        this.actualizarMetricas();
    }

    // 1. Gráfico de Líneas - Efectividad en el Tiempo
    crearGraficoEfectividadTiempo() {
        const ctx = document.getElementById('chart-efectividad-tiempo').getContext('2d');
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.datos.meses,
                datasets: this.datos.productos.map(producto => ({
                    label: producto.nombre,
                    data: producto.efectividad_mensual,
                    borderColor: this.obtenerColor(producto.id),
                    backgroundColor: this.obtenerColor(producto.id, 0.1),
                    tension: 0.4,
                    fill: false,
                    borderWidth: 2
                }))
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Evolución de Efectividad Mensual (%)'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Efectividad (%)' }
                    }
                }
            }
        });
    }

    // 2. Gráfico de Líneas - Eficiencia en el Tiempo
    crearGraficoEficienciaTiempo() {
        const ctx = document.getElementById('chart-eficiencia-tiempo').getContext('2d');
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.datos.meses,
                datasets: this.datos.productos.map(producto => ({
                    label: producto.nombre,
                    data: producto.eficiencia_mensual,
                    borderColor: this.obtenerColor(producto.id),
                    backgroundColor: this.obtenerColor(producto.id, 0.1),
                    tension: 0.4,
                    fill: false,
                    borderWidth: 2
                }))
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Evolución de Eficiencia Mensual (%)'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Eficiencia (%)' }
                    }
                }
            }
        });
    }

    // 3. Gráfico de Líneas - Eficacia en el Tiempo
    crearGraficoEficaciaTiempo() {
        const ctx = document.getElementById('chart-eficacia-tiempo').getContext('2d');
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.datos.meses,
                datasets: this.datos.productos.map(producto => ({
                    label: producto.nombre,
                    data: producto.eficacia_mensual,
                    borderColor: this.obtenerColor(producto.id),
                    backgroundColor: this.obtenerColor(producto.id, 0.1),
                    tension: 0.4,
                    fill: false,
                    borderWidth: 2
                }))
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Evolución de Eficacia Mensual (%)'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Eficacia (%)' }
                    }
                }
            }
        });
    }

    // 4. Gráfico de Líneas - Producción en el Tiempo
    crearGraficoProduccionTiempo() {
        const ctx = document.getElementById('chart-produccion-tiempo').getContext('2d');
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.datos.meses,
                datasets: this.datos.productos.map(producto => ({
                    label: producto.nombre,
                    data: producto.produccion_mensual,
                    borderColor: this.obtenerColor(producto.id),
                    backgroundColor: this.obtenerColor(producto.id, 0.1),
                    tension: 0.4,
                    fill: false,
                    borderWidth: 2
                }))
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Evolución de Producción Mensual (kg)'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Producción (kg)' }
                    }
                }
            }
        });
    }

    // 5. Gráfico de Torta - Ganancia Bruta por Producto
    crearGraficoGananciaProducto() {
        const ctx = document.getElementById('chart-ganancia-producto').getContext('2d');
        
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: this.datos.productos.map(p => p.nombre),
                datasets: [{
                    data: this.datos.productos.map(p => p.ganancia_total),
                    backgroundColor: this.datos.productos.map(p => this.obtenerColor(p.id, 0.7)),
                    borderColor: this.datos.productos.map(p => this.obtenerColor(p.id)),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Distribución de Ganancia Bruta'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const value = context.raw;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${context.label}: $${value.toLocaleString()} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    actualizarMetricas() {
        const container = document.getElementById('metricas-resumen');
        container.innerHTML = this.datos.metricas_generales.map(metric => `
            <div class="metric-item">
                <span>${metric.nombre}:</span>
                <span class="metric-value">${metric.valor}</span>
            </div>
        `).join('');
    }

    obtenerColor(id, alpha = 1) {
        const colores = [
            `rgba(255, 99, 132, ${alpha})`,  // Rojo - Dulce de leche
            `rgba(54, 162, 235, ${alpha})`,   // Azul - Sachet de leche
            `rgba(255, 206, 86, ${alpha})`,   // Amarillo - Queso cremoso
            `rgba(75, 192, 192, ${alpha})`    // Verde - Yogur bebible
        ];
        return colores[id % colores.length];
    }
}

// Inicializar dashboard
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new DashboardProductivo();
    dashboard.cargarDatos();
});