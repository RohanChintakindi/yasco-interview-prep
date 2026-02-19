/*
=====================================================
 CHAPTER 4: ARRAYS & OBJECTS
=====================================================

Arrays and Objects are the two most important data structures in
JavaScript. If you know Python lists and dicts, you already know
the core ideas - JS just has different syntax and more built-in methods.

COMING FROM PYTHON:
  Python list  ->  JS Array     [1, 2, 3]
  Python dict  ->  JS Object    { key: "value" }

The BIG DIFFERENCE: JavaScript array methods (map, filter, reduce) are
used CONSTANTLY. In Python, you'd use list comprehensions. In JS,
you chain array methods. This is the "functional" style of JS.

Python:  [x*2 for x in nums]          # list comprehension
JS:      nums.map(x => x * 2)         # array method with callback


HOW TO RUN:
  node ch4_arrays_and_objects.js
*/

// =============================================================================
// PART 1: ARRAYS (Like Python Lists)
// =============================================================================
//
// Arrays are ordered collections. They work very similarly to Python lists.
// Python: fruits = ["apple", "banana"]
// JS:     const fruits = ["apple", "banana"];

console.log("=".repeat(50));
console.log("PART 1: Arrays (Python lists)");
console.log("=".repeat(50));

const fruits = ["apple", "banana", "cherry", "date"];

// Accessing elements (same as Python - zero-indexed):
console.log(`First:  ${fruits[0]}`);      // apple
console.log(`Last:   ${fruits[fruits.length - 1]}`);  // date
// Python: fruits[-1]  -> JS doesn't support negative indexing!
// Use fruits.at(-1) instead (modern JS):
console.log(`Last (at): ${fruits.at(-1)}`);  // date

console.log(`Length: ${fruits.length}`);   // 4  (Python: len(fruits))

// --- Mutating methods (change the original array) ---

// push/pop: add/remove from END (like Python's append/pop)
const colors = ["red", "green"];
colors.push("blue");              // Python: colors.append("blue")
console.log(`After push: [${colors}]`);  // red, green, blue
const removed = colors.pop();     // Python: colors.pop()
console.log(`Popped: ${removed}, array: [${colors}]`);  // blue, [red, green]

// unshift/shift: add/remove from START (Python doesn't have a clean equivalent)
colors.unshift("yellow");         // Add to front
console.log(`After unshift: [${colors}]`);  // yellow, red, green
const shifted = colors.shift();   // Remove from front
console.log(`Shifted: ${shifted}, array: [${colors}]`);  // yellow, [red, green]

// splice: the Swiss Army knife - add/remove from ANY position
// splice(startIndex, deleteCount, ...itemsToAdd)
const nums = [1, 2, 3, 4, 5];
nums.splice(2, 1);                // Remove 1 element at index 2
console.log(`After splice(2,1): [${nums}]`);  // [1, 2, 4, 5]
nums.splice(1, 0, 99);            // Insert 99 at index 1 (delete 0)
console.log(`After splice(1,0,99): [${nums}]`); // [1, 99, 2, 4, 5]

// includes: check if element exists (like Python's "in" operator)
// Python: "apple" in fruits
// JS:     fruits.includes("apple")
console.log(`includes "banana": ${fruits.includes("banana")}`);  // true
console.log(`indexOf "cherry":  ${fruits.indexOf("cherry")}`);   // 2
console.log();


// =============================================================================
// PART 2: ARRAY METHODS - map, filter, reduce (THE BIG THREE)
// =============================================================================
//
// These are the most important array methods in JavaScript.
// They all take a CALLBACK function and return a new array (they don't
// mutate the original).
//
// PYTHON EQUIVALENTS:
//   map    = list comprehension:     [f(x) for x in list]
//   filter = filtered comprehension: [x for x in list if condition]
//   reduce = functools.reduce()

console.log("=".repeat(50));
console.log("PART 2: map, filter, reduce");
console.log("=".repeat(50));

const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// --- map: transform every element ---
// Python: doubled = [n * 2 for n in numbers]
// JS:     const doubled = numbers.map(n => n * 2);
const doubled = numbers.map(n => n * 2);
console.log(`Original:  [${numbers}]`);
console.log(`Doubled:   [${doubled}]`);

