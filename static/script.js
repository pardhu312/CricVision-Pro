console.log("JavaScript Loaded");
let searchBox = document.getElementById("search");
searchBox.addEventListener("input",function(){
    let searchText = searchBox.value.toLowerCase();
    let playerCards = document.querySelectorAll(".all-players");
    for (let card of playerCards) {
        let playerName = card.querySelector("h3").textContent.toLowerCase();
        if (playerName.includes(searchText)){
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    }
});