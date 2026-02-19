/*
=====================================================
 CHAPTER 5: DOM MANIPULATION & EVENTS
=====================================================

IMPORTANT NOTE:
  This chapter covers browser-only concepts. The DOM (Document Object
  Model) is how JavaScript interacts with HTML web pages. This code
  CANNOT run with "node ch5_dom_and_events.js" because Node.js doesn't
  have a browser or DOM.

  Instead, this file teaches DOM concepts with extensive comments, and
  includes a COMPLETE HTML file you can save and open in your browser.

WHAT IS THE DOM?
  When a browser loads an HTML page, it creates a tree structure in memory
  called the DOM. Each HTML element becomes a "node" in this tree.

  Think of it like this:
    HTML file = the blueprint (source code)
    DOM       = the actual building (live in memory, can be changed)

  Python analogy: The DOM is like a nested dictionary representing the page.
  JavaScript lets you read and modify this dictionary, and the browser
  instantly reflects the changes visually.

WHY DOES THIS MATTER?
  Every interactive website you've ever used - clicking buttons, typing
  in forms, dropdown menus, animations - all of that is JavaScript
  manipulating the DOM and listening for events.


HOW TO USE THIS CHAPTER:
  1. Read through this file to learn the concepts
  2. Copy the HTML block below into a file called "ch5_demo.html"
  3. Open ch5_demo.html in your browser
  4. Open the browser console (F12 or right-click -> Inspect -> Console)
  5. Try the JavaScript commands there!


COMPLETE HTML FILE (save as ch5_demo.html):
============================================

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ch5: DOM & Events Demo</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }
        h1 { color: #333; }
        .highlight { background-color: yellow; padding: 2px 6px; }
        .big { font-size: 24px; font-weight: bold; }
        .red { color: red; }
        .box { padding: 20px; margin: 10px 0; border: 2px solid #ccc; border-radius: 8px; }
        .active { border-color: blue; background-color: #e6f3ff; }
        button { padding: 8px 16px; margin: 5px; cursor: pointer; font-size: 14px; }
        input { padding: 8px; margin: 5px; font-size: 14px; }
        #output { min-height: 30px; padding: 10px; background: #f0f0f0; margin: 10px 0; }
        ul { list-style: none; padding: 0; }
        li { padding: 8px; margin: 4px 0; background: #f9f9f9; border-radius: 4px; }
    </style>
</head>
<body>
    <h1 id="main-title">DOM & Events Demo</h1>
    <p id="intro">This page demonstrates JavaScript DOM manipulation.</p>

    <div class="box" id="demo-box">
        <p>This is a demo box. Click the buttons below to change it.</p>
    </div>

    <div>
        <button id="btn-change-text">Change Text</button>
        <button id="btn-change-style">Change Style</button>
        <button id="btn-toggle-class">Toggle Active</button>
        <button id="btn-add-element">Add Item</button>
    </div>

    <div>
        <input type="text" id="text-input" placeholder="Type something...">
        <span id="char-count">0 characters</span>
    </div>

    <div id="output">Output will appear here</div>

    <ul id="item-list">
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </ul>

    <script>
        // ============================================================
        // SELECTING ELEMENTS
        // ============================================================

        // querySelector: select ONE element (first match)
        // Like document.getElementById but more flexible - uses CSS selectors
        const title = document.querySelector('#main-title');    // By ID
        const intro = document.querySelector('p');              // By tag (first <p>)
        const box = document.querySelector('.box');             // By class

        // querySelectorAll: select ALL matching elements (returns NodeList)
        const allButtons = document.querySelectorAll('button');
        const allListItems = document.querySelectorAll('li');

        console.log('Title element:', title);
        console.log('All buttons:', allButtons);         // NodeList (like an array)
        console.log('Button count:', allButtons.length);

        // ============================================================
        // CHANGING TEXT
        // ============================================================

        // textContent: get/set the text (safe, strips HTML)
        console.log('Title text:', title.textContent);

        // innerHTML: get/set HTML (can include tags - be careful with user input!)
        // Use textContent for plain text, innerHTML only when you need HTML tags.

        // ============================================================
        // CHANGING STYLES
        // ============================================================

        // Direct style: element.style.propertyName = value
        // CSS property names use camelCase in JS:
        //   CSS: background-color  ->  JS: backgroundColor
        //   CSS: font-size         ->  JS: fontSize

        // ============================================================
        // CLASSES: add, remove, toggle
        // ============================================================

        // element.classList.add('classname')
        // element.classList.remove('classname')
        // element.classList.toggle('classname')  // Add if missing, remove if present
        // element.classList.contains('classname')  // Check if has class

        // ============================================================
        // CREATING & REMOVING ELEMENTS
        // ============================================================

        // document.createElement('tag')  -> create a new element
        // parent.appendChild(child)      -> add child to end of parent
        // parent.removeChild(child)      -> remove child from parent
        // element.remove()               -> remove element from DOM

        // ============================================================
        // EVENT LISTENERS - THE CORE OF INTERACTIVITY
        // ============================================================

        // element.addEventListener('eventName', handlerFunction)
        //
        // Common events:
        //   'click'            -> user clicks element
        //   'dblclick'         -> user double-clicks
        //   'mouseover'        -> mouse enters element
        //   'mouseout'         -> mouse leaves element
        //   'keydown'          -> user presses a key
        //   'keyup'            -> user releases a key
        //   'input'            -> user types in an input field
        //   'submit'           -> form is submitted
        //   'change'           -> input value changed (after losing focus)
        //   'DOMContentLoaded' -> HTML fully loaded and parsed
        //   'load'             -> page and all resources loaded

        // --- Button: Change Text ---
        const btnText = document.querySelector('#btn-change-text');
        btnText.addEventListener('click', () => {
            const output = document.querySelector('#output');
            output.textContent = 'Text was changed at ' + new Date().toLocaleTimeString();
        });

        // --- Button: Change Style ---
        const btnStyle = document.querySelector('#btn-change-style');
        btnStyle.addEventListener('click', () => {
            const output = document.querySelector('#output');
            output.style.color = 'white';
            output.style.backgroundColor = '#333';
            output.style.padding = '20px';
            output.style.borderRadius = '8px';
        });

        // --- Button: Toggle Class ---
        const btnToggle = document.querySelector('#btn-toggle-class');
        btnToggle.addEventListener('click', () => {
            box.classList.toggle('active');
            console.log('Box has active class:', box.classList.contains('active'));
        });

        // --- Button: Add Element ---
        let itemCount = 3;
        const btnAdd = document.querySelector('#btn-add-element');
        btnAdd.addEventListener('click', () => {
            itemCount++;
            const newItem = document.createElement('li');
            newItem.textContent = 'Item ' + itemCount + ' (added dynamically!)';
            document.querySelector('#item-list').appendChild(newItem);
        });

        // --- Input: Character Counter ---
        const textInput = document.querySelector('#text-input');
        const charCount = document.querySelector('#char-count');
        textInput.addEventListener('input', (e) => {
            // e is the Event object - contains info about what happened
            // e.target is the element that triggered the event
            const count = e.target.value.length;
            charCount.textContent = count + ' characters';
        });

        // --- Event Object Details ---
        document.addEventListener('click', (e) => {
            console.log('Click event details:');
            console.log('  Target:', e.target.tagName);    // What was clicked
            console.log('  X:', e.clientX, 'Y:', e.clientY); // Mouse position
        });

        // --- Keyboard Events ---
        document.addEventListener('keydown', (e) => {
            console.log('Key pressed:', e.key, 'Code:', e.code);
            if (e.key === 'Escape') {
                document.querySelector('#output').textContent = 'You pressed Escape!';
            }
        });

        // --- DOMContentLoaded (runs when HTML is ready) ---
        // This is already inside a <script> at the end of <body>,
        // so the DOM is already loaded. But for scripts in <head>:
        // document.addEventListener('DOMContentLoaded', () => {
        //     console.log('DOM is ready!');
        // });

        console.log('Ch5 Demo loaded! Click buttons and type to see DOM manipulation.');
    </script>
</body>
</html>

============================================
END OF HTML FILE
*/


