// ============================================================================
// CHAPTER 6: LISTS AND CONDITIONAL RENDERING
// ============================================================================
//
// HOW TO USE THIS FILE:
// 1. Copy this file into your React project's src/ folder
// 2. In src/App.tsx, write:
//      import Chapter6 from './ch6_lists_and_conditionals';
//      function App() { return <Chapter6 />; }
//      export default App;
// 3. Save and check your browser.
//
// ============================================================================
//
// RENDERING LISTS
// ===============
// In React, you render lists by using JavaScript's .map() method to
// transform an array of DATA into an array of JSX ELEMENTS.
//
//   const names = ["Alice", "Bob", "Charlie"];
//   return (
//     <ul>
//       {names.map(name => <li key={name}>{name}</li>)}
//     </ul>
//   );
//
// COMPARE TO PYTHON (Jinja2 templates):
//   {% for name in names %}
//     <li>{{ name }}</li>
//   {% endfor %}
//
//   React uses .map() instead of a for-loop because JSX is JavaScript
//   expressions, and .map() returns a value (a new array). A for-loop
//   is a statement and can't be used inside JSX.
//
// ============================================================================
//
// THE KEY PROP — WHY IT MATTERS
// =============================
// Every item in a list MUST have a "key" prop. React uses keys to:
// 1. Track which items have been added, removed, or changed
// 2. Efficiently update only the items that changed (not the whole list)
// 3. Maintain component state correctly when items are reordered
//
// Rules for keys:
// - Must be UNIQUE among siblings (within the same list)
// - Must be STABLE (don't change between renders)
// - Should be from your DATA (like an id), not the array index
//
// WHY NOT USE THE ARRAY INDEX?
//   If you add an item to the beginning of the list, every item's index shifts:
//     Before: [Alice=0, Bob=1, Charlie=2]
//     After:  [Dave=0, Alice=1, Bob=2, Charlie=3]
//   React thinks "index 0" is the same item, but it's now Dave, not Alice.
//   This breaks state and causes bugs. Use a real unique ID instead.
//
//   Exception: if the list is static (never changes), index as key is fine.
//
// ============================================================================
//
// CONDITIONAL RENDERING
// =====================
// React doesn't have a special syntax for if/else in JSX.
// Instead, you use JavaScript expressions:
//
// Pattern 1: Logical AND (show or hide)
//   {isLoggedIn && <Dashboard />}
//   If isLoggedIn is true, render Dashboard. If false, render nothing.
//
// Pattern 2: Ternary (show one OR the other)
//   {isLoggedIn ? <Dashboard /> : <LoginForm />}
//   If true, show Dashboard. If false, show LoginForm.
//
// Pattern 3: Early return (guard clause)
//   if (loading) return <Spinner />;
//   return <MainContent />;
//   Return early before the main JSX.
//
// Pattern 4: Return null (render nothing)
//   if (!shouldShow) return null;
//
// COMPARE TO PYTHON (Jinja2):
//   {% if is_logged_in %}
//     <p>Welcome!</p>
//   {% else %}
//     <p>Please log in.</p>
//   {% endif %}
//
//   Same logic, different syntax.
//
// ============================================================================

import React, { useState } from 'react';

// ---------------------------------------------------------------------------
// BASIC LIST RENDERING: .map() to transform data into JSX
// ---------------------------------------------------------------------------
function BasicList() {
  const fruits: string[] = ["Apple", "Banana", "Cherry", "Date", "Elderberry"];

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Basic List Rendering</h3>
      <ul>
        {/* .map() takes each fruit and returns a <li> for it */}
        {fruits.map((fruit, index) => (
          // key={fruit} — using the fruit name as the key since they're unique
          // For this simple static list, index would work too, but unique data is better
          <li key={fruit}>
            {index + 1}. {fruit}
          </li>
        ))}
      </ul>
      {/*
        How this works step by step:
        1. fruits.map() is called — it returns a new array of JSX elements
        2. ["Apple", "Banana", ...] becomes [<li>Apple</li>, <li>Banana</li>, ...]
        3. React renders the array of elements as children of the <ul>
      */}
    </div>
  );
}

