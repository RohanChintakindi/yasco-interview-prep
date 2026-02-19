/*
=====================================================
 CHAPTER 2: CONTROL FLOW - DECISIONS & LOOPS
=====================================================

Programs need to make DECISIONS and REPEAT actions.
JavaScript control flow is very similar to Python's, but uses
{ curly braces } instead of indentation to define blocks.

COMING FROM PYTHON:
  Python:  if age >= 18:        JS:  if (age >= 18) {
               print("adult")           console.log("adult");
                                      }

  Python:  for item in list:    JS:  for (const item of list) {
               print(item)              console.log(item);
                                      }

KEY DIFFERENCES:
  - Conditions must be in PARENTHESES: if (condition)
  - Blocks use { curly braces }, not indentation
  - JS has switch statement (Python 3.10+ has match/case)
  - JS has do...while (Python doesn't)
  - JS has THREE types of for loops


HOW TO RUN:
  node ch2_control_flow.js
*/

// =============================================================================
// PART 1: IF / ELSE IF / ELSE
// =============================================================================
//
// Python:  if / elif / else
// JS:      if / else if / else
//
// Conditions MUST be in parentheses (). Blocks use { }.
// "elif" becomes "else if" in JavaScript.

console.log("=".repeat(50));
console.log("PART 1: if / else if / else");
console.log("=".repeat(50));

const age = 20;

if (age >= 18) {
    console.log("You are an adult");
} else if (age >= 13) {
    console.log("You are a teenager");
} else {
    console.log("You are a child");
}

// Chaining conditions with && (and) and || (or):
// Python: and, or, not
// JS:     &&,  ||,  !
const temperature = 25;
const isSunny = true;

if (temperature > 20 && isSunny) {
    console.log("Perfect day for a walk!");
} else if (temperature > 20 || isSunny) {
    console.log("Decent day");
} else {
    console.log("Stay inside");
}
console.log();


// =============================================================================
// PART 2: TERNARY OPERATOR
// =============================================================================
//
// Python:  status = "adult" if age >= 18 else "minor"
// JS:      const status = age >= 18 ? "adult" : "minor";
//
// The format is:  condition ? valueIfTrue : valueIfFalse

console.log("=".repeat(50));
console.log("PART 2: Ternary Operator");
console.log("=".repeat(50));

const status = age >= 18 ? "adult" : "minor";
console.log(`Status: ${status}`);

// You can nest them (but don't go overboard, it gets unreadable):
const score = 85;
const grade = score >= 90 ? "A" : score >= 80 ? "B" : score >= 70 ? "C" : "F";
console.log(`Score ${score} = Grade ${grade}`);
console.log();


// =============================================================================
// PART 3: SWITCH STATEMENT
// =============================================================================
//
// Python doesn't have switch (until match/case in 3.10).
// switch is useful when checking ONE variable against MANY possible values.
// It's like a cleaner version of if/else if/else if/else if...
//
// IMPORTANT: You MUST use "break" after each case, or it "falls through"
// to the next case (this is a common bug!).

console.log("=".repeat(50));
console.log("PART 3: switch statement");
console.log("=".repeat(50));

const day = "Monday";

switch (day) {
    case "Monday":
        console.log("Start of the work week");
        break;  // Without break, it would continue to Tuesday's code!
    case "Tuesday":
    case "Wednesday":
    case "Thursday":
        console.log("Midweek grind");
        break;
    case "Friday":
        console.log("TGIF!");
        break;
    case "Saturday":
    case "Sunday":
        console.log("Weekend vibes");
        break;
    default:  // Like Python's else
        console.log("Not a valid day");
}

// Switch uses === (strict equality) for comparisons.
// Notice Tuesday/Wednesday/Thursday share the same code - that's "fall-through".
console.log();


// =============================================================================
// PART 4: FOR LOOPS - THREE TYPES
// =============================================================================
//
// JavaScript has THREE different for loops:
//
// 1. Classic for (i = 0; i < n; i++)  - like Python's for i in range(n)
// 2. for...of                          - like Python's for item in list
// 3. for...in                          - for object keys (use carefully!)

