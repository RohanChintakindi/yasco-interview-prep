/*
=====================================================
 CHAPTER 9: PRACTICAL PROJECTS
=====================================================

Time to put it all together! This chapter has 4 mini-projects that
combine everything you've learned. Each project is self-contained
and runs with a single command.

PROJECT 1: CLI Todo App (file I/O, arrays, objects)
PROJECT 2: Word Frequency Counter (strings, objects, sorting)
PROJECT 3: Simple HTTP Server (Node.js http module, request/response)
PROJECT 4: API Data Fetcher (async/await, fetch, data processing)

Each project demonstrates real-world JavaScript patterns you'll
encounter in interviews and on the job.

COMING FROM PYTHON:
  Project 1: Like working with Python's open() and json module
  Project 2: Like collections.Counter
  Project 3: Like http.server or Flask
  Project 4: Like using the requests library with asyncio


HOW TO RUN:
  node ch9_practical_projects.js
*/


// =============================================================================
// PROJECT 1: CLI TODO APP
// =============================================================================
//
// A simple in-memory todo list that demonstrates:
//   - Arrays and objects
//   - Array methods (filter, find, map)
//   - File I/O with Node.js fs module
//   - JSON serialization
//
// Python equivalent: Working with a list of dicts and json.dump/json.load

console.log("=".repeat(60));
console.log("PROJECT 1: CLI Todo App");
console.log("=".repeat(60));

const fs = require("fs");       // Node.js file system module (like Python's os/open)
const path = require("path");   // Path handling (like Python's os.path)

class TodoApp {
    constructor(filePath) {
        this.filePath = filePath;
        this.todos = [];
        this.nextId = 1;
    }

    // Add a new todo:
    addTodo(title) {
        const todo = {
            id: this.nextId++,
            title,
            completed: false,
            createdAt: new Date().toISOString(),
        };
        this.todos.push(todo);
        console.log(`  Added: "${title}" (id: ${todo.id})`);
        return todo;
    }

    // Mark as complete:
    completeTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (!todo) {
            console.log(`  Error: Todo #${id} not found`);
            return;
        }
        todo.completed = true;
        console.log(`  Completed: "${todo.title}"`);
    }

    // Remove a todo:
    removeTodo(id) {
        const index = this.todos.findIndex(t => t.id === id);
        if (index === -1) {
            console.log(`  Error: Todo #${id} not found`);
            return;
        }
        const [removed] = this.todos.splice(index, 1);
        console.log(`  Removed: "${removed.title}"`);
    }

    // List all todos:
    listTodos() {
        if (this.todos.length === 0) {
            console.log("  No todos yet!");
            return;
        }
        console.log("  --- Todo List ---");
        for (const todo of this.todos) {
            const status = todo.completed ? "[x]" : "[ ]";
            console.log(`  ${status} #${todo.id}: ${todo.title}`);
        }
        const completed = this.todos.filter(t => t.completed).length;
        console.log(`  --- ${completed}/${this.todos.length} completed ---`);
    }

    // Filter todos:
    getPending() {
        return this.todos.filter(t => !t.completed);
    }

    getCompleted() {
        return this.todos.filter(t => t.completed);
    }

    // Save to file (like Python's json.dump):
    save() {
        try {
            const data = JSON.stringify(this.todos, null, 2);
            // Python: with open(filepath, 'w') as f: json.dump(todos, f)
            // JS:     fs.writeFileSync(filepath, data)
            fs.writeFileSync(this.filePath, data, "utf8");
            console.log(`  Saved ${this.todos.length} todos to ${this.filePath}`);
        } catch (error) {
            console.log(`  Save error: ${error.message}`);
        }
    }

    // Load from file (like Python's json.load):
    load() {
        try {
            if (!fs.existsSync(this.filePath)) {
                console.log("  No save file found, starting fresh");
                return;
            }
            const data = fs.readFileSync(this.filePath, "utf8");
            this.todos = JSON.parse(data);
            this.nextId = Math.max(...this.todos.map(t => t.id), 0) + 1;
            console.log(`  Loaded ${this.todos.length} todos from ${this.filePath}`);
        } catch (error) {
            console.log(`  Load error: ${error.message}`);
        }
    }
}

// Demo the Todo App:
const todoFile = path.join(__dirname, "todos.json");
const app = new TodoApp(todoFile);

