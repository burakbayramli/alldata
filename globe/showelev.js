'use strict';
var path= require('path');
var fs= require('fs');
// Create g10g by cat g10g1 g10g2 g10g3 g10g4 > g10g
var resolution= 120;

var dataFiles= [
    // ...
    { name: 'g10g', latMin:     0, latMax:     50, lngMin:      0, lngMax:     90, elMin:   -407, elMax:    8752, columns:    10800, rows:   6000 }
    // ...
];

var baseDir = '.';

function findFile( lng, lat ) {
    for ( var i in dataFiles ) {
        var df= dataFiles[i];
        if (df.latMin <= lat && df.latMax > lat && df.lngMin <= lng && df.lngMax > lng) {
            return df;
        }
    }
}

function fileIndex( lng, lat, fileEntry, resolution ) {
    var column= Math.floor(lng * resolution);
    var row= Math.floor(lat * resolution);
    var rowIndex= row - fileEntry.latMin * resolution;
    var columnIndex= column - fileEntry.lngMin * resolution;
    var index= ((fileEntry.rows - rowIndex - 1) * fileEntry.columns + columnIndex) * 2;
    return index;
};

function openFile( name ) {
    return fs.openSync(baseDir + '/' + name , 'r');
}

function readNumberFromFile(name,position) {

    var buffer= new Buffer(2);

    var fd = openFile(name);
    if ( fs.readSync(fd, buffer, 0, 2, position) !== 2 ) return new Error('Could not fetch value from file');

    var int16= buffer.readInt16LE(0);
    
    // return 0 for oceans
    return int16 === -500 ? 0 : int16;
}

function getElevation( lng, lat, onError ) {
    var fileEntry= findFile(lng, lat);
    var result= readNumberFromFile(fileEntry.name, fileIndex(lng, lat, fileEntry, resolution));

    return result;
};

// 40.24157520289902, 28.903099362154144 - 66
// 40.26766536150578, 28.93888732350262 - 75

// var res = fileIndex(28.903099362154144,40.24157520289902,dataFiles[0],120);
var res = getElevation(28.903099362154144,40.24157520289902);
console.log(res);
var res = getElevation(40.26766536150578, 28.93888732350262);
console.log(res);
