/*
 * ============================================================================
 *  TYPESCRIPT COURSE — Chapter 6: Classes
 * ============================================================================
 *
 *  TypeScript classes build on JavaScript classes (which you're learning in
 *  the JS course) and add:
 *    - Type annotations for properties and methods
 *    - Access modifiers: public, private, protected
 *    - readonly properties
 *    - Parameter properties shorthand
 *    - Abstract classes
 *    - Interface implementation (implements keyword)
 *
 *  PYTHON COMPARISON:
 *    Python:      class User:                             # _ for "private" (convention only)
 *                     def __init__(self, name: str): ...
 *    TypeScript:  class User {                            // private/protected (ENFORCED)
 *                     constructor(public name: string) {}
 *                 }
 *
 *  Python uses _ prefix as a convention for private. TypeScript ENFORCES it.
 *  Think of TS classes as Python dataclasses with enforced access control.
 *
 *  Run: npx tsx ch6_classes.ts
 * ============================================================================
 */

// ============================================================================
// 1. BASIC TYPED CLASS
// ============================================================================

console.log("=== BASIC TYPED CLASS ===");

// TypeScript classes must declare their properties with types.
// This is different from JS where you just assign in the constructor.

class User {
    // Declare properties with types FIRST
    name: string;
    email: string;
    age: number;

    constructor(name: string, email: string, age: number) {
        this.name = name;
        this.email = email;
        this.age = age;
    }

    describe(): string {
        return `${this.name} (${this.email}), age ${this.age}`;
    }
}

let user = new User("Chint", "chint@example.com", 25);
console.log("user:", user.describe());
console.log("user.name:", user.name);

// TypeScript ensures you pass the right types:
// let bad = new User("Chint", 25, "email");  // ERROR! Wrong types


// ============================================================================
// 2. ACCESS MODIFIERS — public, private, protected
// ============================================================================

console.log("\n=== ACCESS MODIFIERS ===");

// Python comparison:
//   name    = public (convention)
//   _name   = "protected" (convention only — not enforced)
//   __name  = "private" (name mangling — hacky, not truly private)
//
// TypeScript ENFORCES access:
//   public:    accessible everywhere (default)
//   private:   only accessible inside the class
//   protected: accessible inside the class AND subclasses

class BankAccount {
    public owner: string;            // accessible everywhere (default)
    private balance: number;         // ONLY accessible inside this class
    protected accountType: string;   // accessible in this class + subclasses

    constructor(owner: string, balance: number, type: string) {
        this.owner = owner;
        this.balance = balance;
        this.accountType = type;
    }

    // Public method — anyone can call it
    public getBalance(): number {
        return this.balance;
    }

    // Public method that modifies private state
    public deposit(amount: number): void {
        if (amount <= 0) throw new Error("Amount must be positive");
        this.balance += amount;
        this.logTransaction("deposit", amount);   // calling private method
    }

    public withdraw(amount: number): void {
        if (amount > this.balance) throw new Error("Insufficient funds");
        this.balance -= amount;
        this.logTransaction("withdrawal", amount);
    }

    // Private method — only this class can call it
    private logTransaction(type: string, amount: number): void {
        console.log(`  [LOG] ${type}: $${amount}, new balance: $${this.balance}`);
    }
}

let account = new BankAccount("Chint", 1000, "checking");
console.log("Owner:", account.owner);                // OK — public
console.log("Balance:", account.getBalance());       // OK — public method
account.deposit(500);
account.withdraw(200);
// account.balance;          // ERROR! private
// account.logTransaction(); // ERROR! private
// account.accountType;      // ERROR! protected

// Subclass can access protected:
class SavingsAccount extends BankAccount {
    private interestRate: number;

    constructor(owner: string, balance: number, rate: number) {
        super(owner, balance, "savings");
        this.interestRate = rate;
    }

    getInfo(): string {
        // Can access protected accountType from parent:
        return `${this.owner}'s ${this.accountType} (${this.interestRate}% interest)`;
    }
}

let savings = new SavingsAccount("Chint", 5000, 2.5);
console.log(savings.getInfo());


// ============================================================================
// 3. READONLY PROPERTIES
// ============================================================================

console.log("\n=== READONLY PROPERTIES ===");

// readonly properties can only be set in the constructor.
// After that, they can't be changed.

class Config {
    readonly apiKey: string;
    readonly baseUrl: string;
    timeout: number;    // this one CAN be changed

    constructor(apiKey: string, baseUrl: string, timeout: number = 5000) {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
        this.timeout = timeout;
    }
}

let config = new Config("secret-key-123", "https://api.example.com");
console.log("config.apiKey:", config.apiKey);
console.log("config.timeout:", config.timeout);
config.timeout = 10000;   // OK — not readonly
// config.apiKey = "new";  // ERROR! readonly
console.log("config.timeout (changed):", config.timeout);


// ============================================================================
// 4. PARAMETER PROPERTIES — The shorthand you'll love
// ============================================================================

console.log("\n=== PARAMETER PROPERTIES ===");

