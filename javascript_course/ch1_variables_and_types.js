/*
=====================================================
 CHAPTER 1: VARIABLES, TYPES & CONSOLE.LOG
=====================================================

WHAT IS JAVASCRIPT?
-------------------
JavaScript is the language of the web. Every website you've ever used
runs JavaScript in the browser. But it's also used on servers (Node.js),
mobile apps (React Native), and desktop apps (Electron).

COMING FROM PYTHON:
  Python:  print("hello")
  JS:      console.log("hello")

  Python:  name = "Chint"
  JS:      let name = "Chint";    (you MUST declare with let/const)

  Python:  uses indentation for blocks
  JS:      uses { curly braces } for blocks, and ; at end of lines

KEY DIFFERENCE: JavaScript requires you to DECLARE variables with a
keyword (let, const, or var) before using them. Python doesn't.


HOW TO RUN:
  node ch1_variables_and_types.js
*/

// =============================================================================
// PART 1: CONSOLE.LOG - SHOWING OUTPUT (Python's print())
// =============================================================================
//
// console.log() is JavaScript's print(). It outputs to the terminal.
// In Python you wrote: print("Hello")
// In JS you write:     console.log("Hello")

console.log("Hello, World!");   // Your first JavaScript line!
console.log("JavaScript is awesome");
console.log(42);                // Can print numbers too
console.log(3.14);             // And decimals
console.log();                 // Empty line

// You can print multiple values separated by commas (just like Python's print):
console.log("Name:", "Chint", "Age:", 25);


// =============================================================================
// PART 2: VARIABLES - let, const, var
// =============================================================================
//
// In Python:   name = "Chint"       (just assign)
// In JS:       let name = "Chint";  (declare with let/const first)
//
// THREE WAYS TO DECLARE:
//   let    -> value CAN change later (like a normal Python variable)
//   const  -> value CANNOT change (like a constant, final, immutable)
//   var    -> the OLD way, DO NOT USE (explained below)
//
// Rule of thumb: Use const by default. Use let only when you need to reassign.

console.log("=".repeat(50));
console.log("PART 2: Variables - let, const, var");
console.log("=".repeat(50));

// --- let: for values that will change ---
let age = 25;
console.log("Age:", age);   // 25
age = 26;                   // Reassignment is OK with let
console.log("Age now:", age); // 26

// --- const: for values that WON'T change ---
const name = "Chint";
console.log("Name:", name);
// name = "Bob";  // ERROR! Cannot reassign a const. Uncomment to see the error.

// --- var: the OLD way (avoid it!) ---
// Why var is bad:
//   1. var is "function-scoped", not "block-scoped" (confusing behavior in loops)
//   2. var can be re-declared (leads to accidental overwrites)
//   3. var is "hoisted" in weird ways (more on this in ch3)
//
// Python analogy: Imagine if a variable you created inside an if-block
// leaked out and existed everywhere in the function. That's var.
var oldWay = "Please don't use me";
var oldWay = "See? I can be re-declared. That's bad."; // No error! Dangerous.
console.log("var example:", oldWay);

// let prevents this:
let modern = "I'm safe";
// let modern = "Can't re-declare me!";  // ERROR! This is good - catches bugs.
console.log();


// =============================================================================
// PART 3: DATA TYPES
// =============================================================================
//
// JavaScript has these primitive types:
//
// TYPE        | EXAMPLE         | PYTHON EQUIVALENT
// ------------+-----------------+------------------
// string      | "hello"         | str
// number      | 42 or 3.14     | int + float (JS has ONE number type!)
// boolean     | true / false    | bool (True/False, note: lowercase in JS!)
// null        | null            | None
// undefined   | undefined       | (no Python equivalent)
// symbol      | Symbol("id")   | (no Python equivalent)
// bigint      | 42n            | Python's int (arbitrary precision)
//
// BIG DIFFERENCE: JavaScript has BOTH null AND undefined.
//   null      = "I intentionally set this to nothing" (like Python's None)
//   undefined = "This was never given a value" (Python would throw NameError)

console.log("=".repeat(50));
console.log("PART 3: Data Types");
console.log("=".repeat(50));

const text = "Hello";           // string
const wholeNumber = 42;         // number (JS doesn't separate int/float!)
const decimal = 3.14;           // number (same type as 42!)
const isStudent = true;         // boolean (lowercase! not True like Python)
const nothing = null;           // null (intentional "no value")
let notAssigned;                // undefined (no value assigned yet)

