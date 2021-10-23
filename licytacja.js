// ==UserScript==
// @name     Bid Helper
// @version  1
// @grant    none
// @include  https://www.ea.com/pl-pl/*
// ==/UserScript==


let headerInput, btnStartStop, btnOptimal;
let goInterval, correctPrice; // Intervals 

let bid;

let header, navBarek, searchResult, actualPlayer, actualOveral;

const url = 'http://localhost:8000/test.json'; // URL with JSON that contains player data, can be local or remote.

let players; // Object with players

async function fetchData() {
  //Handles JSON file from local or remote server.

  try {

    let response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    players = await response.json();
    console.log(players);



  } catch (e) {

    console.log(e);

  }

}

function getOptimalPrice(player, overall, playersList, buy) {
  // Check if player card is in the array and return apropriet price. If it not change get default from header input.



  if (player && overall && playersList) {
    let list = playersList['players'];
    if (buy) {

      for (let i = 0; i < list.length; i++) {
        if (list[i]['name'] === player && list[i]['overall'] === overall) {
          return list[i]['sugBuy'];
        }
      }


    } else {
      for (let i = 0; i < list.length; i++) {
        if (list[i]['name'] === player && list[i]['overall'] === overall) {
          return list[i]['sugSell'];
        }
      }

    }

    return Number(headerInput.value);



  }
}

function setCurrentCard() {
  //  Set values from curent selected card and inserts price to input fields.
  actualPlayer = document.querySelector('.tns-item.tns-slide-active').childNodes[0].childNodes[4].textContent; // Nazwa na karcie
  actualOveral = document.querySelector('.tns-item.tns-slide-active').childNodes[0].childNodes[7].childNodes[1].childNodes[0].textContent // Overall na karcie

  bid = getOptimalPrice(actualPlayer, actualOveral, players, true);
  changeInput(bid);

}

function getMax(num) {
  //Takes array length and retruns minmax bid
  if (num === 3) {
    return 50;
  } else {
    temp = '1';
    for (let index = 1; index < num - 1; index++) {
      temp += '0';
    }
    return Number(temp);

  }

};

function changeInput(bid_) {
  //Changes input fields with certen bid

  const inputy = document.querySelectorAll('.numericInput');
  if (inputy) {
    inputy.forEach((ele, idx) => {
      if (idx === 0) {
        ele.value = bid_;
      } else {
        ele.value = bid_ + getMax(bid_.toString().length);
      }

    });
  }


}

setTimeout(function () {


  headerInput = document.createElement('input');
  btnStartStop = document.createElement('button');
  btnOptimal = document.createElement('button');
  btnStartStop.textContent = "START";
  btnStartStop.style.backgroundColor = 'green';
  bid = Number(headerInput.value);


  btnStartStop.addEventListener('click', function () {
    btnState = btnStartStop.textContent;
    if (btnState === "START") {
      goInterval = setInterval(function () {
        bid = Number(headerInput.value);
        changeInput(bid);
        console.log("DZIAŁA KURWA");
      }, 500);
      btnStartStop.textContent = "STOP"
      btnStartStop.style.backgroundColor = 'red';

    } else {
      clearInterval(goInterval);
      btnStartStop.textContent = "START"
      btnStartStop.style.backgroundColor = 'green';


    }



  });

  btnOptimal.textContent = "START";
  btnOptimal.style.backgroundColor = 'green';
  btnOptimal.addEventListener('click', function () {
    btnState = btnOptimal.textContent;
    if (btnState === "START") {
      correctPrice = setInterval(function () {
        setCurrentCard();
      }, 500);
      btnOptimal.textContent = "STOP"
      btnOptimal.style.backgroundColor = 'red';

    } else {
      clearInterval(correctPrice);
      btnOptimal.textContent = "START"
      btnOptimal.style.backgroundColor = 'green';


    }



  });


  header = document.querySelector('.ut-fifa-header-view');
  navBarek = document.querySelector('.ut-navigation-bar-view');
  searchResult = document.querySelector('.title');

  header.append(" Wpisz cenę do zakupu/sprzedaży ");
  header.append(headerInput);
  headerInput.value = 450;
  header.append(btnStartStop);
  header.append("   Optymalna cena?   ");
  header.append(btnOptimal);


}, 10000);

fetchData();