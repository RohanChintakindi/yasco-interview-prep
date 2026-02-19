/*
=====================================================
 CHAPTER 6: ASYNCHRONOUS JAVASCRIPT
=====================================================

This is one of the MOST IMPORTANT chapters. Async is where JavaScript
fundamentally differs from Python.

PYTHON: Runs code line by line (synchronous). Line 2 waits for Line 1.
JS:     Runs code asynchronously. If Line 1 takes time (API call, file read),
        JS doesn't wait - it moves to Line 2 and comes back to Line 1 later.

WHY?
  JavaScript was built for the browser. You can't freeze the entire webpage
  while waiting for an image to load or an API to respond. So JS uses a
  "non-blocking" model: start the task, move on, handle the result later.

ANALOGY:
  Python (sync):  You order food, stand at the counter waiting, get food, sit down.
  JS (async):     You order food, get a buzzer, sit down, buzzer goes off, pick up food.

The "buzzer" in JS is called a PROMISE.

THREE ERAS OF ASYNC JS:
  1. Callbacks (the old way) - 2000s
  2. Promises (.then/.catch)  - 2015 (ES6)
  3. async/await              - 2017 (ES8) - the modern, clean way


HOW TO RUN:
  node ch6_async_javascript.js
*/

// =============================================================================
// PART 1: WHY ASYNC MATTERS - THE EVENT LOOP
// =============================================================================

console.log("=".repeat(50));
console.log("PART 1: Synchronous vs Asynchronous");
console.log("=".repeat(50));

// JavaScript is SINGLE-THREADED. It has ONE call stack.
// But it handles async operations using the EVENT LOOP.
//
// The event loop works like this:
//   1. Run synchronous code (the "main thread")
//   2. When you start an async task (timer, API call), it goes to the "task queue"
//   3. When the main thread is done, check the task queue for completed tasks
//   4. Run callbacks from completed tasks
//
// This means: ALL synchronous code runs BEFORE any async callbacks!

console.log("1. First (sync)");

setTimeout(() => {
    console.log("3. Third (async - ran after all sync code!)");
}, 0);  // Even with 0ms delay, it goes to the task queue!

console.log("2. Second (sync)");

// Output order: 1, 2, 3  (NOT 1, 3, 2!)
// The setTimeout callback waits for ALL synchronous code to finish.
console.log();


// =============================================================================
// PART 2: CALLBACKS (The Old Way)
// =============================================================================
//
// A callback is a function you pass to an async operation.
// When the operation finishes, it "calls back" your function.

console.log("=".repeat(50));
console.log("PART 2: Callbacks");
console.log("=".repeat(50));

// Simple callback example with setTimeout:
function fetchUserData(userId, callback) {
    // Simulate an API call that takes 100ms
    setTimeout(() => {
        const user = { id: userId, name: "Chint", email: "chint@example.com" };
        callback(user);  // "Call back" with the result
    }, 100);
}

console.log("Fetching user data...");
fetchUserData(1, (user) => {
    console.log("  Got user:", user.name);
});

// --- CALLBACK HELL (the problem with callbacks) ---
// When you need to do async operations in sequence, callbacks nest inside
// each other, creating an unreadable pyramid of doom:
//
//   getUser(id, (user) => {
//       getOrders(user.id, (orders) => {
//           getOrderDetails(orders[0].id, (details) => {
//               getShippingInfo(details.trackingId, (shipping) => {
//                   console.log(shipping);
//                   // This is 4 levels deep. Real code can be 10+ levels!
//               });
//           });
//       });
//   });
//
// This is called "callback hell" or "pyramid of doom."
// Promises (and then async/await) were invented to fix this.

console.log("  (Callback hell is why Promises were invented)");
console.log();


// =============================================================================
// PART 3: PROMISES
// =============================================================================
//
// A Promise is an object that represents a future value.
// It's the "buzzer" from our restaurant analogy.
//
// A Promise has three states:
//   PENDING    -> Operation in progress (buzzer hasn't gone off)
//   FULFILLED  -> Operation succeeded (buzzer went off, food ready!)
//   REJECTED   -> Operation failed (kitchen ran out of ingredients)
//
// Python analogy: Promises are like asyncio.Future or concurrent.futures.Future

console.log("=".repeat(50));
console.log("PART 3: Promises");
console.log("=".repeat(50));

// Creating a Promise:
function fetchUser(userId) {
    return new Promise((resolve, reject) => {
        // resolve = call this when successful
        // reject = call this when failed
        setTimeout(() => {
            if (userId > 0) {
                resolve({ id: userId, name: "Chint" });  // Success!
            } else {
                reject(new Error("Invalid user ID"));     // Failure!
            }
        }, 100);
    });
}

// Consuming a Promise with .then() and .catch():
console.log("Using .then/.catch:");
fetchUser(1)
    .then((user) => {
        console.log(`  Success: ${user.name}`);
        return user.name.toUpperCase();  // You can return values to chain
    })
    .then((upperName) => {
        console.log(`  Chained: ${upperName}`);
    })
    .catch((error) => {
        console.log(`  Error: ${error.message}`);
    })
    .finally(() => {
        console.log("  Finally: runs whether it succeeded or failed");
    });