// map with index (second parameter is the index):
const indexed = ["a", "b", "c"].map((item, i) => `${i}:${item}`);
console.log(`Indexed:   [${indexed}]`);

// --- filter: keep only elements that pass a test ---
// Python: evens = [n for n in numbers if n % 2 == 0]
// JS:     const evens = numbers.filter(n => n % 2 === 0);
const evens = numbers.filter(n => n % 2 === 0);
console.log(`Evens:     [${evens}]`);

const bigNums = numbers.filter(n => n > 5);
console.log(`Over 5:    [${bigNums}]`);

// --- reduce: combine all elements into a single value ---
// Python: from functools import reduce; reduce(lambda acc, n: acc + n, numbers, 0)
// JS:     const sum = numbers.reduce((acc, n) => acc + n, 0);
//
// reduce takes two arguments:
//   1. A callback with (accumulator, currentValue) -> newAccumulator
//   2. An initial value for the accumulator
const sum = numbers.reduce((acc, n) => acc + n, 0);
console.log(`Sum:       ${sum}`);

const product = numbers.reduce((acc, n) => acc * n, 1);
console.log(`Product:   ${product}`);

// reduce to find max:
const max = numbers.reduce((acc, n) => n > acc ? n : acc, numbers[0]);
console.log(`Max:       ${max}`);
console.log();


// =============================================================================
// PART 3: MORE ARRAY METHODS
// =============================================================================

console.log("=".repeat(50));
console.log("PART 3: More Array Methods");
console.log("=".repeat(50));

const people = [
    { name: "Alice", age: 30 },
    { name: "Bob", age: 25 },
    { name: "Charlie", age: 35 },
    { name: "Diana", age: 28 },
];

// find: return the FIRST element that passes the test (or undefined)
const found = people.find(p => p.age > 28);
console.log(`find(age > 28): ${found.name} (${found.age})`);

// findIndex: return the INDEX of the first match
const idx = people.findIndex(p => p.name === "Charlie");
console.log(`findIndex("Charlie"): ${idx}`);

// some: does ANY element pass the test? (like Python's any())
const hasYoung = people.some(p => p.age < 26);
console.log(`some(age < 26): ${hasYoung}`);

// every: do ALL elements pass the test? (like Python's all())
const allAdults = people.every(p => p.age >= 18);
console.log(`every(age >= 18): ${allAdults}`);

// forEach: like a for loop but as a method (no return value)
// Python: for p in people: print(p)
console.log("forEach example:");
people.forEach(p => console.log(`  ${p.name} is ${p.age}`));

// sort: sorts IN PLACE (mutates!) and returns the array
// GOTCHA: default sort converts to strings! [1, 10, 2] not [1, 2, 10]
const unsorted = [3, 1, 4, 1, 5, 9, 2, 6];
const sorted = [...unsorted].sort((a, b) => a - b);  // Spread to avoid mutation
console.log(`\nSorted: [${sorted}]`);
// a - b: ascending. b - a: descending.

// Chaining methods (very common in JS):
const result = people
    .filter(p => p.age >= 28)           // Keep age >= 28
    .map(p => p.name)                    // Extract just names
    .sort();                             // Sort alphabetically
console.log(`Chain result: [${result}]`);  // Alice, Charlie, Diana

// flat: flatten nested arrays (like Python's itertools.chain)
const nested = [[1, 2], [3, 4], [5, 6]];
console.log(`flat: [${nested.flat()}]`);  // [1, 2, 3, 4, 5, 6]

// flatMap: map then flatten (very handy)
const sentences = ["hello world", "foo bar"];
const words = sentences.flatMap(s => s.split(" "));
console.log(`flatMap: [${words}]`);  // [hello, world, foo, bar]
console.log();


// =============================================================================
// PART 4: OBJECTS (Like Python Dicts)
// =============================================================================
//
// Objects are key-value pairs. Very similar to Python dictionaries.
// Python: person = {"name": "Chint", "age": 25}
// JS:     const person = { name: "Chint", age: 25 };
//
// KEY DIFFERENCE: In JS, keys don't need quotes (if they're valid identifiers).

console.log("=".repeat(50));
console.log("PART 4: Objects (Python dicts)");
console.log("=".repeat(50));

const person = {
    name: "Chint",
    age: 25,
    city: "NYC",
    hobbies: ["coding", "reading"],  // Values can be arrays, objects, anything
};

