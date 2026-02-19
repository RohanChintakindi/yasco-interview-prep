/*
=====================================================
 CHAPTER 7: ES6+ FEATURES - MODERN JAVASCRIPT
=====================================================

ES6 (ECMAScript 2015) was a MASSIVE update to JavaScript. It's when JS
went from "quirky language people tolerated" to "powerful modern language
people actually enjoy." Almost all modern JS code uses ES6+ features.

This chapter covers both recaps of things you've seen and NEW features:
  - Modules (import/export)
  - Classes (like Python classes)
  - Symbols, Iterators, Generators
  - Map and Set
  - Advanced destructuring and spread

COMING FROM PYTHON:
  Most of these features exist in Python already. The JS versions
  are often inspired by Python, so you'll find the concepts familiar.


HOW TO RUN:
  node ch7_es6_plus_features.js
*/

// =============================================================================
// PART 1: LET/CONST RECAP + ADVANCED PATTERNS
// =============================================================================

console.log("=".repeat(50));
console.log("PART 1: let/const Advanced Patterns");
console.log("=".repeat(50));

// const with objects/arrays: the REFERENCE is constant, not the contents!
// This is the same as Python: if you do  x = [1,2,3]  you can still append to x.
const person = { name: "Chint", age: 25 };
person.age = 26;             // This is OK! Modifying the object's contents.
// person = { name: "Bob" }; // ERROR! Can't reassign the variable itself.
console.log("const object (modified):", person);

const arr = [1, 2, 3];
arr.push(4);                 // OK! Array contents can change.
// arr = [5, 6, 7];          // ERROR! Can't reassign.
console.log("const array (modified):", arr);

// To make a truly immutable object, use Object.freeze():
const frozen = Object.freeze({ x: 1, y: 2 });
frozen.x = 99;  // Silently fails (no error, but no change)
console.log("Frozen object:", frozen);  // { x: 1, y: 2 } - unchanged
console.log();


// =============================================================================
// PART 2: ADVANCED DESTRUCTURING
// =============================================================================

console.log("=".repeat(50));
console.log("PART 2: Advanced Destructuring");
console.log("=".repeat(50));

// Nested destructuring:
const company = {
    name: "TechCorp",
    address: {
        street: "123 Main St",
        city: "NYC",
        zip: "10001",
    },
    employees: ["Alice", "Bob", "Charlie"],
};

const { name: companyName, address: { city, zip }, employees: [firstEmployee] } = company;
console.log(`Company: ${companyName}`);
console.log(`City: ${city}, Zip: ${zip}`);
console.log(`First employee: ${firstEmployee}`);

// Destructuring with rename + default:
const { role = "developer", name: empName = "Unknown" } = { name: "Alice" };
console.log(`${empName}, role: ${role}`);

// Swap variables without a temp (like Python's a, b = b, a):
let a = 1, b = 2;
[a, b] = [b, a];
console.log(`Swapped: a=${a}, b=${b}`);

// Destructuring function return values:
function getMinMax(arr) {
    return { min: Math.min(...arr), max: Math.max(...arr) };
}
const { min, max } = getMinMax([3, 1, 4, 1, 5, 9]);
console.log(`Min: ${min}, Max: ${max}`);
console.log();


// =============================================================================
// PART 3: ADVANCED SPREAD/REST
// =============================================================================

console.log("=".repeat(50));
console.log("PART 3: Advanced Spread/Rest");
console.log("=".repeat(50));

// Rest in destructuring (extract some, collect the rest):
const { name: pName, ...otherProps } = { name: "Chint", age: 25, city: "NYC" };
console.log(`Name: ${pName}`);
console.log("Rest:", otherProps);  // { age: 25, city: "NYC" }

// Conditional spread (add properties conditionally):
const isAdmin = true;
const user = {
    name: "Chint",
    ...(isAdmin && { role: "admin", permissions: ["read", "write"] }),
};
console.log("Conditional spread:", user);

// Merging with override:
const defaults = { theme: "dark", lang: "en", fontSize: 14 };
const userPrefs = { lang: "es" };
const config = { ...defaults, ...userPrefs };
console.log("Merged config:", config);
console.log();


