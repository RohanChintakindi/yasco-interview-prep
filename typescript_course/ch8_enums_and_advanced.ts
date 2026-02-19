/*
 * ============================================================================
 *  TYPESCRIPT COURSE — Chapter 8: Enums & Advanced Types
 * ============================================================================
 *
 *  This final chapter covers advanced TypeScript features:
 *    - Enums (and why modern TS often prefers unions instead)
 *    - Mapped types (transform types programmatically)
 *    - Conditional types (if/else for types)
 *    - Template literal types (string pattern types)
 *    - keyof and typeof operators
 *    - Type predicates (custom type guards)
 *    - tsconfig.json basics
 *    - Module patterns and declaration files
 *    - Tips for migrating JavaScript to TypeScript
 *
 *  These are the tools that make TypeScript TRULY powerful.
 *  You don't need to master them all immediately — but knowing they
 *  exist means you'll recognize them in real codebases.
 *
 *  Run: npx tsx ch8_enums_and_advanced.ts
 * ============================================================================
 */

// ============================================================================
// 1. ENUMS — Named constants
// ============================================================================

console.log("=== ENUMS ===");

// Enums define a set of named constants. Like Python's enum.Enum.

// --- Numeric enums (values are auto-incremented numbers) ---
enum Direction {
    Up = 0,     // 0
    Down,       // 1 (auto-incremented)
    Left,       // 2
    Right       // 3
}

console.log("Direction.Up:", Direction.Up);           // 0
console.log("Direction.Right:", Direction.Right);     // 3
console.log("Direction[0]:", Direction[0]);           // "Up" (reverse mapping!)

let move: Direction = Direction.Left;
console.log("move:", move, "(which is Direction.Left)");

// --- String enums (explicit string values — PREFERRED) ---
enum Color {
    Red = "RED",
    Green = "GREEN",
    Blue = "BLUE",
    Yellow = "YELLOW"
}

console.log("Color.Red:", Color.Red);       // "RED"
console.log("Color.Blue:", Color.Blue);     // "BLUE"

function paintWall(color: Color): void {
    console.log(`  Painting wall ${color}`);
}
paintWall(Color.Red);
paintWall(Color.Green);

// --- const enums (completely removed at compile time — more efficient) ---
const enum HttpStatus {
    OK = 200,
    NotFound = 404,
    ServerError = 500
}

// These get INLINED as literal values — no enum object at runtime:
let status = HttpStatus.OK;           // becomes just: let status = 200;
console.log("HttpStatus.OK:", status);
console.log("HttpStatus.NotFound:", HttpStatus.NotFound);


// ============================================================================
// 2. ENUMS vs UNION TYPES — Modern TS prefers unions
// ============================================================================

console.log("\n=== ENUMS vs UNIONS ===");

// In modern TypeScript, many developers prefer union types over enums.
// Why?
//   - Unions are simpler (no extra enum object at runtime)
//   - Unions work better with type narrowing
//   - Unions are just types — no extra JavaScript emitted
//   - Unions are more flexible (can be any literal, not just string/number)

// Enum approach:
enum StatusEnum {
    Active = "active",
    Inactive = "inactive",
    Pending = "pending"
}

// Union approach (preferred in modern TS):
type StatusUnion = "active" | "inactive" | "pending";

// Both work, but unions are lighter:
function handleStatus(status: StatusUnion): void {
    console.log(`  Status: ${status}`);
}
handleStatus("active");
handleStatus("pending");

// Rule of thumb:
//   - Use UNIONS for: string/number constants (most cases)
//   - Use ENUMS for: when you need reverse mapping or iteration
//   - Use CONST ENUMS for: performance-critical numeric constants

console.log("Recommendation: prefer union types in modern TypeScript");
console.log("  type Status = 'active' | 'inactive' | 'pending'");


// ============================================================================
// 3. MAPPED TYPES — Transform types programmatically
// ============================================================================

console.log("\n=== MAPPED TYPES ===");

// Mapped types let you create new types by transforming each property
// of an existing type. This is HOW utility types (Partial, Readonly, etc.) work.