app.addTodo("Learn JavaScript basics");
app.addTodo("Practice array methods");
app.addTodo("Build a real project");
app.addTodo("Study async/await");
app.completeTodo(1);
app.completeTodo(2);
app.listTodos();

console.log(`\n  Pending: ${app.getPending().map(t => t.title).join(", ")}`);
console.log(`  Completed: ${app.getCompleted().map(t => t.title).join(", ")}`);

// Save and clean up:
app.save();

// Clean up the file so we don't leave files around:
try { fs.unlinkSync(todoFile); } catch (e) { /* ignore */ }
console.log();


// =============================================================================
// PROJECT 2: WORD FREQUENCY COUNTER
// =============================================================================
//
// Counts word frequencies in text. Demonstrates:
//   - String manipulation
//   - Objects as hashmaps (like Python's dict or Counter)
//   - Array sorting
//   - Method chaining
//
// Python equivalent: collections.Counter(text.split())

console.log("=".repeat(60));
console.log("PROJECT 2: Word Frequency Counter");
console.log("=".repeat(60));

class WordCounter {
    constructor(text) {
        this.originalText = text;
        this.words = this.tokenize(text);
        this.frequencies = this.countFrequencies();
    }

    // Split text into clean words:
    tokenize(text) {
        return text
            .toLowerCase()
            .replace(/[^a-z\s]/g, "")  // Remove non-letter characters (regex)
            .split(/\s+/)               // Split on whitespace
            .filter(word => word.length > 0);  // Remove empty strings
    }

    // Count word frequencies (like Python's Counter):
    countFrequencies() {
        const freq = {};
        for (const word of this.words) {
            // Python: freq[word] = freq.get(word, 0) + 1
            freq[word] = (freq[word] || 0) + 1;
        }
        return freq;
    }

    // Get top N words:
    topWords(n = 10) {
        // Convert object to array of [word, count] pairs, sort, take top N
        // Python: Counter.most_common(n)
        return Object.entries(this.frequencies)
            .sort((a, b) => b[1] - a[1])   // Sort by count, descending
            .slice(0, n);                    // Take first N
    }

    // Get statistics:
    stats() {
        const uniqueWords = Object.keys(this.frequencies).length;
        const totalWords = this.words.length;
        const avgLength = (this.words.reduce((sum, w) => sum + w.length, 0) / totalWords).toFixed(1);
        const longestWord = this.words.reduce((longest, w) => w.length > longest.length ? w : longest, "");

        return { totalWords, uniqueWords, avgLength, longestWord };
    }

    // Display results:
    display() {
        const stats = this.stats();
        console.log(`  Total words:  ${stats.totalWords}`);
        console.log(`  Unique words: ${stats.uniqueWords}`);
        console.log(`  Avg length:   ${stats.avgLength} chars`);
        console.log(`  Longest word: "${stats.longestWord}"`);

        console.log("\n  Top 10 words:");
        const topTen = this.topWords(10);
        const maxCount = topTen[0]?.[1] || 0;

        for (const [word, count] of topTen) {
            const bar = "#".repeat(Math.round((count / maxCount) * 20));
            console.log(`    ${word.padEnd(15)} ${String(count).padStart(3)} ${bar}`);
        }
    }
}

// Demo with sample text:
const sampleText = `
    JavaScript is a programming language that powers the web. JavaScript is used
    by millions of developers worldwide. The language has evolved significantly
    since its creation in 1995. Modern JavaScript includes features like arrow
    functions, destructuring, async await, and classes. JavaScript runs in the
    browser and on the server with Node.js. Learning JavaScript is essential
    for web development. JavaScript frameworks like React, Vue, and Angular
    are built on top of JavaScript. The JavaScript ecosystem is vast and
    constantly growing. Whether you are building a website, a mobile app,
    or a server, JavaScript has the tools you need. JavaScript is truly
    the language of the web.
`;

const counter = new WordCounter(sampleText);
counter.display();
console.log();


// =============================================================================
// PROJECT 3: SIMPLE HTTP SERVER
// =============================================================================
//
// Creates a basic web server using Node.js built-in http module.
// Demonstrates:
//   - Node.js http module
//   - Request/response handling
//   - Routing
//   - JSON responses
//
// Python equivalent: http.server or a basic Flask app
//
// NOTE: The server starts, demonstrates it works by making a request
// to itself, then shuts down so the script can finish.

