const resultsBox = document.querySelector(".result-box");
const inputBox = document.querySelector("#activity");

inputBox.onkeyup = function() {
    let input = inputBox.value;

    if (input.length) {
        fetch(`/gethint?q=${input}`)
            .then(response => response.text())
            .then(data => {
                if (data.trim() === "no suggestion") {
                    resultsBox.innerHTML = '';
                } else {
                    resultsBox.innerHTML = data;
                    let items = resultsBox.querySelectorAll("li");
                    items.forEach(item => {
                        item.onclick = function() {
                            selectInput(this);
                        };
                    });
                }
            });
    } else {
        resultsBox.innerHTML = '';
    }
};

function selectInput(listItem) {
    inputBox.value = listItem.textContent;
    resultsBox.innerHTML = '';
}