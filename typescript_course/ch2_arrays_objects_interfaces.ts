/*
 * ============================================================================
 *  TYPESCRIPT COURSE — Chapter 2: Arrays, Objects & Interfaces
 * ============================================================================
 *
 *  In Chapter 1 we learned basic types (string, number, boolean).
 *  Now we'll learn how to type COLLECTIONS and STRUCTURES:
 *    - Arrays (lists of things)
 *    - Tuples (fixed-length arrays with specific types per position)
 *    - Objects (key-value structures)
 *    - Interfaces (named shapes for objects — you'll use these EVERYWHERE)
 *    - Type aliases (another way to name types)
 *
 *  PYTHON COMPARISON:
 *    Python:      List[int], Tuple[str, int], TypedDict, dataclass
 *    TypeScript:  number[], [string, number], interface, type
 *
 *  Run: npx tsx ch2_arrays_objects_interfaces.ts
 * ============================================================================
 */

// ============================================================================
// 1. TYPED ARRAYS — Lists with types
// ============================================================================

console.log("=== TYPED ARRAYS ===");

// Two equivalent syntaxes for typed arrays:
let scores: number[] = [95, 87, 92, 78];           // Syntax 1: type[] (preferred)
let names: Array<string> = ["Alice", "Bob", "Chint"]; // Syntax 2: Array<type> (generic style)

// Both are identical. Most people use the first syntax (number[], string[]).
console.log("scores:", scores);
console.log("names:", names);

// TypeScript enforces the element types:
// scores.push("hello");  // ERROR! Can't push a string into number[]

// You can also let TS infer the array type:
let fruits = ["apple", "banana", "cherry"];  // TS infers: string[]
let mixed = [1, "two", 3];                   // TS infers: (string | number)[]
console.log("fruits (inferred string[]):", fruits);
console.log("mixed (inferred (string|number)[]):", mixed);

// Array of arrays (2D array — like a matrix):
let grid: number[][] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];
console.log("grid:", grid);

// Readonly arrays — can't be modified after creation:
let frozenList: readonly number[] = [1, 2, 3];
// frozenList.push(4);    // ERROR! readonly
// frozenList[0] = 99;    // ERROR! readonly
console.log("frozenList (readonly):", frozenList);


// ============================================================================
// 2. TUPLE TYPES — Fixed-length, typed-position arrays
// ============================================================================

console.log("\n=== TUPLE TYPES ===");

// A tuple is an array where:
//   - The LENGTH is fixed
//   - Each POSITION has a specific type
//
// Python comparison:
//   Python:      Tuple[str, int]           (from typing)
//   TypeScript:  [string, number]

// A coordinate pair:
let point: [number, number] = [10, 20];
console.log("point:", point);
console.log("x:", point[0], "y:", point[1]);

// A name-age pair:
let person: [string, number] = ["Chint", 25];
console.log("person:", person);

// TypeScript enforces position types:
// let bad: [string, number] = [25, "Chint"];  // ERROR! Wrong order

// Named tuple elements (for documentation):
let userEntry: [name: string, age: number, active: boolean] = ["Alice", 30, true];
console.log("userEntry:", userEntry);

// Tuples with optional elements:
let flexPoint: [number, number, number?] = [10, 20];  // z is optional
console.log("flexPoint (2D):", flexPoint);
flexPoint = [10, 20, 30];  // Now with z
console.log("flexPoint (3D):", flexPoint);

// Real-world use: destructuring tuples (like React's useState)
// const [state, setState] = useState(0);  // returns [number, function]
let httpResponse: [number, string] = [200, "OK"];
let [statusCode, statusText] = httpResponse;  // destructuring
console.log("status:", statusCode, statusText);


// ============================================================================
// 3. OBJECTS WITH INLINE TYPES
// ============================================================================

console.log("\n=== OBJECTS WITH INLINE TYPES ===");

// You can type an object inline — useful for one-off structures.
let user: { name: string; age: number; email: string } = {
    name: "Chint",
    age: 25,
    email: "chint@example.com"
};
console.log("user:", user);

// But inline types get messy when you reuse them. That's where interfaces come in.

// Object with a method:
let calculator: { add: (a: number, b: number) => number } = {
    add: (a, b) => a + b
};
console.log("calculator.add(3, 4):", calculator.add(3, 4));


// ============================================================================
// 4. INTERFACES — Named shapes for objects
// ============================================================================

console.log("\n=== INTERFACES ===");

