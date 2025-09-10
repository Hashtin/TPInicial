document.addEventListener('DOMContentLoaded', () => {
    let currentSlide = 0;
    const slides = document.querySelectorAll('.chart-slide');
    const charts = {}; // para almacenar los objetos Chart ya creados

    if (slides.length === 0) return;

    // Función para mostrar slide y renderizar gráfico si hace falta
    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });

        const canvasId = slides[index].querySelector('canvas').id;
        if (!charts[canvasId]) {
            renderChart(canvasId);
        }
    }

    // Función para crear el gráfico según el id del canvas
    function renderChart(id) {
        const dashboard = new DashboardProductivo();
        dashboard.cargarDatos().then(() => {
            switch(id) {
                case 'chart-efectividad-tiempo':
                    charts[id] = dashboard.crearGraficoEfectividadTiempo();
                    break;
                case 'chart-eficiencia-tiempo':
                    charts[id] = dashboard.crearGraficoEficienciaTiempo();
                    break;
                case 'chart-eficacia-tiempo':
                    charts[id] = dashboard.crearGraficoEficaciaTiempo();
                    break;
                case 'chart-produccion-tiempo':
                    charts[id] = dashboard.crearGraficoProduccionTiempo();
                    break;
                case 'chart-ganancia-producto':
                    charts[id] = dashboard.crearGraficoGananciaProducto();
                    break;
            }
        });
    }

    document.getElementById('prev-slide').addEventListener('click', () => {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    });

    document.getElementById('next-slide').addEventListener('click', () => {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    });

    // Mostrar primer slide
    showSlide(currentSlide);
});
