/*
=====================================================
 CHAPTER 3: FUNCTIONS
=====================================================

Functions are reusable blocks of code. You've used them in Python:
  def greet(name):
      return f"Hello, {name}!"

JavaScript has MULTIPLE ways to create functions:
  1. Function declaration:  function greet(name) { ... }
  2. Function expression:   const greet = function(name) { ... }
  3. Arrow function:        const greet = (name) => { ... }

Arrow functions are the "modern" way and you'll see them everywhere.

This chapter also covers CALLBACKS and CLOSURES, which are two of the
most important concepts in JavaScript (and common interview questions).

COMING FROM PYTHON:
  def    -> function (or arrow =>)
  *args  -> ...args (rest parameters)
  lambda -> arrow functions (but much more powerful)


HOW TO RUN:
  node ch3_functions.js
*/

// =============================================================================
// PART 1: FUNCTION DECLARATIONS
// =============================================================================
//
// Python:  def greet(name):
//              return f"Hello, {name}!"
//
// JS:      function greet(name) {
//              return `Hello, ${name}!`;
//          }

console.log("=".repeat(50));
console.log("PART 1: Function Declarations");
console.log("=".repeat(50));

function greet(name) {
    return `Hello, ${name}!`;
}

console.log(greet("Chint"));    // Hello, Chint!
console.log(greet("World"));    // Hello, World!

// Functions without a return statement return undefined (Python returns None):
function sayHello(name) {
    console.log(`Hello, ${name}!`);
    // no return statement
}
const result = sayHello("Chint");  // prints "Hello, Chint!"
console.log(`Return value: ${result}`);  // undefined
console.log();


// =============================================================================
// PART 2: FUNCTION EXPRESSIONS
// =============================================================================
//
// You can assign a function to a variable. This is a "function expression."
// The function itself has no name (it's "anonymous").
//
// Why? In JavaScript, functions are "first-class citizens" - they can be
// stored in variables, passed as arguments, and returned from other functions.
// Python also has this (with lambda and regular functions).

console.log("=".repeat(50));
console.log("PART 2: Function Expressions");
console.log("=".repeat(50));

const add = function(a, b) {
    return a + b;
};  // Note the semicolon! It's a variable assignment.

console.log(`add(3, 5) = ${add(3, 5)}`);

// Functions stored in variables can be passed around:
const myFunc = add;  // myFunc now points to the same function
console.log(`myFunc(10, 20) = ${myFunc(10, 20)}`);
console.log();


// =============================================================================
// PART 3: ARROW FUNCTIONS - THE MODERN WAY
// =============================================================================
//
// Arrow functions are a shorter syntax introduced in ES6 (2015).
// They're like Python's lambda but way more powerful and commonly used.
//
// Python lambda:  square = lambda x: x ** 2
// JS arrow:       const square = (x) => x ** 2;
//
// Full syntax:    const fn = (params) => { statements; return value; }
// Short syntax:   const fn = (params) => expression  (implicit return!)
// Single param:   const fn = x => x * 2  (parentheses optional!)

console.log("=".repeat(50));
console.log("PART 3: Arrow Functions");
console.log("=".repeat(50));

// Full arrow function (with curly braces, you need explicit return):
const multiply = (a, b) => {
    const result = a * b;
    return result;
};

// Short arrow function (single expression = implicit return, no braces needed):
const square = (x) => x ** 2;

// Single parameter: parentheses are optional:
const double = x => x * 2;

// No parameters: must use empty parentheses:
const sayHi = () => "Hi!";

console.log(`multiply(3, 4) = ${multiply(3, 4)}`);
console.log(`square(5) = ${square(5)}`);
console.log(`double(7) = ${double(7)}`);
console.log(`sayHi() = ${sayHi()}`);
console.log();


// =============================================================================
// PART 4: DEFAULT PARAMETERS AND REST PARAMETERS
// =============================================================================
//
// Default params work the same as Python.
// Rest params (...args) are like Python's *args.

console.log("=".repeat(50));
console.log("PART 4: Default & Rest Parameters");
console.log("=".repeat(50));

// --- Default parameters (same concept as Python) ---
// Python: def greet(name, greeting="Hello"):
// JS:     function greet(name, greeting = "Hello") {
function greetPerson(name, greeting = "Hello") {
    return `${greeting}, ${name}!`;
}
console.log(greetPerson("Chint"));             // Hello, Chint!
console.log(greetPerson("Chint", "Howdy"));    // Howdy, Chint!

