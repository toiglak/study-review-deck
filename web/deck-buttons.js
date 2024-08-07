const ADDON_PREFIX = "study_review_deck_buttons_addon";

async function main() {
  let config = await cmd("get_config");

  // Add "Study" and "Review" buttons to each deck.
  let decks = document.querySelectorAll("tr.deck");
  for (var deck of decks) {
    let deck_id = deck.getAttribute("id");

    // Study button.
    var btn = create_button({
      title: "Study",
      onclick: () => cmd("start_study", deck_id),
    });
    var td = create_td();
    td.appendChild(btn);
    deck.insertBefore(td, deck.querySelector(".opts"));

    // Review button.
    var btn = create_button({
      title: "Review",
      onclick: () => cmd("start_review", deck_id),
    });
    var td = create_td();
    td.appendChild(btn);
    deck.insertBefore(td, deck.querySelector(".opts"));
  }

  // Remove "New" column.
  if (config["deck_list_hide_new_column"]) {
    let rows = document.querySelectorAll("tr");
    for (var row of rows) {
      var td = row.cells[1]; // get the second column
      if (td) row.removeChild(td); // remove the second column if it exists
    }
  }

  //
  // Add "Study" and "Review" column headers.

  let header = document.querySelector("tbody > tr");

  var th = document.createElement("th");
  th.innerHTML = "Study";
  header.insertBefore(th, header.querySelector(".optscol"));

  var th = document.createElement("th");
  th.innerHTML = "Review";
  header.insertBefore(th, header.querySelector(".optscol"));
}

on_pycmd_defined(main);

//
// Utility functions.

function create_button({ title, onclick }) {
  let button = document.createElement("button");
  button.innerHTML = title;
  button.onclick = onclick;
  // Prevent buttons from affecting layout when hovered.
  button.style.border = "1px solid transparent";
  button.style.cursor = "pointer";
  return button;
}

function create_td() {
  let td = document.createElement("td");
  let style = td.style;
  style.padding = "0";
  return td;
}

// Prefix string with a unique addon identifier to avoid name collisions.
function pre(string) {
  return `${ADDON_PREFIX}_${string}`;
}

// Send a command to the Anki addon. You can await for the return value.
async function cmd(command, ...arg) {
  return new Promise((resolve, _reject) => {
    pycmd(pre(command) + ":" + arg.join(":"), (ret) => {
      resolve(ret);
    });
  });
}

// Wait for the pycmd function to be defined.
async function on_pycmd_defined(callback) {
  if (typeof pycmd !== "undefined") {
    callback();
    return;
  }

  let called = false;
  let _pycmd;

  Object.defineProperty(globalThis, "pycmd", {
    set(value) {
      _pycmd = value;
      if (!called) {
        callback();
        called = true;
      }
    },
    get() {
      return _pycmd;
    },
  });
}
