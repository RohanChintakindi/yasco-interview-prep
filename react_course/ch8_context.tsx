// ============================================================================
// CHAPTER 8: CONTEXT AND useReducer — Global State in React
// ============================================================================
//
// HOW TO USE THIS FILE:
// 1. Copy this file into your React project's src/ folder
// 2. In src/App.tsx, write:
//      import Chapter8 from './ch8_context';
//      function App() { return <Chapter8 />; }
//      export default App;
// 3. Save and check your browser.
//
// ============================================================================
//
// THE PROBLEM: PROP DRILLING
// ==========================
// Imagine you have a "theme" (light/dark) that many components need.
// Without Context, you'd have to pass it through EVERY level:
//
//   <App theme="dark">
//     <Layout theme="dark">             ← doesn't use theme, just passes it
//       <Sidebar theme="dark">          ← doesn't use theme, just passes it
//         <NavItem theme="dark">        ← doesn't use theme, just passes it
//           <Icon theme="dark" />       ← FINALLY uses theme
//         </NavItem>
//       </Sidebar>
//     </Layout>
//   </App>
//
// This is called "prop drilling" — passing props through components that
// don't need them, just so a deeply nested component can access them.
// It's tedious, error-prone, and makes refactoring painful.
//
// WHAT IS CONTEXT?
// ================
// Context lets you share data with ANY component in a subtree, without
// passing it through every level. Components can "reach up" and grab the
// data directly.
//
//   <ThemeContext.Provider value="dark">    ← provides the value
//     <Layout>                             ← doesn't know about theme
//       <Sidebar>                          ← doesn't know about theme
//         <NavItem>                        ← doesn't know about theme
//           <Icon />                       ← uses useContext(ThemeContext) to get "dark"
//         </NavItem>
//       </Sidebar>
//     </Layout>
//   </ThemeContext.Provider>
//
// COMPARE TO PYTHON:
//   Context is like a module-level variable or a singleton, but scoped to
//   a section of your UI tree and React-aware (triggers re-renders):
//
//     # Python: global-ish config
//     app.config["THEME"] = "dark"
//     # Any module can access: current_app.config["THEME"]
//
//   React Context is similar — any component within the Provider can access
//   the value without it being explicitly passed down.
//
// WHEN TO USE CONTEXT VS PROPS:
// - Use props for 1-2 levels of passing. It's simpler and more explicit.
// - Use Context for data that many components at many levels need:
//   themes, authentication, locale/language, UI state.
// - Don't overuse Context — it makes components less reusable because
//   they depend on an implicit provider being present above them.
//
// ============================================================================
//
// useReducer: COMPLEX STATE MANAGEMENT
// =====================================
// useReducer is an alternative to useState for complex state logic.
// It's inspired by Redux and uses the "reducer" pattern:
//
//   const [state, dispatch] = useReducer(reducer, initialState);
//
//   - state: the current state object
//   - dispatch: a function to send "actions" that describe what happened
//   - reducer: a pure function that takes (state, action) and returns new state
//
// COMPARE TO PYTHON:
//   A reducer is like a match/case (or if/elif) that processes commands:
//
//     def reducer(state, action):
//         match action["type"]:
//             case "increment":
//                 return {**state, "count": state["count"] + 1}
//             case "decrement":
//                 return {**state, "count": state["count"] - 1}
//             case "reset":
//                 return {**state, "count": 0}
//
// WHY useReducer over useState?
// - When state has multiple related values (like a form with many fields)
// - When state transitions are complex (multiple ways to change state)
// - When the next state depends on the previous state in complex ways
// - When you want to keep all state logic in one place (the reducer)
//
// ============================================================================

import React, { createContext, useContext, useReducer, useState } from 'react';

// ===========================================================================
// PART 1: Basic Context — Theme Toggle
// ===========================================================================

// Step 1: CREATE the context with a default value.
// The default value is used when a component reads the context but there's
// no Provider above it. It's also useful for TypeScript type inference.
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

// createContext needs a default value. We provide a sensible default.
const ThemeContext = createContext<ThemeContextType>({
  theme: 'light',
  toggleTheme: () => {},  // no-op default
});