console.log("=".repeat(60));
console.log("PROJECT 3: Simple HTTP Server");
console.log("=".repeat(60));

const http = require("http");   // Built-in Node.js module (like Python's http.server)

// In-memory data store:
const serverData = {
    todos: [
        { id: 1, title: "Learn Node.js", completed: false },
        { id: 2, title: "Build an API", completed: true },
    ],
    visits: 0,
};

// Create the server:
// Python Flask equivalent:
//   @app.route('/') -> if (url === '/')
//   return jsonify(data) -> res.end(JSON.stringify(data))
const server = http.createServer((req, res) => {
    serverData.visits++;
    const url = req.url;
    const method = req.method;

    // Set JSON response headers:
    res.setHeader("Content-Type", "application/json");

    // --- ROUTING ---
    if (url === "/" && method === "GET") {
        // Home route
        res.statusCode = 200;
        res.end(JSON.stringify({
            message: "Welcome to the Todo API!",
            routes: {
                "GET /":          "This help message",
                "GET /todos":     "List all todos",
                "GET /stats":     "Server statistics",
            },
            visits: serverData.visits,
        }));

    } else if (url === "/todos" && method === "GET") {
        // List todos
        res.statusCode = 200;
        res.end(JSON.stringify({
            count: serverData.todos.length,
            todos: serverData.todos,
        }));

    } else if (url === "/stats" && method === "GET") {
        // Server stats
        res.statusCode = 200;
        res.end(JSON.stringify({
            uptime: process.uptime().toFixed(1) + "s",
            visits: serverData.visits,
            todoCount: serverData.todos.length,
            memoryUsage: Math.round(process.memoryUsage().heapUsed / 1024 / 1024) + "MB",
        }));

    } else {
        // 404 Not Found
        res.statusCode = 404;
        res.end(JSON.stringify({ error: "Route not found", url }));
    }
});

// Start server, test it, then shut down:
const PORT = 0;  // Port 0 = let OS pick an available port
server.listen(PORT, async () => {
    const actualPort = server.address().port;
    console.log(`  Server running on http://localhost:${actualPort}`);

    // Make a test request to our own server:
    try {
        const response = await fetch(`http://localhost:${actualPort}/`);
        const data = await response.json();
        console.log("  Response from /:", JSON.stringify(data, null, 2).split("\n").map(l => "    " + l).join("\n"));

        const todosResponse = await fetch(`http://localhost:${actualPort}/todos`);
        const todosData = await todosResponse.json();
        console.log(`  Response from /todos: ${todosData.count} todos found`);

        const statsResponse = await fetch(`http://localhost:${actualPort}/stats`);
        const statsData = await statsResponse.json();
        console.log(`  Response from /stats: ${statsData.visits} visits, ${statsData.memoryUsage} memory`);
    } catch (error) {
        console.log(`  Test request failed: ${error.message}`);
    }

    // Shut down the server so the script can exit:
    server.close(() => {
        console.log("  Server shut down.\n");
        runProject4();  // Chain to next project after server closes
    });
});

// =============================================================================
// PROJECT 4: API DATA FETCHER
// =============================================================================
//
// Fetches data from a public API and processes it. Demonstrates:
//   - async/await
//   - fetch()
//   - Error handling
//   - Data transformation with map/filter/reduce
//   - Promise.all for parallel requests
//
// Python equivalent: Using requests + json to fetch and process API data

