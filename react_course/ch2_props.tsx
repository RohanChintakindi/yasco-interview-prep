// ============================================================================
// CHAPTER 2: PROPS — Passing Data Between Components
// ============================================================================
//
// HOW TO USE THIS FILE:
// 1. Copy this file into your React project's src/ folder
// 2. In src/App.tsx, write:
//      import Chapter2 from './ch2_props';
//      function App() { return <Chapter2 />; }
//      export default App;
// 3. Save and check your browser.
//
// ============================================================================
//
// WHAT ARE PROPS?
// ===============
// Props (short for "properties") are how you pass data FROM a parent component
// TO a child component. They're like function arguments.
//
// COMPARE TO PYTHON:
//   Python function:    def greet(name, age):   ...
//   React component:    function Greet({ name, age })   ...
//
//   Python call:        greet("Chint", 25)
//   React usage:        <Greet name="Chint" age={25} />
//
// The concept is IDENTICAL. Props = arguments. Components = functions.
// The only difference is the syntax: HTML-like attributes instead of
// parentheses.
//
// WHY PROPS?
// ----------
// Components need to be REUSABLE. A Greeting component that always says
// "Hello Chint" is useless. But a Greeting that accepts ANY name via props
// can be used everywhere:
//   <Greeting name="Chint" />
//   <Greeting name="Alice" />
//   <Greeting name="Bob" />
// Same component, different data. That's the power of props.
//
// ============================================================================
//
// PROPS ARE READ-ONLY (ONE-WAY DATA FLOW)
// ========================================
// This is a CRITICAL rule in React: props flow DOWN, never up.
//
//   Parent ──(props)──> Child
//
// A child CANNOT modify its props. If you try, React will throw an error.
// This is called "one-way data flow" or "unidirectional data flow."
//
// WHY? Because if any component could change data anywhere, your app
// becomes impossible to debug. You'd never know WHERE a value changed.
// One-way flow means: if data changed, it changed in the component that
// OWNS that state (more on state in Chapter 3).
//
// So how does a child communicate BACK to the parent?
// Answer: The parent passes a FUNCTION as a prop (a callback).
// The child CALLS that function. We'll see this below.
//
// ============================================================================
//
// TYPING PROPS WITH TYPESCRIPT
// ============================
// TypeScript lets us define EXACTLY what props a component accepts.
// We use an "interface" to describe the shape of props:
//
//   interface GreetingProps {
//     name: string;        // required
//     age?: number;        // optional (the ? makes it optional)
//   }
//
// This gives us autocomplete, error checking, and documentation — all free.
// If someone passes the wrong type, TypeScript catches it BEFORE the code runs.
//
// ============================================================================

import React from 'react';

// ---------------------------------------------------------------------------
// BASIC PROPS: Your first component with props
// ---------------------------------------------------------------------------

// Step 1: Define the shape of the props with a TypeScript interface
interface GreetingProps {
  name: string;          // required — must pass a string
  age?: number;          // optional — the ? means it can be undefined
  isStudent?: boolean;   // optional
}

