/*
 * ============================================================================
 *  TYPESCRIPT COURSE — Chapter 4: Unions, Intersections & Type Narrowing
 * ============================================================================
 *
 *  This is one of the MOST important chapters. Understanding unions and
 *  type narrowing is what separates TypeScript beginners from competent TS devs.
 *
 *  Key concepts:
 *    - Union types: "this OR that" (string | number)
 *    - Intersection types: "this AND that" (TypeA & TypeB)
 *    - Type narrowing: how TS gets smarter inside if/switch blocks
 *    - Discriminated unions: the most powerful pattern in TypeScript
 *
 *  PYTHON COMPARISON:
 *    Python:      Union[str, int] or str | int (3.10+)
 *    TypeScript:  string | number
 *
 *    Big difference: Python doesn't narrow types in if blocks.
 *    TypeScript DOES — and that's its superpower.
 *
 *  Run: npx tsx ch4_unions_intersections_narrowing.ts
 * ============================================================================
 */

// ============================================================================
// 1. UNION TYPES — This OR That
// ============================================================================

console.log("=== UNION TYPES ===");

// A union type means "this value can be one of several types."
// Use the | (pipe) character.

let id: string | number;

id = "abc-123";   // OK — it's a string
console.log("id (string):", id);

id = 42;          // OK — it's a number
console.log("id (number):", id);

// id = true;     // ERROR! boolean is not string | number

// Union with more than two types:
let value: string | number | boolean | null = "hello";
console.log("value:", value);

// Functions that accept unions:
function printId(id: string | number): void {
    console.log(`  ID: ${id}`);
}
printId("abc");
printId(42);

// The catch: you can only use methods common to ALL types in the union.
function getLength(input: string | number): void {
    // input.toUpperCase();   // ERROR! number doesn't have toUpperCase
    // input.toFixed(2);      // ERROR! string doesn't have toFixed
    console.log(`  toString: ${input.toString()}`);  // OK — both have toString
}
getLength("hello");
getLength(42);
// To use type-specific methods, you need NARROWING (section 3 below).


// ============================================================================
// 2. INTERSECTION TYPES — This AND That
// ============================================================================

console.log("\n=== INTERSECTION TYPES ===");

// An intersection type combines multiple types into one.
// The result has ALL properties from ALL types.
// Use the & (ampersand) character.

type HasName = {
    name: string;
};

type HasEmail = {
    email: string;
};

type HasAge = {
    age: number;
};

// Intersection: must have ALL properties from ALL types
type ContactInfo = HasName & HasEmail & HasAge;

let contact: ContactInfo = {
    name: "Chint",
    email: "chint@example.com",
    age: 25
};
console.log("contact (intersection):", contact);

// Think of it:
//   Union (|):        "can be A OR B"       — EITHER set of properties
//   Intersection (&): "must be A AND B"     — ALL properties from both

// Real-world: extending an existing type
type ApiResponse = {
    data: unknown;
    status: number;
};

type TimestampedResponse = ApiResponse & {
    timestamp: Date;
    requestId: string;
};

let response: TimestampedResponse = {
    data: { user: "Chint" },
    status: 200,
    timestamp: new Date(),
    requestId: "req-abc-123"
};
console.log("timestamped response status:", response.status);
console.log("timestamped response requestId:", response.requestId);


// ============================================================================
// 3. TYPE NARROWING — TS gets smarter inside conditions
// ============================================================================

console.log("\n=== TYPE NARROWING ===");

// This is TypeScript's KILLER FEATURE.
// When you check a type inside an if/switch, TS "narrows" the type
// automatically. It KNOWS what the type is inside that block.
//
// Python comparison: Python doesn't do this! Even with isinstance() checks,
// your type checker (mypy) is less sophisticated than TS's narrowing.

// --- typeof narrowing ---
console.log("\n--- typeof narrowing ---");

function process(input: string | number): string {
    if (typeof input === "string") {
        // TS KNOWS input is a string here
        return input.toUpperCase();       // string methods work!
    } else {
        // TS KNOWS input is a number here
        return input.toFixed(2);          // number methods work!
    }
}
console.log("process('hello'):", process("hello"));
console.log("process(3.14159):", process(3.14159));

// typeof works for: string, number, boolean, undefined, object, function
function describe(x: string | number | boolean | undefined): string {
    if (typeof x === "string") return `String: "${x}"`;
    if (typeof x === "number") return `Number: ${x}`;
    if (typeof x === "boolean") return `Boolean: ${x}`;
    return "undefined";
}
console.log("describe('hi'):", describe("hi"));
console.log("describe(42):", describe(42));
console.log("describe(true):", describe(true));


// --- instanceof narrowing ---
console.log("\n--- instanceof narrowing ---");

