// ============================================================================
// CHAPTER 3: STATE AND useState — Making Components Dynamic
// ============================================================================
//
// HOW TO USE THIS FILE:
// 1. Copy this file into your React project's src/ folder
// 2. In src/App.tsx, write:
//      import Chapter3 from './ch3_state_useState';
//      function App() { return <Chapter3 />; }
//      export default App;
// 3. Save and check your browser.
//
// ============================================================================
//
// WHAT IS STATE?
// ==============
// State is data that BELONGS to a component and can CHANGE over time.
// When state changes, React automatically RE-RENDERS the component to
// show the new data. This is React's core superpower.
//
// Props vs State:
// - Props: data passed IN from parent. READ-ONLY. Component can't change them.
// - State: data managed BY the component itself. The component CAN change it.
//
// COMPARE TO PYTHON:
//   In Flask, data lives on the SERVER. When you click a button, a new HTTP
//   request goes to the server, the server processes it, and sends back a
//   new page. The whole page reloads.
//
//   In React, state lives IN THE BROWSER, in the component. When you click
//   a button, the state updates instantly, and ONLY the parts of the page
//   that depend on that state re-render. No server round-trip, no page reload.
//   This is why React apps feel fast and responsive.
//
//   Python class analogy:
//     class Counter:
//         def __init__(self):
//             self.count = 0       # <-- this is like state
//         def increment(self):
//             self.count += 1      # <-- this is like setState
//
// ============================================================================
//
// useState HOOK
// =============
// useState is a "hook" — a special function that lets function components
// have state. Hooks always start with "use".
//
// Syntax:
//   const [value, setValue] = useState(initialValue)
//
// This uses array destructuring (from JavaScript):
//   - value: the current state value
//   - setValue: a function to UPDATE the state
//   - initialValue: what value starts as on the first render
//
// WHY CAN'T WE JUST USE A REGULAR VARIABLE?
// ------------------------------------------
//   let count = 0;
//   count = count + 1;    // This changes the variable, BUT...
//                          // React doesn't know it changed!
//                          // The screen won't update!
//
// React needs to KNOW when data changes so it can re-render. useState
// gives you a setter function (setCount) that tells React: "Hey, data
// changed! Please re-render this component."
//
// ============================================================================
//
// UPDATING STATE: TWO FORMS
// =========================
// Form 1 (direct value):
//   setCount(5)                  // Set to exactly 5
//   setCount(count + 1)          // Use current count + 1
//
// Form 2 (function / "updater" form):
//   setCount(prev => prev + 1)   // Use the PREVIOUS value
//
// ALWAYS use Form 2 when new state depends on old state.
// WHY? Because React batches state updates. If you call setCount(count + 1)
// twice in a row, both calls see the SAME "count" (the value at render time).
// With setCount(prev => prev + 1), each call gets the truly latest value.
//
// ============================================================================

import React, { useState } from 'react';

// ---------------------------------------------------------------------------
// BASIC COUNTER: The "Hello World" of state
// ---------------------------------------------------------------------------
function Counter() {
  // useState returns an array of [currentValue, setterFunction].
  // We destructure it: count is the value, setCount is the setter.
  // TypeScript INFERS the type from the initial value (0 => number).
  const [count, setCount] = useState(0);

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Basic Counter</h3>
      <p>Count: <strong>{count}</strong></p>

      {/* When the button is clicked, setCount is called with the new value */}
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(count - 1)} style={{ marginLeft: '8px' }}>Decrement</button>
      <button onClick={() => setCount(0)} style={{ marginLeft: '8px' }}>Reset</button>

      {/*
        What happens when you click "Increment":
        1. setCount(count + 1) is called
        2. React schedules a re-render with the new count
        3. This function runs AGAIN from the top
        4. useState(0) returns the NEW count (not 0 — React remembers)
        5. The JSX renders with the updated count

        The component function runs EVERY time state changes.
        useState remembers the value between renders.
      */}
    </div>
  );
}

