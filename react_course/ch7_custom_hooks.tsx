// ============================================================================
// CHAPTER 7: CUSTOM HOOKS — Reusing Stateful Logic
// ============================================================================
//
// HOW TO USE THIS FILE:
// 1. Copy this file into your React project's src/ folder
// 2. In src/App.tsx, write:
//      import Chapter7 from './ch7_custom_hooks';
//      function App() { return <Chapter7 />; }
//      export default App;
// 3. Save and check your browser.
//
// ============================================================================
//
// WHAT IS A CUSTOM HOOK?
// ======================
// A custom hook is a function that:
// 1. Starts with the word "use" (e.g., useLocalStorage, useFetch)
// 2. Uses other hooks inside it (useState, useEffect, etc.)
// 3. Returns values and/or functions that components can use
//
// Custom hooks let you EXTRACT and REUSE stateful logic between components.
// The hooks themselves are shared, but each component that uses the hook
// gets its OWN independent copy of the state.
//
// COMPARE TO PYTHON:
//   In Python, when you have common logic, you extract it into a function
//   or a class that multiple parts of your code can use:
//
//     # Python: reusable logic in a function
//     def read_json_file(path):
//         with open(path) as f:
//             return json.load(f)
//
//     # Used in multiple places
//     config = read_json_file("config.json")
//     data = read_json_file("data.json")
//
//   In React, when you have common STATEFUL logic (logic involving hooks),
//   you extract it into a custom hook:
//
//     // React: reusable stateful logic in a custom hook
//     function useLocalStorage(key, initial) {
//       const [value, setValue] = useState(...);
//       useEffect(() => { ... }, [...]);
//       return [value, setValue];
//     }
//
//     // Used in multiple components
//     const [theme, setTheme] = useLocalStorage("theme", "dark");
//     const [lang, setLang] = useLocalStorage("lang", "en");
//
// WHY CUSTOM HOOKS?
// -----------------
// Without custom hooks, you'd have to copy-paste the same useState +
// useEffect logic into every component that needs it. Custom hooks let you
// write it ONCE and use it everywhere. DRY principle: Don't Repeat Yourself.
//
// RULES FOR CUSTOM HOOKS:
// 1. Name MUST start with "use" — React uses this to enforce hook rules.
// 2. Can call any other hooks inside (useState, useEffect, other custom hooks).
// 3. Each component that uses the hook gets its OWN state — hooks don't share
//    state between components, they share the LOGIC.
//
// ============================================================================

import React, { useState, useEffect, useCallback } from 'react';

// ===========================================================================
// CUSTOM HOOK 1: useToggle
// ===========================================================================
// The simplest possible custom hook. Wraps a boolean state with a toggle function.
// Instead of writing useState(false) + a toggle handler in every component
// that needs a toggle, write it once here.
//
// Usage: const [isOpen, toggle] = useToggle(false);
// ===========================================================================
function useToggle(initialValue: boolean = false): [boolean, () => void] {
  const [value, setValue] = useState(initialValue);
  const toggle = () => setValue(prev => !prev);
  return [value, toggle];
  // Returns a tuple: [current boolean value, function to flip it]
}

// Component that USES useToggle
function ToggleDemo() {
  const [isVisible, toggleVisible] = useToggle(false);
  const [isDarkMode, toggleDarkMode] = useToggle(false);

  return (
    <div style={{
      border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px',
      backgroundColor: isDarkMode ? '#333' : 'white',
      color: isDarkMode ? 'white' : 'black',
    }}>
      <h3>useToggle Hook</h3>
      <button onClick={toggleVisible}>{isVisible ? 'Hide' : 'Show'} Content</button>
      <button onClick={toggleDarkMode} style={{ marginLeft: '8px' }}>
        {isDarkMode ? 'Light' : 'Dark'} Mode
      </button>
      {isVisible && <p style={{ marginTop: '10px' }}>This content is toggleable!</p>}
    </div>
  );
}