function formatDate(input: string | Date): string {
    if (input instanceof Date) {
        // TS KNOWS input is a Date here
        return input.toISOString();
    } else {
        // TS KNOWS input is a string here
        return new Date(input).toISOString();
    }
}
console.log("formatDate(new Date()):", formatDate(new Date()));
console.log("formatDate('2025-01-01'):", formatDate("2025-01-01"));

// Works with any class:
class Dog {
    bark() { return "Woof!"; }
}
class Cat {
    meow() { return "Meow!"; }
}

function speak(animal: Dog | Cat): string {
    if (animal instanceof Dog) {
        return animal.bark();    // TS knows it's a Dog
    } else {
        return animal.meow();    // TS knows it's a Cat
    }
}
console.log("speak(new Dog()):", speak(new Dog()));
console.log("speak(new Cat()):", speak(new Cat()));


// --- "in" operator narrowing ---
console.log("\n--- 'in' operator narrowing ---");

// The "in" operator checks if a property EXISTS on an object.
// TS uses this to narrow types.

type Fish = { swim: () => string };
type Bird = { fly: () => string };

function move(animal: Fish | Bird): string {
    if ("swim" in animal) {
        return animal.swim();    // TS knows it's a Fish
    } else {
        return animal.fly();     // TS knows it's a Bird
    }
}

let fish: Fish = { swim: () => "Swimming!" };
let bird: Bird = { fly: () => "Flying!" };
console.log("move(fish):", move(fish));
console.log("move(bird):", move(bird));


// --- Truthiness narrowing ---
console.log("\n--- Truthiness narrowing ---");

// Checking if a value is truthy narrows away null/undefined/empty.

function greetUser(name: string | null | undefined): string {
    if (name) {
        // TS knows name is string here (null and undefined are falsy)
        return `Hello, ${name}!`;
    }
    return "Hello, stranger!";
}
console.log("greetUser('Chint'):", greetUser("Chint"));
console.log("greetUser(null):", greetUser(null));
console.log("greetUser(undefined):", greetUser(undefined));


// ============================================================================
// 4. DISCRIMINATED UNIONS (Tagged Unions) — VERY important pattern
// ============================================================================

console.log("\n=== DISCRIMINATED UNIONS ===");

// A discriminated union is a union where each member has a common
// property (the "discriminant" or "tag") with a LITERAL type.
// This lets you use switch/if to narrow to the exact type.
//
// This is THE most important pattern in TypeScript for modeling data.
// It's like Python's match/case with tagged dataclasses, but better.

// Example: shapes with different properties
type Circle = {
    kind: "circle";     // literal type — always the string "circle"
    radius: number;
};

type Square = {
    kind: "square";     // literal type — always the string "square"
    side: number;
};

type Rectangle = {
    kind: "rectangle";  // literal type
    width: number;
    height: number;
};

type Shape = Circle | Square | Rectangle;  // discriminated union

// The "kind" property is the discriminant — it tells us which shape we have.

function area(shape: Shape): number {
    switch (shape.kind) {
        case "circle":
            // TS KNOWS shape is Circle here — has .radius
            return Math.PI * shape.radius ** 2;
        case "square":
            // TS KNOWS shape is Square here — has .side
            return shape.side ** 2;
        case "rectangle":
            // TS KNOWS shape is Rectangle here — has .width and .height
            return shape.width * shape.height;
    }
}

let shapes: Shape[] = [
    { kind: "circle", radius: 5 },
    { kind: "square", side: 4 },
    { kind: "rectangle", width: 6, height: 3 }
];

for (let shape of shapes) {
    console.log(`  ${shape.kind}: area = ${area(shape).toFixed(2)}`);
}

// Real-world example: API responses
type SuccessResponse = {
    status: "success";
    data: { id: number; name: string };
};

type ErrorResponse = {
    status: "error";
    message: string;
    code: number;
};

type LoadingResponse = {
    status: "loading";
};

type ApiResult = SuccessResponse | ErrorResponse | LoadingResponse;

function handleResult(result: ApiResult): string {
    switch (result.status) {
        case "success":
            return `Got user: ${result.data.name}`;
        case "error":
            return `Error ${result.code}: ${result.message}`;
        case "loading":
            return "Loading...";
    }
}

let results: ApiResult[] = [
    { status: "success", data: { id: 1, name: "Chint" } },
    { status: "error", message: "Not found", code: 404 },
    { status: "loading" }
];

for (let result of results) {
    console.log(`  ${handleResult(result)}`);
}


// ============================================================================
// 5. EXHAUSTIVE CHECKING WITH never
// ============================================================================

console.log("\n=== EXHAUSTIVE CHECKING ===");

// Exhaustive checking ensures you handle EVERY case in a union.
// If you forget a case, TypeScript gives you a compile-time error.
// This is incredibly valuable for maintaining code.

type Fruit = "apple" | "banana" | "cherry";