// Step 2: Create a PROVIDER component.
// This wraps part of your component tree and provides the actual value.
function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const toggleTheme = () => setTheme(prev => prev === 'light' ? 'dark' : 'light');

  return (
    // value={...} is what all consumers will receive
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Step 3: CONSUME the context with useContext in any descendant component.
// These components don't receive theme as a prop — they grab it from Context.

function ThemedHeader() {
  const { theme } = useContext(ThemeContext);
  // useContext(ThemeContext) returns whatever value the nearest Provider has

  return (
    <header style={{
      backgroundColor: theme === 'dark' ? '#333' : '#f0f0f0',
      color: theme === 'dark' ? 'white' : 'black',
      padding: '15px',
      borderRadius: '8px 8px 0 0',
    }}>
      <h3>Themed Header (current: {theme})</h3>
      <p>This component reads theme from Context — no props needed!</p>
    </header>
  );
}

function ThemeToggleButton() {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <button
      onClick={toggleTheme}
      style={{
        padding: '8px 16px',
        backgroundColor: theme === 'dark' ? 'white' : '#333',
        color: theme === 'dark' ? '#333' : 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        margin: '10px',
      }}
    >
      Switch to {theme === 'dark' ? 'Light' : 'Dark'} Mode
    </button>
  );
}

function ThemedContent() {
  const { theme } = useContext(ThemeContext);

  return (
    <div style={{
      backgroundColor: theme === 'dark' ? '#444' : 'white',
      color: theme === 'dark' ? '#eee' : '#333',
      padding: '15px',
      borderRadius: '0 0 8px 8px',
      border: `1px solid ${theme === 'dark' ? '#555' : '#ccc'}`,
    }}>
      <p>This content is themed! The theme comes from Context.</p>
      <p>No prop drilling — ThemedContent doesn't receive "theme" as a prop.</p>
      <ThemeToggleButton />
    </div>
  );
}

// Composing the themed section:
// ThemeProvider wraps everything → any descendant can use useContext(ThemeContext)
function ThemeDemo() {
  return (
    <div style={{ margin: '10px' }}>
      <h3>Context Demo: Theme</h3>
      <ThemeProvider>
        {/* These components get theme from Context, not props */}
        <ThemedHeader />
        <ThemedContent />
      </ThemeProvider>
    </div>
  );
}

// ===========================================================================
// PART 2: useReducer — Complex State Management
// ===========================================================================

// Define the state shape
interface CounterState {
  count: number;
  history: number[];     // track previous values
  lastAction: string;
}

// Define ALL possible actions with TypeScript discriminated unions.
// Each action has a "type" string and optional payload data.
type CounterAction =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'reset' }
  | { type: 'set'; payload: number }
  | { type: 'multiply'; payload: number };

// The REDUCER function: takes current state + action, returns NEW state.
// This is a PURE function — no side effects, no mutations.
// Given the same inputs, it always produces the same output.
function counterReducer(state: CounterState, action: CounterAction): CounterState {
  switch (action.type) {
    case 'increment':
      return {
        count: state.count + 1,
        history: [...state.history, state.count],
        lastAction: 'increment',
      };
    case 'decrement':
      return {
        count: state.count - 1,
        history: [...state.history, state.count],
        lastAction: 'decrement',
      };
    case 'reset':
      return {
        count: 0,
        history: [],
        lastAction: 'reset',
      };
    case 'set':
      return {
        count: action.payload,
        history: [...state.history, state.count],
        lastAction: `set to ${action.payload}`,
      };
    case 'multiply':
      return {
        count: state.count * action.payload,
        history: [...state.history, state.count],
        lastAction: `multiply by ${action.payload}`,
      };
    default:
      // TypeScript's exhaustive check — if we forget a case, this errors
      return state;
  }
}

