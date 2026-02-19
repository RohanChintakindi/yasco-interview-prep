/*
 * ============================================================================
 *  TYPESCRIPT COURSE — Chapter 1: Introduction & Basic Types
 * ============================================================================
 *
 *  WHAT IS TYPESCRIPT?
 *  -------------------
 *  TypeScript is JavaScript + types. That's literally it.
 *  Every valid JavaScript file is already valid TypeScript. TypeScript just
 *  adds a type system on top that catches bugs BEFORE you run your code.
 *
 *  Think of it this way:
 *    - JavaScript:  "I'll let you do whatever. Bugs? You'll find them at runtime."
 *    - TypeScript:  "Let me check your work first. I'll catch mistakes NOW."
 *
 *  WHY TYPESCRIPT?
 *  ---------------
 *  1. Catches bugs BEFORE you run the code (compile-time checking)
 *  2. Way better autocomplete in your editor (VS Code knows what every variable is)
 *  3. Self-documenting — types tell you what a function expects and returns
 *  4. Safer refactoring — rename something and TS tells you everywhere it breaks
 *  5. Used by almost every major project: React, Angular, Vue, Node, Deno...
 *
 *  COMPARE TO PYTHON:
 *  ------------------
 *  You know Python, so this will help:
 *    Python:      def greet(name: str) -> str:       # type hints are OPTIONAL, NOT enforced
 *    TypeScript:  function greet(name: string): string  # types are ENFORCED at compile time
 *
 *  Python's type hints are just suggestions. You can write `def add(x: int) -> int`
 *  and pass a string — Python won't stop you. TypeScript WILL stop you.
 *
 *  HOW TO RUN THESE FILES:
 *  -----------------------
 *  First, install TypeScript and tsx (a TypeScript runner):
 *
 *    npm install -g typescript tsx
 *
 *  Then run any .ts file directly (easiest way):
 *
 *    npx tsx ch1_intro_and_basic_types.ts
 *
 *  Or compile to JavaScript first, then run:
 *
 *    tsc ch1_intro_and_basic_types.ts && node ch1_intro_and_basic_types.js
 *
 *  The first method (tsx) runs it directly — great for learning.
 *  The second method (tsc + node) shows you the compile step — what happens in real projects.
 *
 *  Let's dive in!
 * ============================================================================
 */

// ============================================================================
// 1. BASIC TYPES — The building blocks
// ============================================================================

// TypeScript has the same primitive types as JavaScript, but you can
// explicitly declare them. This is called a "type annotation."

// --- string ---
// Text values. Same as Python's str.
let firstName: string = "Chint";
let greeting: string = `Hello, ${firstName}!`;  // template literals work just like JS
console.log("=== BASIC TYPES ===");
console.log("firstName:", firstName);
console.log("greeting:", greeting);

// --- number ---
// All numbers (integers AND decimals). No separate int/float like Python.
// JavaScript (and TypeScript) only has one number type.
let age: number = 25;
let pi: number = 3.14159;
let hex: number = 0xff;        // hexadecimal
let binary: number = 0b1010;   // binary
console.log("\nage:", age);
console.log("pi:", pi);
console.log("hex:", hex, "  binary:", binary);

// --- boolean ---
// true or false. Same as Python's True/False but lowercase.
let isStudent: boolean = true;
let hasGraduated: boolean = false;
console.log("\nisStudent:", isStudent);
console.log("hasGraduated:", hasGraduated);

// --- null and undefined ---
// JavaScript has TWO "nothing" values (unlike Python which just has None):
//   null      = "I explicitly set this to nothing"
//   undefined = "This was never assigned a value"
let emptyValue: null = null;
let notAssigned: undefined = undefined;
console.log("\nemptyValue:", emptyValue);
console.log("notAssigned:", notAssigned);


// ============================================================================
// 2. TYPE INFERENCE — TypeScript is smart
// ============================================================================

// You DON'T always have to write the type. TypeScript can FIGURE IT OUT.
// This is called "type inference." Hover over these in VS Code — TS knows the types!

console.log("\n=== TYPE INFERENCE ===");

let city = "San Francisco";   // TS infers: string
let year = 2025;              // TS infers: number
let isActive = true;          // TS infers: boolean

// These are EXACTLY the same as writing:
//   let city: string = "San Francisco";
//   let year: number = 2025;
//   let isActive: boolean = true;

// Rule of thumb: let TS infer when it's obvious. Add annotations when it's not.
console.log("city (inferred string):", city);
console.log("year (inferred number):", year);
console.log("isActive (inferred boolean):", isActive);

// Where inference REALLY shines — function return types:
function double(x: number) {
    return x * 2;  // TS knows this returns a number
}
console.log("double(21):", double(21));


// ============================================================================
// 3. THE "any" TYPE — The escape hatch (avoid it!)
// ============================================================================

console.log("\n=== any vs unknown ===");

// "any" means "I give up on types." It turns off ALL type checking.
// It's an escape hatch — useful when migrating JS to TS, but avoid it in new code.
let whatever: any = "hello";
whatever = 42;          // no error — any accepts anything
whatever = true;        // still no error
whatever = [1, 2, 3];  // TS doesn't care — it's "any"
console.log("whatever (any):", whatever);

// The problem: "any" lets you do DANGEROUS things with NO warnings:
// let danger: any = "hello";
// danger.toFixed(2);  // This would CRASH at runtime! "hello" doesn't have toFixed.
// But TypeScript won't warn you because you told it "any."


