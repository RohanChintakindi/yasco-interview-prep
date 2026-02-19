// ============================================================================
// CHAPTER 10: CAPSTONE PROJECT — Full Task Manager Application
// ============================================================================
//
// HOW TO USE THIS FILE:
// 1. Copy this file into your React project's src/ folder
// 2. Make sure react-router-dom is installed: npm install react-router-dom
// 3. In src/App.tsx, write:
//      import Chapter10 from './ch10_project_full_app';
//      function App() { return <Chapter10 />; }
//      export default App;
// 4. Save and check your browser.
//
// ============================================================================
//
// WHAT THIS PROJECT COVERS:
// =========================
// This is a COMPLETE, working Task Manager app that uses everything from
// Chapters 1-9. Every piece is annotated to show which chapter it comes from.
//
// Features:
// - Add, delete, and toggle tasks (Chapter 3: useState)
// - Filter tasks: All / Active / Completed (Chapter 6: lists & conditionals)
// - Persist tasks in localStorage (Chapter 7: custom hooks)
// - Dark/light theme toggle (Chapter 8: Context)
// - Two pages: Tasks and About (Chapter 9: React Router)
// - Full TypeScript types throughout (Chapter 1: setup + TypeScript)
// - Controlled form inputs (Chapter 5: events & forms)
// - Component composition (Chapter 2: props)
// - Side effects for persistence (Chapter 4: useEffect)
//
// All components are in ONE FILE for simplicity. In a real app, you'd split
// them into separate files (one component per file is the convention).
//
// ============================================================================
//
// PROJECT ARCHITECTURE:
// =====================
//   Chapter10 (root)
//   |
//   +-- ThemeProvider (Context — Ch8)
//   |   |
//   |   +-- BrowserRouter (Router — Ch9)
//   |       |
//   |       +-- AppLayout
//   |           |
//   |           +-- AppHeader (props for theme toggle — Ch2)
//   |           |
//   |           +-- Routes
//   |               |
//   |               +-- TasksPage
//   |               |   +-- TaskForm (forms — Ch5)
//   |               |   +-- FilterBar (conditionals — Ch6)
//   |               |   +-- TaskList (lists — Ch6)
//   |               |       +-- TaskItem (props + callbacks — Ch2)
//   |               |
//   |               +-- AboutPage (static page)
//
// ============================================================================

import React, { createContext, useContext, useState, useEffect, useReducer } from 'react';
import { BrowserRouter, Routes, Route, NavLink, Outlet } from 'react-router-dom';

// ===========================================================================
// TYPES (TypeScript — covered since Chapter 1)
// ===========================================================================
// Define the data shapes used throughout the app.
// This is one of TypeScript's biggest benefits: you define the shape ONCE,
// and every component that uses this data gets type checking and autocomplete.
// ===========================================================================

interface Task {
  id: number;
  text: string;
  completed: boolean;
  createdAt: string;    // ISO date string
}

type FilterType = 'all' | 'active' | 'completed';

// ===========================================================================
// CUSTOM HOOK: useLocalStorage (Chapter 7)
// ===========================================================================
// Reusing the custom hook from Chapter 7 to persist tasks and theme.
// When the user refreshes the page, their tasks and theme preference are preserved.
// ===========================================================================
function useLocalStorage<T>(key: string, initialValue: T): [T, React.Dispatch<React.SetStateAction<T>>] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      console.error('localStorage write error:', error);
    }
  }, [key, storedValue]);

  return [storedValue, setStoredValue];
}

// ===========================================================================
// THEME CONTEXT (Chapter 8)
// ===========================================================================
// The theme (dark/light) is provided via Context so any component can
// access it without prop drilling. The theme preference is also persisted
// in localStorage.
// ===========================================================================

interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
  colors: {
    bg: string;
    surface: string;
    text: string;
    textSecondary: string;
    primary: string;
    border: string;
    danger: string;
    success: string;
  };
}