// =============================================================================
// PART 4: MODULES (import/export)
// =============================================================================
//
// Python: from math import sqrt     or    import os
// JS:     import { sqrt } from 'math'  or  import os from 'os'
//
// NOTE: To use import/export in Node.js, you need EITHER:
//   1. Name your files .mjs (ES module extension)
//   2. Add "type": "module" to package.json
//   3. Use require() instead (CommonJS, the Node.js default)
//
// We'll explain the concepts here without running import/export
// (since this is a single .js file).

console.log("=".repeat(50));
console.log("PART 4: Modules (import/export)");
console.log("=".repeat(50));

console.log(`
  ES MODULES (the standard):
  ---------------------------
  // math.js (exporting)
  export function add(a, b) { return a + b; }
  export function subtract(a, b) { return a - b; }
  export default class Calculator { ... }

  // main.js (importing)
  import Calculator from './math.js';           // Default import
  import { add, subtract } from './math.js';    // Named imports
  import { add as sum } from './math.js';       // Rename on import
  import * as math from './math.js';            // Import everything

  COMMONJS (Node.js traditional way):
  ------------------------------------
  // math.js
  module.exports = { add, subtract };
  // OR: exports.add = function(a, b) { ... };

  // main.js
  const { add, subtract } = require('./math');
  const math = require('./math');

  PYTHON EQUIVALENTS:
    export function add      ->  def add (just define it in the module)
    export default           ->  the "main" thing in a module
    import { add }           ->  from module import add
    import * as math         ->  import module as math
    require('./math')        ->  import math (CommonJS)
`);
console.log();


// =============================================================================
// PART 5: CLASSES
// =============================================================================
//
// JavaScript classes work similarly to Python classes.
// Under the hood, JS classes are syntactic sugar over "prototypes"
// (an older OOP system), but you don't need to know that to use them.
//
// Python:                      JS:
//   class Dog:                   class Dog {
//       def __init__(self, n):       constructor(name) {
//           self.name = n                this.name = name;
//       def bark(self):              }
//           print("Woof!")           bark() {
//                                        console.log("Woof!");
//                                    }
//                                  }

console.log("=".repeat(50));
console.log("PART 5: Classes");
console.log("=".repeat(50));

class Animal {
    // Constructor (like Python's __init__)
    constructor(name, sound) {
        this.name = name;    // this = self in Python
        this.sound = sound;
    }

    // Method (no "function" keyword needed!)
    speak() {
        console.log(`  ${this.name} says ${this.sound}!`);
    }

    // Getter (like Python's @property):
    get info() {
        return `${this.name} (${this.sound})`;
    }

    // Setter:
    set nickname(value) {
        this._nickname = value;
    }

    // Static method (like Python's @staticmethod):
    static kingdom() {
        return "Animalia";
    }

    // toString (like Python's __str__):
    toString() {
        return `Animal(${this.name})`;
    }
}

const dog = new Animal("Rex", "Woof");  // "new" keyword required!
dog.speak();                             // Rex says Woof!
console.log(`Info: ${dog.info}`);        // Uses getter
console.log(`Kingdom: ${Animal.kingdom()}`);  // Static method
console.log(`toString: ${dog}`);          // Uses toString

// --- Inheritance (like Python's class Dog(Animal):) ---
class Dog extends Animal {
    constructor(name, breed) {
        super(name, "Woof");  // Call parent constructor (like Python's super().__init__)
        this.breed = breed;
    }

    // Override parent method:
    speak() {
        super.speak();  // Call parent's speak first
        console.log(`  (${this.name} wags tail)`);
    }

    fetch(item) {
        console.log(`  ${this.name} fetches the ${item}!`);
    }
}

console.log("\nDog (extends Animal):");
const myDog = new Dog("Buddy", "Golden Retriever");
myDog.speak();
myDog.fetch("ball");
console.log(`  instanceof Dog: ${myDog instanceof Dog}`);        // true
console.log(`  instanceof Animal: ${myDog instanceof Animal}`);  // true

// Private fields (ES2022) - like Python's name-mangling with __:
class BankAccount {
    #balance;  // Private field! Cannot be accessed outside the class.

    constructor(initialBalance) {
        this.#balance = initialBalance;
    }

