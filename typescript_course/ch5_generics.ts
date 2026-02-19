/*
 * ============================================================================
 *  TYPESCRIPT COURSE — Chapter 5: Generics
 * ============================================================================
 *
 *  Generics let you write functions, interfaces, and classes that work with
 *  ANY type — while still keeping type safety. They're like "type variables."
 *
 *  Without generics: you'd have to write separate functions for each type,
 *  or use "any" (which loses type safety). Generics give you BOTH.
 *
 *  PYTHON COMPARISON:
 *    Python:      from typing import TypeVar, Generic
 *                 T = TypeVar('T')
 *                 def first(items: list[T]) -> T: ...
 *
 *    TypeScript:  function first<T>(items: T[]): T { ... }
 *
 *  Same idea, but TypeScript's syntax is cleaner and it's ENFORCED.
 *
 *  Run: npx tsx ch5_generics.ts
 * ============================================================================
 */

// ============================================================================
// 1. WHY GENERICS? — The problem they solve
// ============================================================================

console.log("=== WHY GENERICS? ===");

// Problem: You want a function that wraps ANY value in an object.

// Bad approach 1: Use "any" — LOSES type information
function wrapAny(value: any): { value: any } {
    return { value };
}
let wrappedAny = wrapAny("hello");
// wrappedAny.value is type "any" — TS doesn't know it's a string!

// Bad approach 2: Write separate functions for each type
function wrapString(value: string): { value: string } {
    return { value };
}
function wrapNumber(value: number): { value: number } {
    return { value };
}
// This doesn't scale — what about boolean, Date, custom types, etc.?

// GOOD approach: Use generics!
function wrap<T>(value: T): { value: T } {
    return { value };
}

// T is a "type variable" — it gets replaced with the actual type:
let wrappedStr = wrap("hello");     // T = string, returns { value: string }
let wrappedNum = wrap(42);          // T = number, returns { value: number }
let wrappedBool = wrap(true);       // T = boolean, returns { value: boolean }

console.log("wrap('hello'):", wrappedStr);        // { value: 'hello' }
console.log("wrap(42):", wrappedNum);              // { value: 42 }
console.log("wrap(true):", wrappedBool);           // { value: true }

// TS inferred T automatically! You CAN be explicit:
let explicit = wrap<string>("explicit");
console.log("wrap<string>('explicit'):", explicit);


// ============================================================================
// 2. GENERIC FUNCTIONS
// ============================================================================

console.log("\n=== GENERIC FUNCTIONS ===");

// The <T> goes right before the parameters.
// Convention: T for "type", but you can use any name.
// Common names: T, U, V, K (key), V (value), E (element)

// Get the first element of any array:
function first<T>(arr: T[]): T | undefined {
    return arr[0];
}
console.log("first([10, 20, 30]):", first([10, 20, 30]));
console.log("first(['a', 'b', 'c']):", first(["a", "b", "c"]));
console.log("first([]):", first([]));

// Get the last element:
function last<T>(arr: T[]): T | undefined {
    return arr[arr.length - 1];
}
console.log("last([10, 20, 30]):", last([10, 20, 30]));

// Reverse an array (returns new array, doesn't mutate):
function reverse<T>(arr: T[]): T[] {
    return [...arr].reverse();
}
console.log("reverse([1, 2, 3]):", reverse([1, 2, 3]));
console.log("reverse(['a', 'b', 'c']):", reverse(["a", "b", "c"]));

// Map with a generic transform:
function mapArray<T, U>(arr: T[], transform: (item: T) => U): U[] {
    return arr.map(transform);
}
let lengths = mapArray(["hello", "world", "ts"], (s) => s.length);
let doubled = mapArray([1, 2, 3], (n) => n * 2);
console.log("mapArray strings->lengths:", lengths);
console.log("mapArray numbers->doubled:", doubled);

// Arrow function with generics:
const identity = <T>(value: T): T => value;
console.log("identity(42):", identity(42));
console.log("identity('hello'):", identity("hello"));


// ============================================================================
// 3. GENERIC INTERFACES
// ============================================================================

console.log("\n=== GENERIC INTERFACES ===");

// Interfaces can be generic too — define the shape once, use with any type.

// A box that holds any type:
interface Box<T> {
    value: T;
    label: string;
}

let stringBox: Box<string> = { value: "TypeScript", label: "language" };
let numberBox: Box<number> = { value: 42, label: "answer" };
let arrayBox: Box<string[]> = { value: ["a", "b"], label: "letters" };

console.log("stringBox:", stringBox);
console.log("numberBox:", numberBox);
console.log("arrayBox:", arrayBox);

// A pair of two different types:
interface Pair<A, B> {
    first: A;
    second: B;
}

let nameAge: Pair<string, number> = { first: "Chint", second: 25 };
let coordinates: Pair<number, number> = { first: 40.7, second: -74.0 };
console.log("nameAge:", nameAge);
console.log("coordinates:", coordinates);

// Generic interface for a result (success or failure):
interface Result<T> {
    success: boolean;
    data?: T;
    error?: string;
}