function ReducerCounter() {
  const initialState: CounterState = {
    count: 0,
    history: [],
    lastAction: 'none',
  };

  // useReducer replaces useState for complex state.
  // dispatch sends actions to the reducer, which computes the new state.
  const [state, dispatch] = useReducer(counterReducer, initialState);

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>useReducer Demo: Advanced Counter</h3>
      <p style={{ fontSize: '28px' }}>Count: <strong>{state.count}</strong></p>
      <p>Last action: {state.lastAction}</p>

      {/* dispatch sends an action object to the reducer */}
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        <button onClick={() => dispatch({ type: 'decrement' })}>-1</button>
        <button onClick={() => dispatch({ type: 'increment' })}>+1</button>
        <button onClick={() => dispatch({ type: 'multiply', payload: 2 })}>x2</button>
        <button onClick={() => dispatch({ type: 'set', payload: 42 })}>Set to 42</button>
        <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
      </div>

      {state.history.length > 0 && (
        <p style={{ fontSize: '13px', color: '#666', marginTop: '10px' }}>
          History: {state.history.slice(-8).join(' -> ')} -> {state.count}
        </p>
      )}
    </div>
  );
}

// ===========================================================================
// PART 3: Context + useReducer — The Full Pattern
// ===========================================================================
// This is the pattern used in many real apps for global state management.
// Context provides the state to all components. useReducer manages the
// state transitions. Together, they're a lightweight alternative to Redux.
// ===========================================================================

// State shape for our todo app
interface TodoState {
  todos: Array<{ id: number; text: string; completed: boolean }>;
  nextId: number;
  filter: 'all' | 'active' | 'completed';
}

// All possible actions
type TodoAction =
  | { type: 'add'; payload: string }
  | { type: 'toggle'; payload: number }
  | { type: 'remove'; payload: number }
  | { type: 'setFilter'; payload: 'all' | 'active' | 'completed' };

// Reducer: handles all state transitions in one place
function todoReducer(state: TodoState, action: TodoAction): TodoState {
  switch (action.type) {
    case 'add':
      return {
        ...state,
        todos: [...state.todos, { id: state.nextId, text: action.payload, completed: false }],
        nextId: state.nextId + 1,
      };
    case 'toggle':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.payload ? { ...todo, completed: !todo.completed } : todo
        ),
      };
    case 'remove':
      return {
        ...state,
        todos: state.todos.filter(todo => todo.id !== action.payload),
      };
    case 'setFilter':
      return {
        ...state,
        filter: action.payload,
      };
    default:
      return state;
  }
}

// Create context for the todo state and dispatch
interface TodoContextType {
  state: TodoState;
  dispatch: React.Dispatch<TodoAction>;
}

const TodoContext = createContext<TodoContextType | null>(null);

// Custom hook to use the todo context — provides a nicer API and error checking
function useTodoContext(): TodoContextType {
  const context = useContext(TodoContext);
  if (!context) {
    throw new Error('useTodoContext must be used within a TodoProvider');
    // This error fires if you use the hook outside of a <TodoProvider>.
    // It's a helpful developer experience pattern.
  }
  return context;
}

// Provider component: creates the reducer and provides it via context
function TodoProvider({ children }: { children: React.ReactNode }) {
  const initialState: TodoState = {
    todos: [
      { id: 1, text: "Learn Context", completed: false },
      { id: 2, text: "Learn useReducer", completed: false },
    ],
    nextId: 3,
    filter: 'all',
  };

  const [state, dispatch] = useReducer(todoReducer, initialState);

  return (
    <TodoContext.Provider value={{ state, dispatch }}>
      {children}
    </TodoContext.Provider>
  );
}

// Consumer components: they use the custom hook to access state and dispatch
function TodoInput() {
  const { dispatch } = useTodoContext();
  const [text, setText] = useState("");

  const handleAdd = () => {
    if (text.trim()) {
      dispatch({ type: 'add', payload: text });
      setText("");
    }
  };

  return (
    <div style={{ display: 'flex', gap: '8px', marginBottom: '10px' }}>
      <input
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleAdd()}
        placeholder="Add todo..."
        style={{ flex: 1, padding: '6px' }}
      />
      <button onClick={handleAdd}>Add</button>
    </div>
  );
}

