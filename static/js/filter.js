function menaFilter() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("inputMeno");
    filter = input.value.toUpperCase();
    table = document.getElementById("tabulka");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function priezvFilter() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("inputPriezv");
    filter = input.value.toUpperCase();
    table = document.getElementById("tabulka");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[2];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                console.log(td.innerHTML.toUpperCase().indexOf(filter))
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}
