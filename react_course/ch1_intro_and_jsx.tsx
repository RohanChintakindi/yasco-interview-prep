// ============================================================================
// CHAPTER 1: INTRODUCTION TO REACT AND JSX
// ============================================================================
//
// HOW TO SET UP A REACT PROJECT (DO THIS FIRST!)
// -----------------------------------------------
// You have two main options. Pick ONE:
//
// Option A — Vite (RECOMMENDED, faster):
//   npx create vite@latest myapp -- --template react-ts
//   cd myapp
//   npm install
//   npm run dev
//
// Option B — Create React App (older, still works):
//   npx create-react-app myapp --template typescript
//   cd myapp
//   npm start
//
// Both create a project with React + TypeScript configured and ready.
// Vite is newer and faster for development — use it unless told otherwise.
//
// HOW TO USE THESE CHAPTER FILES:
// 1. Copy this file into your React project's src/ folder
// 2. Open src/App.tsx
// 3. Replace its contents with:
//      import Chapter1 from './ch1_intro_and_jsx';
//      function App() { return <Chapter1 />; }
//      export default App;
// 4. Save and look at your browser — it auto-refreshes!
//
// ============================================================================
//
// WHAT IS REACT?
// ==============
// React is a JavaScript LIBRARY (not a framework) for building user interfaces.
// It was created by Facebook (Meta) and is the most popular way to build
// modern web apps.
//
// The key idea: your UI is made of COMPONENTS. A component is a reusable piece
// of UI — like a button, a header, a card, a whole page. You build small
// components and compose them together like LEGO blocks.
//
// COMPARE TO PYTHON:
// - In Flask, you write HTML templates (Jinja2) separately from your Python code.
//   Your Python route returns render_template("page.html", name="Chint").
//   The HTML and logic live in DIFFERENT files and DIFFERENT languages.
//
// - In React, your components ARE the HTML (sort of). You write what looks like
//   HTML directly inside your JavaScript/TypeScript code. The logic and the UI
//   live TOGETHER in the same file, in the same language. This is called JSX.
//
// WHY does React exist?
// - The DOM (the browser's HTML tree) is slow to update manually.
// - React keeps a "virtual DOM" — a lightweight copy of the real DOM.
// - When data changes, React figures out the MINIMUM changes needed and
//   updates only those parts. This is fast and efficient.
// - You just describe WHAT the UI should look like, and React figures out HOW
//   to update it. This is called "declarative" programming.
//
// ============================================================================
//
// WHAT IS JSX?
// ============
// JSX stands for JavaScript XML. It's a syntax extension that lets you write
// HTML-like code inside JavaScript. It looks like HTML but it's actually
// JavaScript under the hood.
//
// When you write:    <h1>Hello</h1>
// It compiles to:    React.createElement('h1', null, 'Hello')
//
// You never need to write React.createElement yourself — JSX does it for you.
// But knowing this helps you understand that JSX is NOT HTML. It's syntactic
// sugar for function calls.
//
// Since we're using TypeScript, our files end in .tsx (TypeScript + JSX).
// Regular JavaScript React files end in .jsx.
//
// JSX RULES (these trip up EVERYONE at first):
// 1. Must return ONE root element — wrap in a <div> or use a Fragment <></>
// 2. Use className instead of class (because "class" is a reserved word in JS)
// 3. Use htmlFor instead of for (on <label> elements, same reason)
// 4. Self-closing tags MUST have a slash: <img />, <br />, <input />
// 5. All tags must be closed: <div></div>, not just <div>
// 6. JavaScript expressions go inside curly braces: {variable}
//
// ============================================================================
//
// COMPONENTS
// ==========
// A component is just a function that returns JSX. That's it.
//
//   function Welcome() {
//     return <h1>Hello!</h1>;
//   }
//
// Rules for components:
// - The function name MUST start with a Capital letter.
//   <welcome /> = React thinks it's an HTML tag (lowercase = HTML element)
//   <Welcome /> = React knows it's your component (uppercase = component)
// - Must return JSX (or null to render nothing)
// - Can accept "props" (we'll cover those in Chapter 2)
//
// COMPARE TO PYTHON:
//   In Python, a function returns a value:
//     def welcome(): return "Hello!"
//   In React, a component returns UI:
//     function Welcome() { return <h1>Hello!</h1> }
//   The concept is the same — functions that return things — but React
//   functions return UI elements instead of data.
//
// ============================================================================

