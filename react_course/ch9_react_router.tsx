// ============================================================================
// CHAPTER 9: REACT ROUTER — Navigation and Routing
// ============================================================================
//
// HOW TO USE THIS FILE:
// 1. Copy this file into your React project's src/ folder
// 2. Install React Router: npm install react-router-dom
// 3. In src/App.tsx, write:
//      import Chapter9 from './ch9_react_router';
//      function App() { return <Chapter9 />; }
//      export default App;
// 4. Save and check your browser.
//
// IMPORTANT: This chapter REQUIRES react-router-dom to be installed.
// Run: npm install react-router-dom
// For TypeScript types (if needed): npm install @types/react-router-dom
// (Recent versions of react-router-dom include types, so this may not be needed.)
//
// ============================================================================
//
// WHAT IS ROUTING?
// ================
// In a traditional website, clicking a link sends a request to the server,
// which returns a new HTML page. The browser reloads completely.
//
// In a React SPA (Single Page Application), there's only ONE HTML page.
// "Routing" means showing different components based on the URL, without
// a page reload. The URL changes, React renders a different component,
// but the page never actually reloads. It's all client-side.
//
// COMPARE TO FLASK:
//   Flask:
//     @app.route("/")
//     def home(): return render_template("home.html")
//
//     @app.route("/about")
//     def about(): return render_template("about.html")
//
//     @app.route("/user/<int:id>")
//     def user(id): return render_template("user.html", id=id)
//
//   React Router:
//     <Route path="/" element={<Home />} />
//     <Route path="/about" element={<About />} />
//     <Route path="/user/:id" element={<UserProfile />} />
//
//   Same concept — URL maps to a view. But Flask runs on the server,
//   React Router runs in the browser.
//
// KEY CONCEPTS:
// - BrowserRouter: wraps your app, enables routing
// - Routes: container for all your Route definitions
// - Route: maps a URL path to a component
// - Link: navigate without page reload (use instead of <a>)
// - useParams: read URL parameters (/user/:id → id)
// - useNavigate: navigate programmatically (redirect after form submit)
// - useSearchParams: read/write query strings (?search=react)
// - Outlet: render child routes inside a parent layout
//
// ============================================================================
//
// WHY NOT USE <a> TAGS?
// =====================
// Regular <a href="/about"> causes a FULL PAGE RELOAD. The browser sends
// a new HTTP request, your React app re-initializes from scratch, and all
// component state is lost.
//
// React Router's <Link to="/about"> intercepts the click, updates the URL
// using the browser's History API, and renders the new component — all
// without a page reload. Your app's state is preserved.
//
// Rule: Use <Link> for internal navigation, <a> for external links.
//
// ============================================================================

import React, { useState } from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  NavLink,
  useParams,
  useNavigate,
  useSearchParams,
  Outlet,
  Navigate,
} from 'react-router-dom';

// ---------------------------------------------------------------------------
// NAVIGATION BAR: Using Link and NavLink
// ---------------------------------------------------------------------------
// NavLink is like Link but adds an "active" class/style when the current
// URL matches its "to" prop. Perfect for navigation menus.
// ---------------------------------------------------------------------------
function Navbar() {
  // NavLink's style prop can be a function that receives { isActive }
  const navStyle = ({ isActive }: { isActive: boolean }): React.CSSProperties => ({
    padding: '8px 16px',
    textDecoration: 'none',
    color: isActive ? 'white' : '#333',
    backgroundColor: isActive ? '#007bff' : 'transparent',
    borderRadius: '4px',
    marginRight: '8px',
    fontWeight: isActive ? 'bold' : 'normal',
  });

  return (
    <nav style={{
      backgroundColor: '#f0f0f0',
      padding: '10px',
      borderRadius: '8px',
      marginBottom: '20px',
      display: 'flex',
      flexWrap: 'wrap',
      gap: '4px',
    }}>
      {/* NavLink highlights the active link automatically */}
      <NavLink to="/" style={navStyle} end>
        Home
      </NavLink>
      {/* "end" prop means this only matches exactly "/", not "/about" etc. */}

      <NavLink to="/about" style={navStyle}>About</NavLink>
      <NavLink to="/users" style={navStyle}>Users</NavLink>
      <NavLink to="/search" style={navStyle}>Search</NavLink>
      <NavLink to="/dashboard" style={navStyle}>Dashboard</NavLink>
      <NavLink to="/nonexistent" style={navStyle}>404 Demo</NavLink>
    </nav>
  );
}