// Accessing values - TWO ways:
// Dot notation (preferred):
console.log(`Name: ${person.name}`);
// Bracket notation (needed for dynamic keys or keys with spaces):
console.log(`Age: ${person["age"]}`);

// Modifying:
person.age = 26;
person.email = "chint@example.com";  // Add new property
console.log(`Updated person:`, person);

// Deleting a property:
delete person.email;

// Check if key exists:
// Python: "name" in person
// JS:     "name" in person  (same!) or person.hasOwnProperty("name")
console.log(`"name" in person: ${"name" in person}`);  // true

// Looping over objects:
// Python: for key, value in person.items():
// JS:     for (const [key, value] of Object.entries(person))
console.log("\nObject.entries (like Python's .items()):");
for (const [key, value] of Object.entries(person)) {
    console.log(`  ${key}: ${JSON.stringify(value)}`);
}

// Useful Object methods:
console.log(`\nObject.keys:   [${Object.keys(person)}]`);    // Like dict.keys()
console.log(`Object.values: ${JSON.stringify(Object.values(person))}`);  // Like dict.values()
console.log();


// =============================================================================
// PART 5: DESTRUCTURING
// =============================================================================
//
// Destructuring lets you "unpack" values from arrays/objects into variables.
// Python has tuple unpacking: a, b, c = [1, 2, 3]
// JS destructuring is more powerful and works with objects too.

console.log("=".repeat(50));
console.log("PART 5: Destructuring");
console.log("=".repeat(50));

// --- Array destructuring (like Python tuple unpacking) ---
// Python: a, b, c = [1, 2, 3]
// JS:     const [a, b, c] = [1, 2, 3];
const [a, b, c] = [1, 2, 3];
console.log(`a=${a}, b=${b}, c=${c}`);  // 1, 2, 3

// Skip elements:
const [first, , third] = [10, 20, 30];
console.log(`first=${first}, third=${third}`);  // 10, 30

// Rest in destructuring (like Python's *rest):
// Python: head, *tail = [1, 2, 3, 4]
// JS:     const [head, ...tail] = [1, 2, 3, 4]
const [head, ...tail] = [1, 2, 3, 4];
console.log(`head=${head}, tail=[${tail}]`);  // 1, [2,3,4]

// --- Object destructuring (Python doesn't have a clean equivalent) ---
const user = { name: "Chint", age: 25, city: "NYC" };

// Extract specific properties into variables:
const { name: userName, age: userAge, city } = user;
console.log(`\nname=${userName}, age=${userAge}, city=${city}`);

// With default values:
const { role = "user", city: userCity } = user;
console.log(`role=${role} (default), city=${userCity}`);

// Destructuring in function parameters (very common in JS!):
function printUser({ name, age, city = "Unknown" }) {
    console.log(`${name}, ${age}, from ${city}`);
}
printUser({ name: "Alice", age: 30 });
printUser(user);
console.log();


// =============================================================================
// PART 6: SPREAD OPERATOR
// =============================================================================
//
// The ... (spread) operator "spreads" an array/object into individual elements.
// Python: * unpacks iterables, ** unpacks dicts
// JS:     ... works for both

console.log("=".repeat(50));
console.log("PART 6: Spread Operator");
console.log("=".repeat(50));

// --- Spread arrays (like Python's *) ---
// Copy an array:
const original = [1, 2, 3];
const copy = [...original];          // Python: copy = [*original] or list(original)
console.log(`Copy: [${copy}]`);

// Merge arrays:
const arr1 = [1, 2];
const arr2 = [3, 4];
const merged = [...arr1, ...arr2];   // Python: [*arr1, *arr2]
console.log(`Merged: [${merged}]`);

// Add elements while spreading:
const withExtra = [0, ...arr1, 99];
console.log(`With extra: [${withExtra}]`);

// --- Spread objects (like Python's **) ---
const defaults = { theme: "dark", language: "en", fontSize: 14 };
const userPrefs = { language: "es", fontSize: 18 };

// Merge (later properties override earlier ones):
const settings = { ...defaults, ...userPrefs };
// Python: settings = {**defaults, **user_prefs}
console.log(`Settings:`, settings);
// { theme: "dark", language: "es", fontSize: 18 }

