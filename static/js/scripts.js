document.addEventListener("DOMContentLoaded", function () {
  function tables(data) {
    const tables = document.querySelector("#tables");
    tables.innerHTML = "";

    for (let i = 0; i < data.length; i++) {
      const peso = Math.round(data[i].pesos[data[i].pesos.length - 1]);
      const bateria = data[i].bateria[data[i].bateria.length - 1];
      tables.innerHTML += `
            <div class="col-4 col-lg-2 col-xxl-2 mb-1" style="border-radius: 10px; max-width: fit-content;" id="table_${data[i].id}">
              <div class="liq">
                <div id="numero" class="feature bg-primary bg-gradient text-white rounded-3" style="position=absolute;">${data[i].id}</div>
                <img src="static/garrafa_png2.png" class="img-fluid"/>
                <p class="porcentagem" id="porcentagem_${data[i].id}">${peso}%</p>
                <div class="bateria">
                                <div class="carga" id="bateria_${data[i].id}"></div>
                </div>
              </div>
            </div>`;
      const qtde = document.querySelector(`#table_${data[i].id} .liq`);
      const porc = document.querySelector(`#porcentagem_${data[i].id}`);
      // const mesa = document.querySelector(`#table_${data[i].id}`);
      const numero = document.querySelector(`#table_${data[i].id} #numero`);
      // //   const msg = document.querySelector(`#mensagem_${data[i].id}`);
      const bat = document.querySelector(`#bateria_${data[i].id}`);

      // qtde.style.height = `${peso}%`;
      bat.style.height = `${bateria}%`;

      if (bateria < 20) {
        bat.style.backgroundColor = "red";
      }
      if (peso < 20) {
        qtde.style.background = `linear-gradient(to bottom, white 50% , red )`;
        // msg.innerText = "TROCAR";
        numero.style.setProperty("background-color", "red", "important");
        // mesa.style.borderColor = "red !important";
        porc.style.color = "red";
      } else if (peso < 50) {
        qtde.style.background = "linear-gradient(to bottom, white 30%, orange)";
      } else {
        qtde.style.background =
          "linear-gradient(to bottom, white 10%, rgb(248, 229, 68))";
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

  setInterval(fetchData, 100000);
  fetchData();
});