console.log("=".repeat(50));
console.log("PART 4: for loops");
console.log("=".repeat(50));

// --- 1. Classic for loop ---
// Python: for i in range(5):
// JS:     for (let i = 0; i < 5; i++)
//
// Format: for (initialize; condition; update)
//   initialize: let i = 0   (start at 0)
//   condition:  i < 5       (keep going while this is true)
//   update:     i++         (add 1 after each loop)   i++ is shorthand for i = i + 1

console.log("Classic for loop (like range(5)):");
for (let i = 0; i < 5; i++) {
    console.log(`  i = ${i}`);
}
console.log();

// Counting by 2 (like Python's range(0, 10, 2)):
console.log("Count by 2:");
for (let i = 0; i < 10; i += 2) {
    console.log(`  i = ${i}`);
}
console.log();

// --- 2. for...of loop (MOST COMMON, like Python's for...in) ---
// This is what you'll use most of the time. It iterates over VALUES.
// Python: for fruit in fruits:
// JS:     for (const fruit of fruits) {

console.log("for...of loop (like Python's for...in):");
const fruits = ["apple", "banana", "cherry"];
for (const fruit of fruits) {
    console.log(`  I like ${fruit}`);
}
console.log();

// for...of works with strings too:
console.log("for...of with a string:");
for (const char of "JavaScript") {
    process.stdout.write(char + " ");  // print without newline
}
console.log("\n");

// Getting index + value (like Python's enumerate()):
// JS doesn't have enumerate(), but you can use .entries() on arrays:
console.log("Index + value (like Python's enumerate()):");
const languages = ["Python", "JavaScript", "Rust"];
for (const [index, lang] of languages.entries()) {
    console.log(`  ${index}: ${lang}`);
}
console.log();

// --- 3. for...in loop (for OBJECT KEYS, like iterating a Python dict) ---
// WARNING: for...in gives you KEYS (property names), not values.
// Don't use for...in on arrays! Use for...of instead.

console.log("for...in loop (for object properties):");
const person = { name: "Chint", age: 25, city: "NYC" };
for (const key in person) {
    console.log(`  ${key}: ${person[key]}`);
}
console.log();


// =============================================================================
// PART 5: WHILE AND DO...WHILE
// =============================================================================

console.log("=".repeat(50));
console.log("PART 5: while and do...while");
console.log("=".repeat(50));

// --- while loop (same concept as Python) ---
let count = 0;
while (count < 5) {
    console.log(`  Count: ${count}`);
    count++;  // count++ is shorthand for count = count + 1
}
console.log();

// --- do...while (Python doesn't have this!) ---
// The difference: do...while ALWAYS runs at least ONCE, then checks the condition.
// Regular while checks FIRST, so it might never run.
//
// Analogy: A do...while is like "eat at least one bite, then decide if you want more."
// A while is like "check if you're hungry before eating."

console.log("do...while (always runs at least once):");
let num = 10;
do {
    console.log(`  num is ${num}`);
    num++;
} while (num < 5);  // Condition is false! But it still ran once.
console.log("  (The loop body ran even though 10 < 5 is false)\n");


// =============================================================================
// PART 6: BREAK AND CONTINUE
// =============================================================================
//
// Same concept as Python:
//   break    -> exit the loop entirely
//   continue -> skip to the next iteration

console.log("=".repeat(50));
console.log("PART 6: break and continue");
console.log("=".repeat(50));

// break: stop when we find what we're looking for
console.log("break example:");
for (let i = 1; i < 100; i++) {
    if (i === 5) {
        console.log(`  Found 5! Stopping.`);
        break;
    }
    console.log(`  Checking ${i}...`);
}
console.log();

// continue: skip even numbers
console.log("continue example (skip evens):");
for (let i = 1; i <= 7; i++) {
    if (i % 2 === 0) {
        continue;  // Skip this iteration
    }
    console.log(`  Odd: ${i}`);
}
console.log();