const ThemeContext = createContext<ThemeContextType | null>(null);

function useTheme(): ThemeContextType {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider');
  return ctx;
}

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('task_app_theme', 'light');

  const toggleTheme = () => setTheme(prev => prev === 'light' ? 'dark' : 'light');

  // Define color palettes for each theme
  const lightColors = {
    bg: '#f5f5f5', surface: '#ffffff', text: '#333333', textSecondary: '#666666',
    primary: '#007bff', border: '#dddddd', danger: '#dc3545', success: '#28a745',
  };
  const darkColors = {
    bg: '#1a1a2e', surface: '#16213e', text: '#e0e0e0', textSecondary: '#a0a0a0',
    primary: '#4dabf7', border: '#333355', danger: '#ff6b6b', success: '#51cf66',
  };

  const colors = theme === 'light' ? lightColors : darkColors;

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, colors }}>
      {children}
    </ThemeContext.Provider>
  );
}

// ===========================================================================
// TASK REDUCER (Chapter 8: useReducer)
// ===========================================================================
// All task state transitions are managed by a reducer.
// This keeps state logic centralized and predictable.
// ===========================================================================

type TaskAction =
  | { type: 'add'; payload: string }
  | { type: 'toggle'; payload: number }
  | { type: 'remove'; payload: number }
  | { type: 'clearCompleted' }
  | { type: 'load'; payload: Task[] };

function taskReducer(state: Task[], action: TaskAction): Task[] {
  switch (action.type) {
    case 'add':
      const newId = state.length > 0 ? Math.max(...state.map(t => t.id)) + 1 : 1;
      return [
        ...state,
        {
          id: newId,
          text: action.payload,
          completed: false,
          createdAt: new Date().toISOString(),
        },
      ];
    case 'toggle':
      return state.map(task =>
        task.id === action.payload ? { ...task, completed: !task.completed } : task
      );
    case 'remove':
      return state.filter(task => task.id !== action.payload);
    case 'clearCompleted':
      return state.filter(task => !task.completed);
    case 'load':
      return action.payload;
    default:
      return state;
  }
}

// ===========================================================================
// HEADER COMPONENT (Chapter 2: Props)
// ===========================================================================
// Receives the task count as props and uses theme from Context.
// Demonstrates: props, context, NavLink (from Chapter 9).
// ===========================================================================

interface AppHeaderProps {
  totalTasks: number;
  completedTasks: number;
}

function AppHeader({ totalTasks, completedTasks }: AppHeaderProps) {
  const { theme, toggleTheme, colors } = useTheme();

  const navLinkStyle = ({ isActive }: { isActive: boolean }): React.CSSProperties => ({
    textDecoration: 'none',
    padding: '6px 14px',
    borderRadius: '4px',
    color: isActive ? 'white' : colors.text,
    backgroundColor: isActive ? colors.primary : 'transparent',
    fontWeight: isActive ? 'bold' : 'normal',
    fontSize: '14px',
  });

  return (
    <header style={{
      backgroundColor: colors.surface,
      padding: '15px 20px',
      borderBottom: `2px solid ${colors.border}`,
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      flexWrap: 'wrap',
      gap: '10px',
    }}>
      <div>
        <h1 style={{ margin: 0, fontSize: '22px', color: colors.text }}>
          Task Manager
        </h1>
        <p style={{ margin: '4px 0 0', fontSize: '13px', color: colors.textSecondary }}>
          {completedTasks}/{totalTasks} completed
        </p>
      </div>

      <nav style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
        <NavLink to="/" style={navLinkStyle} end>Tasks</NavLink>
        <NavLink to="/about" style={navLinkStyle}>About</NavLink>
        <button
          onClick={toggleTheme}
          style={{
            marginLeft: '10px',
            padding: '6px 12px',
            border: `1px solid ${colors.border}`,
            borderRadius: '4px',
            backgroundColor: colors.surface,
            color: colors.text,
            cursor: 'pointer',
            fontSize: '14px',
          }}
        >
          {theme === 'light' ? 'Dark' : 'Light'} Mode
        </button>
      </nav>
    </header>
  );
}

