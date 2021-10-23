// ==UserScript==
// @name     Bid Helper
// @version  1
// @grant    none
// @include  https://www.ea.com/pl-pl/*
// ==/UserScript==


let headerInput, btnStartStop;
let goInterval;

let bid;

let header, navBarek, searchResult;

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



function changeInput() {



  bid = Number(headerInput.value);
  const inputy = document.querySelectorAll('.numericInput');
  if (inputy) {
    inputy.forEach((ele, idx) => {
      if (idx === 0) {
        ele.value = bid;
      } else {
        ele.value = bid + getMax(bid.toString().length);


      }

    });
  }


}


setTimeout(function () {
  headerInput = document.createElement('input');
  btnStartStop = document.createElement('button');
  btnStartStop.textContent = "START";
  btnStartStop.style.backgroundColor = 'green';
  
  btnStartStop.addEventListener('click', function() {
    btnState = btnStartStop.textContent;
    if(btnState ==="START"){
      goInterval = setInterval(function () {
        changeInput();
        console.log("DZIAŁA KURWA");
      }, 500);
      btnStartStop.textContent ="STOP"
      btnStartStop.style.backgroundColor = 'red';

    }
    else {
      clearInterval(goInterval);
      btnStartStop.textContent ="START"
      btnStartStop.style.backgroundColor = 'green';


    }



  });

  header = document.querySelector('.ut-fifa-header-view');
  navBarek = document.querySelector('.ut-navigation-bar-view');
  searchResult = document.querySelector('.title');

  header.append(" Wpisz cenę do zakupu/sprzedaży ");
  header.append(headerInput);
  headerInput.value = 450;
  header.append(btnStartStop);


}, 10000);





