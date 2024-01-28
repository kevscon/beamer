
// var script = document.createElement('script');
// script.src = 'https://code.jquery.com/jquery-3.6.3.min.js'; // Check https://jquery.com/ for the current version
// document.getElementsByTagName('head')[0].appendChild(script);
//
// // how to use jquery?
// function loadFactors() {
//   $.getJSON('result.json')
//   .done( function(data) {
//     console.log(data);
//   });
// }
//
//
// function fun1(b) {
//   console.log("1st function running...");
//   let a = b + 1;
//   return a;
// }
//
// function fun2() {
//   console.log("1st function complete, running 2nd");
// }
//
// loadFactors();

async function getPersonsInfo(name) {
  console.log('starting...');
  const people = await server.getPeople();
  console.log('got the people!')
  const person = people.find(person => { return person.name === name });
  // return person;
  console.log(person);
}

const server = {
  people: [
    {
      name: "Odin",
      age: 20,
    },
    {
      name: "Thor",
      age: 35,
    },
    {
      name: "Freyja",
      age: 29,
    },
  ],

  getPeople() {
    return new Promise((resolve, reject) => {
      // Simulating a delayed network call to the server
      setTimeout(() => {
        resolve(this.people);
      }, 2000);
    });
  },
};

getPersonsInfo('Odin');