// typeof tells you the type (like Python's type()):
console.log(`"${text}" is ${typeof text}`);           // string
console.log(`${wholeNumber} is ${typeof wholeNumber}`); // number
console.log(`${decimal} is ${typeof decimal}`);         // number (same!)
console.log(`${isStudent} is ${typeof isStudent}`);     // boolean
console.log(`${nothing} is ${typeof nothing}`);         // object (this is a JS bug!)
console.log(`${notAssigned} is ${typeof notAssigned}`); // undefined

// GOTCHA: typeof null === "object" is a famous JavaScript bug from 1995.
// It should say "null" but they can never fix it without breaking the web.
console.log();


// =============================================================================
// PART 4: TYPE COERCION - THE #1 JAVASCRIPT GOTCHA
// =============================================================================
//
// Python is strict: "5" + 5 throws TypeError
// JavaScript is loose: "5" + 5 gives "55" (converts number to string!)
//
// This is called TYPE COERCION: JS automatically converts types to make
// operations work, often in surprising ways.
//
// TWO EQUALITY OPERATORS:
//   == (loose equality)  - converts types, then compares. AVOID THIS.
//   === (strict equality) - no conversion, compares type AND value. USE THIS.

console.log("=".repeat(50));
console.log("PART 4: Type Coercion (== vs ===)");
console.log("=".repeat(50));

// --- Loose equality (==) is DANGEROUS ---
console.log('5 == "5":', 5 == "5");     // true!  (JS converts string to number)
console.log("0 == false:", 0 == false);  // true!  (JS converts false to 0)
console.log('"" == false:', "" == false); // true!  (both become 0)
console.log("null == undefined:", null == undefined); // true!
console.log("0 == '':", 0 == "");        // true!  (wat?)

// --- Strict equality (===) is SAFE ---
console.log('\n5 === "5":', 5 === "5");      // false (different types)
console.log("0 === false:", 0 === false);    // false (different types)
console.log('"" === false:', "" === false);  // false (different types)
console.log("null === undefined:", null === undefined); // false

// RULE: ALWAYS use === and !==. Pretend == and != don't exist.

// More coercion surprises:
console.log('\n"5" + 3:', "5" + 3);     // "53" (number -> string, concatenates)
console.log('"5" - 3:', "5" - 3);       // 2    (string -> number, subtracts!)
console.log("true + 1:", true + 1);     // 2    (true -> 1)
console.log('"" + 0:', "" + 0);         // "0"  (number -> string)
console.log();


// =============================================================================
// PART 5: TEMPLATE LITERALS (Python's f-strings)
// =============================================================================
//
// Python: f"Hello {name}, you are {age} years old"
// JS:     `Hello ${name}, you are ${age} years old`
//
// KEY DIFFERENCES:
//   Python uses f"..." with {variable}
//   JS uses `...` (BACKTICKS, not quotes!) with ${expression}

console.log("=".repeat(50));
console.log("PART 5: Template Literals");
console.log("=".repeat(50));

const userName = "Chint";
const userAge = 25;

// Old way (string concatenation - ugly):
console.log("Hello, " + userName + "! You are " + userAge + " years old.");

// Modern way (template literals - clean, like Python f-strings):
console.log(`Hello, ${userName}! You are ${userAge} years old.`);

// You can put ANY expression inside ${}:
console.log(`2 + 2 = ${2 + 2}`);
console.log(`Uppercase: ${userName.toUpperCase()}`);
console.log(`Name length: ${userName.length} characters`);

// Template literals can span MULTIPLE LINES (Python needs triple quotes):
const multiline = `
  This is line 1
  This is line 2
  This is line 3
`;
console.log(multiline);


// =============================================================================
// PART 6: STRING METHODS
// =============================================================================
//
// Most string methods are similar to Python but use camelCase instead of
// snake_case. Also, JS strings are immutable (same as Python).

console.log("=".repeat(50));
console.log("PART 6: String Methods");
console.log("=".repeat(50));

const str = "  Hello, World!  ";

// Python: str.strip()        -> JS: str.trim()
// Python: str.lower()        -> JS: str.toLowerCase()
// Python: str.upper()        -> JS: str.toUpperCase()
// Python: str.replace(a, b)  -> JS: str.replace(a, b)
// Python: str.split(sep)     -> JS: str.split(sep)
// Python: str.startswith(x)  -> JS: str.startsWith(x)  (capital S!)
// Python: str.find(x)        -> JS: str.indexOf(x) (-1 if not found)
// Python: len(str)            -> JS: str.length (property, not function!)