// ===========================================================================
// TASK FORM COMPONENT (Chapter 5: Events & Forms)
// ===========================================================================
// A controlled form for adding new tasks.
// Demonstrates: controlled input, onSubmit, preventDefault, form validation.
// ===========================================================================

interface TaskFormProps {
  onAddTask: (text: string) => void;
}

function TaskForm({ onAddTask }: TaskFormProps) {
  const [text, setText] = useState('');
  const { colors } = useTheme();

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();  // Prevent page reload (Ch5)
    const trimmed = text.trim();
    if (!trimmed) return;
    onAddTask(trimmed);    // Callback prop to parent (Ch2)
    setText('');            // Reset form
  };

  return (
    <form onSubmit={handleSubmit} style={{
      display: 'flex',
      gap: '8px',
      marginBottom: '15px',
    }}>
      <input
        type="text"
        value={text}                              // Controlled input (Ch5)
        onChange={e => setText(e.target.value)}    // Update state on change (Ch5)
        placeholder="What needs to be done?"
        style={{
          flex: 1,
          padding: '10px 14px',
          fontSize: '16px',
          border: `1px solid ${colors.border}`,
          borderRadius: '6px',
          backgroundColor: colors.surface,
          color: colors.text,
          outline: 'none',
        }}
      />
      <button
        type="submit"
        disabled={!text.trim()}   // Disable when empty
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: text.trim() ? colors.primary : colors.border,
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: text.trim() ? 'pointer' : 'not-allowed',
        }}
      >
        Add Task
      </button>
    </form>
  );
}

// ===========================================================================
// FILTER BAR COMPONENT (Chapter 6: Conditionals)
// ===========================================================================

interface FilterBarProps {
  currentFilter: FilterType;
  onFilterChange: (filter: FilterType) => void;
  counts: { all: number; active: number; completed: number };
  onClearCompleted: () => void;
}

function FilterBar({ currentFilter, onFilterChange, counts, onClearCompleted }: FilterBarProps) {
  const { colors } = useTheme();
  const filters: FilterType[] = ['all', 'active', 'completed'];

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '10px',
      flexWrap: 'wrap',
      gap: '8px',
    }}>
      <div style={{ display: 'flex', gap: '4px' }}>
        {filters.map(f => (
          <button
            key={f}
            onClick={() => onFilterChange(f)}  // Callback prop (Ch2)
            style={{
              padding: '5px 12px',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              backgroundColor: currentFilter === f ? colors.primary : colors.surface,
              color: currentFilter === f ? 'white' : colors.text,
              borderWidth: '1px',
              borderStyle: 'solid',
              borderColor: currentFilter === f ? colors.primary : colors.border,
              fontSize: '13px',
            }}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)} ({counts[f]})
          </button>
        ))}
      </div>
      {/* Conditional rendering (Ch6): only show clear button if there are completed tasks */}
      {counts.completed > 0 && (
        <button
          onClick={onClearCompleted}
          style={{
            padding: '5px 12px',
            fontSize: '13px',
            backgroundColor: 'transparent',
            color: colors.danger,
            border: `1px solid ${colors.danger}`,
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Clear Completed ({counts.completed})
        </button>
      )}
    </div>
  );
}

// ===========================================================================
// TASK ITEM COMPONENT (Chapter 2: Props + Callbacks)
// ===========================================================================
// A single task item. Receives data and callbacks as props.
// ===========================================================================

interface TaskItemProps {
  task: Task;
  onToggle: (id: number) => void;
  onRemove: (id: number) => void;
}

