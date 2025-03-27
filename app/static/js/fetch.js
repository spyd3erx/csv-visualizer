document.getElementById('describeButton').addEventListener('click', function () {
    fetch('/describe', {
      method: 'GET',
    })
      .then(response => response.json())
      .then(data => {
        const describeContent = document.getElementById('describeContent');
        if (describeContent) {
            
            let html = '<div id="table-describe" class="table-container">';
            html += '<table class="table table-striped">';
            html += '<thead><tr><th>Statistic</th>';
            for (const column of Object.keys(data)) {
              html += `<th>${column}</th>`;
            }
            html += '</tr></thead><tbody>';
    
            const stats = Object.keys(data[Object.keys(data)[0]]);
            for (const stat of stats) {
              html += `<tr><td>${stat}</td>`;
              for (const column of Object.keys(data)) {
                html += `<td>${data[column][stat]}</td>`;
              }
              html += '</tr>';
            }
    
            html += '</tbody></table>';
            html += '</div>'; // Cerrar el contenedor
            describeContent.innerHTML = html;
          }
      })
      .catch(error => {
        console.error('Error fetching describe data:', error);
        const describeContent = document.getElementById('describeContent');
        if (describeContent) {
          describeContent.innerHTML = '<p>Error loading data.</p>';
        }
      });
  });