// An interface defines the SHAPE of an object — what properties it must have.
// This is one of TypeScript's most important features.
//
// Python comparison:
//   Python:      TypedDict or @dataclass
//   TypeScript:  interface

interface User {
    name: string;
    email: string;
    age: number;
}

// Now we can use User as a type:
let alice: User = {
    name: "Alice",
    email: "alice@example.com",
    age: 30
};

let bob: User = {
    name: "Bob",
    email: "bob@example.com",
    age: 28
};

console.log("alice:", alice);
console.log("bob:", bob);

// If you forget a property, TypeScript catches it:
// let incomplete: User = { name: "Eve" };  // ERROR! Missing email and age

// If you add an extra property directly, TypeScript catches that too:
// let extra: User = { name: "Eve", email: "e@e.com", age: 25, foo: "bar" }; // ERROR!


// ============================================================================
// 5. OPTIONAL & READONLY PROPERTIES
// ============================================================================

console.log("\n=== OPTIONAL & READONLY ===");

// Optional properties — might or might not exist (use ?)
interface Profile {
    username: string;
    bio?: string;           // optional — may be undefined
    avatarUrl?: string;     // optional
}

let profile1: Profile = { username: "chint_codes" };  // OK — bio and avatar are optional
let profile2: Profile = { username: "alice", bio: "TypeScript fan" };

console.log("profile1:", profile1);
console.log("profile2:", profile2);
console.log("profile1.bio:", profile1.bio);  // undefined (not set)

// Readonly properties — can't be changed after creation
interface Config {
    readonly apiKey: string;
    readonly baseUrl: string;
    timeout: number;             // this one CAN be changed
}

let config: Config = {
    apiKey: "abc123",
    baseUrl: "https://api.example.com",
    timeout: 5000
};

config.timeout = 10000;   // OK — timeout is mutable
// config.apiKey = "xyz";  // ERROR! apiKey is readonly

console.log("config:", config);


// ============================================================================
// 6. TYPE ALIASES — Another way to name types
// ============================================================================

console.log("\n=== TYPE ALIASES ===");

// The "type" keyword creates an alias for ANY type — not just objects.

// Simple alias:
type UserID = string | number;  // Can be either string or number

let id1: UserID = "abc-123";
let id2: UserID = 42;
console.log("id1:", id1);
console.log("id2:", id2);

// Object type alias (works like an interface):
type Point = {
    x: number;
    y: number;
};

let origin: Point = { x: 0, y: 0 };
console.log("origin:", origin);

// Type alias for a function signature:
type MathOp = (a: number, b: number) => number;

let multiply: MathOp = (a, b) => a * b;
console.log("multiply(6, 7):", multiply(6, 7));

// Type alias for a union of literals:
type Direction = "up" | "down" | "left" | "right";
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";

let dir: Direction = "up";
let method: HttpMethod = "POST";
console.log("direction:", dir, "  method:", method);


// ============================================================================
// 7. INTERFACE vs TYPE ALIAS — When to use which
// ============================================================================

console.log("\n=== INTERFACE vs TYPE ===");

// Both can describe object shapes. Key differences:
//
// INTERFACE:
//   - Can be extended (interface B extends A)
//   - Can be "declaration merged" (add properties later)
//   - Best for: object shapes, class contracts, public APIs
//
// TYPE ALIAS:
//   - Can represent ANY type (unions, primitives, tuples, etc.)
//   - Cannot be re-opened / merged
//   - Best for: unions, intersections, function types, computed types
//
// Rule of thumb:
//   - Use INTERFACE for objects and class shapes
//   - Use TYPE for everything else (unions, tuples, function types)

// Declaration merging (only interfaces can do this):
interface Animal {
    name: string;
}
interface Animal {      // Same name — TypeScript MERGES them
    sound: string;
}
// Now Animal has BOTH name and sound
let dog: Animal = { name: "Rex", sound: "Woof" };
console.log("dog (merged interface):", dog);

// Type aliases CANNOT be merged:
// type Fruit = { name: string };
// type Fruit = { color: string };  // ERROR! Duplicate identifier


// ============================================================================
// 8. EXTENDING INTERFACES — Building on existing shapes
// ============================================================================

console.log("\n=== EXTENDING INTERFACES ===");

// Interfaces can extend other interfaces — like class inheritance.
// Python comparison: similar to class inheritance, or TypedDict inheritance

interface BaseUser {
    id: number;
    name: string;
    email: string;
}