function TaskItem({ task, onToggle, onRemove }: TaskItemProps) {
  const { colors } = useTheme();

  // Format the date (side computation, not a side effect)
  const formattedDate = new Date(task.createdAt).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
  });

  return (
    <li style={{
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      padding: '12px 15px',
      backgroundColor: colors.surface,
      borderRadius: '6px',
      marginBottom: '6px',
      border: `1px solid ${colors.border}`,
      transition: 'opacity 0.2s',
      opacity: task.completed ? 0.6 : 1,
    }}>
      {/* Checkbox to toggle completion */}
      <input
        type="checkbox"
        checked={task.completed}                  // Controlled (Ch5)
        onChange={() => onToggle(task.id)}         // Callback to parent (Ch2)
        style={{ width: '18px', height: '18px', cursor: 'pointer' }}
      />

      {/* Task text */}
      <div style={{ flex: 1 }}>
        <span style={{
          textDecoration: task.completed ? 'line-through' : 'none',
          color: task.completed ? colors.textSecondary : colors.text,
          fontSize: '16px',
        }}>
          {task.text}
        </span>
        <br />
        <span style={{ fontSize: '12px', color: colors.textSecondary }}>
          {formattedDate}
        </span>
      </div>

      {/* Delete button */}
      <button
        onClick={() => onRemove(task.id)}       // Callback to parent (Ch2)
        style={{
          background: 'none',
          border: 'none',
          color: colors.danger,
          fontSize: '18px',
          cursor: 'pointer',
          padding: '4px 8px',
          borderRadius: '4px',
        }}
        title="Delete task"
      >
        X
      </button>
    </li>
  );
}

// ===========================================================================
// TASK LIST COMPONENT (Chapter 6: Lists)
// ===========================================================================

interface TaskListProps {
  tasks: Task[];
  onToggle: (id: number) => void;
  onRemove: (id: number) => void;
}

function TaskList({ tasks, onToggle, onRemove }: TaskListProps) {
  const { colors } = useTheme();

  // Conditional rendering (Ch6): show empty state if no tasks
  if (tasks.length === 0) {
    return (
      <div style={{
        textAlign: 'center',
        padding: '40px 20px',
        color: colors.textSecondary,
      }}>
        <p style={{ fontSize: '18px' }}>No tasks to show</p>
        <p style={{ fontSize: '14px' }}>Add a task above or change the filter.</p>
      </div>
    );
  }

  return (
    <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
      {/* List rendering with .map() (Ch6) — key is the unique task id */}
      {tasks.map(task => (
        <TaskItem
          key={task.id}           // Key prop for list items (Ch6)
          task={task}             // Data prop (Ch2)
          onToggle={onToggle}    // Callback prop (Ch2)
          onRemove={onRemove}    // Callback prop (Ch2)
        />
      ))}
    </ul>
  );
}

// ===========================================================================
// TASKS PAGE: Main task management view
// ===========================================================================
// This page composes all the task-related components together.
// It owns the task state and passes data/callbacks down via props.
// This is the "lifting state up" pattern from Chapter 2.
// ===========================================================================

interface TasksPageProps {
  tasks: Task[];
  dispatch: React.Dispatch<TaskAction>;
}

function TasksPage({ tasks, dispatch }: TasksPageProps) {
  const [filter, setFilter] = useState<FilterType>('all');
  const { colors } = useTheme();

  // Derived data: compute filtered list and counts from the task state
  // These aren't separate state — they're computed from the existing state.
  // This is a key React pattern: derive what you can, don't duplicate state.
  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  });

  const counts = {
    all: tasks.length,
    active: tasks.filter(t => !t.completed).length,
    completed: tasks.filter(t => t.completed).length,
  };

  return (
    <div style={{ padding: '20px' }}>
      <TaskForm onAddTask={(text) => dispatch({ type: 'add', payload: text })} />
      <FilterBar
        currentFilter={filter}
        onFilterChange={setFilter}
        counts={counts}
        onClearCompleted={() => dispatch({ type: 'clearCompleted' })}
      />
      <TaskList
        tasks={filteredTasks}
        onToggle={(id) => dispatch({ type: 'toggle', payload: id })}
        onRemove={(id) => dispatch({ type: 'remove', payload: id })}
      />

      {/* Stats footer */}
      {tasks.length > 0 && (
        <div style={{
          marginTop: '15px',
          padding: '10px',
          fontSize: '13px',
          color: colors.textSecondary,
          textAlign: 'center',
          borderTop: `1px solid ${colors.border}`,
        }}>
          {counts.active} task{counts.active !== 1 ? 's' : ''} remaining
          {' | '}
          {counts.completed} completed
        </div>
      )}
    </div>
  );
}

