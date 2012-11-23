#!/usr/bin/env phantomjs --ignore-ssl-errors=yes

// 
// https://github.com/ariya/phantomjs/blob/master/examples/rasterize.js
//

var fs = require('fs');

var page = new WebPage(),
    address, output, size;

if (phantom.args.length != 3 ) {
    console.log('Usage: urlender.js URL urlsfilename renderfilename');
    phantom.exit();

} else {

    // Open file:
    urlf = fs.open( phantom.args[1], 'w' );

    // Track requests
    page.onResourceRequested = function (request) {
        urlf.writeLine( request.url );
    };

    // Set up parameters
    address = phantom.args[0];
    output = phantom.args[2];
    page.viewportSize = { width: 1024, height: 1024 };
    // These parameters apply to .pdf
    page.paperSize = { format: 'A4', orientation: 'portrait', margin: '1cm' };
    // page.zoomFactor = 

    // Start 
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
        } else {
            window.setTimeout(function () {
                page.render(output);
                urlf.close();
                phantom.exit();
            }, 200);
        }
    });
}
