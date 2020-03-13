var orderDict = {};

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

function getFilters(){
    var filters = {};
    let els = document.getElementsByClassName("filter-box");
    Array.prototype.forEach.call(els,
        filter => {
           let cnm = filter.value.toString();
            filters[filter.getAttribute("for")] = cnm;
        }
    );
    return filters;
}

function queryTable(){
    postData('/query_request', { columns: getSelectedColumns(), filters: getFilters(), sort: orderDict})
        .then((data) => {
            document.getElementById("table-container").innerHTML = data;
        });
}

function selectOrder(column, what){
    orderDict[column] = what;
    console.log(orderDict);
}