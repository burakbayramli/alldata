
function init() {

    var url = "../globe/g10g1";
    
    fetch(url, {
        headers: {
            'content-type': 'multipart/byteranges',
            'range': 'bytes=2000-2000',
        },
    }).then(response => {
        if (response.ok) {
	    return response.arrayBuffer();
        }
    }).then(response => {
	var a = new Uint8Array(response);
        console.log(a[0]);
    });
    
}
