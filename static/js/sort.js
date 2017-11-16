function swap(firstRow, secondRow) {
    let tempRow = firstRow.innerHTML;
    firstRow.innerHTML = secondRow.innerHTML;
    secondRow.innerHTML = tempRow;
}

function sortTable(colNum, order) {
    var table = document.getElementById('tabulka');
    

    //Bubble sort
    let swapped = true;
    while (swapped) {
        let allRows = table.getElementsByTagName('tr');
        swapped = false;
        // For
        for (let i = 1; i < allRows.length -2 ; i++) {
            if (order === 'asc' && (allRows[i].getElementsByTagName('td')[colNum].innerHTML < allRows[i + 1].getElementsByTagName('td')[colNum].innerHTML)) {
                swap(allRows[i], allRows[i + 1]);
                swapped = true;
            }
            else if (order === 'desc' && (allRows[i].getElementsByTagName('td')[colNum].innerHTML > allRows[i + 1].getElementsByTagName('td')[colNum].innerHTML)) {
                swap(allRows[i], allRows[i + 1]);
                swapped = true;
            }
        }
    }
}