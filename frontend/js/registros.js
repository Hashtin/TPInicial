document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch(`${API_URL}/registros`);
        const registros = await response.json();

        const tbody = document.querySelector("#tabla-registros tbody");
        tbody.innerHTML = "";

        registros.forEach(r => {
            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td>${r[0]}</td>
                <td>${r[1]}</td>
                <td>${r[2]}</td>
                <td>${r[3]}</td>
                <td>${r[4]}</td>
            `;
            tbody.appendChild(fila);
        });
    } catch (error) {
        console.error("Error cargando registros:", error);
    }
});