// --- Rest parameters (...args) ---
// Python: def sum_all(*args):
// JS:     function sumAll(...args) {
//
// The ... (spread/rest operator) collects all remaining arguments into an array.
function sumAll(...numbers) {
    let total = 0;
    for (const num of numbers) {
        total += num;
    }
    return total;
}
console.log(`sumAll(1, 2, 3) = ${sumAll(1, 2, 3)}`);       // 6
console.log(`sumAll(10, 20, 30, 40) = ${sumAll(10, 20, 30, 40)}`); // 100

// Rest params must be LAST (same rule as Python's *args):
function introduce(greeting, ...names) {
    return `${greeting}: ${names.join(", ")}`;
}
console.log(introduce("Meet the team", "Alice", "Bob", "Charlie"));
console.log();


// =============================================================================
// PART 5: CALLBACKS - FUNCTIONS PASSED TO OTHER FUNCTIONS
// =============================================================================
//
// A CALLBACK is a function you pass as an argument to another function.
// The receiving function will "call back" your function at the right time.
//
// This is CRITICAL in JavaScript. Everything uses callbacks:
//   - Array methods (map, filter, forEach)
//   - Event handlers (click, submit)
//   - Async operations (API calls, timers)
//
// Python has this too (map, filter, sorted with key=), but JS relies on it
// much more heavily.

console.log("=".repeat(50));
console.log("PART 5: Callbacks");
console.log("=".repeat(50));

// A simple callback example:
function doMath(a, b, operation) {
    return operation(a, b);  // Calls whatever function was passed in
}

const addNums = (a, b) => a + b;
const subtractNums = (a, b) => a - b;

console.log(`doMath(10, 3, add) = ${doMath(10, 3, addNums)}`);
console.log(`doMath(10, 3, sub) = ${doMath(10, 3, subtractNums)}`);

// You can also pass the function directly (inline, anonymous):
console.log(`doMath(10, 3, multiply) = ${doMath(10, 3, (a, b) => a * b)}`);

// Real-world callback example - setTimeout (run code after a delay):
// Python: time.sleep(1) then run code (blocking)
// JS:     setTimeout(callback, delay) (non-blocking! More in ch6)
console.log("\nsetTimeout example (runs after 100ms):");
setTimeout(() => {
    console.log("  This message appeared after a short delay!");
}, 100);

// Array methods use callbacks everywhere (more detail in ch4):
const nums = [1, 2, 3, 4, 5];
const doubled = nums.map(n => n * 2);     // Like Python: [n*2 for n in nums]
const evens = nums.filter(n => n % 2 === 0); // Like Python: [n for n in nums if n%2==0]
console.log(`doubled: [${doubled}]`);
console.log(`evens:   [${evens}]`);
console.log();


// =============================================================================
// PART 6: CLOSURES - FUNCTION REMEMBERS ITS SCOPE
// =============================================================================
//
// A CLOSURE is when a function "remembers" variables from the scope where
// it was created, even after that scope has finished executing.
//
// Analogy: Imagine you're in a room (scope) with a whiteboard (variable).
// You take a photo (closure) of the whiteboard. Even after you leave the room,
// you can still see the whiteboard in your photo.
//
// This is a COMMON INTERVIEW QUESTION.

console.log("=".repeat(50));
console.log("PART 6: Closures");
console.log("=".repeat(50));

// Example 1: Counter factory
function makeCounter() {
    let count = 0;  // This variable is "enclosed" in the returned function
    return function() {
        count++;    // The inner function can still access and modify count!
        return count;
    };
}

const counter = makeCounter();
console.log(`counter(): ${counter()}`);  // 1
console.log(`counter(): ${counter()}`);  // 2
console.log(`counter(): ${counter()}`);  // 3
// Each call increments the SAME count variable. It's "trapped" in the closure.

// Example 2: Private variables (JS doesn't have private keyword in functions)
function createPerson(name) {
    // name is "private" - only accessible through the returned methods
    return {
        getName: () => name,
        setName: (newName) => { name = newName; },
    };
}

const person = createPerson("Chint");
console.log(`getName(): ${person.getName()}`);  // Chint
person.setName("Bob");
console.log(`getName(): ${person.getName()}`);  // Bob
// There's no way to access 'name' directly - only through these functions.

// Example 3: Closure in a loop (classic gotcha)
console.log("\nClosure in loop (correct with let):");
for (let i = 0; i < 3; i++) {
    setTimeout(() => console.log(`  i = ${i}`), 10);
}
// Prints 0, 1, 2 (correct! because let creates a new scope each iteration)
// With var, this would print 3, 3, 3 (the classic closure bug)
console.log();