async function runProject4() {
    console.log("=".repeat(60));
    console.log("PROJECT 4: API Data Fetcher");
    console.log("=".repeat(60));

    const BASE_URL = "https://jsonplaceholder.typicode.com";

    // --- Helper: fetch with error handling ---
    async function fetchJSON(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`  Fetch failed for ${url}: ${error.message}`);
            return null;
        }
    }

    // --- Task 1: Fetch users and their posts in parallel ---
    console.log("\n  Task 1: Fetch users and posts in parallel...");
    try {
        const [users, posts] = await Promise.all([
            fetchJSON(`${BASE_URL}/users`),
            fetchJSON(`${BASE_URL}/posts`),
        ]);

        if (!users || !posts) {
            console.log("  Failed to fetch data.");
            return;
        }

        console.log(`  Fetched ${users.length} users and ${posts.length} posts`);

        // --- Task 2: Find top posters ---
        console.log("\n  Task 2: Top posters (most posts):");

        // Count posts per user (like Python's Counter):
        const postCounts = posts.reduce((counts, post) => {
            counts[post.userId] = (counts[post.userId] || 0) + 1;
            return counts;
        }, {});

        // Join with user names and sort:
        const topPosters = Object.entries(postCounts)
            .map(([userId, count]) => {
                const user = users.find(u => u.id === Number(userId));
                return { name: user?.name || "Unknown", count };
            })
            .sort((a, b) => b.count - a.count)
            .slice(0, 5);

        for (const poster of topPosters) {
            console.log(`    ${poster.name}: ${poster.count} posts`);
        }

        // --- Task 3: Fetch todos and analyze completion rates ---
        console.log("\n  Task 3: Todo completion rates by user...");
        const todos = await fetchJSON(`${BASE_URL}/todos`);

        if (todos) {
            // Group by user and calculate completion rate:
            const userStats = {};
            for (const todo of todos) {
                if (!userStats[todo.userId]) {
                    userStats[todo.userId] = { total: 0, completed: 0 };
                }
                userStats[todo.userId].total++;
                if (todo.completed) userStats[todo.userId].completed++;
            }

            // Display results:
            const completion = Object.entries(userStats)
                .map(([userId, stats]) => {
                    const user = users.find(u => u.id === Number(userId));
                    const rate = ((stats.completed / stats.total) * 100).toFixed(0);
                    return { name: user?.name || "Unknown", ...stats, rate: Number(rate) };
                })
                .sort((a, b) => b.rate - a.rate);

            console.log("    User                   Done/Total  Rate");
            console.log("    " + "-".repeat(50));
            for (const stat of completion) {
                const bar = "#".repeat(Math.round(stat.rate / 5));
                console.log(
                    `    ${stat.name.padEnd(25)} ${String(stat.completed).padStart(2)}/${stat.total}     ${String(stat.rate).padStart(3)}% ${bar}`
                );
            }
        }

        // --- Task 4: Search posts by keyword ---
        console.log("\n  Task 4: Search posts for 'aut' keyword...");
        const keyword = "aut";
        const matchingPosts = posts
            .filter(p => p.title.toLowerCase().includes(keyword))
            .slice(0, 5);

        console.log(`  Found ${posts.filter(p => p.title.toLowerCase().includes(keyword)).length} posts matching "${keyword}" (showing 5):`);
        for (const post of matchingPosts) {
            const author = users.find(u => u.id === post.userId);
            console.log(`    [${author?.name}] ${post.title}`);
        }

    } catch (error) {
        console.error(`  Project 4 error: ${error.message}`);
    }

    console.log();
    console.log("=".repeat(60));
    console.log("All projects complete! You've seen JavaScript in action.");
    console.log("=".repeat(60));
}


// =============================================================================
// QUICK REFERENCE
// =============================================================================
//
// FILE I/O (Node.js fs module):
//   const fs = require('fs');
//   fs.readFileSync('file.txt', 'utf8')     // Python: open('file').read()
//   fs.writeFileSync('file.txt', data)      // Python: open('file', 'w').write(data)
//   fs.existsSync('file.txt')               // Python: os.path.exists('file')
//
// HTTP SERVER (Node.js http module):
//   const server = http.createServer((req, res) => { ... });
//   server.listen(port);
//   req.url, req.method                     // Like Flask's request.path, request.method
//   res.statusCode = 200;
//   res.setHeader('Content-Type', 'application/json');
//   res.end(JSON.stringify(data));           // Like Flask's jsonify(data)
//
// FETCH (built-in in Node 18+):
//   const response = await fetch(url);
//   const data = await response.json();     // Like requests.get(url).json()
//
// JSON:
//   JSON.stringify(obj)                      // Python: json.dumps(obj)
//   JSON.stringify(obj, null, 2)             // Pretty print with 2-space indent
//   JSON.parse(str)                          // Python: json.loads(str)
//
// PYTHON -> JS:
//   collections.Counter   -> reduce to object + Object.entries
//   sorted(list, key=)    -> list.sort((a, b) => ...)
//   open('f').read()       -> fs.readFileSync('f', 'utf8')
//   http.server            -> http.createServer
//   requests.get(url)      -> await fetch(url)
//   json.dumps/loads       -> JSON.stringify/parse
//
// =============================================================================
