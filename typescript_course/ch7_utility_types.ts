/*
 * ============================================================================
 *  TYPESCRIPT COURSE — Chapter 7: Utility Types
 * ============================================================================
 *
 *  TypeScript comes with BUILT-IN types that transform other types.
 *  These are called "utility types" and they're INCREDIBLY useful.
 *
 *  Instead of creating new types from scratch, you transform existing ones:
 *    - Make all properties optional: Partial<User>
 *    - Make all properties readonly: Readonly<User>
 *    - Pick specific properties: Pick<User, "name" | "email">
 *    - Remove specific properties: Omit<User, "password">
 *
 *  These save TONS of code and keep your types DRY (Don't Repeat Yourself).
 *
 *  PYTHON COMPARISON:
 *    Python doesn't have built-in type transformers like these.
 *    The closest things are typing.Optional and TypedDict with total=False.
 *    TypeScript's utility types are far more powerful.
 *
 *  Run: npx tsx ch7_utility_types.ts
 * ============================================================================
 */

// Base type we'll use throughout this chapter:
interface User {
    id: number;
    name: string;
    email: string;
    age: number;
    role: "admin" | "user" | "guest";
}

// ============================================================================
// 1. Partial<T> — Make all properties optional
// ============================================================================

console.log("=== Partial<T> ===");

// Partial<T> takes a type and makes EVERY property optional.
// Incredibly useful for update functions where you only change some fields.

// Without Partial, you'd need a separate interface:
// interface UserUpdate { name?: string; email?: string; age?: number; ... }

// With Partial, just transform the existing type:
function updateUser(user: User, updates: Partial<User>): User {
    return { ...user, ...updates };
}

let originalUser: User = {
    id: 1,
    name: "Chint",
    email: "chint@example.com",
    age: 25,
    role: "user"
};

// Only update name and age — other properties stay the same:
let updated = updateUser(originalUser, { name: "Chint Updated", age: 26 });
console.log("original:", originalUser);
console.log("updated:", updated);

// Partial<User> is equivalent to:
// {
//     id?: number;
//     name?: string;
//     email?: string;
//     age?: number;
//     role?: "admin" | "user" | "guest";
// }

// Real-world: form state where fields are filled in gradually
type FormState = Partial<User>;
let form: FormState = {};           // start empty
form.name = "Chint";                // fill in gradually
form.email = "chint@example.com";
console.log("form (partial):", form);


// ============================================================================
// 2. Required<T> — Make all properties required
// ============================================================================

console.log("\n=== Required<T> ===");

// Required<T> is the OPPOSITE of Partial — makes everything required.
// Useful when you have a type with optional properties but need them all.

interface Settings {
    theme?: "light" | "dark";
    fontSize?: number;
    language?: string;
    notifications?: boolean;
}

// Settings has all optional properties. Required<Settings> makes them all required.
function applySettings(settings: Required<Settings>): void {
    console.log("  Theme:", settings.theme);
    console.log("  Font size:", settings.fontSize);
    console.log("  Language:", settings.language);
    console.log("  Notifications:", settings.notifications);
}

// Must provide ALL properties:
applySettings({
    theme: "dark",
    fontSize: 16,
    language: "en",
    notifications: true
});

// This would ERROR because Required demands all properties:
// applySettings({ theme: "dark" });  // ERROR! Missing fontSize, language, notifications


// ============================================================================
// 3. Readonly<T> — Make all properties readonly
// ============================================================================

console.log("\n=== Readonly<T> ===");

// Readonly<T> makes every property readonly — can't be modified after creation.
// Like Python's frozen dataclass: @dataclass(frozen=True)

let frozenUser: Readonly<User> = {
    id: 1,
    name: "Chint",
    email: "chint@example.com",
    age: 25,
    role: "user"
};

console.log("frozenUser:", frozenUser);
// frozenUser.name = "Alice";  // ERROR! Cannot assign to 'name' because it is read-only

