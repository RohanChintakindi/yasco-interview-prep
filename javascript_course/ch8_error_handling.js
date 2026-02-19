/*
=====================================================
 CHAPTER 8: ERROR HANDLING & DEBUGGING
=====================================================

Errors are inevitable. Good code doesn't avoid errors - it HANDLES them
gracefully. JavaScript's error handling is very similar to Python's
try/except/finally system.

COMING FROM PYTHON:
  Python: try / except / finally / raise
  JS:     try / catch  / finally / throw

  Python: except ValueError as e:
  JS:     catch (error) { ... }   (JS catches ALL errors in one catch)

KEY DIFFERENCE: Python lets you catch specific error types:
    except ValueError:  ...
    except TypeError:   ...
  JS catches everything in one catch block, then you check the type manually.


HOW TO RUN:
  node ch8_error_handling.js
*/

// =============================================================================
// PART 1: TRY / CATCH / FINALLY
// =============================================================================
//
// try:     Code that might throw an error
// catch:   Handle the error if one occurs
// finally: Always runs, whether error happened or not

console.log("=".repeat(50));
console.log("PART 1: try / catch / finally");
console.log("=".repeat(50));

// Basic try/catch:
try {
    console.log("  Before error");
    const result = JSON.parse("not valid json");  // This will throw!
    console.log("  After error (never runs)");
} catch (error) {
    console.log(`  Caught: ${error.message}`);
    console.log(`  Error type: ${error.constructor.name}`);
}

// With finally:
console.log("\nWith finally:");
try {
    const data = JSON.parse('{"name": "Chint"}');
    console.log(`  Parsed: ${data.name}`);
} catch (error) {
    console.log(`  Error: ${error.message}`);
} finally {
    console.log("  Finally: this ALWAYS runs (cleanup goes here)");
}

// try/catch without catch (just try/finally):
console.log("\ntry/finally (no catch):");
function riskyOperation() {
    try {
        return "success";
    } finally {
        console.log("  Finally runs even with return!");
    }
}
console.log(`  Result: ${riskyOperation()}`);
console.log();


// =============================================================================
// PART 2: THROW - CREATING ERRORS
// =============================================================================
//
// Python: raise ValueError("bad value")
// JS:     throw new Error("bad value")
//
// You can throw anything in JS (strings, numbers, objects), but you
// SHOULD always throw Error objects because they include a stack trace.

console.log("=".repeat(50));
console.log("PART 2: throw (like Python's raise)");
console.log("=".repeat(50));

function divide(a, b) {
    if (typeof a !== "number" || typeof b !== "number") {
        throw new TypeError("Both arguments must be numbers");
    }
    if (b === 0) {
        throw new RangeError("Cannot divide by zero");
    }
    return a / b;
}

// Test with valid input:
console.log(`divide(10, 3) = ${divide(10, 3)}`);

// Test with invalid input:
try {
    divide(10, 0);
} catch (error) {
    console.log(`Caught: ${error.constructor.name}: ${error.message}`);
}

try {
    divide("hello", 5);
} catch (error) {
    console.log(`Caught: ${error.constructor.name}: ${error.message}`);
}

// Re-throwing (catch, inspect, and throw again if you can't handle it):
function processData(data) {
    try {
        return JSON.parse(data);
    } catch (error) {
        if (error instanceof SyntaxError) {
            console.log("  Bad JSON, returning default");
            return {};  // Handle SyntaxError
        }
        throw error;  // Re-throw anything else
    }
}

console.log("processData result:", processData("not json"));
console.log();


// =============================================================================
// PART 3: ERROR TYPES
// =============================================================================
//
// JavaScript has several built-in error types. In Python you have
// ValueError, TypeError, etc. JS has a similar set.

console.log("=".repeat(50));
console.log("PART 3: Error Types");
console.log("=".repeat(50));

// The built-in error hierarchy:
// Error (base class, like Python's Exception)
//   ├── TypeError       -> Wrong type (like Python's TypeError)
//   ├── ReferenceError  -> Variable doesn't exist (like Python's NameError)
//   ├── SyntaxError     -> Invalid syntax (like Python's SyntaxError)
//   ├── RangeError      -> Value out of range (like Python's ValueError sometimes)
//   ├── URIError        -> Bad URI functions
//   └── EvalError       -> eval() errors (rare)

const errorExamples = [
    { code: '(null).prop', desc: "TypeError: Cannot read property of null" },
    { code: 'JSON.parse("{")', desc: "SyntaxError: Bad JSON" },
    { code: 'new Array(-1)', desc: "RangeError: Invalid array length" },
];

console.log("Common error types:");
for (const example of errorExamples) {
    try {
        eval(example.code);  // eval is bad in real code, just for demo
    } catch (error) {
        console.log(`  ${error.constructor.name}: ${error.message}`);
    }
}

