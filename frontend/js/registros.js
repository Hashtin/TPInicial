document.addEventListener("DOMContentLoaded", async () => {
    const tbody = document.querySelector("#tabla-registros tbody");
    try {
        const response = await fetch(`${API_URL}/registros`);
        if (!response.ok) throw new Error("Error HTTP " + response.status);

        const registros = await response.json(); // ya es lista de listas

        if (registros.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5">No hay registros para mostrar</td></tr>`;
        } else {
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
        }
    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="5" style="color:red;">Error cargando registros: ${error.message}</td></tr>`;
        console.error(error);
    }
});
