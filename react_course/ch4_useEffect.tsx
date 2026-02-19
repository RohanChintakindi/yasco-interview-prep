// ============================================================================
// CHAPTER 4: useEffect — Side Effects in React
// ============================================================================
//
// HOW TO USE THIS FILE:
// 1. Copy this file into your React project's src/ folder
// 2. In src/App.tsx, write:
//      import Chapter4 from './ch4_useEffect';
//      function App() { return <Chapter4 />; }
//      export default App;
// 3. Save and check your browser. Open the console (F12) for extra output.
//
// ============================================================================
//
// WHAT ARE SIDE EFFECTS?
// ======================
// A "side effect" is anything that reaches OUTSIDE of React's rendering system:
//   - Fetching data from an API
//   - Setting up timers (setInterval, setTimeout)
//   - Changing the document title (document.title = ...)
//   - Subscribing to events (window.addEventListener)
//   - Writing to localStorage
//   - Directly modifying the DOM
//
// React components are supposed to be "pure" — given the same props and state,
// they should return the same JSX. Side effects break this purity, so React
// gives us useEffect to handle them in a controlled way.
//
// COMPARE TO PYTHON:
//   Side effects in React are like __init__ (setup) and __del__ (cleanup)
//   in Python classes:
//     class FileHandler:
//         def __init__(self):
//             self.file = open("data.txt")     # <-- side effect (setup)
//         def __del__(self):
//             self.file.close()                 # <-- cleanup
//
//   In React:
//     useEffect(() => {
//         const timer = setInterval(...);       // <-- side effect (setup)
//         return () => clearInterval(timer);    // <-- cleanup
//     }, []);
//
// ============================================================================
//
// useEffect SYNTAX
// ================
//   useEffect(() => {
//     // Side effect code runs AFTER React updates the DOM
//
//     return () => {
//       // Cleanup function (optional) — runs before the effect re-runs
//       // or when the component unmounts (is removed from the page)
//     };
//   }, [dependency1, dependency2]);
//
// THE DEPENDENCY ARRAY (the second argument) is CRUCIAL:
//
//   []          = Run once, when the component first appears (mounts).
//                 Like __init__ in Python. Most common for initial data fetching.
//
//   [value]     = Run once on mount, AND again every time "value" changes.
//                 React compares the old and new value — if different, re-run.
//
//   no array    = Run on EVERY single render. This is almost always a BUG.
//                 (Causes infinite loops if the effect updates state.)
//
// ============================================================================
//
// RULES OF HOOKS
// ==============
// 1. Only call hooks at the TOP LEVEL — not inside if statements, loops,
//    or nested functions. React relies on hooks being called in the same
//    order every render.
//
// 2. Only call hooks in React function components or custom hooks — not
//    in regular JavaScript functions.
//
// These rules exist because React uses the ORDER of hook calls to track
// which useState goes with which state, which useEffect goes with which
// effect, etc. If hooks are called conditionally, the order could change
// between renders, and React would get confused.
//
// ============================================================================

import React, { useState, useEffect } from 'react';

