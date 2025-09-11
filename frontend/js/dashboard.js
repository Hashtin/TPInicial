class DashboardProductivo {
    constructor() {
        this.datos = null;
    }

    async cargarDatos() {
        try {
            const response = await fetch(`${API_URL}/analisis/productividad`);
            this.datos = await response.json();
            this.actualizarMetricas();
        } catch (error) {
            console.error('Error cargando datos:', error);
        }
    }

    actualizarMetricas() {
        const container = document.getElementById('metricas-resumen');
        if (!this.datos || !this.datos.metricas_generales) return;
        container.innerHTML = this.datos.metricas_generales.map(metric => `
            <div class="metric-item">
                <span>${metric.nombre}:</span>
                <span class="metric-value">${metric.valor}</span>
            </div>
        `).join('');
    }

    obtenerColor(id, alpha = 1) {
        const colores = [
            `rgba(255, 99, 132, ${alpha})`,
            `rgba(54, 162, 235, ${alpha})`,
            `rgba(255, 206, 86, ${alpha})`,
            `rgba(75, 192, 192, ${alpha})`
        ];
        return colores[id % colores.length];
    }

    static ajustarCanvas(canvas) {
        const dpr = window.devicePixelRatio || 1;
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        const ctx = canvas.getContext('2d');
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    crearGraficoLinea(canvas, dataKey, title, miniatura = false) {
        if (!canvas) return null;
        const ctx = canvas.getContext('2d');

        const opciones = miniatura ? {
            responsive: true,
            plugins: { legend: { display: false }, title: { display: false }, tooltip: { enabled: false } },
            scales: { x: { display: false }, y: { display: false } }
        } : {
            responsive: true,
            plugins: { title: { display: true, text: title } },
            scales: { y: { beginAtZero: true, title: { display: true, text: title.includes('Evolución') ? title.split('Evolución de ')[1] : '' } } }
        };

        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.datos.meses,
                datasets: this.datos.productos.map(p => ({
                    label: p.nombre,
                    data: p[dataKey],
                    borderColor: this.obtenerColor(p.id),
                    backgroundColor: this.obtenerColor(p.id, 0.1),
                    tension: 0.4,
                    fill: false,
                    borderWidth: 2
                }))
            },
            options: opciones
        });

        return chart;
    }

    crearGraficoEfectividadTiempo(canvas, miniatura = false) {
        return this.crearGraficoLinea(canvas, 'efectividad_mensual', 'Evolución de Efectividad Mensual (%)', miniatura);
    }

    crearGraficoEficienciaTiempo(canvas, miniatura = false) {
        return this.crearGraficoLinea(canvas, 'eficiencia_mensual', 'Evolución de Eficiencia Mensual (%)', miniatura);
    }

    crearGraficoEficaciaTiempo(canvas, miniatura = false) {
        return this.crearGraficoLinea(canvas, 'eficacia_mensual', 'Evolución de Eficacia Mensual (%)', miniatura);
    }

    crearGraficoProduccionTiempo(canvas, miniatura = false) {
        return this.crearGraficoLinea(canvas, 'produccion_mensual', 'Evolución de Producción Mensual (kg)', miniatura);
    }

    crearGraficoGananciaProducto(canvas, miniatura = false) {
        if (!canvas) return null;
        const ctx = canvas.getContext('2d');

        const opciones = miniatura ? {
            responsive: true,
            plugins: { legend: { display: false }, title: { display: false }, tooltip: { enabled: false } }
        } : {
            responsive: true,
            plugins: { title: { display: true, text: 'Distribución de Ganancia Bruta' } }
        };

        const chart = new Chart(ctx, {
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
            options: opciones
        });

        return chart;
    }
}

// Inicialización y slider
document.addEventListener('DOMContentLoaded', async () => {
    const dashboard = new DashboardProductivo();
    await dashboard.cargarDatos();

    const principalCanvas = document.getElementById('chart-principal');
    const thumbnails = document.querySelectorAll('.thumbnail');
    let currentChart = null;

    function mostrarGraficoGrande(index) {
        if (currentChart) currentChart.destroy();

        switch(index) {
            case 0: currentChart = dashboard.crearGraficoEfectividadTiempo(principalCanvas); break;
            case 1: currentChart = dashboard.crearGraficoEficienciaTiempo(principalCanvas); break;
            case 2: currentChart = dashboard.crearGraficoEficaciaTiempo(principalCanvas); break;
            case 3: currentChart = dashboard.crearGraficoProduccionTiempo(principalCanvas); break;
            case 4: currentChart = dashboard.crearGraficoGananciaProducto(principalCanvas); break;
        }

        thumbnails.forEach(t => t.classList.remove('active'));
        thumbnails[index].classList.add('active');
    }

    // Crear miniaturas limpias
    thumbnails.forEach((canvas, index) => {
        canvas.id = `thumb-${index}`;
        DashboardProductivo.ajustarCanvas(canvas);

        switch(index) {
            case 0: dashboard.crearGraficoEfectividadTiempo(canvas, true); break;
            case 1: dashboard.crearGraficoEficienciaTiempo(canvas, true); break;
            case 2: dashboard.crearGraficoEficaciaTiempo(canvas, true); break;
            case 3: dashboard.crearGraficoProduccionTiempo(canvas, true); break;
            case 4: dashboard.crearGraficoGananciaProducto(canvas, true); break;
        }

        canvas.addEventListener('click', () => mostrarGraficoGrande(index));
    });

    DashboardProductivo.ajustarCanvas(principalCanvas);
    mostrarGraficoGrande(0); // primer gráfico grande
});
