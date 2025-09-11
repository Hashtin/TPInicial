document.addEventListener('DOMContentLoaded', async () => {
    const dashboard = new DashboardProductivo();
    await dashboard.cargarDatos();

    const principalCanvas = document.getElementById('chart-principal');
    const thumbnails = document.querySelectorAll('.thumbnail');
    let currentChart = null;

    const tipos = ['efectividad', 'eficiencia', 'eficacia', 'produccion', 'ganancia'];

    // Mostrar gráfico grande
    function mostrarGraficoGrande(index) {
        if (currentChart) currentChart.destroy();

        switch(index) {
            case 0: currentChart = dashboard.crearGraficoEfectividadTiempo(principalCanvas); break;
            case 1: currentChart = dashboard.crearGraficoEficienciaTiempo(principalCanvas); break;
            case 2: currentChart = dashboard.crearGraficoEficaciaTiempo(principalCanvas); break;
            case 3: currentChart = dashboard.crearGraficoProduccionTiempo(principalCanvas); break;
            case 4: currentChart = dashboard.crearGraficoGananciaProducto(principalCanvas); break;
        }

        thumbnails.forEach((t, i) => t.classList.toggle('active', i === index));
    }

    // Crear miniaturas limpias
    function crearMiniatura(canvas, tipo) {
        const opcionesMini = {
            responsive: true,
            plugins: {
                legend: { display: false },
                title: { display: false },
                tooltip: { enabled: false }
            },
            scales: {
                x: { display: false },
                y: { display: false }
            }
        };

        const ctx = canvas.getContext('2d');

        switch(tipo) {
            case 'efectividad':
                return new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: dashboard.datos.meses,
                        datasets: dashboard.datos.productos.map(p => ({
                            label: p.nombre,
                            data: p.efectividad_mensual,
                            borderColor: dashboard.obtenerColor(p.id),
                            backgroundColor: dashboard.obtenerColor(p.id, 0.1),
                            tension: 0.4,
                            fill: false,
                            borderWidth: 2
                        }))
                    },
                    options: opcionesMini
                });
            case 'eficiencia':
                return new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: dashboard.datos.meses,
                        datasets: dashboard.datos.productos.map(p => ({
                            label: p.nombre,
                            data: p.eficiencia_mensual,
                            borderColor: dashboard.obtenerColor(p.id),
                            backgroundColor: dashboard.obtenerColor(p.id, 0.1),
                            tension: 0.4,
                            fill: false,
                            borderWidth: 2
                        }))
                    },
                    options: opcionesMini
                });
            case 'eficacia':
                return new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: dashboard.datos.meses,
                        datasets: dashboard.datos.productos.map(p => ({
                            label: p.nombre,
                            data: p.eficacia_mensual,
                            borderColor: dashboard.obtenerColor(p.id),
                            backgroundColor: dashboard.obtenerColor(p.id, 0.1),
                            tension: 0.4,
                            fill: false,
                            borderWidth: 2
                        }))
                    },
                    options: opcionesMini
                });
            case 'produccion':
                return new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: dashboard.datos.meses,
                        datasets: dashboard.datos.productos.map(p => ({
                            label: p.nombre,
                            data: p.produccion_mensual,
                            borderColor: dashboard.obtenerColor(p.id),
                            backgroundColor: dashboard.obtenerColor(p.id, 0.1),
                            tension: 0.4,
                            fill: false,
                            borderWidth: 2
                        }))
                    },
                    options: opcionesMini
                });
            case 'ganancia':
                return new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: dashboard.datos.productos.map(p => p.nombre),
                        datasets: [{
                            data: dashboard.datos.productos.map(p => p.ganancia_total),
                            backgroundColor: dashboard.datos.productos.map(p => dashboard.obtenerColor(p.id, 0.7)),
                            borderColor: dashboard.datos.productos.map(p => dashboard.obtenerColor(p.id)),
                            borderWidth: 1
                        }]
                    },
                    options: opcionesMini
                });
        }
    }

    // Inicializar miniaturas
    thumbnails.forEach((canvas, index) => {
        canvas.id = `thumb-${index}`;
        crearMiniatura(canvas, tipos[index]);
        canvas.addEventListener('click', () => mostrarGraficoGrande(index));
    });

    // Mostrar primer gráfico grande
    mostrarGraficoGrande(0);
});