// Copy and modify:
const updatedPerson = { ...person, age: 30, email: "new@email.com" };
console.log(`Updated:`, updatedPerson);
console.log();


// =============================================================================
// PART 7: OPTIONAL CHAINING AND NULLISH COALESCING
// =============================================================================
//
// These are modern JS features (ES2020) that handle null/undefined gracefully.
// Python doesn't have direct equivalents.

console.log("=".repeat(50));
console.log("PART 7: Optional Chaining & Nullish Coalescing");
console.log("=".repeat(50));

// --- Optional chaining (?.) ---
// Problem: accessing nested properties that might not exist crashes.
const userData = {
    name: "Chint",
    address: {
        street: "123 Main St",
        city: "NYC",
    },
    // No 'company' property
};

// Without optional chaining:
// console.log(userData.company.name);  // TypeError! Cannot read property 'name' of undefined

// With optional chaining: returns undefined instead of crashing
console.log(`Company: ${userData.company?.name}`);          // undefined (no crash!)
console.log(`Street:  ${userData.address?.street}`);        // "123 Main St"
console.log(`Deep:    ${userData.company?.address?.zip}`);  // undefined (no crash!)

// Works with methods too:
console.log(`toFixed: ${(42).toFixed?.(2)}`);       // "42.00"
console.log(`noMethod: ${userData.getName?.()}`);    // undefined

// --- Nullish coalescing (??) ---
// Provides a default value when something is null or undefined.
// Python: value = x if x is not None else default (or x or default, but that catches 0/"")
//
// DIFFERENCE from || (or):
//   || uses falsy check (0, "", false also trigger the default)
//   ?? only triggers on null and undefined

const config = {
    timeout: 0,       // 0 is a valid value!
    name: "",          // Empty string is a valid value!
    retries: null,     // null means "not set"
    debug: undefined,  // undefined means "not set"
};

// || treats 0 and "" as falsy (WRONG for our case):
console.log(`timeout || 5000: ${config.timeout || 5000}`);  // 5000 (wrong! 0 was valid)
console.log(`name || "anon":  ${config.name || "anonymous"}`); // "anonymous" (wrong!)

// ?? only triggers on null/undefined (CORRECT):
console.log(`timeout ?? 5000: ${config.timeout ?? 5000}`);  // 0 (correct!)
console.log(`name ?? "anon":  ${config.name ?? "anonymous"}`); // "" (correct!)
console.log(`retries ?? 3:    ${config.retries ?? 3}`);       // 3 (null -> use default)
console.log(`debug ?? false:  ${config.debug ?? false}`);     // false (undefined -> default)
console.log();


// =============================================================================
// QUICK REFERENCE
// =============================================================================
//
// ARRAYS:
//   Create:     const arr = [1, 2, 3]
//   Access:     arr[0], arr.at(-1)
//   Add/Remove: push, pop, unshift, shift, splice
//   Transform:  map, filter, reduce
//   Search:     find, findIndex, includes, indexOf
//   Check:      some, every
//   Sort:       sort((a,b) => a-b)
//   Chain:      arr.filter(...).map(...).sort(...)
//
// OBJECTS:
//   Create:     const obj = { key: value }
//   Access:     obj.key or obj["key"]
//   Loop:       Object.entries(obj), Object.keys(obj), Object.values(obj)
//   Check:      "key" in obj
//
// DESTRUCTURING:
//   Array:      const [a, b, ...rest] = [1, 2, 3, 4]
//   Object:     const { name, age } = person
//
// SPREAD:
//   Array:      [...arr1, ...arr2]
//   Object:     { ...obj1, ...obj2 }
//
// OPTIONAL CHAINING:  obj?.prop?.nested   (undefined if any part is null/undefined)
// NULLISH COALESCING: value ?? default    (default only for null/undefined)
//
// PYTHON -> JS:
//   [x*2 for x in list]        ->  list.map(x => x*2)
//   [x for x in list if cond]  ->  list.filter(x => cond)
//   functools.reduce()         ->  list.reduce((acc, x) => ..., initial)
//   {**dict1, **dict2}         ->  { ...obj1, ...obj2 }
//   a, b, *rest = [1,2,3,4]   ->  const [a, b, ...rest] = [1,2,3,4]
//
// =============================================================================
