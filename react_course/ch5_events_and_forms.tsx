// ============================================================================
// CHAPTER 5: EVENTS AND FORMS — Handling User Input in React
// ============================================================================
//
// HOW TO USE THIS FILE:
// 1. Copy this file into your React project's src/ folder
// 2. In src/App.tsx, write:
//      import Chapter5 from './ch5_events_and_forms';
//      function App() { return <Chapter5 />; }
//      export default App;
// 3. Save and check your browser.
//
// ============================================================================
//
// EVENT HANDLING IN REACT
// =======================
// React wraps browser events in a "SyntheticEvent" system. This means:
// - Events work the same across all browsers (cross-browser compatibility)
// - Event names use camelCase: onClick, onChange, onSubmit (not onclick)
// - You pass a FUNCTION, not a string: onClick={handleClick} (not onclick="handleClick()")
//
// Common events:
//   onClick      — mouse click
//   onChange     — input/select/textarea value changes
//   onSubmit     — form submission
//   onKeyDown    — key pressed down
//   onMouseEnter — mouse enters an element
//   onFocus      — element receives focus
//   onBlur       — element loses focus
//
// COMPARE TO PYTHON/FLASK:
//   In Flask, user input is handled via form submission:
//     @app.route("/submit", methods=["POST"])
//     def submit():
//         name = request.form["name"]   # get input after page submits
//
//   In React, you handle input LIVE as the user types:
//     <input onChange={e => setName(e.target.value)} />
//
//   Flask: user fills form → submits → server processes → new page loads
//   React: user types → state updates instantly → UI re-renders → no page reload
//
// ============================================================================
//
// EVENT TYPES IN TYPESCRIPT
// =========================
// TypeScript needs to know the TYPE of every event. Common ones:
//
//   React.MouseEvent<HTMLButtonElement>        — onClick on buttons
//   React.ChangeEvent<HTMLInputElement>        — onChange on inputs
//   React.ChangeEvent<HTMLSelectElement>       — onChange on selects
//   React.ChangeEvent<HTMLTextAreaElement>     — onChange on textareas
//   React.FormEvent<HTMLFormElement>           — onSubmit on forms
//   React.KeyboardEvent<HTMLInputElement>      — onKeyDown/onKeyUp
//   React.FocusEvent<HTMLInputElement>         — onFocus/onBlur
//
// Don't memorize these — your IDE (VS Code) will suggest them.
// The pattern is: React.{EventType}<HTML{Element}Element>
//
// ============================================================================
//
// CONTROLLED COMPONENTS
// =====================
// A "controlled component" is an input whose value is controlled by React state.
// The input ALWAYS shows what's in state. When you type, onChange updates state,
// and the input re-renders with the new state value.
//
//   const [name, setName] = useState("");
//   <input value={name} onChange={e => setName(e.target.value)} />
//
// WHY "controlled"? Because React is the "single source of truth" for the
// input's value. The input never has a value that React doesn't know about.
// This makes it easy to validate, transform, or reset the input.
//
// The alternative is "uncontrolled" — where the DOM itself holds the value
// and you read it with refs. Controlled is preferred in most cases.
//
// ============================================================================

import React, { useState } from 'react';

