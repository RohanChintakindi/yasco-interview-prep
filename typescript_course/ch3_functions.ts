/*
 * ============================================================================
 *  TYPESCRIPT COURSE — Chapter 3: Functions
 * ============================================================================
 *
 *  Functions are the core of any program. TypeScript makes them safer by typing:
 *    - Parameters (what goes IN)
 *    - Return values (what comes OUT)
 *    - Callbacks and function types
 *
 *  You already know JS functions from the javascript_course. TypeScript just
 *  adds type annotations. If you know Python type hints, same idea — but enforced.
 *
 *  PYTHON COMPARISON:
 *    Python:      def greet(name: str, times: int = 1) -> str:
 *    TypeScript:  function greet(name: string, times: number = 1): string
 *
 *  Run: npx tsx ch3_functions.ts
 * ============================================================================
 */

// ============================================================================
// 1. TYPED PARAMETERS AND RETURN TYPES
// ============================================================================

console.log("=== TYPED PARAMETERS & RETURN TYPES ===");

// Add types after each parameter with : and the return type after the ()
function add(a: number, b: number): number {
    return a + b;
}
console.log("add(3, 4):", add(3, 4));

// TypeScript catches type errors:
// add("3", 4);     // ERROR! Can't pass string where number is expected
// add(3, 4, 5);    // ERROR! Too many arguments
// add(3);          // ERROR! Too few arguments

// Arrow functions with types:
const subtract = (a: number, b: number): number => a - b;
console.log("subtract(10, 4):", subtract(10, 4));

// Return type inference — TS can figure out the return type:
function multiply(a: number, b: number) {   // TS infers: returns number
    return a * b;
}
console.log("multiply(6, 7):", multiply(6, 7));

// When to annotate return types explicitly:
//   - Public API functions (makes intentions clear)
//   - Complex functions (helps you catch mistakes)
//   - When TS infers something unexpected


// ============================================================================
// 2. OPTIONAL PARAMETERS
// ============================================================================

console.log("\n=== OPTIONAL PARAMETERS ===");

// Add ? after the parameter name to make it optional.
// Optional params must come AFTER required params.
// Python comparison: def greet(name: str, greeting: str = None)

function greet(name: string, greeting?: string): string {
    // greeting is string | undefined (might not be provided)
    if (greeting) {
        return `${greeting}, ${name}!`;
    }
    return `Hello, ${name}!`;
}

console.log("greet('Chint'):", greet("Chint"));
console.log("greet('Chint', 'Hey'):", greet("Chint", "Hey"));

// Another example: formatting a price
function formatPrice(amount: number, currency?: string, locale?: string): string {
    const curr = currency ?? "USD";      // default via nullish coalescing
    const loc = locale ?? "en-US";
    return `${curr} ${amount.toFixed(2)} (${loc})`;
}

console.log("formatPrice(9.99):", formatPrice(9.99));
console.log("formatPrice(9.99, 'EUR'):", formatPrice(9.99, "EUR"));
console.log("formatPrice(9.99, 'GBP', 'en-GB'):", formatPrice(9.99, "GBP", "en-GB"));


// ============================================================================
// 3. DEFAULT PARAMETERS
// ============================================================================

console.log("\n=== DEFAULT PARAMETERS ===");

// Default values work just like JavaScript (and Python).
// If a default is provided, the parameter is automatically optional.

function createUser(name: string, role: string = "user", active: boolean = true) {
    return { name, role, active };
}

console.log("createUser('Chint'):", createUser("Chint"));
console.log("createUser('Alice', 'admin'):", createUser("Alice", "admin"));
console.log("createUser('Bob', 'mod', false):", createUser("Bob", "mod", false));

// TS infers the type from the default value — no annotation needed:
function repeat(text: string, times = 3): string {
    // 'times' is inferred as number because the default is 3
    return text.repeat(times);
}
console.log("repeat('ha'):", repeat("ha"));
console.log("repeat('ha', 5):", repeat("ha", 5));


// ============================================================================
// 4. REST PARAMETERS
// ============================================================================

console.log("\n=== REST PARAMETERS ===");

// Rest parameters collect multiple arguments into an array.
// Python comparison: def foo(*args: int) -> int
// TypeScript:        function foo(...args: number[]): number

function sum(...nums: number[]): number {
    return nums.reduce((total, n) => total + n, 0);
}
console.log("sum(1, 2, 3):", sum(1, 2, 3));
console.log("sum(10, 20, 30, 40):", sum(10, 20, 30, 40));