// =============================================================================
// PART 7: TRUTHY AND FALSY VALUES
// =============================================================================
//
// In Python, things like 0, "", [], {}, None are "falsy" (treated as False).
// JavaScript is similar, but with its own set of falsy values.
//
// FALSY VALUES (these are treated as false in conditions):
//   false, 0, -0, 0n, "" (empty string), null, undefined, NaN
//
// EVERYTHING ELSE is truthy, including:
//   "0" (non-empty string), [] (empty array!), {} (empty object!)
//
// GOTCHA: In Python, [] and {} are falsy. In JS, they're TRUTHY!

console.log("=".repeat(50));
console.log("PART 7: Truthy and Falsy values");
console.log("=".repeat(50));

const falsyValues = [false, 0, -0, "", null, undefined, NaN];
const truthyValues = [true, 1, -1, "0", "false", [], {}, "hello"];

console.log("Falsy values (all treated as false):");
for (const val of falsyValues) {
    console.log(`  ${String(val).padEnd(12)} -> ${Boolean(val)}`);
}

console.log("\nTruthy values (all treated as true):");
for (const val of truthyValues) {
    // JSON.stringify handles objects/arrays for display
    const display = typeof val === "object" ? JSON.stringify(val) : String(val);
    console.log(`  ${display.padEnd(12)} -> ${Boolean(val)}`);
}

// Practical example: checking if a variable has a useful value
console.log("\nPractical truthy/falsy check:");
const username = "";
if (username) {
    console.log(`  Welcome, ${username}!`);
} else {
    console.log("  No username provided");  // This runs because "" is falsy
}

// GOTCHA alert:
console.log("\nGOTCHA: empty array [] is truthy in JS (falsy in Python!):");
const emptyArr = [];
if (emptyArr) {
    console.log("  [] is truthy! (to check empty array, use arr.length === 0)");
}
if (emptyArr.length === 0) {
    console.log("  arr.length === 0: the correct way to check empty arrays");
}
console.log();


// =============================================================================
// PART 8: PRACTICAL EXAMPLES
// =============================================================================

console.log("=".repeat(50));
console.log("PART 8: Practical examples");
console.log("=".repeat(50));

// FizzBuzz (classic interview question):
console.log("FizzBuzz (1-15):");
for (let i = 1; i <= 15; i++) {
    if (i % 3 === 0 && i % 5 === 0) {
        console.log(`  ${i}: FizzBuzz`);
    } else if (i % 3 === 0) {
        console.log(`  ${i}: Fizz`);
    } else if (i % 5 === 0) {
        console.log(`  ${i}: Buzz`);
    } else {
        console.log(`  ${i}`);
    }
}
console.log();

// Find max in an array:
const numbers = [4, 2, 9, 1, 7, 3];
let maximum = numbers[0];
for (const n of numbers) {
    if (n > maximum) maximum = n;
}
console.log(`Max of [${numbers}] = ${maximum}`);

// Count vowels:
const text = "Hello World";
let vowelCount = 0;
for (const char of text.toLowerCase()) {
    if ("aeiou".includes(char)) {
        vowelCount++;
    }
}
console.log(`Vowels in "${text}": ${vowelCount}`);
console.log();


// =============================================================================
// QUICK REFERENCE
// =============================================================================
//
// if (condition) {            for (let i = 0; i < n; i++) {
//     ...                         ...
// } else if (condition) {     }
//     ...                     for (const item of array) {
// } else {                        ...
//     ...                     }
// }                           for (const key in object) {
//                                 ...
// condition ? yes : no        }
//                              while (condition) { ... }
// switch (val) {               do { ... } while (condition);
//     case "a": ...; break;
//     default: ...;
// }
//
// Logical:  && (and)   || (or)   ! (not)
// Falsy:    false, 0, "", null, undefined, NaN
// Truthy:   everything else (including [] and {}!)
//
// PYTHON -> JS:
//   elif           -> else if
//   and / or / not -> && / || / !
//   for x in list  -> for (const x of list)
//   range(n)       -> for (let i = 0; i < n; i++)
//   enumerate(arr) -> arr.entries()
//
// =============================================================================