function getFruitColor(fruit: Fruit): string {
    switch (fruit) {
        case "apple":
            return "red";
        case "banana":
            return "yellow";
        case "cherry":
            return "dark red";
        default:
            // If all cases are handled, fruit is type "never" here.
            // If you ADD a new fruit to the union and forget to handle it,
            // this line will ERROR — forcing you to update the switch.
            const _exhaustive: never = fruit;
            throw new Error(`Unhandled fruit: ${_exhaustive}`);
    }
}

console.log("apple:", getFruitColor("apple"));
console.log("banana:", getFruitColor("banana"));
console.log("cherry:", getFruitColor("cherry"));

// Try adding "mango" to the Fruit type — the default case will error,
// reminding you to add a case for "mango". THAT'S the power of exhaustive checking.

// Helper function pattern (used in many codebases):
function assertNever(value: never): never {
    throw new Error(`Unexpected value: ${value}`);
}

// Use it in any switch:
function describeShape(shape: Shape): string {
    switch (shape.kind) {
        case "circle":    return `Circle with radius ${shape.radius}`;
        case "square":    return `Square with side ${shape.side}`;
        case "rectangle": return `Rectangle ${shape.width}x${shape.height}`;
        default:          return assertNever(shape);
    }
}

for (let shape of shapes) {
    console.log(`  ${describeShape(shape)}`);
}


// ============================================================================
// 6. PRACTICAL EXAMPLES
// ============================================================================

console.log("\n=== PRACTICAL EXAMPLES ===");

// --- Example 1: Parsing user input ---
function parseInput(input: string): string | number | boolean {
    if (input === "true") return true;
    if (input === "false") return false;
    const num = Number(input);
    if (!isNaN(num)) return num;
    return input;
}

let inputs = ["42", "hello", "true", "3.14", "false"];
for (let inp of inputs) {
    let result = parseInput(inp);
    console.log(`  parseInput("${inp}"): ${result} (${typeof result})`);
}

// --- Example 2: Type-safe event system using discriminated unions ---
type ClickEvent = { type: "click"; x: number; y: number };
type KeyEvent = { type: "key"; key: string; code: number };
type ScrollEvent = { type: "scroll"; deltaY: number };

type UIEvent = ClickEvent | KeyEvent | ScrollEvent;

function handleEvent(event: UIEvent): void {
    switch (event.type) {
        case "click":
            console.log(`  Click at (${event.x}, ${event.y})`);
            break;
        case "key":
            console.log(`  Key "${event.key}" (code: ${event.code})`);
            break;
        case "scroll":
            console.log(`  Scroll delta: ${event.deltaY}`);
            break;
    }
}

let events: UIEvent[] = [
    { type: "click", x: 100, y: 200 },
    { type: "key", key: "Enter", code: 13 },
    { type: "scroll", deltaY: -50 }
];

console.log("Events:");
events.forEach(handleEvent);

// --- Example 3: Union narrowing with arrays ---
function sumValues(values: (string | number)[]): number {
    let total = 0;
    for (let val of values) {
        if (typeof val === "number") {
            total += val;
        } else {
            total += parseFloat(val) || 0;
        }
    }
    return total;
}
console.log("\nsumValues([1, '2', 3, 'four', '5']):", sumValues([1, "2", 3, "four", "5"]));


// ============================================================================
// 7. PYTHON vs TYPESCRIPT NARROWING — Key differences
// ============================================================================

console.log("\n=== PYTHON vs TYPESCRIPT NARROWING ===");

// Python (3.10+):
//   def process(x: str | int) -> str:
//       if isinstance(x, str):
//           return x.upper()     # mypy understands this
//       return str(x)
//
// TypeScript:
//   function process(x: string | number): string {
//       if (typeof x === "string") {
//           return x.toUpperCase();  // TS understands this
//       }
//       return x.toFixed(2);         // TS knows it's number here
//   }
//
// Key differences:
//   1. Python uses isinstance(), TS uses typeof/instanceof/in
//   2. Python narrowing depends on your type checker (mypy, pyright)
//   3. TS narrowing is built into the language — always works
//   4. TS narrowing is more sophisticated (discriminated unions, control flow analysis)

console.log("Python: isinstance() checks, narrowing depends on mypy/pyright");
console.log("TypeScript: typeof/instanceof/in, narrowing is built-in and automatic");
console.log("TypeScript's discriminated unions have no Python equivalent");


// ============================================================================
// RECAP
// ============================================================================

console.log("\n=== CHAPTER 4 RECAP ===");
console.log("1. Union types: string | number (this OR that)");
console.log("2. Intersection types: A & B (this AND that — all properties)");
console.log("3. Type narrowing: TS narrows types in if/switch blocks");
console.log("4. Narrowing methods: typeof, instanceof, 'in', truthiness");
console.log("5. Discriminated unions: { kind: 'circle'; radius: number } — the best pattern");
console.log("6. Exhaustive checking: use never to ensure all cases are handled");
console.log("\nNext up: Chapter 5 — Generics!");