// Error handling:
fetchUser(-1)
    .then((user) => console.log(`  Got: ${user.name}`))
    .catch((error) => console.log(`  Caught error: ${error.message}`));

// Promise chaining solves callback hell:
// Instead of nesting, you CHAIN with .then():
//   getUser(id)
//       .then(user => getOrders(user.id))
//       .then(orders => getOrderDetails(orders[0].id))
//       .then(details => getShippingInfo(details.trackingId))
//       .then(shipping => console.log(shipping))
//       .catch(error => console.log("Something failed:", error));
//
// Much flatter and more readable!
console.log();


// =============================================================================
// PART 4: ASYNC/AWAIT - THE MODERN WAY
// =============================================================================
//
// async/await is syntactic sugar over Promises. It makes async code
// LOOK synchronous, which is much easier to read.
//
// Python has async/await too! The concept is similar, but in JS it's
// used WAY more often because almost all I/O is async in JS.
//
// RULES:
//   1. Mark a function as "async" to use await inside it
//   2. "await" pauses until the Promise resolves
//   3. An async function ALWAYS returns a Promise

console.log("=".repeat(50));
console.log("PART 4: async/await");
console.log("=".repeat(50));

// Using async/await (MUCH cleaner than .then chains):
async function getUserInfo(userId) {
    try {
        const user = await fetchUser(userId);  // Waits for the Promise to resolve
        console.log(`  async/await: Got ${user.name}`);
        return user;
    } catch (error) {
        console.log(`  async/await error: ${error.message}`);
    }
}

// Call the async function:
console.log("Calling async function:");
getUserInfo(1);
getUserInfo(-1);

// COMPARE - the same logic three ways:
//
// CALLBACKS (old, messy):
//   fetchUserCB(1, (user) => {
//       fetchOrdersCB(user.id, (orders) => {
//           console.log(orders);
//       });
//   });
//
// PROMISES (.then, better):
//   fetchUser(1)
//       .then(user => fetchOrders(user.id))
//       .then(orders => console.log(orders));
//
// ASYNC/AWAIT (best, reads like synchronous code!):
//   const user = await fetchUser(1);
//   const orders = await fetchOrders(user.id);
//   console.log(orders);
console.log();


// =============================================================================
// PART 5: FETCH - MAKING HTTP REQUESTS
// =============================================================================
//
// fetch() is the built-in way to make HTTP requests in JavaScript.
// Python: requests.get("url")
// JS:     await fetch("url")
//
// fetch() returns a Promise, so you use it with async/await.
// Note: fetch is built into Node.js 18+ and all modern browsers.

console.log("=".repeat(50));
console.log("PART 5: fetch() - HTTP Requests");
console.log("=".repeat(50));

async function fetchTodo() {
    try {
        // fetch() returns a Response object
        const response = await fetch("https://jsonplaceholder.typicode.com/todos/1");

        // Check if the request was successful:
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON body (also returns a Promise!):
        // Python: response.json()  (synchronous in requests)
        // JS:     await response.json()  (async!)
        const data = await response.json();

        console.log("  Fetched todo:");
        console.log(`    ID:        ${data.id}`);
        console.log(`    Title:     ${data.title}`);
        console.log(`    Completed: ${data.completed}`);
    } catch (error) {
        console.log(`  Fetch error: ${error.message}`);
    }
}

// Call it (we'll wait for it):
fetchTodo();

// POST request example:
async function createTodo(title) {
    try {
        const response = await fetch("https://jsonplaceholder.typicode.com/todos", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({  // Must stringify the body!
                title: title,
                completed: false,
                userId: 1,
            }),
        });

        const newTodo = await response.json();
        console.log(`  Created todo: id=${newTodo.id}, title="${newTodo.title}"`);
    } catch (error) {
        console.log(`  Create error: ${error.message}`);
    }
}

createTodo("Learn JavaScript async");
console.log();


// =============================================================================
// PART 6: PROMISE.ALL - PARALLEL ASYNC OPERATIONS
// =============================================================================
//
// If you have multiple independent async operations, don't await them
// one by one (that's slow). Use Promise.all() to run them in parallel!
//
// Python: asyncio.gather(task1, task2, task3)
// JS:     Promise.all([task1, task2, task3])

console.log("=".repeat(50));
console.log("PART 6: Promise.all()");
console.log("=".repeat(50));

async function fetchMultipleTodos() {
    try {
        // BAD: Sequential (slow - each waits for the previous):
        // const todo1 = await fetch(url1); // waits...
        // const todo2 = await fetch(url2); // then waits...
        // const todo3 = await fetch(url3); // then waits...

        // GOOD: Parallel (fast - all start at the same time!):
        const urls = [
            "https://jsonplaceholder.typicode.com/todos/1",
            "https://jsonplaceholder.typicode.com/todos/2",
            "https://jsonplaceholder.typicode.com/todos/3",
        ];

        const promises = urls.map(url => fetch(url).then(r => r.json()));
        const results = await Promise.all(promises);

        console.log("  Fetched 3 todos in parallel:");
        for (const todo of results) {
            console.log(`    ${todo.id}: ${todo.title}`);
        }
    } catch (error) {
        // If ANY Promise rejects, Promise.all rejects immediately
        console.log(`  Error: ${error.message}`);
    }
}