// Syntax: { [K in keyof T]: NewType }

interface User {
    name: string;
    email: string;
    age: number;
}

// Make all properties boolean (e.g., for "which fields changed?"):
type BooleanFlags<T> = {
    [K in keyof T]: boolean;
};

let userChanges: BooleanFlags<User> = {
    name: true,
    email: false,
    age: true
};
console.log("userChanges:", userChanges);

// Make all properties into getter functions:
type Getters<T> = {
    [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

// This transforms User into:
// { getName: () => string; getEmail: () => string; getAge: () => number }

let userGetters: Getters<User> = {
    getName: () => "Chint",
    getEmail: () => "chint@example.com",
    getAge: () => 25
};
console.log("getName():", userGetters.getName());
console.log("getAge():", userGetters.getAge());

// Nullable version of all properties:
type Nullable<T> = {
    [K in keyof T]: T[K] | null;
};

let nullableUser: Nullable<User> = {
    name: "Chint",
    email: null,     // OK — can be null
    age: null         // OK — can be null
};
console.log("nullableUser:", nullableUser);


// ============================================================================
// 4. CONDITIONAL TYPES — If/else for types
// ============================================================================

console.log("\n=== CONDITIONAL TYPES ===");

// Conditional types choose between two types based on a condition.
// Syntax: T extends U ? X : Y
//         "If T extends U, then X, else Y"

// Simple example: is it a string?
type IsString<T> = T extends string ? "yes" : "no";

type A = IsString<string>;     // "yes"
type B = IsString<number>;     // "no"
type C = IsString<"hello">;    // "yes" (literal string extends string)

// We can't directly console.log types, but we can show the concept:
let testA: IsString<string> = "yes";
let testB: IsString<number> = "no";
console.log("IsString<string>:", testA);
console.log("IsString<number>:", testB);

// Extract array element type:
type ElementType<T> = T extends (infer E)[] ? E : T;

// Usage demonstrated with variables:
type NumArrayElement = ElementType<number[]>;    // number
type StrElement = ElementType<string>;            // string (not an array, returns T)

let numEl: NumArrayElement = 42;
let strEl: StrElement = "hello";
console.log("ElementType<number[]>:", numEl, "(type is number)");
console.log("ElementType<string>:", strEl, "(type is string, not an array)");

// Flatten Promise type:
type Unwrap<T> = T extends Promise<infer U> ? U : T;
type ResolvedString = Unwrap<Promise<string>>;    // string
type JustNumber = Unwrap<number>;                  // number

let resolved: ResolvedString = "unwrapped";
console.log("Unwrap<Promise<string>>:", resolved, "(type is string)");


// ============================================================================
// 5. TEMPLATE LITERAL TYPES — String pattern types
// ============================================================================

console.log("\n=== TEMPLATE LITERAL TYPES ===");

// Template literal types let you create string types with specific PATTERNS.
// Uses backtick syntax, just like template literal strings.

// Email pattern:
type Email = `${string}@${string}.${string}`;

let validEmail: Email = "chint@example.com";
// let badEmail: Email = "not-an-email";  // ERROR in strict scenarios

console.log("email:", validEmail);

// CSS units:
type CSSUnit = "px" | "em" | "rem" | "%";
type CSSValue = `${number}${CSSUnit}`;

let fontSize: CSSValue = "16px";
let margin: CSSValue = "2rem";
let width: CSSValue = "100%";
console.log("fontSize:", fontSize);
console.log("margin:", margin);
console.log("width:", width);

// Event handler names:
type EventName = "click" | "scroll" | "keypress";
type HandlerName = `on${Capitalize<EventName>}`;
// Result: "onClick" | "onScroll" | "onKeypress"

let handler: HandlerName = "onClick";
console.log("handler:", handler);

// API endpoint pattern:
type ApiVersion = "v1" | "v2";
type Resource = "users" | "posts" | "comments";
type Endpoint = `/api/${ApiVersion}/${Resource}`;
// Result: "/api/v1/users" | "/api/v1/posts" | ... (6 combinations)

let endpoint: Endpoint = "/api/v2/users";
console.log("endpoint:", endpoint);

// Built-in string manipulation types:
type Upper = Uppercase<"hello">;        // "HELLO"
type Lower = Lowercase<"HELLO">;        // "hello"
type Cap = Capitalize<"hello">;          // "Hello"
type Uncap = Uncapitalize<"Hello">;      // "hello"

let upper: Upper = "HELLO";
let cap: Cap = "Hello";
console.log("Uppercase<'hello'>:", upper);
console.log("Capitalize<'hello'>:", cap);


// ============================================================================
// 6. keyof AND typeof OPERATORS
// ============================================================================

console.log("\n=== keyof AND typeof ===");

// keyof: gets all property names of a type as a union
// typeof: gets the type of a JavaScript value

interface Product {
    id: number;
    name: string;
    price: number;
    inStock: boolean;
}

// keyof Product = "id" | "name" | "price" | "inStock"
type ProductKey = keyof Product;

function getField(product: Product, key: ProductKey): Product[ProductKey] {
    return product[key];
}

let laptop: Product = { id: 1, name: "Laptop", price: 999, inStock: true };
console.log("getField(name):", getField(laptop, "name"));
console.log("getField(price):", getField(laptop, "price"));
// getField(laptop, "foo");  // ERROR! "foo" is not a key of Product

// typeof: get the TYPE of a runtime value
const config = {
    apiUrl: "https://api.example.com",
    timeout: 5000,
    retries: 3,
    debug: false
};

// typeof config gives us the inferred type of the config object:
type AppConfig = typeof config;
// Result: { apiUrl: string; timeout: number; retries: number; debug: boolean }

// Useful with keyof:
type ConfigKey = keyof typeof config;
// Result: "apiUrl" | "timeout" | "retries" | "debug"

function getConfig(key: ConfigKey): (typeof config)[ConfigKey] {
    return config[key];
}
console.log("getConfig('apiUrl'):", getConfig("apiUrl"));
console.log("getConfig('timeout'):", getConfig("timeout"));


// ============================================================================
// 7. TYPE PREDICATES — Custom type guards with "is"
// ============================================================================

console.log("\n=== TYPE PREDICATES ===");

// Type predicates let you create CUSTOM type guard functions.
// The return type uses the "is" keyword: param is Type

interface Cat {
    type: "cat";
    meow(): string;
}

interface Dog {
    type: "dog";
    bark(): string;
}

type Pet = Cat | Dog;

// Custom type guard using "is":
function isCat(pet: Pet): pet is Cat {
    return pet.type === "cat";
}

function isDog(pet: Pet): pet is Dog {
    return pet.type === "dog";
}

function petSound(pet: Pet): string {
    if (isCat(pet)) {
        return pet.meow();   // TS KNOWS pet is Cat here
    }
    return pet.bark();       // TS KNOWS pet is Dog here
}

let myCat: Cat = { type: "cat", meow: () => "Meow!" };
let myDog: Dog = { type: "dog", bark: () => "Woof!" };
console.log("cat:", petSound(myCat));
console.log("dog:", petSound(myDog));

// Real-world: checking if a value is a specific shape
function isUser(value: unknown): value is User {
    return (
        typeof value === "object" &&
        value !== null &&
        "name" in value &&
        "email" in value &&
        "age" in value
    );
}

let maybeUser: unknown = { name: "Chint", email: "c@c.com", age: 25 };
if (isUser(maybeUser)) {
    console.log("Validated user:", maybeUser.name);  // TS knows it's User
}

// Filtering arrays with type predicates:
let mixed: (string | number | null)[] = ["hello", 42, null, "world", null, 7];
let strings = mixed.filter((x): x is string => typeof x === "string");
console.log("filtered strings:", strings);  // ["hello", "world"]


// ============================================================================
// 8. tsconfig.json BASICS
// ============================================================================

console.log("\n=== tsconfig.json BASICS ===");

// tsconfig.json configures the TypeScript compiler for your project.
// Here are the most important settings:

console.log("Key tsconfig.json settings:");
console.log('  "strict": true           — Enable ALL strict checks (always use this!)');
console.log('  "target": "ES2020"       — Which JS version to compile to');
console.log('  "module": "ESNext"       — Module system (ESNext for modern, CommonJS for Node)');
console.log('  "outDir": "./dist"       — Where compiled JS goes');
console.log('  "rootDir": "./src"       — Where your TS source files are');
console.log('  "esModuleInterop": true  — Better import compatibility');
console.log('  "resolveJsonModule": true — Allow importing .json files');
console.log('  "declaration": true       — Generate .d.ts type files');
console.log('  "noEmit": true           — Type-check only (when using bundler)');

// Example tsconfig.json:
// {
//   "compilerOptions": {
//     "strict": true,
//     "target": "ES2020",
//     "module": "ESNext",
//     "moduleResolution": "node",
//     "outDir": "./dist",
//     "rootDir": "./src",
//     "esModuleInterop": true,
//     "resolveJsonModule": true,
//     "declaration": true
//   },
//   "include": ["src/**/*"],
//   "exclude": ["node_modules", "dist"]
// }

console.log("\nMost important: ALWAYS use strict: true!");
console.log("It enables: strictNullChecks, noImplicitAny, strictFunctionTypes, etc.");


// ============================================================================
// 9. MODULE PATTERNS — import/export with types
// ============================================================================

console.log("\n=== MODULE PATTERNS ===");

// TypeScript fully supports ES modules (import/export).
// You can also import/export TYPES specifically.

// Export a type (in a real module file):
//   export interface User { name: string; email: string; }
//   export type ID = string | number;

// Import a type:
//   import { User, ID } from "./types";

// Import TYPE ONLY (removed at compile time — no runtime cost):
//   import type { User } from "./types";

// This is important for:
//   - Bundler optimization (tree shaking)
//   - Clarity about what's a type vs a value

console.log("Type-only imports: import type { User } from './types'");
console.log("  - Removed at compile time (no runtime cost)");
console.log("  - Makes it clear this is just a type, not a value");

// Re-exporting types:
//   export type { User } from "./models";
//   export { type User, createUser } from "./models";

console.log("\nCommon module patterns:");
console.log("  types.ts      — shared type definitions");
console.log("  models/       — interfaces and types for data models");
console.log("  utils/        — utility functions with typed signatures");
console.log("  index.ts      — barrel file that re-exports everything");


// ============================================================================
// 10. DECLARATION FILES (.d.ts)
// ============================================================================

console.log("\n=== DECLARATION FILES (.d.ts) ===");

// .d.ts files contain ONLY type information — no runtime code.
// They tell TypeScript about the types in JavaScript libraries.

// When you install a library:
//   npm install lodash               — JavaScript library (no types)
//   npm install @types/lodash         — Type declarations for lodash

// The @types/ packages on npm are from DefinitelyTyped — a HUGE repo of
// community-maintained type declarations for JavaScript libraries.

// Modern libraries often ship their own types:
//   npm install axios    — includes its own .d.ts files!

console.log("Declaration files (.d.ts):");
console.log("  - Contain ONLY types (no runtime code)");
console.log("  - Let TypeScript understand JavaScript libraries");
console.log("  - @types/xxx packages from DefinitelyTyped");
console.log("  - Modern libraries ship their own .d.ts files");
console.log("  - Generated by tsc with 'declaration: true' in tsconfig");

// Writing a simple .d.ts file (for a JS library without types):
//
// // mylib.d.ts
// declare module "mylib" {
//     export function doSomething(input: string): number;
//     export interface Config {
//         verbose: boolean;
//         timeout: number;
//     }
// }


// ============================================================================
// 11. TIPS FOR MIGRATING JS TO TS
// ============================================================================

console.log("\n=== JS TO TS MIGRATION TIPS ===");

let tips = [
    "1. Rename .js to .ts (start with one file at a time)",
    "2. Use 'strict: false' initially, then enable strict checks one by one",
    "3. Use 'any' as a temporary escape hatch — then gradually replace",
    "4. Add types to function signatures FIRST (biggest bang for buck)",
    "5. Create interfaces for your data shapes (API responses, DB records)",
    "6. Install @types/ packages for your dependencies",
    "7. Enable 'noImplicitAny' once you've typed the obvious stuff",
    "8. Use 'unknown' instead of 'any' for values you'll type later",
    "9. Don't try to type EVERYTHING at once — incremental is fine",
    "10. TypeScript can check .js files too! Add // @ts-check at the top"
];

for (let tip of tips) {
    console.log(`  ${tip}`);
}

// Migration order for a typical project:
console.log("\nMigration order:");
console.log("  1. Add tsconfig.json (with allowJs: true)");
console.log("  2. Rename entry point .js -> .ts");
console.log("  3. Fix errors (add types, install @types/)");
console.log("  4. Rename more files, fix errors, repeat");
console.log("  5. Enable strict mode when most files are typed");


// ============================================================================
// 12. BONUS: Type assertions and the "as const" pattern
// ============================================================================

console.log("\n=== BONUS: as const ===");

// "as const" makes values deeply readonly and gives them literal types.
// Incredibly useful for configuration objects and constant arrays.

// Without "as const":
let colors = ["red", "green", "blue"];        // type: string[]
let point = { x: 10, y: 20 };                 // type: { x: number; y: number }

// With "as const":
let colorsConst = ["red", "green", "blue"] as const;
// type: readonly ["red", "green", "blue"]

let pointConst = { x: 10, y: 20 } as const;
// type: { readonly x: 10; readonly y: 20 }

// This is amazing for creating types from values:
const ROLES = ["admin", "user", "guest"] as const;
type Role = typeof ROLES[number];  // "admin" | "user" | "guest"

let role: Role = "admin";
console.log("role:", role);
console.log("ROLES:", ROLES);

// Configuration with as const:
const API_ENDPOINTS = {
    users: "/api/users",
    posts: "/api/posts",
    comments: "/api/comments"
} as const;

type EndpointKey = keyof typeof API_ENDPOINTS;     // "users" | "posts" | "comments"
type EndpointValue = typeof API_ENDPOINTS[EndpointKey]; // "/api/users" | "/api/posts" | "/api/comments"

function fetchFromEndpoint(key: EndpointKey): void {
    console.log(`  Fetching from ${API_ENDPOINTS[key]}`);
}

fetchFromEndpoint("users");
fetchFromEndpoint("posts");


// ============================================================================
// FINAL RECAP — THE WHOLE COURSE
// ============================================================================

console.log("\n" + "=".repeat(60));
console.log("  TYPESCRIPT COURSE — COMPLETE!");
console.log("=".repeat(60));

console.log("\nChapter 1: Basic Types");
console.log("  string, number, boolean, null, undefined, any, unknown, void");

console.log("\nChapter 2: Arrays, Objects & Interfaces");
console.log("  number[], [string, number], interface User { ... }");

console.log("\nChapter 3: Functions");
console.log("  Typed params, optional/default/rest, function types, overloads");

console.log("\nChapter 4: Unions, Intersections & Narrowing");
console.log("  A | B, A & B, typeof/instanceof/in guards, discriminated unions");

console.log("\nChapter 5: Generics");
console.log("  function first<T>(arr: T[]): T, constraints, generic classes");

console.log("\nChapter 6: Classes");
console.log("  public/private/protected, readonly, abstract, implements");

console.log("\nChapter 7: Utility Types");
console.log("  Partial, Required, Readonly, Pick, Omit, Record, and more");

console.log("\nChapter 8: Enums & Advanced (this chapter)");
console.log("  Enums vs unions, mapped types, conditional types, keyof/typeof");

console.log("\nYou now have a SOLID foundation in TypeScript!");
console.log("Next steps:");
console.log("  1. Build something! (a Node.js API, a React app, a CLI tool)");
console.log("  2. Read the TypeScript Handbook: typescriptlang.org/docs/handbook");
console.log("  3. Practice on: typehero.dev, type-challenges on GitHub");
console.log("  4. Use TypeScript in your JavaScript course projects!");