import React from 'react';

// ---------------------------------------------------------------------------
// Your FIRST component. This is a valid React component.
// It's a function that returns JSX. That's ALL a component is.
// ---------------------------------------------------------------------------
function Welcome() {
  return <h1>Hello, welcome to React!</h1>;
}

// ---------------------------------------------------------------------------
// JSX EXPRESSIONS: Using JavaScript inside JSX
// Anything inside curly braces {} is evaluated as JavaScript.
// ---------------------------------------------------------------------------
function JsxExpressions() {
  const name: string = "Chint";
  const age: number = 25;
  const isStudent: boolean = true;

  return (
    // Rule 1: Must return ONE root element. We use a <div> to wrap everything.
    <div>
      <h2>JSX Expressions Demo</h2>

      {/* This is how you write comments in JSX — curly braces + block comment */}

      {/* Using a variable */}
      <p>Hello, {name}!</p>

      {/* Math expressions */}
      <p>2 + 2 = {2 + 2}</p>
      <p>Age in 10 years: {age + 10}</p>

      {/* String concatenation */}
      <p>{"Hello " + name + ", you are " + age}</p>

      {/* Template literals work great in JSX (backticks inside curly braces) */}
      <p>{`Welcome ${name}, age ${age}`}</p>

      {/* Ternary operator (condition ? if_true : if_false) */}
      <p>{isStudent ? "You are a student" : "You are not a student"}</p>

      {/* Logical AND: shows ONLY if condition is true */}
      {/* If isStudent is true, the <p> renders. If false, nothing renders. */}
      {isStudent && <p>Student discount available!</p>}

      {/* Calling functions */}
      <p>Name uppercase: {name.toUpperCase()}</p>
      <p>Name length: {name.length}</p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// JSX RULES DEMO: All the gotchas in one place
// ---------------------------------------------------------------------------
function JsxRules() {
  const inputId: string = "email-input";

  return (
    <div>
      <h2>JSX Rules Demo</h2>

      {/* Rule: className instead of class */}
      {/* In HTML: <div class="container"> */}
      {/* In JSX: <div className="container"> */}
      <div className="container">
        <p>We use className, not class</p>
      </div>

      {/* Rule: htmlFor instead of for */}
      {/* In HTML: <label for="email"> */}
      {/* In JSX: <label htmlFor="email"> */}
      <label htmlFor={inputId}>Email:</label>
      <input id={inputId} type="email" />

      {/* Rule: Self-closing tags MUST have the slash */}
      {/* In HTML you can write: <img src="photo.jpg"> or <br> or <input> */}
      {/* In JSX you MUST write: <img src="photo.jpg" /> or <br /> or <input /> */}
      <br />
      <img src="" alt="demo - self closing tag required" />
      <input type="text" placeholder="Self-closing with slash" />

      {/* Rule: style takes an OBJECT, not a string */}
      {/* In HTML: <div style="color: red; font-size: 20px"> */}
      {/* In JSX: <div style={{ color: 'red', fontSize: '20px' }}> */}
      {/* Notice: double curly braces {{ }} — outer = JSX expression, inner = object literal */}
      {/* Notice: camelCase instead of kebab-case (fontSize not font-size) */}
      <p style={{ color: 'blue', fontSize: '18px', fontWeight: 'bold' }}>
        Inline styles use objects with camelCase properties
      </p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// FRAGMENTS: Return multiple elements without an extra wrapper <div>
// ---------------------------------------------------------------------------
// Sometimes you don't WANT a wrapper div — it adds an unnecessary element
// to the DOM. Use a Fragment instead: <> ... </>
//
// Fragment is shorthand for <React.Fragment>. It groups elements without
// adding any real DOM node.
// ---------------------------------------------------------------------------
function FragmentDemo() {
  // This returns two <p> elements without wrapping them in a <div>.
  // The <> and </> are the Fragment — they disappear from the final HTML.
  return (
    <>
      <h2>Fragment Demo</h2>
      <p>This paragraph has no wrapper div around it.</p>
      <p>Neither does this one. Inspect the DOM to verify!</p>
    </>
  );
}

// ---------------------------------------------------------------------------
// COMPONENT COMPOSITION: Using components inside other components
// ---------------------------------------------------------------------------
// This is the POWER of React. You build small pieces and snap them together.
// Think of it like Python functions calling other functions.
// ---------------------------------------------------------------------------
function Header() {
  return (
    <header style={{ backgroundColor: '#282c34', color: 'white', padding: '20px', textAlign: 'center' }}>
      <h1>Chapter 1: Intro to React & JSX</h1>
      <p>Learning React step by step</p>
    </header>
  );
}

function Footer() {
  return (
    <footer style={{ backgroundColor: '#f0f0f0', padding: '10px', textAlign: 'center', marginTop: '20px' }}>
      <p>End of Chapter 1 — Next up: Props!</p>
    </footer>
  );
}

// ---------------------------------------------------------------------------
// IMPORTANT: TypeScript + JSX
// ---------------------------------------------------------------------------
// Since we're using .tsx files, TypeScript checks our JSX too.
// If you try to pass a number where a string is expected, TypeScript will
// catch it at compile time — before you even run the code.
// This is a HUGE advantage over plain JavaScript React (.jsx files).
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// CONDITIONAL RENDERING PATTERNS (preview — more in Chapter 6)
// ---------------------------------------------------------------------------
function ConditionalDemo() {
  const isLoggedIn: boolean = true;
  const userName: string | null = "Chint";
  const itemCount: number = 3;

  return (
    <div>
      <h2>Conditional Rendering Preview</h2>

      {/* Pattern 1: Ternary — choose between two things */}
      <p>{isLoggedIn ? "Welcome back!" : "Please log in"}</p>

      {/* Pattern 2: Logical AND — show or hide ONE thing */}
      {userName && <p>Hello, {userName}</p>}

      {/* Pattern 3: Nullish check with ternary */}
      <p>{userName !== null ? `User: ${userName}` : "No user"}</p>

      {/* Pattern 4: Showing counts (careful with 0!) */}
      {/* WARNING: {0 && <p>text</p>} renders "0", not nothing! */}
      {/* Always convert to boolean first: */}
      {itemCount > 0 && <p>You have {itemCount} items</p>}
    </div>
  );
}

// ---------------------------------------------------------------------------
// MAIN CHAPTER COMPONENT
// This is the "root" component for this chapter. It composes all the
// smaller components above into one view. This is the one you import.
// ---------------------------------------------------------------------------
function Chapter1() {
  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <Header />

      <section style={{ marginTop: '20px' }}>
        <h2>Welcome Component</h2>
        <Welcome />
      </section>

      <hr />
      <JsxExpressions />
      <hr />
      <JsxRules />
      <hr />
      <FragmentDemo />
      <hr />
      <ConditionalDemo />

      <Footer />
    </div>
  );
}

// ---------------------------------------------------------------------------
// CONSOLE LOG TAKEAWAYS
// When this file is imported, these will print in the browser console (F12).
// ---------------------------------------------------------------------------
console.log(`
============================================================
CHAPTER 1 TAKEAWAYS: Intro to React & JSX
============================================================

1. React is a library for building UIs with reusable components.
2. A component is just a function that returns JSX.
3. JSX looks like HTML but compiles to React.createElement() calls.
4. JSX rules:
   - Return ONE root element (or use Fragment <></>)
   - className not class
   - htmlFor not for
   - Self-closing tags need a slash: <br />, <img />
5. Curly braces {} let you embed JavaScript expressions in JSX.
6. Component names MUST start with a Capital letter.
7. Components compose: use <MyComponent /> inside other components.
8. TypeScript (.tsx) adds type safety to your JSX.

PYTHON COMPARISON:
- Flask: route returns render_template("page.html", data=data)
- React: component returns <div>{data}</div>
  Both produce HTML, but React keeps logic and UI together.

============================================================
`);

// Default export — this is what gets imported when you write:
// import Chapter1 from './ch1_intro_and_jsx'
export default Chapter1;

// Named exports — you can also import individual components:
// import { Welcome, JsxExpressions } from './ch1_intro_and_jsx'
export { Welcome, JsxExpressions, JsxRules, FragmentDemo, ConditionalDemo };
