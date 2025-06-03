function showHint(str) {
    if (str.length == 0) { 
        document.getElementById("txtHint").innerHTML = "";
        return;
    }

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        const txtHint = document.getElementById("txtHint");
        txtHint.innerHTML = this.responseText;

        // Make suggestions clickable
        txtHint.querySelectorAll("li").forEach(item => {
            item.onclick = function() {
                document.getElementById("activity").value = this.innerText;
                txtHint.innerHTML = "";
            }
        });
    }
    xhttp.open("GET", "/gethint?q=" + encodeURIComponent(str));
    xhttp.send();   
}


document.addEventListener("DOMContentLoaded", function() {
    const input = document.getElementById("activity");
    if (input) {
        input.addEventListener("keyup", function() {
            showHint(this.value);
        });
    }
});