// Step 2: Use the interface as the type for the function parameter
// We DESTRUCTURE the props object: { name, age, isStudent }
// This is the same as writing: function Greeting(props: GreetingProps)
// and then using props.name, props.age, etc. Destructuring is cleaner.
function Greeting({ name, age, isStudent = false }: GreetingProps) {
  // Notice: isStudent = false gives a DEFAULT VALUE.
  // If the parent doesn't pass isStudent, it defaults to false.
  // Compare to Python: def greeting(name, age=None, is_student=False)

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Hello, {name}!</h3>
      {/* Only show age if it was provided (it's optional) */}
      {age !== undefined && <p>Age: {age}</p>}
      <p>Student: {isStudent ? "Yes" : "No"}</p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// PASSING DIFFERENT TYPES AS PROPS
// ---------------------------------------------------------------------------
// Props can be ANY type: strings, numbers, booleans, arrays, objects,
// functions, even other React components.
// ---------------------------------------------------------------------------

interface UserCardProps {
  username: string;
  email: string;
  avatar?: string;          // optional URL
  skills: string[];         // array of strings
  isActive: boolean;
  joinDate: Date;           // Date object
}

function UserCard({ username, email, avatar, skills, isActive, joinDate }: UserCardProps) {
  return (
    <div style={{
      border: `2px solid ${isActive ? 'green' : 'gray'}`,
      padding: '15px',
      margin: '10px',
      borderRadius: '8px',
      backgroundColor: isActive ? '#f0fff0' : '#f5f5f5'
    }}>
      <h3>{username} {isActive ? "(Active)" : "(Inactive)"}</h3>
      <p>Email: {email}</p>
      {avatar && <img src={avatar} alt={username} style={{ width: 50, height: 50, borderRadius: '50%' }} />}
      <p>Joined: {joinDate.toLocaleDateString()}</p>
      <div>
        <strong>Skills: </strong>
        {/* Map over the array to render each skill */}
        {skills.map((skill, index) => (
          <span key={index} style={{
            backgroundColor: '#e0e0e0',
            padding: '2px 8px',
            margin: '0 4px',
            borderRadius: '4px',
            fontSize: '14px'
          }}>
            {skill}
          </span>
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// CHILDREN PROP: Passing JSX INSIDE a component
// ---------------------------------------------------------------------------
// React has a special prop called "children" — it's whatever you put
// BETWEEN the opening and closing tags of your component.
//
// Compare to Python:
//   In Python, you might use a decorator or wrapper function.
//   In React, you use a "wrapper" component with children.
//
// <Card>
//   <h2>Title</h2>          <-- this is "children"
//   <p>Description</p>      <-- this too
// </Card>
// ---------------------------------------------------------------------------

interface CardProps {
  title: string;
  children: React.ReactNode;   // React.ReactNode = any valid JSX
  // React.ReactNode includes: string, number, JSX, arrays of JSX, null, undefined
  // It's the broadest type for "things React can render."
}

function Card({ title, children }: CardProps) {
  return (
    <div style={{
      border: '1px solid #333',
      borderRadius: '8px',
      overflow: 'hidden',
      margin: '10px',
    }}>
      <div style={{ backgroundColor: '#333', color: 'white', padding: '10px' }}>
        <h3 style={{ margin: 0 }}>{title}</h3>
      </div>
      <div style={{ padding: '15px' }}>
        {/* children renders whatever was put between <Card> and </Card> */}
        {children}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// FUNCTIONS AS PROPS (CALLBACKS) — How child talks to parent
// ---------------------------------------------------------------------------
// The parent passes a function to the child.
// The child CALLS that function when something happens (like a button click).
// This is how data flows BACK UP from child to parent.
//
// Pattern:
//   Parent defines: const handleClick = (message: string) => { ... }
//   Parent passes:  <Child onButtonClick={handleClick} />
//   Child calls:    props.onButtonClick("Hello from child!")
//
// Convention: callback prop names start with "on": onClick, onSubmit, onChange
// ---------------------------------------------------------------------------

interface ButtonProps {
  label: string;
  onClick: () => void;           // function that takes nothing, returns nothing
  variant?: 'primary' | 'secondary' | 'danger';  // union type = limited choices
}

function StyledButton({ label, onClick, variant = 'primary' }: ButtonProps) {
  // Choose color based on variant
  const colorMap: Record<string, string> = {
    primary: '#007bff',
    secondary: '#6c757d',
    danger: '#dc3545',
  };

  return (
    <button
      onClick={onClick}    // When clicked, call the function the parent gave us
      style={{
        backgroundColor: colorMap[variant],
        color: 'white',
        border: 'none',
        padding: '8px 16px',
        borderRadius: '4px',
        cursor: 'pointer',
        margin: '4px',
        fontSize: '14px',
      }}
    >
      {label}
    </button>
  );
}

// ---------------------------------------------------------------------------
// CALLBACK WITH DATA: Child sends information UP to parent
// ---------------------------------------------------------------------------

interface RatingProps {
  maxStars: number;
  onRate: (rating: number) => void;   // callback that sends a number up
}

function RatingPicker({ maxStars, onRate }: RatingProps) {
  // When the user clicks a star, we call onRate with the star number.
  // The PARENT decides what to do with that rating — maybe update state,
  // maybe send it to a server. The child doesn't know or care.
  return (
    <div>
      <p>Click a star to rate:</p>
      {Array.from({ length: maxStars }, (_, i) => i + 1).map(star => (
        <button
          key={star}
          onClick={() => onRate(star)}   // call parent's function with data
          style={{ fontSize: '24px', cursor: 'pointer', background: 'none', border: 'none' }}
        >
          {star <= 3 ? '\u2605' : '\u2606'}
        </button>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// LIFTING STATE UP: The most important pattern in React
// ---------------------------------------------------------------------------
// When two sibling components need to share data, you "lift" the state
// up to their common parent.
//
//   Parent (OWNS the state)
//   /              \
// ChildA          ChildB
// (displays it)   (changes it)
//
// The parent passes the state DOWN to ChildA (as props).
// The parent passes a setState function DOWN to ChildB (as a callback prop).
// When ChildB calls the function, the parent's state updates,
// which re-renders both children with the new data.
//
// We'll implement this fully in Chapter 3 when we learn useState.
// For now, just understand the CONCEPT.
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// PROPS SPREADING: Pass many props at once with the spread operator
// ---------------------------------------------------------------------------
interface ProfileProps {
  name: string;
  email: string;
  role: string;
}

function Profile({ name, email, role }: ProfileProps) {
  return (
    <div style={{ padding: '10px', margin: '10px', border: '1px dashed #999', borderRadius: '6px' }}>
      <strong>{name}</strong> — {email} ({role})
    </div>
  );
}

// ---------------------------------------------------------------------------
// MAIN CHAPTER COMPONENT
// ---------------------------------------------------------------------------
function Chapter2() {
  // Callback handlers (these would normally update state — Chapter 3)
  const handleButtonClick = () => {
    alert("Button clicked! In a real app, this would update state.");
  };

  const handleRate = (rating: number) => {
    alert(`You rated: ${rating} stars! Parent received this from child.`);
  };

  // Props spreading example
  const userData: ProfileProps = {
    name: "Chint",
    email: "chint@example.com",
    role: "Developer",
  };

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>Chapter 2: Props</h1>
      <p><em>Props are how components receive data — like function arguments.</em></p>

      <h2>Basic Props</h2>
      <Greeting name="Chint" age={25} isStudent={true} />
      <Greeting name="Alice" age={30} />
      <Greeting name="Bob" />   {/* age and isStudent will use defaults */}

      <h2>Complex Props (arrays, objects, dates)</h2>
      <UserCard
        username="chint_dev"
        email="chint@example.com"
        skills={["Python", "TypeScript", "React"]}
        isActive={true}
        joinDate={new Date(2024, 0, 15)}
      />

      <h2>Children Prop</h2>
      <Card title="About Children Props">
        <p>Everything between the opening and closing Card tags is "children".</p>
        <p>This lets you create reusable wrapper/layout components.</p>
        <strong>Any JSX works here!</strong>
      </Card>

      <h2>Functions as Props (Callbacks)</h2>
      <StyledButton label="Primary" onClick={handleButtonClick} variant="primary" />
      <StyledButton label="Secondary" onClick={handleButtonClick} variant="secondary" />
      <StyledButton label="Danger" onClick={handleButtonClick} variant="danger" />

      <h2>Callback With Data (Child to Parent)</h2>
      <RatingPicker maxStars={5} onRate={handleRate} />

      <h2>Props Spreading</h2>
      {/* Instead of writing name={userData.name} email={userData.email} ... */}
      {/* We can spread the entire object: */}
      <Profile {...userData} />

      <footer style={{ backgroundColor: '#f0f0f0', padding: '10px', textAlign: 'center', marginTop: '20px' }}>
        <p>End of Chapter 2 — Next: State and useState!</p>
      </footer>
    </div>
  );
}

// ---------------------------------------------------------------------------
// CONSOLE LOG TAKEAWAYS
// ---------------------------------------------------------------------------
console.log(`
============================================================
CHAPTER 2 TAKEAWAYS: Props
============================================================

1. Props = data passed from parent to child (like function arguments).
2. Define prop types with TypeScript interfaces:
     interface Props { name: string; age?: number }
3. Destructure in the function signature:
     function Comp({ name, age = 0 }: Props)
4. Props are READ-ONLY. Never modify props in a child.
5. Data flows ONE WAY: Parent -> Child (via props).
6. Children prop (React.ReactNode): content between <Tag>...</Tag>.
7. Functions as props: how children communicate BACK to parents.
8. Convention: callback props start with "on" (onClick, onSubmit).
9. Spread operator: <Component {...propsObject} /> passes all fields.

PYTHON COMPARISON:
- Props are like function keyword arguments:
    def greet(name: str, age: int = 0) -> str: ...
    greet(name="Chint", age=25)
  Same concept, different syntax.

KEY PATTERN — LIFTING STATE UP:
  When siblings need shared data, lift state to their parent.
  Parent owns the data, children receive it via props.

============================================================
`);

export default Chapter2;
export { Greeting, UserCard, Card, StyledButton, RatingPicker, Profile };