// ===========================================================================
// ABOUT PAGE (Chapter 9: React Router)
// ===========================================================================

function AboutPage() {
  const { colors } = useTheme();

  const chapterList = [
    "Ch1: JSX & Components",
    "Ch2: Props & Callbacks",
    "Ch3: State & useState",
    "Ch4: useEffect & Side Effects",
    "Ch5: Events & Forms",
    "Ch6: Lists & Conditional Rendering",
    "Ch7: Custom Hooks",
    "Ch8: Context & useReducer",
    "Ch9: React Router",
    "Ch10: This Capstone Project",
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h2 style={{ color: colors.text }}>About This App</h2>
      <p style={{ color: colors.textSecondary }}>
        This Task Manager is the capstone project for the React course.
        It demonstrates every concept from Chapters 1-9 in a single, working app.
      </p>

      <div style={{
        backgroundColor: colors.surface,
        border: `1px solid ${colors.border}`,
        borderRadius: '8px',
        padding: '20px',
        marginTop: '15px',
      }}>
        <h3 style={{ color: colors.text, marginTop: 0 }}>Concepts Used:</h3>
        <ul style={{ color: colors.text }}>
          {chapterList.map(ch => (
            <li key={ch} style={{ marginBottom: '6px' }}>{ch}</li>
          ))}
        </ul>
      </div>

      <div style={{
        backgroundColor: colors.surface,
        border: `1px solid ${colors.border}`,
        borderRadius: '8px',
        padding: '20px',
        marginTop: '15px',
      }}>
        <h3 style={{ color: colors.text, marginTop: 0 }}>Features:</h3>
        <ul style={{ color: colors.text }}>
          <li>Add, toggle, and delete tasks</li>
          <li>Filter by All / Active / Completed</li>
          <li>Clear all completed tasks at once</li>
          <li>Dark / Light theme toggle (persisted)</li>
          <li>All data saved in localStorage (survives refresh)</li>
          <li>Two pages with client-side routing</li>
          <li>Full TypeScript throughout</li>
        </ul>
      </div>
    </div>
  );
}

// ===========================================================================
// APP LAYOUT (Chapter 9: Outlet pattern)
// ===========================================================================

interface AppLayoutProps {
  totalTasks: number;
  completedTasks: number;
}

function AppLayout({ totalTasks, completedTasks }: AppLayoutProps) {
  const { colors } = useTheme();

  return (
    <div style={{
      backgroundColor: colors.bg,
      minHeight: '100vh',
      transition: 'background-color 0.3s',
    }}>
      <div style={{ maxWidth: '700px', margin: '0 auto' }}>
        <AppHeader totalTasks={totalTasks} completedTasks={completedTasks} />
        {/* Outlet renders the matched child route (Ch9) */}
        <Outlet />
      </div>
    </div>
  );
}

// ===========================================================================
// ROOT COMPONENT: Wires everything together
// ===========================================================================
// This is the entry point. It sets up:
// 1. ThemeProvider (Context) wrapping the entire app
// 2. useReducer for task state management
// 3. useEffect for localStorage persistence
// 4. BrowserRouter for routing
// 5. All routes pointing to their respective pages
// ===========================================================================