function divide(a: number, b: number): Result<number> {
    if (b === 0) return { success: false, error: "Division by zero" };
    return { success: true, data: a / b };
}

console.log("divide(10, 3):", divide(10, 3));
console.log("divide(10, 0):", divide(10, 0));


// ============================================================================
// 4. GENERIC CLASSES
// ============================================================================

console.log("\n=== GENERIC CLASSES ===");

// Classes can be generic — great for data structures.
// Python comparison: class Stack(Generic[T]): ...

class Stack<T> {
    private items: T[] = [];

    push(item: T): void {
        this.items.push(item);
    }

    pop(): T | undefined {
        return this.items.pop();
    }

    peek(): T | undefined {
        return this.items[this.items.length - 1];
    }

    get size(): number {
        return this.items.length;
    }

    toArray(): T[] {
        return [...this.items];
    }
}

// Stack of numbers:
let numStack = new Stack<number>();
numStack.push(10);
numStack.push(20);
numStack.push(30);
console.log("numStack:", numStack.toArray());
console.log("numStack.pop():", numStack.pop());
console.log("numStack.peek():", numStack.peek());

// Stack of strings:
let strStack = new Stack<string>();
strStack.push("hello");
strStack.push("world");
console.log("strStack:", strStack.toArray());
console.log("strStack.size:", strStack.size);

// A generic key-value store:
class KeyValueStore<K, V> {
    private store = new Map<K, V>();

    set(key: K, value: V): void {
        this.store.set(key, value);
    }

    get(key: K): V | undefined {
        return this.store.get(key);
    }

    has(key: K): boolean {
        return this.store.has(key);
    }

    entries(): [K, V][] {
        return [...this.store.entries()];
    }
}

let userStore = new KeyValueStore<number, string>();
userStore.set(1, "Alice");
userStore.set(2, "Bob");
userStore.set(3, "Chint");
console.log("userStore.get(2):", userStore.get(2));
console.log("userStore entries:", userStore.entries());


// ============================================================================
// 5. GENERIC CONSTRAINTS — Limiting what T can be
// ============================================================================

console.log("\n=== GENERIC CONSTRAINTS ===");

// Sometimes you need T to have certain properties.
// Use "extends" to constrain what types T can be.

// Constraint: T must have a .length property
interface HasLength {
    length: number;
}

function logLength<T extends HasLength>(item: T): void {
    console.log(`  Length of ${JSON.stringify(item)}: ${item.length}`);
}

logLength("hello");        // string has .length
logLength([1, 2, 3]);     // array has .length
logLength({ length: 42 }); // object with .length
// logLength(42);           // ERROR! number doesn't have .length

// Constraint: T must be an object with specific properties
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

let person = { name: "Chint", age: 25, city: "NYC" };
console.log("getProperty name:", getProperty(person, "name"));
console.log("getProperty age:", getProperty(person, "age"));
// getProperty(person, "foo");  // ERROR! "foo" is not a key of person

// Constraint: T must be a certain shape
interface Identifiable {
    id: number;
}

function findById<T extends Identifiable>(items: T[], id: number): T | undefined {
    return items.find(item => item.id === id);
}

let users = [
    { id: 1, name: "Alice", email: "a@a.com" },
    { id: 2, name: "Bob", email: "b@b.com" },
    { id: 3, name: "Chint", email: "c@c.com" }
];

console.log("findById(2):", findById(users, 2));


// ============================================================================
// 6. MULTIPLE TYPE PARAMETERS
// ============================================================================

console.log("\n=== MULTIPLE TYPE PARAMETERS ===");

// Functions can have multiple type parameters: <K, V>, <T, U>, etc.

function zip<A, B>(arrA: A[], arrB: B[]): [A, B][] {
    let length = Math.min(arrA.length, arrB.length);
    let result: [A, B][] = [];
    for (let i = 0; i < length; i++) {
        result.push([arrA[i], arrB[i]]);
    }
    return result;
}

let names = ["Alice", "Bob", "Chint"];
let ages = [30, 28, 25];
console.log("zip(names, ages):", zip(names, ages));

let letters = ["a", "b", "c"];
let numbers = [1, 2, 3];
console.log("zip(letters, numbers):", zip(letters, numbers));

// Swap two values:
function swap<A, B>(pair: [A, B]): [B, A] {
    return [pair[1], pair[0]];
}
console.log("swap(['hello', 42]):", swap(["hello", 42]));


// ============================================================================
// 7. DEFAULT TYPE PARAMETERS
// ============================================================================

console.log("\n=== DEFAULT TYPE PARAMETERS ===");

// Like default function parameters, you can give type parameters defaults.
// Python comparison: class MyClass(Generic[T]): ... doesn't really have defaults

interface ApiResponse<T = unknown> {
    status: number;
    data: T;
    message: string;
}

// With a specific type:
let userResponse: ApiResponse<{ name: string }> = {
    status: 200,
    data: { name: "Chint" },
    message: "OK"
};

// With the default (unknown):
let genericResponse: ApiResponse = {
    status: 500,
    data: null,
    message: "Internal error"
};

console.log("userResponse:", userResponse);
console.log("genericResponse:", genericResponse);