console.log(`Original:   "${str}"`);
console.log(`trim():     "${str.trim()}"`);
console.log(`toLowerCase: "${str.trim().toLowerCase()}"`);
console.log(`toUpperCase: "${str.trim().toUpperCase()}"`);
console.log(`replace:    "${str.trim().replace("World", "JavaScript")}"`);
console.log(`split:      ${JSON.stringify(str.trim().split(", "))}`);
console.log(`startsWith: ${str.trim().startsWith("He")}`);
console.log(`indexOf:    ${str.indexOf("World")}`);
console.log(`length:     ${str.length}`);      // Property! No () needed.
console.log(`includes:   ${str.includes("World")}`);  // Python: "World" in str
console.log(`slice(2,7): "${str.slice(2, 7)}"`);       // Python: str[2:7]

// charAt - get character at index (Python: str[0])
console.log(`charAt(2):  "${str.charAt(2)}"`);
console.log(`str[2]:     "${str[2]}"`);  // Also works in JS (like Python)
console.log();


// =============================================================================
// PART 7: NUMBER OPERATIONS
// =============================================================================

console.log("=".repeat(50));
console.log("PART 7: Numbers");
console.log("=".repeat(50));

const a = 10;
const b = 3;

console.log(`${a} + ${b} = ${a + b}`);        // 13
console.log(`${a} - ${b} = ${a - b}`);        // 7
console.log(`${a} * ${b} = ${a * b}`);        // 30
console.log(`${a} / ${b} = ${a / b}`);        // 3.333... (no // in JS!)
console.log(`${a} % ${b} = ${a % b}`);        // 1 (modulo)
console.log(`${a} ** ${b} = ${a ** b}`);      // 1000 (exponent, same as Python)

// No floor division (//) in JS. Use Math.floor() instead:
// Python: 10 // 3 = 3
// JS:     Math.floor(10 / 3) = 3
console.log(`Floor division: Math.floor(${a}/${b}) = ${Math.floor(a / b)}`);

// Useful Math methods:
console.log(`Math.round(3.7):  ${Math.round(3.7)}`);    // 4
console.log(`Math.ceil(3.2):   ${Math.ceil(3.2)}`);     // 4
console.log(`Math.floor(3.9):  ${Math.floor(3.9)}`);    // 3
console.log(`Math.abs(-5):     ${Math.abs(-5)}`);       // 5
console.log(`Math.max(1,5,3):  ${Math.max(1, 5, 3)}`);  // 5
console.log(`Math.min(1,5,3):  ${Math.min(1, 5, 3)}`);  // 1
console.log(`Math.random():    ${Math.random()}`);       // 0 to 0.999...

// Type conversion:
const numStr = "42";
console.log(`\nNumber("42"):     ${Number("42")}`);       // 42
console.log(`parseInt("42px"):  ${parseInt("42px")}`);    // 42 (ignores trailing text!)
console.log(`parseFloat("3.14"): ${parseFloat("3.14")}`); // 3.14
console.log(`String(42):        "${String(42)}"`);        // "42"

// NaN (Not a Number) - what you get from invalid math:
console.log(`Number("hello"):   ${Number("hello")}`);    // NaN
console.log(`NaN === NaN:       ${NaN === NaN}`);         // false! (another JS gotcha)
console.log(`isNaN(NaN):        ${isNaN(NaN)}`);          // true (use this to check)
console.log();


// =============================================================================
// QUICK REFERENCE
// =============================================================================
//
// Declare:     let x = 5;  const y = 10;   (avoid var)
// Print:       console.log("text")
// Types:       string, number, boolean, null, undefined, symbol, bigint
// Type check:  typeof x
// Equality:    === (strict, ALWAYS use)  vs  == (loose, AVOID)
// Template:    `Hello ${name}`  (backticks + ${})
// Strings:     .trim() .toLowerCase() .toUpperCase() .includes() .split() .length
// Numbers:     Math.floor() Math.round() Math.random() parseInt() Number()
// Convert:     Number("42")  String(42)  Boolean(0)
//
// KEY PYTHON -> JS DIFFERENCES:
//   print()          ->  console.log()
//   True/False       ->  true/false (lowercase!)
//   None             ->  null (+ undefined)
//   type()           ->  typeof
//   f"..."           ->  `...${}`
//   ==               ->  === (always use triple equals!)
//   len(str)         ->  str.length
//   str.lower()      ->  str.toLowerCase()
//
// =============================================================================