// ---------------------------------------------------------------------------
// LIST OF OBJECTS: Rendering more complex data
// ---------------------------------------------------------------------------
interface Product {
  id: number;      // A real unique ID — perfect for the key prop
  name: string;
  price: number;
  inStock: boolean;
}

function ProductList() {
  const [products] = useState<Product[]>([
    { id: 1, name: "Laptop", price: 999, inStock: true },
    { id: 2, name: "Mouse", price: 29, inStock: true },
    { id: 3, name: "Keyboard", price: 79, inStock: false },
    { id: 4, name: "Monitor", price: 349, inStock: true },
    { id: 5, name: "Webcam", price: 69, inStock: false },
  ]);

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Product List (Objects with IDs)</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #333' }}>
            <th style={{ textAlign: 'left', padding: '8px' }}>Product</th>
            <th style={{ textAlign: 'right', padding: '8px' }}>Price</th>
            <th style={{ textAlign: 'center', padding: '8px' }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {products.map(product => (
            // key={product.id} — ALWAYS use a unique ID from your data
            <tr
              key={product.id}
              style={{
                borderBottom: '1px solid #eee',
                opacity: product.inStock ? 1 : 0.5,
              }}
            >
              <td style={{ padding: '8px' }}>{product.name}</td>
              <td style={{ padding: '8px', textAlign: 'right' }}>${product.price}</td>
              <td style={{ padding: '8px', textAlign: 'center' }}>
                {product.inStock ? "In Stock" : "Out of Stock"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ---------------------------------------------------------------------------
// DYNAMIC LIST: Add, remove, filter items
// ---------------------------------------------------------------------------
interface TodoItem {
  id: number;
  text: string;
  completed: boolean;
}

function DynamicList() {
  const [todos, setTodos] = useState<TodoItem[]>([
    { id: 1, text: "Learn React basics", completed: true },
    { id: 2, text: "Understand props", completed: true },
    { id: 3, text: "Master useState", completed: false },
    { id: 4, text: "Learn useEffect", completed: false },
  ]);
  const [newTodoText, setNewTodoText] = useState("");
  const [nextId, setNextId] = useState(5);  // Simple ID counter
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  // ADD a new todo
  const addTodo = () => {
    if (!newTodoText.trim()) return;
    setTodos(prev => [...prev, { id: nextId, text: newTodoText, completed: false }]);
    setNextId(prev => prev + 1);
    setNewTodoText("");
  };

  // TOGGLE completed status
  const toggleTodo = (id: number) => {
    setTodos(prev => prev.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  };

  // REMOVE a todo
  const removeTodo = (id: number) => {
    setTodos(prev => prev.filter(todo => todo.id !== id));
  };

  // FILTER the list (creates a NEW array — doesn't modify the original)
  const filteredTodos = todos.filter(todo => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true; // 'all'
  });

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Dynamic List (Add/Remove/Filter)</h3>

      {/* Add new todo */}
      <div style={{ marginBottom: '10px', display: 'flex', gap: '8px' }}>
        <input
          type="text"
          value={newTodoText}
          onChange={e => setNewTodoText(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && addTodo()}
          placeholder="Add a new todo..."
          style={{ padding: '6px', flex: 1 }}
        />
        <button onClick={addTodo}>Add</button>
      </div>

      {/* Filter buttons */}
      <div style={{ marginBottom: '10px' }}>
        {(['all', 'active', 'completed'] as const).map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            style={{
              margin: '0 4px',
              padding: '4px 12px',
              backgroundColor: filter === f ? '#007bff' : '#e0e0e0',
              color: filter === f ? 'white' : 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)} ({
              f === 'all' ? todos.length :
              f === 'active' ? todos.filter(t => !t.completed).length :
              todos.filter(t => t.completed).length
            })
          </button>
        ))}
      </div>

      {/* Todo list */}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {filteredTodos.map(todo => (
          <li
            key={todo.id}   // Using the unique id, NOT the array index!
            style={{
              padding: '8px',
              marginBottom: '4px',
              backgroundColor: '#f9f9f9',
              borderRadius: '4px',
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
            }}
          >
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleTodo(todo.id)}
            />
            <span style={{
              flex: 1,
              textDecoration: todo.completed ? 'line-through' : 'none',
              color: todo.completed ? '#999' : '#333',
            }}>
              {todo.text}
            </span>
            <button
              onClick={() => removeTodo(todo.id)}
              style={{ color: 'red', background: 'none', border: 'none', cursor: 'pointer' }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>

      {/* Empty state */}
      {filteredTodos.length === 0 && (
        <p style={{ color: '#999', textAlign: 'center' }}>No todos match this filter.</p>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// CONDITIONAL RENDERING PATTERNS: All the ways to show/hide things
// ---------------------------------------------------------------------------
function ConditionalPatterns() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState<'admin' | 'user' | 'guest'>('guest');
  const [notifications, setNotifications] = useState(3);

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Conditional Rendering Patterns</h3>

      {/* Controls */}
      <div style={{ marginBottom: '15px', padding: '10px', backgroundColor: '#f0f0f0', borderRadius: '4px' }}>
        <button onClick={() => setIsLoggedIn(!isLoggedIn)} style={{ margin: '4px' }}>
          Toggle Login ({isLoggedIn ? 'logged in' : 'logged out'})
        </button>
        <select
          value={userRole}
          onChange={e => setUserRole(e.target.value as 'admin' | 'user' | 'guest')}
          style={{ margin: '4px', padding: '4px' }}
        >
          <option value="admin">Admin</option>
          <option value="user">User</option>
          <option value="guest">Guest</option>
        </select>
        <button onClick={() => setNotifications(prev => prev + 1)} style={{ margin: '4px' }}>
          Add Notification
        </button>
        <button onClick={() => setNotifications(0)} style={{ margin: '4px' }}>
          Clear Notifications
        </button>
      </div>

      {/* Pattern 1: Logical AND — show if true, nothing if false */}
      <div style={{ padding: '5px' }}>
        <strong>Pattern 1 (&&):</strong>{' '}
        {isLoggedIn && <span style={{ color: 'green' }}>Welcome back!</span>}
        {!isLoggedIn && <span style={{ color: 'red' }}>Please log in.</span>}
      </div>

      {/* Pattern 2: Ternary — one thing OR another */}
      <div style={{ padding: '5px' }}>
        <strong>Pattern 2 (ternary):</strong>{' '}
        {isLoggedIn ? (
          <span style={{ color: 'green' }}>Dashboard access granted</span>
        ) : (
          <span style={{ color: 'orange' }}>Login required for dashboard</span>
        )}
      </div>

      {/* Pattern 3: Multiple conditions with ternary chains */}
      <div style={{ padding: '5px' }}>
        <strong>Pattern 3 (role):</strong>{' '}
        {userRole === 'admin' ? (
          <span style={{ color: 'purple' }}>Full admin access</span>
        ) : userRole === 'user' ? (
          <span style={{ color: 'blue' }}>Standard user access</span>
        ) : (
          <span style={{ color: 'gray' }}>Guest — limited access</span>
        )}
      </div>

      {/* Pattern 4: Careful with 0! */}
      <div style={{ padding: '5px' }}>
        <strong>Pattern 4 (notifications):</strong>{' '}
        {/* BAD:  {notifications && <span>...</span>} renders "0" when count is 0 */}
        {/* GOOD: {notifications > 0 && <span>...</span>} renders nothing when 0 */}
        {notifications > 0 && (
          <span style={{ backgroundColor: 'red', color: 'white', padding: '2px 8px', borderRadius: '10px' }}>
            {notifications} new
          </span>
        )}
        {notifications === 0 && <span style={{ color: '#999' }}>No notifications</span>}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// EARLY RETURN PATTERN: Loading/Error/Data states
// ---------------------------------------------------------------------------
interface DataDisplayProps {
  status: 'loading' | 'error' | 'success';
  data?: string[];
  error?: string;
}

function DataDisplay({ status, data, error }: DataDisplayProps) {
  // Early return for loading state
  if (status === 'loading') {
    return (
      <div style={{ padding: '20px', textAlign: 'center', color: '#999' }}>
        Loading data...
      </div>
    );
  }

  // Early return for error state
  if (status === 'error') {
    return (
      <div style={{ padding: '20px', textAlign: 'center', color: 'red' }}>
        Error: {error || 'Something went wrong'}
      </div>
    );
  }

  // Early return if no data
  if (!data || data.length === 0) {
    return (
      <div style={{ padding: '20px', textAlign: 'center', color: '#999' }}>
        No data available.
      </div>
    );
  }

  // Main render — only reached if we have data
  return (
    <ul>
      {data.map(item => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  );
}

function EarlyReturnDemo() {
  const [status, setStatus] = useState<'loading' | 'error' | 'success'>('success');

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Early Return Pattern (Loading/Error/Data)</h3>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => setStatus('loading')} style={{ margin: '4px' }}>Set Loading</button>
        <button onClick={() => setStatus('error')} style={{ margin: '4px' }}>Set Error</button>
        <button onClick={() => setStatus('success')} style={{ margin: '4px' }}>Set Success</button>
      </div>
      <DataDisplay
        status={status}
        data={["React", "TypeScript", "JavaScript"]}
        error="Failed to fetch data"
      />
    </div>
  );
}

// ---------------------------------------------------------------------------
// NESTED LISTS: Rendering lists within lists
// ---------------------------------------------------------------------------
interface Category {
  id: number;
  name: string;
  items: string[];
}

function NestedList() {
  const categories: Category[] = [
    { id: 1, name: "Frontend", items: ["React", "Vue", "Angular"] },
    { id: 2, name: "Backend", items: ["Node.js", "Python", "Go"] },
    { id: 3, name: "Database", items: ["PostgreSQL", "MongoDB", "Redis"] },
  ];

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Nested Lists</h3>
      {categories.map(category => (
        // Outer list: each category. Key from category.id
        <div key={category.id} style={{ marginBottom: '10px' }}>
          <h4 style={{ margin: '5px 0' }}>{category.name}</h4>
          <ul>
            {/* Inner list: items within each category */}
            {category.items.map(item => (
              // Inner key just needs to be unique within THIS list
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// MAIN CHAPTER COMPONENT
// ---------------------------------------------------------------------------
function Chapter6() {
  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>Chapter 6: Lists & Conditional Rendering</h1>
      <p><em>Rendering dynamic lists and showing/hiding UI based on conditions.</em></p>

      <BasicList />
      <hr />
      <ProductList />
      <hr />
      <DynamicList />
      <hr />
      <ConditionalPatterns />
      <hr />
      <EarlyReturnDemo />
      <hr />
      <NestedList />

      <footer style={{ backgroundColor: '#f0f0f0', padding: '10px', textAlign: 'center', marginTop: '20px' }}>
        <p>End of Chapter 6 — Next: Custom Hooks!</p>
      </footer>
    </div>
  );
}

// ---------------------------------------------------------------------------
// CONSOLE LOG TAKEAWAYS
// ---------------------------------------------------------------------------
console.log(`
============================================================
CHAPTER 6 TAKEAWAYS: Lists & Conditional Rendering
============================================================

1. Render lists with .map():
     items.map(item => <li key={item.id}>{item.name}</li>)
2. ALWAYS provide a key prop — unique, stable identifier from your data.
3. Do NOT use array index as key for dynamic lists (reordering breaks).
4. Conditional rendering patterns:
   - {condition && <Component />}     — show or hide
   - {condition ? <A /> : <B />}      — one or the other
   - if (loading) return <Spinner />;  — early return
   - return null;                      — render nothing
5. Watch out for 0: {0 && <div>}</div>} renders "0", not nothing.
   Use: {count > 0 && <div>...</div>}
6. Loading/Error/Data pattern: three states, three early returns.

JINJA2 vs REACT:
   Jinja: {% for item in items %}<li>{{ item }}</li>{% endfor %}
   React: {items.map(item => <li key={...}>{item}</li>)}

   Jinja: {% if logged_in %}<p>Welcome</p>{% endif %}
   React: {loggedIn && <p>Welcome</p>}

============================================================
`);

export default Chapter6;
export { BasicList, ProductList, DynamicList, ConditionalPatterns, EarlyReturnDemo, NestedList };