// =============================================================================
// PART 7: IIFE (Immediately Invoked Function Expression)
// =============================================================================
//
// An IIFE is a function that runs immediately when defined.
// It creates a private scope (useful before ES6 modules existed).
//
// You might see this in older code or libraries.

console.log("=".repeat(50));
console.log("PART 7: IIFE");
console.log("=".repeat(50));

// Regular function: define, then call separately
// IIFE: define AND call in one step

const iiifeResult = (function() {
    const secret = "I'm private!";
    return secret.toUpperCase();
})();  // <-- These () at the end INVOKE it immediately

console.log(`IIFE result: ${iiifeResult}`);  // I'M PRIVATE!
// console.log(secret);  // ERROR! secret doesn't exist out here.

// Arrow function IIFE:
const sum = ((a, b) => a + b)(3, 4);
console.log(`Arrow IIFE: ${sum}`);
console.log();


// =============================================================================
// PART 8: HOISTING
// =============================================================================
//
// "Hoisting" means JavaScript moves declarations to the top of their scope
// BEFORE running the code. This affects var and function declarations.
//
// Python doesn't have hoisting - if you try to use something before
// defining it, you get a NameError. JS is more permissive (and confusing).

console.log("=".repeat(50));
console.log("PART 8: Hoisting");
console.log("=".repeat(50));

// Function declarations are FULLY hoisted (you can call them before defining):
console.log(`hoistedFunc(): ${hoistedFunc()}`);  // Works!
function hoistedFunc() {
    return "I was called before my definition!";
}

// Function expressions and arrow functions are NOT hoisted:
// console.log(notHoisted());  // ERROR! notHoisted is not defined
// const notHoisted = () => "I can't be called before my line";

// var is hoisted but NOT initialized (value is undefined until assigned):
console.log(`hoistedVar: ${hoistedVar}`);  // undefined (not an error!)
var hoistedVar = "Now I have a value";
console.log(`hoistedVar: ${hoistedVar}`);  // "Now I have a value"

// let and const are NOT hoisted (well, technically they are, but you can't
// access them before their declaration - it's called the "Temporal Dead Zone"):
// console.log(notHoistedLet);  // ERROR! Cannot access before initialization
// let notHoistedLet = "I'm let";

console.log("\nHoisting summary:");
console.log("  function declarations -> fully hoisted (can call before definition)");
console.log("  var                   -> hoisted but undefined until assigned");
console.log("  let/const             -> NOT accessible before declaration (TDZ)");
console.log("  arrow functions       -> NOT hoisted (they're const/let expressions)");
console.log();


// =============================================================================
// PART 9: PRACTICAL EXAMPLES
// =============================================================================

console.log("=".repeat(50));
console.log("PART 9: Practical Examples");
console.log("=".repeat(50));

// A reusable greeting function with options:
const createGreeter = (greeting) => {
    return (name) => `${greeting}, ${name}!`;
};

const helloGreeter = createGreeter("Hello");
const howdyGreeter = createGreeter("Howdy");
console.log(helloGreeter("Chint"));  // Hello, Chint!
console.log(howdyGreeter("Chint"));  // Howdy, Chint!

// A simple pipe function (compose functions left to right):
const pipe = (...fns) => (x) => fns.reduce((val, fn) => fn(val), x);

const addOne = x => x + 1;
const doubleIt = x => x * 2;
const subtractThree = x => x - 3;

const transform = pipe(addOne, doubleIt, subtractThree);
console.log(`pipe(addOne, double, subThree)(5) = ${transform(5)}`);
// 5 -> 6 -> 12 -> 9
console.log();


// =============================================================================
// QUICK REFERENCE
// =============================================================================
//
// Declaration:   function name(params) { return value; }
// Expression:    const name = function(params) { return value; };
// Arrow:         const name = (params) => expression;
// Arrow (full):  const name = (params) => { statements; return value; };
//
// Default param: function fn(x = 10) { }
// Rest params:   function fn(...args) { }  (like Python's *args)
//
// Callback:      function doStuff(callback) { callback(); }
// Closure:       Inner function remembers outer scope variables
// IIFE:          (function() { ... })()
//
// Hoisting:      function declarations -> hoisted
//                var -> hoisted (undefined)
//                let/const/arrow -> NOT accessible before declaration
//
// PYTHON -> JS:
//   def fn(x):     -> function fn(x) { } or const fn = (x) => { }
//   lambda x: x+1  -> x => x + 1  (but arrow functions can be multi-line!)
//   *args           -> ...args
//   return None     -> return undefined (or just no return statement)
//
// =============================================================================
