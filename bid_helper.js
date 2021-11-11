// ==UserScript==
// @name     Bid Helper
// @version  1
// @grant    none
// @include  https://www.ea.com/pl-pl/*
// ==/UserScript==


let headerInput, btnStartStop, btnOptimal;
let goInterval, correctPrice; // Intervals 

let bid;

let header, oppInput, actualPlayer, actualOveral, desiredValueInp;

const url = 'http://localhost:8000/players_data.json'; // URL with JSON that contains player data, can be local or remote.

let players; // Object with players dictionary

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

function addStar(checkbox, header, times = 1) {
  //Takes refrence of checkbox and string to add star
  if (checkbox.checked) {
    if (!header.classList.contains("ON")) {
      header.classList.toggle("ON");
      for (let i = 0; i < times; i++) {
        header.textContent += " ★ ";
      };
    }
  }

};



function highlightPlayer(players, value) {
  //Highlights players over certin price

  if (players) {

    if (oppInput.checked) { // Check if checkbox is checked

      const allEntities = document.querySelectorAll('.entityContainer');
      const list = players['players'];

      allEntities.forEach(function (cNode) {
        for (let i = 0; i < list.length; i++) {
          const playerName = cNode.childNodes[1];
          if (list[i]['name'] === playerName.textContent) {
            if (list[i]['price'] >= value) {
              addStar(oppInput, playerName);


            }            
          }

        }
    

      });

    }
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

    return Number(headerInput.value); // If player not found get value from header

  }
}

function buyOrSell() {
  // Checks headline to determine what to do
  const bidButton = document.querySelector(".bidButton");
  const searchResult = document.querySelector('.title');
  // If we have a bidButton we definitely have an auction
  if (bidButton) {
    return true;
  };
  if (searchResult.textContent === "LISTA TRANSFEROWA" || searchResult.textContent === "Obserwowane") {
    return false;
  }
  return null;

}

function setCurrentCard() {
  //  Set values from curent selected card and inserts price to input fields.
  actualPlayer = document.querySelector('.tns-item.tns-slide-active').childNodes[0].childNodes[4].textContent; // Nazwa na karcie
  actualOveral = document.querySelector('.tns-item.tns-slide-active').childNodes[0].childNodes[7].childNodes[1].childNodes[0].textContent // Overall na karcie


  let action = buyOrSell();
  if (action !== null) {
    bid = getOptimalPrice(actualPlayer, actualOveral, players, action);
    changeInput(bid);
  }

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

  // Creating interface
  headerInput = document.createElement('input');
  btnStartStop = document.createElement('button');
  btnOptimal = document.createElement('button');
  btnStartStop.textContent = "START";
  btnStartStop.style.backgroundColor = 'green';
  oppInput = document.createElement('input');
  oppInput.type = "checkbox";
  desiredValueInp = document.createElement('input');
  desiredValueInp.value = 0;


  bid = Number(headerInput.value);


  btnStartStop.addEventListener('click', function () {
    btnState = btnStartStop.textContent;
    if (btnState === "START") {
      goInterval = setInterval(function () {
        bid = Number(headerInput.value);
        changeInput(bid);
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
        highlightPlayer(players, desiredValueInp.value);
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
  header.append("  Cena stała  ");
  header.append(headerInput);
  headerInput.value = 450;
  header.append(btnStartStop);
  header.append("   Optymalna cena?   ");
  header.append(btnOptimal);
  header.append("   Zaznaczać okazje?   ");
  header.append(oppInput);
  header.append("   Wpisz minimalną szukaną wartość   ");
  header.append(desiredValueInp);
  


}, 10000);

fetchData();