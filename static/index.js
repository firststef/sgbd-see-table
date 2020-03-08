async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return await response.text(); // parses JSON response into native JavaScript objects
}

function getSelectedColumns(){
    let nameArray = [];
    let els = document.getElementsByClassName("table-column-label");
    Array.prototype.forEach.call(els,
        label => {
            let inp = document.getElementById(label.getAttribute("for"));
            if (inp == null)
                return;
            if (!inp.checked)
                return;
            let cnm = inp.value;
            if (cnm == null)
                return;
            nameArray.push(cnm);
        }
    );
    return nameArray;
}

function queryTable(){
    postData('/query_request', { columns: getSelectedColumns() })
        .then((data) => {
            document.getElementById("table-container").innerHTML = data;
        });
}