// TypeScript has a SHORTHAND that eliminates boilerplate.
// Instead of declaring properties AND assigning them in the constructor,
// just add an access modifier to the constructor parameters.

// BEFORE (verbose):
class PersonVerbose {
    public name: string;
    private age: number;
    readonly id: number;

    constructor(name: string, age: number, id: number) {
        this.name = name;
        this.age = age;
        this.id = id;
    }
}

// AFTER (parameter properties — same result, way less code):
class PersonShort {
    constructor(
        public name: string,       // creates AND assigns this.name
        private age: number,       // creates AND assigns this.age
        readonly id: number        // creates AND assigns this.id
    ) {
        // No body needed! TypeScript does it all.
    }

    describe(): string {
        return `${this.name}, age ${this.age}, id ${this.id}`;
    }
}

let person = new PersonShort("Chint", 25, 1);
console.log("person:", person.describe());
console.log("person.name:", person.name);     // OK — public
// person.age;  // ERROR! private
// person.id = 2;  // ERROR! readonly

// This is like Python's @dataclass but even shorter:
//   @dataclass
//   class Person:
//       name: str
//       age: int
//       id: int


// ============================================================================
// 5. IMPLEMENTS — Classes that conform to interfaces
// ============================================================================

console.log("\n=== IMPLEMENTS ===");

// An interface defines a CONTRACT. A class can IMPLEMENT that contract.
// This ensures the class has all the required properties and methods.
// Python comparison: like an ABC (Abstract Base Class) but for shape checking.

interface Printable {
    toString(): string;
    print(): void;
}

interface Serializable {
    toJSON(): string;
}

// A class can implement MULTIPLE interfaces:
class Product implements Printable, Serializable {
    constructor(
        public name: string,
        public price: number,
        public category: string
    ) {}

    toString(): string {
        return `${this.name} ($${this.price})`;
    }

    print(): void {
        console.log(`  Product: ${this.toString()}`);
    }

    toJSON(): string {
        return JSON.stringify({ name: this.name, price: this.price, category: this.category });
    }
}

let laptop = new Product("Laptop", 999, "electronics");
laptop.print();
console.log("JSON:", laptop.toJSON());

// If you forget to implement a method, TypeScript gives an error:
// class BadProduct implements Printable {
//     // ERROR! Missing print() and toString()
// }

// Interface for a repository pattern (common in backends):
interface Repository<T> {
    getAll(): T[];
    getById(id: number): T | undefined;
    add(item: T): void;
}

interface TodoItem {
    id: number;
    text: string;
    done: boolean;
}

class TodoRepo implements Repository<TodoItem> {
    private items: TodoItem[] = [];

    getAll(): TodoItem[] {
        return [...this.items];
    }

    getById(id: number): TodoItem | undefined {
        return this.items.find(item => item.id === id);
    }

    add(item: TodoItem): void {
        this.items.push(item);
    }
}

let todos = new TodoRepo();
todos.add({ id: 1, text: "Learn TypeScript", done: false });
todos.add({ id: 2, text: "Build a project", done: false });
console.log("todos:", todos.getAll());
console.log("todo #1:", todos.getById(1));


// ============================================================================
// 6. ABSTRACT CLASSES — Base classes that can't be instantiated
// ============================================================================

console.log("\n=== ABSTRACT CLASSES ===");

// An abstract class:
//   - Cannot be instantiated directly (can't do "new AbstractClass()")
//   - Can have abstract methods (no body — subclasses MUST implement them)
//   - Can have regular methods (with bodies — shared by all subclasses)
//
// Python comparison: from abc import ABC, abstractmethod

abstract class Shape {
    constructor(public color: string) {}

    // Abstract method — subclasses MUST implement this
    abstract area(): number;
    abstract perimeter(): number;

    // Regular method — shared by all subclasses
    describe(): string {
        return `${this.color} ${this.constructor.name}: area=${this.area().toFixed(2)}, perimeter=${this.perimeter().toFixed(2)}`;
    }
}

// let shape = new Shape("red");  // ERROR! Can't instantiate abstract class

class Circle extends Shape {
    constructor(color: string, public radius: number) {
        super(color);
    }

    area(): number {
        return Math.PI * this.radius ** 2;
    }

    perimeter(): number {
        return 2 * Math.PI * this.radius;
    }
}

class RectangleShape extends Shape {
    constructor(color: string, public width: number, public height: number) {
        super(color);
    }

    area(): number {
        return this.width * this.height;
    }

    perimeter(): number {
        return 2 * (this.width + this.height);
    }
}

let shapes: Shape[] = [
    new Circle("red", 5),
    new RectangleShape("blue", 4, 6),
    new Circle("green", 3)
];

console.log("Shapes:");
for (let shape of shapes) {
    console.log(`  ${shape.describe()}`);
}


// ============================================================================
// 7. GENERICS WITH CLASSES — Typed data structures
// ============================================================================

console.log("\n=== GENERICS WITH CLASSES ===");

// Combining generics + classes = powerful typed data structures.

class Queue<T> {
    private items: T[] = [];

    enqueue(item: T): void {
        this.items.push(item);
    }