// Checking error type (since JS has only one catch block):
// Python: except TypeError: ...
// JS:     catch (e) { if (e instanceof TypeError) ... }
console.log("\nType checking in catch:");
try {
    undefined.toString();
} catch (error) {
    if (error instanceof TypeError) {
        console.log("  It's a TypeError!");
    } else if (error instanceof ReferenceError) {
        console.log("  It's a ReferenceError!");
    } else {
        console.log("  Some other error");
    }
}
console.log();


// =============================================================================
// PART 4: CUSTOM ERROR CLASSES
// =============================================================================
//
// Python: class ValidationError(Exception): ...
// JS:     class ValidationError extends Error { ... }

console.log("=".repeat(50));
console.log("PART 4: Custom Error Classes");
console.log("=".repeat(50));

class ValidationError extends Error {
    constructor(field, message) {
        super(message);                // Call parent constructor
        this.name = "ValidationError"; // Override the name (default is "Error")
        this.field = field;            // Custom property
    }
}

class NotFoundError extends Error {
    constructor(resource, id) {
        super(`${resource} with id ${id} not found`);
        this.name = "NotFoundError";
        this.resource = resource;
        this.id = id;
        this.statusCode = 404;
    }
}

// Using custom errors:
function validateUser(user) {
    if (!user.name || user.name.trim() === "") {
        throw new ValidationError("name", "Name is required");
    }
    if (!user.email || !user.email.includes("@")) {
        throw new ValidationError("email", "Valid email is required");
    }
    if (user.age < 0 || user.age > 150) {
        throw new ValidationError("age", "Age must be between 0 and 150");
    }
    return true;
}

// Test validation:
const testUsers = [
    { name: "", email: "test@example.com", age: 25 },
    { name: "Chint", email: "not-an-email", age: 25 },
    { name: "Chint", email: "chint@example.com", age: 25 },
    { name: "Chint", email: "chint@example.com", age: -5 },
];

for (const user of testUsers) {
    try {
        validateUser(user);
        console.log(`  Valid: ${user.name} (${user.email})`);
    } catch (error) {
        if (error instanceof ValidationError) {
            console.log(`  Invalid [${error.field}]: ${error.message}`);
        } else {
            throw error;  // Re-throw unexpected errors
        }
    }
}

// NotFoundError example:
function findUser(id) {
    const users = { 1: "Alice", 2: "Bob" };
    if (!users[id]) {
        throw new NotFoundError("User", id);
    }
    return users[id];
}

try {
    console.log(`\n  Found: ${findUser(1)}`);
    console.log(`  Found: ${findUser(99)}`);
} catch (error) {
    if (error instanceof NotFoundError) {
        console.log(`  ${error.name} (${error.statusCode}): ${error.message}`);
    }
}
console.log();


// =============================================================================
// PART 5: ASYNC ERROR HANDLING
// =============================================================================
//
// In async code, errors can happen in Promises. You handle them with
// try/catch in async functions, or .catch() on Promise chains.

console.log("=".repeat(50));
console.log("PART 5: Async Error Handling");
console.log("=".repeat(50));

// --- async/await: use try/catch (recommended) ---
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        // Catches both network errors AND our thrown errors
        console.log(`  Fetch error: ${error.message}`);
        return null;  // Return a safe default
    }
}

// This will succeed:
fetchData("https://jsonplaceholder.typicode.com/todos/1")
    .then(data => {
        if (data) console.log(`  Fetched: ${data.title}`);
    });

// This will fail gracefully:
fetchData("https://jsonplaceholder.typicode.com/invalid-endpoint-12345")
    .then(data => {
        console.log(`  Result: ${data === null ? "null (handled gracefully)" : data}`);
    });

// --- Promise .catch() ---
function riskyPromise() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            reject(new Error("Something went wrong in the promise"));
        }, 50);
    });
}

riskyPromise()
    .then(result => console.log(result))
    .catch(error => console.log(`  Promise .catch(): ${error.message}`));

// IMPORTANT: Unhandled Promise rejections crash Node.js!
// Always add .catch() or wrap in try/catch.
console.log();


// =============================================================================
// PART 6: COMMON PATTERNS
// =============================================================================

console.log("=".repeat(50));
console.log("PART 6: Common Error Handling Patterns");
console.log("=".repeat(50));

// Pattern 1: Default values with try/catch
function safeJSONParse(str, fallback = null) {
    try {
        return JSON.parse(str);
    } catch {
        return fallback;  // catch without (error) - we don't need the error object
    }
}
console.log('safeJSONParse valid:', safeJSONParse('{"a":1}'));
console.log('safeJSONParse invalid:', safeJSONParse('bad', {}));

// Pattern 2: Validation with early returns
function processAge(age) {
    if (age === undefined || age === null) return "Age not provided";
    if (typeof age !== "number") return "Age must be a number";
    if (age < 0 || age > 150) return "Age out of range";
    if (!Number.isInteger(age)) return "Age must be a whole number";
    return `Valid age: ${age}`;
}

console.log(`\n${processAge(25)}`);
console.log(processAge("twenty"));
console.log(processAge(-5));
console.log(processAge(25.5));
console.log(processAge(null));

