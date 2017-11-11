var nameFilter = '';
var surnameFilter = '';

function mainFilter() {
    var td;
    var table = document.getElementById('tabulka');
    tr = table.getElementsByTagName('tr');

    for (var i = 0; i < tr.length; i++) {
        nameCol = tr[i].getElementsByTagName('td')[1];
        surnameCol = tr[i].getElementsByTagName('td')[2];

        //Checks if both column are populted
        if (nameCol && surnameCol) {
            if (nameCol.innerHTML.toUpperCase().indexOf(nameFilter) > -1 && surnameCol.innerHTML.toUpperCase().indexOf(surnameFilter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
    window.scrollTo(0,0);
}

function filterByID() {
    var td;
    var table = document.getElementById('tabulka');
    filterID = document.getElementById('inputID').value.toUpperCase();
    tr = table.getElementsByTagName('tr');

    for (var i = 0; i < tr.length; i++) {
        id_Col = tr[i].getElementsByTagName('td')[0];

        //Checks if both column are populted
        if (id_Col) {
            if (id_Col.innerHTML.toUpperCase() == filterID || filterID == "") {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function deleteIDFilter() {
    document.getElementById('inputID').value = "";
}

function menaFilter() {
    nameFilter = document.getElementById('inputName').value.toUpperCase();
    deleteIDFilter();
    mainFilter();
}


function priezvFilter() {
    surnameFilter = document.getElementById('inputSurname').value.toUpperCase();
    deleteIDFilter();
    mainFilter();
}