interface Admin extends BaseUser {
    role: string;
    permissions: string[];
}

interface SuperAdmin extends Admin {
    canDeleteUsers: boolean;
}

let admin: Admin = {
    id: 1,
    name: "Chint",
    email: "chint@example.com",
    role: "moderator",
    permissions: ["edit", "delete", "ban"]
};
console.log("admin:", admin);

let superAdmin: SuperAdmin = {
    id: 0,
    name: "Root",
    email: "root@example.com",
    role: "superadmin",
    permissions: ["everything"],
    canDeleteUsers: true
};
console.log("superAdmin:", superAdmin);

// You can also extend MULTIPLE interfaces:
interface HasTimestamps {
    createdAt: Date;
    updatedAt: Date;
}

interface BlogPost extends BaseUser, HasTimestamps {
    title: string;
    content: string;
}

// Type aliases use & (intersection) instead of extends:
type TaggedItem = BaseUser & { tags: string[] };
let taggedUser: TaggedItem = {
    id: 2,
    name: "Alice",
    email: "alice@example.com",
    tags: ["typescript", "javascript"]
};
console.log("taggedUser:", taggedUser);


// ============================================================================
// 9. INDEX SIGNATURES — Dynamic keys
// ============================================================================

console.log("\n=== INDEX SIGNATURES ===");

// Sometimes you don't know all the property names ahead of time.
// Index signatures let you describe the TYPE of keys and values.
//
// Python comparison: Dict[str, int]  ~  { [key: string]: number }

interface ScoreBoard {
    [playerName: string]: number;   // any string key, number value
}

let scores2: ScoreBoard = {
    alice: 95,
    bob: 87,
    chint: 92
};
scores2["diana"] = 88;  // Can add new keys
console.log("scoreboard:", scores2);

// You can mix index signatures with known properties:
interface FlexibleUser {
    name: string;                   // required
    email: string;                  // required
    [key: string]: string;          // any other string properties are OK
}

let flexUser: FlexibleUser = {
    name: "Chint",
    email: "chint@example.com",
    nickname: "C",
    twitter: "@chint"
};
console.log("flexUser:", flexUser);

// Record type is a shorthand for index signatures (preview — more in ch7):
let wordCounts: Record<string, number> = {
    hello: 5,
    world: 3,
    typescript: 12
};
console.log("wordCounts:", wordCounts);


// ============================================================================
// 10. PUTTING IT ALL TOGETHER — A real example
// ============================================================================

console.log("\n=== PUTTING IT ALL TOGETHER ===");

// Let's model a simple blog system:

interface Author {
    readonly id: number;
    name: string;
    bio?: string;
}

interface Post {
    readonly id: number;
    title: string;
    content: string;
    author: Author;          // nested interface!
    tags: string[];          // array of strings
    published: boolean;
    metadata: {              // inline nested object type
        views: number;
        likes: number;
    };
}

let post: Post = {
    id: 1,
    title: "Why TypeScript is Awesome",
    content: "Because it catches bugs before you run your code...",
    author: {
        id: 42,
        name: "Chint",
        bio: "Learning TS!"
    },
    tags: ["typescript", "javascript", "tutorial"],
    published: true,
    metadata: { views: 1500, likes: 42 }
};

function displayPost(p: Post): void {
    console.log(`  Title: ${p.title}`);
    console.log(`  Author: ${p.author.name}`);
    console.log(`  Tags: ${p.tags.join(", ")}`);
    console.log(`  Views: ${p.metadata.views}  Likes: ${p.metadata.likes}`);
    console.log(`  Published: ${p.published ? "Yes" : "Draft"}`);
}

console.log("Blog Post:");
displayPost(post);


// ============================================================================
// RECAP
// ============================================================================

console.log("\n=== CHAPTER 2 RECAP ===");
console.log("1. Typed arrays: number[], string[], Array<T>");
console.log("2. Tuples: [string, number] — fixed length, typed positions");
console.log("3. Inline object types: { name: string; age: number }");
console.log("4. Interfaces: named object shapes (most common way to type objects)");
console.log("5. Optional (?), readonly properties");
console.log("6. Type aliases: type X = ... (for unions, functions, primitives)");
console.log("7. Interface vs Type: use interface for objects, type for everything else");
console.log("8. Extending interfaces: interface Admin extends User");
console.log("9. Index signatures: { [key: string]: number } for dynamic keys");
console.log("\nNext up: Chapter 3 — Functions!");