// ---------------------------------------------------------------------------
// BASIC EVENT HANDLING: onClick with TypeScript
// ---------------------------------------------------------------------------
function ClickDemo() {
  const [message, setMessage] = useState("Click a button!");
  const [clickCount, setClickCount] = useState(0);

  // Event handler as a named function.
  // React.MouseEvent<HTMLButtonElement> is the TypeScript type for button clicks.
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setClickCount(prev => prev + 1);
    setMessage(`Button clicked at position (${event.clientX}, ${event.clientY})`);
    // event.clientX and clientY are mouse coordinates — from the SyntheticEvent
  };

  // You can also pass data to handlers using arrow functions in JSX
  const handleNamedClick = (name: string) => {
    setMessage(`Hello, ${name}!`);
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Click Events</h3>
      <p>{message} (Total clicks: {clickCount})</p>

      {/* Named handler */}
      <button onClick={handleClick}>Click Me (shows coordinates)</button>

      {/* Inline arrow function — useful when you need to pass arguments */}
      <button onClick={() => handleNamedClick("Chint")} style={{ marginLeft: '8px' }}>
        Greet Chint
      </button>
      <button onClick={() => handleNamedClick("Alice")} style={{ marginLeft: '8px' }}>
        Greet Alice
      </button>

      {/*
        IMPORTANT: onClick={handleClick} passes the FUNCTION itself.
        Do NOT write onClick={handleClick()} — that would CALL the function
        during render, not on click! The () means "call now."

        If you need to pass arguments, wrap in an arrow function:
        onClick={() => handleClick("arg")}
      */}
    </div>
  );
}

// ---------------------------------------------------------------------------
// CONTROLLED INPUT: Text input tied to state
// ---------------------------------------------------------------------------
function ControlledInput() {
  const [text, setText] = useState("");

  // The event type for onChange on an <input> element
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    // event.target is the input element itself
    // event.target.value is what the user typed
    setText(event.target.value);
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Controlled Input</h3>
      <input
        type="text"
        value={text}           // value comes FROM state
        onChange={handleChange}  // onChange updates state
        placeholder="Type something..."
        style={{ padding: '8px', fontSize: '16px', width: '300px' }}
      />
      <p>You typed: <strong>{text}</strong></p>
      <p>Character count: {text.length}</p>
      <p>Uppercase: {text.toUpperCase()}</p>

      {/*
        The "controlled" flow:
        1. User types "H"
        2. onChange fires with event.target.value = "H"
        3. setText("H") updates state
        4. React re-renders — input shows "H" from state
        5. User types "i" → event.target.value = "Hi"
        6. setText("Hi") → re-render → input shows "Hi"

        At every moment, the input's value === the state value.
        React is the single source of truth.
      */}
    </div>
  );
}

// ---------------------------------------------------------------------------
// FORM SUBMISSION: onSubmit with preventDefault
// ---------------------------------------------------------------------------
interface FormData {
  name: string;
  email: string;
  message: string;
}