// Great for config objects that shouldn't change:
function loadConfig(): Readonly<{ apiUrl: string; timeout: number; debug: boolean }> {
    return {
        apiUrl: "https://api.example.com",
        timeout: 5000,
        debug: false
    };
}
let cfg = loadConfig();
console.log("config:", cfg);
// cfg.debug = true;  // ERROR! readonly


// ============================================================================
// 4. Pick<T, K> — Pick specific properties
// ============================================================================

console.log("\n=== Pick<T, K> ===");

// Pick<T, K> creates a new type with ONLY the specified properties.
// K must be keys of T.

// Only want name and email from User:
type UserPreview = Pick<User, "name" | "email">;
// Equivalent to: { name: string; email: string }

let preview: UserPreview = {
    name: "Chint",
    email: "chint@example.com"
};
console.log("preview:", preview);

// Real-world: a login form only needs email and name
type LoginCredentials = Pick<User, "email"> & { password: string };
let creds: LoginCredentials = { email: "chint@example.com", password: "secret123" };
console.log("credentials (email only from User):", creds.email);

// API response that only includes public fields:
type PublicProfile = Pick<User, "name" | "age" | "role">;
function getPublicProfile(user: User): PublicProfile {
    return {
        name: user.name,
        age: user.age,
        role: user.role
    };
}
console.log("public profile:", getPublicProfile(originalUser));


// ============================================================================
// 5. Omit<T, K> — Remove specific properties
// ============================================================================

console.log("\n=== Omit<T, K> ===");

// Omit<T, K> is the OPPOSITE of Pick — it creates a type WITHOUT the specified properties.
// Great for removing sensitive fields.

// User without id (for creating new users before they have an ID):
type NewUser = Omit<User, "id">;

let newUser: NewUser = {
    name: "Alice",
    email: "alice@example.com",
    age: 30,
    role: "user"
};
console.log("newUser (no id):", newUser);

// Remove multiple properties:
type UserMinimal = Omit<User, "id" | "role" | "age">;
let minimal: UserMinimal = { name: "Bob", email: "bob@example.com" };
console.log("minimal:", minimal);

// Real-world: API request body (no id, server generates it)
interface BlogPost {
    id: number;
    title: string;
    content: string;
    authorId: number;
    createdAt: Date;
    updatedAt: Date;
}

type CreateBlogPost = Omit<BlogPost, "id" | "createdAt" | "updatedAt">;
let newPost: CreateBlogPost = {
    title: "Learning TypeScript",
    content: "Utility types are awesome...",
    authorId: 1
};
console.log("newPost (Omit id + timestamps):", newPost);


// ============================================================================
// 6. Record<K, V> — Create object type with specific keys and values
// ============================================================================

console.log("\n=== Record<K, V> ===");

// Record<K, V> creates an object type where:
//   K = the type of the keys
//   V = the type of the values
// Python comparison: Dict[str, int]  ~  Record<string, number>

// Simple: string keys, number values
let scores: Record<string, number> = {
    alice: 95,
    bob: 87,
    chint: 92
};
console.log("scores:", scores);

// With literal type keys — ensures you have ALL keys:
type Day = "mon" | "tue" | "wed" | "thu" | "fri";
let schedule: Record<Day, string> = {
    mon: "Math",
    tue: "Science",
    wed: "English",
    thu: "History",
    fri: "Art"
};
console.log("schedule:", schedule);
// If you forget a day, TypeScript errors!

// With complex value types:
type UserRecord = Record<number, User>;
let usersById: UserRecord = {
    1: { id: 1, name: "Alice", email: "a@a.com", age: 30, role: "admin" },
    2: { id: 2, name: "Bob", email: "b@b.com", age: 28, role: "user" }
};
console.log("usersById[1]:", usersById[1]);

// Real-world: HTTP status codes
let statusMessages: Record<number, string> = {
    200: "OK",
    201: "Created",
    400: "Bad Request",
    404: "Not Found",
    500: "Internal Server Error"
};
console.log("status 404:", statusMessages[404]);