// =============================================================================
// RUNNABLE NODE.JS SECTION
// =============================================================================
//
// Since this file runs in Node.js, we'll demonstrate the concepts by
// printing explanations and showing what each DOM method does.

console.log("=".repeat(60));
console.log("CHAPTER 5: DOM & EVENTS - Concept Reference");
console.log("=".repeat(60));
console.log();
console.log("NOTE: DOM code runs in the BROWSER, not Node.js.");
console.log("Save the HTML from the top of this file as 'ch5_demo.html'");
console.log("and open it in your browser to see it in action.");
console.log();


// =============================================================================
// CONCEPT 1: SELECTING ELEMENTS
// =============================================================================

console.log("=".repeat(50));
console.log("CONCEPT 1: Selecting Elements");
console.log("=".repeat(50));

console.log(`
  querySelector('#id')        -> Select by ID (like Python: dict['key'])
  querySelector('.class')     -> Select by CSS class
  querySelector('tag')        -> Select by HTML tag
  querySelector('div.box')    -> Select by combo (tag + class)
  querySelectorAll('li')      -> Select ALL matches (returns list)

  OLD WAYS (still work but querySelector is preferred):
  getElementById('id')         -> By ID only
  getElementsByClassName('c')  -> By class (returns live collection)
  getElementsByTagName('div')  -> By tag (returns live collection)

  PYTHON ANALOGY:
    querySelector is like soup.find() in BeautifulSoup
    querySelectorAll is like soup.find_all()
`);


// =============================================================================
// CONCEPT 2: MODIFYING ELEMENTS
// =============================================================================

console.log("=".repeat(50));
console.log("CONCEPT 2: Modifying Elements");
console.log("=".repeat(50));