    dequeue(): T | undefined {
        return this.items.shift();
    }

    peek(): T | undefined {
        return this.items[0];
    }

    get size(): number {
        return this.items.length;
    }

    isEmpty(): boolean {
        return this.items.length === 0;
    }
}

// Queue of numbers:
let numQueue = new Queue<number>();
numQueue.enqueue(10);
numQueue.enqueue(20);
numQueue.enqueue(30);
console.log("numQueue.dequeue():", numQueue.dequeue());  // 10 (FIFO)
console.log("numQueue.peek():", numQueue.peek());        // 20
console.log("numQueue.size:", numQueue.size);             // 2

// Queue of strings:
let taskQueue = new Queue<string>();
taskQueue.enqueue("Write code");
taskQueue.enqueue("Run tests");
taskQueue.enqueue("Deploy");
console.log("taskQueue.dequeue():", taskQueue.dequeue());  // "Write code"

// Generic class with constraint:
class SortedList<T extends number | string> {
    private items: T[] = [];

    add(item: T): void {
        this.items.push(item);
        this.items.sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
    }

    getAll(): T[] {
        return [...this.items];
    }
}

let sortedNums = new SortedList<number>();
sortedNums.add(30);
sortedNums.add(10);
sortedNums.add(20);
console.log("sortedNums:", sortedNums.getAll());  // [10, 20, 30]

let sortedNames = new SortedList<string>();
sortedNames.add("Charlie");
sortedNames.add("Alice");
sortedNames.add("Bob");
console.log("sortedNames:", sortedNames.getAll());  // ["Alice", "Bob", "Charlie"]


// ============================================================================
// 8. PYTHON vs TYPESCRIPT CLASSES — Side by side
// ============================================================================

console.log("\n=== PYTHON vs TYPESCRIPT COMPARISON ===");

// Python:
//   @dataclass
//   class User:
//       name: str
//       email: str
//       _age: int = 0               # "private" by convention
//
//       def greet(self) -> str:
//           return f"Hi, I'm {self.name}"

// TypeScript equivalent:
class UserTS {
    constructor(
        public name: string,
        public email: string,
        private age: number = 0      // TRULY private (enforced)
    ) {}

    greet(): string {
        return `Hi, I'm ${this.name}`;
    }
}

let userTS = new UserTS("Chint", "chint@example.com", 25);
console.log(userTS.greet());

// Key differences:
console.log("\nPython vs TypeScript classes:");
console.log("  - Python: self.name      | TypeScript: this.name");
console.log("  - Python: _private       | TypeScript: private keyword (enforced)");
console.log("  - Python: @abstractmethod| TypeScript: abstract keyword");
console.log("  - Python: @dataclass     | TypeScript: parameter properties");
console.log("  - Python: no interfaces  | TypeScript: implements keyword");
console.log("  - Python: duck typing    | TypeScript: structural typing (similar!)");


// ============================================================================
// 9. STATIC MEMBERS
// ============================================================================

console.log("\n=== STATIC MEMBERS ===");

// Static properties and methods belong to the CLASS, not instances.
// Same as Python's @staticmethod and @classmethod.

class MathHelper {
    static readonly PI = 3.14159;

    static square(n: number): number {
        return n ** 2;
    }

    static cube(n: number): number {
        return n ** 3;
    }

    static clamp(value: number, min: number, max: number): number {
        return Math.min(Math.max(value, min), max);
    }
}

// Called on the CLASS, not an instance:
console.log("MathHelper.PI:", MathHelper.PI);
console.log("MathHelper.square(5):", MathHelper.square(5));
console.log("MathHelper.cube(3):", MathHelper.cube(3));
console.log("MathHelper.clamp(15, 0, 10):", MathHelper.clamp(15, 0, 10));

// Singleton pattern using static:
class Database {
    private static instance: Database;
    private connected = false;

    private constructor() {}  // private constructor = can't use "new"

    static getInstance(): Database {
        if (!Database.instance) {
            Database.instance = new Database();
        }
        return Database.instance;
    }

    connect(): void {
        this.connected = true;
        console.log("  Database connected");
    }

    isConnected(): boolean {
        return this.connected;
    }
}

let db1 = Database.getInstance();
let db2 = Database.getInstance();
db1.connect();
console.log("db1 === db2:", db1 === db2);  // true — same instance
console.log("db2.isConnected():", db2.isConnected());  // true — same instance


// ============================================================================
// RECAP
// ============================================================================

console.log("\n=== CHAPTER 6 RECAP ===");
console.log("1. Typed classes: declare property types, typed constructor");
console.log("2. Access modifiers: public, private (enforced!), protected");
console.log("3. readonly: can only be set in constructor");
console.log("4. Parameter properties: constructor(public name: string) — shorthand!");
console.log("5. implements: class conforms to an interface contract");
console.log("6. abstract: base class with required methods for subclasses");
console.log("7. Generics + classes: class Stack<T> for typed data structures");
console.log("8. static: class-level properties and methods");
console.log("\nNext up: Chapter 7 — Utility Types!");