// ============================================================================
// 4. THE "unknown" TYPE — Safer than any
// ============================================================================

// "unknown" is like "any" but SAFE. It says "I don't know the type YET."
// You MUST check the type before using it.
let mystery: unknown = "could be anything";

// mystery.toUpperCase();  // ERROR! Can't use it until you check the type.

// You have to NARROW it first:
if (typeof mystery === "string") {
    // Inside this block, TS knows mystery is a string
    console.log("mystery is a string:", mystery.toUpperCase());
}

// Think of it like this:
//   any     = "Trust me, I know what I'm doing" (TS: "okay, no checks")
//   unknown = "I don't know what this is yet"    (TS: "prove it before using it")


// ============================================================================
// 5. THE "void" TYPE — Functions that don't return anything
// ============================================================================

console.log("\n=== void type ===");

// void means "this function doesn't return a value."
// Like Python functions that don't have a return statement (they return None).
function logMessage(msg: string): void {
    console.log("LOG:", msg);
    // no return statement — that's void
}

logMessage("This function returns void");

// You rarely need to write `: void` explicitly — TS infers it.
// But it's good documentation: "this function is called for its side effects."


// ============================================================================
// 6. TYPE ASSERTIONS — "Trust me, I know the type"
// ============================================================================

console.log("\n=== TYPE ASSERTIONS ===");

// Sometimes YOU know more about a type than TypeScript does.
// Type assertions let you tell TS: "treat this as type X."

// Two syntaxes (they do the same thing):
let someValue: unknown = "this is a string";

// Syntax 1: "as" keyword (preferred — works everywhere)
let strLength1: number = (someValue as string).length;

// Syntax 2: angle bracket (doesn't work in JSX/React files)
let strLength2: number = (<string>someValue).length;

console.log("String length (as):", strLength1);
console.log("String length (<>):", strLength2);

// IMPORTANT: Type assertions DON'T convert types! They just tell the compiler.
// If you lie to the compiler, you'll get runtime errors.
// let oops = (42 as string);  // TS might warn you about this — it's a lie!

// Real-world example: DOM elements
// const input = document.getElementById("myInput") as HTMLInputElement;
// input.value = "hello";  // Without assertion, TS doesn't know it's an input


// ============================================================================
// 7. LITERAL TYPES — Exact values as types
// ============================================================================

console.log("\n=== LITERAL TYPES ===");

// A literal type is a type that represents ONE specific value.
// This is incredibly powerful for creating restricted options.

// Instead of string (any string), you can specify EXACT strings:
let direction: "up" | "down" | "left" | "right" = "up";
console.log("direction:", direction);

direction = "down";  // OK
// direction = "diagonal";  // ERROR! Not one of the allowed values.

// Works with numbers too:
let diceRoll: 1 | 2 | 3 | 4 | 5 | 6 = 3;
console.log("diceRoll:", diceRoll);

// Works with booleans:
let alwaysTrue: true = true;
// alwaysTrue = false;  // ERROR!

// Compare to Python:
//   Python: Literal["up", "down", "left", "right"]  (from typing import Literal, 3.8+)
//   TypeScript: "up" | "down" | "left" | "right"    (built into the language)

// const makes literal types automatic:
const myName = "Chint";   // Type is literally "Chint", not string
let myCity = "NYC";        // Type is string (because let can be reassigned)
console.log("const literal type:", myName);
console.log("let string type:", myCity);


// ============================================================================
// 8. PUTTING IT ALL TOGETHER — A real example
// ============================================================================

console.log("\n=== PUTTING IT ALL TOGETHER ===");

// Let's build a tiny user profile with everything we learned:

let username: string = "chint_codes";
let userAge: number = 25;
let isPremium: boolean = false;
let bio: string | null = null;                          // union with null — might not have a bio
let theme: "light" | "dark" | "system" = "dark";        // literal type — only 3 options

function displayProfile(
    name: string,
    age: number,
    premium: boolean,
    bio: string | null,
    theme: "light" | "dark" | "system"
): void {
    console.log(`  Username: ${name}`);
    console.log(`  Age: ${age}`);
    console.log(`  Premium: ${premium ? "Yes" : "No"}`);
    console.log(`  Bio: ${bio ?? "(no bio set)"}`);      // ?? is nullish coalescing (like Python's `or` but only for null/undefined)
    console.log(`  Theme: ${theme}`);
}

console.log("User Profile:");
displayProfile(username, userAge, isPremium, bio, theme);

// Now with a bio:
bio = "Learning TypeScript!";
theme = "light";
console.log("\nUpdated Profile:");
displayProfile(username, userAge, isPremium, bio, theme);


// ============================================================================
// RECAP
// ============================================================================

console.log("\n=== CHAPTER 1 RECAP ===");
console.log("1. TypeScript = JavaScript + types (enforced at compile time)");
console.log("2. Basic types: string, number, boolean, null, undefined");
console.log("3. Type annotations: let x: string = 'hello'");
console.log("4. Type inference: let x = 'hello' (TS figures it out)");
console.log("5. any = no type checking (avoid!), unknown = safe version");
console.log("6. void = function returns nothing");
console.log("7. Type assertions: value as string (tell TS what you know)");
console.log("8. Literal types: 'up' | 'down' (exact values as types)");
console.log("\nNext up: Chapter 2 — Arrays, Objects & Interfaces!");