    deposit(amount) {
        this.#balance += amount;
        console.log(`  Deposited $${amount}. Balance: $${this.#balance}`);
    }

    get balance() {
        return this.#balance;
    }
}

console.log("\nBankAccount with private fields:");
const account = new BankAccount(100);
account.deposit(50);
console.log(`  Balance via getter: $${account.balance}`);
// console.log(account.#balance);  // SyntaxError! Private field.
console.log();


// =============================================================================
// PART 6: SYMBOLS
// =============================================================================
//
// Symbols are unique identifiers. They're used for:
//   1. Guaranteed-unique property keys (no name collisions)
//   2. Built-in language behaviors (Symbol.iterator, Symbol.toPrimitive)
//
// Python doesn't have a direct equivalent, but it's like using
// unique sentinel values.

console.log("=".repeat(50));
console.log("PART 6: Symbols");
console.log("=".repeat(50));

const sym1 = Symbol("description");
const sym2 = Symbol("description");
console.log(`sym1 === sym2: ${sym1 === sym2}`);  // false! Each Symbol is unique.
console.log(`typeof sym1: ${typeof sym1}`);       // "symbol"

// Using Symbols as object keys (guaranteed no collisions):
const ID = Symbol("id");
const userObj = {
    [ID]: 12345,       // Symbol key (not visible in normal iteration)
    name: "Chint",
};
console.log(`Symbol key: ${userObj[ID]}`);
console.log(`Object.keys:`, Object.keys(userObj));  // ["name"] - Symbol hidden!
console.log();


// =============================================================================
// PART 7: ITERATORS AND GENERATORS
// =============================================================================
//
// Generators in JS work like Python generators: they use yield to
// produce values one at a time (lazy evaluation).
//
// Python: def count():    JS: function* count() {
//             yield 1              yield 1;
//             yield 2              yield 2;
//             yield 3              yield 3;
//                              }

console.log("=".repeat(50));
console.log("PART 7: Iterators & Generators");
console.log("=".repeat(50));

// Generator function (note the * after "function"):
function* fibonacci() {
    let a = 0, b = 1;
    while (true) {
        yield a;           // Pause here, return 'a', resume on next call
        [a, b] = [b, a + b];
    }
}

// Using a generator:
const fib = fibonacci();
console.log("Fibonacci (generator):");
for (let i = 0; i < 10; i++) {
    process.stdout.write(`${fib.next().value} `);
}
console.log();

// Generator with for...of:
function* range(start, end, step = 1) {
    for (let i = start; i < end; i += step) {
        yield i;
    }
}

console.log("range(0, 10, 2):");
for (const num of range(0, 10, 2)) {
    process.stdout.write(`${num} `);
}
console.log();

// Making an object iterable (like Python's __iter__):
class NumberRange {
    constructor(start, end) {
        this.start = start;
        this.end = end;
    }

    // Symbol.iterator makes this work with for...of:
    *[Symbol.iterator]() {
        for (let i = this.start; i <= this.end; i++) {
            yield i;
        }
    }
}

console.log("Custom iterable (1-5):");
const range1to5 = new NumberRange(1, 5);
console.log([...range1to5]);  // [1, 2, 3, 4, 5]
console.log();


// =============================================================================
// PART 8: MAP AND SET
// =============================================================================
//
// Map and Set are built-in data structures added in ES6.
// They're similar to Python's dict and set, but with a different API.
//
// Map vs Object:
//   - Map keys can be ANY type (objects, functions, etc.)
//   - Object keys are always strings/symbols
//   - Map remembers insertion order (Objects do too, but Map is guaranteed)
//   - Map has a .size property

console.log("=".repeat(50));
console.log("PART 8: Map and Set");
console.log("=".repeat(50));

// --- Map (like Python's dict, but keys can be anything) ---
const map = new Map();

// Set values (Python: d[key] = value):
map.set("name", "Chint");
map.set("age", 25);
map.set(42, "the answer");     // Number as key!
map.set(true, "yes");          // Boolean as key!

const objKey = { id: 1 };
map.set(objKey, "object key!");  // Object as key!