// ============================================================================
// 7. Exclude<T, U> — Remove types from a union
// ============================================================================

console.log("\n=== Exclude<T, U> ===");

// Exclude<T, U> removes types from a UNION that match U.
// Think of it as "T minus U" for union types.

type AllRoles = "admin" | "user" | "guest" | "superadmin";

// Remove "guest" from the roles:
type AuthenticatedRole = Exclude<AllRoles, "guest">;
// Result: "admin" | "user" | "superadmin"

let myRole: AuthenticatedRole = "admin";  // OK
// let badRole: AuthenticatedRole = "guest";  // ERROR! "guest" was excluded

// Remove multiple types:
type BasicRole = Exclude<AllRoles, "admin" | "superadmin">;
// Result: "user" | "guest"

let basicRole: BasicRole = "user";
console.log("myRole:", myRole);
console.log("basicRole:", basicRole);

// Works with any union:
type Primitives = string | number | boolean | null | undefined;
type NonNullPrimitives = Exclude<Primitives, null | undefined>;
// Result: string | number | boolean

let val: NonNullPrimitives = "hello";
console.log("nonNull value:", val);


// ============================================================================
// 8. Extract<T, U> — Keep only matching types from a union
// ============================================================================

console.log("\n=== Extract<T, U> ===");

// Extract<T, U> is the OPPOSITE of Exclude — keeps only types that match U.

type AllTypes = string | number | boolean | null | undefined | object;

// Keep only the string-like types:
type StringTypes = Extract<AllTypes, string>;
// Result: string

// Keep string or number:
type StringOrNumber = Extract<AllTypes, string | number>;
// Result: string | number

let extracted: StringOrNumber = 42;
console.log("extracted:", extracted);
extracted = "hello";
console.log("extracted:", extracted);

// Real-world: extract event types
type EventNames = "click" | "scroll" | "keydown" | "keyup" | "mousemove" | "mousedown";
type KeyboardEvents = Extract<EventNames, "keydown" | "keyup">;
type MouseEvents = Extract<EventNames, "click" | "mousemove" | "mousedown">;

let kbEvent: KeyboardEvents = "keydown";
let mouseEvent: MouseEvents = "click";
console.log("keyboard event:", kbEvent);
console.log("mouse event:", mouseEvent);


// ============================================================================
// 9. ReturnType<T> — Get the return type of a function
// ============================================================================

console.log("\n=== ReturnType<T> ===");

// ReturnType<T> extracts the return type of a function type.
// Super useful when you want the type a function returns but don't have
// a separate type defined for it.

function createUser(name: string, email: string) {
    return {
        id: Math.random(),
        name,
        email,
        createdAt: new Date()
    };
}

// Get the return type WITHOUT defining a separate interface:
type CreatedUser = ReturnType<typeof createUser>;
// Result: { id: number; name: string; email: string; createdAt: Date }

let newlyCreated: CreatedUser = createUser("Chint", "chint@example.com");
console.log("createdUser:", newlyCreated);

// Works with arrow functions too:
const fetchData = async (url: string) => {
    return { data: "mock", status: 200 };
};
type FetchResult = ReturnType<typeof fetchData>;
// Result: Promise<{ data: string; status: number }>
console.log("(ReturnType works with async functions too — gives Promise<...>)");


// ============================================================================
// 10. Parameters<T> — Get the parameter types of a function
// ============================================================================

console.log("\n=== Parameters<T> ===");

// Parameters<T> extracts the parameter types as a tuple.

function sendEmail(to: string, subject: string, body: string, urgent: boolean): void {
    console.log(`  Sending ${urgent ? "URGENT " : ""}email to ${to}: "${subject}"`);
}

// Get the parameter types as a tuple:
type EmailParams = Parameters<typeof sendEmail>;
// Result: [to: string, subject: string, body: string, urgent: boolean]

// Use it to create a wrapper:
function scheduledEmail(...args: EmailParams): void {
    console.log("  (scheduled for later)");
    sendEmail(...args);
}

