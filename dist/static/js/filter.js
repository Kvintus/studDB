let nameFilter = '';
let surnameFilter = '';

function mainFilter() {
    let td;
    const table = document.getElementById('tabulka');
    const tr = table.getElementsByTagName('tr');

    for (let i = 0; i < tr.length; i++) {
        const nameCol = tr[i].getElementsByTagName('td')[1];
        const surnameCol = tr[i].getElementsByTagName('td')[2];

        // Checks if both column are populted
        if (nameCol && surnameCol) {
            if (nameCol.innerHTML.toUpperCase().indexOf(nameFilter) > -1 && surnameCol.innerHTML.toUpperCase().indexOf(surnameFilter) > -1) {
                tr[i].style.display = '';
            } else {
                tr[i].style.display = 'none';
            }
        }
    }
    window.scrollTo(0, 0);
}

function filterByID() {
    let td;
    const table = document.getElementById('tabulka');
    const filterID = document.getElementById('inputID').value.toUpperCase();
    const tr = table.getElementsByTagName('tr');

    for (let i = 0; i < tr.length; i++) {
        const idCol = tr[i].getElementsByTagName('td')[0];

        if (idCol) {
            if (idCol.innerHTML.toUpperCase() === filterID || filterID === '') {
                tr[i].style.display = '';
            } else {
                tr[i].style.display = 'none';
            }
        }
    }
}


function deleteIDFilter() {
    document.getElementById('inputID').value = '';
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