function TodoFilter() {
  const { state, dispatch } = useTodoContext();
  const filters: Array<'all' | 'active' | 'completed'> = ['all', 'active', 'completed'];

  return (
    <div style={{ marginBottom: '10px' }}>
      {filters.map(f => (
        <button
          key={f}
          onClick={() => dispatch({ type: 'setFilter', payload: f })}
          style={{
            margin: '0 4px',
            padding: '4px 10px',
            backgroundColor: state.filter === f ? '#007bff' : '#e0e0e0',
            color: state.filter === f ? 'white' : 'black',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          {f.charAt(0).toUpperCase() + f.slice(1)}
        </button>
      ))}
    </div>
  );
}

function TodoItems() {
  const { state, dispatch } = useTodoContext();

  const filteredTodos = state.todos.filter(todo => {
    if (state.filter === 'active') return !todo.completed;
    if (state.filter === 'completed') return todo.completed;
    return true;
  });

  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {filteredTodos.map(todo => (
        <li key={todo.id} style={{
          display: 'flex', alignItems: 'center', gap: '8px',
          padding: '6px', backgroundColor: '#f9f9f9', marginBottom: '4px', borderRadius: '4px',
        }}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => dispatch({ type: 'toggle', payload: todo.id })}
          />
          <span style={{
            flex: 1,
            textDecoration: todo.completed ? 'line-through' : 'none',
            color: todo.completed ? '#999' : '#333',
          }}>
            {todo.text}
          </span>
          <button
            onClick={() => dispatch({ type: 'remove', payload: todo.id })}
            style={{ color: 'red', background: 'none', border: 'none', cursor: 'pointer' }}
          >
            Remove
          </button>
        </li>
      ))}
      {filteredTodos.length === 0 && (
        <p style={{ color: '#999', textAlign: 'center' }}>No todos match this filter.</p>
      )}
    </ul>
  );
}

function ContextReducerDemo() {
  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Context + useReducer: Todo App</h3>
      <p style={{ fontSize: '13px', color: '#666' }}>
        All components below access state through Context — no prop drilling!
      </p>
      <TodoProvider>
        <TodoInput />
        <TodoFilter />
        <TodoItems />
      </TodoProvider>
    </div>
  );
}

// ---------------------------------------------------------------------------
// MAIN CHAPTER COMPONENT
// ---------------------------------------------------------------------------
function Chapter8() {
  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>Chapter 8: Context & useReducer</h1>
      <p><em>Share state across components without prop drilling, and manage complex state with reducers.</em></p>

      <ThemeDemo />
      <hr />
      <ReducerCounter />
      <hr />
      <ContextReducerDemo />

      <footer style={{ backgroundColor: '#f0f0f0', padding: '10px', textAlign: 'center', marginTop: '20px' }}>
        <p>End of Chapter 8 — Next: React Router!</p>
      </footer>
    </div>
  );
}

// ---------------------------------------------------------------------------
// CONSOLE LOG TAKEAWAYS
// ---------------------------------------------------------------------------
console.log(`
============================================================
CHAPTER 8 TAKEAWAYS: Context & useReducer
============================================================

1. PROP DRILLING = passing props through components that don't need them.
2. Context solves this:
   - createContext(defaultValue) — create the context
   - <Context.Provider value={...}> — provide the value
   - useContext(Context) — consume the value in any descendant
3. useReducer: alternative to useState for complex state.
   - const [state, dispatch] = useReducer(reducer, initialState)
   - reducer(state, action) => newState (pure function)
   - dispatch({ type: 'ACTION_NAME', payload: data })
4. Context + useReducer = lightweight state management (alternative to Redux).
5. Custom hook pattern: useSomethingContext() with error checking.
6. DON'T overuse Context — props are simpler for 1-2 levels.
   Use Context for: theme, auth, locale, app-wide state.

PYTHON COMPARISON:
   Context is like Flask's g object or app.config:
     - Set once at the top level
     - Accessible anywhere in the request/app
   useReducer is like a state machine or command pattern:
     - Centralized logic for all state transitions
     - Actions describe WHAT happened, reducer decides HOW state changes

============================================================
`);

export default Chapter8;
export { ThemeProvider, ThemeContext, TodoProvider, useTodoContext };