// Pattern 3: Defensive programming with optional chaining
const apiResponse = {
    data: {
        users: [
            { name: "Alice", address: { city: "NYC" } },
            { name: "Bob" },  // No address!
        ],
    },
};

// Without defensive coding: apiResponse.data.users[1].address.city -> CRASH!
// With optional chaining: safe
for (const user of apiResponse.data.users) {
    console.log(`  ${user.name}: ${user.address?.city ?? "no city"}`);
}
console.log();


// =============================================================================
// PART 7: DEBUGGING TOOLS
// =============================================================================

console.log("=".repeat(50));
console.log("PART 7: Debugging Tools");
console.log("=".repeat(50));

// console.log - the classic (like Python's print)
console.log("console.log: basic output");

// console.error - prints to stderr (red in browser/some terminals)
console.error("console.error: error messages (goes to stderr)");

// console.warn - warning messages (yellow in browsers)
console.warn("console.warn: warning messages");

// console.table - display objects/arrays as a table (great for debugging!)
const users = [
    { name: "Alice", age: 30, role: "admin" },
    { name: "Bob", age: 25, role: "user" },
    { name: "Charlie", age: 35, role: "user" },
];
console.log("\nconsole.table:");
console.table(users);

// console.time / console.timeEnd - measure execution time
// Python: import time; start = time.time() ... time.time() - start
console.time("loop-timer");
let sum = 0;
for (let i = 0; i < 1000000; i++) {
    sum += i;
}
console.timeEnd("loop-timer");  // Prints: loop-timer: Xms

// console.group / console.groupEnd - group related logs
console.group("User Details");
console.log("Name: Chint");
console.log("Age: 25");
console.log("City: NYC");
console.groupEnd();

// console.assert - only logs if condition is FALSE
console.assert(1 === 1, "This won't print (condition is true)");
console.assert(1 === 2, "This WILL print (condition is false)");

// console.count - count how many times something happens
for (let i = 0; i < 3; i++) {
    console.count("loop iteration");
}

// debugger keyword (for browser DevTools):
// When the browser encounters "debugger;", it pauses execution
// and opens DevTools, like a breakpoint.
// debugger;  // Uncomment to test in browser DevTools

console.log("\n--- Stack trace ---");
// console.trace() - print the call stack (like Python's traceback):
function innerFunction() {
    console.trace("Where am I?");
}
function outerFunction() {
    innerFunction();
}
outerFunction();
console.log();


// =============================================================================
// PART 8: PRACTICAL EXAMPLES
// =============================================================================

console.log("=".repeat(50));
console.log("PART 8: Practical Examples");
console.log("=".repeat(50));

// A robust config loader:
function loadConfig(configString) {
    let config;

    // Step 1: Parse
    try {
        config = JSON.parse(configString);
    } catch (error) {
        throw new Error(`Invalid config format: ${error.message}`);
    }

    // Step 2: Validate required fields
    const required = ["host", "port"];
    for (const field of required) {
        if (!(field in config)) {
            throw new ValidationError(field, `Missing required config: ${field}`);
        }
    }

    // Step 3: Validate types
    if (typeof config.port !== "number") {
        throw new ValidationError("port", "Port must be a number");
    }

    // Step 4: Apply defaults
    return {
        host: config.host,
        port: config.port,
        debug: config.debug ?? false,
        timeout: config.timeout ?? 5000,
    };
}

// Test the config loader:
const testConfigs = [
    '{"host": "localhost", "port": 3000}',
    '{"host": "localhost", "port": 3000, "debug": true}',
    '{"host": "localhost"}',
    'not json at all',
    '{"host": "localhost", "port": "not a number"}',
];

for (const configStr of testConfigs) {
    try {
        const config = loadConfig(configStr);
        console.log(`  Valid config:`, config);
    } catch (error) {
        console.log(`  Error: [${error.constructor.name}] ${error.message}`);
    }
}
console.log();


// =============================================================================
// QUICK REFERENCE
// =============================================================================
//
// TRY/CATCH:
//   try {
//       riskyCode();
//   } catch (error) {
//       console.error(error.message);
//   } finally {
//       cleanup();
//   }
//
// THROW:
//   throw new Error("message")
//   throw new TypeError("message")
//
// ERROR TYPES:
//   Error, TypeError, ReferenceError, SyntaxError, RangeError
//
// CUSTOM ERRORS:
//   class MyError extends Error {
//       constructor(msg) { super(msg); this.name = "MyError"; }
//   }
//
// CHECK TYPE:
//   error instanceof TypeError
//
// ASYNC:
//   async/await -> try/catch
//   .then()     -> .catch()
//
// DEBUGGING:
//   console.log, .error, .warn, .table, .time/.timeEnd
//   console.trace(), console.assert(), console.count()
//   debugger;  (breakpoint in browser)
//
// PYTHON -> JS:
//   try/except/finally  -> try/catch/finally
//   raise               -> throw
//   except TypeError:   -> catch (e) { if (e instanceof TypeError) }
//   class E(Exception): -> class E extends Error { }
//   traceback.print_exc -> console.trace()
//
// =============================================================================