scheduledEmail("chint@example.com", "Hello", "Learning TS!", false);

// Get a single parameter type:
type FirstParam = Parameters<typeof sendEmail>[0];   // string (the "to" param)
type ThirdParam = Parameters<typeof sendEmail>[2];   // string (the "body" param)
console.log("(FirstParam is string, ThirdParam is string)");


// ============================================================================
// 11. NonNullable<T> — Remove null and undefined
// ============================================================================

console.log("\n=== NonNullable<T> ===");

// NonNullable<T> removes null and undefined from a type.

type MaybeString = string | null | undefined;
type DefiniteString = NonNullable<MaybeString>;
// Result: string

function processValue(value: MaybeString): void {
    if (value != null) {
        // value is now NonNullable<MaybeString> = string
        let definite: DefiniteString = value;
        console.log("  processed:", definite.toUpperCase());
    } else {
        console.log("  value was null/undefined, skipping");
    }
}

processValue("hello");
processValue(null);
processValue(undefined);

// Common pattern: cleaning up arrays with nulls
let messyData: (string | null | undefined)[] = ["hello", null, "world", undefined, "ts"];
let cleanData: NonNullable<typeof messyData[number]>[] = messyData.filter(
    (item): item is string => item != null
);
console.log("messy:", messyData);
console.log("clean:", cleanData);


// ============================================================================
// 12. COMBINING UTILITY TYPES — Real-world patterns
// ============================================================================

console.log("\n=== COMBINING UTILITY TYPES ===");

// The real power comes from COMBINING utility types.

// Pattern 1: Create without ID, update with partial fields
interface Product {
    id: number;
    name: string;
    price: number;
    description: string;
    category: string;
}

type CreateProduct = Omit<Product, "id">;                    // no id when creating
type UpdateProduct = Partial<Omit<Product, "id">> & { id: number }; // id required, rest optional

let createReq: CreateProduct = {
    name: "Widget",
    price: 9.99,
    description: "A useful widget",
    category: "tools"
};
console.log("create request:", createReq);

let updateReq: UpdateProduct = {
    id: 1,
    price: 14.99  // only updating price
};
console.log("update request:", updateReq);

// Pattern 2: Readonly version for display, mutable for editing
type DisplayUser = Readonly<User>;
type EditableUser = Partial<Omit<User, "id">> & Readonly<Pick<User, "id">>;

let display: DisplayUser = {
    id: 1, name: "Chint", email: "chint@example.com", age: 25, role: "user"
};
// display.name = "New";  // ERROR! readonly
console.log("display (readonly):", display);

// Pattern 3: Type-safe configuration builder
type DeepPartial<T> = {
    [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

interface AppConfig {
    server: {
        port: number;
        host: string;
    };
    database: {
        url: string;
        poolSize: number;
    };
}

// Deep partial lets you override just the pieces you need:
let overrides: DeepPartial<AppConfig> = {
    server: { port: 8080 }    // don't need to specify host
};
console.log("config overrides:", overrides);


// ============================================================================
// RECAP
// ============================================================================

console.log("\n=== CHAPTER 7 RECAP ===");
console.log("1.  Partial<T>      — all properties optional");
console.log("2.  Required<T>     — all properties required");
console.log("3.  Readonly<T>     — all properties readonly");
console.log("4.  Pick<T, K>      — keep only specified properties");
console.log("5.  Omit<T, K>      — remove specified properties");
console.log("6.  Record<K, V>    — object with key type K, value type V");
console.log("7.  Exclude<T, U>   — remove types from union");
console.log("8.  Extract<T, U>   — keep matching types from union");
console.log("9.  ReturnType<T>   — get function's return type");
console.log("10. Parameters<T>   — get function's parameter types");
console.log("11. NonNullable<T>  — remove null and undefined");
console.log("12. Combine them for powerful patterns!");
console.log("\nNext up: Chapter 8 — Enums & Advanced Types!");