// Rest params with other params (rest must be LAST):
function tag(tagName: string, ...classes: string[]): string {
    const classStr = classes.length > 0 ? ` class="${classes.join(" ")}"` : "";
    return `<${tagName}${classStr}>`;
}
console.log("tag('div'):", tag("div"));
console.log("tag('div', 'container', 'flex'):", tag("div", "container", "flex"));

// You can also type rest params as tuples:
function makeEntry(...args: [string, number, boolean]): void {
    const [name, age, active] = args;
    console.log(`  ${name}, age ${age}, active: ${active}`);
}
console.log("makeEntry:");
makeEntry("Chint", 25, true);


// ============================================================================
// 5. FUNCTION TYPES — Typing a function itself
// ============================================================================

console.log("\n=== FUNCTION TYPES ===");

// You can describe the TYPE of a function — its signature.
// This is useful for callbacks, variables that hold functions, etc.
//
// Syntax: (param1: type1, param2: type2) => returnType

// A variable that holds a function:
let mathOp: (a: number, b: number) => number;

mathOp = (a, b) => a + b;          // assign an add function
console.log("mathOp (add):", mathOp(5, 3));

mathOp = (a, b) => a * b;          // reassign to multiply
console.log("mathOp (multiply):", mathOp(5, 3));

// mathOp = (a, b) => `${a + b}`;  // ERROR! Returns string, not number

// Using a type alias for cleaner code:
type Predicate = (value: number) => boolean;

const isPositive: Predicate = (n) => n > 0;
const isEven: Predicate = (n) => n % 2 === 0;

console.log("isPositive(5):", isPositive(5));
console.log("isPositive(-3):", isPositive(-3));
console.log("isEven(4):", isEven(4));


// ============================================================================
// 6. TYPING CALLBACKS
// ============================================================================

console.log("\n=== TYPING CALLBACKS ===");

// Callbacks are just function parameters. Type them like any function type.

function processNumbers(
    numbers: number[],
    callback: (n: number) => number      // callback type
): number[] {
    return numbers.map(callback);
}

let doubled = processNumbers([1, 2, 3, 4], (n) => n * 2);
let squared = processNumbers([1, 2, 3, 4], (n) => n ** 2);
console.log("doubled:", doubled);
console.log("squared:", squared);

// A more complex callback example — event handler style:
type EventHandler = (event: { type: string; target: string }) => void;

function onEvent(handler: EventHandler): void {
    // Simulating an event:
    handler({ type: "click", target: "button" });
}

onEvent((e) => {
    console.log(`Event: ${e.type} on ${e.target}`);
});

// Array method callbacks are already typed by TypeScript:
let words = ["hello", "WORLD", "TypeScript"];
let lower = words.map((w) => w.toLowerCase());     // TS knows w is string
let lengths = words.map((w) => w.length);           // TS knows this returns number[]
console.log("lower:", lower);
console.log("lengths:", lengths);


// ============================================================================
// 7. void vs undefined RETURN
// ============================================================================

console.log("\n=== void vs undefined ===");

// void:      "this function doesn't return anything meaningful"
// undefined: "this function explicitly returns undefined"

// They seem the same but behave differently:
function logSomething(): void {
    console.log("  I return void (nothing)");
    // no return statement
}

function getNothing(): undefined {
    console.log("  I explicitly return undefined");
    return undefined;   // MUST have this return statement
}

logSomething();
getNothing();

// Why does this matter?
// void allows callbacks to return anything (the return is just ignored):
type VoidCallback = () => void;

// This is VALID — push returns a number, but the void callback ignores it:
const nums: number[] = [];
const addNum: VoidCallback = () => nums.push(42);
addNum();
console.log("nums after void callback:", nums);


// ============================================================================
// 8. THE "never" TYPE — Functions that never return
// ============================================================================

console.log("\n=== never TYPE ===");

// "never" means "this function NEVER completes normally."
// Two cases:
//   1. It always throws an error
//   2. It loops forever

// Case 1: Always throws
function throwError(message: string): never {
    throw new Error(message);
}

// Case 2: Infinite loop (like a server loop)
// function forever(): never {
//     while (true) { /* ... */ }
// }

// never is useful for exhaustive checking (more in ch4):
type Color = "red" | "green" | "blue";

function getColorHex(color: Color): string {
    switch (color) {
        case "red": return "#ff0000";
        case "green": return "#00ff00";
        case "blue": return "#0000ff";
        default:
            // If we handled all cases, this is unreachable.
            // If we FORGOT a case, TS would error here.
            const _exhaustive: never = color;
            throw new Error(`Unknown color: ${_exhaustive}`);
    }
}

