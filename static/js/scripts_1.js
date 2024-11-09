document.addEventListener("DOMContentLoaded", function () {
  function tables(data) {
    const tables = document.querySelector("#tables");
    tables.innerHTML = "";

    for (let i = 0; i < data.length; i++) {
      const peso = Math.round(data[i].pesos[data[i].pesos.length - 1]);
      const bateria = data[i].bateria[data[i].bateria.length - 1];
      tables.innerHTML += `
            <div class="col-lg-6 col-xxl-4 mb-5" id="table_${data[i].id}">
                <div class="card bg-light border-0 h-100">
                        <div class="card-body text-center p-4 p-lg-5 pt-0 pt-lg-0">
                            <div id="numero" class="feature bg-primary bg-gradient text-white rounded-3 mb-4 mt-n4" >${data[i].id}</div>
                                <div class="bottle">
                                    <div class="boca"></div>
                                    <svg width="20px" height="50px" viewBox="0 0 20 50" xmlns="http://www.w3.org/2000/svg">
                                        <polygon class="neck" points="3.5,0 16.5,0 20,50 0,50" fill="#ff0" stroke="none" />
                                        <line x1="4.5" y1="0" x2="15.5" y2="0" stroke="black" stroke-width="1.5" />
                                        <line x1="4.5" y1="0" x2="0" y2="50" stroke="black" stroke-width="1.5" />
                                        <line x1="15.5" y1="0" x2="20" y2="50" stroke="black" stroke-width="1.5" />
                                    </svg>
                                    <div class="body">
                                        <div class="liq"></div>
                                    </div>
                            </div>
                            <p class="porcentagem" id="porcentagem_${data[i].id}">${peso}%</p>
                            <div class="bateria">
                                <div class="carga" id="bateria_${data[i].id}"></div>
                            </div>
                            
                        </div>
                </div>
            </div>`;
      const qtde = document.querySelector(`#table_${data[i].id} .liq`);
      const porc = document.querySelector(`#porcentagem_${data[i].id}`);
      const mesa = document.querySelector(`#table_${data[i].id}`);
      const numero = document.querySelector(`#table_${data[i].id} #numero`);
      //   const msg = document.querySelector(`#mensagem_${data[i].id}`);
      const bat = document.querySelector(`#bateria_${data[i].id}`);

      qtde.style.height = `${peso}%`;
      bat.style.height = `${bateria}%`;

      if (bateria < 20) {
        bat.style.backgroundColor = "red";
      }
      if (peso < 20) {
        qtde.style.backgroundColor = "red";
        // msg.innerText = "TROCAR";
        numero.style.setProperty("background-color", "red", "important");
        mesa.style.borderColor = "red !important";
        porc.style.color = "red";
      }
    }
  }

  function fetchData() {
    fetch("/api/measures")
      .then((response) => response.json())
      .then((data) => {
        tables(data);
      })
      .catch((error) => {
        console.error("Erro ao buscar dados:", error);
      });
  }

  setInterval(fetchData, 1000);
  fetchData();
});
