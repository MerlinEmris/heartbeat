const SUCCESS_CLASS = "success"
const ERROR_CLASS = "danger"
const OTHER_CLASS = 'warning'
const LIST_GROUP = document.getElementById('list-item-container');
const START_BUTTON = document.getElementById('start-btn');

const toggleStartButtonState = (state=!START_BUTTON.disabled) => {
    START_BUTTON.disabled = state
}
const startScanProcess =  ()=>{
    toggleStartButtonState(true);
    fetch('/api/v1/scan/').then(()=>{
        // setTimeout(toggleStartButtonState(false),600)
    }).catch(()=>{
    })
}

/**
 * Add list item to list group
 * @param {{site: {id: number,url: string, name: string}, status:{code: string, type: string, message: string} }} data
 * @param {HTMLAnchorElement} listItem
 */
const addListItem = (data, listItem) => {
    listItem.setAttribute('id', ''+data.site.id)
    const color =  parseInt(data.status['code']) > 199 && parseInt(data.status['code']) < 299  ? SUCCESS_CLASS : parseInt(data.status['code']) > 399 && parseInt(data.status['code']) < 499 ? ERROR_CLASS : OTHER_CLASS
    listItem.setAttribute('class', `list-group-item list-group-item-action container-fluid list-group-item-${color}`);
    listItem.setAttribute('style', 'display: flex; justify-content: space-between;')
    listItem.setAttribute('href', data.site.url )
    listItem.setAttribute('target', '_blank' )
    listItem.setAttribute('rel', 'noreferrer noopener' )
    listItem.innerHTML = `<span>${data.site['id']} ${data.status['type']} ${data.site['url']}</span><span style="display: flex">${data.status['message']}  ${data.status['code']}</span>`
    LIST_GROUP.appendChild(listItem);
};

/**
 * makes toast and show it
 * @param data {{type: string, message: string}}
 */
const makeToast = (data) => {

}


const clearListItems = () => {

};

/**
 * handle status logic
 * @param data {{type: string, message: string}}
 */
const handleStatusInfo = data => {
    if(data.message === 'Scan completed!'){
        toggleStartButtonState(false);
    }
    makeToast(data)
};

/**
 * get element by id or create new one
 * @param id {number}
 * @return {HTMLAnchorElement}
 */
const getOrCreateHTMLAnchorElement = (id) => {
    return !!document.getElementById(''+id) ? document.getElementById(''+id) : document.createElement('a');
}

/**
 * handle logic related with scan data
 * @param {{site: {id: number,url: string, name: string}, status:{code: string, type: string, message: string} } } data
 */
const handleUrlInfo = data => {
    addListItem(data, getOrCreateHTMLAnchorElement(data.site.id))
};

/**
 * handle socket pong
 * @param {{type: 'scan.data' | 'state.info',data: {site: string, status:string } || {type: string, message: string} }} data
 */
const handleResults = data => {
    switch (data.type) {
            case "scan.data":
                 /**
                 * @type {{id: number,url: string, name: string}}
                 */
                const site = JSON.parse(data.data.site)
                /**
                 * @type {{code: string, type: string, message: string}}
                 */
                const status = JSON.parse(data.data.status)
                handleUrlInfo({site,status});
                break;
            case "state.info":
                // console.log('state info', data)
                handleStatusInfo(data.data);
                break
            default:
                // console.log('unknown',data)
                console.error("Unknown message type!");
                break;
        }
};

START_BUTTON.onclick=startScanProcess;