// ===========================================================================
// CUSTOM HOOK 2: useLocalStorage
// ===========================================================================
// Persists state in the browser's localStorage. When the page reloads,
// the state is restored from localStorage instead of resetting to the
// initial value.
//
// This is a VERY common hook in real apps (user preferences, form drafts, etc.)
//
// Usage: const [name, setName] = useLocalStorage("user_name", "");
// ===========================================================================
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((prev: T) => T)) => void] {
  // The generic type <T> means this hook works with any type:
  // useLocalStorage<string>("key", "hello")
  // useLocalStorage<number>("key", 42)
  // useLocalStorage<{ name: string }>("key", { name: "" })

  // Initialize state from localStorage (if available) or use initialValue
  const [storedValue, setStoredValue] = useState<T>(() => {
    // This function form of useState is called "lazy initialization."
    // The function only runs on the FIRST render, not on every re-render.
    // This is important because reading from localStorage is slow.
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Whenever the stored value changes, save it to localStorage
  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      console.error(`Error writing to localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);

  return [storedValue, setStoredValue];
}

// Component that USES useLocalStorage
function LocalStorageDemo() {
  const [name, setName] = useLocalStorage<string>("demo_name", "");
  const [count, setCount] = useLocalStorage<number>("demo_count", 0);

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>useLocalStorage Hook</h3>
      <p>These values persist even if you refresh the page!</p>

      <div style={{ marginBottom: '10px' }}>
        <label>Name (persisted): </label>
        <input
          type="text"
          value={name}
          onChange={e => setName(e.target.value)}
          style={{ padding: '6px' }}
        />
      </div>

      <div>
        <label>Count (persisted): {count} </label>
        <button onClick={() => setCount(prev => prev + 1)}>+1</button>
        <button onClick={() => setCount(0)} style={{ marginLeft: '8px' }}>Reset</button>
      </div>

      <p style={{ fontSize: '13px', color: '#666', marginTop: '10px' }}>
        Open DevTools &gt; Application &gt; Local Storage to see the stored values.
      </p>
    </div>
  );
}

// ===========================================================================
// CUSTOM HOOK 3: useFetch
// ===========================================================================
// Reusable data fetching hook. Handles loading, error, and data states.
// Every component that needs to fetch data can use this instead of
// writing the same useEffect + useState pattern over and over.
//
// Usage: const { data, loading, error } = useFetch<Post[]>(url);
// ===========================================================================
interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;     // function to manually re-fetch the data
}

function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [fetchCount, setFetchCount] = useState(0);  // Increment to trigger refetch

  useEffect(() => {
    let isCancelled = false;

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const result: T = await response.json();
        if (!isCancelled) setData(result);
      } catch (err) {
        if (!isCancelled) {
          setError(err instanceof Error ? err.message : 'Unknown error');
        }
      } finally {
        if (!isCancelled) setLoading(false);
      }
    };

    fetchData();

    return () => { isCancelled = true; };
  }, [url, fetchCount]);   // Re-run when URL changes or refetch is called

  const refetch = useCallback(() => {
    setFetchCount(prev => prev + 1);
  }, []);

  return { data, loading, error, refetch };
}

// Component that USES useFetch
interface Todo {
  id: number;
  title: string;
  completed: boolean;
}

function FetchDemo() {
  const { data, loading, error, refetch } = useFetch<Todo[]>(
    'https://jsonplaceholder.typicode.com/todos?_limit=5'
  );

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>useFetch Hook</h3>
      <button onClick={refetch}>Refetch Data</button>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {data && (
        <ul>
          {data.map(todo => (
            <li key={todo.id} style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}>
              {todo.title}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// ===========================================================================
// CUSTOM HOOK 4: useDebounce
// ===========================================================================
// Debouncing delays an action until the user STOPS doing something for a
// specified time. Most common use: search input — you don't want to search
// on every keystroke, only after the user stops typing.
//
// How it works:
// 1. User types "R" → start a 500ms timer
// 2. User types "Re" (200ms later) → CANCEL old timer, start new 500ms timer
// 3. User types "Rea" (150ms later) → cancel again, start new timer
// 4. User stops typing → 500ms passes → debounced value updates to "Rea"
//
// Usage: const debouncedSearch = useDebounce(searchTerm, 500);
// ===========================================================================
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    // Set a timer to update the debounced value after the delay
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cleanup: if value changes before the delay is up, cancel the timer
    // and a new one will be set by the next effect run
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Component that USES useDebounce
function DebounceDemo() {
  const [searchTerm, setSearchTerm] = useState("");
  const debouncedSearch = useDebounce(searchTerm, 500);
  const [searchResults, setSearchResults] = useState<string[]>([]);

  // Simulated search — runs only when debouncedSearch changes (after user stops typing)
  useEffect(() => {
    if (!debouncedSearch) {
      setSearchResults([]);
      return;
    }

    // Simulate an API search
    const allItems = ["React", "Redux", "Router", "Remix", "RSC", "Relay", "Recoil", "RxJS"];
    const results = allItems.filter(item =>
      item.toLowerCase().includes(debouncedSearch.toLowerCase())
    );
    setSearchResults(results);
    console.log(`[Debounce] Searching for: "${debouncedSearch}"`);
  }, [debouncedSearch]);

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>useDebounce Hook</h3>
      <input
        type="text"
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
        placeholder="Search (waits 500ms after you stop typing)..."
        style={{ padding: '8px', width: '350px', fontSize: '16px' }}
      />
      <p style={{ fontSize: '13px', color: '#666' }}>
        Typing: "{searchTerm}" | Debounced (actual search): "{debouncedSearch}"
      </p>
      {searchResults.length > 0 && (
        <ul>
          {searchResults.map(r => <li key={r}>{r}</li>)}
        </ul>
      )}
      {debouncedSearch && searchResults.length === 0 && (
        <p style={{ color: '#999' }}>No results for "{debouncedSearch}"</p>
      )}
    </div>
  );
}

// ===========================================================================
// CUSTOM HOOK 5: useWindowSize
// ===========================================================================
// Tracks the browser window dimensions. Useful for responsive behavior
// that can't be done with CSS alone (e.g., showing a different component
// layout on mobile vs desktop).
//
// Usage: const { width, height } = useWindowSize();
// ===========================================================================
interface WindowSize {
  width: number;
  height: number;
}

function useWindowSize(): WindowSize {
  const [size, setSize] = useState<WindowSize>({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return size;
}

// Component that USES useWindowSize
function WindowSizeDemo() {
  const { width, height } = useWindowSize();

  // Determine breakpoint
  const breakpoint = width < 600 ? 'mobile' : width < 1024 ? 'tablet' : 'desktop';

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>useWindowSize Hook</h3>
      <p>Window: <strong>{width}</strong> x <strong>{height}</strong></p>
      <p>Breakpoint: <strong>{breakpoint}</strong></p>
      <p style={{ fontSize: '13px', color: '#666' }}>
        Resize your browser window to see these values update in real time.
      </p>
    </div>
  );
}

// ===========================================================================
// CUSTOM HOOK 6: useCounter (combining hooks)
// ===========================================================================
// A slightly richer example showing that custom hooks can return objects
// with multiple functions. This is a common pattern.
// ===========================================================================
interface UseCounterReturn {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
  setCount: (value: number) => void;
}

function useCounter(initialValue: number = 0, step: number = 1): UseCounterReturn {
  const [count, setCount] = useState(initialValue);

  return {
    count,
    increment: () => setCount(prev => prev + step),
    decrement: () => setCount(prev => prev - step),
    reset: () => setCount(initialValue),
    setCount,
  };
}

// Component that USES useCounter
function CounterDemo() {
  const counter = useCounter(0, 5);   // Start at 0, step by 5

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>useCounter Hook (step: 5)</h3>
      <p style={{ fontSize: '24px' }}>Count: <strong>{counter.count}</strong></p>
      <button onClick={counter.decrement}>-5</button>
      <button onClick={counter.increment} style={{ marginLeft: '8px' }}>+5</button>
      <button onClick={counter.reset} style={{ marginLeft: '8px' }}>Reset</button>
      <button onClick={() => counter.setCount(100)} style={{ marginLeft: '8px' }}>Set to 100</button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// MAIN CHAPTER COMPONENT
// ---------------------------------------------------------------------------
function Chapter7() {
  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>Chapter 7: Custom Hooks</h1>
      <p><em>Extract and reuse stateful logic with functions that start with "use".</em></p>

      <ToggleDemo />
      <hr />
      <LocalStorageDemo />
      <hr />
      <FetchDemo />
      <hr />
      <DebounceDemo />
      <hr />
      <WindowSizeDemo />
      <hr />
      <CounterDemo />

      <footer style={{ backgroundColor: '#f0f0f0', padding: '10px', textAlign: 'center', marginTop: '20px' }}>
        <p>End of Chapter 7 — Next: Context and useReducer!</p>
      </footer>
    </div>
  );
}

// ---------------------------------------------------------------------------
// CONSOLE LOG TAKEAWAYS
// ---------------------------------------------------------------------------
console.log(`
============================================================
CHAPTER 7 TAKEAWAYS: Custom Hooks
============================================================

1. A custom hook is a function starting with "use" that uses other hooks.
2. Custom hooks SHARE LOGIC, not state. Each component gets its own copy.
3. Common custom hooks:
   - useToggle:       simple boolean toggle
   - useLocalStorage: persist state in browser storage
   - useFetch:        reusable data fetching with loading/error
   - useDebounce:     delay value updates (search inputs)
   - useWindowSize:   track browser window dimensions
   - useCounter:      counter with increment/decrement/reset
4. Custom hooks can return:
   - Tuples: [value, setter]   (like useState)
   - Objects: { data, loading, error, refetch }   (for complex returns)
5. Name MUST start with "use" — enforced by React and linters.
6. Can call other hooks inside — even other custom hooks.

PYTHON COMPARISON:
   Custom hooks are like writing reusable functions/classes:
     class DatabaseConnection:
         def __init__(self, url):
             self.conn = connect(url)
         def query(self, sql): ...
         def close(self): ...

   Same idea: encapsulate reusable logic. But hooks are for UI state.

============================================================
`);

export default Chapter7;
export {
  useToggle, useLocalStorage, useFetch, useDebounce, useWindowSize, useCounter,
  ToggleDemo, LocalStorageDemo, FetchDemo, DebounceDemo, WindowSizeDemo, CounterDemo,
};