// ---------------------------------------------------------------------------
// BASIC useEffect: Document title update
// ---------------------------------------------------------------------------
function DocumentTitleUpdater() {
  const [count, setCount] = useState(0);

  // This effect runs every time "count" changes.
  // It updates the browser tab title to show the current count.
  useEffect(() => {
    document.title = `Count: ${count}`;
    console.log(`[DocumentTitleUpdater] Effect ran! Count is now ${count}`);

    // No cleanup needed here — we're just setting a string.
  }, [count]); // <-- Dependency array: re-run when count changes

  // This effect runs ONCE on mount (empty dependency array).
  useEffect(() => {
    console.log("[DocumentTitleUpdater] Component mounted! This runs only once.");

    // Cleanup: runs when the component is removed (unmounts)
    return () => {
      console.log("[DocumentTitleUpdater] Component unmounting! Cleanup runs.");
      document.title = "React App"; // Reset the title
    };
  }, []); // <-- Empty array = run once on mount

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Document Title Updater</h3>
      <p>Look at your browser tab title! It shows the count.</p>
      <p>Count: <strong>{count}</strong></p>
      <button onClick={() => setCount(prev => prev + 1)}>Increment</button>
      <button onClick={() => setCount(0)} style={{ marginLeft: '8px' }}>Reset</button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// TIMER with cleanup: setInterval + clearInterval
// ---------------------------------------------------------------------------
function StopWatch() {
  const [seconds, setSeconds] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    // Only set up the interval if the stopwatch is running
    if (!isRunning) return;  // No effect, no cleanup needed

    console.log("[StopWatch] Setting up interval");

    const intervalId = setInterval(() => {
      setSeconds(prev => prev + 1);  // Use updater form! This runs inside a closure.
    }, 1000);

    // CLEANUP: This runs when:
    // 1. isRunning changes (effect will re-run with new isRunning)
    // 2. Component unmounts (removed from page)
    //
    // WHY cleanup matters: Without clearInterval, the timer would keep running
    // even after the component is gone, causing memory leaks and errors.
    return () => {
      console.log("[StopWatch] Cleaning up interval");
      clearInterval(intervalId);
    };
  }, [isRunning]); // Re-run when isRunning changes

  const reset = () => {
    setIsRunning(false);
    setSeconds(0);
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Stopwatch (Timer with Cleanup)</h3>
      <p style={{ fontSize: '32px', fontFamily: 'monospace' }}>
        {Math.floor(seconds / 60).toString().padStart(2, '0')}:
        {(seconds % 60).toString().padStart(2, '0')}
      </p>
      <button onClick={() => setIsRunning(true)}>Start</button>
      <button onClick={() => setIsRunning(false)} style={{ marginLeft: '8px' }}>Pause</button>
      <button onClick={reset} style={{ marginLeft: '8px' }}>Reset</button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// FETCHING DATA: The most common use of useEffect
// ---------------------------------------------------------------------------
// This is the pattern you'll use in almost every real app:
// 1. Start with loading=true
// 2. Fetch data in useEffect
// 3. On success: save data to state, set loading=false
// 4. On error: save error to state, set loading=false
// ---------------------------------------------------------------------------

interface Post {
  id: number;
  title: string;
  body: string;
}

function DataFetcher() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // We can't make the useEffect callback itself async.
    // Instead, define an async function inside and call it immediately.
    // WHY? useEffect expects the return value to be a cleanup function (or undefined).
    // An async function returns a Promise, which would confuse React.

    const fetchPosts = async () => {
      try {
        setLoading(true);
        setError(null);

        // fetch is a built-in browser API for making HTTP requests
        const response = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5');

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data: Post[] = await response.json();
        setPosts(data);
      } catch (err) {
        // err is unknown type in TypeScript, so we check before using
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();   // Call the async function

    // No cleanup needed for a simple fetch.
    // (In production, you might use an AbortController to cancel the fetch on unmount.)
  }, []); // Empty array = run once on mount

  // RENDER PATTERN: loading → error → data
  // This pattern handles all three states cleanly.
  if (loading) {
    return (
      <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
        <h3>Data Fetcher</h3>
        <p>Loading posts...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ border: '1px solid red', padding: '15px', margin: '10px', borderRadius: '8px' }}>
        <h3>Data Fetcher</h3>
        <p style={{ color: 'red' }}>Error: {error}</p>
      </div>
    );
  }

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Data Fetcher (from JSONPlaceholder API)</h3>
      <p>Fetched {posts.length} posts on mount:</p>
      <ul>
        {posts.map(post => (
          <li key={post.id} style={{ marginBottom: '8px' }}>
            <strong>{post.title}</strong>
            <br />
            <span style={{ fontSize: '13px', color: '#666' }}>{post.body.slice(0, 80)}...</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

// ---------------------------------------------------------------------------
// EFFECT WITH CHANGING DEPENDENCY: Fetch data when a value changes
// ---------------------------------------------------------------------------
function UserSearch() {
  const [userId, setUserId] = useState(1);
  const [user, setUser] = useState<{ name: string; email: string } | null>(null);
  const [loading, setLoading] = useState(false);

  // This effect runs EVERY TIME userId changes.
  // When the user clicks a different ID button, we fetch that user's data.
  useEffect(() => {
    let isCancelled = false;  // Flag to prevent updating state after unmount
    // This is called the "cleanup flag" pattern. It prevents a race condition:
    // If userId changes quickly (1 → 2 → 3), the fetch for user 1 might finish
    // AFTER the fetch for user 3 started. Without this flag, old data could
    // overwrite new data.

    const fetchUser = async () => {
      setLoading(true);
      try {
        const response = await fetch(`https://jsonplaceholder.typicode.com/users/${userId}`);
        const data = await response.json();

        if (!isCancelled) {   // Only update if this effect is still relevant
          setUser({ name: data.name, email: data.email });
        }
      } catch {
        if (!isCancelled) {
          setUser(null);
        }
      } finally {
        if (!isCancelled) {
          setLoading(false);
        }
      }
    };

    fetchUser();

    // Cleanup: set the flag so stale responses are ignored
    return () => {
      isCancelled = true;
    };
  }, [userId]); // <-- Re-run whenever userId changes

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Fetch on Dependency Change</h3>
      <p>Click a user ID to fetch their data:</p>
      <div>
        {[1, 2, 3, 4, 5].map(id => (
          <button
            key={id}
            onClick={() => setUserId(id)}
            style={{
              margin: '4px',
              padding: '6px 12px',
              backgroundColor: userId === id ? '#007bff' : '#e0e0e0',
              color: userId === id ? 'white' : 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            User {id}
          </button>
        ))}
      </div>
      {loading && <p>Loading...</p>}
      {user && !loading && (
        <div style={{ marginTop: '10px', padding: '10px', backgroundColor: '#f9f9f9', borderRadius: '4px' }}>
          <p><strong>Name:</strong> {user.name}</p>
          <p><strong>Email:</strong> {user.email}</p>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// WINDOW EVENT LISTENER: Subscribe and unsubscribe
// ---------------------------------------------------------------------------
function WindowSizeTracker() {
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const [windowHeight, setWindowHeight] = useState(window.innerHeight);

  useEffect(() => {
    // Handler function for the resize event
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
      setWindowHeight(window.innerHeight);
    };

    // Subscribe to the event
    window.addEventListener('resize', handleResize);

    // Cleanup: UNSUBSCRIBE when the component unmounts
    // If we don't do this, the event listener keeps running even after
    // the component is removed, which is a memory leak.
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty array = set up once, clean up on unmount

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Window Size Tracker</h3>
      <p>Resize your browser window to see the values change!</p>
      <p>Width: <strong>{windowWidth}px</strong></p>
      <p>Height: <strong>{windowHeight}px</strong></p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// COMMON PITFALL: Infinite loop
// ---------------------------------------------------------------------------
// This component demonstrates what NOT to do.
// Uncomment the bad useEffect to see the infinite loop (it will freeze your browser!).
function InfiniteLoopWarning() {
  const [count, setCount] = useState(0);

  // GOOD: dependency array controls when the effect runs
  useEffect(() => {
    console.log("[InfiniteLoopWarning] This runs once on mount.");
  }, []);

  // BAD - DO NOT UNCOMMENT (infinite loop!):
  // useEffect(() => {
  //   setCount(count + 1);   // Updates state...
  // });                       // No dependency array = runs EVERY render
  //                            // setState causes a re-render → effect runs again
  //                            // → setState again → infinite loop!

  // ALSO BAD (object as dependency):
  // const config = { theme: "dark" };  // New object created every render
  // useEffect(() => {
  //   console.log("Config changed!");
  // }, [config]);  // { theme: "dark" } !== { theme: "dark" } because
  //                // objects are compared by REFERENCE, not by value.
  //                // A new object is created every render → always "different"
  //                // → infinite loop!

  return (
    <div style={{ border: '1px solid orange', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Infinite Loop Warning</h3>
      <p>Count: {count}</p>
      <p style={{ color: 'orange', fontWeight: 'bold' }}>
        Check the source code for examples of what causes infinite loops.
        The bad code is commented out so it doesn't crash your browser.
      </p>
      <p><strong>Common causes of infinite loops:</strong></p>
      <ul>
        <li>No dependency array + setState inside the effect</li>
        <li>Object/array in dependency array (new reference each render)</li>
        <li>Forgetting to include the dependency array entirely</li>
      </ul>
    </div>
  );
}

// ---------------------------------------------------------------------------
// MAIN CHAPTER COMPONENT
// ---------------------------------------------------------------------------
function Chapter4() {
  const [showStopWatch, setShowStopWatch] = useState(true);

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>Chapter 4: useEffect</h1>
      <p><em>useEffect handles side effects: API calls, timers, DOM changes, and more.</em></p>

      <DocumentTitleUpdater />
      <hr />

      {/* Toggle the stopwatch to demonstrate cleanup */}
      <div style={{ margin: '10px', padding: '10px', backgroundColor: '#fffacd' }}>
        <p>Toggle the stopwatch to see cleanup in action (check console):</p>
        <button onClick={() => setShowStopWatch(prev => !prev)}>
          {showStopWatch ? "Hide Stopwatch (triggers cleanup)" : "Show Stopwatch"}
        </button>
      </div>
      {showStopWatch && <StopWatch />}
      <hr />

      <DataFetcher />
      <hr />
      <UserSearch />
      <hr />
      <WindowSizeTracker />
      <hr />
      <InfiniteLoopWarning />

      <footer style={{ backgroundColor: '#f0f0f0', padding: '10px', textAlign: 'center', marginTop: '20px' }}>
        <p>End of Chapter 4 — Next: Events and Forms!</p>
      </footer>
    </div>
  );
}

// ---------------------------------------------------------------------------
// CONSOLE LOG TAKEAWAYS
// ---------------------------------------------------------------------------
console.log(`
============================================================
CHAPTER 4 TAKEAWAYS: useEffect
============================================================

1. useEffect handles SIDE EFFECTS (API calls, timers, subscriptions).
2. Syntax: useEffect(() => { ... return cleanup; }, [deps]);
3. Dependency array controls WHEN the effect runs:
   - []         = once on mount
   - [value]    = on mount + when value changes
   - (omitted)  = every render (usually a bug!)
4. Cleanup function prevents memory leaks (clear timers, unsubscribe).
5. Data fetching pattern:
   - loading/error/data states
   - async function defined INSIDE useEffect
   - isCancelled flag to prevent race conditions
6. NEVER make the useEffect callback itself async.
7. PITFALLS:
   - No deps array + setState = infinite loop
   - Objects in deps = compared by reference, not value
   - Stale closures: old values captured in the effect

PYTHON COMPARISON:
   class Connection:
       def __init__(self):
           self.conn = database.connect()   # setup (useEffect)
       def __del__(self):
           self.conn.close()                # cleanup (return () => ...)

============================================================
`);

export default Chapter4;
export { DocumentTitleUpdater, StopWatch, DataFetcher, UserSearch, WindowSizeTracker };