console.log(`
  CHANGING TEXT:
    element.textContent = "New text"     // Safe (plain text only)
    element.innerHTML = "<b>Bold</b>"    // Can include HTML (careful!)

  CHANGING STYLES:
    element.style.color = "red"
    element.style.backgroundColor = "#333"    // camelCase, not kebab-case!
    element.style.fontSize = "20px"

  CHANGING CLASSES (preferred over direct style):
    element.classList.add("active")
    element.classList.remove("active")
    element.classList.toggle("active")    // Add if missing, remove if present
    element.classList.contains("active")  // Returns true/false

  CHANGING ATTRIBUTES:
    element.setAttribute("href", "https://example.com")
    element.getAttribute("href")
    element.removeAttribute("disabled")

  PYTHON ANALOGY:
    Changing textContent is like modifying a dict value
    Classes are like adding/removing tags from a set
`);


// =============================================================================
// CONCEPT 3: CREATING AND REMOVING ELEMENTS
// =============================================================================

console.log("=".repeat(50));
console.log("CONCEPT 3: Creating & Removing Elements");
console.log("=".repeat(50));

console.log(`
  CREATE:
    const newDiv = document.createElement("div")
    newDiv.textContent = "I'm new!"
    newDiv.classList.add("highlight")

  ADD TO PAGE:
    parent.appendChild(newDiv)              // Add at end
    parent.insertBefore(newDiv, reference)  // Add before specific element
    parent.prepend(newDiv)                  // Add at beginning

  REMOVE:
    element.remove()                  // Remove element from DOM
    parent.removeChild(childElement)  // Remove specific child

  PYTHON ANALOGY:
    Like list.append() to add and list.remove() to delete
    But instead of a list, you're modifying a tree of HTML nodes
`);


// =============================================================================
// CONCEPT 4: EVENT LISTENERS
// =============================================================================

console.log("=".repeat(50));
console.log("CONCEPT 4: Event Listeners");
console.log("=".repeat(50));

console.log(`
  ADDING EVENT LISTENERS:
    element.addEventListener("click", (event) => {
        console.log("Clicked!", event.target);
    });

  THE EVENT OBJECT (e or event):
    e.target          -> The element that was clicked/interacted with
    e.currentTarget   -> The element the listener is attached to
    e.preventDefault() -> Stop default behavior (e.g., form submit reload)
    e.stopPropagation() -> Stop event from bubbling up to parent elements
    e.key             -> Which key was pressed (for keyboard events)
    e.clientX / e.clientY -> Mouse coordinates

  COMMON EVENTS:
    "click"            -> Mouse click
    "dblclick"         -> Double click
    "submit"           -> Form submission
    "input"            -> User typing in input field (fires on every keystroke)
    "change"           -> Input value changed (fires when focus leaves)
    "keydown"          -> Key pressed down
    "keyup"            -> Key released
    "mouseover"        -> Mouse enters element
    "mouseout"         -> Mouse leaves element
    "scroll"           -> Page scrolled
    "DOMContentLoaded" -> HTML loaded and parsed (use this!)
    "load"             -> Everything loaded (images, styles, etc.)

  REMOVING EVENT LISTENERS:
    // Must use a named function (not anonymous arrow function)
    function handleClick(e) { console.log("clicked"); }
    element.addEventListener("click", handleClick);
    element.removeEventListener("click", handleClick);

  PYTHON ANALOGY:
    Event listeners are like callbacks in GUI frameworks (Tkinter, PyQt).
    tkinter: button.bind("<Button-1>", handler)
    JS:      button.addEventListener("click", handler)
`);


// =============================================================================
// CONCEPT 5: EVENT BUBBLING AND DELEGATION
// =============================================================================

console.log("=".repeat(50));
console.log("CONCEPT 5: Event Bubbling & Delegation");
console.log("=".repeat(50));

console.log(`
  EVENT BUBBLING:
    When you click a button inside a div inside the body,
    the click event fires on the button, THEN the div, THEN the body.
    It "bubbles up" from the target to the root.

    <body>              <- click event reaches here (3rd)
      <div>             <- click event reaches here (2nd)
        <button>Click   <- click event starts here (1st)

  EVENT DELEGATION:
    Instead of adding a listener to EVERY list item, add ONE listener
    to the parent <ul> and check which child was clicked:

    document.querySelector("ul").addEventListener("click", (e) => {
        if (e.target.tagName === "LI") {
            console.log("Clicked:", e.target.textContent);
        }
    });

    This is more efficient and works with dynamically added elements!
`);


// =============================================================================
// CONCEPT 6: PREVENTING DEFAULT BEHAVIOR
// =============================================================================

console.log("=".repeat(50));
console.log("CONCEPT 6: Preventing Defaults");
console.log("=".repeat(50));

console.log(`
  Some elements have default behaviors:
    - <a> links navigate to a URL
    - <form> submits and reloads the page
    - Right-click shows a context menu

  e.preventDefault() stops these:

    // Prevent form reload (VERY common):
    form.addEventListener("submit", (e) => {
        e.preventDefault();  // Stop page reload!
        const data = new FormData(form);
        console.log("Form data:", Object.fromEntries(data));
    });

    // Prevent link navigation:
    link.addEventListener("click", (e) => {
        e.preventDefault();
        console.log("Link click intercepted!");
    });
`);

console.log();
console.log("=".repeat(60));
console.log("Remember: Save the HTML from the top of this file as");
console.log("'ch5_demo.html' and open it in your browser to practice!");
console.log("=".repeat(60));
