// ==UserScript==
// @name         JSON TEST
// @version      1.0.4
// @description  Test JSONA
// @author       wkq
// @include      http://example.com/*
// @grant        none
// ==/UserScript==




// sprawdzenie overealla i nazwy zawodnika

const actualPlayer = document.querySelector('.tns-item.tns-slide-active').childNodes[0].childNodes[4].textContent; // Nazwa na karcie
const actualOveral = document.querySelector('.tns-item.tns-slide-active').childNodes[0].childNodes[7].childNodes[1].childNodes[0].textContent // Overall na karcie




const url = 'http://localhost:8000/test.json';

function inicialize(json) {
  //Inicjacja danych

  let players = json['players'];
  players.forEach(element => {
    console.log(element['price']);
    
  });
  


};


async function fetchData() {
  //Pobieranie aktualnego JSONA z lokalnego serwera

  try {

    let response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    let myJson = await response.json();
    inicialize(myJson);

  } catch (e) {

    console.log(e);

  }

}


fetchData();