// ---------------------------------------------------------------------------
// UPDATER FUNCTION FORM: prev => prev + 1
// ---------------------------------------------------------------------------
function UpdaterDemo() {
  const [count, setCount] = useState(0);

  // BAD: Using count directly — both see the same count value
  const incrementTwiceBad = () => {
    setCount(count + 1);   // If count is 0, this sets count to 1
    setCount(count + 1);   // count is STILL 0 here (same render), sets to 1 again!
    // Result: count goes from 0 to 1, not 0 to 2!
  };

  // GOOD: Using the updater function — each gets the latest value
  const incrementTwiceGood = () => {
    setCount(prev => prev + 1);   // prev is 0, returns 1
    setCount(prev => prev + 1);   // prev is 1 (updated!), returns 2
    // Result: count correctly goes from 0 to 2!
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Updater Function Demo</h3>
      <p>Count: <strong>{count}</strong></p>
      <button onClick={incrementTwiceBad}>Add 2 (broken: count + 1)</button>
      <button onClick={incrementTwiceGood} style={{ marginLeft: '8px' }}>Add 2 (correct: prev + 1)</button>
      <button onClick={() => setCount(0)} style={{ marginLeft: '8px' }}>Reset</button>
      <p style={{ fontSize: '14px', color: '#666' }}>
        Click each button — the broken one only adds 1 because both setCount calls see the same value.
      </p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// STATE WITH STRINGS AND TYPED STATE
// ---------------------------------------------------------------------------
function NameInput() {
  // TypeScript infers string from the initial value ""
  const [name, setName] = useState("");

  // Explicit typing: useState<string | null>(null)
  // This says: state can be string OR null. Useful when initial value is null.
  const [submitted, setSubmitted] = useState<string | null>(null);

  const handleSubmit = () => {
    if (name.trim()) {
      setSubmitted(name);
      setName("");   // Clear the input after submitting
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>State with Strings</h3>
      <input
        type="text"
        value={name}          // The input's value comes from state ("controlled input")
        onChange={(e) => setName(e.target.value)}   // Update state on every keystroke
        placeholder="Type your name"
        style={{ padding: '6px', fontSize: '16px' }}
      />
      <button onClick={handleSubmit} style={{ marginLeft: '8px' }}>Submit</button>
      {submitted && <p>Hello, <strong>{submitted}</strong>!</p>}

      {/*
        This is a "controlled component" — the input's value is controlled by React state.
        Every time you type a character:
        1. onChange fires
        2. setName updates the state with e.target.value (the new input value)
        3. React re-renders
        4. The input shows the new state value

        It feels instant, but React is actually re-rendering on every keystroke.
        This is fine — React is very fast.
      */}
    </div>
  );
}

// ---------------------------------------------------------------------------
// STATE WITH OBJECTS: Use the spread operator to update
// ---------------------------------------------------------------------------
interface User {
  name: string;
  email: string;
  age: number;
}

function UserProfile() {
  // State can hold objects. We type it with our interface.
  const [user, setUser] = useState<User>({
    name: "Chint",
    email: "chint@example.com",
    age: 25,
  });

  // IMPORTANT: Never mutate state directly!
  // BAD:  user.name = "New Name"         // Mutates the object — React won't re-render!
  // GOOD: setUser({...user, name: "New"}) // Creates a NEW object — React sees the change!
  //
  // The spread operator (...user) copies all properties from the old object,
  // then the property after it (name: "New") overrides just that one field.
  // This creates a completely new object, which React can detect as a change.

  const updateName = (newName: string) => {
    setUser({ ...user, name: newName });   // Spread old user, override name
  };

  const birthday = () => {
    setUser(prev => ({ ...prev, age: prev.age + 1 }));  // Updater form with objects
    // Note the extra parentheses: (prev) => ({ ... })
    // Without them, the { } would be interpreted as a function body, not an object.
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>State with Objects</h3>
      <p>Name: {user.name}</p>
      <p>Email: {user.email}</p>
      <p>Age: {user.age}</p>
      <input
        type="text"
        value={user.name}
        onChange={(e) => updateName(e.target.value)}
        style={{ padding: '6px' }}
      />
      <button onClick={birthday} style={{ marginLeft: '8px' }}>Happy Birthday! (+1 age)</button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// STATE WITH ARRAYS: Add, remove, update items
// ---------------------------------------------------------------------------
function TodoList() {
  const [todos, setTodos] = useState<string[]>(["Learn React", "Learn TypeScript"]);
  const [newTodo, setNewTodo] = useState("");

  // ADD: spread old array + new item
  const addTodo = () => {
    if (newTodo.trim()) {
      setTodos([...todos, newTodo]);    // [...old, new] = new array with all old items plus the new one
      setNewTodo("");                    // Clear input
    }
  };

  // REMOVE: filter creates a new array WITHOUT the removed item
  const removeTodo = (indexToRemove: number) => {
    setTodos(todos.filter((_, index) => index !== indexToRemove));
    // filter returns a NEW array with only items where the condition is true.
    // We keep every item EXCEPT the one at indexToRemove.
  };

  // UPDATE: map creates a new array with one item changed
  const editTodo = (indexToEdit: number, newText: string) => {
    setTodos(todos.map((todo, index) =>
      index === indexToEdit ? newText : todo
    ));
    // map returns a NEW array. For the item at indexToEdit, we return newText.
    // For all other items, we return the original todo unchanged.
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>State with Arrays (Todo List)</h3>

      <div style={{ marginBottom: '10px' }}>
        <input
          type="text"
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          placeholder="Add a todo"
          style={{ padding: '6px' }}
          onKeyDown={(e) => e.key === 'Enter' && addTodo()}  // Enter key adds too
        />
        <button onClick={addTodo} style={{ marginLeft: '8px' }}>Add</button>
      </div>

      <ul>
        {todos.map((todo, index) => (
          <li key={index} style={{ marginBottom: '4px' }}>
            {todo}
            <button
              onClick={() => removeTodo(index)}
              style={{ marginLeft: '8px', color: 'red', cursor: 'pointer' }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>

      {todos.length === 0 && <p style={{ color: '#999' }}>No todos yet. Add one above!</p>}

      {/*
        NEVER do this with arrays:
          todos.push(newTodo)        // Mutates the array — React won't see it!
          setTodos(todos)            // Same reference — React thinks nothing changed!

        ALWAYS create a NEW array:
          setTodos([...todos, newTodo])     // Add
          setTodos(todos.filter(...))       // Remove
          setTodos(todos.map(...))          // Update
      */}
    </div>
  );
}

// ---------------------------------------------------------------------------
// MULTIPLE STATE VARIABLES: Each piece of state is independent
// ---------------------------------------------------------------------------
function MultipleStates() {
  // Each useState is independent. Updating one doesn't affect the others.
  const [firstName, setFirstName] = useState("Chint");
  const [lastName, setLastName] = useState("D");
  const [age, setAge] = useState(25);

  // You could also use ONE state object:
  //   const [form, setForm] = useState({ firstName: "", lastName: "", age: 0 })
  // But separate useState calls are simpler and more common for unrelated values.
  // Use an object when the values are closely related and always change together.

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Multiple State Variables</h3>
      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <input value={firstName} onChange={e => setFirstName(e.target.value)} placeholder="First" style={{ padding: '6px' }} />
        <input value={lastName} onChange={e => setLastName(e.target.value)} placeholder="Last" style={{ padding: '6px' }} />
        <input type="number" value={age} onChange={e => setAge(Number(e.target.value))} style={{ padding: '6px', width: '60px' }} />
      </div>
      <p>Full info: {firstName} {lastName}, age {age}</p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// STATE IS LOCAL: Each component INSTANCE has its own state
// ---------------------------------------------------------------------------
function IndependentCounters() {
  // When you render <Counter /> twice, each one has its OWN count.
  // Clicking one doesn't affect the other. State is local and isolated.
  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>State is Local (Each Instance is Independent)</h3>
      <p>Each counter below has its own separate count state:</p>
      <Counter />
      <Counter />
    </div>
  );
}

// ---------------------------------------------------------------------------
// MAIN CHAPTER COMPONENT
// ---------------------------------------------------------------------------
function Chapter3() {
  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>Chapter 3: State & useState</h1>
      <p><em>State is data that changes over time and triggers re-renders.</em></p>

      <Counter />
      <hr />
      <UpdaterDemo />
      <hr />
      <NameInput />
      <hr />
      <UserProfile />
      <hr />
      <TodoList />
      <hr />
      <MultipleStates />
      <hr />
      <IndependentCounters />

      <footer style={{ backgroundColor: '#f0f0f0', padding: '10px', textAlign: 'center', marginTop: '20px' }}>
        <p>End of Chapter 3 — Next: useEffect and Side Effects!</p>
      </footer>
    </div>
  );
}

// ---------------------------------------------------------------------------
// CONSOLE LOG TAKEAWAYS
// ---------------------------------------------------------------------------
console.log(`
============================================================
CHAPTER 3 TAKEAWAYS: State & useState
============================================================

1. State = data that a component OWNS and can CHANGE.
2. useState hook: const [value, setValue] = useState(initialValue)
3. NEVER modify state directly (no push, no mutation).
   Always use the setter: setValue(newValue)
4. When new state depends on old state, use the updater form:
   setValue(prev => prev + 1)   NOT   setValue(value + 1)
5. Objects: setObj({ ...obj, key: newValue })
6. Arrays:
   - Add:    setArr([...arr, newItem])
   - Remove: setArr(arr.filter(...))
   - Update: setArr(arr.map(...))
7. State is LOCAL: each component instance has its own copy.
8. Type state explicitly when needed: useState<string | null>(null)

PYTHON COMPARISON:
   class Counter:
       def __init__(self): self.count = 0
       def increment(self): self.count += 1

   In React:
       const [count, setCount] = useState(0)
       const increment = () => setCount(prev => prev + 1)

   Same concept: encapsulated, mutable data.
   Difference: React's setter triggers a UI re-render.

============================================================
`);

export default Chapter3;
export { Counter, UpdaterDemo, NameInput, UserProfile, TodoList, MultipleStates };