function Chapter10() {
  // Load initial tasks from localStorage (Ch7: custom hook concept, done inline here)
  const getInitialTasks = (): Task[] => {
    try {
      const saved = window.localStorage.getItem('task_app_tasks');
      if (saved) return JSON.parse(saved);
    } catch { /* ignore parse errors */ }
    // Default tasks for first-time users
    return [
      { id: 1, text: "Learn React fundamentals", completed: true, createdAt: new Date().toISOString() },
      { id: 2, text: "Build a project with React", completed: false, createdAt: new Date().toISOString() },
      { id: 3, text: "Explore advanced patterns", completed: false, createdAt: new Date().toISOString() },
    ];
  };

  // useReducer manages ALL task state transitions (Ch8)
  const [tasks, dispatch] = useReducer(taskReducer, null, () => getInitialTasks());
  // The third argument is a lazy initializer — it runs once to set the initial state.
  // This prevents reading localStorage on every re-render.

  // useEffect persists tasks to localStorage whenever they change (Ch4)
  useEffect(() => {
    try {
      window.localStorage.setItem('task_app_tasks', JSON.stringify(tasks));
    } catch (error) {
      console.error('Failed to save tasks:', error);
    }
  }, [tasks]);

  const completedCount = tasks.filter(t => t.completed).length;

  return (
    // ThemeProvider wraps everything — any descendant can use useTheme() (Ch8)
    <ThemeProvider>
      {/* BrowserRouter enables client-side routing (Ch9) */}
      <BrowserRouter>
        <Routes>
          {/* Layout route wraps all pages with the header (Ch9: Outlet) */}
          <Route element={<AppLayout totalTasks={tasks.length} completedTasks={completedCount} />}>
            {/* Tasks page is the default (index) route */}
            <Route index element={<TasksPage tasks={tasks} dispatch={dispatch} />} />
            <Route path="/about" element={<AboutPage />} />
            {/* 404 catch-all (Ch9) */}
            <Route path="*" element={
              <div style={{ padding: '40px', textAlign: 'center' }}>
                <h2>404 — Page Not Found</h2>
                <p>This page does not exist in the Task Manager app.</p>
              </div>
            } />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

// ---------------------------------------------------------------------------
// CONSOLE LOG TAKEAWAYS
// ---------------------------------------------------------------------------
console.log(`
============================================================
CHAPTER 10: CAPSTONE PROJECT — Task Manager
============================================================

This app demonstrates EVERY concept from the course:

ARCHITECTURE DECISIONS AND WHY:
1. TypeScript interfaces for Task, FilterType, etc.
   WHY: Type safety catches bugs at compile time, not runtime.

2. useReducer for task state (not useState).
   WHY: Multiple actions (add, toggle, remove, clear) on the same state.
   A reducer centralizes all transitions in one pure function.

3. Context for theme (not prop drilling).
   WHY: Theme is used by almost every component at every level.
   Prop drilling would be tedious. Context makes it accessible everywhere.

4. localStorage via useEffect (not on every render).
   WHY: localStorage is synchronous and slow. useEffect runs AFTER render,
   so it doesn't block the UI. The dependency array ensures we only write
   when tasks actually change.

5. Derived state for filtered tasks (not separate state).
   WHY: filteredTasks = tasks.filter(...) is computed from existing state.
   Storing it separately would risk it getting out of sync.

6. Callback props for child-to-parent communication.
   WHY: One-way data flow. Parent owns the state, passes dispatch down.
   Children don't directly modify state — they tell the parent what happened.

7. React Router for multi-page feel.
   WHY: SPA navigation without page reloads. URL-based routing means
   users can bookmark and share pages.

WHAT TO BUILD NEXT:
- Add due dates and priority levels
- Add edit/rename functionality
- Add categories or tags
- Connect to a real backend API (replace localStorage with fetch)
- Add user authentication
- Deploy to Vercel or Netlify

============================================================
`);

export default Chapter10;
export { ThemeProvider, useTheme, TaskForm, FilterBar, TaskItem, TaskList, TasksPage };