fetchMultipleTodos();

// Promise.allSettled: like Promise.all but doesn't fail if one rejects
// Returns the status of each Promise (fulfilled or rejected)
async function fetchWithSettled() {
    const promises = [
        fetchUser(1),            // Will succeed
        fetchUser(-1),           // Will fail
        fetchUser(2),            // Will succeed
    ];

    const results = await Promise.allSettled(promises);
    console.log("\n  Promise.allSettled results:");
    for (const result of results) {
        if (result.status === "fulfilled") {
            console.log(`    Fulfilled: ${result.value.name}`);
        } else {
            console.log(`    Rejected: ${result.reason.message}`);
        }
    }
}

fetchWithSettled();

// Other Promise combinators:
// Promise.race()   -> resolves/rejects with the FIRST completed Promise
// Promise.any()    -> resolves with the FIRST SUCCESSFUL Promise
console.log();


// =============================================================================
// PART 7: ERROR HANDLING IN ASYNC CODE
// =============================================================================

console.log("=".repeat(50));
console.log("PART 7: Async Error Handling");
console.log("=".repeat(50));

// --- With async/await: use try/catch (just like Python!) ---
async function safeAsyncOperation() {
    try {
        const user = await fetchUser(-1);  // This will reject
        console.log(user);  // Never reaches here
    } catch (error) {
        // Catches both Promise rejections and regular errors
        console.log(`  Caught: ${error.message}`);
    } finally {
        // Always runs (like Python's finally)
        console.log("  Finally block: cleanup code goes here");
    }
}

safeAsyncOperation();

// --- With .then/.catch: chain .catch() ---
// fetchUser(-1)
//     .then(user => console.log(user))
//     .catch(error => console.log(`Caught: ${error.message}`));

// --- Common pattern: wrapper function for async error handling ---
async function tryCatch(promise) {
    try {
        const data = await promise;
        return [data, null];       // [data, no error]
    } catch (error) {
        return [null, error];      // [no data, error]
    }
}

// Usage (Go-style error handling):
async function demo() {
    const [user, error] = await tryCatch(fetchUser(1));
    if (error) {
        console.log(`  Error: ${error.message}`);
        return;
    }
    console.log(`  User: ${user.name}`);
}

// Wait a bit for previous async operations to complete, then run demo
setTimeout(() => {
    console.log("\n  Go-style error handling:");
    demo();
}, 500);
console.log();


// =============================================================================
// PART 8: REAL-WORLD ASYNC PATTERN
// =============================================================================

console.log("=".repeat(50));
console.log("PART 8: Real-World Pattern");
console.log("=".repeat(50));

// A realistic async function that fetches and processes data:
async function getTopUsers() {
    try {
        console.log("  Fetching users...");
        const response = await fetch("https://jsonplaceholder.typicode.com/users");

        if (!response.ok) {
            throw new Error(`Failed to fetch: ${response.status}`);
        }

        const users = await response.json();

        // Process the data (synchronous operations after await):
        const userSummaries = users
            .slice(0, 5)  // Take first 5
            .map(u => ({
                name: u.name,
                email: u.email,
                city: u.address.city,
            }));

        console.log("  Top 5 users:");
        for (const user of userSummaries) {
            console.log(`    ${user.name} (${user.email}) - ${user.city}`);
        }

        return userSummaries;
    } catch (error) {
        console.error(`  Failed to get users: ${error.message}`);
        return [];  // Return empty array on failure
    }
}

getTopUsers();


// =============================================================================
// QUICK REFERENCE
// =============================================================================
//
// CALLBACKS:
//   doSomething(data, (result) => { ... })
//   Problem: callback hell (nested callbacks)
//
// PROMISES:
//   const promise = new Promise((resolve, reject) => { ... })
//   promise.then(result => ...).catch(error => ...).finally(() => ...)
//
// ASYNC/AWAIT:
//   async function fn() {
//       try {
//           const result = await somePromise;
//       } catch (error) {
//           console.error(error);
//       }
//   }
//
// FETCH:
//   const response = await fetch(url);
//   const data = await response.json();
//
// PROMISE COMBINATORS:
//   Promise.all([p1, p2, p3])         -> Wait for ALL (fail if any fails)
//   Promise.allSettled([p1, p2, p3])   -> Wait for ALL (never fails)
//   Promise.race([p1, p2, p3])        -> First to complete (pass or fail)
//   Promise.any([p1, p2, p3])         -> First to SUCCEED
//
// PYTHON -> JS:
//   requests.get(url)       -> await fetch(url)
//   response.json()         -> await response.json()  (async in JS!)
//   asyncio.gather()        -> Promise.all()
//   try/except              -> try/catch
//   async def / await       -> async function / await
//
// =============================================================================