// Default with constraint:
interface Collection<T extends object = Record<string, unknown>> {
    items: T[];
    count: number;
}

let defaultCollection: Collection = {
    items: [{ a: 1 }, { b: 2 }],
    count: 2
};
console.log("defaultCollection:", defaultCollection);


// ============================================================================
// 8. GENERIC UTILITY EXAMPLE — API Response Wrapper
// ============================================================================

console.log("\n=== API RESPONSE WRAPPER ===");

// Real-world pattern: a generic wrapper for API responses.

interface SuccessResult<T> {
    ok: true;
    data: T;
}

interface ErrorResult {
    ok: false;
    error: string;
}

type ApiResult<T> = SuccessResult<T> | ErrorResult;

// Generic fetch function:
function createSuccess<T>(data: T): ApiResult<T> {
    return { ok: true, data };
}

function createError<T>(message: string): ApiResult<T> {
    return { ok: false, error: message };
}

// Usage:
interface User {
    id: number;
    name: string;
    email: string;
}

function fetchUser(id: number): ApiResult<User> {
    // Simulating an API call:
    if (id === 1) {
        return createSuccess({ id: 1, name: "Chint", email: "chint@example.com" });
    }
    return createError(`User ${id} not found`);
}

let result1 = fetchUser(1);
let result2 = fetchUser(999);

// Handle the result with narrowing:
function displayResult<T>(result: ApiResult<T>): void {
    if (result.ok) {
        console.log("  Success:", result.data);
    } else {
        console.log("  Error:", result.error);
    }
}

displayResult(result1);
displayResult(result2);


// ============================================================================
// 9. REAL-WORLD EXAMPLE — Generic Fetch Function
// ============================================================================

console.log("\n=== GENERIC FETCH FUNCTION ===");

// A type-safe mock fetch that demonstrates the pattern:

// Mock database:
const mockDB: Record<string, unknown[]> = {
    "/users": [
        { id: 1, name: "Alice" },
        { id: 2, name: "Bob" }
    ],
    "/posts": [
        { id: 1, title: "Hello TS", author: "Alice" },
        { id: 2, title: "Generics Rule", author: "Bob" }
    ]
};

// Generic fetch:
async function fetchData<T>(endpoint: string): Promise<ApiResult<T[]>> {
    // Simulate network delay
    const data = mockDB[endpoint];
    if (data) {
        return createSuccess(data as T[]);
    }
    return createError(`Endpoint ${endpoint} not found`);
}

// Type-safe usage:
interface Post {
    id: number;
    title: string;
    author: string;
}

// We use an async IIFE to demonstrate:
(async () => {
    let usersResult = await fetchData<User>("/users");
    let postsResult = await fetchData<Post>("/posts");
    let badResult = await fetchData<unknown>("/nonexistent");

    console.log("Users:");
    displayResult(usersResult);
    console.log("Posts:");
    displayResult(postsResult);
    console.log("Bad endpoint:");
    displayResult(badResult);


    // ============================================================================
    // 10. GENERIC TYPE MANIPULATION — Building blocks for Ch7
    // ============================================================================

    console.log("\n=== GENERIC TYPE MANIPULATION ===");

    // You can use generics to BUILD new types from existing ones.
    // This is a teaser for Chapter 7 (Utility Types).

    // Make all properties optional:
    type MyPartial<T> = {
        [K in keyof T]?: T[K];
    };

    interface FullUser {
        name: string;
        email: string;
        age: number;
    }

    // All properties are now optional:
    let partialUser: MyPartial<FullUser> = { name: "Chint" };
    console.log("partialUser:", partialUser);

    // Make all properties readonly:
    type MyReadonly<T> = {
        readonly [K in keyof T]: T[K];
    };

    let frozenUser: MyReadonly<FullUser> = {
        name: "Chint",
        email: "chint@example.com",
        age: 25
    };
    // frozenUser.name = "Alice";  // ERROR! readonly
    console.log("frozenUser:", frozenUser);

    // Pick specific properties:
    type MyPick<T, K extends keyof T> = {
        [P in K]: T[P];
    };

    let nameOnly: MyPick<FullUser, "name" | "email"> = {
        name: "Chint",
        email: "chint@example.com"
    };
    console.log("nameOnly:", nameOnly);

    console.log("\n(These utilities are built-in as Partial<T>, Readonly<T>, Pick<T, K>)");
    console.log("We'll cover ALL built-in utility types in Chapter 7!");


    // ============================================================================
    // RECAP
    // ============================================================================

    console.log("\n=== CHAPTER 5 RECAP ===");
    console.log("1. Generics: <T> = type variables that work with ANY type");
    console.log("2. Generic functions: function first<T>(arr: T[]): T");
    console.log("3. Generic interfaces: interface Box<T> { value: T }");
    console.log("4. Generic classes: class Stack<T> { push(item: T) }");
    console.log("5. Constraints: <T extends HasLength> — T must have .length");
    console.log("6. Multiple params: <K, V>, <A, B>");
    console.log("7. Defaults: <T = string>");
    console.log("8. Real-world: API response wrappers, typed fetch functions");
    console.log("\nNext up: Chapter 6 — Classes!");
})();