// Get values (Python: d[key] or d.get(key)):
console.log(`map.get("name"): ${map.get("name")}`);
console.log(`map.get(42): ${map.get(42)}`);
console.log(`map.size: ${map.size}`);
console.log(`map.has("age"): ${map.has("age")}`);

// Iterate (Python: for key, value in d.items()):
console.log("\nMap entries:");
for (const [key, value] of map) {
    console.log(`  ${String(key).substring(0, 20)}: ${value}`);
}

// Create from array of pairs (like Python's dict()):
const map2 = new Map([["a", 1], ["b", 2], ["c", 3]]);
console.log("Map from pairs:", [...map2.entries()]);

// --- Set (like Python's set) ---
const set = new Set();

set.add(1);
set.add(2);
set.add(3);
set.add(2);  // Duplicate! Will be ignored.
set.add(1);  // Duplicate! Will be ignored.

console.log(`\nSet: [${[...set]}]`);     // [1, 2, 3]
console.log(`set.size: ${set.size}`);     // 3
console.log(`set.has(2): ${set.has(2)}`); // true

// Set from array (great for removing duplicates!):
// Python: list(set([1, 2, 2, 3, 3, 3]))
// JS:     [...new Set([1, 2, 2, 3, 3, 3])]
const unique = [...new Set([1, 2, 2, 3, 3, 3, 4])];
console.log(`Unique: [${unique}]`);

// Set operations (not built-in like Python, but easy to do):
const setA = new Set([1, 2, 3, 4]);
const setB = new Set([3, 4, 5, 6]);

const union = new Set([...setA, ...setB]);
const intersection = new Set([...setA].filter(x => setB.has(x)));
const difference = new Set([...setA].filter(x => !setB.has(x)));

console.log(`Union:        [${[...union]}]`);
console.log(`Intersection: [${[...intersection]}]`);
console.log(`Difference:   [${[...difference]}]`);
console.log();


// =============================================================================
// PART 9: FOR...OF vs FOR...IN
// =============================================================================

console.log("=".repeat(50));
console.log("PART 9: for...of vs for...in");
console.log("=".repeat(50));

// for...of: iterates over VALUES (arrays, strings, Maps, Sets, generators)
// for...in: iterates over KEYS/INDICES (objects, but also array indices)

const colors = ["red", "green", "blue"];

// for...of -> VALUES (what you usually want):
console.log("for...of (values):");
for (const color of colors) {
    console.log(`  ${color}`);
}

// for...in -> KEYS/INDICES (usually for objects):
console.log("for...in (keys/indices):");
for (const index in colors) {
    console.log(`  ${index}: ${colors[index]}`);
}

// RULE OF THUMB:
//   for...of -> arrays, strings, Map, Set (values)
//   for...in -> objects (keys)
//   NEVER use for...in on arrays (it includes prototype properties!)
console.log();


// =============================================================================
// QUICK REFERENCE
// =============================================================================
//
// MODULES:
//   export function fn() {}    import { fn } from './file.js'
//   export default class {}    import MyClass from './file.js'
//   module.exports = {}        const x = require('./file')  (CommonJS)
//
// CLASSES:
//   class Dog extends Animal { constructor(name) { super(name); } }
//   new Dog("Rex")             this.name = name (like self.name in Python)
//   static method()            @staticmethod
//   get prop() {}              @property
//   #privateField               __private (name mangling)
//
// GENERATORS:
//   function* gen() { yield 1; yield 2; }
//   const g = gen(); g.next(); // { value: 1, done: false }
//
// MAP/SET:
//   new Map([[k, v]])          map.set(k, v)  map.get(k)  map.has(k)
//   new Set([1, 2, 3])         set.add(v)     set.has(v)  set.delete(v)
//   [...new Set(arr)]          Remove duplicates
//
// PYTHON -> JS:
//   class Dog(Animal):     -> class Dog extends Animal
//   self                   -> this
//   super().__init__()     -> super()
//   __init__              -> constructor()
//   __str__               -> toString()
//   @property              -> get prop() {}
//   yield                  -> yield (same!)
//   dict                   -> Map (for non-string keys) or plain object
//   set                    -> Set
//   set([1,2,2,3])         -> new Set([1,2,2,3])
//
// =============================================================================