// ---------------------------------------------------------------------------
// PAGE COMPONENTS: Each one is shown for a different URL
// ---------------------------------------------------------------------------

function HomePage() {
  return (
    <div style={{ padding: '20px' }}>
      <h2>Home Page</h2>
      <p>Welcome to the React Router demo! Click the navigation links above.</p>
      <p>This component renders when the URL is exactly "/".</p>

      <div style={{ marginTop: '15px', padding: '15px', backgroundColor: '#e8f4fd', borderRadius: '8px' }}>
        <h4>How This Router Works:</h4>
        <ul>
          <li><strong>Home (/)</strong> — This page</li>
          <li><strong>About (/about)</strong> — Static page</li>
          <li><strong>Users (/users)</strong> — List with links to individual user pages</li>
          <li><strong>User Detail (/users/:id)</strong> — Dynamic route with URL parameter</li>
          <li><strong>Search (/search)</strong> — Query string parameters demo</li>
          <li><strong>Dashboard (/dashboard)</strong> — Protected route (login required)</li>
          <li><strong>404</strong> — Catch-all for unknown URLs</li>
        </ul>
      </div>
    </div>
  );
}

function AboutPage() {
  return (
    <div style={{ padding: '20px' }}>
      <h2>About Page</h2>
      <p>This is a simple static page. It renders when the URL is "/about".</p>
      <p>
        In Flask, this would be:
        <code style={{ backgroundColor: '#f0f0f0', padding: '2px 6px' }}>
          @app.route("/about")
        </code>
      </p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// USER LIST: Links to individual user pages (dynamic routes)
// ---------------------------------------------------------------------------
interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

const MOCK_USERS: User[] = [
  { id: 1, name: "Alice Johnson", email: "alice@example.com", role: "Developer" },
  { id: 2, name: "Bob Smith", email: "bob@example.com", role: "Designer" },
  { id: 3, name: "Charlie Brown", email: "charlie@example.com", role: "Manager" },
  { id: 4, name: "Diana Prince", email: "diana@example.com", role: "Developer" },
];

function UsersPage() {
  return (
    <div style={{ padding: '20px' }}>
      <h2>Users</h2>
      <p>Click a user to see their details (using URL parameters):</p>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {MOCK_USERS.map(user => (
          <li key={user.id} style={{ marginBottom: '8px' }}>
            {/* Link navigates without page reload */}
            <Link
              to={`/users/${user.id}`}
              style={{
                textDecoration: 'none',
                color: '#007bff',
                padding: '8px 12px',
                display: 'inline-block',
                backgroundColor: '#f0f0f0',
                borderRadius: '4px',
              }}
            >
              {user.name} — {user.role}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

// ---------------------------------------------------------------------------
// USER DETAIL: Dynamic route with useParams
// ---------------------------------------------------------------------------
// URL: /users/3 → useParams() returns { id: "3" }
// Compare to Flask: @app.route("/users/<int:id>") → id parameter
// ---------------------------------------------------------------------------
function UserDetailPage() {
  // useParams extracts URL parameters defined in the Route path.
  // Route path="/users/:id" → useParams() returns { id: string }
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();  // For programmatic navigation

  // Find the user (in a real app, you'd fetch from an API)
  const user = MOCK_USERS.find(u => u.id === Number(id));

  if (!user) {
    return (
      <div style={{ padding: '20px' }}>
        <h2>User Not Found</h2>
        <p>No user with ID {id}.</p>
        {/* useNavigate for programmatic navigation — like redirect() in Flask */}
        <button onClick={() => navigate('/users')}>Back to Users</button>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px' }}>
      <h2>User Detail: {user.name}</h2>
      <div style={{ padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
        <p><strong>ID:</strong> {user.id}</p>
        <p><strong>Name:</strong> {user.name}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Role:</strong> {user.role}</p>
      </div>
      <div style={{ marginTop: '15px' }}>
        {/* navigate(-1) goes back one page in history (like browser back button) */}
        <button onClick={() => navigate(-1)}>Go Back</button>
        <button onClick={() => navigate('/users')} style={{ marginLeft: '8px' }}>
          All Users
        </button>
        {/* Navigate to next user */}
        {user.id < MOCK_USERS.length && (
          <button onClick={() => navigate(`/users/${user.id + 1}`)} style={{ marginLeft: '8px' }}>
            Next User
          </button>
        )}
      </div>

      <p style={{ fontSize: '13px', color: '#666', marginTop: '15px' }}>
        The URL parameter ":id" = {id}. Extracted with useParams().
        <br />
        Flask equivalent: @app.route("/users/&lt;int:id&gt;")
      </p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// SEARCH PAGE: useSearchParams for query strings
// ---------------------------------------------------------------------------
// URL: /search?q=react&category=frontend
// useSearchParams reads and writes these query parameters.
// Compare to Flask: request.args.get("q") and request.args.get("category")
// ---------------------------------------------------------------------------
function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();

  // Read current query params
  const query = searchParams.get('q') || '';
  const category = searchParams.get('category') || 'all';

  const categories = ['all', 'frontend', 'backend', 'devops'];

  // Simulated search results
  const allResults = [
    { title: "React Basics", category: "frontend" },
    { title: "TypeScript Guide", category: "frontend" },
    { title: "Node.js API", category: "backend" },
    { title: "Python Flask", category: "backend" },
    { title: "Docker Setup", category: "devops" },
    { title: "CSS Flexbox", category: "frontend" },
  ];

  const filteredResults = allResults.filter(r => {
    const matchesQuery = !query || r.title.toLowerCase().includes(query.toLowerCase());
    const matchesCategory = category === 'all' || r.category === category;
    return matchesQuery && matchesCategory;
  });

  return (
    <div style={{ padding: '20px' }}>
      <h2>Search (Query Parameters)</h2>
      <p style={{ fontSize: '13px', color: '#666' }}>
        Current URL params: ?q={query}&category={category}
      </p>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '15px', flexWrap: 'wrap' }}>
        <input
          type="text"
          value={query}
          onChange={e => {
            // setSearchParams updates the URL query string
            setSearchParams({ q: e.target.value, category });
          }}
          placeholder="Search..."
          style={{ padding: '8px', flex: 1, minWidth: '200px' }}
        />
        <select
          value={category}
          onChange={e => setSearchParams({ q: query, category: e.target.value })}
          style={{ padding: '8px' }}
        >
          {categories.map(c => (
            <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>
          ))}
        </select>
      </div>

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {filteredResults.map(r => (
          <li key={r.title} style={{
            padding: '8px',
            backgroundColor: '#f9f9f9',
            marginBottom: '4px',
            borderRadius: '4px',
          }}>
            <strong>{r.title}</strong>
            <span style={{ color: '#666', marginLeft: '10px' }}>({r.category})</span>
          </li>
        ))}
        {filteredResults.length === 0 && (
          <p style={{ color: '#999' }}>No results found.</p>
        )}
      </ul>
    </div>
  );
}

// ---------------------------------------------------------------------------
// PROTECTED ROUTE: Redirect if not authenticated
// ---------------------------------------------------------------------------
// This is a very common pattern: some pages require login.
// If the user isn't logged in, redirect them to the login page.
// Compare to Flask: @login_required decorator
// ---------------------------------------------------------------------------

function ProtectedRoute({ isLoggedIn, children }: { isLoggedIn: boolean; children: React.ReactNode }) {
  // If not logged in, redirect to home (or a login page)
  if (!isLoggedIn) {
    // <Navigate> is a component that redirects immediately when rendered.
    // replace prevents the redirect from being added to browser history
    // (so the back button doesn't go to the protected page).
    return <Navigate to="/" replace />;
  }
  return <>{children}</>;
}

function DashboardPage() {
  return (
    <div style={{ padding: '20px' }}>
      <h2>Dashboard (Protected)</h2>
      <p style={{ color: 'green' }}>You are logged in and can see this page!</p>
      <div style={{ padding: '15px', backgroundColor: '#f0fff0', borderRadius: '8px' }}>
        <h4>Your Stats:</h4>
        <p>Projects: 5</p>
        <p>Tasks completed: 42</p>
        <p>Streak: 7 days</p>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// LAYOUT WITH OUTLET: Nested routes
// ---------------------------------------------------------------------------
// Outlet is a placeholder where child routes render.
// This lets you create a persistent layout (header + footer) that wraps
// all pages, with only the middle part changing.
//
// Compare to Flask/Jinja:
//   {% extends "base.html" %}
//   {% block content %}...{% endblock %}
//
// The layout is like base.html, and <Outlet /> is like {% block content %}.
// ---------------------------------------------------------------------------
function Layout() {
  return (
    <div>
      <Navbar />
      {/* Outlet renders whatever child Route matches the current URL */}
      <Outlet />
    </div>
  );
}

// ---------------------------------------------------------------------------
// 404 PAGE: Catch-all for unknown routes
// ---------------------------------------------------------------------------
function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h2 style={{ fontSize: '48px', color: '#999' }}>404</h2>
      <p>Page not found!</p>
      <p>The URL you requested doesn't match any route.</p>
      <button onClick={() => navigate('/')}>Go Home</button>
      <p style={{ fontSize: '13px', color: '#666', marginTop: '15px' }}>
        In the Route config, path="*" catches everything that didn't match above.
      </p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// MAIN CHAPTER COMPONENT: Putting it all together
// ---------------------------------------------------------------------------
function Chapter9() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>Chapter 9: React Router</h1>
      <p><em>Navigate between pages without reloading — client-side routing.</em></p>

      {/* Login toggle for the protected route demo */}
      <div style={{
        padding: '10px',
        backgroundColor: isLoggedIn ? '#d4edda' : '#f8d7da',
        borderRadius: '8px',
        marginBottom: '15px',
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
      }}>
        <span>{isLoggedIn ? 'Logged in' : 'Logged out'} — </span>
        <button onClick={() => setIsLoggedIn(!isLoggedIn)}>
          {isLoggedIn ? 'Logout' : 'Login'}
        </button>
        <span style={{ fontSize: '13px', color: '#666' }}>
          (Toggle to test the protected Dashboard route)
        </span>
      </div>

      {/* BrowserRouter must wrap everything that uses routing */}
      <BrowserRouter>
        <Routes>
          {/* Layout route: Navbar is shown on ALL pages */}
          <Route element={<Layout />}>
            {/* index route = the default child route (shown at /) */}
            <Route index element={<HomePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/users" element={<UsersPage />} />
            <Route path="/users/:id" element={<UserDetailPage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute isLoggedIn={isLoggedIn}>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />
            {/* Catch-all: any URL not matched above shows the 404 page */}
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </BrowserRouter>

      <footer style={{ backgroundColor: '#f0f0f0', padding: '10px', textAlign: 'center', marginTop: '20px' }}>
        <p>End of Chapter 9 — Next: Full Project App!</p>
      </footer>
    </div>
  );
}

// ---------------------------------------------------------------------------
// CONSOLE LOG TAKEAWAYS
// ---------------------------------------------------------------------------
console.log(`
============================================================
CHAPTER 9 TAKEAWAYS: React Router
============================================================

1. Install: npm install react-router-dom
2. Wrap your app in <BrowserRouter> to enable routing.
3. Define routes with <Routes> and <Route path="..." element={...} />.
4. Navigate with <Link to="/path"> (not <a href>) to avoid page reloads.
5. <NavLink> is like Link but adds active styling.
6. URL parameters: path="/users/:id" → useParams() returns { id }.
7. useNavigate() for programmatic navigation:
   - navigate("/path")     — go to a specific page
   - navigate(-1)          — go back (like browser back button)
8. useSearchParams() for query strings (?key=value).
9. <Outlet /> renders child routes inside a layout (like Jinja blocks).
10. Protected routes: check auth, render <Navigate to="/login" /> if not.
11. 404 page: path="*" catches all unmatched URLs.

FLASK COMPARISON:
   @app.route("/user/<id>")  ←→  <Route path="/user/:id" element={...} />
   request.args.get("q")     ←→  searchParams.get("q")
   redirect(url_for("home")) ←→  navigate("/") or <Navigate to="/" />
   @login_required            ←→  <ProtectedRoute> wrapper component

============================================================
`);

export default Chapter9;
export { Navbar, HomePage, AboutPage, UsersPage, UserDetailPage, SearchPage, NotFoundPage };