function ContactForm() {
  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    message: "",
  });
  const [submitted, setSubmitted] = useState(false);

  // Generic handler for multiple inputs — uses the input's "name" attribute
  // to know WHICH field to update. This avoids writing a separate handler
  // for each input.
  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = event.target;
    // name is the "name" attribute of the input (e.g., "email")
    // value is what the user typed

    setFormData(prev => ({
      ...prev,        // keep all other fields
      [name]: value,  // update just this one field
      // [name] is a "computed property name" — the key is dynamic
      // If name is "email", this becomes { ...prev, email: value }
    }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    // preventDefault stops the browser's default form behavior
    // (which would reload the page — we don't want that in React!)
    event.preventDefault();

    console.log("Form submitted:", formData);
    setSubmitted(true);

    // In a real app, you'd send this data to a server:
    // await fetch('/api/contact', { method: 'POST', body: JSON.stringify(formData) })
  };

  if (submitted) {
    return (
      <div style={{ border: '1px solid green', padding: '15px', margin: '10px', borderRadius: '8px' }}>
        <h3>Contact Form — Submitted!</h3>
        <p>Name: {formData.name}</p>
        <p>Email: {formData.email}</p>
        <p>Message: {formData.message}</p>
        <button onClick={() => { setSubmitted(false); setFormData({ name: "", email: "", message: "" }); }}>
          Send Another
        </button>
      </div>
    );
  }

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Contact Form (onSubmit + preventDefault)</h3>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="name">Name: </label>
          <input
            id="name"
            name="name"              // This "name" attribute is used by handleChange
            type="text"
            value={formData.name}
            onChange={handleChange}
            required
            style={{ padding: '6px', marginLeft: '8px' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="email">Email: </label>
          <input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            required
            style={{ padding: '6px', marginLeft: '8px' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="message">Message: </label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            required
            rows={3}
            style={{ padding: '6px', marginLeft: '8px', verticalAlign: 'top', width: '300px' }}
          />
        </div>
        <button type="submit" style={{ padding: '8px 16px', fontSize: '16px' }}>
          Submit
        </button>
      </form>
    </div>
  );
}

// ---------------------------------------------------------------------------
// SELECT, CHECKBOX, and RADIO: Different input types
// ---------------------------------------------------------------------------
function VariousInputs() {
  const [color, setColor] = useState("blue");
  const [agreed, setAgreed] = useState(false);
  const [size, setSize] = useState("medium");

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Select, Checkbox, and Radio Inputs</h3>

      {/* SELECT: value is the selected option's value */}
      <div style={{ marginBottom: '10px' }}>
        <label htmlFor="color-select">Favorite Color: </label>
        <select
          id="color-select"
          value={color}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setColor(e.target.value)}
          style={{ padding: '6px' }}
        >
          <option value="red">Red</option>
          <option value="blue">Blue</option>
          <option value="green">Green</option>
          <option value="purple">Purple</option>
        </select>
        <span style={{ marginLeft: '10px', color: color, fontWeight: 'bold' }}>
          Selected: {color}
        </span>
      </div>

      {/* CHECKBOX: uses "checked" instead of "value" */}
      <div style={{ marginBottom: '10px' }}>
        <label>
          <input
            type="checkbox"
            checked={agreed}     // "checked" not "value" for checkboxes!
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setAgreed(e.target.checked)}
            // e.target.checked is a boolean (true/false), not e.target.value
          />
          {' '}I agree to the terms
        </label>
        <span style={{ marginLeft: '10px' }}>
          {agreed ? "Agreed!" : "Not yet agreed"}
        </span>
      </div>

      {/* RADIO BUTTONS: group by same "name", each has different "value" */}
      <div style={{ marginBottom: '10px' }}>
        <p style={{ margin: '0 0 5px 0' }}>Size:</p>
        {["small", "medium", "large"].map(s => (
          <label key={s} style={{ marginRight: '15px' }}>
            <input
              type="radio"
              name="size"                    // Same name = same radio group
              value={s}
              checked={size === s}           // Controlled: checked when state matches
              onChange={(e) => setSize(e.target.value)}
            />
            {' '}{s.charAt(0).toUpperCase() + s.slice(1)}
          </label>
        ))}
        <span style={{ marginLeft: '10px' }}>Selected: {size}</span>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// FORM VALIDATION: Simple validation with error messages
// ---------------------------------------------------------------------------
function ValidatedForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  const [success, setSuccess] = useState(false);

  const validate = (): boolean => {
    const newErrors: { email?: string; password?: string } = {};

    // Email validation
    if (!email) {
      newErrors.email = "Email is required";
    } else if (!email.includes("@")) {
      newErrors.email = "Email must contain @";
    }

    // Password validation
    if (!password) {
      newErrors.password = "Password is required";
    } else if (password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }

    setErrors(newErrors);
    // Return true if no errors (empty object = valid)
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (validate()) {
      setSuccess(true);
      console.log("Form is valid! Submitting:", { email, password });
    }
  };

  if (success) {
    return (
      <div style={{ border: '1px solid green', padding: '15px', margin: '10px', borderRadius: '8px' }}>
        <h3>Form Validated!</h3>
        <p>Email: {email}</p>
        <button onClick={() => { setSuccess(false); setEmail(""); setPassword(""); }}>
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Form Validation</h3>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <input
            type="text"
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            style={{
              padding: '8px',
              border: errors.email ? '2px solid red' : '1px solid #ccc',
              borderRadius: '4px',
              width: '250px',
            }}
          />
          {errors.email && (
            <p style={{ color: 'red', fontSize: '13px', margin: '4px 0 0 0' }}>{errors.email}</p>
          )}
        </div>
        <div style={{ marginBottom: '10px' }}>
          <input
            type="password"
            placeholder="Password (min 6 chars)"
            value={password}
            onChange={e => setPassword(e.target.value)}
            style={{
              padding: '8px',
              border: errors.password ? '2px solid red' : '1px solid #ccc',
              borderRadius: '4px',
              width: '250px',
            }}
          />
          {errors.password && (
            <p style={{ color: 'red', fontSize: '13px', margin: '4px 0 0 0' }}>{errors.password}</p>
          )}
        </div>
        <button type="submit" style={{ padding: '8px 16px' }}>Login</button>
      </form>
    </div>
  );
}

// ---------------------------------------------------------------------------
// KEYBOARD EVENTS: onKeyDown
// ---------------------------------------------------------------------------
function KeyboardDemo() {
  const [lastKey, setLastKey] = useState("(none)");
  const [pressedKeys, setPressedKeys] = useState<string[]>([]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    setLastKey(e.key);
    setPressedKeys(prev => [...prev.slice(-9), e.key]); // Keep last 10 keys

    // Example: do something on Enter
    if (e.key === 'Enter') {
      console.log("Enter was pressed!");
    }

    // Example: Ctrl+K shortcut
    if (e.ctrlKey && e.key === 'k') {
      e.preventDefault(); // Prevent browser's default Ctrl+K behavior
      console.log("Ctrl+K pressed!");
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px', borderRadius: '8px' }}>
      <h3>Keyboard Events</h3>
      <input
        type="text"
        placeholder="Type here to see key events..."
        onKeyDown={handleKeyDown}
        style={{ padding: '8px', fontSize: '16px', width: '300px' }}
      />
      <p>Last key: <strong>{lastKey}</strong></p>
      <p>Recent keys: <code>{pressedKeys.join(', ')}</code></p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// MAIN CHAPTER COMPONENT
// ---------------------------------------------------------------------------
function Chapter5() {
  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>Chapter 5: Events & Forms</h1>
      <p><em>React handles user input with controlled components and event handlers.</em></p>

      <ClickDemo />
      <hr />
      <ControlledInput />
      <hr />
      <ContactForm />
      <hr />
      <VariousInputs />
      <hr />
      <ValidatedForm />
      <hr />
      <KeyboardDemo />

      <footer style={{ backgroundColor: '#f0f0f0', padding: '10px', textAlign: 'center', marginTop: '20px' }}>
        <p>End of Chapter 5 — Next: Lists and Conditional Rendering!</p>
      </footer>
    </div>
  );
}

// ---------------------------------------------------------------------------
// CONSOLE LOG TAKEAWAYS
// ---------------------------------------------------------------------------
console.log(`
============================================================
CHAPTER 5 TAKEAWAYS: Events & Forms
============================================================

1. Event names are camelCase: onClick, onChange, onSubmit.
2. Pass functions, not calls: onClick={handler} NOT onClick={handler()}.
3. TypeScript event types:
   - React.MouseEvent<HTMLButtonElement>
   - React.ChangeEvent<HTMLInputElement>
   - React.FormEvent<HTMLFormElement>
4. Controlled components: input value comes from state.
     <input value={state} onChange={e => setState(e.target.value)} />
5. Form submission: onSubmit + e.preventDefault()
   (prevents page reload — React handles everything client-side).
6. Multiple inputs: use a single handler + input "name" attribute:
     const { name, value } = e.target;
     setForm(prev => ({ ...prev, [name]: value }));
7. Checkbox: use "checked" not "value", and e.target.checked (boolean).
8. Validation: check fields on submit, show error messages from state.

FLASK vs REACT FORMS:
   Flask: HTML form → POST request → server validates → redirect/render
   React: Controlled inputs → state updates live → validate in JS → fetch API

============================================================
`);

export default Chapter5;
export { ClickDemo, ControlledInput, ContactForm, VariousInputs, ValidatedForm, KeyboardDemo };
