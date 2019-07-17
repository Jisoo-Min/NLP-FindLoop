const cheerio = require('cheerio');
const request  = require('request');
const fs = require('fs');
const probAndLoop = [
  ['simple',0],
  ['array',1],
  ['list',1],
  ['string',1],
  ['dictionary',2],
  ["tuple",0],
  ["searchingandsorting",1],
  ["pattern",2],
  ['datetime',0],
  ['moreprograms',1]
];
//Logic1 및 Logic2는 Loop가 있는지 없는지 재확인 필요.
//만약 Loop가 있을 시 해당 항목을 -1로 변경 후 수작업


const crawl_prob = async function(href,loop){
  return new Promise((resolve,reject)=>{
    request({method:'GET',
     url:'https://codingbat.com/'+href,
    }, (err1,res1,body1)=>{
     let $1 = cheerio.load(body1);
     let speech = $1('.max2').text();
     //console.log(speech);
     resolve({'speech':speech, 'loop':loop});
    });
  });
}
const crawl_chapter = async function(filename,loop){
  return new Promise((resolve,reject)=>{
    request({method:'GET',
     url:'https://www.geeksforgeeks.org/python-programming-examples/',
     }, (err,res,body)=>{
     if(err) return console.error(err);
     for()
     let $ = cheerio.load(body);
     let links = $('table > tbody > tr > td > a').toArray();
     let promises = [];
     let result = [];
      for(let i in links){
          console.log(links[i].attribs.href);
          try{
          console.log(i);
            promises[i] = crawl_prob(links[i].attribs.href,loop);
            promises[i].then((res)=>{
              result[i] = res;
            });
          }
          catch{
          console.log(i+'err');
            promises[i] = crawl_prob(links[i].attribs.href,loop);
            promises[i].then((res)=>{
              result[i] = res;
            });
          }
      }
      Promise.all(promises).then(()=>{
        //console.log(result);

        const createCsvWriter = require('csv-writer').createObjectCsvWriter;
        const csvWriter = createCsvWriter({
          path: 'dataset_'+filename+'.csv',
          header: [
            {id: 'speech', title: 'Speech'},
            {id: 'loop', title: 'Loop'},
          ]
        });
        csvWriter.writeRecords(result);
        /*fs.writeFile('dataset_'+filename+'.json',result,function(err){
          if(err){
            console.log(err);
          }
        });*/
      });
    });
  });
}
for(let i in probAndLoop){
  crawl_chapter(probAndLoop[i][0],probAndLoop[i][1]);
}
/*
{'speech':'Given an array of ints length 3, return a new array with the elements in reverse order, so {1, 2, 3} becomes {3, 2, 1}.','loop':0}
*/