console.log("red hex:", getColorHex("red"));
console.log("blue hex:", getColorHex("blue"));


// ============================================================================
// 9. FUNCTION OVERLOADS — Multiple signatures, one implementation
// ============================================================================

console.log("\n=== FUNCTION OVERLOADS ===");

// Sometimes a function behaves differently based on its input types.
// Overloads let you define multiple type signatures.
//
// Python comparison: @overload from typing (similar concept)

// Overload signatures (no body):
function format(value: string): string;
function format(value: number): string;
function format(value: boolean): string;

// Implementation (must handle all overloads):
function format(value: string | number | boolean): string {
    if (typeof value === "string") {
        return `"${value}"`;
    } else if (typeof value === "number") {
        return value.toFixed(2);
    } else {
        return value ? "YES" : "NO";
    }
}

console.log("format('hello'):", format("hello"));
console.log("format(3.14159):", format(3.14159));
console.log("format(true):", format(true));

// More practical overload — different return types based on input:
function createElement(tag: "input"): { type: string; value: string };
function createElement(tag: "div"): { children: string[] };
function createElement(tag: string): { tag: string };
function createElement(tag: string): any {
    if (tag === "input") return { type: "text", value: "" };
    if (tag === "div") return { children: [] };
    return { tag };
}

let input = createElement("input");   // TS knows: { type: string; value: string }
let div = createElement("div");       // TS knows: { children: string[] }
console.log("createElement('input'):", input);
console.log("createElement('div'):", div);


// ============================================================================
// 10. GENERIC FUNCTIONS — Teaser for Chapter 5
// ============================================================================

console.log("\n=== GENERIC FUNCTIONS (TEASER) ===");

// Sometimes you want a function that works with ANY type but keeps
// the relationship between input and output types.
// That's what generics do — we'll cover them fully in Chapter 5.

// Simple example: get the first element of any array
function first<T>(arr: T[]): T | undefined {
    return arr[0];
}

// T gets replaced with the actual type you pass:
let firstNum = first([10, 20, 30]);        // T = number, returns number
let firstStr = first(["a", "b", "c"]);     // T = string, returns string
console.log("first([10, 20, 30]):", firstNum);
console.log("first(['a', 'b', 'c']):", firstStr);

// Another example: wrapping a value
function wrap<T>(value: T): { value: T } {
    return { value };
}

console.log("wrap(42):", wrap(42));           // { value: 42 }
console.log("wrap('hello'):", wrap("hello")); // { value: "hello" }

// We'll go MUCH deeper into generics in Chapter 5!


// ============================================================================
// 11. PUTTING IT ALL TOGETHER
// ============================================================================

console.log("\n=== PUTTING IT ALL TOGETHER ===");

// A typed utility function that filters, transforms, and summarizes data:

interface Product {
    name: string;
    price: number;
    category: string;
    inStock: boolean;
}

function filterProducts(
    products: Product[],
    predicate: (p: Product) => boolean,
    transform?: (p: Product) => string
): string[] {
    const filtered = products.filter(predicate);
    const formatter = transform ?? ((p) => `${p.name} ($${p.price})`);
    return filtered.map(formatter);
}

const products: Product[] = [
    { name: "Laptop", price: 999, category: "electronics", inStock: true },
    { name: "Book", price: 15, category: "education", inStock: true },
    { name: "Phone", price: 699, category: "electronics", inStock: false },
    { name: "Pen", price: 2, category: "office", inStock: true }
];

let affordable = filterProducts(products, (p) => p.price < 100);
let electronics = filterProducts(
    products,
    (p) => p.category === "electronics",
    (p) => `${p.name}: $${p.price} ${p.inStock ? "[IN STOCK]" : "[OUT]"}`
);

console.log("Affordable:", affordable);
console.log("Electronics:", electronics);


// ============================================================================
// RECAP
// ============================================================================

console.log("\n=== CHAPTER 3 RECAP ===");
console.log("1. Type parameters: function add(a: number, b: number): number");
console.log("2. Optional params: function f(x?: string) — x is string | undefined");
console.log("3. Default params: function f(x = 'hello') — infers type from default");
console.log("4. Rest params: function f(...args: number[]) — collects into array");
console.log("5. Function types: (a: number) => string — typing a function itself");
console.log("6. Callbacks: pass function types as parameters");
console.log("7. void = returns nothing, never = never completes");
console.log("8. Overloads: multiple signatures, one implementation");
console.log("9. Generics: function first<T>(arr: T[]): T (more in ch5!)");
console.log("\nNext up: Chapter 4 — Unions, Intersections & Narrowing!");
